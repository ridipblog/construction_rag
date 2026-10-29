import json
import logging
from typing import List, Dict, Any, Optional
from pgvector.psycopg2 import register_vector
from app.database import get_db

logger = logging.getLogger(__name__)

def insert_document(
    content: str,
    source: str,
    embedding: List[float],
    category: str = "standards",
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """Inserts a document chunk with vector embedding into PostgreSQL."""
    metadata_json = json.dumps(metadata or {})
    with get_db() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO construction_documents 
                (content, source, category, metadata, embedding)
                VALUES (%s, %s, %s, %s, %s::vector)
                RETURNING id;
            """, (content, source, category, metadata_json, embedding))
            doc_id = cur.fetchone()[0]
            return doc_id

def search_similar_documents(
    query_embedding: List[float],
    limit: int = 5,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Finds top matching Indian construction standards and rate items
    using pgvector cosine distance (<=> operator).
    """
    with get_db() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            if category:
                query = """
                    SELECT id, content, source, category, metadata,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM construction_documents
                    WHERE category = %s
                    ORDER BY embedding <=> %s::vector ASC
                    LIMIT %s;
                """
                cur.execute(query, (query_embedding, category, query_embedding, limit))
            else:
                query = """
                    SELECT id, content, source, category, metadata,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM construction_documents
                    ORDER BY embedding <=> %s::vector ASC
                    LIMIT %s;
                """
                cur.execute(query, (query_embedding, query_embedding, limit))

            rows = cur.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "content": row[1],
                    "source": row[2],
                    "category": row[3],
                    "metadata": row[4],
                    "similarity": round(float(row[5]), 4) if row[5] is not None else 0.0
                })
            return results

def get_document_count() -> int:
    """Returns total indexed construction reference documents."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM construction_documents;")
            return cur.fetchone()[0]

def clear_documents():
    """Clears all indexed documents (used for re-indexing)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE construction_documents RESTART IDENTITY;")
