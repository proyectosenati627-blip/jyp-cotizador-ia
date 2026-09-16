"""
train_model.py
---------------
Entrena un modelo de clasificación (Random Forest) para predecir si una
combinación de componentes de PC es compatible o no, a partir del dataset
generado en generate_dataset.py.

Este es el "modelo de validación de compatibilidad de componentes" del
proyecto de tesina: el chatbot lo consultará antes de armar una cotización.
"""
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix, f1_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_PATH = "/home/claude/work/ml-models/compatibility/data/dataset_compatibilidad.csv"
MODEL_PATH = "/home/claude/work/ml-models/compatibility/models/modelo_compatibilidad.joblib"
METRICS_PATH = "/home/claude/work/ml-models/compatibility/models/metricas.json"

CATEGORICAS = ["cpu_socket", "mb_socket", "ram_type", "mb_ram_type",
               "case_form_factor", "mb_form_factor"]
NUMERICAS = ["cpu_tdp_w", "gpu_tdp_w", "psu_wattage", "gpu_length_mm"]


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[CATEGORICAS + NUMERICAS]
    y = df["compatible"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocesador = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ],
        remainder="passthrough",
    )

    modelo = Pipeline(steps=[
        ("preprocesador", preprocesador),
        ("clasificador", RandomForestClassifier(
            n_estimators=200, max_depth=12, random_state=42, class_weight="balanced"
        )),
    ])

    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    reporte = classification_report(y_test, y_pred, output_dict=True)
    matriz = confusion_matrix(y_test, y_pred).tolist()

    print(f"Accuracy: {acc:.4f}")
    print(f"F1-score: {f1:.4f}")
    print("Matriz de confusión (filas=real, columnas=predicho):")
    print(matriz)

    joblib.dump(modelo, MODEL_PATH)

    metricas = {
        "accuracy": acc,
        "f1_score": f1,
        "matriz_confusion": matriz,
        "reporte_clasificacion": reporte,
        "n_train": len(X_train),
        "n_test": len(X_test),
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)

    print(f"\nModelo guardado en: {MODEL_PATH}")
    print(f"Métricas guardadas en: {METRICS_PATH}")


if __name__ == "__main__":
    main()
