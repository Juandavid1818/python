from sqlalchemy import Column, String, Boolean, DateTime, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=True)  # opcional, Microsoft puede no enviar
    email = Column(String, unique=True, nullable=False)    # obligatorio, de dominio permitido
    microsoft_id = Column(String, unique=True, nullable=False)  # ID de usuario de Microsoft

    # Estados del usuario
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)  # Microsoft ya valida email

    # Seguridad adicional
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    two_factor_secret = Column(String, nullable=True)   # Para 2FA futura

    # Sesiones persistentes
    refresh_tokens = Column(ARRAY(String), default=[])  # Tokens activos de sesión
    session_logs = Column(ARRAY(String), default=[])    # Registro de sesiones con device/ip
    last_login = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
