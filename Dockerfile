# Usar una versión moderna y ligera de Python
FROM python:3.12-slim

# Evitar archivos pyc y forzar flush de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (Opcional) orígenes CORS por defecto para dev
ENV CORS_ORIGINS="http://localhost:5173"

# Crear directorio de la app
WORKDIR /usr/src/app

# Dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]"

# Copiar el resto del código
COPY . /usr/src/app

# Usuario no root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
USER appuser

# Healthcheck simple (ajusta si quieres)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://127.0.0.1:${PORT:-8080}/api/health || exit 1

# Cloud Run usa $PORT (no EXPOSE necesario)
CMD sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}'
