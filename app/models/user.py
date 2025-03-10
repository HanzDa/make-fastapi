from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from ..core.security import verify_password
from ..crud.user_crud import UserCRUD


class User(Base, UserCRUD):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                                                 onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active})"

    def authenticate(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)
