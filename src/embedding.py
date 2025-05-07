from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv


def get_embedding_function():
    load_dotenv()
    return OpenAIEmbeddings(model="text-embedding-3-small")




