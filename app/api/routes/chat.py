from fastapi import APIRouter, Depends, HTTPException
from app.services.chat_service import chat_service
from app.services.emergency_service import emergency_service
from app.api.dependencies import get_current_user
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_with_medilocator(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Main endpoint for the Medilocator chat interface"""
    try:
        # Process chat message
        chat_response = await chat_service.process_chat_message(
            message=request.message,
            conversation_history=[msg.dict() for msg in request.conversation_history],
            user_location=request.user_location
        )
        
        # Log the conversation
        emergency_service.log_conversation(
            user_id=current_user["id"],
            user_message=request.message,
            assistant_reply=chat_response.reply,
            dispatch_triggered=chat_response.dispatch_triggered
        )
        
        # Log emergency if dispatch was triggered
        if chat_response.dispatch_triggered and chat_response.emergency_details:
            emergency_service.log_emergency(
                chat_response.emergency_details,
                current_user["id"]
            )
        
        return chat_response
        
    except Exception as e:
        # Log the error
        emergency_service.log_conversation(
            user_id=current_user["id"],
            user_message=request.message,
            assistant_reply=f"Error: {str(e)}",
            dispatch_triggered=False
        )
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")