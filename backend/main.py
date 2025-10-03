from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Backend API",
    description="Microservicio backend con FastAPI",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ Endpoint raíz: en lugar de 404, responde algo útil o redirige
@app.get("/", include_in_schema=False)
def root_redirect():
    # Si prefieres redirigir al swagger:
    return RedirectResponse(url="/docs")
    # O si prefieres mostrar un JSON en lugar de redirigir, comenta la línea de arriba y descomenta esto:
    # return {"service": "backend", "status": "ok", "docs": "/docs", "api": "/api"}

# ✅ Ejemplo de endpoint de API
@app.get("/api/hello")
def hello():
    return {"message": "Hola, soy tu backend funcionando 🚀"}

# ✅ Otro ejemplo de API (útil para probar desde el front)
@app.get("/api/status")
def status():
    return {"status": "ok", "detail": "Backend en línea"}
