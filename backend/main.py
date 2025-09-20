from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, Base, engine
from models import Sweet
from schemas import SweetCreate, SweetResponse
# from auth import router as auth_router  # authentication routes
# from sweets import router as sweets_router
from routers.auth import router as auth_router
from routers.sweets import router as sweets_router

from routers import sweets, auth   # 👈 import routers



# ------------------- APP CONFIG -------------------
app = FastAPI(title="Sweet Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ------------------- STARTUP -------------------
@app.on_event("startup")
async def startup():
    """Create tables if they don’t exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ------------------- ROUTERS -------------------
# app.include_router(auth_router)       # /api/auth/*
# app.include_router(sweets_router)     # /api/sweets/*
# Include routers
app.include_router(auth.router)
app.include_router(sweets.router)


# ------------------- ROOT -------------------
@app.get("/")
async def root():
    return {"message": "Sweet Shop API is running!"}


# ------------------- CRUD ENDPOINTS -------------------

# Create a new sweet
@app.post("/api/sweets", response_model=SweetResponse)
async def create_sweet(sweet: SweetCreate, db: AsyncSession = Depends(get_db)):
    db_sweet = Sweet(**sweet.dict())
    db.add(db_sweet)
    await db.commit()
    await db.refresh(db_sweet)
    return db_sweet


# List all sweets
@app.get("/api/sweets", response_model=List[SweetResponse])
async def get_sweets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        Sweet.__table__.select()
    )
    return result.fetchall()


# Update sweet by ID
@app.put("/api/sweets/{sweet_id}", response_model=SweetResponse)
async def update_sweet(sweet_id: int, sweet_data: SweetCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Sweet.__table__.select().where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    for key, value in sweet_data.dict().items():
        setattr(sweet, key, value)

    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)
    return sweet


# Delete sweet by ID
@app.delete("/api/sweets/{sweet_id}")
async def delete_sweet(sweet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Sweet.__table__.select().where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    await db.delete(sweet)
    await db.commit()
    return {"detail": "Sweet deleted successfully"}


# ------------------- EXTRA ENDPOINTS -------------------

# Search sweets
@app.get("/api/sweets/search", response_model=List[SweetResponse])
async def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    query = Sweet.__table__.select()
    if name:
        query = query.where(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.where(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.where(Sweet.price >= min_price)
    if max_price is not None:
        query = query.where(Sweet.price <= max_price)

    result = await db.execute(query)
    return result.fetchall()


# Purchase a sweet
@app.post("/api/sweets/{sweet_id}/purchase", response_model=SweetResponse)
async def purchase_sweet(sweet_id: int, quantity: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Sweet.__table__.select().where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if sweet.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough quantity in stock")

    sweet.quantity -= quantity
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)
    return sweet


# Restock a sweet
@app.post("/api/sweets/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(sweet_id: int, quantity: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Sweet.__table__.select().where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.quantity += quantity
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)
    return sweet
