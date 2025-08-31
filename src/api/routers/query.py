from fastapi import APIRouter, HTTPException
from src.schemas.query import QueryRequest, QueryResponse, SourceDoc
from src.deps import get_chain
import asyncio

router = APIRouter(tags=['semantic'])
REQUEST_TIMEOUT = 25

@router.post('/query')
async def query_enpoint(req: QueryRequest) -> QueryResponse: 
    chain = get_chain()
    
    try:
        result = await asyncio.wait_for(
            chain.ainvoke({"input": req.query}),  # the real work
            timeout=REQUEST_TIMEOUT                            # hard cap in seconds
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Model timeout")

    #result = await chain.ainvoke({"input" : req.query})
    #print("RAW OUT:", result)
    answer, docs = normalize_chain_output(result)
    sources = [
        SourceDoc(
            id=d.id,
            metadata=d.metadata,
            snippet=d.page_content[:200]
        )
        for d in docs
    ]
    
    return QueryResponse(
        resp=answer,
        docs=sources
    )

def normalize_chain_output(out):
    """
    Return (answer: str, docs: list[Document]) from common LangChain outputs.
    Never raises; falls back to ("", []).
    """
    # 0) Messages → string
    try:
        from langchain_core.messages import AIMessage
        if isinstance(out, AIMessage):
            return (out.content or ""), []
    except Exception:
        pass

    # 1) Plain string
    if isinstance(out, str):
        return out, []

    # 2) Pydantic-ish
    if hasattr(out, "dict"):
        out = out.dict()

    # 3) Dict-like (most chains)
    if isinstance(out, dict):
        # Prefer explicit keys, then common fallbacks
        answer = (
            out.get("result")
            or out.get("output_text")
            or out.get("answer")
            or out.get("output")
            or out.get("text")
            or ""
        )

        # Sources show up under different keys
        docs = (
            out.get("source_documents")
            or out.get("documents")
            or out.get("context_documents")
            or out.get("context")
            or []
        )

        # Sometimes context is a string blob; treat as answer if we have none
        if not answer and isinstance(docs, str):
            return docs, []

        # Ensure list for docs
        if not isinstance(docs, list):
            docs = []

        return answer, docs

    # 4) Fallback: unknown type
    return str(out), []
    



