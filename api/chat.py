from fastapi import APIRouter
from schemas.chat_models import ChatRequest, ChatResponse
from app.graph import graph
from langchain_core.messages import HumanMessage
import asyncio

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    result = await asyncio.to_thread(
        graph.invoke,
        {"messages": [HumanMessage(content=req.query)]},
        {"configurable": {"thread_id": req.session_id}},
    )

    messages = result.get("messages", [])

    final_answer = messages[-1].content

    return ChatResponse(
        answer=final_answer,
        confidence=0.93, 
        source=["DB", "WEB"],
    )
