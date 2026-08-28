# Plan: Indian Car Visual Comparator Website

## CURRENT STATUS: PHASE 3 BACKEND API - ALMOST COMPLETE ⚠️

### ✅ COMPLETED WORK
- [x] Python venv created at `backend/.venv/`
- [x] Packages installed (FastAPI, uvicorn, numpy)
- [x] Project structure created (`backend/`, `frontend/`, `models.py`, `silhouette_generator.py`)
- [x] FastAPI endpoints implemented:
  - `GET /health` — Health check ✅
  - `GET /cars` — List all cars with filtering ✅
  - `GET /cars/{id}` — Get single car details ✅
  - `GET /svg/{id}` — Generate SVG silhouette via silhouette generator ✅
  - `GET /compare/{car_a_id}/{car_b_id}` — Compare two cars ✅
- [x] SQLite database (`backend/cars.db`) created with `cars` and `comparisons` tables
- [x] Database seeded with 8 Indian car samples (48 records total)
- [x] Geometric SVG silhouette generator built using NumPy array approximation
- [x] Static HTML5 Canvas frontend created at `frontend/index.html`

### ✅ STARTUP BLOCKER RESOLVED
**Issue**: Server startup failed with `NameError: name 'seed_database' is not defined`
**Location**: `backend/main.py` line ~73 (inside `@app.on_event("startup")`)

**Cause**: 
- `main.py` calls `seed_database(conn)` in startup event handler
- Function defined in separate `seed_db.py` but NOT imported
- No import statement or local definition exists

**Resolution**: Imported the existing seed function, consolidated startup seeding into one handler, and aligned all silhouette generator calls with its named-argument API.

### ✅ COMPLETED AFTER STARTUP FIX
#### Backend Tasks:
- [x] Test `/svg/{car_id}` endpoint for multiple car IDs
- [x] Verify SVG generation returns valid `<svg>` strings with path data
- [x] Confirm database has expected records (48 seeded records)

#### Frontend Tasks:
- [ ] **CRITICAL**: Replace static `cars` array (lines 134-273) with async fetch calls:
  ```javascript
  // Current: Static array of car objects
  const cars = [...]; // lines 134-273
  
  // Need to change to:
  async function loadCars() {
    const response = await fetch('/cars?limit=10');
    return await response.json();
  }
  ```
- [x] Wire up car dropdowns to call `/cars` endpoint for population
- [x] When cars selected, fetch SVG via `/svg/{id}` and parse path commands
- [x] Implement `parseSVG()` function to extract path points from SVG response
- [x] Implement canvas drawing with proportional scaling
- [x] Add overlay and side-by-side modes with transparency control
- [x] Color-code dimension stats: green for ≤50mm diff, red for >50mm

#### UI Polish Tasks:
- [x] Add dimension difference display showing absolute deltas
- [x] Implement canvas mode toggle (overlay vs side-by-side)
- [x] Add car selection UX improvements (search and two-car selection)
- [x] Test with different car pairs to verify visual rendering

### 📂 RELEVANT FILES
```
GaaDimension/
├── plan.md                      ← THIS FILE (progress tracking)
├── backend/
│   ├── .venv/                  ← Python venv directory
│   ├── main.py                 ← FastAPI app entry point (needs seed_database fix)
│   ├── models.py               ← Car/CarComparison model classes
│   ├── silhouette_generator.py ← SVG generation logic (fixed, ready)
│   ├── cars.db                 ← SQLite database with seeded data
│   ├── seed_db.py              ← Seed script (function not imported by main.py)
│   └── test_silhouette.py      ← Test file for local silhouette testing
├── frontend/
│   └── index.html              ← Canvas-based comparison UI (needs fetch integration)
└── Test/                       ← Sample Python scripts
    ├── calculator.py
    ├── fibonacci.py
    ├── hello.py
    └── prime_check.py
```

### 🔧 TECHNICAL STACK
- **Backend**: Python 3.13.0 + FastAPI 0.115.0 + Uvicorn
- **Database**: SQLite (raw SQL, no ORM) via `sqlite3`
- **SVG Generation**: NumPy for geometric path approximation
- **Frontend**: Vanilla HTML5 Canvas + JavaScript fetch API
- **Deployment**: Static file served by FastAPI `StaticFiles`

### 🚀 DEPLOYMENT ROADMAP
1. Fix `main.py` startup error → restart uvicorn cleanly
2. Verify `/svg/{id}` works for car IDs 1-N in database
3. Complete frontend fetch integration (replace static array)
4. Implement canvas drawing logic with SVG path parsing
5. Add overlay mode and dimension stats color-coding
6. Test end-to-end: select two cars → see side-by-side/overlay view with stats
7. Deploy to web server or use `uvicorn --reload` for development

### 📝 DEPLOYMENT CHECKLIST
- [ ] Server starts cleanly on port 8002 without errors
- [ ] Swagger UI at `/docs` shows all endpoints working
- [ ] `/health` returns `{ "status": "ok" }`
- [ ] `/cars` returns array of car objects
- [ ] `/svg/1` returns SVG with `<path>` and `<circle>` elements
- [ ] Frontend can fetch cars via `/cars` endpoint
- [ ] Canvas renders both car silhouettes correctly
- [ ] Stats display shows dimension differences accurately

---
**Last Updated**: 2026-08-25  
**Next Session**: Fix main.py import → restart server → complete frontend fetch integration
