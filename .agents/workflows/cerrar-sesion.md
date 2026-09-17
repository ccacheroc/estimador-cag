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

### Paso 2: Validación y Commit de cambios
1. Si hay cambios pendientes:
   - Ejecutar la suite de pruebas del proyecto:
     ```bash
     uv run python -m unittest discover -s tests -v
     ```
   - Si los tests fallan, detener el workflow e informar al usuario para corregir los errores.
   - Si los tests pasan correctamente, añadir y commitear todos los cambios:
     ```bash
     git add .
     git commit -m "<mensaje descriptivo y trazable de la sesión>"
     ```
2. Si el directorio de trabajo ya estaba limpio, informar de que no hay cambios pendientes de commit.

### Paso 3: Push al repositorio remoto
1. Identificar la rama actual (`git branch --show-current`).
2. Subir la rama actual con seguimiento de upstream:
   ```bash
   git push -u origin <rama-actual>
   ```

### Paso 4: Preguntar por creación de Pull Request
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

### Paso 5: Resumen final
1. Informar al usuario de:
   - Estado final del repositorio.
   - Rama remota actualizada.
   - Estado del Pull Request (creado o declinado).
   - Fin de la sesión de trabajo.
