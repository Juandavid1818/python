# backend/auth/services.py
"""
Lógica de negocio de auth: register, authenticate, token handling.
"""

from sqlalchemy.orm import Session
from core.security import verify_password, create_access_token, create_refresh_token
from auth.repository import get_user_by_email
from auth.repository import create_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_tokens_for_user(user):
    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh}
