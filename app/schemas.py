from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from enum import Enum

class FrequencyEnum(str,Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


# ========== User Schemas ==========


class UserBase(BaseModel):
    username : str
    email : EmailStr
class UserLogin(BaseModel):
    username : str
    password : str

class UserCreate(UserBase):
    password : str
    
class UserResponse(UserBase):
    user_id : int
    created_at : datetime

    class Config:
        from_attributes = True
    
    
# ========== Habit Schemas ==========

class HabitBase(BaseModel):
    title : str
    description : Optional[str] = None
    periodicity : str = "daily"
    
class HabitCreate(HabitBase):
    frequency: FrequencyEnum = FrequencyEnum.daily

class HabitResponse(HabitBase):
    habit_id : int
    user_id : int
    created_at : datetime
    updated_at : datetime
    
    class Config:
        from_attributes = True
        

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    periodicity: Optional[str] = None
    
class HabitProgressResponse(BaseModel):
    progress_id: int
    habit_id: int
    user_id: int
    completed: bool
    completed_at: Optional[datetime] = None
    habit : HabitResponse

    class Config:
        from_attributes = True
        
        
class HabitStreakResponse(BaseModel):
    habit_id : int
    title : str
    frequency :FrequencyEnum
    current_streak : int

    class Config:
        from_attributes = True
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: Optional[int] = None