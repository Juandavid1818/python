from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Hashing de passwords ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# --- JWT ---
def create_access_token(sub: str, expires_minutes: Optional[int] = None):
    exp = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(sub: str, expires_days: Optional[int] = None):
    exp = datetime.utcnow() + timedelta(days=expires_days or settings.REFRESH_TOKEN_EXPIRES_DAYS)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
