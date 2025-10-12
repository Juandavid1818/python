# backend/Dockerfile (actualizado)
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

# crear usuario no privilegiado
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
USER appuser

# CMD: ejecuta migraciones (si APPLY_MIGRATIONS=1) y luego uvicorn
CMD sh -c 'if [ "${APPLY_MIGRATIONS}" = "1" ]; then python scripts/init_db.py; fi && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}'
