from fastapi import FastAPI
from app.routers.auth import router as auth_router

app = FastAPI(
    title="To-Do List Training", description="To-Do List Training", version="1.0"
)


app.include_router(auth_router)
