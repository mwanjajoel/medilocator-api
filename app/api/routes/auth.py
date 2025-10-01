from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import auth_service
from app.models.schemas import Token

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/anonymous", response_model=Token)
async def create_anonymous_user_endpoint():
    """
    Create an anonymous user and return JWT token
    
    This endpoint creates a new anonymous user in Supabase Auth
    and returns an access token that can be used for subsequent requests.
    """
    try:
        result, error = await auth_service.sign_in_anonymously()
        if error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create anonymous user: {str(e)}"
        )