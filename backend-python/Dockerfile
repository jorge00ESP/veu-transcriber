# 1. Usar Python 3.10 oficial (para evitar el bug de MediaPipe)
FROM python:3.10-slim

# 2. Instalar herramientas del sistema que necesita OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Movernos a la carpeta de trabajo dentro del Docker
WORKDIR /app

# 4. Copiar los requirements e instalarlos primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. EL TRUCO MAESTRO: Descargar el modelo pesado directamente dentro de Docker
RUN gdown 1r1kx7l9sWnDOCnaFHIGvOtzuhFyFA88_ -O vsr_trlrs2lrs3vox2avsp_base.pth

# 6. Copiar tu código (api.py y las carpetas del repositorio)
COPY . .

# 7. Exponer el puerto de conexión
EXPOSE 8000

# 8. El comando que arrancará la API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]