---
description: Workflow para iniciar el trabajo en un nuevo requisito, asegurando commits y push de cambios pendientes, creación opcional de PR y apertura de una nueva rama.
---

# Workflow: Abrir Sesión (`/abrir-sesion`)

Este workflow se ejecuta cada vez que el usuario va a comenzar un nuevo requisito de desarrollo.

## Objetivo
Asegurar que el repositorio quede limpio y sincronizado antes de comenzar, gestionar la subida y posible Pull Request de los cambios previos, y preparar una nueva rama de trabajo para el nuevo requisito.

## Procedimiento Paso a Paso

### Paso 1: Comprobar el estado del repositorio
1. Ejecutar `git status` para comprobar si existen cambios locales sin confirmar (staged, unstaged o untracked).

### Paso 2: Validación y Commit de cambios pendientes (si los hay)
1. Si hay cambios pendientes:
   - Ejecutar la suite de pruebas del proyecto según el stack definido:
     ```bash
     uv run python -m unittest discover -s tests -v
     ```
   - Si los tests fallan, detener el workflow e informar al usuario para resolverlos antes de continuar.
   - Si los tests pasan correctamente, preparar los cambios y realizar el commit:
     ```bash
     git add .
     git commit -m "<mensaje descriptivo de los cambios realizados>"
     ```
   - Hacer push a la rama actual en el repositorio remoto:
     ```bash
     git push origin <rama-actual>
     ```
2. Si no hay cambios pendientes, continuar al Paso 3.

### Paso 3: Preguntar por creación de Pull Request
1. Preguntar explícitamente al usuario:
   > *"¿Deseas abrir un Pull Request con los cambios realizados hasta el momento?"*
2. Si el usuario responde **SÍ**:
   - Comprobar si `gh` CLI está disponible o si se cuenta con la herramienta adecuada.
   - Si está disponible, ejecutar `gh pr create --fill` o con título/descripción adecuados.
   - Si no está disponible, proporcionar el enlace web directo al repositorio en GitHub para abrir el PR.
3. Si el usuario responde **NO**:
   - Continuar directamente al Paso 4.

### Paso 4: Solicitar el nombre del nuevo requisito
1. Solicitar al usuario el nombre o identificador del nuevo requisito en el que va a trabajar (por ejemplo, `feat/cag-prompt-tuning` o `fix-rate-limits`).

### Paso 5: Crear y posicionarse en la nueva rama
1. Asegurarse de tener la versión más reciente de `main` (o la rama base configurada):
   ```bash
   git checkout main
   git pull origin main
   ```
2. Crear la nueva rama para el requisito y posicionarse en ella:
   ```bash
   git checkout -b <nombre-del-requisito>
   ```
3. Confirmar al usuario que la sesión está abierta, indicando la rama activa actual y que el entorno está listo para comenzar el desarrollo.
