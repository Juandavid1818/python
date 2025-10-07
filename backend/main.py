from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Backend API",
    description="Microservicio backend con FastAPI",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Configuración de la base de datos ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://appuser:apppass@db:5432/appdb")

# Crea el motor SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# ✅ Endpoint raíz
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")


# ✅ Ejemplo de endpoint básico
@app.get("/api/hello")
def hello():
    return {"message": "Hola, soy tu backend funcionando 🚀"}


# ✅ Endpoint de estado general
@app.get("/api/status")
def status():
    return {"status": "ok", "detail": "Backend en línea"}


# ✅ Nuevo endpoint: prueba de conexión con la base de datos
@app.get("/api/db-check")
def db_check():
    """
    Intenta conectarse a la base de datos y ejecutar una consulta mínima.
    Devuelve 'ok' si la conexión funciona, o un error si falla.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            _ = result.scalar()
        return {"db_status": "ok", "detail": "Conexión exitosa a la base de datos ✅"}
    except SQLAlchemyError as e:
        return {"db_status": "error", "detail": str(e)}
