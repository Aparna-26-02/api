from fastapi import APIRouter, HTTPException
from models.schemas import Login
from dotenv import load_dotenv
import os
import logging

load_dotenv()

router = APIRouter()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

@router.post("/login")
def login(user: Login):
    if user.username == ADMIN_USERNAME and user.password == ADMIN_PASSWORD:
        logging.info("Login success")
        return {"token": SECRET_TOKEN}

    logging.error("Login failed")
    raise HTTPException(status_code=401, detail="Invalid username or password")