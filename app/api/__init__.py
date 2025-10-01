from fastapi import APIRouter
from app.api.routes import auth, chat, health

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(health.router)