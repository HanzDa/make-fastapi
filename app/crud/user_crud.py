from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseCRUD
from .base_crud import ModelType
from ..core.security import get_password_hash


class UserCRUD(BaseCRUD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    async def create(cls, *, db_session: AsyncSession, commit: bool = True, **kwargs) -> ModelType:
        hashed_password = get_password_hash(kwargs.pop("password"))
        kwargs["hashed_password"] = hashed_password
        return await super().create(db_session=db_session, commit=commit, **kwargs)
