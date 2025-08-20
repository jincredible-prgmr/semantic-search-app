from pydantic import BaseModel
from typing import List, Optional

class SourceDoc(BaseModel):
    id: Optional[str] = None
    metadata: dict = {}
    snippet: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    k: int = 6              # default number of docs
    search_type: str = "mmr"

class QueryResponse(BaseModel):
    resp: str
    docs: List[SourceDoc]
