from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def verify_token(token: str):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")