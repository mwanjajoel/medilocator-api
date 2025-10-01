from typing import List, Optional, Dict
from datetime import datetime
from app.models.database import supabase

class EmergencyService:
    @staticmethod
    def log_emergency(emergency_data: Dict, user_id: str) -> Optional[Dict]:
        """Log emergency to Supabase"""
        try:
            emergency_log = {
                "user_id": user_id,
                "location": emergency_data.get("location", ""),
                "incident": emergency_data.get("incident", ""),
                "victim_count": emergency_data.get("victim_count", ""),
                "user_reported_status": emergency_data.get("user_reported_status", ""),
                "created_at": datetime.utcnow().isoformat(),
                "status": "dispatched"
            }
            
            response = supabase.table("emergency_logs").insert(emergency_log).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error logging emergency: {e}")
            return None

    @staticmethod
    def get_user_emergencies(user_id: str) -> List[Dict]:
        """Get emergencies for a specific user"""
        try:
            response = supabase.table("emergency_logs")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user emergencies: {e}")
            return []

    @staticmethod
    def log_conversation(
        user_id: str,
        user_message: str,
        assistant_reply: str,
        dispatch_triggered: bool = False
    ) -> Optional[Dict]:
        """Log conversation to Supabase"""
        try:
            conversation_log = {
                "user_id": user_id,
                "user_message": user_message,
                "assistant_reply": assistant_reply,
                "dispatch_triggered": dispatch_triggered,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("conversation_messages").insert(conversation_log).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error logging conversation: {e}")
            return None

emergency_service = EmergencyService()