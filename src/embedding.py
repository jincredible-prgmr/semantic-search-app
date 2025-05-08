from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import Chroma




def get_embedding_fn():
    load_dotenv()
    return OpenAIEmbeddings(model="text-embedding-3-small")

def embed_store_chunks(chunks):
    embedding_fn = get_embedding_fn()
    vector_store = Chroma.from_texts(
        texts=[chunk.get("chunk") for chunk in chunks],
        embedding=embedding_fn,
        metadatas=[chunk.get("metadata") for chunk in chunks],
        ids=[chunk.get("id") for chunk in chunks],
        persist_directory="chroma_db/"
    )
    vector_store.persist()







