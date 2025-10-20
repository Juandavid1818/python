import os
import sys
from logging.config import fileConfig
import logging
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# Añadir la raíz del proyecto al path
BASE_DIR = Path(__file__).resolve().parents[3]  # backend/
sys.path.append(str(BASE_DIR / "app"))

# Config Alembic
config = context.config

# Logging
try:
    cfg_file = getattr(config, "config_file_name", None)
    if cfg_file and Path(cfg_file).exists():
        fileConfig(cfg_file)
    else:
        logging.basicConfig(level=logging.INFO)
except Exception:
    logging.basicConfig(level=logging.INFO)

# Importar settings y metadata de Base (todos los modelos)
from core.config import settings
from models.base import Base           # <-- Base central
from models.user import User           # <-- Modelos individuales

# Metadata para Alembic
target_metadata = Base.metadata

# URL DB
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", settings.DATABASE_URL))

def run_migrations_offline():
    """Run migrations en modo offline"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations en modo online"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
