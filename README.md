# Construction RAG Estimation AI Agent (Indian Standards)

A specialized AI Agent for civil engineering construction estimation on Windows, built with **Python (FastAPI)**, **Ollama** (`nomic-embed-text` & `llama3.2`), and **PostgreSQL with pgvector**. Exposes REST API endpoints for seamless integration into **Laravel** or any construction ERP software.

---

## Architecture Overview

```
 ┌──────────────────────────────────────────────────────────────┐
 │               Laravel 10/11 Web Application                  │
 │  (Input Form: Length, Width, Height, Location, RCC Bridge)   │
 └──────────────────────────────┬───────────────────────────────┘
                                │ HTTP POST /api/construction/estimate
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │             Python FastAPI Service (Port 8001)               │
 └──────────────┬───────────────────────────────┬───────────────┘
                │                               │
                ▼                               ▼
 ┌─────────────────────────────┐ ┌─────────────────────────────┐
 │       RAG Engine            │ │ Civil Engineering Calculator│
 │  - Ollama (nomic-embed)     │ │  - IRC:112-2020             │
 │  - PostgreSQL + pgvector    │ │  - MoRTH 5th Revision       │
 │    (IRC 112, MoRTH, SOR)    │ │  - CPWD DSR 2023 Analysis   │
 └──────────────┬──────────────┘ └──────────────┬──────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │         Ollama LLM (llama3.2:3b) Engineering Review          │
 │   - Validates span ratios & seismic zone V ductile detailing │
 │   - Flags missing borelogs, scour depth & HFL data           │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │             Structured JSON Estimation Report                │
 │  (Itemized BOQ, Materials, Total Cost, Citations, Warnings)  │
 └──────────────────────────────────────────────────────────────┘
```

---

## 1. Prerequisites (Configured on your Windows PC)

- **Python 3.13 / 3.15** with `.venv` created in `c:\rag_agent_core`
- **Ollama** running locally on port 11434 with models:
  - `nomic-embed-text:latest` (Embeddings, 768 dimensions)
  - `llama3.2:3b` (Inference & technical analysis)
- **PostgreSQL 17 with pgvector** running in Docker:
  - Container: `construction-postgres`
  - Host Port: `5433` (mapped to 5432)
  - Database: `construction_rag`
  - User: `construction_user`
  - Password: `ChangeThisPassword123!`

---

## 2. Project File Structure

```
c:\rag_agent_core\
├── .env                                  # Database & Ollama settings
├── requirements.txt                      # Python dependencies
├── seed_database.py                      # Seeds Indian Standards into pgvector
├── test_agent.py                         # End-to-end agent test script
├── sample_estimate_response.json         # Real output sample from agent
├── app\
│   ├── main.py                           # FastAPI app entry point & CORS
│   ├── config.py                         # Settings from .env
│   ├── database.py                       # PostgreSQL connection pool & schema
│   ├── api\
│   │   └── estimate.py                   # REST endpoints (/estimate, /health, /ingest)
│   ├── calculations\
│   │   ├── bridge_calculator.py          # Deterministic civil engineering volume formulas
│   │   └── cost_calculator.py            # Rate analysis & BOQ costing
│   ├── rag\
│   │   ├── agent.py                      # Core AI Agent Orchestrator
│   │   ├── ollama_client.py              # Ollama embeddings & LLM client
│   │   ├── vector_store.py               # pgvector similarity search repository
│   │   ├── seed_data.py                  # Curated IRC, MoRTH, and SOR data
│   │   └── ingest.py                     # Document embedding & ingestion
│   └── schemas\
│       └── estimate.py                   # Pydantic input/output schemas
└── laravel_integration\
    ├── README_LARAVEL.md                 # Complete Laravel setup guide
    ├── ConstructionAgentService.php      # Laravel HTTP service
    ├── ConstructionEstimateController.php# Laravel Controller
    ├── estimate.blade.php                # Tailwind-styled dashboard blade view
    └── routes_example.php                # Laravel route definitions
```

---

## 3. How to Start the FastAPI Server

Open PowerShell in `c:\rag_agent_core`:

```powershell
cd c:\rag_agent_core
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The server starts at `http://127.0.0.1:8001`.
- **Interactive Swagger Docs:** `http://127.0.0.1:8001/docs`
- **Health Check:** `http://127.0.0.1:8001/api/construction/health`

---

## 4. API Endpoints

### `POST /api/construction/estimate`
Accepts project parameters and returns a complete engineering estimate.

**Sample Request Body:**
```json
{
  "project_type": "bridge",
  "bridge_type": "RCC",
  "length_m": 100.0,
  "width_m": 10.0,
  "height_m": 8.0,
  "location": "Assam, India",
  "currency": "INR",
  "concrete_grade": "M35",
  "steel_grade": "Fe500D"
}
```

**Key Items Returned:**
- `project`: Dimensions, span count (e.g. 5 spans of 20m), foundation type.
- `estimation`: Total cost (`₹44,460,190.60`), cost per linear metre (`₹444,601.91/m`).
- `components`: Superstructure, Substructure, and Pile Foundation breakdown.
- `materials`: Itemized quantities for Concrete, Fe500D Steel, Shuttering, Cement (16,298 bags), River Sand, Coarse Aggregate, and Bored Piling.
- `source_references`: Retrieved Indian Standards (IRC 112, Assam PWD SOR, MoRTH).
- `missing_inputs`: Critical missing engineering items (Borelog report, HFL survey, GAD drawings).
- `ai_engineer_analysis`: Senior civil structural engineer review.

---

## 5. Integrating with Laravel

Refer to [laravel_integration/README_LARAVEL.md](file:///c:/rag_agent_core/laravel_integration/README_LARAVEL.md) for full instructions.

In Laravel:
```php
use App\Services\ConstructionAgentService;

$agent = new ConstructionAgentService();
$estimate = $agent->getBridgeEstimate([
    'project_type' => 'bridge',
    'bridge_type'  => 'RCC',
    'length_m'     => 100,
    'width_m'      => 10,
    'height_m'     => 8,
    'location'     => 'Assam, India',
]);
```
