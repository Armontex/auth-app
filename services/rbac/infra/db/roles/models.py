from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.base.db import Base

if TYPE_CHECKING:
    from ..permissions.models import Permission
    from services.auth.infra.db.users.models import User


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="roles", secondary="role_permissions", lazy="selectin"
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="roles", secondary="user_roles", lazy="selectin"
    )
