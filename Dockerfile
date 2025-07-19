#Imagen base
FROM python:3.10-slim

#Variables de entorno de Python (bytecode y buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \  
    PYTHONUNBUFFERED=1

#Crear directorio de trabajo
WORKDIR /app

#Copiar los archivos necesarios
COPY requirements.txt .

#Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el resto del código
COPY . .

#Exponer el puerto de la API
EXPOSE 8080

#Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
