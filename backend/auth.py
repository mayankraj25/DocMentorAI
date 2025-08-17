from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET=os.get("JWT_SECRET","secret")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str)-> bool:
    return pwd_context.verify(plain,hashed)

def create_access_token(sub: str,expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"sub":sub,"exp":expire}
    return jwt.encode(payload,JWT_SECRET,alogorith=JWT_ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token,JWT_SECRET,alogoriths=[JWT_ALGORITHM])  