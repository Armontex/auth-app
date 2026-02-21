from fastapi import APIRouter
from .routers import register_router


router = APIRouter(prefix="/register", tags=["register"])

router.include_router(register_router)
