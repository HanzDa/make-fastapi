from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.exceptions.credentials import (
    user_exception,
    token_expired_exception)
from jose import jwt
from app.core.config import settings
from app.core.security import decode_access_token

from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login",
    scheme_name="JWT"
)


async def get_current_user(
        db: AsyncSession = Depends(get_db_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = decode_access_token(token)
        subject = payload.get("subject")
        if not subject:
            raise user_exception
        user: User = await User.get(db_session=db, id=int(subject))
        if user is None:
            raise user_exception
        return user
    except jwt.ExpiredSignatureError:
        raise token_expired_exception


async def get_superuser(
        db: AsyncSession = Depends(get_db_session), token: str = Depends(reusable_oauth2)
) -> User:
    user = await get_current_user(db, token)
    if not user.is_superuser:
        raise user_exception
    return user


