# Implementation Plan: AI-Powered Restaurant Recommendation System

> **Reference Documents:**
> - [context.md](file:///c:/Users/Admin/Documents/Zomato%20Project/Docs/context.md) — Problem statement & objectives
> - [architecture.md](file:///c:/Users/Admin/Documents/Zomato%20Project/Docs/architecture.md) — System architecture & design

---

## Phase Overview

```
Phase 1          Phase 2          Phase 3          Phase 4          Phase 5
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Project   │──►│   Data     │──►│  Backend   │──►│  Frontend  │──►│  Polish &  │
│  Setup     │   │  Pipeline  │   │  API +LLM  │   │     UI     │   │  Deploy    │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
  ~30 min          ~1–2 hrs         ~2–3 hrs         ~2–3 hrs         ~1–2 hrs
```

---

## Phase 1: Project Setup & Environment Configuration

**Goal:** Establish project scaffolding, install dependencies, and configure environment variables.

### Tasks

| #  | Task                                            | File(s) Created / Modified            |
|----|-------------------------------------------------|---------------------------------------|
| 1.1 | Create the full directory structure             | All folders per architecture.md       |
| 1.2 | Initialise Python virtual environment           | `venv/`                               |
| 1.3 | Create `requirements.txt` with all dependencies | `requirements.txt`                    |
| 1.4 | Install dependencies                            | —                                     |
| 1.5 | Create `.env` file with Groq API key placeholder| `.env`                                |
| 1.6 | Create `.gitignore`                             | `.gitignore`                          |
| 1.7 | Create `backend/config.py` to load env vars     | `backend/config.py`                   |

### 1.1 — Directory Structure

```
mkdir -p data backend/routers backend/services backend/models backend/utils frontend/css frontend/js Docs
```

### 1.2 — Virtual Environment

```
python -m venv venv
venv\Scripts\activate       # Windows
```

### 1.3 — `requirements.txt`

```
fastapi
uvicorn[standard]
pandas
groq
python-dotenv
pydantic
datasets          # Hugging Face datasets library
```

### 1.5 — `.env`

```
GROQ_API_KEY=your_groq_api_key_here
```

### 1.7 — `backend/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "zomato.csv")
TOP_N_CANDIDATES = 20
CACHE_TTL_SECONDS = 3600
```

### Deliverables

- [x] All folders exist
- [x] `venv` active with all packages installed
- [x] `.env` configured with Groq key
- [x] `config.py` loads and exposes all settings

### Exit Criteria

✅ `python -c "import fastapi, groq, pandas; print('OK')"` runs without errors.

---

## Phase 2: Data Ingestion & Preprocessing

**Goal:** Download the Zomato dataset, clean it, and expose it as a reusable in-memory DataFrame.

### Tasks

| #  | Task                                                   | File(s)                       |
|----|--------------------------------------------------------|-------------------------------|
| 2.1 | Download dataset from Hugging Face → `data/zomato.csv` | `data/zomato.csv`             |
| 2.2 | Explore dataset — inspect columns, dtypes, nulls       | Jupyter / scratch script      |
| 2.3 | Build preprocessing pipeline in `data_loader.py`       | `backend/services/data_loader.py` |
| 2.4 | Add helper endpoints: `/api/locations`, `/api/cuisines`| `backend/routers/recommend.py`|
| 2.5 | Validate cleaned data with unit checks                 | manual / script               |

### 2.1 — Download Script

```python
from datasets import load_dataset

ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
ds["train"].to_csv("data/zomato.csv", index=False)
```

### 2.3 — `backend/services/data_loader.py`

Implement the full preprocessing pipeline:

```
Raw CSV
  │
  ├─► Drop duplicates & null rows
  ├─► Normalise column names → lowercase, snake_case
  ├─► Clean 'cost' column → numeric float
  ├─► Clean 'rating' column → numeric float
  ├─► Normalise 'location' → title-case, strip whitespace
  ├─► Normalise 'cuisine' → lowercase list (split by comma)
  ├─► Map cost → budget bracket (low / medium / high)
  └─► Cache cleaned DataFrame in module-level variable
```

**Budget Bracket Mapping (suggested thresholds — adjust after exploring data):**

| Bracket   | Cost for Two (₹)  |
|-----------|--------------------|
| Low       | ≤ 500              |
| Medium    | 501 – 1500         |
| High      | > 1500             |

### Deliverables

- [x] `data/zomato.csv` downloaded and available locally
- [x] `data_loader.py` loads, cleans, and caches the DataFrame
- [x] Unique location and cuisine lists extractable from the DataFrame

### Exit Criteria

✅ `data_loader.get_dataframe()` returns a clean DataFrame with no nulls in key columns.
✅ `/api/locations` and `/api/cuisines` return non-empty JSON arrays.

---

## Phase 3: Backend API & LLM Integration

**Goal:** Build the FastAPI server with filtering logic, Groq LLM integration, prompt engineering, and response caching.

### Tasks

| #  | Task                                                    | File(s)                              |
|----|---------------------------------------------------------|--------------------------------------|
| 3.1 | Define Pydantic request & response models              | `backend/models/request.py`, `response.py` |
| 3.2 | Build multi-criteria filter engine                     | `backend/services/filter.py`         |
| 3.3 | Build LLM recommendation engine with prompt template   | `backend/services/llm.py`            |
| 3.4 | Implement in-memory response cache                     | `backend/utils/cache.py`             |
| 3.5 | Wire up `POST /api/recommend` endpoint                 | `backend/routers/recommend.py`       |
| 3.6 | Create FastAPI app entry point with CORS & static files| `backend/main.py`                    |
| 3.7 | Add health check endpoint `GET /api/health`            | `backend/main.py`                    |
| 3.8 | Test the full pipeline end-to-end via curl / Swagger   | —                                    |

### 3.1 — Pydantic Models

**`backend/models/request.py`**

```python
class RecommendRequest(BaseModel):
    location: str
    budget: str              # "low" | "medium" | "high"
    cuisine: str
    min_rating: float = 0.0
    additional_preferences: str = ""
```

**`backend/models/response.py`**

```python
class Recommendation(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    cost_for_two: float
    explanation: str

class RecommendResponse(BaseModel):
    success: bool
    query: dict
    candidates_found: int
    recommendations: list[Recommendation]
```

### 3.2 — Filter Engine (`services/filter.py`)

```
filter_restaurants(df, location, budget, cuisine, min_rating) → DataFrame
```

- Case-insensitive location matching (contains / fuzzy)
- Cuisine partial match (restaurant may serve multiple cuisines)
- Budget bracket filter
- Rating ≥ threshold
- Sort by rating descending, return top N (default 20)

### 3.3 — LLM Engine (`services/llm.py`)

```
get_recommendations(user_prefs, candidates_df) → list[Recommendation]
```

- Build the system + user prompt using the template from architecture.md
- Call `groq.Client().chat.completions.create()` with:
  - `model = "llama-3.3-70b-versatile"`
  - `response_format = {"type": "json_object"}`
  - `temperature = 0.3` (deterministic but not rigid)
- Parse JSON response → list of `Recommendation` objects
- Handle malformed responses with a fallback parser

### 3.4 — Cache (`utils/cache.py`)

```python
class ResponseCache:
    def __init__(self, ttl=3600): ...
    def _hash_key(self, prefs: dict) -> str: ...
    def get(self, prefs: dict) -> Optional[list]: ...
    def set(self, prefs: dict, recommendations: list): ...
```

### 3.6 — `backend/main.py`

```python
app = FastAPI(title="Zomato AI Recommendations")

# CORS middleware
# Mount frontend static files
# Include recommendation router
# Load dataset on startup event
```

### Deliverables

- [x] `POST /api/recommend` returns AI-ranked restaurants with explanations
- [x] Filtering correctly narrows candidates before LLM call
- [x] Groq LLM integration returns structured JSON
- [x] Cache prevents duplicate LLM calls
- [x] Swagger docs auto-generated at `/docs`

### Exit Criteria

✅ `POST /api/recommend` with sample payload returns 5 ranked recommendations with explanations.
✅ Second identical request is served from cache (< 10ms response time).
✅ Invalid input returns 422 with descriptive error.

---

## Phase 4: Frontend UI

**Goal:** Build a premium, responsive web interface with dark-mode glassmorphism design.

### Tasks

| #  | Task                                                   | File(s)                   |
|----|--------------------------------------------------------|---------------------------|
| 4.1 | Create HTML structure with semantic elements          | `frontend/index.html`     |
| 4.2 | Design the CSS design system (dark mode, glassmorphism)| `frontend/css/style.css`  |
| 4.3 | Build the preference form (dropdowns populated from API)| `frontend/js/app.js`     |
| 4.4 | Build recommendation card rendering                   | `frontend/js/app.js`      |
| 4.5 | Add loading states (skeleton / spinner animation)     | `frontend/css/style.css`  |
| 4.6 | Add error toast notifications                         | `frontend/js/app.js`      |
| 4.7 | Add micro-animations and hover effects                | `frontend/css/style.css`  |
| 4.8 | Ensure mobile responsiveness                          | `frontend/css/style.css`  |

### 4.1 — HTML Structure (`index.html`)

```
<body>
  <header>    → Logo, title, tagline
  <main>
    <section#preferences>  → Form with location, budget, cuisine, rating, extras
    <section#results>      → Dynamically rendered recommendation cards
  </main>
  <footer>    → Credits
</body>
```

### 4.2 — CSS Design System (`style.css`)

| Token                  | Value                                    |
|------------------------|------------------------------------------|
| `--bg-primary`         | `hsl(230, 25%, 8%)`  (deep dark)         |
| `--bg-card`            | `rgba(255, 255, 255, 0.04)` (glass)      |
| `--border-glass`       | `rgba(255, 255, 255, 0.08)`              |
| `--accent-primary`     | `hsl(350, 85%, 55%)` (Zomato red-inspired)|
| `--accent-secondary`   | `hsl(40, 95%, 60%)`  (warm gold)         |
| `--text-primary`       | `hsl(0, 0%, 95%)`                        |
| `--text-secondary`     | `hsl(0, 0%, 60%)`                        |
| `--radius`             | `16px`                                   |
| `--blur`               | `20px`                                   |
| `--font-family`        | `'Inter', sans-serif`                    |

Key design features:
- Glassmorphism cards with `backdrop-filter: blur()`
- Gradient accent borders
- Smooth `transition` on all interactive elements
- `@keyframes` for loading skeleton pulse
- `@media` breakpoints for mobile / tablet / desktop

### 4.3 — JavaScript (`app.js`)

```
On page load:
  ├─► fetch /api/locations → populate location dropdown
  └─► fetch /api/cuisines  → populate cuisine dropdown

On form submit:
  ├─► Validate inputs
  ├─► Show loading overlay
  ├─► POST /api/recommend with JSON body
  ├─► On success → render recommendation cards
  └─► On error   → show error toast
```

### 4.4 — Recommendation Card

Each card displays:

```
┌─────────────────────────────────────────┐
│  #1  ★ 4.6                              │
│  Bella Italia                           │
│  Italian, Continental                   │
│  ₹1,200 for two                         │
│                                         │
│  "Bella Italia is a top-rated family-   │
│   friendly Italian restaurant..."       │
└─────────────────────────────────────────┘
```

### Deliverables

- [x] Fully functional single-page UI
- [x] Dropdowns dynamically populated from API
- [x] Premium glassmorphism dark-mode design
- [x] Smooth loading states and error handling
- [x] Responsive across mobile, tablet, desktop

### Exit Criteria

✅ User can select preferences, submit, and see AI recommendations rendered as cards.
✅ Loading spinner appears during API call.
✅ Error toast appears on network failure.
✅ UI looks polished on both mobile (375px) and desktop (1440px).

---

## Phase 5: Integration Testing, Polish & Documentation

**Goal:** End-to-end validation, edge-case handling, performance tuning, and final documentation.

### Tasks

| #  | Task                                                    | File(s)                    |
|----|---------------------------------------------------------|----------------------------|
| 5.1 | End-to-end test: full user flow from UI to LLM & back | —                          |
| 5.2 | Edge case testing (no results, invalid inputs, LLM fail)| —                         |
| 5.3 | Prompt tuning — refine LLM prompt for better output    | `backend/services/llm.py`  |
| 5.4 | Performance check — cache hits, response times         | —                          |
| 5.5 | Add `README.md` with setup & usage instructions        | `README.md`                |
| 5.6 | Final UI polish — animations, spacing, typography      | `frontend/css/style.css`   |
| 5.7 | Code cleanup — remove debug prints, add docstrings     | all backend files          |

### 5.1 — E2E Test Scenarios

| # | Scenario                           | Expected Result                                     |
|---|------------------------------------|-----------------------------------------------------|
| 1 | Valid request (Indiranagar, medium, Italian, 4.0) | 5 ranked recommendations with explanations   |
| 2 | No matching restaurants            | Friendly message: "Try broadening your criteria"    |
| 3 | Empty optional fields              | Works with defaults; no crash                       |
| 4 | Repeated identical request         | Served from cache; response < 50ms                  |
| 5 | Groq API key missing / invalid     | Clear error message; no stack trace leaked to UI     |
| 6 | Groq API rate limit / timeout      | Retry once, then fallback to top-rated filter results|
| 7 | Very broad query (all locations)   | Returns top 5 overall; doesn't overwhelm LLM prompt |

### 5.5 — `README.md` Structure

```markdown
# Zomato AI Restaurant Recommender

## Overview
## Tech Stack
## Setup
  ### Prerequisites
  ### Installation
  ### Configuration (.env)
## Running the App
## API Endpoints
## Screenshots
## Architecture
## License
```

### Deliverables

- [x] All 7 E2E scenarios pass
- [x] LLM prompt produces consistent, well-structured output
- [x] README with complete setup instructions
- [x] Clean, documented codebase

### Exit Criteria

✅ Application runs end-to-end with `uvicorn backend.main:app --reload`.
✅ User can interact with the full recommendation flow from the browser.
✅ All edge cases handled gracefully without crashes or leaked errors.

---

## Summary Timeline

| Phase | Description                      | Estimated Time | Key Output                        |
|-------|----------------------------------|----------------|-----------------------------------|
| 1     | Project Setup & Environment      | ~30 min        | Scaffolding, deps, config         |
| 2     | Data Ingestion & Preprocessing   | ~1–2 hrs       | Clean dataset, data_loader.py     |
| 3     | Backend API & LLM Integration    | ~2–3 hrs       | Working API with Groq LLM         |
| 4     | Frontend UI                      | ~2–3 hrs       | Premium glassmorphism web UI      |
| 5     | Testing, Polish & Documentation  | ~1–2 hrs       | E2E tested, documented app        |
| **Total** |                              | **~7–11 hrs**  |                                   |

---

## Dependency Graph

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
  setup       data        API         UI         polish
                          │                        ▲
                          └────────────────────────┘
                            (prompt tuning in Phase 5
                             requires working API)
```

> **Note:** Phases are sequential — each phase depends on the deliverables of the previous one. However, Phase 4 (Frontend) can begin in parallel with late Phase 3 tasks if the API contract is finalized early.
