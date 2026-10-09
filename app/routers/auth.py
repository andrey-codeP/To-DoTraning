from fastapi import APIRouter, status
from app.schemas.user import SUserCreate, SUserResponse
from app.database.depends import SessionDep
from app.repository.user import RepositoryUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=SUserResponse
)
async def registry(user: SUserCreate, session: SessionDep) -> SUserResponse:
    user_in_db = await RepositoryUser.create_user(user, session)
    return user_in_db
