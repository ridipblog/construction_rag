from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
import logging
from app.schemas.estimate import BridgeEstimateRequest, EstimateResponse, DocumentIngestRequest
from app.rag.agent import construction_agent
from app.rag.ingest import ingest_text_document, seed_indian_construction_knowledge_base
from app.rag.vector_store import get_document_count
from app.rag.ollama_client import ollama_client
from app.rag.pdf_processor import extract_and_chunk_pdf
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/construction", tags=["Construction Estimation RAG Agent"])

@router.post("/estimate", response_model=EstimateResponse)
async def generate_estimate(request: BridgeEstimateRequest):
    """
    Primary endpoint called by Laravel Construction App.
    Accepts project dimensions and location, retrieves Indian standards via RAG,
    runs civil engineering formulas, and returns itemized material quantities,
    cost analysis, and engineer notes.
    """
    try:
        response = construction_agent.process_estimate(request)
        return response
    except Exception as e:
        logger.error(f"Error processing construction estimate: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Construction Estimation Agent Error: {str(e)}")

@router.post("/ingest")
async def ingest_document(request: DocumentIngestRequest):
    """
    Upload and index custom Indian standards, BOQs, or Schedule of Rates.
    Generates 768-dim embeddings with nomic-embed-text and stores in PostgreSQL pgvector.
    """
    try:
        doc_id = ingest_text_document(
            content=request.content,
            source=request.source,
            category=request.category,
            metadata=request.metadata
        )
        return {"success": True, "document_id": doc_id, "source": request.source}
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-pdf")
async def upload_pdf_document(
    file: UploadFile = File(..., description="PDF document containing standards, rates, or BOQ"),
    category: str = Form("standards", description="Category: standards, schedule_of_rates, or boq")
):
    """
    Upload a PDF document (e.g. Assam PWD SOR, MoRTH specifications, or BOQ drawings).
    Automatically extracts text, creates chunks, computes pgvector embeddings, and saves to database.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported.")

    try:
        file_bytes = await file.read()
        chunks = extract_and_chunk_pdf(file_bytes=file_bytes, filename=file.filename)
        if not chunks:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")

        indexed_count = 0
        for chunk in chunks:
            ingest_text_document(
                content=chunk["content"],
                source=chunk["source"],
                category=category,
                metadata=chunk["metadata"]
            )
            indexed_count += 1

        total_docs = get_document_count()
        return {
            "success": True,
            "filename": file.filename,
            "chunks_indexed": indexed_count,
            "category": category,
            "total_documents_in_db": total_docs
        }
    except Exception as e:
        logger.error(f"Error uploading and indexing PDF {file.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.post("/seed")
async def seed_knowledge_base(force: bool = False):
    """Seed the database with default MoRTH, IRC, Assam PWD SOR, and CPWD DSR references."""
    try:
        result = seed_indian_construction_knowledge_base(force_refresh=force)
        return result
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents_summary():
    """Returns the total number of indexed construction reference documents."""
    count = get_document_count()
    return {
        "total_documents": count,
        "supported_standards": [
            "IRC:112-2020 (Concrete Road Bridges)",
            "IRC:6-2017 (Loads & Seismic Zone V)",
            "MoRTH 5th Rev (Sections 1500, 1600, 1700, 2100, 2200, 2700)",
            "Assam PWD Schedule of Rates 2023-24",
            "CPWD Delhi Schedule of Rates (DSR 2023)"
        ]
    }

@router.get("/documents/all")
async def get_all_documents_in_db():
    """Returns all documents, categories, and sources stored in PostgreSQL pgvector."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, category, source, substring(content from 1 for 150) || '...' as snippet, created_at
                FROM construction_documents
                ORDER BY id ASC;
            """)
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "category": r[1],
                    "source": r[2],
                    "content_preview": r[3],
                    "created_at": str(r[4])
                }
                for r in rows
            ]

@router.get("/health")
async def health_check():
    """Verify status of Database, pgvector, and Ollama."""
    db_status = "error"
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                db_status = "connected"
    except Exception as e:
        db_status = f"unreachable: {str(e)}"

    ollama_status = ollama_client.check_health()
    doc_count = get_document_count()

    return {
        "service": "Construction RAG Estimation Agent API",
        "database": db_status,
        "ollama": ollama_status,
        "indexed_documents_count": doc_count,
        "status": "operational" if db_status == "connected" and ollama_status.get("status") == "online" else "degraded"
    }
