from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#URL de conexión: mariadb+mysqlconnector://usuario:contraseña@host/db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@juegos-db/juegos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Sesión para hacer consultas desde FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base declarativa de los modelos
Base = declarative_base()
