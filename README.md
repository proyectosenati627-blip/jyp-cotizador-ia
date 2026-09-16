# Sistema de Cotización Inteligente — J&P Periféricos S.A.C.

Proyecto de Innovación y Mejora — Ingeniería de Software con Inteligencia Artificial,
SENATI (6to ciclo). Desarrollado para la empresa **J&P Periféricos S.A.C.**, dedicada
a la venta de periféricos, equipos de cómputo y soporte técnico.

El proyecto busca reducir los errores de compatibilidad y el tiempo de respuesta en
el proceso de cotización de la empresa, mediante dos modelos de Machine Learning
entrenados por el equipo y un chatbot conversacional que los consulta:

1. **Modelo de validación de compatibilidad de componentes** — valida si una
   combinación de piezas (CPU, placa madre, RAM, GPU, fuente, gabinete) es compatible
   antes de generar una cotización. ✅ Entrenado y expuesto vía API.
2. **Modelo de predicción de demanda** — apoya la gestión de inventario a partir del
   historial de ventas. ⏳ Pendiente de iniciar (depende de la confirmación de datos
   históricos por parte de la empresa).
3. **Chatbot conversacional** — interfaz con el cliente; consulta a ambos modelos
   para armar cotizaciones confiables. ⏳ No iniciado.

> El diferenciador académico del proyecto son los modelos entrenados, no el chatbot
> en sí mismo (que actúa solo como interfaz). Ver `CONTEXTO.md` para el detalle
> completo del planteamiento, alcance y decisiones ya tomadas por el equipo.

## Estado actual del proyecto

| Componente | Estado |
|---|---|
| Sitio WordPress local (copia de desarrollo, vía Duplicator) | ✅ Levantado |
| Modelo de validación de compatibilidad | ✅ Entrenado (97.25% accuracy, F1 0.957) |
| API del modelo de compatibilidad (Flask) | ✅ Funcionando, probada localmente |
| Modelo de predicción de demanda | ⏳ Pendiente |
| Chatbot conversacional | ⏳ Pendiente |
| Conexión API ↔ plugin de WordPress | ⏳ Pendiente |
| Tesina (Capítulos 1 y 2, APA 7) | ✅ Completos |
| Tesina (Capítulos 3, 4 y 5) | ⏳ Pendientes |

## Estructura del repositorio

```
jyp-cotizador-ia/
├── .github/
│   └── copilot-instructions.md   # Contexto automático para asistentes de IA
├── CONTEXTO.md                   # Contexto completo del proyecto (leer primero)
├── .gitignore
├── src/                          # Código PHP del plugin de WordPress
└── ml-models/
    └── compatibility/            # Modelo de validación de compatibilidad
        ├── data/                 # Dataset de entrenamiento
        ├── src/                  # Generación de datos, entrenamiento y predicción
        ├── models/               # Modelo entrenado (.joblib) y métricas
        ├── api/                  # API Flask que expone el modelo
        └── README.md             # Metodología detallada de este modelo
```

> Nota: este repositorio **no** contiene el núcleo de WordPress (`wp-admin`,
> `wp-includes`, etc.), solo el código propio del equipo. El sitio de desarrollo se
> levanta en local a partir de un paquete de Duplicator compartido por Drive entre
> el equipo (ver `CONTEXTO.md`, sección "Entorno de desarrollo").

## Cómo levantar el proyecto en local

### 1. Sitio WordPress (entorno de desarrollo)
1. Instalar Laragon o XAMPP.
2. Solicitar al equipo el paquete de Duplicator (`.zip` + `installer.php`, compartido
   por Drive) y la base de datos (`.sql`).
3. Colocar el paquete en `www/` (Laragon) o `htdocs/` (XAMPP) y correr el instalador
   desde el navegador.
4. Clonar este repositorio dentro de `wp-content/plugins/` de esa instalación local.

### 2. Modelo de compatibilidad + API
```bash
cd ml-models/compatibility
pip install -r requirements.txt
python src/train_model.py       # ya entrenado; solo si se quiere reentrenar
python api/app.py               # levanta la API en http://localhost:5001
```

Probar la API:
```bash
curl -X POST http://localhost:5001/validar-compatibilidad \
  -H "Content-Type: application/json" \
  -d '{"cpu_socket":"AM4","mb_socket":"AM4","ram_type":"DDR4","mb_ram_type":"DDR4","cpu_tdp_w":105,"gpu_tdp_w":220,"psu_wattage":650,"gpu_length_mm":310,"case_form_factor":"ATX","mb_form_factor":"ATX"}'
```

Ver `ml-models/compatibility/README.md` para la metodología completa (por qué se
usó un dataset sintético, qué reglas de compatibilidad se aplicaron, y las métricas
detalladas del modelo).

## Tecnologías utilizadas

- **WordPress** — sitio base de la empresa (entorno de desarrollo local).
- **Python** (`scikit-learn`, `pandas`, `Flask`) — modelos de Machine Learning y su API.
- **PHP** — plugin personalizado de WordPress (`jyp-cotizador-ia`).
- **LaTeX** — documentación de la tesina en formato APA 7ma edición.
- **Git / GitHub** — control de versiones del código propio del equipo.

## Equipo

- Guillermo Alex Donayre Patow
- Andres Daniel Galindo Gonzalez
- Angelo Aaron Rojas Tipiani

**Asesor:** Mg. Jose Armando Tiznado Ubillus — SENATI, Ingeniería de Software con
Inteligencia Artificial.

## Nota académica

Este es un proyecto académico (tesina de fin de carrera). El sitio real de J&P
Periféricos S.A.C. **no es modificado en ningún momento**; todo el desarrollo se
realiza sobre una copia local. El diagnóstico inicial del problema se realizó con
respuestas estimadas del equipo (autorizado por el docente del curso), pendientes de
reemplazar por respuestas reales de la empresa en cuanto se coordine la entrevista.
