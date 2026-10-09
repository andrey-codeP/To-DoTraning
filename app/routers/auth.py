from fastapi import APIRouter
from app.schemas.user import SUserCreate, SUserResponse
from app.database.depends import SessionDep
from app.repository.user import RepositoryUser
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", response_model=SUserResponse)
async def registry(user: SUserCreate, session: SessionDep) -> SUserResponse:
    user_in_db = await RepositoryUser.create_user(user, session)
    return user_in_db