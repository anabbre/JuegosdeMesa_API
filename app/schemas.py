from pydantic import BaseModel, Field, validator

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
        description="Número o rango de jugadores (ej. “2-4”)"
    )

    @validator("nombre")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("Campo obligatorio: debes indicar un nombre")
        return v

class Juego(JuegoCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
