# backend/scripts/init_db.py
"""
Script para inicializar la BD: ejecuta `alembic upgrade head`.
Se puede lanzar desde Dockerfile en el CMD/ENTRYPOINT.
"""

import subprocess
import sys

def main():
    print("Aplicando migraciones Alembic (upgrade head)...")
    result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=False)
    if result.returncode != 0:
        print("Error aplicando migraciones. Código:", result.returncode)
        sys.exit(result.returncode)
    print("Migraciones aplicadas correctamente.")


if __name__ == "__main__":
    main()
