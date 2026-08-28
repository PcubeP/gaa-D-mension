# 🚗 Indian Car Visual Comparator

**Compare car dimensions side-by-side** to visualize size differences between popular Indian vehicles.

## ✨ Features

- **FastAPI Backend** serving:
  - `GET /health` — Health check
  - `GET /` — Serves the web UI
  - `GET /cars` — List all cars with filtering (search by make/model)
  - `GET /svg/{car_id}` — Generate SVG silhouette for a specific car
  - `GET /compare/{car_a_id}/{car_b_id}` — Compare two cars side-by-side
  
- **Vanilla JavaScript Frontend** with:
  - Debounced search input for filtering
  - Side-by-side/overlay comparison modes
  - Canvas rendering with transparency control
  - Color-coded dimension difference stats (green ≤50mm, red >50mm)

- **SQLite Database** automatically seeded on startup with 48 records of Indian cars.

- **SVG Silhouette Generator** using NumPy for geometric path approximation.

## 🛠️ Quick Start

```bash
# From root directory: E:\Coding\dev\GaaDimension

cd backend
# Activate venv (optional if already active)
\.venv\Scripts\activate  
# Start the server
uvicorn main:app --host 127.0.0.1 --port 8002
```

Then open `http://127.0.0.1:8002/` in your browser.

## 📁 Project Structure

```
GaaDimension/
├── README.md                     ← This file
├── .gitignore                    ← Git ignore rules
├── plan.md                       ← Development progress tracking
├── backend/
│   ├── main.py                  ← FastAPI app entry point
│   ├── models.py                ← Car comparison model definitions
│   ├── silhouette_generator.py  ← SVG generation logic (NumPy)
│   ├── seed_db.py               ← Database seeding script
│   ├── .venv/                   ← Python venv directory
│   └── cars.db                  ← SQLite database
├── frontend/
│   └── index.html               ← Canvas-based comparison UI
└── Test/                        ← Sample scripts for local testing
```

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.13, FastAPI 0.115 |
| **Database** | SQLite (raw SQL) |
| **SVG Generation** | NumPy |
| **Frontend** | Vanilla HTML5 Canvas + Fetch API |
| **Server** | Uvicorn |

## 🔍 Available API Endpoints

### `/health`
Health check endpoint. Returns `{ "status": "ok" }`.

### `/cars[?search=<query>&make=<make>]`
List cars with optional filtering. Query supports partial matching on make/model.

Example: `/cars?search=Tata&make=Tata` → returns Tata-branded cars only.

### `/cars/{car_id}`
Get detailed information for a specific car by ID.

### `/svg/{car_id}`
Generate an SVG silhouette for a given car. Returns JSON with `svg` key containing the SVG string.

### `/compare/{car_a_id}/{car_b_id}`
Compare two cars. Generates side-by-side silhouettes and dimension difference stats. Results are cached (LRU).

## 🚀 Deployment

1. Ensure Python 3.12+ is installed.
2. Create/activate virtual environment at `backend/.venv`.
3. Install dependencies: `pip install -r requirements.txt` (if you have one) or manually:
   ```bash
   pip install fastapi uvicorn numpy sqlalchemy
   ```
4. Start server: `uvicorn main:app --host 0.0.0.0 --port 8002`

## 📝 License

MIT License - feel free to use and modify!

---

**Last Updated:** 2026-08-28  
**Author:** GaaD-Mension Team