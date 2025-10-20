FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APPLY_MIGRATIONS=1

WORKDIR /usr/src/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias y luego instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Dar permisos al entrypoint
RUN chmod +x docker-entrypoint.sh

# Comando de inicio
CMD ["./docker-entrypoint.sh"]
