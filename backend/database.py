from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Password 'Sakshi@2004' URL-encoded (@ → %40)
DATABASE_URL = "mysql+aiomysql://root:Sakshi%402004@localhost:3306/sweetshop"

# Async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
