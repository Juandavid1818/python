# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.auth.routes import router as auth_router
import os

# ---------------------------------------------------------------
# 🚀 Configuración general del backend
# ---------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="Microservicio backend con FastAPI",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------------
# 🌐 Configuración de CORS
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------
# 🗄️ Configuración de la base de datos
# ---------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ---------------------------------------------------------------
# 🔗 Rutas principales
# ---------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirige a la documentación interactiva."""
    return RedirectResponse(url="/docs")

@app.get("/api/hello")
def hello():
    """Endpoint simple de prueba."""
    return {"message": "Hola, soy tu backend funcionando 🚀"}

@app.get("/api/status")
def status():
    """Verifica el estado general del backend."""
    return {"status": "ok", "detail": "Backend en línea ✅"}

@app.get("/api/db-check")
def db_check():
    """
    Prueba la conexión a la base de datos.
    Ejecuta una consulta mínima y devuelve el estado.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            _ = result.scalar()
        return {"db_status": "ok", "detail": "Conexión exitosa a la base de datos ✅"}
    except SQLAlchemyError as e:
        return {"db_status": "error", "detail": str(e)}

# ---------------------------------------------------------------
# 📦 Rutas de autenticación
# ---------------------------------------------------------------
# Microsoft OAuth, JWT, refresh tokens
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# ---------------------------------------------------------------
# 🔄 Refresh token endpoint (opcional)
# ---------------------------------------------------------------
from fastapi import Body
from app.core.security import decode_token, create_access_token
from app.models.user import User

@app.post("/api/auth/refresh", response_model=dict)
def refresh_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    """
    Refresca un access token usando el refresh token.
    Valida que el refresh token esté activo en la DB.
    """
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Refresh token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or refresh_token not in user.refresh_tokens:
        raise HTTPException(status_code=401, detail="Refresh token expirado o inválido")

    # Crear nuevo access token
    access_token = create_access_token(sub=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------------------------------------------------------
# ✅ Punto de entrada
# ---------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
