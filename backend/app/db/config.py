# backend/db/config.py
"""
Configuración de SQLAlchemy: engine, SessionLocal, base metadata.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# create_engine con pool_pre_ping para detectar reconnects
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory (autocommit=False, autoflush=False recomendado)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
