# backend/auth/routes.py
"""
Rutas de autenticación: register, login, refresh.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.config import SessionLocal
from auth import schemas, services, repository
from auth.schemas import UserCreate, Token, UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if repository.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    user = repository.create_user(db, payload.email, payload.password)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = services.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    tokens = services.create_tokens_for_user(user)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(token: dict):
    # Implementación sencilla: en producción valida token de refresh y rota.
    # Aquí devolvemos un nuevo access token si el refresh es válido.
    from core.security import decode_token, create_access_token

    try:
        payload = decode_token(token.get("refresh_token"))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token no es de tipo refresh")

    user_id = payload.get("sub")
    new_access = create_access_token(subject=user_id)
    new_refresh = create_refresh_token(subject=user_id)
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}
