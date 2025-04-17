from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from sqlalchemy.orm import relationship
 

class User (Base):  
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String, nullable=False)
    username = Column(String,nullable=False,unique=True)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False, server_default=text('now()'))
    progress = relationship("HabitProgress", back_populates="user")
    habits = relationship("Habit", back_populates="user")