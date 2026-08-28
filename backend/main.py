"""Car dimensions comparison API backend (FastAPI, pure Python + NumPy)."""
from fastapi import FastAPI
from sqlite3 import connect
from pathlib import Path
import sqlite3
import json
import base64
import numpy as np
from fastapi.staticfiles import StaticFiles
from silhouette_generator import generate_side_profile_svg
from seed_db import seed_database

app = FastAPI(title="Indian Car Visual Comparator API")


def get_engine():
    """Get SQLite database engine with inline schema."""
    db_path = "cars.db"
    
    conn = connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            length REAL NOT NULL,
            width REAL NOT NULL,
            height REAL NOT NULL,
            wheelbase REAL NOT NULL,
            side_view_url TEXT DEFAULT '',
            front_view_url TEXT DEFAULT '',
            rear_view_url TEXT DEFAULT '',
            description TEXT DEFAULT ''
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comparisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_a_id INTEGER NOT NULL REFERENCES cars(id),
            car_b_id INTEGER NOT NULL REFERENCES cars(id),
            thumbnail_url TEXT DEFAULT '',
            comparison_data_json TEXT DEFAULT '',
            FOREIGN KEY (car_a_id) REFERENCES cars(id),
            FOREIGN KEY (car_b_id) REFERENCES cars(id)
        )
    """)
    
    conn.commit()
    return conn


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}



@app.get("/cars")
async def list_cars(search: str | None = None, make: str | None = None):
    """List all cars with optional filtering."""
    conn = get_engine()
    try:
        cursor = conn.cursor()
        
        if search and make:
            query = "SELECT id, make, model, year, length, width, height, wheelbase FROM cars WHERE (make LIKE ? OR model LIKE ?) AND make LIKE ? ORDER BY year DESC, make, model"
            params = (f"%{search}%", f"%{search}%", f"%{make}%")
        elif search:
            query = "SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?"
            params = (f"%{search}%", f"%{search}%")
        elif make:
            query = "SELECT * FROM cars WHERE make LIKE ?"
            params = (f"%{make}%",)
        else:
            query = "SELECT id, make, model, year, length, width, height, wheelbase FROM cars ORDER BY year DESC, make, model"
            params = ()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [
            {
                "id": row[0],
                "make": row[1],
                "model": row[2],
                "year": row[3],
                "length": row[4],
                "width": row[5],
                "height": row[6],
                "wheelbase": row[7],
            }
            for row in rows
        ]
    finally:
        conn.close()


@app.get("/cars/{car_id}")
async def get_car(car_id: int):
    """Get a single car by ID."""
    conn = get_engine()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, make, model, year, length, width, height, wheelbase FROM cars WHERE id = ?",
            (car_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return {"error": "Car not found"}, 404
        
        return {
            "id": row[0],
            "make": row[1],
            "model": row[2],
            "year": row[3],
            "length": row[4],
            "width": row[5],
            "height": row[6],
            "wheelbase": row[7],
        }
    finally:
        conn.close()


@app.get("/svg/{car_id}")
async def get_car_svg(car_id: int):
    """Generate SVG silhouette for a car."""
    conn = get_engine()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT make, model, length, width, height, wheelbase FROM cars WHERE id = ?",
            (car_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return {"error": "Car not found"}, 404
        
        # Unpack row into separate parameters for generate_side_profile_svg
        svg_result = generate_side_profile_svg(
            make=row[0], model=row[1], length_mm=row[2],
            height_mm=row[4], wheelbase_mm=row[5], width_mm=row[3]
        )
        
        return {
            "id": car_id,
            "svg": svg_result["svg_data"]
        }
    finally:
        conn.close()


# LRU cache for comparison results
_CACHE_SIZE = 100
_cache = {}


def simple_lru_get(key):
    """Simple LRU get."""
    if key in _cache:
        value, timestamp = _cache[key]
        if timestamp > 3600:  # Cache valid for 1 hour
            return value
        else:
            del _cache[key]
    return None


def simple_lru_set(key, value):
    """Simple LRU set."""
    global _cache
    if len(_cache) >= _CACHE_SIZE:
        oldest_key = min(_cache.keys(), key=lambda k: _cache[k][0])
        del _cache[oldest_key]
    _cache[key] = (datetime.now().timestamp(), value)


from datetime import datetime


@app.get("/compare/{car_a_id}/{car_b_id}")
async def compare_cars(car_a_id: int, car_b_id: int):
    """Compare two cars side-by-side."""
    conn = get_engine()
    try:
        cursor = conn.cursor()
        
        # Get car A
        cursor.execute(
            "SELECT id, make, model, year, length, width, height, wheelbase FROM cars WHERE id = ?",
            (car_a_id,)
        )
        row_a = cursor.fetchone()
        if not row_a:
            return {"error": "Car A not found"}, 404
        
        # Get car B
        cursor.execute(
            "SELECT id, make, model, year, length, width, height, wheelbase FROM cars WHERE id = ?",
            (car_b_id,)
        )
        row_b = cursor.fetchone()
        if not row_b:
            return {"error": "Car B not found"}, 404
        
        car_a = {
            "id": row_a[0],
            "make": row_a[1],
            "model": row_a[2],
            "year": row_a[3],
            "length": row_a[4],
            "width": row_a[5],
            "height": row_a[6],
            "wheelbase": row_a[7],
        }
        
        car_b = {
            "id": row_b[0],
            "make": row_b[1],
            "model": row_b[2],
            "year": row_b[3],
            "length": row_b[4],
            "width": row_b[5],
            "height": row_b[6],
            "wheelbase": row_b[7],
        }
        
        # Generate SVGs
        svg_a = generate_side_profile_svg(
            make=car_a["make"], model=car_a["model"], length_mm=car_a["length"],
            height_mm=car_a["height"], wheelbase_mm=car_a["wheelbase"], width_mm=car_a["width"]
        )
        svg_b = generate_side_profile_svg(
            make=car_b["make"], model=car_b["model"], length_mm=car_b["length"],
            height_mm=car_b["height"], wheelbase_mm=car_b["wheelbase"], width_mm=car_b["width"]
        )
        
        # Prepare comparison data (will be cached as JSON string for persistence)
        comparison_data = {
            "car_a": car_a,
            "car_b": car_b,
            "svg_a": svg_a["svg_data"],
            "svg_b": svg_b["svg_data"],
        }
        
        # Check cache first
        cache_key = f"{car_a_id}_{car_b_id}"
        cached = simple_lru_get(cache_key)
        if cached:
            return {"cached": True, **json.loads(cached)}
        
        # Store in database (JSON for persistence)
        cursor.execute(
            "INSERT INTO comparisons (car_a_id, car_b_id, comparison_data_json) VALUES (?, ?, ?)",
            (car_a_id, car_b_id, json.dumps(comparison_data))
        )
        conn.commit()
        
        # Cache the result
        simple_lru_set(cache_key, json.dumps(comparison_data))
        
        return comparison_data
        
    finally:
        conn.close()


@app.on_event("startup")
async def startup_event():
    """Seed database on startup."""
    conn = get_engine()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cars")
        if cursor.fetchone()[0] == 0:
            seed_database()
    finally:
        conn.close()


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent.parent / "frontend", html=True),
    name="frontend",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
