from typing import override
from passlib.context import CryptContext
from services.auth.app.ports import IPasswordHasher


class PasswordHasher(IPasswordHasher):

    def __init__(self) -> None:
        self._pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @override
    def hash(self, password: str) -> str:
        return self._pwd_ctx.hash(password)

    @override
    def verify(self, password: str, password_hash: str) -> bool:
        return self._pwd_ctx.verify(password, password_hash)
