from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.core.security import verify_token
from app.services.auth_service import auth_service

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Dependency to get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token.credentials)
    if not payload:
        raise credentials_exception
        
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = auth_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    return user