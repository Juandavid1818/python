# backend/Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CORS_ORIGINS="http://localhost:5173" \
    APPLY_MIGRATIONS=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends curl gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD sh -c 'if [ "${APPLY_MIGRATIONS}" = "1" ]; then alembic -c app/alembic.ini upgrade head || { echo "❌ Migraciones fallaron; abortando."; exit 1; }; fi; exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}'
