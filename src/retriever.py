from langchain_openai import ChatOpenAI 
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.embedding import get_vector_store
from src.config import settings


def get_retriever(k=8, search_type="mmr", score_threshold=None, filters=None):
    vs = get_vector_store()
    search_kwargs = {"k": k}
    if score_threshold is not None:
        search_kwargs["score_threshold"] = score_threshold
    if filters is not None:
        search_kwargs["filter"] = filters

    return vs.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )

def get_rag(k=8, search_type='mmr'):
    retriever = get_retriever(k, search_type)
    llm = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=0
    )
    prompt = ChatPromptTemplate.from_template(
        "Use the context to answer the question. Be concise.\n\n"
        "Context:\n{context}\n\nQuestion: {input}"
    )
    doc_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, doc_chain)
    return rag_chain




