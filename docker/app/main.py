from fastapi import FastAPI, Depends, HTTPException, Query, Request
import datetime
import logging
from sqlalchemy.orm import Session
from app import crud, models, schemas, database
from app.database import Base, engine
import time
from sqlalchemy.exc import OperationalError


#Configuración básica del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


#Intentar conectar varias veces antes de rendirse
MAX_RETRIES = 10
RETRY_WAIT = 2  #segundos

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine.connect()
        logger.info("✅ Conexión a la base de datos exitosa.")
        break
    except OperationalError as e:
        logger.error(f"Error al conectar a la BD (intento {attempt}): {e}")
        time.sleep(RETRY_WAIT)
else:
    logger.critical("❌ No se pudo conectar a la base de datos después de varios intentos.")
    raise SystemExit(1)


#Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CRUD Juegos de Mesa",
    description="API RESTful para la gestión de un catálogo de juegos de mesa. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) de información detallada sobre juegos, incluyendo su nombre, año de lanzamiento, categoría y número de jugadores.",
    version="2.0."
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.datetime.utcnow()
    logger.info(f"➡️ Petición: {request.method} {request.url}")
    response = await call_next(request)
    process_time = (datetime.datetime.utcnow() - start_time).total_seconds()
    logger.info(f"⬅️ Respuesta: {response.status_code} {request.method} {request.url} "
                f"in {process_time:.3f}s")
    return response


#Dependencia para obtener una sesión de base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Obtener todos los juegos
@app.get("/juegos", response_model=list[schemas.Juego])
def listar_juegos(db: Session = Depends(get_db)):
    return crud.get_juegos(db)

#Buscar juego por nombre
@app.get("/juegos/buscar", response_model=list[schemas.Juego])
def buscar_juego(nombre: str = Query(..., description="Nombre del juego a buscar"), db: Session = Depends(get_db)):
    juegos = crud.buscar_juego_por_nombre(db, nombre)
    if not juegos:
        raise HTTPException(status_code=404, detail="No se encontraron juegos con ese nombre")
    return juegos

#Obtener juego por ID
@app.get("/juegos/{juego_id}", response_model=schemas.Juego)
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = crud.get_juego(db, juego_id)
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego

#Crear nuevo juego
@app.post("/juegos", response_model=schemas.Juego)
def crear_juego(juego: schemas.JuegoCreate, db: Session = Depends(get_db)):
    if not juego.nombre:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")
    return crud.create_juego(db, juego)

#Eliminar juego por ID
@app.delete("/juegos/{juego_id}", response_model=schemas.Juego)
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = crud.delete_juego(db, juego_id)
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego
