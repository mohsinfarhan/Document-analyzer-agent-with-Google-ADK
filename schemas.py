from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]