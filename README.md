# Heart Disease MLOps

Proyecto integrador: predicción de falla cardíaca con pipeline de ML, despliegue local (FastAPI + Docker + Kubernetes), CI/CD y monitoreo de deriva de datos.

## Estructura
- `notebooks/` — análisis, detección de data leakage, modelado con validación segura
- `app/` — API de predicción (FastAPI)
- `docker/` — contenerización
- `k8s/` — manifiestos de Kubernetes
- `.github/workflows/` — integración continua
- `drift_report.html` — reporte de monitoreo (Evidently)
- `model.joblib` — modelo entrenado exportado

## Dataset
Heart Failure Prediction — https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
Coloca `heart.csv` dentro de `notebooks/` o en la raíz según tu flujo de trabajo.
