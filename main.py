from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)
