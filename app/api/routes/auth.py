from fastapi import APIRouter, HTTPException, Depends, status, Response
from app.services.auth_service import auth_service
from app.models.schemas import Token
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["authentication"])

# Security scheme for OpenAPI documentation
security = HTTPBearer()

@router.post("/anonymous", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_anonymous_user_endpoint(response: Response):
    """
    Create an anonymous user and return JWT token
    
    This endpoint creates a new anonymous user in Supabase Auth
    and returns an access token that can be used for subsequent requests.
    
    The token should be included in the Authorization header for protected endpoints:
    ```
    Authorization: Bearer <token>
    ```
    """
    try:
        result, error = await auth_service.sign_in_anonymously()
        if error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )
        
        # Set the Authorization header in the response
        response.headers["Authorization"] = f"Bearer {result['access_token']}"
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create anonymous user: {str(e)}"
        )