from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

URL = settings.DATABASE_URL

engine = create_async_engine(url=URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
