from fastapi import APIRouter
from src.schemas.query import QueryRequest, QueryResponse, SourceDoc
from src.deps import get_chain

router = APIRouter()

@router.post('/query')
async def query_enpoint(req: QueryRequest) -> QueryResponse: 
    chain = get_chain()
    result = await chain.ainvoke({"input" : req.query})
    print("RAW OUT:", result)
    answer = result.get('answer','')
    sources = [
        SourceDoc(
            id=d.id,
            metadata=d.metadata,
            snippet=d.page_content[:200]
        )
        for d in result.get('context', '')
    ]
    return QueryResponse(
        resp=answer,
        docs=sources
    )




