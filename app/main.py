from fastapi import FastAPI,Depends
from .routers import user,habits,auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ["*"]
app.add_middleware(
   CORSMiddleware,
   allow_origins  = origins,
   allow_credentials = True,
   allow_methods = ["*"],
   allow_headers = ["*"] 
)
@app.get("/")
async def root():
    return {"message":"Running!!"}


app.include_router(user.router)
app.include_router(habits.router)
app.include_router(auth.router)