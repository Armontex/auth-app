from fastapi import APIRouter
from services.auth.api.v1 import router as auth_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(auth_router)
