from typing import Optional, Dict
import uuid
from datetime import datetime
from app.models.database import supabase
from app.core.security import create_access_token
from app.models.schemas import AnonymousUserCreate, Token

class AuthService:
    @staticmethod
    def create_anonymous_user(device_id: str) -> Optional[Dict]:
        """Create an anonymous user in Supabase"""
        try:
            user_data = {
                "device_id": device_id,
                "created_at": datetime.utcnow().isoformat(),
                "is_active": True
            }
            
            response = supabase.table("anonymous_users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating anonymous user: {e}")
            return None

    @staticmethod
    def get_anonymous_user(device_id: str) -> Optional[Dict]:
        """Get anonymous user by device ID"""
        try:
            response = supabase.table("anonymous_users")\
                .select("*")\
                .eq("device_id", device_id)\
                .eq("is_active", True)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting anonymous user: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = supabase.table("anonymous_users")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    def authenticate_anonymous_user(request: AnonymousUserCreate = None) -> Token:
        """Authenticate or create anonymous user and return token"""
        device_id = request.device_id if request and request.device_id else str(uuid.uuid4())
        
        # Check if user already exists
        existing_user = AuthService.get_anonymous_user(device_id)
        if existing_user:
            user_id = existing_user["id"]
        else:
            # Create new anonymous user
            new_user = AuthService.create_anonymous_user(device_id)
            if not new_user:
                raise Exception("Could not create anonymous user")
            user_id = new_user["id"]
        
        # Create access token
        access_token = create_access_token(data={"sub": user_id})
        return Token(access_token=access_token, token_type="bearer", user_id=user_id)

auth_service = AuthService()