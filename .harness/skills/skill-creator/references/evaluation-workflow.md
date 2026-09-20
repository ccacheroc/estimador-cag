# Flujo de evaluación

Usa este procedimiento para medir si una skill cambia resultados de forma útil.

## Preparar casos

Crea inicialmente 2–3 solicitudes realistas: un caso habitual, una variación y
un límite relevante. Registra identificador, nombre, solicitud, archivos de
entrada, resultado esperado y expectativas verificables cuando el contrato esté
claro. Guarda los casos en `evals/evals.json` según `schemas.md`.

## Obtener el baseline

- Skill nueva: ejecuta los casos sin la skill antes de redactarla.
- Skill existente: conserva una copia inmutable de la versión original.
- Cambio meramente estructural: valida la estructura sin fabricar un fallo.

Registra decisiones, errores y pasos innecesarios. No reveles al ejecutor del
baseline la respuesta deseada ni la solución propuesta.

## Ejecutar la candidata

Ejecuta los mismos casos con la candidata en contextos limpios. Usa workers
independientes en paralelo si existen; en caso contrario, sesiones secuenciales
aisladas.

```text
<skill-name>-workspace/
└── iteration-N/
    └── eval-<name>/
        ├── candidate/run-1/
        └── baseline/run-1/
```

Cada ejecución puede contener `outputs/`, `transcript.md`, `timing.json` y
`grading.json`. Los campos que el host no proporcione quedan ausentes o `null`.

## Evaluar

1. Inspecciona artefactos reales, no solo el mensaje final.
2. Usa validadores programáticos para formatos, fórmulas e invariantes.
3. Califica cada expectativa con `passed` y evidencia concreta.
4. Señala expectativas que también pasa el baseline y no discriminan valor.
5. Usa comparación ciega A/B para resultados subjetivos.
6. Solicita revisión humana cuando la calidad dependa del contexto o gusto.

## Agregar, analizar e iterar

`scripts/aggregate_benchmark.py` agrega resultados compatibles con
`schemas.md`. Compara como mínimo tasa de éxito. Tiempo, tokens, llamadas a
herramientas y errores son opcionales.

Busca mejoras consistentes, regresiones, varianza, expectativas no
discriminantes, coste sin mejora y trabajo repetido que justifique un script.
Modifica solo instrucciones respaldadas por evidencia y generaliza el problema.

Detente cuando el usuario acepte los resultados, no queden fallos relevantes,
no haya mejora significativa o continuar requiera permisos, coste o información
no disponibles.
