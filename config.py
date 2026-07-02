import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    origins =  os.getenv(ORIGINS)

settings = Settings()