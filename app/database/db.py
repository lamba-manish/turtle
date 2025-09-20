from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create async engine
engine = create_async_engine(
    DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=True,
    future=True,
)

# Create async session
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Create declarative base
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
