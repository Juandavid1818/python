# backend/auth/repository.py
"""
Operaciones CRUD básicas sobre User.
"""

from sqlalchemy.orm import Session

from auth.models import User
from core.security import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str, is_superuser: bool = False) -> User:
    hashed = hash_password(password)
    user = User(email=email, hashed_password=hashed, is_superuser=is_superuser)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
