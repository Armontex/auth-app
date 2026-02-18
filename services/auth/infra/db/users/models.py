from datetime import datetime
from sqlalchemy import String, DateTime, func, text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from common.base.db import Base
from services.auth.domain.const import NAME_MAX_LENGTH


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(
        String(NAME_MAX_LENGTH),
    )
    last_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("true"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
