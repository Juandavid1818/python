# backend/app/auth/schemas.py
"""
Schemas Pydantic para autenticación y usuarios.
Incluye creación, lectura y tokens JWT.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# --- Usuario que se crea desde frontend ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # contraseña en texto plano, se hasheará en backend

# --- Usuario que se retorna (lectura) ---
class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    is_verified: bool
    failed_login_attempts: int
    locked_until: Optional[datetime] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Usuario con sesión y refresh tokens ---
class UserSession(UserRead):
    refresh_tokens: List[str] = []
    session_logs: List[str] = []

# --- Tokens JWT ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# --- Esquema para login (solo email y password) ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str
