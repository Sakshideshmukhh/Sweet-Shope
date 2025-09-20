import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# DATABASE_URL = "mysql+aiomysql://root:Sakshi@2004@localhost:3306/sweetshop"
# Use pymysql for sync creation
DATABASE_URL = "mysql+pymysql://root:Sakshi%402004@localhost:3306/sweetshop"

engine = create_async_engine(DATABASE_URL, echo=True)

async def test():
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT DATABASE();")
            db = result.scalar()
            print("Connected to database:", db)
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
