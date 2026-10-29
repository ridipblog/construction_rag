import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.rag.ingest import seed_indian_construction_knowledge_base
from app.rag.vector_store import get_document_count
from app.api.estimate import router as estimate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("construction_rag_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Construction RAG Agent Database & Knowledge Base...")
    try:
        init_db()
        count = get_document_count()
        if count == 0:
            logger.info("Database empty on startup. Automatically seeding Indian Construction Standards...")
            seed_indian_construction_knowledge_base()
        else:
            logger.info(f"Database ready with {count} Indian Construction Standards.")
    except Exception as e:
        logger.error(f"Error during startup initialization: {e}")
    yield
    logger.info("Shutting down Construction RAG Agent...")

app = FastAPI(
    title="Construction Estimation RAG Agent API",
    description=(
        "FastAPI AI Agent for Indian Bridge & Infrastructure Estimation. "
        "Integrates PostgreSQL + pgvector, Ollama (nomic-embed-text & llama3.2), "
        "deterministic civil engineering calculations, and Laravel HTTP client integration."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Laravel application calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Laravel app running on localhost:8000 or any domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estimate_router)

@app.get("/")
def read_root():
    return {
        "service": "Construction RAG Estimation Agent",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "estimate": "POST /api/construction/estimate",
            "health": "GET /api/construction/health",
            "documents": "GET /api/construction/documents",
            "ingest": "POST /api/construction/ingest",
            "seed": "POST /api/construction/seed"
        }
    }
