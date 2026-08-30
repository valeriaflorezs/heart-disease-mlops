from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)

VALID_PATIENT = {
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


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_predict_valid_patient():
    response = client.post("/predict", json=VALID_PATIENT)
    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] in (0, 1)
    assert body["label"] in ("Enfermedad cardíaca", "Sin enfermedad cardíaca")
    assert 0.0 <= body["probability_heart_disease"] <= 1.0


def test_predict_invalid_patient_rejected():
    invalid_patient = {**VALID_PATIENT, "Sex": "X"}
    response = client.post("/predict", json=invalid_patient)
    assert response.status_code == 422
