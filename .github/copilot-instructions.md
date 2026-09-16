# Instrucciones para el asistente de IA en este repositorio

Este archivo lo lee automáticamente GitHub Copilot Chat en cada conversación
(VS Code). Si usas Gemini Code Assist, Codeium u otra extensión, pega este
contenido como primer mensaje de la conversación.

## Quién soy y qué estamos construyendo

Somos un equipo de 3 estudiantes de último ciclo de Ingeniería de Software con IA
(SENATI) desarrollando la tesina "Sistema de cotización inteligente" para la empresa
real J&P Periféricos S.A.C. Lee `CONTEXTO.md` en la raíz del repo antes de responder
cualquier pregunta sobre el proyecto en general, y el `README.md` de
`ml-models/compatibility/` antes de tocar código de ese módulo.

## Cómo quiero que me ayudes con el código

- **Prioriza código simple y legible sobre código "elegante" u optimizado.** Estamos
  aprendiendo y tenemos que poder explicar cada línea frente al profesor.
- **Comenta el código en español**, con comentarios que expliquen el *por qué*, no
  solo el *qué* (ej. por qué se generó un dataset sintético, por qué se usó Random
  Forest y no otro modelo, por qué ese umbral de compatibilidad).
- Si vas a modificar un archivo existente (`generate_dataset.py`, `train_model.py`,
  `predict.py`, `app.py`), **explica primero en 2-3 líneas qué vas a cambiar y por
  qué**, antes de mostrar el código.
- No reemplaces las reglas de compatibilidad ni el enfoque de dataset sintético sin
  preguntar — esa decisión ya está documentada y justificada en el README académico.
- Cuando agregues una funcionalidad nueva, dime también **qué archivo del README
  o del `CONTEXTO.md` habría que actualizar** para que quede consistente.

## Cómo quiero que me expliques las cosas

- Explica como si se lo estuvieras explicando a un profesor que no programa pero sí
  entiende de procesos de negocio: evita jerga técnica sin explicarla la primera vez
  que aparece (ej. "F1-score: mide qué tan bien el modelo acierta sin favorecer
  solo la clase más común").
- Cuando el resultado de un modelo o script sea un número (accuracy, F1, etc.),
  siempre acompáñalo de una frase en lenguaje simple de qué significa en la práctica.
- Si te pido ayuda para "explicar esto para la sustentación", dame una explicación
  corta (máximo 1 párrafo) en un lenguaje natural, sin código, que yo pueda decir en
  voz alta frente al profesor.

## Alcance actual (no lo cambies sin que te lo pida)

- Modelo de compatibilidad: ✅ entrenado y expuesto en API Flask (`ml-models/compatibility/`).
- Modelo de demanda: ⏳ no iniciado.
- Chatbot: ⏳ no iniciado.
- Conexión API ↔ plugin de WordPress: ⏳ pendiente.

Antes de proponer trabajo en el modelo de demanda o el chatbot, pregunta si ya
tenemos datos reales de la empresa disponibles (puede que sigan sin confirmarse).
