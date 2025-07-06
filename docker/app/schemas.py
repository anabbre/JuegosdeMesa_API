from pydantic import BaseModel, Field, validator 

#Base para crear un juego (POST)
class JuegoCreate(BaseModel):
    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del juego de mesa (ej. “Catan”)"
    )
    anio: int | None = Field(
        None,
        ge=0,
        description="Año de lanzamiento (opcional)"
    )
    categoria: str = Field(
        ...,
        min_length=1,
        description="Categoría del juego (ej. “Estrategia”, “Familiar”)"
    )
    jugadores: str = Field(
        ...,
        min_length=1,
        description="Número o rango de jugadores (ej. “2–4”)"
    )

    @validator("nombre")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("Campo obligatorio: debes indicar un nombre")
        return v



#Respuesta al obtener un juego (ID generado)
class Juego(JuegoCreate):
    id: int

    class Config:
        orm_mode = True #Permite a FastAPI convertir modelos SQLAlchemy en JSON 
