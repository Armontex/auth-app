from fastapi import APIRouter
from .routers import role_router

router = APIRouter(prefix="/rbac", tags=["rbac"])
router.include_router(role_router)
