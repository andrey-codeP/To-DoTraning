from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends, Cookie
from typing import Annotated
import jwt

from datetime import datetime, timezone, timedelta

from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
    }
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(settings.EXPIRE_ACCESS_FROM_MINUTES)
    )
    payload.update({"exp": expire_time})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
    }
    expire_time = datetime.now(timezone.utc) + timedelta(
        days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    payload.update({"exp": expire_time})
    encoded_token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_token


def get_current_user_by_id(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])

        if encoded_jwt["type"] != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = int(encoded_jwt["sub"])

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="the token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_with_refersh_token(
    refresh_token: Annotated[str | None, Cookie(default=None, alias="refresh_token")],
):
    try:
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid or expired token",
            )
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid or expired token",
            )
        user_id = int(payload["sub"])
        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

VerifUserId = Annotated[int, Depends(get_current_user_by_id)]