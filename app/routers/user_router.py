from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt  # type: ignore
from tortoise.exceptions import IntegrityError

from app.models.users import User
from app.schemas.users import RegisterUserRequest, TokenResponse, UserResponse
from app.utils.auth import authenticate
from app.utils.jwt import create_access_token, create_refresh_token

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register")
async def register(user: RegisterUserRequest) -> UserResponse:
    try:
        created_user = await User.create(username=user.username, password_hash=bcrypt.hash(user.password))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")

    return UserResponse(id=created_user.id, username=created_user.username)


@user_router.post("/login")
async def login(login_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    user = await authenticate(login_data.username, login_data.password)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
