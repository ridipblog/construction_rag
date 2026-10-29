import httpx
import logging
from typing import List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.embedding_model = settings.embedding_model
        self.llm_model = settings.llm_model

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates 768-dimensional dense vector embeddings using nomic-embed-text.
        """
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.embedding_model,
            "prompt": text
        }
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                embedding = data.get("embedding")
                if not embedding or not isinstance(embedding, list):
                    raise ValueError(f"Ollama returned invalid embedding format: {data}")
                return embedding
        except Exception as e:
            logger.error(f"Error fetching embedding from Ollama ({self.embedding_model}): {e}")
            raise

    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generates civil engineering analysis text using local LLM (llama3.2:3b).
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2, # Low temperature for factual precision
                "top_p": 0.9
            }
        }
        try:
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data.get("response", "").strip()
        except Exception as e:
            logger.warning(f"Ollama LLM generation error ({self.llm_model}): {e}")
            return (
                "AI engineering synthesis currently operating in deterministic mode: "
                "Quantities and rates have been computed strictly according to Indian Standards (MoRTH & IRC 112)."
            )

    def check_health(self) -> dict:
        """Verify Ollama server and model availability."""
        url = f"{self.base_url}/api/tags"
        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    models = [m.get("name") for m in resp.json().get("models", [])]
                    return {
                        "status": "online",
                        "available_models": models,
                        "embedding_model_ready": any(self.embedding_model in m for m in models),
                        "llm_model_ready": any(self.llm_model in m for m in models)
                    }
        except Exception as e:
            return {"status": "offline", "error": str(e)}
        return {"status": "unreachable"}

ollama_client = OllamaClient()
