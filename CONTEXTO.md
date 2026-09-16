# Contexto del Proyecto — Sistema de Cotización Inteligente (J&P Periféricos S.A.C.)

> Este archivo resume el proyecto para que cualquier asistente de IA (GitHub Copilot,
> Continue, Claude Code, etc.) que trabaje en este repo tenga el contexto completo sin
> que el equipo tenga que explicarlo cada vez. Referencia este archivo al inicio de
> cualquier sesión de desarrollo.

## 1. Qué es este proyecto

Tesina de 6to ciclo (último) de Ingeniería de Software con Inteligencia Artificial —
SENATI, curso "Mejora de Métodos en el Trabajo — Elaboración de Proyecto de
Innovación y Mejora". Equipo de 3 personas.

**Empresa real:** J & P Periféricos S.A.C. (RUC 20545122520), venta de periféricos y
equipos de cómputo + soporte técnico, Lima, Perú. Tiene un sitio WordPress real en
producción que **no se toca**; se trabaja sobre una copia local (ver sección 3).

**Título del proyecto:** Sistema de cotización inteligente para J&P Periféricos.
El diferenciador académico son los **modelos entrenados**, no el chatbot en sí:

1. **Modelo de validación de compatibilidad de componentes** — ✅ en desarrollo (ver sección 4).
2. **Modelo de predicción de demanda** (con historial de ventas) — ⏳ pendiente, depende
   de que la empresa confirme si tiene un registro histórico explotable.
3. **Chatbot conversacional** — consulta a los dos modelos anteriores para armar
   cotizaciones. Aún no iniciado.

## 2. Problema y alcance (ya decidido, no volver a discutir)

Se identificaron 3 hipótesis (compatibilidad, predicción de demanda, búsqueda de
productos). El equipo decidió que el **Capítulo 2 de la tesina combina compatibilidad
+ demanda** como un solo "sistema de cotización inteligente" (no se eligió un único
problema aislado). La entrevista de diagnóstico con la empresa se hizo con
**respuestas estimadas** (autorizado por el profesor, ya que no hay acceso directo a
personal de la empresa); están documentadas en el Capítulo 1 del LaTeX.

## 3. Entorno de desarrollo

- El sitio WordPress real **no se modifica nunca**. Se exportó con **Duplicator** y se
  importó en un entorno **local** (Laragon/XAMPP) en cada máquina del equipo.
- El repositorio de GitHub está ubicado **dentro de**
  `wp-content/plugins/jyp-cotizador-ia/` (no en la raíz de WordPress), para no
  versionar el núcleo de WordPress por error.
- El paquete de Duplicator (.zip + installer.php) y la base de datos (.sql) se
  comparten por Google Drive entre el equipo, **no por GitHub**.
- Cada integrante nuevo: clona el repo dentro de su propio `wp-content/plugins/` local
  (después de levantar su propio WordPress con el paquete de Duplicator compartido).

### Estructura del repo (`jyp-cotizador-ia/`)
```
jyp-cotizador-ia/
├── .gitignore
├── CONTEXTO.md              # este archivo
├── src/                     # código PHP del plugin de WordPress
└── ml-models/
    └── compatibility/       # modelo de validación de compatibilidad (ver sección 4)
        └── (demand/ pendiente de crear cuando se inicie el modelo de demanda)
```

## 4. Estado actual del modelo de compatibilidad

Carpeta: `ml-models/compatibility/`. Ver su propio `README.md` para el detalle completo.
Resumen:

- **Dataset**: sintético (4,000 filas), generado con reglas reales de hardware
  (`src/generate_dataset.py`) porque este modelo no depende del historial de ventas
  de la empresa (eso es para el modelo de demanda), sino de reglas técnicas objetivas
  (socket, tipo de RAM, dimensiones, consumo eléctrico).
- **Modelo**: Random Forest (`scikit-learn`). **Accuracy 97.25%, F1-score 0.957**.
  Guardado en `models/modelo_compatibilidad.joblib`.
- **API**: expuesta con Flask en `api/app.py` (puerto 5001), ya probada con 4 casos
  reales vía HTTP (`/health` y `/validar-compatibilidad`).
- **Pendiente**: conectar esta API con el plugin de PHP (`wp_remote_post`), y
  eventualmente reemplazar/ampliar el dataset sintético con casos reales de la
  empresa si se consiguen.

## 5. Estado de la tesina (LaTeX, APA 7ma edición)

- **Capítulo 1** (Generalidades de la empresa): completo, incluida la entrevista con
  respuestas estimadas.
- **Capítulo 2** (Identificación del problema, objetivos, referencias): completo.
  Cita una tesis peruana (Montero, 2025, USAT) para el problema nacional y un artículo
  de Elsevier (Alves Pereira et al., 2018) para el internacional.
- **Anexos**: tablas del método de Pareto (Identificación del Problema / Lista de
  Problema), con datos estimados por el equipo (aún no hay encuesta real al personal).
- **Capítulos 3, 4 y 5**: placeholders vacíos, pendientes (antecedentes/marco teórico,
  DOP-cronograma-presupuesto, resultados/conclusiones).
- Formato: márgenes 2.54 cm, Times New Roman, interlineado 1.5, índice con hipervínculos,
  tablas sin bordes verticales (estilo APA).

## 6. Pendientes generales del equipo

- [ ] Iniciar el modelo de predicción de demanda (con datos simulados mientras se
      confirma si hay historial real de ventas explotable).
- [ ] Conectar la API de compatibilidad al plugin de WordPress.
- [ ] Iniciar el desarrollo del chatbot conversacional.
- [ ] Completar Capítulos 3, 4 y 5 de la tesina.
- [ ] Si se logra contacto real con la empresa, reemplazar las respuestas estimadas
      de la entrevista por respuestas reales.
