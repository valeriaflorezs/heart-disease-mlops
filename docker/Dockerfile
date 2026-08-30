FROM python:3.10-slim

WORKDIR /code

# Instalar dependencias primero (aprovecha la cache de Docker si no cambian)
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API y el modelo entrenado
COPY app/api.py .
COPY model.joblib .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
