import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Configuración de la URL de conexión de la Base de Datos 
#Si DATABASE_URL está definida en el entorno (por ejemplo MySQL en Docker), la usaremos. En caso contrario, arrancamos con SQLite local: un archivo juegos.db en el directorio actual
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./juegos.db"  #Fallback para desarrollo local sin Docker DB
)

#Configuración de argumentos de conexión específicos
#Para SQLite hay que pasar check_same_thread=False; para otros motores, no necesitamos args extra
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

#Creación del motro de la bases de datos (Engine)
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

#Configuración de sesiones y base declarativa
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, #Configurada para no autocomit y no autoflush, que permite un control explícito de las transaciones 
    bind=engine
)
Base = declarative_base()
