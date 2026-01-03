from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    settings.db.db_url.render_as_string(hide_password=False)
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
