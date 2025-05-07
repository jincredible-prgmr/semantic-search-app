from langchain.embeddings import OpenAIEmbeddings


def get_embedding_function():
    return OpenAIEmbeddings(model="text-embedding-3-small")




