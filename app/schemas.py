from pydantic import BaseModel

#Base para crear un juego (POST)
class JuegoCreate(BaseModel):
    nombre: str
    anio: int | None = None
    categoria: str | None = None
    jugadores: str | None = None

#Respuesta al obtener un juego (ID generado)
class Juego(JuegoCreate):
    id: int

    class Config:
        orm_mode = True #Permite a FastAPI convertir modelos SQLAlchemy en JSON 
