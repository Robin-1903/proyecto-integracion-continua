# Imagen base oficial con versión fija especificada (Punto 2)
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Desactivar la generación de bytecode de Python
ENV PYTHONTONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias requeridas para compilar psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instalación de dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia del código de la aplicación
COPY app.py /app/

# Exponer el puerto de la aplicación (Punto 2)
EXPOSE 5000

# Comando de inicio del contenedor (Punto 2)
CMD ["python", "app.py"]