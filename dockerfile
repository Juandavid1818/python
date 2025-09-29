FROM python:3.9-slim
COPY . usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload