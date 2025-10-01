from fastapi import APIRouter
from app.core.config import settings
from app.api.dependencies import get_current_user
from app.services.emergency_service import emergency_service

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "Medilocator Chat API with Supabase",
        "version": settings.api_version
    }

@router.get("/user/emergencies")
async def get_user_emergencies(current_user: dict = Depends(get_current_user)):
    """Get emergencies for the current user"""
    emergencies = emergency_service.get_user_emergencies(current_user["id"])
    return {"emergencies": emergencies}