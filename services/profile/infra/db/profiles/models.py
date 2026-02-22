from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.base.db import Base

from services.profile.domain.const import NAME_MAX_LENGTH

if TYPE_CHECKING:
    from services.auth.infra.db.users.models import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(
        String(NAME_MAX_LENGTH),
    )
    last_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)

    user: Mapped["User"] = relationship(back_populates="profile")
