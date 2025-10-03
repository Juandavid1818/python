from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os

app = FastAPI(title="Backend API")

# ----- CORS -----
# En dev: React corre en http://localhost:5173
# En prod: añade el dominio del front (p. ej. https://app.tu-dominio.com)
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Health -----
@app.get("/api/health")
def health():
    return {"ok": True}


# ----- Ejemplo de recurso: Users -----
class User(BaseModel):
    id: int
    email: EmailStr
    name: str


# Basecita en memoria para ejemplo
_USERS = [
    User(id=1, email="neo@matrix.io", name="Neo"),
    User(id=2, email="trinity@matrix.io", name="Trinity"),
]


@app.get("/api/users", response_model=list[User])
def list_users():
    return _USERS


@app.post("/api/users", response_model=User, status_code=201)
def create_user(u: User):
    # Verificar si ya existe ese id
    if any(x.id == u.id for x in _USERS):  
        raise HTTPException(409, "User id already exists")

    _USERS.append(u)
    return u
