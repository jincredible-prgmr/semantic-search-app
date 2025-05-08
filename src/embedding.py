from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
import os



def get_embedding_fn():
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY"), "API key not loaded!"
    return OpenAIEmbeddings(model="text-embedding-3-small")

def embed_store_chunks(chunks):
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







