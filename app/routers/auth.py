from fastapi import APIRouter,Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import schemas

from app.db.session import get_db
import app.db.models.user as models
import app.utils as utils
import app.oauth2 as oauth2
#from ..schemas import UserLogin

router  = APIRouter(
    tags=['Authentiation']
)

@router.post("/login",response_model=schemas.Token)
async def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.user_id})
    return {"access_token": access_token, "token_type" : "bearer"}