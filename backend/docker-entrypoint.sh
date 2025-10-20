#!/bin/sh
set -euo pipefail

echo "✅ Iniciando entrypoint del backend..."

# --- tu parseo de DATABASE_URL (igual que antes) ---
DB_URL=${DATABASE_URL#postgresql+psycopg2://}
DB_USER=$(echo $DB_URL | cut -d':' -f1)
DB_PASS=$(echo $DB_URL | cut -d':' -f2 | cut -d'@' -f1)
DB_HOST=$(echo $DB_URL | cut -d'@' -f2 | cut -d':' -f1)
DB_PORT=$(echo $DB_URL | cut -d':' -f3 | cut -d'/' -f1)
DB_NAME=$(echo $DB_URL | cut -d'/' -f2)

export PGPASSWORD=$DB_PASS

# Esperar DB
echo "⏳ Esperando a PostgreSQL en $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; do
  echo "Esperando DB..."
  sleep 2
done
echo "✅ PostgreSQL listo"

# --- MIGRACIONES ---
if [ "${APPLY_MIGRATIONS:-0}" = "1" ]; then
  echo "🔄 Preparando carpeta de migraciones persistente..."
  mkdir -p /app/alembic/versions
  touch /app/alembic/versions/.keep || true

  # Obtener revision desde BD (si existe)
  DB_REV=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -A -c "SELECT version_num FROM alembic_version LIMIT 1;" 2>/dev/null || echo "")

  if [ -n "$DB_REV" ]; then
    if ! ls /app/alembic/versions/*"$DB_REV"* >/dev/null 2>&1; then
      echo "⚠️ La BD referencia la revision $DB_REV, que no existe localmente. Creando placeholder..."
      alembic -c app/alembic.ini revision --rev-id "$DB_REV" -m "placeholder for missing $DB_REV" || true
      echo "✔ Placeholder creado en /app/alembic/versions (revisar y commitear si aplica)."
    fi
  fi

  echo "📌 Marcando estado local como cabeza (stamp head)..."
  alembic -c app/alembic.ini stamp head || true

  echo "🔁 Autogenerando migración si hay cambios..."
  alembic -c app/alembic.ini revision --autogenerate -m "auto" || echo "⚡ Sin cambios detectados"

  echo "⬆️ Ejecutando upgrade head..."
  alembic -c app/alembic.ini upgrade head && echo "✅ Migraciones aplicadas"
fi

# Iniciar servidor
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
