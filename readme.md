# 🎲 API CRUD Juegos de Mesa

Proyecto realizado con **FastAPI**, **MariaDB** y **Docker Compose**. Esta API permite gestionar un catálogo de juegos de mesa con operaciones CRUD (crear, obtener, eliminar, etc.), incorporando robustez, configurabilidad y mejores prácticas de desarrollo y despliegue.

## 📦 Tecnologías Usadas

- Python 3.10 (imagen `slim` optimizada)
- FastAPI
- SQLAlchemy
- MariaDB 10.6
- Docker / Docker Compose
- Uvicorn
- PyMySQL
- Python-dotenv (para la gestión de variables de entorno)

---

## 🧠 ¿Qué Hace Esta API?

- Permite registrar nuevos juegos de mesa con nombre, año, categoría y número de jugadores, incluyendo **validación de entrada estricta** para asegurar la calidad de los datos.
- Permite listar todos los juegos registrados.
- Permite obtener un juego por su `id`.
- Permite buscar por nombre de juego (GET con query param).
- Permite eliminar juegos por `id`.
- Incluye una lógica de **reintento de conexión a la base de datos** configurable si aún no está disponible.
- Incorpora un **sistema de logging avanzado** para la trazabilidad de la aplicación, incluyendo logs de conexión a la base de datos y un middleware para registrar todas las peticiones y respuestas HTTP.
- Es **completamente configurable** mediante variables de entorno para la conexión a la base de datos, facilitando su despliegue en diferentes entornos (desarrollo, producción, etc.).

---

## 🛠 Estructura del Proyecto

```text
JuegosMesa_API/
├── .env                  # Archivo para variables de entorno (¡nuevo!)
├── app/                  # Aquí ya no está el código principal, ahora en ./docker/app
├── docker/               # Configuración Docker y código principal 
│   ├── app/              # Código fuente de la API (¡movido aquí!)
│   │   ├── main.py       # Entrypoint de la API, configuración de logging y middleware
│   │   ├── crud.py       # Lógica CRUD
│   │   ├── database.py   # Configuración de conexión a MariaDB (lee de variables de entorno)
│   │   ├── models.py     # Modelo SQLAlchemy
│   │   └── schemas.py    # Validación con Pydantic (con min_length y validators)
│   ├── Dockerfile        # Imagen personalizada y optimizada para FastAPI (¡movido aquí!)
│   └── requirements.txt  # Dependencias (¡movido aquí!)
├── docker-compose.base.yml # Orquestación base de servicios y red entre contenedores 
├── docker-compose.dev.yml  # Configuración para desarrollo (¡nuevo!)
├── docker-compose.prod.yml # Configuración para producción (¡nuevo!)
├── mejoras.md            # Documento explicando las mejoras implementadas después de una primera versión
├── README.md             # Este documento
```

El proyecto utiliza múltiples archivos docker-compose para diferentes entornos:

- **docker-compose.base.yml**: Define los servicios base (api y db), la red y los volúmenes compartidos.
- **docker-compose.dev.yml**: Extiende la configuración base para un entorno de desarrollo (ej. con montajes de volúmenes para desarrollo en caliente).
- **docker-compose.prod.yml**: Extiende la configuración base para un entorno de producción (ej. con healthchecks y sin montajes de código).

Estos archivos orquestan dos contenedores principales:

- **juegosmesa_api**: contenedor que ejecuta la API desarrollada en FastAPI.
- **juegos-db**: contenedor de base de datos MariaDB.

Ambos contenedores comparten la red `juegos-net` (definida en `docker-compose.base.yml`), por lo que la API puede resolver la base de datos simplemente usando el host `juegos-db`.

![Salida de `docker ps` con contenedores juegosmesa_api y juegos-db levantados](img/1.jpg)
---

## 🚀 Cómo ejecutar el proyecto

1. **Configuración de Variables de Entorno**:

   Crea un archivo llamado `.env` en la raíz de tu proyecto (al mismo nivel que `docker-compose.base.yml`). Este archivo contendrá las credenciales de tu base de datos y la URL de conexión de la API.

   ```bash
   MYSQL_ROOT_PASSWORD=your_secure_password
   MYSQL_DATABASE=juegos
   DATABASE_URL=mysql+pymysql://root:your_secure_password@juegos-db/juegos
   # Para SQLite local (solo para desarrollo/pruebas si no usas Docker DB):
   # DATABASE_URL=sqlite:///./juegos.db
   ```

   Asegúrate de reemplazar `your_secure_password` con una contraseña fuerte.

2. **Clonar el Repositorio**:

   ```bash
   git clone https://github.com/anabbre/JuegosdeMesa_API
   cd JuegosMesa_API
   ```

3. **Levanta los contenedores (Entorno de Desarrollo)**:

   Para levantar la API y la base de datos en un entorno de desarrollo:
   ```bash
   docker compose -f docker-compose.base.yml -f docker-compose.dev.yml up --build
   ```
  ![Salida de `docker.ps` mostrando los contenedores `juegosmesa_api` y `juegos-db` corriendo correctamente ](img/1.jpg)

   El `docker-compose.dev.yml` montará tu código localmente, permitiendo cambios en vivo si usas un recargador (como el de Uvicorn).

4. **Levanta los contenedores (Entorno de Producción)**:

   Para levantar la API y la base de datos en un entorno de producción (la imagen de la API ya contendrá el código):
   ```bash
   docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up --build
   ```

5. **Accede a la documentación automática de la API**:

   - Swagger UI: http://localhost:8080/docs
   - Redoc: http://localhost:8080/redoc

6. **Accede al contenedor de base de datos y consulta**:

   Para interactuar directamente con la base de datos MariaDB dentro de su contenedor:

   ```bash
   docker exec -it juegos-db bash
   mariadb -u root -p # Te pedirá la contraseña definida en .env
   USE juegos;
   SELECT * FROM juegos;
   ```

---

## 📂 Endpoints disponibles

| Método | Ruta                         | Descripción                     |
| ------ | ---------------------------- | ------------------------------- |
| POST   | `/juegos`                    | Crear un nuevo juego            |
| GET    | `/juegos`                    | Obtener todos los juegos        |
| GET    | `/juegos/{id}`               | Obtener juego por `id`          |
| GET    | `/juegos/buscar?nombre=<str>`| Buscar juegos por nombre        |
| DELETE | `/juegos/{id}`               | Eliminar juego por `id`         |

---

## 🧪 Pruebas en Swagger

- Ejemplo de JSON para registrar un juego:
  ```json
  {
    "nombre": "Dixit",
    "anio": 2008,
    "categoria": "Creatividad",
    "jugadores": "3-6"
  }
  ```
- Intento de crear juego con campos vacíos (nombre, categoría, jugadores):
  ```json
  {
    "nombre": "",
    "anio": 2023,
    "categoria": "",
    "jugadores": ""
  }
  ```
  Se espera una respuesta con error de validación (422 Unprocessable Entity), indicando que los campos no pueden ser cadenas vacías o tener una longitud mínima.

---


## 📊 Ejemplos Visuales

### 🚀 Arranque y Logging de la API
Al iniciar los servicios con Docker Compose, la API muestra en sus logs la confirmación de la conexión exitosa a la base de datos MariaDB y el inicio del servidor Uvicorn. Esto demuestra la robustez de la conexión y la disponibilidad de la API.

![Logs mostrando "✅ Conexión a la base de datos exitosa." y Uvicorn corriendo](img/3.jpg)

### ✅ Crear Juego desde Swagger UI
La documentación interactiva de Swagger UI permite probar fácilmente el endpoint `POST /juegos`. Al enviar un JSON con los datos de un nuevo juego, la API lo registra correctamente en la base de datos.

![Vista de Swagger UI con el formulario POST /juegos](img/2.jpg)
![Respuesta exitosa de Swagger UI tras la creación de un juego](img/2.1.jpg)

### ❌ Validación de Datos en Acción
Para demostrar la robusta validación de entrada implementada en la API (mediante Pydantic y validadores personalizados), un intento de crear un juego con campos obligatorios vacíos o inválidos resultará en un error HTTP 422 (Unprocessable Entity), indicando los problemas de validación.

![Error 422 Unprocessable Entity por validación de datos en Swagger UI](img/6.jpg)

### 📋 Listar Todos los Juegos
El endpoint `GET /juegos` permite obtener un listado completo de todos los juegos de mesa registrados en el sistema.

![Listado completo de juegos desde Swagger UI mostrando múltiples entradas](img/4.jpg)

### 🔍 Buscar Juego por Nombre
El endpoint `GET /juegos/buscar` con un parámetro de consulta (`nombre=...`) permite filtrar el catálogo de juegos. En el ejemplo, al buscar "Catan", solo se retorna el juego que coincide.

![Respuesta filtrada por nombre, con un único registro que coincide con “Catan"](img/5.jpg)

### 🩺 Health-check de MariaDB en Producción
En un entorno de producción, la configuración de Docker Compose incluye un `healthcheck` para la base de datos MariaDB. Esto asegura que la API solo se inicie una vez que la base de datos esté completamente operativa y saludable. El comando `docker compose ps` refleja este estado.

![docker-compose ps mostrando contenedor juegos-db healthy](img/7.jpg)

### 📂 Verificación Directa de Registros en MariaDB
Para confirmar la persistencia y correcta inserción de los datos, es posible acceder directamente a la consola del contenedor de MariaDB y realizar consultas SQL, como se muestra a continuación.

![MariaDB CLI dentro del contenedor mostrando resultados de SELECT * FROM juegos](img/8.jpg)
---


## 👤 Autoría
- Ana Belén Ballesteros 
- LinkedIn: www.linkedin.com/in/ana-belén-ballesteros-redondo
