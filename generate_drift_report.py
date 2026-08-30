"""
Genera un reporte de data drift (train vs. test) con Evidently.

Reproduce el mismo split usado en el notebook de entrenamiento
(notebooks/2_model_pipeline_cv.ipynb: test_size=0.2, random_state=42,
stratify=y) para comparar la distribución de train contra test y
detectar drift entre ambos conjuntos.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset

RANDOM_STATE = 42
DATA_PATH = "notebooks/heart.csv"
TARGET_COL = "HeartDisease"
OUTPUT_PATH = "drift_report.html"


def main():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    train_df = X_train.copy()
    train_df[TARGET_COL] = y_train
    test_df = X_test.copy()
    test_df[TARGET_COL] = y_test

    data_definition = DataDefinition()
    reference_dataset = Dataset.from_pandas(train_df, data_definition=data_definition)
    current_dataset = Dataset.from_pandas(test_df, data_definition=data_definition)

    report = Report(metrics=[DataDriftPreset()])
    result = report.run(current_data=current_dataset, reference_data=reference_dataset)

    result.save_html(OUTPUT_PATH)
    print(f"Reporte de drift guardado en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
