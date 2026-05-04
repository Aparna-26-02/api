from fastapi import APIRouter, HTTPException
from models.schemas import Login
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
import logging

# Load environment variables
load_dotenv()

router = APIRouter()

# Env variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")   

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Safety check
if not SECRET_KEY:
    raise Exception("SECRET_KEY not set in .env")


# 🔐 Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔑 Login API
@router.post("/login")
def login(user: Login):
    if user.username == ADMIN_USERNAME and user.password == ADMIN_PASSWORD:
        logging.info(f"Login success for user: {user.username}")

        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    logging.warning(f"Login failed for user: {user.username}")
    raise HTTPException(status_code=401, detail="Invalid username or password")