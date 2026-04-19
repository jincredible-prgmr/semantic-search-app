import chromadb
from config import CHROMA_DB_PATH, COLLECTION_NAME


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def add_chunks(chunks: list, embedding_fn, batch_size: int = 100):
    collection = get_collection()
    total = len(chunks)

    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["chunk"] for c in batch]
        embeddings = embedding_fn.embed_documents(texts)
        collection.add(
            ids=[c["id"] for c in batch],
            documents=texts,
            embeddings=embeddings,
            metadatas=[c["metadata"] for c in batch],
        )
        print(f"Ingested {min(i + batch_size, total)}/{total} chunks")


def query(query_text: str, embedding_fn, n_results: int = 5, category: str = None):
    collection = get_collection()
    query_embedding = embedding_fn.embed_query(query_text)
    where = {"category": category} if category else None

    kwargs = dict(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    if where:
        kwargs["where"] = where

    return collection.query(**kwargs)


def collection_count() -> int:
    return get_collection().count()
