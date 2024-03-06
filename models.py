import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON, String


POSTGRES_USER = os.getenv("POSTGRES_USER", "swapi")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPeople(Base):

    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(100), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(100), nullable=True)
    films: Mapped[str] = mapped_column(String(1000), nullable=True)
    gender: Mapped[str] = mapped_column(String(100), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(100), nullable=True)
    height: Mapped[str] = mapped_column(String(100), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(100), nullable=True)
    mass: Mapped[str] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(100), nullable=True)
    species: Mapped[str] = mapped_column(String(1000), nullable=True)
    starships: Mapped[str] = mapped_column(String(1000), nullable=True)
    vehicles: Mapped[str] = mapped_column(String(1000), nullable=True)
    # json: Mapped[dict] = mapped_column(JSON, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)