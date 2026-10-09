from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import UserTable
from app.schemas.user import SUserCreate
from sqlalchemy import select


class RepositoryUser:
    @classmethod
    async def create_user(cls, user_db: SUserCreate, session: AsyncSession):
        user = user_db.model_dump()

        hashed_password = user["password"]
        user.pop("password")
        user["hashed_password"] = hashed_password

        user_db = UserTable(**user)

        session.add(user_db)

        await session.commit()
        await session.refresh(user_db)

        return user_db

    @classmethod
    async def get_user(cls, user_id, session: AsyncSession):
        query = select(UserTable).where(UserTable.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
