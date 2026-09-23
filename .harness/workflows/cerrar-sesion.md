---
description: Validar, confirmar y subir el trabajo de la sesión actual.
---

# Workflow: Cerrar Sesión (`/cerrar-sesion`)

## Objetivo

Dejar validado, confirmado y subido el trabajo de la sesión actual, sin
integrar automáticamente la rama en `main` ni crear tags.

## Procedimiento

### 1. Revisar el estado y la documentación

1. Ejecutar:

   ```bash
   git branch --show-current
   git status
   git diff
   ```

2. Confirmar que los cambios pertenecen a la sesión actual. No añadir
   indiscriminadamente ficheros ajenos o generados.
3. Revisar y actualizar, cuando proceda, `docs/architecture-state.md`, los ADR,
   `README.md`, `.env.example` y las especificaciones de `.harness/` afectadas.
4. Si cambia `.harness/`, ejecutar `governance-check` antes de confirmar los
   cambios.

### 2. Validar

1. Ejecutar:

   ```bash
   uv run --no-sync pyright
   uv run pytest
   ```

2. Si alguna comprobación falla, detenerse e informar del resultado. No crear
   el commit ni hacer push de cambios no validados.

### 3. Confirmar los cambios

1. Si hay cambios pendientes, seleccionar explícitamente los ficheros que
   pertenecen a la sesión y solicitar la confirmación exigida por
   `.harness/rules/task-change-commit-prompt.md` antes de crear el commit.
2. Crear un commit con un mensaje descriptivo y trazable en español.
3. Si no hay cambios pendientes, informar de ello y continuar.

### 4. Publicar la rama

1. Subir la rama actual, tenga o no commits nuevos desde el último push:

   ```bash
   git push -u origin <rama-actual>
   ```

2. Informar de la rama, el último commit, el resultado de las validaciones y
   el estado del push.

Este workflow **MUST NOT** crear un Pull Request ni un tag. La integración en
`main` y el punto de partida recuperable de la siguiente sesión pertenecen a
`/abrir-sesion`.
