---
trigger: model_decision
---

# Convenciones de desarrollo frontend

Esta regla define convenciones estables. El estado concreto de la arquitectura
se documenta en `@docs/architecture-state.md` y **MUST NOT** duplicarse aquí.
Todo código frontend **MUST** cumplir `@.harness/rules/code-quality-standards.md`
y `@.harness/rules/language-standards.md`.

## Responsabilidades y dependencias

- El frontend **MUST** actuar como adaptador de presentación: recoger entrada,
  mostrar estado y resultados, y delegar los casos de uso.
- La interfaz **MUST NOT** duplicar lógica de negocio, construcción de prompts,
  acceso directo a proveedores externos ni carga de secretos.
- El frontend **MUST** reutilizar el servicio o contrato canónico del caso de
  uso en lugar de mantener una implementación paralela.
- El estado mutable **MUST** tener un propietario y un alcance explícitos. El
  estado de una sesión **MUST NOT** convertirse accidentalmente en estado
  global compartido.

## Interacción y errores

- La entrada del usuario **MUST** validarse en la frontera de presentación sin
  sustituir la validación del contrato backend.
- Las operaciones lentas **MUST** mostrar progreso y **MUST NOT** bloquear el
  ciclo de renderizado cuando la plataforma permita evitarlas.
- Los errores **MUST** ser comprensibles y accionables para el usuario, sin
  exponer credenciales, trazas internas ni datos sensibles.
- Los controles **MUST** tener etiquetas comprensibles y el estado de carga,
  éxito o error **MUST** ser perceptible sin depender solo del color.

## Verificación y documentación

- Toda verificación **MUST** seguir
  `@.harness/rules/testing-standards.md`.
- Todo cambio estructural del frontend **MUST** actualizar
  `@docs/architecture-state.md` en la misma tarea.
- Si el frontend necesita asumir una responsabilidad nueva, el agente **MUST**
  aclarar primero si pertenece a presentación o a una capa compartida.

## Ejemplos actuales

- `app/streamlit_app.py` ejemplifica un adaptador de presentación que reutiliza
  el servicio de estimación y conserva estado limitado a la sesión.
