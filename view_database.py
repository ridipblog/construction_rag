import sys
sys.stdout.reconfigure(encoding='utf-8')
from app.database import get_db
from app.rag.vector_store import get_document_count

def display_database_contents():
    total = get_document_count()
    print("=" * 80)
    print(f"POSTGRESQL PGVECTOR DATABASE: {total} DOCUMENTS STORED")
    print("=" * 80)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    id, 
                    category, 
                    source, 
                    content, 
                    metadata,
                    embedding::text,
                    created_at
                FROM construction_documents
                ORDER BY id ASC;
            """)
            rows = cur.fetchall()

            for row in rows:
                doc_id = row[0]
                category = row[1]
                source = row[2]
                content = row[3]
                metadata = row[4]
                vector_str = row[5]
                created_at = row[6]

                # Parse vector sample
                vector_preview = vector_str[:60] + "...]" if vector_str else "None"
                # Count dimensions
                vector_dims = len(vector_str.strip("[]").split(",")) if vector_str else 0

                print(f"\n[DOCUMENT ID: #{doc_id}]")
                print(f"Category:   {category.upper()}")
                print(f"Source:     {source}")
                print(f"Created At: {created_at}")
                print(f"Metadata:   {metadata}")
                print(f"Embedding:  {vector_dims}-dimensional dense vector: {vector_preview}")
                print("-" * 80)
                print("CONTENT:")
                print(content.strip())
                print("=" * 80)

if __name__ == "__main__":
    display_database_contents()
