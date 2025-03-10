from fastapi import HTTPException
from typing import TypeVar, Generic, Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.exceptions.crud import integrity_exception

ModelType = TypeVar("ModelType", bound=Base)


async def commit_transaction(*, db_session: AsyncSession, instance: Any, exception: HTTPException) -> None:
    try:
        await db_session.commit()
        await db_session.refresh(instance)
    except IntegrityError:
        await db_session.rollback()
        raise exception


class BaseCRUD(Generic[ModelType]):
    def __init__(self, *args, **kwargs):
        pass

    def __await__(self):
        yield self

    @classmethod
    async def get(cls, *, db_session: AsyncSession, **kwargs) -> ModelType | None:
        query = select(cls).filter_by(**kwargs)
        result = await db_session.scalars(query)
        return result.first()

    @classmethod
    async def get_all(cls,
                      *,
                      db_session: AsyncSession,
                      start: int | None = None,
                      limit: int | None = None,
                      **kwargs) -> list[ModelType]:
        query = select(cls).filter_by(**kwargs)
        if start is not None:
            query = query.offset(start)
        if limit is not None:
            query = query.limit(limit)
        result = await db_session.scalars(query)
        return result.all()  # type: ignore

    @classmethod
    async def create(cls, *, db_session: AsyncSession, commit: bool = True, **kwargs) -> ModelType:
        obj = cls(**kwargs)
        db_session.add(obj)
        if commit:
            await commit_transaction(db_session=db_session, instance=obj, exception=integrity_exception)
        return obj  # type: ignore

    async def update(self, *, db_session: AsyncSession, commit: bool = True, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(self, key, value)
        if commit:
            await commit_transaction(db_session=db_session, instance=self, exception=integrity_exception)
        return self  # type: ignore

    async def delete(self, *, db_session: AsyncSession) -> None:
        await db_session.delete(self)
        await db_session.commit()
