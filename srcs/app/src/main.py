from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, create_tables
from models import User

app = FastAPI(title="GameHub API")

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_tables()
    print("Database tables created!")

# Health check
@app.get("/")
async def root():
    return {"message": "GameHub API is running!"}

# User registration
@app.post("/register/")
async def register(username: str, email: str, display_name: str = None, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    new_user = User(
        username=username,
        email=email,
        display_name=display_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "user_id": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
        "display_name": new_user.display_name,
        "join_date": new_user.join_date
    }

# User Profile
@app.get("/profile/{user_id}")
async def get_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)