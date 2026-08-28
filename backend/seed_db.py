"""Seed database with sample Indian car data."""
from sqlite3 import connect

def seed_database():
    """Seed with sample Indian car data."""
    conn_str = "sqlite:///cars.db"
    if isinstance(conn_str, str):
        conn = connect(conn_str)
    
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM comparisons")
    cursor.execute("DELETE FROM cars")
    
    # Sample Indian car dimensions (length x width x height in mm)
    cars = [
        ("Mahindra", "Thar", 2024, 3971, 1680, 1750, 2450),
        ("Mahindra", "Bolero", 2024, 3723, 1540, 1820, 2200),
        ("Tata", "Nexon", 2024, 3963, 1765, 1608, 2508),
        ("Tata", "Harrier", 2024, 4597, 1905, 1710, 2741),
        ("Tata", "XUV700", 2024, 4630, 1914, 1746, 2751),
        ("Tata", "Tiago", 2024, 3688, 1635, 1597, 2330),
        ("Tata", "Scorpio", 2024, 4710, 1842, 1755, 2760),
        ("Tata", "Punch", 2024, 3592, 1668, 1530, 2340),
    ]
    
    for make, model, year, length, width, height, wheelbase in cars:
        cursor.execute(
            "INSERT INTO cars (make, model, year, length, width, height, wheelbase) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (make, model, year, length, width, height, wheelbase)
        )
    
    conn.commit()
    print(f"Seeded database with {len(cars)} cars")
    return conn


if __name__ == "__main__":
    seed_database()
