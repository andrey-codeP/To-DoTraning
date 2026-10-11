from fastapi import APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.depends import SessionDep
from app.schemas.task import TaskResponse, TaskCreate
from app.repository.task import TaskRepository

router = APIRouter(prefix="/task", tags=["task"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: SessionDep):
    task = await TaskRepository.create_task(task, session)
    return task


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_id: int, session: SessionDep):
    task = await TaskRepository.get_task_with_id(task_id, session)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task