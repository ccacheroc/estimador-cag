---
description: Integrar la sesión anterior, fijar el estado inicial de la nueva sesión y abrir su rama.
---

# Workflow: Abrir Sesión (`/abrir-sesion`)

## Objetivo

Integrar en `main` el trabajo validado de la sesión anterior y crear, sobre
el mismo commit, un tag recuperable y la rama de trabajo de la nueva sesión.

## Entradas necesarias

- Rama de la sesión anterior.
- Número de la nueva sesión con dos dígitos (`NN`).
- Nombre de la nueva rama, por defecto `<usuario>/sesionNN`.

Si alguna entrada no puede deducirse sin ambigüedad, el agente **MUST**
preguntarla antes de cambiar el repositorio.

## Procedimiento

### 1. Comprobar el estado inicial

1. Ejecutar:

   ```bash
   git branch --show-current
   git status
   ```

2. Confirmar que la rama de la sesión anterior está identificada.
3. Si contiene cambios pendientes, ejecutar primero `/cerrar-sesion`.
4. No cambiar de rama hasta que el directorio de trabajo esté limpio y la
   rama anterior esté subida a `origin`.

### 2. Integrar la sesión anterior

1. Actualizar `main`:

   ```bash
   git switch main
   git pull --ff-only origin main
   ```

2. Integrar la rama anterior:

   ```bash
   git merge <rama-anterior>
   ```

3. Si hay conflictos, detenerse, informar de los ficheros afectados y
   resolverlos antes de continuar.
4. Ejecutar sobre el resultado integrado:

   ```bash
   uv run --no-sync pyright
   uv run pytest
   ```

5. Si alguna validación falla, no publicar `main`, no crear el tag y no crear
   la rama nueva.
6. Si `main` admite push directo, publicar la integración:

   ```bash
   git push origin main
   ```

7. Si `main` exige Pull Request, abrirlo desde la rama anterior y continuar
   solo cuando esté integrado. Crear el Pull Request no equivale a integrar
   sus cambios.

### 3. Crear el punto de inicio recuperable

1. Calcular el tag `inicio-sesion-NN` y comprobar si ya existe localmente o
   en `origin`.
2. Si ya existe, informar del tag y del commit al que apunta y detenerse. Un
   tag publicado **MUST NOT** moverse ni eliminarse sin autorización expresa.
3. Si no existe, crearlo y publicarlo:

   ```bash
   git tag -a inicio-sesion-NN -m "Estado inicial de la sesión NN"
   git push origin inicio-sesion-NN
   ```

### 4. Abrir la rama de la nueva sesión

1. Crear la rama desde el mismo commit etiquetado:

   ```bash
   git switch -c <usuario>/sesionNN inicio-sesion-NN
   ```

2. Comprobar que la rama y el tag apuntan al mismo commit:

   ```bash
   git rev-parse HEAD
   git rev-list -n 1 inicio-sesion-NN
   git status
   ```

3. Informar de la rama activa, el tag publicado, el commit compartido y el
   resultado de las validaciones.
