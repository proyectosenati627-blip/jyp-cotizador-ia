"""
generate_dataset.py
--------------------
Genera un dataset sintético de combinaciones de componentes de PC (CPU, motherboard,
RAM, GPU, gabinete, fuente de poder) etiquetadas como compatibles / no compatibles.

¿Por qué sintético y no el historial de ventas de la empresa?
J&P Periféricos S.A.C. aún no ha confirmado si cuenta con un registro histórico de
ventas explotable (ver Capítulo 1, sección de entrevista, pregunta 6), y ese dataset
serviría para el MODELO DE DEMANDA, no para el de compatibilidad. El de compatibilidad
no depende de ventas históricas, sino de reglas técnicas objetivas (sockets, tipos de
RAM, dimensiones físicas, consumo eléctrico), por lo que sí es posible construir un
dataset de entrenamiento confiable sin depender de datos internos de la empresa.

Reglas de compatibilidad usadas para etiquetar cada combinación:
  1. El socket del CPU debe coincidir con el socket de la motherboard.
  2. El tipo de RAM (DDR4/DDR5) debe coincidir con el soportado por la motherboard.
  3. La longitud física de la GPU no debe superar el espacio máximo del gabinete.
  4. La potencia de la fuente debe superar el consumo total (CPU + GPU) con un
     margen de seguridad de al menos 20% (regla estándar de la industria).
  5. El factor de forma de la motherboard debe caber en el gabinete.
"""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

CPU_SOCKETS = ["AM4", "AM5", "LGA1700", "LGA1200"]
RAM_TYPES = ["DDR4", "DDR5"]
FORM_FACTORS = ["ATX", "Micro-ATX", "Mini-ITX"]

# Compatibilidad real socket -> tipo de RAM soportado por placas de ese socket
SOCKET_RAM_SOPORTADO = {
    "AM4": ["DDR4"],
    "AM5": ["DDR5"],
    "LGA1700": ["DDR4", "DDR5"],  # existen versiones de placa para ambos
    "LGA1200": ["DDR4"],
}

# Tamaño máximo de GPU (mm) que admite cada factor de forma de gabinete (aprox. real)
MAX_GPU_LEN_POR_GABINETE = {
    "ATX": 380,
    "Micro-ATX": 320,
    "Mini-ITX": 240,
}


def generar_fila():
    cpu_socket = RNG.choice(CPU_SOCKETS)
    # 70% de las veces la mobo tiene el socket correcto (para tener casos positivos y negativos)
    if RNG.random() < 0.7:
        mb_socket = cpu_socket
    else:
        mb_socket = RNG.choice(CPU_SOCKETS)

    mb_ram_type = RNG.choice(SOCKET_RAM_SOPORTADO[mb_socket])
    # 75% de las veces la RAM elegida es la correcta para esa mobo
    ram_type = mb_ram_type if RNG.random() < 0.75 else RNG.choice(RAM_TYPES)

    cpu_tdp = int(RNG.integers(65, 170))          # Watts
    gpu_tdp = int(RNG.integers(75, 450))          # Watts
    psu_wattage = int(RNG.choice([450, 550, 650, 750, 850, 1000]))

    gpu_length_mm = int(RNG.integers(180, 360))
    case_form_factor = RNG.choice(FORM_FACTORS)
    max_gpu_len = MAX_GPU_LEN_POR_GABINETE[case_form_factor]

    mb_form_factor = RNG.choice(FORM_FACTORS)

    # ---- Reglas de compatibilidad ----
    r1_socket_ok = (cpu_socket == mb_socket)
    r2_ram_ok = (ram_type == mb_ram_type)
    r3_gpu_cabe = (gpu_length_mm <= max_gpu_len)
    r4_psu_ok = (psu_wattage >= 1.2 * (cpu_tdp + gpu_tdp))
    # Mini-ITX solo admite mobo Mini-ITX; Micro-ATX admite Micro-ATX o Mini-ITX; ATX admite cualquiera
    tam_orden = {"Mini-ITX": 0, "Micro-ATX": 1, "ATX": 2}
    r5_form_ok = tam_orden[mb_form_factor] <= tam_orden[case_form_factor]

    compatible = int(r1_socket_ok and r2_ram_ok and r3_gpu_cabe and r4_psu_ok and r5_form_ok)

    return {
        "cpu_socket": cpu_socket,
        "mb_socket": mb_socket,
        "ram_type": ram_type,
        "mb_ram_type": mb_ram_type,
        "cpu_tdp_w": cpu_tdp,
        "gpu_tdp_w": gpu_tdp,
        "psu_wattage": psu_wattage,
        "gpu_length_mm": gpu_length_mm,
        "case_form_factor": case_form_factor,
        "mb_form_factor": mb_form_factor,
        "compatible": compatible,
    }


def generar_dataset(n=4000, seed=42):
    global RNG
    RNG = np.random.default_rng(seed)
    filas = [generar_fila() for _ in range(n)]
    df = pd.DataFrame(filas)
    return df


if __name__ == "__main__":
    df = generar_dataset(n=4000)
    df.to_csv("/home/claude/work/ml-models/compatibility/data/dataset_compatibilidad.csv", index=False)
    print("Dataset generado:", df.shape)
    print(df["compatible"].value_counts(normalize=True))
