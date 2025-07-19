from sqlalchemy.orm import Session
from . import models, schemas

#Obtener todos los juegos
def get_juegos(db: Session):
    return db.query(models.Juego).all()

#Obtener un juego por ID
def get_juego(db: Session, juego_id: int):
    return db.query(models.Juego).filter(models.Juego.id == juego_id).first()

#Buscar juegos por nombre
def buscar_juego_por_nombre(db: Session, nombre: str):
    return db.query(models.Juego).filter(models.Juego.nombre.ilike(f"%{nombre}%")).all()

#Crear un nuevo juego
def create_juego(db: Session, juego: schemas.JuegoCreate):
    # Primero, verificar si ya existe un juego con ese nombre
    existing_juego = db.query(models.Juego).filter(models.Juego.nombre == juego.nombre).first()
    if existing_juego:
        return None # Indica que el juego ya existe, lo manejaremos en el endpoint

    nuevo_juego = models.Juego(**juego.dict())
    db.add(nuevo_juego)
    db.commit()
    db.refresh(nuevo_juego)
    return nuevo_juego

#Eliminar un juego por ID
def delete_juego(db: Session, juego_id: int):
    juego = db.query(models.Juego).filter(models.Juego.id == juego_id).first()
    if juego:
        db.delete(juego)
        db.commit()
    return juego