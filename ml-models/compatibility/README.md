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

## Cómo usarlo

```bash
pip install -r requirements.txt
python src/generate_dataset.py   # (ya generado, solo si se quiere regenerar)
python src/train_model.py        # (ya entrenado, solo si se quiere reentrenar)
python src/predict.py            # corre 2 ejemplos de demostración
```

Para integrarlo con el chatbot / plugin de WordPress, se expondrá `predict.py`
como un endpoint de una API (por ejemplo, con FastAPI), que el plugin de PHP
consultará vía HTTP antes de mostrarle la cotización final al cliente.

## Pendiente

- [ ] Reemplazar/ampliar el dataset sintético con casos reales de la empresa en
      cuanto estén disponibles.
- [ ] Exponer `predict.py` como API (FastAPI) para conexión con el plugin de WordPress.
- [ ] Ampliar el conjunto de reglas si se detectan más restricciones técnicas
      relevantes al catálogo real de J&P Periféricos (ej. compatibilidad de
      refrigeración, conectores PCIe específicos).
