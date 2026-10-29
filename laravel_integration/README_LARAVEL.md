# Laravel Integration Guide for Construction RAG Agent

This package connects your Laravel application with the Python FastAPI Construction RAG Estimation Agent running locally on Windows.

---

## 1. Copy Files into your Laravel Project

Copy the provided integration files into your Laravel project structure:

| Source File | Destination in Laravel | Purpose |
|---|---|---|
| `ConstructionAgentService.php` | `app/Services/ConstructionAgentService.php` | HTTP Client service calling Python API |
| `ConstructionEstimateController.php` | `app/Http/Controllers/ConstructionEstimateController.php` | Handles web forms and API requests |
| `estimate.blade.php` | `resources/views/construction/estimate.blade.php` | Beautiful UI with BOQ, metrics, & citations |
| `routes_example.php` | Append to `routes/web.php` | Registers web and API endpoints |

---

## 2. Configure Laravel `.env`

Add these settings to your Laravel `.env` file:

```env
# URL where Python FastAPI agent is running
CONSTRUCTION_AI_URL=http://127.0.0.1:8001
CONSTRUCTION_AI_TIMEOUT=120
```

Also add to `config/services.php` (optional, for clean config):

```php
'construction_ai' => [
    'url'     => env('CONSTRUCTION_AI_URL', 'http://127.0.0.1:8001'),
    'timeout' => env('CONSTRUCTION_AI_TIMEOUT', 120),
],
```

---

## 3. Register Routes in Laravel `routes/web.php`

```php
use App\Http\Controllers\ConstructionEstimateController;

Route::get('/construction/estimate', [ConstructionEstimateController::class, 'index'])->name('construction.estimate');
Route::post('/construction/estimate', [ConstructionEstimateController::class, 'generate'])->name('construction.estimate.generate');
```

---

## 4. Run the Python Agent Server on Windows

Open PowerShell in `c:\rag_agent_core`:

```powershell
cd c:\rag_agent_core
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Interactive API documentation will be accessible at:
- **Swagger Docs:** `http://127.0.0.1:8001/docs`
- **Health Check:** `http://127.0.0.1:8001/api/construction/health`

---

## 5. Direct PHP / Laravel Usage Example

You can call the agent anywhere in your Laravel application (e.g., inside Jobs, Commands, or Controllers):

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
    'currency'     => 'INR',
]);

// Access calculated quantities:
$totalConcrete = $estimate['components'][0]['concrete_volume_m3'];
$totalCost     = $estimate['estimation']['total_estimated_cost'];
$citations     = $estimate['source_references'];
$engineerNotes = $estimate['ai_engineer_analysis'];
```

---

## 6. Accessing the UI in Laravel

Visit `http://localhost:8000/construction/estimate` in your browser.
Enter project dimensions and click **Run Estimation Agent** to see the full estimation report!
