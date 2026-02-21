from fastapi import APIRouter

from .routers import (
    login_router,
    logout_router,
    delete_user_router,
    change_email_router,
    change_password_router,
)

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(login_router)
router.include_router(logout_router)
router.include_router(delete_user_router)
router.include_router(change_email_router)
router.include_router(change_password_router)
