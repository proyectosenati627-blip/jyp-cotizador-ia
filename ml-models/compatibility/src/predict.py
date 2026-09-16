"""
predict.py
----------
Punto de entrada que usará el chatbot (o cualquier otro componente, como el
plugin de WordPress vía una API) para validar la compatibilidad de una
combinación de componentes ANTES de generar una cotización.

Uso:
    from predict import validar_compatibilidad
    resultado = validar_compatibilidad({
        "cpu_socket": "AM4", "mb_socket": "AM4",
        "ram_type": "DDR4", "mb_ram_type": "DDR4",
        "cpu_tdp_w": 105, "gpu_tdp_w": 220,
        "psu_wattage": 650, "gpu_length_mm": 310,
        "case_form_factor": "ATX", "mb_form_factor": "ATX",
    })
    print(resultado)
"""
import joblib
import pandas as pd

MODEL_PATH = "/home/claude/work/ml-models/compatibility/models/modelo_compatibilidad.joblib"

_modelo = None


def _cargar_modelo():
    global _modelo
    if _modelo is None:
        _modelo = joblib.load(MODEL_PATH)
    return _modelo


def validar_compatibilidad(componentes: dict) -> dict:
    """
    Recibe un diccionario con los componentes de una cotización y devuelve
    si son compatibles, junto con la probabilidad y una explicación básica
    (qué reglas técnicas parecen no cumplirse), útil para que el chatbot
    le explique al cliente por qué una combinación no es recomendable.
    """
    modelo = _cargar_modelo()
    X = pd.DataFrame([componentes])
    proba = modelo.predict_proba(X)[0]
    pred = int(modelo.predict(X)[0])

    explicaciones = []
    if componentes["cpu_socket"] != componentes["mb_socket"]:
        explicaciones.append(
            f"El socket del procesador ({componentes['cpu_socket']}) no coincide "
            f"con el de la placa madre ({componentes['mb_socket']})."
        )
    if componentes["ram_type"] != componentes["mb_ram_type"]:
        explicaciones.append(
            f"La RAM es {componentes['ram_type']} pero la placa madre soporta "
            f"{componentes['mb_ram_type']}."
        )
    consumo_total = componentes["cpu_tdp_w"] + componentes["gpu_tdp_w"]
    if componentes["psu_wattage"] < 1.2 * consumo_total:
        explicaciones.append(
            f"La fuente de {componentes['psu_wattage']}W podría ser insuficiente "
            f"para un consumo estimado de {consumo_total}W (se recomienda al menos "
            f"{int(1.2 * consumo_total)}W)."
        )

    return {
        "compatible": bool(pred),
        "probabilidad_compatible": round(float(proba[1]), 4),
        "explicaciones": explicaciones if not pred else [],
    }


if __name__ == "__main__":
    # Ejemplo 1: combinación compatible
    ejemplo_ok = {
        "cpu_socket": "AM4", "mb_socket": "AM4",
        "ram_type": "DDR4", "mb_ram_type": "DDR4",
        "cpu_tdp_w": 105, "gpu_tdp_w": 220,
        "psu_wattage": 650, "gpu_length_mm": 310,
        "case_form_factor": "ATX", "mb_form_factor": "ATX",
    }
    print("Ejemplo compatible:", validar_compatibilidad(ejemplo_ok))

    # Ejemplo 2: combinación con error típico (socket distinto + fuente insuficiente)
    ejemplo_mal = {
        "cpu_socket": "AM5", "mb_socket": "AM4",
        "ram_type": "DDR5", "mb_ram_type": "DDR4",
        "cpu_tdp_w": 120, "gpu_tdp_w": 320,
        "psu_wattage": 450, "gpu_length_mm": 330,
        "case_form_factor": "ATX", "mb_form_factor": "ATX",
    }
    print("Ejemplo NO compatible:", validar_compatibilidad(ejemplo_mal))
