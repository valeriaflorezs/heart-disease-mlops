# Etapa 3 — Despliegue con FastAPI + Docker

El pipeline entrenado (`model.joblib`, exportado al final de la Etapa 2) se sirve mediante una
API REST construida con [FastAPI](https://fastapi.tiangolo.com/) y contenerizada con Docker.

## `app/api.py`

Expone tres endpoints:

- **`GET /`** — mensaje de estado.
- **`GET /health`** — verifica que el modelo haya cargado correctamente.
- **`POST /predict`** — recibe las características clínicas de un paciente (`Age`, `Sex`,
  `ChestPainType`, `RestingBP`, `Cholesterol`, `FastingBS`, `RestingECG`, `MaxHR`,
  `ExerciseAngina`, `Oldpeak`, `ST_Slope`) y devuelve la predicción junto con la probabilidad
  de enfermedad cardíaca.

## Contenerización

`docker/Dockerfile` empaqueta la API sobre una imagen `python:3.10-slim`, instalando las
dependencias de `docker/requirements.txt` y copiando `app/api.py` y `model.joblib`.

```bash
docker build -t heart-disease-api -f docker/Dockerfile .
docker run -p 8000:8000 heart-disease-api
```

Con el contenedor corriendo, `http://localhost:8000/docs` expone la interfaz interactiva de
FastAPI (Swagger UI) para probar `/predict` directamente desde el navegador.

## Verificación

```{code} text
GET  /health   → {"status": "ok", "model_loaded": true}
POST /predict  → {"prediction": 0, "label": "Sin enfermedad cardíaca",
                   "probability_heart_disease": 0.0785}
```
