from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from app.schemas.user import SUserCreate, SUserResponse
from app.database.depends import SessionDep
from app.repository.user import RepositoryUser

from app.security import verify_hashed_password
from app.security.login import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=SUserResponse
)
async def registry(user: SUserCreate, session: SessionDep) -> SUserResponse:
    created_user = await RepositoryUser.create_user(user, session)
    return created_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    username = user.username
    user_db = await RepositoryUser.get_user_by_username(username, session)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED_NOT_FOUND,
            detail="incorrect password or username",
        )

    password = user.password

    if not verify_hashed_password(password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect password or username",
        )

    user_id = user_db.id

    access_token = create_access_token(user_id)

    return {"access_token": access_token, "token_type": "bearer"}
