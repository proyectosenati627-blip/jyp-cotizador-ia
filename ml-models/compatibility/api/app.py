"""
app.py
------
API REST que expone el modelo de validación de compatibilidad de componentes.
El plugin de WordPress (jyp-cotizador-ia) y el chatbot consultarán esta API
antes de mostrarle una cotización al cliente.

Cómo correrla:
    pip install -r ../requirements.txt flask
    python app.py
    # queda escuchando en http://localhost:5001

Endpoints:
    GET  /health                     -> Verifica que la API esté viva
    POST /validar-compatibilidad     -> Recibe los componentes y responde si son compatibles
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from flask import Flask, request, jsonify
from predict import validar_compatibilidad

app = Flask(__name__)

CAMPOS_REQUERIDOS = [
    "cpu_socket", "mb_socket", "ram_type", "mb_ram_type",
    "cpu_tdp_w", "gpu_tdp_w", "psu_wattage", "gpu_length_mm",
    "case_form_factor", "mb_form_factor",
]


@app.after_request
def agregar_cors(response):
    # Permite que el plugin de WordPress (otro origen/puerto) consulte la API
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "modelo": "validacion_compatibilidad"})


@app.route("/validar-compatibilidad", methods=["POST", "OPTIONS"])
def validar():
    if request.method == "OPTIONS":
        return "", 204

    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se esperaba un JSON con los componentes"}), 400

    faltantes = [c for c in CAMPOS_REQUERIDOS if c not in datos]
    if faltantes:
        return jsonify({
            "error": "Faltan campos requeridos",
            "campos_faltantes": faltantes,
            "campos_requeridos": CAMPOS_REQUERIDOS,
        }), 400

    try:
        resultado = validar_compatibilidad(datos)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error al validar: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
