# backend/core/config.py
"""
Configuración central del proyecto.
CORS_ORIGINS puede venir como:
 - JSON array: '["http://a","http://b"]'
 - CSV: "http://a,http://b"
 - Single origin: "http://localhost:5173"
La propiedad `cors_origins` normaliza todo a list[str].
"""

from pydantic_settings import BaseSettings
import json
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Backend API"
    ENVIRONMENT: str = "development"
    PORT: int = 8080

    # DB
    DATABASE_URL: str = "postgresql+psycopg2://appuser:apppass@db:5432/appdb"

    # Seguridad / JWT
    JWT_SECRET_KEY: str = "CAMBIA_ESTA_SECRETO_POR_PRODUCCION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30

    # Recibimos CORS_ORIGINS como string y la normalizamos mediante la propiedad cors_origins
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def _parse_origins(self, raw: str) -> List[str]:
        """Intenta parsear raw como JSON array, si falla lo trata como CSV o single value."""
        if not raw:
            return []
        raw = raw.strip()
        # Si parece JSON array, intentar parsear
        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = json.loads(raw)
                # Asegurar que sean strings
                return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                # caído el JSON, continuar con CSV fallback
                pass
        # CSV / single value fallback
        return [p.strip() for p in raw.split(",") if p.strip()]

    @property
    def cors_origins(self) -> List[str]:
        """Lista normalizada de orígenes para usar en CORS middleware."""
        return self._parse_origins(self.CORS_ORIGINS)


# Instancia global de settings que importarán otros módulos
settings = Settings()
