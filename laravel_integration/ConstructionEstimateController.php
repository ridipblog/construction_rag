<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\ConstructionAgentService;
use Exception;

class ConstructionEstimateController extends Controller
{
    protected ConstructionAgentService $agentService;

    public function __construct(ConstructionAgentService $agentService)
    {
        $this->agentService = $agentService;
    }

    /**
     * Display the Construction Estimate Dashboard & Input Form.
     */
    public function index()
    {
        $health = $this->agentService->checkAgentHealth();
        return view('construction.estimate', [
            'estimate' => session('current_estimate'),
            'inputs'   => session('estimate_inputs', [
                'project_type'   => 'bridge',
                'bridge_type'    => 'RCC',
                'length_m'       => 100,
                'width_m'        => 10,
                'height_m'       => 8,
                'location'       => 'Assam, India',
                'concrete_grade' => 'M35',
                'steel_grade'    => 'Fe500D'
            ]),
            'agentHealth' => $health
        ]);
    }

    /**
     * Handle the estimation form submission or AJAX request.
     */
    public function generate(Request $request)
    {
        $validated = $request->validate([
            'project_type'    => 'required|string',
            'bridge_type'     => 'required|string',
            'length_m'        => 'required|numeric|min:5|max:5000',
            'width_m'         => 'required|numeric|min:3|max:60',
            'height_m'        => 'required|numeric|min:2|max:100',
            'location'        => 'required|string|max:200',
            'span_length_m'   => 'nullable|numeric|min:5|max:150',
            'concrete_grade'  => 'nullable|string',
            'steel_grade'     => 'nullable|string',
            'foundation_type' => 'nullable|string',
        ]);

        try {
            $estimateData = $this->agentService->getBridgeEstimate($validated);

            if ($request->wantsJson()) {
                return response()->json($estimateData);
            }

            return redirect()->route('construction.estimate')
                ->with('current_estimate', $estimateData)
                ->with('estimate_inputs', $validated)
                ->with('success', 'Bridge estimation and RAG analysis generated successfully!');

        } catch (Exception $e) {
            if ($request->wantsJson()) {
                return response()->json([
                    'success' => false,
                    'error'   => $e->getMessage()
                ], 500);
            }

            return back()->withInput()->with('error', 'Failed to generate estimate: ' . $e->getMessage());
        }
    }

    /**
     * API Endpoint for other apps or mobile clients.
     */
    public function apiEstimate(Request $request)
    {
        $validated = $request->validate([
            'project_type' => 'required|string',
            'bridge_type'  => 'required|string',
            'length_m'     => 'required|numeric|min:1',
            'width_m'      => 'required|numeric|min:1',
            'height_m'     => 'required|numeric|min:1',
            'location'     => 'required|string',
        ]);

        try {
            $data = $this->agentService->getBridgeEstimate($validated);
            return response()->json($data);
        } catch (Exception $e) {
            return response()->json([
                'success' => false,
                'error'   => $e->getMessage()
            ], 500);
        }
    }
}
