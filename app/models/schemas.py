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

class AnonymousUser(BaseModel):
    """Anonymous user model"""
    id: str
    created_at: datetime
    last_activity: datetime
    is_active: bool

class Token(BaseModel):
    """Authentication token response model"""
    access_token: str
    token_type: str = "bearer"
    user_id: str

class EmergencyDispatch(BaseModel):
    location: str
    incident: str
    victim_count: str
    user_reported_status: str
    user_id: str

class EmergencyLog(BaseModel):
    """Emergency log model"""
    id: str
    anonymous_user_id: str
    location: dict
    incident_type: str
    description: Optional[str] = None
    severity: Optional[int] = None
    status: str = "reported"
    created_at: datetime
    updated_at: datetime

class ConversationMessage(BaseModel):
    """Conversation message model"""
    id: str
    anonymous_user_id: str
    emergency_incident_id: Optional[str] = None
    message_type: str  # 'user_message', 'assistant_reply', 'system_alert'
    content: str
    created_at: datetime