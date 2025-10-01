from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import auth_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/anonymous")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to get current user from Supabase JWT token
    
    Args:
        token: Bearer token extracted from Authorization header by OAuth2PasswordBearer
        
    Returns:
        dict: User data if authenticated
        
    Raises:
        HTTPException: If authentication fails
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user = await auth_service.get_current_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )