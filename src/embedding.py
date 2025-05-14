from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
import os



def get_embedding_fn():
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY"), "API key not loaded!"
    return OpenAIEmbeddings(model="text-embedding-3-small")

def embed_chunks(chunks):
    embedding_fn = get_embedding_fn()
    texts = [chunk.get("chunk") for chunk in chunks]
    print(f"Embedding {len(texts)} chunks")
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embedding_fn,
        metadatas=[chunk.get("metadata") for chunk in chunks],
        ids=[chunk.get("id") for chunk in chunks],
        persist_directory="chroma_db/"
    )
    vector_store.persist()

def test_embed_subset(chunks):
    embed_chunks(chunks)

def embed_store_data(chunks):
    embed_chunks(chunks)

def query_db(query, k):
    embedding_fn = get_embedding_fn()
    vector_store = Chroma(
        persist_directory="chroma_db/",  
        embedding_function=embedding_fn
    )
    results = vector_store.similarity_search(query, k=k)
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print("Content:", doc.page_content)
        print("Metadata:", doc.metadata)







