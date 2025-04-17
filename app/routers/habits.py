from fastapi import FastAPI,Response,status, HTTPException,Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from ..import oauth2
from app import schemas
from app.db.session import get_db
from app.db.models import habit as habit_models
from app.db.models import user as user_models
from app import utils
from typing import List
from datetime import datetime,timedelta
from app.schemas import FrequencyEnum
import enum

router = APIRouter(
    prefix="/habits",
    tags = ['Habits']
)

# CREATE a new habit

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.HabitResponse)
async def create_habit(habit : schemas.HabitCreate, db : Session = Depends(get_db),current_user : user_models.User = Depends(oauth2.get_current_user)):
    # Map 'periodicity' to 'frequency'
    habit.frequency = FrequencyEnum(habit.periodicity)  # Directly assign periodicity to frequency
    new_habit = habit_models.Habit(**habit.model_dump())
    new_habit.user_id = current_user.user_id
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

# READ all habits
@router.get("/",response_model=list[schemas.HabitResponse])
async def get_all_habits(db : Session = Depends(get_db),current_user : user_models.User = Depends(oauth2.get_current_user)):
    habits = db.query(habit_models.Habit).filter(habit_models.Habit.user_id == current_user.user_id).all()
    return habits



# Habit streaks
@router.get("/streak", response_model=List[schemas.HabitStreakResponse])
async def get_habit_streak(db:Session = Depends(get_db),current_user:user_models.User = Depends(oauth2.get_current_user)):
    # check habit ownership
    habits = db.query(habit_models.Habit).filter(habit_models.Habit.user_id == current_user.user_id).all()
    if not habits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    # return streaks
    streaks = []
    for habit in habits:
        streak = db.query(habit_models.HabitProgress).filter(habit_models.HabitProgress.habit_id == habit.habit_id,habit_models.HabitProgress.user_id == current_user.user_id,habit_models.HabitProgress.completed == True).order_by(habit_models.HabitProgress.completed_at.desc()).all()
        dates = [s.completed_at.date() for s in streak]
        today = datetime.now().date()
        streak_count = 0
        if habit.frequency.value == "daily":
            while dates and (today - timedelta(days=streak_count)) in dates:
                streak_count += 1
                
        elif habit.frequency.value == "weekly":
            current_week = today.isocalendar().week
            current_year = today.isocalendar().year
            seen_weeks = set((d.isocalendar().year, d.isocalendar().week) for d in dates)
            while(current_year, current_week) in seen_weeks:
                streak_count += 1
                current_week -= 1
                if current_week == 0:
                    current_year -= 1
                    current_week = 52
        
        elif habit.frequency.value == "monthly":
            current_month = today.month
            current_year = today.year
            seen_months = set((d.year,d.month) for d in dates)
            while(current_year, current_month) in seen_months:
                streak_count +=1
                current_month -= 1
                if current_month == 0:
                    current_month = 12
                    current_year -= 1
        
        streaks.append({
            "habit_id": habit.habit_id,
            "title": habit.title,
            "frequency": habit.frequency,
            "current_streak": streak_count
        })
        
    return streaks




# READ habit by ID
@router.get("/{habit_id}",response_model=schemas.HabitResponse)
async def get_habit(habit_id : int, db : Session = Depends(get_db),current_user : user_models.User = Depends(oauth2.get_current_user)):
    habit = db.query(habit_models.Habit).filter(habit_models.Habit.habit_id == habit_id,habit_models.Habit.user_id == current_user.user_id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    return habit



# UPDATE habit
@router.put("/{habit_id}",response_model=schemas.HabitResponse)
async def update_habit(habit_id : int, updated_habit : schemas.HabitUpdate, db : Session = Depends(get_db),current_user : user_models.User = Depends(oauth2.get_current_user)):
    habit_query = db.query(habit_models.Habit).filter(habit_models.Habit.habit_id == habit_id,habit_models.Habit.user_id == current_user.user_id)
    habit = habit_query.first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    habit_query.update(updated_habit.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return habit_query.first()



# DELETE habit
@router.delete("/{habit_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id : int, db : Session = Depends(get_db),current_user : user_models.User = Depends(oauth2.get_current_user)):
    habit_query = db.query(habit_models.Habit).filter(habit_models.Habit.habit_id == habit_id,habit_models.Habit.user_id == current_user.user_id)
    habit = habit_query.first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    habit_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Habit deleted successfully"})


# Record habit completion
@router.post("/{habit_id}/complete", response_model=schemas.HabitProgressResponse)
async def mark_habit_completed(habit_id:int,db:Session = Depends(get_db),current_user:user_models.User = Depends(oauth2.get_current_user)):
    habit = db.query(habit_models.Habit).filter(habit_models.Habit.habit_id == habit_id,habit_models.Habit.user_id == current_user.user_id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    # Record the completion for today
    progress = habit_models.HabitProgress(habit_id=habit_id,user_id=current_user.user_id,completed=True,completed_at = text('now()'))
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress
    
    
    
# Get progress for a specific habit
@router.get("/{habit_id}/progress", response_model=List[schemas.HabitProgressResponse])
async def get_habit_progress(habit_id:int,db:Session = Depends(get_db),current_user:user_models.User = Depends(oauth2.get_current_user)):
    # check habit ownership
    habit = db.query(habit_models.Habit).filter(habit_models.Habit.habit_id == habit_id,habit_models.Habit.user_id == current_user.user_id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Habit with id {habit_id} not found or not owned by the user")
    # Fetch progress records
    progress_records = db.query(habit_models.HabitProgress).filter(habit_models.HabitProgress.habit_id == habit_id,habit_models.HabitProgress.user_id == current_user.user_id).order_by(habit_models.HabitProgress.completed_at.desc()).all()
    # If no progress records, create a default one
    if not progress_records:
        return  [{
            "progress_id": 0,
            "habit_id": habit_id,
            "user_id": current_user.user_id,
            "completed": False,
            "completed_at": None,
            "habit": habit
        }]
    return progress_records

