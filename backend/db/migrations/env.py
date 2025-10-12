# backend/db/migrations/env.py
"""
Alembic env.py robusto: carga metadata desde models/base y toma DATABASE_URL
desde variables de entorno o core.config. Maneja logging de forma tolerante
para evitar KeyError al ejecutar en contenedores.
"""
import os
import sys
from logging.config import fileConfig
import logging
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# Añadir la raíz del proyecto al path para poder importar core, models, etc.
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

# Intentamos cargar alembic config file si existe
config = context.config

# --- Logging: usar fileConfig si el archivo existe y tiene secciones, sino basicConfig ---
try:
    cfg_file = getattr(config, "config_file_name", None)
    if cfg_file and Path(cfg_file).exists():
        fileConfig(cfg_file)
    else:
        # archivo no encontrado: configurar logging básico para evitar errores con fileConfig
        logging.basicConfig(level=logging.INFO)
except Exception:
    # cualquier fallo en fileConfig no debe detener las migraciones
    logging.basicConfig(level=logging.INFO)

# Importar settings y metadata de nuestros modelos
from core.config import settings  # noqa: E402
from models.base import Base  # noqa: E402

target_metadata = Base.metadata

# Set sqlalchemy.url desde la variable de entorno o settings
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", settings.DATABASE_URL))

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
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
