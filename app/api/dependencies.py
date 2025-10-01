from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import auth_service

# This will be used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/anonymous")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to get current user from Supabase JWT token
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        dict: User data if authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Get the user from the token using Supabase
        user = await auth_service.get_current_user(token)
        if not user:
            raise credentials_exception
            
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_optional_user(request: Request) -> Optional[dict]:
    """
    Optional dependency that returns the current user if authenticated, None otherwise
    
    This is useful for endpoints that should work both with and without authentication
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
        
    token = auth_header.split(" ")[1]
    try:
        return get_current_user(token)
    except HTTPException:
        return None