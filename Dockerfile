#Imagen base
FROM python:3.10

#Crear directorio de trabajo
WORKDIR /app

#Copiar los archivos necesarios
COPY ./app /app/app
COPY requirements.txt /app

#Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

#Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
