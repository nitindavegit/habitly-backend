from sqlalchemy import Column, Integer, String, ForeignKey,DateTime,Boolean,Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum
from app.schemas import FrequencyEnum

class Habit (Base):
    __tablename__ = "habits"
    habit_id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable = True)
    periodicity = Column(String,default="daily")
    created_at = Column(TIMESTAMP(timezone = True),nullable = False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
    frequency = Column(Enum(FrequencyEnum,name = 'frequencyenum'),nullable=False)
    progress = relationship("HabitProgress", back_populates="habit")
    user = relationship("User", back_populates="habits")
    

class HabitProgress(Base):
    __tablename__ = "habit_progress"
    
    progress_id = Column(Integer,primary_key=True,nullable=False,index=True)
    habit_id = Column(Integer,ForeignKey("habits.habit_id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    completed = Column(Boolean,default=True,nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    habit = relationship("Habit",back_populates="progress")
    user = relationship("User",back_populates="progress")