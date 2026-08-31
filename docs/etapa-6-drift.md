# Etapa 6 — Monitoreo de deriva de datos (Evidently)

`generate_drift_report.py` reproduce el mismo split de entrenamiento usado en la Etapa 2
(`test_size=0.2`, `random_state=42`, estratificado) y compara la distribución de los datos de
**train** contra los de **test** con `DataDriftPreset` de [Evidently](https://www.evidentlyai.com/).

```bash
python generate_drift_report.py
# → Reporte de drift guardado en drift_report.html
```

## Reporte

📊 [**Abrir el reporte de drift completo**](../drift_report.html)

El reporte incluye, por cada una de las 11 variables clínicas del dataset, la comparación de
distribuciones entre train y test, el resultado del test estadístico correspondiente, y un
resumen de cuántas columnas mostraron *drift* — la base para decidir si el modelo en producción
necesita reentrenarse.
