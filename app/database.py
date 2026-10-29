import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Connection pool for PostgreSQL
_pool: pool.SimpleConnectionPool | None = None

def get_connection_pool():
    global _pool
    if _pool is None:
        try:
            _pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=settings.db_host,
                port=settings.db_port,
                user=settings.db_user,
                password=settings.db_password,
                dbname=settings.db_name
            )
            logger.info("PostgreSQL connection pool created successfully.")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    return _pool

@contextmanager
def get_db():
    conn_pool = get_connection_pool()
    conn = conn_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn_pool.putconn(conn)

def init_db():
    """Ensure vector extension and documents table exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Enable pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create construction_documents table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS construction_documents (
                    id BIGSERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT,
                    category TEXT DEFAULT 'general',
                    metadata JSONB DEFAULT '{}'::jsonb,
                    embedding VECTOR(768),
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Ensure category and metadata columns exist if table was previously created without them
            cur.execute("""
                ALTER TABLE construction_documents 
                ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'general';
            """)
            cur.execute("""
                ALTER TABLE construction_documents 
                ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;
            """)

            # Create an HNSW index on embeddings for fast cosine similarity search
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_construction_docs_embedding 
                ON construction_documents 
                USING hnsw (embedding vector_cosine_ops);
            """)
            
            logger.info("Database schema initialized and verified.")
