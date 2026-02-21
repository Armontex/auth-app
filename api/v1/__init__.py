from fastapi import APIRouter

from services.auth.api.v1 import router as auth_router
from services.register.api.v1 import router as register_router

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(auth_router)
router.include_router(register_router)