import sys
import logging
from app.database import init_db
from app.rag.ingest import seed_indian_construction_knowledge_base
from app.rag.vector_store import get_document_count, search_similar_documents
from app.rag.ollama_client import ollama_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

def main():
    print("=" * 60)
    print("Seeding Indian Construction Standards into pgvector...")
    print("=" * 60)

    # 1. Initialize schema & extensions
    init_db()

    # 2. Seed documents
    result = seed_indian_construction_knowledge_base(force_refresh=True)
    print(f"Result: {result}")

    total = get_document_count()
    print(f"Total reference documents in PostgreSQL: {total}")

    # 3. Test vector similarity retrieval
    test_query = "Bridge superstructure M35 concrete Fe500D rebar Assam"
    print(f"\nTesting vector similarity search for: '{test_query}'")
    query_emb = ollama_client.get_embedding(test_query)
    matches = search_similar_documents(query_emb, limit=3)
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} (Similarity: {match['similarity']:.4f}) ---")
        print(f"Source: {match['source']}")
        print(f"Snippet: {match['content'][:180]}...")

    print("\nKnowledge base verified and ready!")

if __name__ == "__main__":
    main()
