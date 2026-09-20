---
name: skill-creator
description: Crea, modifica, valida y optimiza skills portables para agentes de codificación. Úsala al diseñar una skill, mejorar una existente, comprobar su activación o comportamiento, comparar versiones, reducir acoplamientos de proveedor o preparar una skill para distribución.
compatibility: El flujo documental es independiente del runtime; la automatización incluida requiere Python 3.11 o posterior.
---

# Creador de skills portables

Construye skills basadas en el estándar Agent Skills que mejoren decisiones y
resultados observables sin depender de un proveedor, modelo, interfaz o nombre
de herramienta concreto.

## Principios

1. **Una fuente canónica.** Mantén una sola implementación. Los archivos
   exigidos por un host son adaptadores mínimos, no copias completas.
2. **Núcleo portable.** Expresa intenciones, capacidades, entradas, salidas,
   invariantes y criterios de éxito. Aísla comandos, eventos, rutas y metadatos
   específicos del host en adaptadores opcionales.
3. **Evidencia antes que intuición.** Para cambios conductuales relevantes,
   define una evaluación y observa el baseline antes de escribir la solución.
4. **Rigor proporcional al riesgo.** Usa pruebas objetivas para resultados
   verificables, revisión humana para calidad subjetiva y pruebas de presión
   solo para skills que imponen disciplina.
5. **Instrucciones mínimas.** Incluye únicamente conocimiento no obvio que
   cambie decisiones. No repitas capacidades generales ni políticas del repo.
6. **Alcance y permisos intactos.** Una skill no amplía la solicitud ni autoriza
   publicaciones, commits, red, secretos o mutaciones externas.

## Flujo de trabajo

### 1. Descubrir el contexto

Lee primero las instrucciones canónicas del repositorio y localiza skills,
reglas y adaptadores existentes. Identifica la fuente de verdad antes de editar.

### 2. Capturar la intención

Obtén del contexto disponible, preguntando solo cuando sea imprescindible:

- capacidad que debe aportar la skill;
- solicitudes que deben y no deben activarla;
- entradas, salidas y criterios de éxito;
- riesgos, permisos y dependencias;
- hosts o entornos en los que debe funcionar.

No crees una skill para una solución puntual, conocimiento genérico que el
agente ya posee o una restricción mecánica validable mejor mediante código.

### 3. Clasificar el trabajo y diseñar la evaluación

Selecciona el nivel mínimo de evidencia adecuado:

- **Skill nueva con comportamiento verificable:** ejecuta primero 2–3 casos
  realistas sin la skill.
- **Skill existente:** conserva la versión original y úsala como baseline.
- **Skill normativa:** añade escenarios con presión e incentivos para incumplir.
- **Skill técnica:** comprueba aplicación, variantes y casos límite.
- **Skill de referencia:** comprueba recuperación y uso correcto de datos.
- **Skill creativa:** prioriza comparación ciega y revisión humana.
- **Cambio documental menor sin efecto conductual:** basta la validación
  estructural y de portabilidad.

Lee [flujo de evaluación](references/evaluation-workflow.md) cuando vayas a
ejecutar evaluaciones. Para skills normativas, lee además
[pruebas de disciplina](references/discipline-skill-testing.md).

### 4. Diseñar la skill

Usa este mínimo portable:

```text
skill-name/
├── SKILL.md
├── scripts/       # automatización determinista, solo si aporta valor
├── references/    # detalle condicional cargado bajo demanda
└── assets/        # plantillas o recursos usados en los resultados
```

El `SKILL.md` debe contener:

```yaml
---
name: skill-name
description: Qué capacidad aporta y cuándo debe activarse.
---
```

- `name`: 1–64 caracteres, minúsculas ASCII, dígitos y guiones; debe coincidir
  con el nombre de la carpeta.
- `description`: 1–1024 caracteres; debe distinguir qué hace la skill, cuándo
  usarla y los límites que eviten activaciones erróneas.
- Cuerpo: propósito, decisiones, restricciones y rutas a recursos necesarios.

Usa solo campos adicionales admitidos por el estándar cuando sean necesarios.
Evita campos de invocación, modelo o herramientas que otro host pueda
interpretar de forma distinta.

### 5. Escribir la versión mínima

- Mantén `SKILL.md` por debajo de 500 líneas y, preferiblemente, 5000 tokens.
- Usa referencias de un solo salto y explica cuándo deben leerse.
- Incluye scripts solo para lógica repetida o determinista; declara sus
  dependencias y valida sus errores.
- Ofrece una opción predeterminada clara en vez de catálogos de alternativas.
- Explica el motivo de una restricción. Reserva `MUST`, `NEVER` y secuencias
  rígidas para seguridad, permisos o flujos realmente frágiles.
- No copies manuales extensos ni ejemplos narrativos de una única incidencia.

### 6. Ejecutar candidate y baseline

Ejecuta cada caso en contextos limpios e independientes:

1. `candidate`: con la nueva skill.
2. `baseline`: sin skill para una creación o con la versión anterior para una
   mejora.

Usa workers aislados en paralelo si el entorno los proporciona. En caso
contrario, usa sesiones limpias secuenciales. No inventes aislamiento,
telemetría o métricas que el host no exponga.

Para automatización externa, usa el
[protocolo de runner](references/runner-protocol.md). El núcleo nunca debe
invocar directamente una CLI concreta.

### 7. Evaluar e iterar

- Define expectativas objetivas después de observar la primera ejecución,
  salvo que ya exista un contrato estable.
- Usa verificadores programáticos para propiedades mecánicas.
- Exige evidencia concreta para cada resultado aprobado.
- Compara calidad, corrección, tiempo y coste solo con métricas disponibles;
  representa las ausentes como `null`.
- Presenta resultados en conversación, archivos o visor estático según las
  capacidades disponibles.
- Generaliza a partir de los fallos; no sobreajustes a los ejemplos.
- Repite hasta que el usuario esté satisfecho o no haya mejora significativa.

La comparación ciega es recomendable cuando dos versiones producen artefactos
subjetivos o las métricas no explican la diferencia de calidad.

### 8. Optimizar el descubrimiento

Después de estabilizar el comportamiento:

1. Crea unas 20 consultas realistas: 8–10 positivas y 8–10 negativas cercanas.
2. Ejecuta cada consulta tres veces cuando el coste lo permita.
3. Mantén una división fija aproximada de 60/40 entre entrenamiento y
   validación.
4. Selecciona la descripción por validación, no por la última iteración.
5. Comprueba 5–10 consultas nuevas antes de aceptar el resultado.

La optimización automática requiere un runner que informe si la skill fue
activada. Si el host no expone esa señal, revisa la selección manualmente y
documenta la limitación.

### 9. Validar y entregar

Ejecuta, como mínimo:

Ejecuta `scripts/quick_validate.py <skill-directory> --portable` con el
intérprete de Python disponible en el entorno.

Además:

- comprueba referencias relativas y recursos requeridos;
- ejecuta scripts añadidos o modificados;
- revisa seguridad, red, secretos y efectos externos;
- verifica los adaptadores o archivos puente afectados;
- confirma que no existen copias divergentes de la fuente canónica;
- no publiques, instales, hagas commit ni push sin autorización.

Lee [lista de portabilidad](references/portability-checklist.md) antes de cerrar
una creación o revisión sustancial.

## Recursos de esta skill

- [Flujo de evaluación](references/evaluation-workflow.md): baseline,
  candidate, grading, comparación e iteración.
- [Pruebas de disciplina](references/discipline-skill-testing.md): escenarios de
  presión y cierre de racionalizaciones.
- [Protocolo de runner](references/runner-protocol.md): automatización portable
  mediante JSON por entrada y salida estándar.
- [Lista de portabilidad](references/portability-checklist.md): revisión final.
- [Esquemas](references/schemas.md): contratos JSON para resultados y métricas.
- `agents/grader.md`, `agents/comparator.md` y `agents/analyzer.md`: prompts de
  roles independientes cuando el entorno permita delegación.

## Criterio de finalización

Una skill está lista cuando:

- pasa la validación estructural y de portabilidad;
- mejora resultados significativos frente al baseline, o existe una razón
  documentada para no medirlos;
- activa en solicitudes pertinentes y evita negativas cercanas;
- funciona sin nombres, comandos ni supuestos de un host concreto;
- conserva el alcance, permisos y fuente canónica del proyecto;
- sus scripts, referencias y adaptadores necesarios han sido verificados.
