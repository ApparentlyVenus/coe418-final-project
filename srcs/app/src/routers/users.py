from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from dependencies import CurrentUser
import schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile/", response_model=schemas.UserOut)
async def get_profile(current_user: CurrentUser):
    return current_user

@router.put("/profile/", response_model=schemas.UserOut)
async def update_profile(
    user_update: schemas.UserUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.user_id != current_user.user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_update.email
    
    if user_update.display_name is not None:
        current_user.display_name = user_update.display_name
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=schemas.UserPublicOut)
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user
