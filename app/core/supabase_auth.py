"""
Supabase authentication utilities
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from supabase import Client
from app.core.config import settings
from app.models.database import supabase

class SupabaseAuth:
    """Handles Supabase authentication operations"""
    
    def __init__(self, supabase_client: Client = supabase):
        self.supabase = supabase_client
    
    async def get_user(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get user from Supabase using JWT token
        
        Args:
            token: JWT access token
            
        Returns:
            Optional[Dict]: User data if valid, None otherwise
        """
        try:
            # Verify the token with Supabase
            user = self.supabase.auth.get_user(token)
            if not user or not user.user:
                return None
                
            # Get additional user data from our database
            response = self.supabase.table("anonymous_users")\
                .select("*")\
                .eq("id", user.user.id)\
                .single()\
                .execute()
                
            if not response.data:
                return None
                
            # Update last activity
            self.supabase.table("anonymous_users")\
                .update({"last_activity": "now()"})\
                .eq("id", user.user.id)\
                .execute()
                
            return response.data
            
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None
    
    async def sign_in_anonymously(self) -> Dict[str, Any]:
        """
        Sign in anonymously using Supabase Auth
        
        Returns:
            Dict: {
                'access_token': str,
                'token_type': 'bearer',
                'user': Dict
            }
        """
        try:
            # Sign in anonymously
            auth_response = self.supabase.auth.sign_in_anonymously()
            user = auth_response.user
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create anonymous user"
                )
            
            # Store/update user in our database
            user_data = {
                "id": user.id,
                "is_active": True
            }
            
            self.supabase.table("anonymous_users")\
                .upsert(user_data, on_conflict="id")\
                .execute()
            
            return {
                "access_token": auth_response.session.access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "is_anonymous": True
                }
            }
            
        except Exception as e:
            print(f"Error in sign_in_anonymously: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to sign in anonymously: {str(e)}"
            )

# Create a singleton instance
supabase_auth = SupabaseAuth()
