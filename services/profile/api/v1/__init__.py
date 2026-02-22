from fastapi import APIRouter
from .routers import update_router

router = APIRouter(prefix="/profile", tags=["profile"])
router.include_router(update_router)