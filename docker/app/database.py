import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CONFIGURACIÓN DE LA URL DE CONEXIÓN
# Si DATABASE_URL está definida en el entorno (por ejemplo MySQL en Docker), la usaremos. En caso contrario, arrancamos con SQLite local: un archivo juegos.db en el directorio actual.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./juegos.db"  # fallback: SQLite local
)

# CREACIÓN DEL ENGINE
# Para SQLite hay que pasar check_same_thread=False; para otros motores, no necesitamos args extra.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# SESIONES Y BASE
# SessionLocal para dependencias en FastAPI y Base para los modelos.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
