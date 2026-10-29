<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Exception;

class ConstructionAgentService
{
    protected string $baseUrl;
    protected int $timeout;

    public function __construct()
    {
        // Read from config or .env, default to local FastAPI agent server
        $this->baseUrl = rtrim(config('services.construction_ai.url', env('CONSTRUCTION_AI_URL', 'http://127.0.0.1:8001')), '/');
        $this->timeout = (int) config('services.construction_ai.timeout', env('CONSTRUCTION_AI_TIMEOUT', 120));
    }

    /**
     * Call the Python RAG Agent API to calculate bridge construction estimate.
     *
     * @param array $params
     * @return array
     * @throws Exception
     */
    public function getBridgeEstimate(array $params): array
    {
        $payload = [
            'project_type'   => $params['project_type'] ?? 'bridge',
            'bridge_type'    => $params['bridge_type'] ?? 'RCC',
            'length_m'       => (float) ($params['length_m'] ?? 100),
            'width_m'        => (float) ($params['width_m'] ?? 10),
            'height_m'       => (float) ($params['height_m'] ?? 8),
            'location'       => $params['location'] ?? 'Assam, India',
            'currency'       => $params['currency'] ?? 'INR',
            'span_length_m'  => !empty($params['span_length_m']) ? (float)$params['span_length_m'] : null,
            'concrete_grade' => $params['concrete_grade'] ?? 'M35',
            'steel_grade'    => $params['steel_grade'] ?? 'Fe500D',
            'foundation_type'=> !empty($params['foundation_type']) ? $params['foundation_type'] : null,
            'custom_rates'   => $params['custom_rates'] ?? null,
        ];

        try {
            Log::info('Dispatching construction estimation request to Python RAG agent', $payload);

            $response = Http::timeout($this->timeout)
                ->retry(2, 500)
                ->asJson()
                ->acceptJson()
                ->post("{$this->baseUrl}/api/construction/estimate", $payload);

            if ($response->successful()) {
                return $response->json();
            }

            Log::error('Construction RAG Agent responded with error', [
                'status' => $response->status(),
                'body'   => $response->body()
            ]);

            throw new Exception("Agent API Error ({$response->status()}): " . ($response->json('detail') ?? $response->body()));

        } catch (Exception $e) {
            Log::error('Failed to communicate with Construction RAG Agent', [
                'message' => $e->getMessage()
            ]);
            throw $e;
        }
    }

    /**
     * Check health of Python RAG Agent API, pgvector, and Ollama.
     */
    public function checkAgentHealth(): array
    {
        try {
            $response = Http::timeout(5)->get("{$this->baseUrl}/api/construction/health");
            return $response->json();
        } catch (Exception $e) {
            return [
                'status'  => 'offline',
                'message' => 'Python Construction RAG service is not reachable on ' . $this->baseUrl,
                'error'   => $e->getMessage()
            ];
        }
    }

    /**
     * Upload custom specification or BOQ chunk into pgvector knowledge base.
     */
    public function ingestKnowledgeChunk(string $content, string $source, string $category = 'standards', array $metadata = []): array
    {
        $response = Http::timeout(60)->post("{$this->baseUrl}/api/construction/ingest", [
            'content'  => $content,
            'source'   => $source,
            'category' => $category,
            'metadata' => $metadata
        ]);

        return $response->json();
    }
}
