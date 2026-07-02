from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#import os
#from dotenv import load_dotenv
from config import settings

app = FastAPI()

#load_dotenv()

#SECRET_KEY = os.getenv("SECRET_KEY")
origins =  settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.get("/")
def home():
    return{
        "message":"CORS ENABLE API"
    }
