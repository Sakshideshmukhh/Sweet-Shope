from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models import Sweet, User
from schemas import SweetCreate, SweetResponse
from dependencies import get_current_user

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])


# Create sweet (admin only)
@router.post("/", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def create_sweet(
    sweet: SweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can add sweets")

    result = await db.execute(select(Sweet).filter_by(name=sweet.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Sweet already exists")

    db_sweet = Sweet(**sweet.dict())
    db.add(db_sweet)
    await db.commit()
    await db.refresh(db_sweet)
    return db_sweet


# Get all sweets (any logged-in user)
@router.get("/", response_model=List[SweetResponse])
async def get_sweets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Sweet))
    return result.scalars().all()


# Get sweet by ID (any logged-in user)
@router.get("/{sweet_id}", response_model=SweetResponse)
async def get_sweet(
    sweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Sweet).where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return sweet


# Update sweet (admin only)
@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(
    sweet_id: int,
    sweet_data: SweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update sweets")

    result = await db.execute(select(Sweet).where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    for key, value in sweet_data.dict().items():
        setattr(sweet, key, value)

    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)
    return sweet


# Delete sweet (admin only)
@router.delete("/{sweet_id}", status_code=status.HTTP_200_OK)
async def delete_sweet(
    sweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete sweets")

    result = await db.execute(select(Sweet).where(Sweet.id == sweet_id))
    sweet = result.scalar_one_or_none()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    await db.delete(sweet)
    await db.commit()
    return {"message": "Sweet deleted successfully"}
