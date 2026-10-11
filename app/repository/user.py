from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import UserTable
from app.schemas.user import SUserCreate
from sqlalchemy import select


from app.security import hash_password, verify_hashed_password


class RepositoryUser:
    @classmethod
    async def create_user(cls, user_db: SUserCreate, session: AsyncSession):
        user = user_db.model_dump()

        plain_password=user.pop("password")
        hashed_password = hash_password(plain_password)
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
