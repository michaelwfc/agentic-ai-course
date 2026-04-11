from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List
from agents.chat_agents import SimpleChatAgent

chat_api = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    thread_id: str = "t001"
    
class ResumeRequest(BaseModel):
    approved: bool
    thread_id: str = "t001"
    


@chat_api.post("/chat")
async def chat_endpoint(chat_request: ChatRequest, req: Request) -> Dict[str, str|bool]:
    # Simple echo response for now
    agent:SimpleChatAgent = req.app.state.chat_agent
    
    need_approval = agent.run_until_approval(chat_request.messages, chat_request.thread_id)
    return {"need_approval": need_approval,
            "response": agent.get_last_message(chat_request.thread_id)
            }


@chat_api.post("/resume")
async def resume_endpoint(resume_request: ResumeRequest, req: Request) -> Dict[str, str|bool]:
    # Simple echo response for now
    agent = req.app.state.chat_agent
    
    response = agent.resume(resume_request.approved, resume_request.thread_id)
    
    return {
        "need_approval": False,
        "response": response,
   
    }


@chat_api.get("/health")
async def health_check():
    return {"status": "healthy"}