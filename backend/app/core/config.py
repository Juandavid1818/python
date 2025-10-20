# backend/app/core/config.py
"""
Configuración central del proyecto (producción segura).
Todas las credenciales y secretos deben estar en el archivo .env.
CORS_ORIGINS se normaliza automáticamente a list[str].
"""

from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # --- General ---
    APP_NAME: str
    ENVIRONMENT: str
    PORT: int

    # --- Database ---
    DATABASE_URL: str

    # --- JWT ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_DAYS: int

    # --- Microsoft OAuth ---
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    MICROSOFT_ALLOWED_DOMAIN: str  # solo emails de este dominio

    # --- CORS ---
    CORS_ORIGINS: str  # puede ser JSON array, CSV o single origin

    class Config:
        env_file = ".env"
        case_sensitive = True

    # --- Helpers ---
    def _parse_origins(self, raw: str) -> List[str]:
        """Parsea CORS_ORIGINS desde JSON array, CSV o single origin."""
        if not raw:
            return []
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = json.loads(raw)
                return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                pass
        return [p.strip() for p in raw.split(",") if p.strip()]

    @property
    def cors_origins(self) -> List[str]:
        return self._parse_origins(self.CORS_ORIGINS)


# Instancia global de settings
settings = Settings()
