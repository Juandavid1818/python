# backend/auth/utils.py
"""
Funciones utilitarias para auth (por ejemplo, extraer user desde token).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_token
from db.config import SessionLocal
from auth.repository import get_user_by_email

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    db = SessionLocal()
    try:
        # en este ejemplo buscamos por id convertido a int (si lo guardaste así)
        user = db.query.__self__.query // placeholder
    finally:
        db.close()
