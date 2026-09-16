# Modelo de Validación de Compatibilidad de Componentes

Componente del proyecto **Sistema de cotización inteligente — J&P Periféricos S.A.C.**
Valida si una combinación de componentes (CPU, motherboard, RAM, GPU, gabinete, PSU)
es compatible, **antes** de que el chatbot genere una cotización al cliente.

## ¿Por qué un dataset sintético?

La empresa aún no ha confirmado si dispone de un historial de ventas explotable
(pendiente en la entrevista de diagnóstico, Cap. 1). Ese dato es indispensable para
el **modelo de predicción de demanda**, pero no para este modelo: la compatibilidad
de hardware depende de reglas técnicas objetivas y documentadas (sockets, tipos de
memoria, dimensiones físicas, consumo eléctrico), no del comportamiento de compra
de los clientes. Por eso generamos un dataset de entrenamiento a partir de esas
reglas reales (ver `src/generate_dataset.py`), en vez de esperar datos internos
de la empresa que corresponden a otro componente del sistema.

Cuando se consiga acceso a casos reales de cotizaciones con errores de
compatibilidad (mencionados en la entrevista, pregunta 3), se pueden añadir como
datos reales adicionales para reentrenar y validar el modelo.

## Estructura

```
compatibility/
├── data/
│   └── dataset_compatibilidad.csv   # 4000 combinaciones generadas y etiquetadas
├── src/
│   ├── generate_dataset.py          # Genera el dataset a partir de reglas de hardware
│   ├── train_model.py               # Entrena y evalúa el modelo
│   └── predict.py                   # Función que usará el chatbot para validar
├── models/
│   ├── modelo_compatibilidad.joblib # Modelo entrenado (Random Forest)
│   └── metricas.json                # Métricas de evaluación
├── requirements.txt
└── README.md
```

## Metodología

1. **Variables de entrada**: socket de CPU y motherboard, tipo de RAM (CPU y mobo),
   TDP de CPU y GPU, potencia de la fuente, longitud de la GPU, factor de forma de
   motherboard y gabinete.
2. **Reglas de etiquetado** (ver docstring de `generate_dataset.py`): coincidencia de
   socket, coincidencia de tipo de RAM, la GPU cabe en el gabinete, la fuente cubre
   el consumo total con 20% de margen, y la motherboard cabe en el gabinete.
3. **Modelo**: Random Forest (`scikit-learn`), con `OneHotEncoder` para variables
   categóricas y `class_weight="balanced"` por el desbalance natural de clases
   (~68% no compatible / 32% compatible en la generación aleatoria).
4. **Resultados** (conjunto de prueba, 20%): **Accuracy 97.25%**, **F1-score 0.957**.
   Ver `models/metricas.json` para el detalle completo (matriz de confusión y
   reporte de clasificación).

## Cómo usarlo (scripts locales)

```bash
pip install -r requirements.txt
python src/generate_dataset.py   # (ya generado, solo si se quiere regenerar)
python src/train_model.py        # (ya entrenado, solo si se quiere reentrenar)
python src/predict.py            # corre 2 ejemplos de demostración
```

### Preparación en Windows

Desde la carpeta `ml-models/compatibility`, cada integrante puede preparar un
entorno aislado y levantar la API con estos comandos en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python api\app.py
```

La API quedará disponible en `http://127.0.0.1:5001`. Para comprobar que está
activa, abrir otra ventana de PowerShell y ejecutar:

```powershell
Invoke-RestMethod http://127.0.0.1:5001/health
```

Para probar una combinación, se puede enviar un JSON con los diez campos
requeridos al endpoint `POST /validar-compatibilidad`.

## API (para conectar con el chatbot / plugin de WordPress)

El modelo ya está expuesto como una API REST con Flask en `api/app.py`.

```bash
cd api
python app.py
# queda escuchando en http://localhost:5001
```

**Endpoints:**
- `GET /health` — verifica que el servicio esté vivo.
- `POST /validar-compatibilidad` — recibe un JSON con los 10 campos del
  componente (ver `predict.py`) y devuelve `compatible`, `probabilidad_compatible`
  y `explicaciones` (lista de razones técnicas si no es compatible).

Ejemplo de consumo desde el plugin de WordPress (PHP, con `wp_remote_post`):

```php
$response = wp_remote_post('http://localhost:5001/validar-compatibilidad', [
    'headers' => ['Content-Type' => 'application/json'],
    'body'    => json_encode([
        'cpu_socket' => 'AM4', 'mb_socket' => 'AM4',
        'ram_type' => 'DDR4', 'mb_ram_type' => 'DDR4',
        'cpu_tdp_w' => 105, 'gpu_tdp_w' => 220,
        'psu_wattage' => 650, 'gpu_length_mm' => 310,
        'case_form_factor' => 'ATX', 'mb_form_factor' => 'ATX',
    ]),
]);
$resultado = json_decode(wp_remote_retrieve_body($response), true);
```

Ya fue probada en vivo con 4 casos: salud del servicio, combinación compatible,
combinación no compatible (con explicaciones) y validación de campos faltantes.

## Limitaciones conocidas

El modelo verifica la coincidencia entre el socket del procesador y el de la
motherboard, así como entre el tipo de RAM indicado para ambos componentes, pero
no valida si esa combinación de socket y tipo de RAM es técnicamente realista.
Por ejemplo, puede recibir una motherboard con una combinación de características
que no existe en el mercado y aun así generar una predicción.

Por esta razón, los resultados pueden ser poco confiables cuando se envían
combinaciones inexistentes o productos que no corresponden a hardware real. Antes
de usar el modelo en producción, los datos deberían contrastarse con un catálogo
real de componentes y ampliarse las reglas de validación cuando sea necesario.

## Pendiente

- [ ] Reemplazar/ampliar el dataset sintético con casos reales de la empresa en
      cuanto estén disponibles.
- [ ] Conectar el endpoint con el plugin de WordPress (`jyp-cotizador-ia`) y con
      el chatbot.
- [ ] Ampliar el conjunto de reglas si se detectan más restricciones técnicas
      relevantes al catálogo real de J&P Periféricos (ej. compatibilidad de
      refrigeración, conectores PCIe específicos).
- [ ] Antes de producción: reemplazar el servidor de desarrollo de Flask por uno
      productivo (ej. `waitress` o `gunicorn`), y restringir CORS a los dominios
      reales en vez de `*`.
