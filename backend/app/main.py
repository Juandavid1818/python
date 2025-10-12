# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
import os

# ---------------------------------------------------------------
# 🚀 Configuración general del backend
# ---------------------------------------------------------------
app = FastAPI(
    title="Backend API",
    description="Microservicio backend con FastAPI",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------------
# 🌐 Configuración de CORS
# ---------------------------------------------------------------
# Esto permite que el frontend (React/Vite) pueda comunicarse con el backend
# sin ser bloqueado por el navegador.
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

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
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://appuser:apppass@db:5432/appdb"
)

# Crea el motor SQLAlchemy (con ping automático para evitar conexiones rotas)
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
# 📦 Integración futura: módulos (auth, usuarios, etc.)
# ---------------------------------------------------------------
# from auth.routes import router as auth_router
# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
#
# Más adelante se podrán incluir aquí otros routers (ej. /api/users)

# ---------------------------------------------------------------
# ✅ Punto de entrada
# ---------------------------------------------------------------
# Este archivo será ejecutado automáticamente por Uvicorn dentro del contenedor.
# No es necesario modificar el CMD del Dockerfile.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
