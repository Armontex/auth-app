from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.base.db import Base

if TYPE_CHECKING:
    from ..roles.models import Role


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        back_populates="permissions",
        secondary="role_permissions",
        lazy="selectin"
    )