# mcp.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mcp", tags=["MCP"])

class PingRequest(BaseModel):
    prompt: str

@router.post("/ping_llm")
async def ping_llm(request: PingRequest):
    prompt = request.prompt
    reply = f"(Cosmos AI simulated) → Based on your prompt '{prompt}', here's a fake LLM answer."
    return {
        "status": "ok",
        "message": "Simulated LLM response served by MCP",
        "data": {"llm_reply": reply}
    }