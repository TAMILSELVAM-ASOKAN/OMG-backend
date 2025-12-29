from pydantic import BaseModel, Field
from typing import List

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="User Session ID")
    query: str = Field(..., description="User query")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Agent response")
    confidence: float = Field(..., ge=0, le=1)
    source: List[str] = Field(..., description="DB | WEB | RAG")
