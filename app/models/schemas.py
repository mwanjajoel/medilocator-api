from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []
    user_location: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    emergency_details: Optional[Dict[str, Any]] = None
    dispatch_triggered: bool = False
    requires_location: bool = False

class AnonymousUserCreate(BaseModel):
    device_id: Optional[str] = None

class AnonymousUser(BaseModel):
    id: str
    device_id: str
    created_at: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str

class EmergencyDispatch(BaseModel):
    location: str
    incident: str
    victim_count: str
    user_reported_status: str
    user_id: str

class EmergencyLog(BaseModel):
    id: str
    user_id: str
    location: str
    incident: str
    victim_count: str
    user_reported_status: str
    created_at: datetime
    status: str

class ConversationLog(BaseModel):
    id: str
    user_id: str
    user_message: str
    assistant_reply: str
    dispatch_triggered: bool
    created_at: datetime