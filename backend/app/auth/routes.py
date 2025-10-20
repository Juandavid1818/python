from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import Token, UserRead
from app.models.user import User
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from fastapi.responses import RedirectResponse
import httpx
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MICROSOFT_USER_URL = "https://graph.microsoft.com/v1.0/me"

@router.get("/login/microsoft")
def microsoft_login(code: str, db: Session = Depends(get_db)):
    """
    Endpoint de callback de Microsoft OAuth.
    Recibe code -> obtiene token -> obtiene user -> valida dominio
    """
    # 1️⃣ Obtener token
    data = {
        "client_id": settings.MICROSOFT_CLIENT_ID,
        "client_secret": settings.MICROSOFT_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5173/auth/microsoft/callback"
    }
    resp = httpx.post(MICROSOFT_TOKEN_URL, data=data)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Microsoft login failed")
    token_data = resp.json()
    access_token_microsoft = token_data["access_token"]

    # 2️⃣ Obtener info de usuario
    headers = {"Authorization": f"Bearer {access_token_microsoft}"}
    user_resp = httpx.get(MICROSOFT_USER_URL, headers=headers).json()
    email = user_resp.get("mail") or user_resp.get("userPrincipalName")

    # 3️⃣ Validar dominio
    if not email.endswith(f"@{settings.MICROSOFT_ALLOWED_DOMAIN}"):
        raise HTTPException(status_code=403, detail="Dominio no permitido")

    # 4️⃣ Buscar o crear usuario
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(username=email.split("@")[0], email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 5️⃣ Crear tokens JWT
    access_token = create_access_token(sub=str(user.id))
    refresh_token = create_refresh_token(sub=str(user.id))

    # Guardar refresh token en la DB
    user.refresh_tokens.append(refresh_token)
    db.commit()

    return Token(access_token=access_token, refresh_token=refresh_token)
