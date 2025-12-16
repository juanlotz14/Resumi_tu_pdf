# Usamos una imagen ligera de Python como base
FROM python:3.9-slim

# Evita que Python genere archivos caché (.pyc) y muestra los logs inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de requerimientos (para aprovechar la caché)
COPY requirements.txt .

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código (app.py, etc.)
COPY . .

# Exponemos el puerto 8501 (el default de Streamlit)
EXPOSE 8501

# Comando para iniciar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]