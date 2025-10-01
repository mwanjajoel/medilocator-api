import json
from typing import List, Dict, Any
from app.utils.openai_client import openai_client
from app.models.schemas import ChatResponse

class ChatService:
    # System prompt for Medilocator
    SYSTEM_PROMPT = """
    You are Medilocator, a critical emergency medical response assistant. Your primary goal is to extract specific, actionable information from the user as quickly and calmly as possible to dispatch an ambulance.

    **CRITICAL RULES:**
    1. **Identify Emergency:** Immediately determine if the situation is life-threatening (e.g., chest pain, choking, unconsciousness, severe bleeding).
    2. **Extract Key Information:** You MUST get these three pieces of information before anything else:
       a. **Location:** The exact address or a description of where the emergency is happening.
       b. **Nature of Emergency:** What is happening? (e.g., "heart attack," "car accident," "difficulty breathing").
       c. **Number of People:** How many people need help?
    3. **Be Direct and Calming:** Use short, clear sentences. Guide the user. For example: "I'm getting you help. What is your exact address?" or "Stay with me. Is the person conscious?"
    4. **DO NOT** diagnose the medical condition. Your role is to relay accurate information to human responders.
    5. **DO NOT** provide medical advice. Do not tell them how to perform CPR; instead, if they ask, state "I can connect you to a professional who can guide you through CPR until the ambulance arrives."

    Once you have confirmed the Location, Nature of Emergency, and Number of People, you MUST respond with a very specific JSON format and then stop the conversation. The JSON is:

    {
      "confirmation": "Help is on the way. An ambulance has been dispatched to [Confirmed Address]. Please wait for further instructions.",
      "emergency_details": {
        "location": "[The extracted location]",
        "incident": "[The extracted nature of emergency]",
        "victim_count": "[Number of people]",
        "user_reported_status": "[e.g., conscious, bleeding, not breathing]"
      },
      "next_step": "A professional may call you on the number we have on file. Please keep your phone free and unlocked.",
      "dispatch_triggered": true
    }

    If you don't have all the required information, respond with normal text to continue gathering information.
    """

    @staticmethod
    async def process_chat_message(
        message: str,
        conversation_history: List[Dict],
        user_location: Dict[str, Any] = None
    ) -> ChatResponse:
        """Process chat message through OpenAI and return structured response"""
        try:
            # Prepare messages for OpenAI
            messages = ChatService._prepare_messages(message, conversation_history, user_location)
            
            # Call OpenAI API
            response_text = await openai_client.chat_completion(messages)
            
            # Parse the response
            return ChatService._parse_openai_response(response_text)
            
        except Exception as e:
            return ChatResponse(
                reply="I'm having trouble connecting right now. Please call emergency services directly at 911 immediately and provide your location and the nature of the emergency.",
                emergency_details=None,
                dispatch_triggered=False,
                requires_location=False
            )

    @staticmethod
    def _prepare_messages(
        user_message: str,
        conversation_history: List[Dict],
        user_location: Dict[str, Any] = None
    ) -> List[Dict]:
        """Prepare messages for OpenAI API"""
        messages = [{"role": "system", "content": ChatService.SYSTEM_PROMPT}]
        
        # Add location context if available
        if user_location:
            location_context = f"User location data: {user_location}. Use this to help confirm their address."
            messages.append({"role": "system", "content": location_context})
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages

    @staticmethod
    def _parse_openai_response(response_text: str) -> ChatResponse:
        """Parse OpenAI response to detect dispatch triggers or normal responses"""
        # Check if the response is a JSON dispatch trigger
        if response_text.strip().startswith('{') and 'emergency_details' in response_text:
            try:
                dispatch_data = json.loads(response_text)
                return ChatResponse(
                    reply=dispatch_data['confirmation'],
                    emergency_details=dispatch_data['emergency_details'],
                    dispatch_triggered=True,
                    requires_location=False
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, treat as normal response
                pass
        
        # Normal text response
        return ChatResponse(
            reply=response_text,
            emergency_details=None,
            dispatch_triggered=False,
            requires_location=ChatService._should_request_location(response_text)
        )

    @staticmethod
    def _should_request_location(response_text: str) -> bool:
        """Simple heuristic to detect if the AI is asking for location"""
        location_keywords = ['location', 'address', 'where are you', 'your location', 'where is this']
        return any(keyword in response_text.lower() for keyword in location_keywords)

chat_service = ChatService()