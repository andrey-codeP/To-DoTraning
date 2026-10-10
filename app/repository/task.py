from sqlalchemy import select
from app.schemas.task import TaskCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.task import TaskTable


from datetime import datetime, timezone


class TaskRepository:
    @classmethod
    async def create_task(cls, task: TaskCreate, session: AsyncSession):
        task_from_user = task.model_dump()
        now = datetime.now(timezone.utc)
        task_from_user["created_at"] = now
        task = TaskTable(**task_from_user)

        session.add(task)

        await session.commit()
        await session.refresh(task)

        return task

    @classmethod
    async def get_task_with_id(cls, task_id: int, session: AsyncSession):
        query = select(TaskTable).where(TaskTable.id == task_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
