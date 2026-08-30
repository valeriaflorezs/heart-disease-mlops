"""
API de predicción de falla cardíaca.

Carga el pipeline entrenado (preprocesador + modelo KNN) exportado en la Etapa 2
y expone un endpoint /predict que recibe las características de un paciente
y devuelve la predicción junto con la probabilidad de enfermedad cardíaca.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import joblib
import os

# --------------------------------------------------------------------------
# Carga del modelo
# --------------------------------------------------------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "model.joblib")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Predice la probabilidad de enfermedad cardíaca a partir de datos clínicos.",
    version="1.0.0",
)


# --------------------------------------------------------------------------
# Esquema de entrada
#
# Ajusta estos campos si tu dataset heart.csv tiene columnas distintas.
# Los valores por defecto siguen el dataset "Heart Failure Prediction" de Kaggle:
# https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
# --------------------------------------------------------------------------
class PatientData(BaseModel):
    Age: int = Field(..., ge=0, le=120, example=54)
    Sex: Literal["M", "F"] = Field(..., example="M")
    ChestPainType: Literal["TA", "ATA", "NAP", "ASY"] = Field(..., example="ATA")
    RestingBP: int = Field(..., ge=0, le=300, example=130)
    Cholesterol: int = Field(..., ge=0, le=700, example=246)
    FastingBS: Literal[0, 1] = Field(..., example=0)
    RestingECG: Literal["Normal", "ST", "LVH"] = Field(..., example="Normal")
    MaxHR: int = Field(..., ge=0, le=250, example=150)
    ExerciseAngina: Literal["Y", "N"] = Field(..., example="N")
    Oldpeak: float = Field(..., example=1.0)
    ST_Slope: Literal["Up", "Flat", "Down"] = Field(..., example="Up")

    class Config:
        json_schema_extra = {
            "example": {
                "Age": 54,
                "Sex": "M",
                "ChestPainType": "ATA",
                "RestingBP": 130,
                "Cholesterol": 246,
                "FastingBS": 0,
                "RestingECG": "Normal",
                "MaxHR": 150,
                "ExerciseAngina": "N",
                "Oldpeak": 1.0,
                "ST_Slope": "Up",
            }
        }


class PredictionResponse(BaseModel):
    prediction: int
    label: str
    probability_heart_disease: float


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Heart Disease Prediction API está activa. Visita /docs para probarla."}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientData):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="El modelo no está cargado. Verifica que model.joblib exista en la ruta "
            "configurada.",
        )

    input_df = pd.DataFrame([patient.model_dump()])

    try:
        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0, 1])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error al predecir: {exc}")

    return PredictionResponse(
        prediction=prediction,
        label="Enfermedad cardíaca" if prediction == 1 else "Sin enfermedad cardíaca",
        probability_heart_disease=round(probability, 4),
    )
