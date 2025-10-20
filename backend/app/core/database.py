# backend/app/core/database.py
"""
Conexión a la base de datos usando SQLAlchemy.
Incluye Base para modelos y sesión global.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# --- Motor de SQLAlchemy ---
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # True para debug SQL
    future=True,
)

# --- Sesión de base de datos ---
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# --- Base para todos los modelos ---
Base = declarative_base()

# --- Dependencia para FastAPI ---
def get_db():
    """
    Yield de sesión para endpoints de FastAPI.
    Uso:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
