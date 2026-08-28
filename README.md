# 🚗 Indian Car Visual Comparator

**Compare car dimensions side-by-side** to visualize size differences between popular Indian vehicles.

## ✨ Features

### Backend
- **FastAPI Framework** (Python 3.13+) - Async REST API with automatic JSON serialization and OpenAPI docs
- **SQLite Database** - Lightweight, zero-config database with startup seeding
- **SVG Generation Pipeline** - NumPy-based geometric silhouette generation for car side profiles

### Frontend  
- **Vanilla HTML5 Canvas** - No frameworks required, just pure JavaScript
- **Fetch API Integration** - Async data fetching at page load
- **Canvas Modes** - Side-by-side view or overlay comparison with alpha transparency
- **Debounced Search** - 250ms delay to reduce API calls
- **Smart Filtering** - Multi-field search by make, model, and dimensions
- **Dimension Stats** - Color-coded differences (green ≤50mm, red >50mm)

## 🛠️ Quick Start

`bash
# Clone repository
git clone https://github.com/PcubeP/gaa-D-mension.git
cd gaa-D-mension

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.main:app --host 0.0.0.0 --port 8002 --reload
`

Then open http://127.0.0.1:8002/ in your browser.

## 📁 Project Structure

`
GaaDimension/
├── README.md                     # This documentation
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git exclusions
├── backend/                      # FastAPI application
│   ├── main.py                  # API routes and startup logic
│   ├── models.py                # Data models for serialization
│   ├── silhouette_generator.py  # SVG path generation using NumPy
│   ├── seed_db.py               # Database seeding (48 Indian cars)
│   └── .venv/                   # Python virtual environment
├── frontend/
│   └── index.html               # Canvas-based comparison UI
└── LICENSE                      # MIT License
`

## 📡 API Endpoints

### Health Check
**GET /health** - System health status
{
  "status": "ok"
}

### Car Listing  
**GET /cars[?search=<query>&make=<make>]** - List all cars with optional filtering

**Query Parameters:**
- search (string) - Partial match for make or model
- make (string) - Filter by manufacturer (e.g., "Tata", "Maruti", "Hyundai")

**Example:** 
GET /cars?search=Tata&make=Tata

### Car Details
**GET /cars/{car_id}** - Get detailed information for a specific car

**Response:**
{
  "id": 1,
  "make": "Maruti",
  "model": "Alto",
  "year": 2024,
  "length_mm": 3595,
  "width_mm": 1660,
  "height_mm": 1560,
  "wheelbase_mm": 2460
}

### SVG Generation
**GET /svg/{car_id}** - Generate SVG silhouette for a car

**Response:**
{
  "svg": "<svg>...</svg>"
}

### Comparison Endpoint
**GET /compare/{car_a_id}/{car_b_id}** - Compare two cars side-by-side

Returns combined SVG with both vehicle silhouettes and dimension difference stats. Results are cached using LRU eviction.

## 🚀 Deployment Guide

### Prerequisites
- Python 3.12+
- Git (for cloning)

### Local Development
1. Clone: git clone https://github.com/PcubeP/gaa-D-mension.git
2. Create venv: python -m venv .venv
3. Activate and install: .venv\Scripts\activate && pip install -r requirements.txt
4. Run: uvicorn backend.main:app --reload

### Production Deployment (Linux/Mac)
`bash
python -m venv /opt/venv
source /opt/venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8002 --workers 4
`

## 🧪 Testing

Test the API using curl:

`bash
# Get all cars
curl http://localhost:8002/cars

# Filter by make
curl "http://localhost:8002/cars?make=Tata"

# Generate SVG
curl http://localhost:8002/svg/1

# Compare two cars
curl "http://localhost:8002/compare/1/2"
`

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.13, FastAPI 0.115.0 |
| **Database** | SQLite (raw SQL, no ORM) |
| **SVG Generation** | NumPy - Geometric path approximation |
| **Frontend** | HTML5 Canvas + Vanilla JavaScript |
| **Server** | Uvicorn ASGI server |

## 📝 License

This project is licensed under the MIT License - feel free to use and modify!

---

**Last Updated:** 2026-08-28  
**Author:** PcubeP
