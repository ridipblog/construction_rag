import logging
from typing import List, Dict, Any, Optional
from app.rag.ollama_client import ollama_client
from app.rag.vector_store import insert_document, get_document_count, clear_documents
from app.rag.seed_data import INDIAN_CONSTRUCTION_DOCUMENTS

logger = logging.getLogger(__name__)

def ingest_text_document(
    content: str,
    source: str,
    category: str = "standards",
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """Embeds and indexes a single document chunk into pgvector."""
    logger.info(f"Generating embedding for doc: {source} ({category})")
    embedding = ollama_client.get_embedding(content)
    doc_id = insert_document(
        content=content,
        source=source,
        category=category,
        embedding=embedding,
        metadata=metadata
    )
    return doc_id

def seed_indian_construction_knowledge_base(force_refresh: bool = False) -> Dict[str, Any]:
    """
    Populates PostgreSQL pgvector with curated Indian Standards,
    MoRTH specs, and Assam PWD rates.
    """
    current_count = get_document_count()
    if current_count > 0 and not force_refresh:
        logger.info(f"Knowledge base already contains {current_count} documents. Skipping re-seed.")
        return {"status": "skipped", "document_count": current_count}

    if force_refresh:
        logger.info("Clearing existing documents for force refresh...")
        clear_documents()

    indexed_count = 0
    for doc in INDIAN_CONSTRUCTION_DOCUMENTS:
        try:
            ingest_text_document(
                content=doc["content"],
                source=doc["source"],
                category=doc.get("category", "standards"),
                metadata=doc.get("metadata", {})
            )
            indexed_count += 1
        except Exception as e:
            logger.error(f"Failed to index {doc.get('source')}: {e}")

    logger.info(f"Successfully seeded {indexed_count} Indian construction reference documents.")
    return {
        "status": "success",
        "indexed_count": indexed_count,
        "total_documents": get_document_count()
    }
