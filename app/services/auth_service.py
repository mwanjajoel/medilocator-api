from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
from supabase import Client
from app.core.config import settings
from app.models.database import supabase
from app.core.security import create_access_token
from app.models.schemas import Token

class AuthService:
    def __init__(self, supabase_client: Client = supabase):
        self.supabase = supabase_client

    async def sign_in_anonymously(self) -> Tuple[Optional[Dict], Optional[str]]:
        """Sign in anonymously using Supabase Auth"""
        try:
            # Sign in anonymously
            auth_response = self.supabase.auth.sign_in_anonymously()
            user = auth_response.user
            
            if not user:
                return None, "Failed to create anonymous user"
                
            # Create a token for the user
            access_token = create_access_token(
                data={"sub": user.id},
                expires_delta=timedelta(days=settings.access_token_expire_days)
            )
            
            # Store additional user data in the database
            user_data = {
                "id": user.id,
                "created_at": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat(),
                "is_active": True
            }
            
            # Insert or update the user in the database
            self.supabase.table("anonymous_users").upsert(
                user_data,
                on_conflict="id"
            ).execute()
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id
            }, None
            
        except Exception as e:
            return None, str(e)

    async def get_current_user(self, token: str) -> Optional[Dict]:
        """Get current user from JWT token"""
        try:
            # Verify and decode the JWT token
            from app.core.security import verify_token
            payload = verify_token(token)

            if not payload or "sub" not in payload:
                return None

            user_id = payload["sub"]

            # Get user data from our database
            response = self.supabase.table("anonymous_users")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()

            if not response.data:
                return None

            # Update last activity
            self.supabase.table("anonymous_users")\
                .update({"last_activity": datetime.utcnow().isoformat()})\
                .eq("id", user_id)\
                .execute()

            return response.data

        except Exception as e:
            print(f"Error getting current user: {e}")
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = self.supabase.table("anonymous_users")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

# Initialize the auth service
auth_service = AuthService()