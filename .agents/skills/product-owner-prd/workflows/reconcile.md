# RECONCILE — Reconciliar PRD e implementación

Usa este flujo después de cambios de código o para auditar la alineación entre intención y comportamiento.

1. Extrae requisitos, flujos, reglas, permisos, estados, métricas y decisiones del PRD.
2. Inspecciona rutas, UI, modelos, schemas, servicios y tests relevantes para determinar el comportamiento implementado.
3. Clasifica cada diferencia como:
   - `PRD_ONLY`: documentado, pero aparentemente no implementado.
   - `CODE_ONLY`: implementado, pero sin intención de producto confirmada.
   - `CONFLICT`: PRD y código describen comportamientos distintos.
   - `TEST_CONFLICT`: los tests contradicen la intención actual.
4. Para cada discrepancia, aporta evidencia, impacto, hipótesis explicativas y la decisión necesaria. No asumas que el código es correcto ni que el PRD está actualizado.
5. Actualiza PRD, código o tests solo después de establecer la intención; registra las decisiones materiales y conserva la trazabilidad.

Resultado esperado: matriz de discrepancias y plan de corrección priorizado, o confirmación fundamentada de alineación.
