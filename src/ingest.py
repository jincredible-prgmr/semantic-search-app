"""
ingest.py

Run this once to embed all Elden Ring data and persist it to ChromaDB.
Requires OPENAI_API_KEY in environment or a .env file.

Usage:
    python ingest.py
"""

from dotenv import load_dotenv
load_dotenv()

from load_data import load_data
from embedding import get_embedding_function
from vector_store import add_chunks, collection_count


def main():
    existing = collection_count()
    if existing > 0:
        print(f"Collection already contains {existing} chunks. Use --force to re-ingest.")
        return

    print("Loading and chunking data...")
    chunks = load_data()
    print(f"Loaded {len(chunks)} chunks across all categories.")

    print("Embedding and storing (this calls the OpenAI API)...")
    embedding_fn = get_embedding_function()
    add_chunks(chunks, embedding_fn)
    print(f"Done. {collection_count()} chunks stored in ChromaDB.")


if __name__ == "__main__":
    import sys
    if "--force" in sys.argv:
        import chromadb
        from config import CHROMA_DB_PATH, COLLECTION_NAME
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        client.delete_collection(COLLECTION_NAME)
        print("Cleared existing collection.")
    main()
