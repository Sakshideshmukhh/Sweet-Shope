from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from utils import SECRET_KEY, ALGORITHM

# OAuth2 scheme - looks for "Authorization: Bearer <token>" in request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Verify current logged-in user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch the user from DB
    result = await db.execute(select(User).filter_by(username=username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
