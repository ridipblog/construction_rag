# Construction RAG Agent - Commands Cheat Sheet & Quick Reference

A complete, quick-reference guide containing all daily commands to start the RAG agent, inspect the PostgreSQL vector database, upload PDFs, and test endpoints.

---

## 1. Quick Start Commands (Daily Usage)

### Step 1: Start the PostgreSQL + pgvector Database
Before starting the API server, ensure the database container is running:
```powershell
docker start construction-postgres
```

### Step 2: Start the FastAPI AI Agent Server
Open PowerShell in your project directory:
```powershell
cd c:\rag_agent_core
.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8001 --reload
```

> **One-Click Shortcut:** You can also simply double-click `c:\rag_agent_core\start_server.bat`.

---

## 2. Browser & Testing Links

Once the server is running, use these direct links in your browser:

| Action | URL |
|---|---|
| **Interactive API Documentation** | [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) |
| **System Health Check** | [http://127.0.0.1:8001/api/construction/health](http://127.0.0.1:8001/api/construction/health) |
| **View All Database Documents (Browser)** | [http://127.0.0.1:8001/api/construction/documents/all](http://127.0.0.1:8001/api/construction/documents/all) |

---

## 3. How to View & Inspect the PostgreSQL Database

### Option A: Using the Python Viewer Script (Recommended)
Prints all documents, categories, metadata, and 768-dimensional vector samples in your console:
```powershell
cd c:\rag_agent_core
.venv\Scripts\python.exe view_database.py
```

### Option B: Using the Docker PostgreSQL Command Line (`psql`)
Log directly into the PostgreSQL database terminal:
```powershell
docker exec -it construction-postgres psql -U construction_user -d construction_rag
```

**Common SQL Commands inside psql:**
```sql
-- See all tables:
\dt

-- See table structure (columns & vector data type):
\d construction_documents

-- View all documents with their IDs and sources:
SELECT id, category, source FROM construction_documents ORDER BY id;

-- View sample 768-dimensional vector numbers:
SELECT id, source, substring(embedding::text from 1 for 45) || '...' AS vector_sample 
FROM construction_documents LIMIT 5;

-- Exit psql:
\q
```

### Option C: Using a Database GUI (DBeaver / pgAdmin / TablePlus / VS Code)
Create a new PostgreSQL connection with these credentials:
* **Host:** `localhost` (or `127.0.0.1`)
* **Port:** `5433` *(Note: Port 5433, not 5432)*
* **Database:** `construction_rag`
* **Username:** `construction_user`
* **Password:** `ChangeThisPassword123!`

---

## 4. How to Upload New Documents & PDFs into pgvector

### Option A: In the Browser via Swagger UI
1. Go to [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).
2. Click **`POST /api/construction/upload-pdf`**.
3. Click **"Try it out"**, select your `.pdf` file, set category (`standards`, `schedule_of_rates`, or `boq`), and click **"Execute"**.

### Option B: In PowerShell using `curl.exe`
```powershell
curl.exe -X POST "http://127.0.0.1:8001/api/construction/upload-pdf" `
  -F "file=@C:\rag_agent_core\documents\Assam_PWD_Bridge_Rates_2025.pdf" `
  -F "category=schedule_of_rates"
```

### Option C: Batch Folder Drop
Drop any `.pdf` files into `c:\rag_agent_core\documents\` and run:
```powershell
cd c:\rag_agent_core
.venv\Scripts\python.exe ingest_folder.py
```

---

## 5. How to Test the Estimation Endpoint via cURL

```powershell
curl.exe -X POST "http://127.0.0.1:8001/api/construction/estimate" `
  -H "Content-Type: application/json" `
  -d '{
    "project_type": "bridge",
    "bridge_type": "RCC",
    "length_m": 100.0,
    "width_m": 10.0,
    "height_m": 8.0,
    "location": "Assam, India",
    "concrete_grade": "M35",
    "steel_grade": "Fe500D"
  }'
```

---

## 6. How to Re-Seed or Reset the Database

To reload the original official Indian Standards (IRC:112, MoRTH, Assam PWD SOR):
```powershell
cd c:\rag_agent_core
.venv\Scripts\python.exe seed_database.py
```

---

## 7. Connecting from Laravel 10 / 11

In your Laravel project's `.env` file:
```env
CONSTRUCTION_AI_URL=http://127.0.0.1:8001
CONSTRUCTION_AI_TIMEOUT=120
```

In any Laravel Controller or Service:
```php
use Illuminate\Support\Facades\Http;

$response = Http::timeout(120)->post('http://127.0.0.1:8001/api/construction/estimate', [
    'project_type'   => 'bridge',
    'bridge_type'    => 'RCC',
    'length_m'       => 100,
    'width_m'        => 10,
    'height_m'       => 8,
    'location'       => 'Assam, India',
    'concrete_grade' => 'M35',
    'steel_grade'    => 'Fe500D'
]);

$data = $response->json();
$totalCost   = $data['estimation']['total_estimated_cost'];
$totalCement = $data['materials'][3]['quantity']; // Bags
$totalSteel  = $data['materials'][1]['quantity']; // Tonnes
```

