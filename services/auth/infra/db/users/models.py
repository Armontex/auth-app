from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, func, text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.base.db import Base

if TYPE_CHECKING:
    from services.profile.infra.db.profiles.models import Profile
    from services.rbac.infra.db.roles.models import Role


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index(
            "unique_users_email_active",
            "email",
            unique=True,
            postgresql_where=text("is_active"),
        ),  # Только один активный пользователь на email. Неактивных - хоть сколько
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("true"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    roles: Mapped[list["Role"]] = relationship(
        back_populates="users", secondary="user_roles", lazy="selectin"
    )
