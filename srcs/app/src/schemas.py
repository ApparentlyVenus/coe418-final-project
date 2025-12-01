from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List
from models import PlayStatus, Rarity, FriendshipStatus 

# POST /register/ (Input)
class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str
    display_name: Optional[str] = Field(None, max_length=100)

# POST /login/ (Input)
class UserLogin(BaseModel):
    username: str 
    password: str

# GET /profile/{user_id}, POST /register/ (Output)
class UserOut(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    join_date: datetime
    
    class Config:
        from_attributes = True 

# GET /users/{user_id} (Output for public viewing)
class UserPublicOut(BaseModel):
    user_id: str
    username: str
    display_name: Optional[str] = None
    join_date: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)

# POST /games/{igdb_id}/add/ (Input)
class UserGameAdd(BaseModel):
    external_api_id: str = Field(..., description="External game ID for API lookup.")
    play_status: Optional[PlayStatus] = PlayStatus.NOT_STARTED

# PUT /collection/{game_id}/status/ (Input)
class UserGameStatusUpdate(BaseModel):
    play_status: PlayStatus

# PUT /collection/{game_id}/rating/ (Input)
class UserGameRatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Personal rating from 1 to 5.")

# GET /collection/ (Output)
class UserGameOut(BaseModel):
    game_id: str
    title: str
    release_date: Optional[date] = None
    
    # UserGames data
    play_status: PlayStatus
    personal_notes: Optional[str] = None
    rating: Optional[int] = None
    
    class Config:
        from_attributes = True

# Base Achievement Definition (Output for GET /collection/{game_id}/achievements/)
class AchievementOut(BaseModel):
    achievement_id: str
    achievement_name: str
    description: Optional[str] = None
    rarity: Optional[Rarity] = None
    points_value: int
    
    class Config:
        from_attributes = True

# Combined User Achievement Data (Output for GET /collection/{game_id}/achievements/)
class UserAchievementOut(AchievementOut):
    date_earned: datetime

# POST /achievements/{achievement_id}/complete/ (Input - body is optional)
class UserAchievementComplete(BaseModel):
    date_earned: Optional[datetime] = None

# POST /games/{game_id}/reviews/ (Input)
class ReviewCreate(BaseModel):
    review_text: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Review rating from 1 to 5 stars.")

# GET /games/{game_id}/reviews/ (Output)
class ReviewOut(BaseModel):
    review_id: str
    user_id: str
    game_id: str
    review_text: Optional[str] = None
    rating: int
    review_date: datetime
    
    class Config:
        from_attributes = True

# GET /friends/ (Output)
class FriendRequestOut(BaseModel):
    friendship_id: str
    user_id_initiator: str
    user_id_recipient: str
    friendship_date: datetime
    friendship_status: FriendshipStatus
    
    class Config:
        from_attributes = True
        
# POST /sessions/start/ (Input)
class PlaySessionStart(BaseModel):
    game_id: str
    start_time: Optional[datetime] = None 

# PUT /sessions/{session_id}/end/ (Input)
class PlaySessionEnd(BaseModel):
    end_time: Optional[datetime] = None
    session_notes: Optional[str] = None

# Output
class PlaySessionOut(BaseModel):
    session_id: int
    user_id: str
    game_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    session_notes: Optional[str] = None
    
    class Config:
        from_attributes = True