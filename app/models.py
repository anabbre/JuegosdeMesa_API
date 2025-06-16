from sqlalchemy import Column, Integer, String
from .database import Base

#Definición del modelo que representa la tabla
class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    anio = Column(Integer)
    categoria = Column(String(50))
    jugadores = Column(String(20))
