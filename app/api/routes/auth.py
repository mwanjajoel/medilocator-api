from fastapi import APIRouter, HTTPException
from app.services.auth_service import auth_service
from app.models.schemas import AnonymousUserCreate, Token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/anonymous", response_model=Token)
async def create_anonymous_user_endpoint(request: AnonymousUserCreate = None):
    """Create an anonymous user and return JWT token"""
    try:
        return auth_service.authenticate_anonymous_user(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))