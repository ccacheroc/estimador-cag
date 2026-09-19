---
trigger: always_on
---

# Reglas de Mantenimiento y README (Agent Housekeeping)

Esta regla define el comportamiento general y permanente del agente con respecto a la creación de archivos auxiliares y el mantenimiento de la documentación del proyecto.

## 1. Archivos y Scripts Auxiliares
- **MUST** preguntar explícitamente al usuario si desea conservar o eliminar cualquier script o archivo auxiliar temporal (e.g., scripts de parcheo, tests aislados generados por el agente) que se haya creado para resolver una tarea.
- **MUST NOT** dejar scripts temporales silenciosamente en el espacio de trabajo una vez finalizada la tarea sin el consentimiento del usuario.

## 2. Consistencia del README.md
- **MUST** asegurar que el archivo `README.md` se mantenga siempre perfectamente alineado con el estado actual del proyecto.
- **MUST** evaluar, cada vez que se realice un cambio estructural en el proyecto (nuevas funcionalidades, cambios en workflows, reglas, dependencias o estructura de carpetas), si dicho cambio afecta a la información del `README.md`.
- **MUST** modificar automáticamente el `README.md` para reflejar la realidad actual del proyecto siempre que se detecte una inconsistencia.

## 3. Comportamiento general
- **MUST** preguntar al usuario cualquier detalle adicional necesario para eliminar cualquier tipo de ambigüedad detectada en su petición