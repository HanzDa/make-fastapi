from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.core.config import settings
from app.core.security import create_access_token
from app.deps.user_deps import get_current_user
from app.exceptions.credentials import credential_exception
from app.models.user import User
from app.schemas.user import UserCreateSchema, TokenSchema, UserGetSchema

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenSchema)
async def login_for_access_token(
        db: AsyncSession = Depends(get_db_session),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> JSONResponse:
    user: User = await User.get(db_session=db, email=form_data.username)
    if not user or not user.authenticate(form_data.password):
        raise credential_exception

    access_token = create_access_token(subject=user.id)
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response


@router.post("/logout", dependencies=[Depends(get_current_user)])
async def logout(response: JSONResponse) -> JSONResponse:
    response.delete_cookie(key="access_token")
    return response


@router.get("/me", response_model=UserGetSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserGetSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
        userIn: UserCreateSchema,
        db: AsyncSession = Depends(get_db_session)
) -> User:
    new_user: User = await User.create(db_session=db, **userIn.model_dump())
    return new_user
