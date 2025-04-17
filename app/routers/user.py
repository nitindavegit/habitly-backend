from fastapi import FastAPI,Response,status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session


from app import schemas
from app.db.session import get_db
from app.db.models import user as models
from app import utils

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate,db : Session = Depends(get_db)):
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username :
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail=f"Username '{user.username}' is already taken")
    
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Email '{user.email}' is already registered")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/search",response_model=schemas.UserResponse)
async def get_user(username : str, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    return user