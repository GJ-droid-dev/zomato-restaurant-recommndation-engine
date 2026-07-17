# Architecture: AI-Powered Restaurant Recommendation System

## 1. System Overview

This document defines the end-to-end architecture for the Zomato-inspired AI-powered restaurant recommendation system. The application combines a structured restaurant dataset with a Large Language Model (LLM) to deliver personalized, explainable dining recommendations through a modern web interface.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                          │
│                  (HTML / CSS / JavaScript Web UI)                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │  HTTP (REST API)
┌──────────────────────────────▼──────────────────────────────────────┐
│                        APPLICATION LAYER                           │
│                     (Python – FastAPI Server)                       │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │
│  │ User Input   │→ │ Filter & Ranking │→ │ LLM Recommendation  │   │
│  │ Handler      │  │ Engine           │  │ Engine              │   │
│  └──────────────┘  └──────────────────┘  └─────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌───────────────┐  ┌───────────────────┐  ┌───────────────────────┐
│  DATA LAYER   │  │  LLM PROVIDER     │  │  CACHE LAYER          │
│  (CSV/Pandas) │  │  (Groq LLM API)   │  │  (In-Memory / File)   │
└───────────────┘  └───────────────────┘  └───────────────────────┘
```

---

## 2. Layer Breakdown

### 2.1 Presentation Layer (Frontend)

| Aspect        | Detail                                                   |
|---------------|----------------------------------------------------------|
| **Tech**      | HTML5, Vanilla CSS, JavaScript (ES6+)                    |
| **Hosting**   | Served by the FastAPI backend (static files)             |
| **Design**    | Responsive, mobile-first, glassmorphism dark-mode UI     |
| **Comms**     | `fetch()` calls to REST endpoints; JSON request/response |

**Key UI Components:**

| Component               | Responsibility                                                       |
|--------------------------|----------------------------------------------------------------------|
| `PreferenceForm`         | Collects location, budget, cuisine, rating, and free-text preferences |
| `RecommendationCard`     | Displays a single restaurant with name, cuisine, rating, cost, and AI explanation |
| `ResultsContainer`       | Renders a list of `RecommendationCard` components                    |
| `LoadingOverlay`         | Skeleton / spinner shown while the LLM generates results             |
| `ErrorToast`             | Non-blocking notification for API or validation errors               |

---

### 2.2 Application Layer (Backend)

| Aspect        | Detail                                         |
|---------------|-------------------------------------------------|
| **Framework** | Python 3.10+ with **FastAPI**                   |
| **Runner**    | Uvicorn (ASGI)                                  |
| **Role**      | API gateway, business logic, LLM orchestration  |

The backend is composed of three core modules:

#### Module A – User Input Handler (`routers/recommend.py`)

- Receives JSON payloads from the frontend.
- Validates and normalises user preferences using **Pydantic** models.

```
POST /api/recommend
Content-Type: application/json

{
  "location": "Indiranagar",
  "budget": "medium",
  "cuisine": "Italian",
  "min_rating": 4.0,
  "additional_preferences": "family-friendly"
}
```

#### Module B – Filter & Ranking Engine (`services/filter.py`)

- Loads the preprocessed restaurant DataFrame.
- Applies multi-criteria filtering:

```
Dataset
  │
  ├─► Filter by Location  (exact / fuzzy match)
  ├─► Filter by Cuisine   (partial match, multi-cuisine support)
  ├─► Filter by Budget    (cost-bracket mapping)
  └─► Filter by Rating    (≥ min_rating threshold)
        │
        ▼
  Candidate Set (Top-N restaurants passed to LLM)
```

- Returns a shortlist (default **top 20 candidates**) sorted by rating to keep the LLM prompt concise.

#### Module C – LLM Recommendation Engine (`services/llm.py`)

- Constructs a structured prompt with:
  - User preferences (natural language summary)
  - Candidate restaurant data (tabular / JSON)
  - Instructions for ranking, explanation, and output format
- Calls the **Groq API** (ultra-fast LLM inference).
- Parses the structured JSON response from the LLM.
- Returns the **top 5 recommendations** with explanations.

**Prompt Template Strategy:**

```
System: You are a restaurant recommendation expert. Given the user's
preferences and a list of candidate restaurants, rank the best matches
and explain why each one is a good fit.

User Preferences:
  - Location: {location}
  - Budget: {budget}
  - Cuisine: {cuisine}
  - Minimum Rating: {min_rating}
  - Other: {additional_preferences}

Candidate Restaurants:
{candidate_json}

Instructions:
  1. Select the top 5 restaurants that best match the preferences.
  2. For each, provide: name, cuisine, rating, cost, and a 2–3 sentence
     explanation of why it is recommended.
  3. Return the result as a JSON array.
```

---

### 2.3 Data Layer

| Aspect          | Detail                                                                                     |
|-----------------|--------------------------------------------------------------------------------------------|
| **Source**       | [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) (Hugging Face) |
| **Format**      | CSV → Pandas DataFrame                                                                     |
| **Storage**     | Local file (`data/zomato.csv`), loaded into memory at server startup                       |
| **Preprocessing** | Handled by `services/data_loader.py` at boot time                                        |

**Preprocessing Pipeline:**

```
Raw CSV
  │
  ├─► Drop duplicates & null rows
  ├─► Normalise column names (lowercase, snake_case)
  ├─► Clean 'cost' column → numeric (float)
  ├─► Clean 'rating' column → numeric (float)
  ├─► Normalise 'location' → title-case, strip whitespace
  ├─► Normalise 'cuisine' → lowercase list
  ├─► Map cost to budget brackets (low / medium / high)
  └─► Cache cleaned DataFrame in memory
```

**Key Fields:**

| Field             | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `name`            | str    | Restaurant name                      |
| `location`        | str    | City or area                         |
| `cuisines`        | list   | List of cuisines offered             |
| `cost_for_two`    | float  | Average cost for two people          |
| `rating`          | float  | Aggregate rating (0–5)              |
| `votes`           | int    | Number of votes / reviews            |
| `budget_bracket`  | str    | Derived: low / medium / high         |

---

### 2.4 Cache Layer

| Aspect       | Detail                                                       |
|--------------|--------------------------------------------------------------|
| **Purpose**  | Avoid redundant LLM calls for identical preference sets      |
| **Strategy** | Hash of normalised user preferences → cached LLM response    |
| **Storage**  | In-memory dictionary (optionally persisted to JSON file)     |
| **TTL**      | Configurable; default 1 hour                                 |

---

## 3. API Contract

### Endpoints

| Method | Path              | Description                          | Auth     |
|--------|-------------------|--------------------------------------|----------|
| GET    | `/`               | Serve the frontend UI                | None     |
| POST   | `/api/recommend`  | Get AI-powered recommendations       | API Key  |
| GET    | `/api/locations`  | List all available locations          | None     |
| GET    | `/api/cuisines`   | List all available cuisines           | None     |
| GET    | `/api/health`     | Health check                         | None     |

### Response Schema – `/api/recommend`

```json
{
  "success": true,
  "query": {
    "location": "Indiranagar",
    "budget": "medium",
    "cuisine": "Italian",
    "min_rating": 4.0,
    "additional_preferences": "family-friendly"
  },
  "candidates_found": 18,
  "recommendations": [
    {
      "rank": 1,
      "name": "Bella Italia",
      "cuisine": "Italian, Continental",
      "rating": 4.6,
      "cost_for_two": 1200,
      "explanation": "Bella Italia is a top-rated family-friendly Italian restaurant in Indiranagar, offering wood-fired pizzas and pastas at a mid-range price point."
    }
  ]
}
```

---

## 4. Directory Structure

```
Zomato Project/
├── Docs/
│   ├── problemstatement.txt
│   ├── context.md
│   └── architecture.md          ← this file
├── data/
│   └── zomato.csv               ← downloaded dataset
├── backend/
│   ├── main.py                  ← FastAPI app entry point
│   ├── config.py                ← env vars, API keys, constants
│   ├── routers/
│   │   └── recommend.py         ← /api/recommend endpoint
│   ├── services/
│   │   ├── data_loader.py       ← CSV loading & preprocessing
│   │   ├── filter.py            ← multi-criteria filtering
│   │   └── llm.py               ← LLM prompt construction & API call
│   ├── models/
│   │   ├── request.py           ← Pydantic request schemas
│   │   └── response.py          ← Pydantic response schemas
│   └── utils/
│       └── cache.py             ← in-memory response cache
├── frontend/
│   ├── index.html               ← main UI page
│   ├── css/
│   │   └── style.css            ← global styles
│   └── js/
│       └── app.js               ← fetch calls, DOM rendering
├── requirements.txt             ← Python dependencies
├── .env                         ← API keys (git-ignored)
└── README.md
```

---

## 5. Technology Stack

| Layer          | Technology                          | Version / Notes          |
|----------------|-------------------------------------|--------------------------|
| Language       | Python                              | 3.10+                    |
| Web Framework  | FastAPI                             | latest                   |
| ASGI Server    | Uvicorn                             | latest                   |
| Data Processing| Pandas                              | latest                   |
| LLM Provider   | Groq                                | `llama-3.3-70b-versatile` model |
| LLM SDK        | `groq`                              | latest                   |
| Validation     | Pydantic                            | v2                       |
| Frontend       | HTML5 / CSS3 / Vanilla JS           | —                        |
| Dataset Source | Hugging Face `datasets` library      | latest                   |
| Env Management | python-dotenv                       | latest                   |

---

## 6. Data Flow Diagram

```
┌────────┐       ┌──────────┐       ┌──────────┐       ┌─────────┐       ┌──────────┐
│  User  │──────►│ Frontend │──────►│ FastAPI  │──────►│ Filter  │──────►│   LLM    │
│        │ prefs │   (UI)   │ POST  │  Router  │ query │ Engine  │ top-N │  Engine  │
└────────┘       └──────────┘       └──────────┘       └─────────┘       └────┬─────┘
                                                                              │
                      ┌───────────────────────────────────────────────────────┘
                      │  ranked recommendations (JSON)
                      ▼
               ┌──────────┐       ┌──────────┐       ┌────────┐
               │ FastAPI  │──────►│ Frontend │──────►│  User  │
               │ Response │ JSON  │ Renderer │ cards │        │
               └──────────┘       └──────────┘       └────────┘
```

---

## 7. Key Design Decisions

| Decision                          | Rationale                                                                 |
|-----------------------------------|---------------------------------------------------------------------------|
| **FastAPI over Flask**            | Native async support, automatic OpenAPI docs, Pydantic integration        |
| **Pandas for filtering**         | Efficient in-memory operations on tabular data; no database overhead      |
| **Pre-filter before LLM**        | Reduces token usage and cost; improves relevance of LLM output            |
| **Structured JSON output from LLM** | Enables reliable parsing and consistent UI rendering                   |
| **In-memory cache**              | Simple, zero-dependency caching for identical queries                     |
| **Vanilla CSS + JS frontend**    | Lightweight, no build step; sufficient for a single-page recommendation UI|
| **Groq**                        | Ultra-low latency inference, generous free tier, strong structured output support |

---

## 8. Error Handling Strategy

| Scenario                     | Handling                                                    |
|------------------------------|-------------------------------------------------------------|
| No restaurants match filters | Return a helpful message suggesting broader criteria         |
| LLM API timeout / failure    | Retry once; fall back to top-rated filter results           |
| Invalid user input           | Pydantic validation with descriptive 422 error responses     |
| Dataset load failure         | Fail fast at startup with a clear log message               |
| Malformed LLM response       | Fallback parser; return raw candidates if JSON parse fails  |

---

## 9. Security Considerations

| Concern                | Mitigation                                                   |
|------------------------|--------------------------------------------------------------|
| API key exposure       | Stored in `.env`, never committed; loaded via `python-dotenv`|
| Prompt injection       | User input sanitised before inclusion in LLM prompt          |
| Rate limiting          | Optional middleware on `/api/recommend`                      |
| CORS                   | Restricted to frontend origin in production                  |

---

## 10. Future Enhancements

| Enhancement                       | Description                                                    |
|-----------------------------------|----------------------------------------------------------------|
| Vector search (RAG)               | Embed restaurant descriptions; use semantic similarity search  |
| User accounts & history           | Persist preferences and past recommendations                   |
| Real-time data                    | Integrate Zomato/Swiggy APIs for live menus and availability   |
| Multi-turn conversation           | Chat-style interface for iterative preference refinement       |
| Deployment                        | Containerise with Docker; deploy on Cloud Run / Railway        |
