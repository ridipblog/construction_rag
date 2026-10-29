<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ConstructionEstimateController;

/*
|--------------------------------------------------------------------------
| Construction Estimation RAG Agent Routes (Copy into routes/web.php or routes/api.php)
|--------------------------------------------------------------------------
*/

// Web routes (UI dashboard)
Route::middleware(['web'])->group(function () {
    Route::get('/construction/estimate', [ConstructionEstimateController::class, 'index'])->name('construction.estimate');
    Route::post('/construction/estimate', [ConstructionEstimateController::class, 'generate'])->name('construction.estimate.generate');
});

// API routes (for mobile app, SPA, or external microservices)
Route::prefix('api/v1/construction')->group(function () {
    Route::post('/estimate', [ConstructionEstimateController::class, 'apiEstimate']);
});
