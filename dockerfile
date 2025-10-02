# Usar una versión moderna y ligera de Python
FROM python:3.12-slim

# Evitar archivos pyc y forzar flush de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /usr/src/app

# Instalar dependencias del sistema (si necesitas compilar libs, agrega aquí)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cachear mejor
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]"

# Copiar el resto del código
COPY . /usr/src/app

# Crear usuario no root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
USER appuser

# Cloud Run establece la variable $PORT. No expongas un puerto fijo.
# Usamos shell form para que se expanda ${PORT:-8080} (fallback 8080 en local).
CMD sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}'
