---
description: Workflow para finalizar una sesión de trabajo sobre un requisito, asegurando commits, push a la rama remota y apertura opcional de Pull Request.
---

# Workflow: Cerrar Sesión (`/cerrar-sesion`)

Este workflow se ejecuta al concluir una sesión de desarrollo de un requisito.

## Objetivo
Verificar que todo el trabajo pendiente quede validado mediante tests, debidamente confirmado en Git, subido al repositorio remoto y opcionalmente preparado como Pull Request.

## Procedimiento Paso a Paso

### Paso 1: Comprobar el estado del repositorio
1. Ejecutar `git status` para detectar cualquier cambio no confirmado o archivos pendientes.

### Paso 2: Revisión sistemática de documentación técnica afectada
Antes de proceder a la validación de código o commit, el agente **MUST** ejecutar una revisión paso a paso de los cambios recientes (`git status` y `git diff`) y contrastarlos contra la documentación técnica del repositorio:

1. **Estado de la arquitectura (`docs/architecture-state.md`):**
   - Comprobar si los cambios alteran componentes, flujos, contratos entre capas, límites del sistema, dependencias externas o tecnologías empleadas.
   - Si se modificó la estructura del sistema o del stack, actualizar `docs/architecture-state.md` reflejando el estado observable actual.
2. **Decisiones de arquitectura (`docs/decisions/ADR-*.md`):**
   - Comprobar si se ha introducido, reemplazado o descartado una tecnología principal, framework, biblioteca de infraestructura o patrón estructural relevante.
   - Si aplica y no existe ADR previo, redactar el correspondiente `docs/decisions/ADR-XXX-<tema>.md` con contexto, alternativas consideradas y consecuencias.
3. **Contratos HTTP y OpenAPI (`app/http_errors.py`, `app/routers/`, `app/schemas/`):**
   - Comprobar si se han añadido o modificado endpoints, códigos de estado, esquemas Pydantic de entrada/salida o contratos RFC 9457 de error.
   - Asegurar que la documentación OpenAPI autogenerada y las referencias en la documentación reflejen los contratos actualizados.
4. **Guía de desarrollo y dependencias (`README.md`, `pyproject.toml`):**
   - Comprobar si han variado las instrucciones de instalación, dependencias añadidas/eliminadas, comandos de arranque local, variables de entorno (`.env.example`) o suites de prueba.
   - Actualizar `README.md` para mantener absoluta sincronía con el estado real de ejecución del proyecto.
5. **Reglas y especificaciones agénticas (`.harness/`):**
   - Comprobar si los cambios requieren actualizar o sincronizar reglas en `.harness/rules/` o registrar nuevos artefactos en `.harness/manifest.yaml`.
   - Ejecutar la verificación de no-contradicción y consistencia según `.harness/rules/ai-specs-and-rule-evolution.md`.
6. **Informe de verificación de documentación:**
   - Registrar y detallar qué ficheros de documentación han sido revisados, cuáles han requerido actualización y qué cambios se han aplicado.

### Paso 3: Validación y Commit de cambios
1. Si hay cambios pendientes:
   - Ejecutar la comprobación de tipos estáticos:
     ```bash
     uv run --no-sync pyright
     ```
   - Ejecutar la suite de pruebas del proyecto:
     ```bash
     uv run pytest
     ```
   - Si las comprobaciones o tests fallan, detener el workflow e informar al usuario para corregir los errores.
   - Si todo pasa correctamente, añadir y commitear todos los cambios (código y documentación actualizada):
     ```bash
     git add .
     git commit -m "<mensaje descriptivo y trazable de la sesión>"
     ```
2. Si el directorio de trabajo ya estaba limpio, informar de que no hay cambios pendientes de commit.

### Paso 4: Push al repositorio remoto
1. Identificar la rama actual (`git branch --show-current`).
2. Subir la rama actual con seguimiento de upstream:
   ```bash
   git push -u origin <rama-actual>
   ```

### Paso 5: Preguntar por creación de Pull Request
1. Preguntar explícitamente al usuario:
   > *"¿Deseas crear un Pull Request hacia main para esta rama?"*
2. Si el usuario responde **SÍ**:
   - Crear el Pull Request usando `gh` CLI si está instalado:
     ```bash
     gh pr create --base main --head <rama-actual> --fill
     ```
   - O bien proporcionar el enlace directo de GitHub para abrirlo desde el navegador.
3. Si el usuario responde **NO**:
   - Informar de que la rama ha quedado subida al repositorio remoto sin crear PR.

### Paso 6: Resumen final
1. Informar al usuario de:
   - Estado final del repositorio.
   - Rama remota actualizada.
   - Estado del Pull Request (creado o declinado).
   - Fin de la sesión de trabajo.
