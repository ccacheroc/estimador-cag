---
trigger: model_decision
---

# Convenciones de desarrollo backend

Esta regla define convenciones estables. El estado concreto de la arquitectura
se documenta en `@docs/architecture-state.md` y **MUST NOT** duplicarse aquí.
Todo código backend **MUST** cumplir `@.harness/rules/code-quality-standards.md`
y `@.harness/rules/language-standards.md`.

## Responsabilidades y dependencias

- El punto de composición **MUST** limitarse a crear la aplicación, registrar
  adaptadores y aplicar configuración transversal.
- Los adaptadores de entrada **MUST** validar el contrato, delegar el caso de
  uso y traducir su resultado o sus errores al protocolo correspondiente.
- La lógica de negocio y de integración **MUST** residir fuera de los
  adaptadores de entrada y **MUST** poder probarse sin levantar un servidor.
- Los contratos de entrada y salida **MUST** ser explícitos y estar separados
  de la implementación del caso de uso.
- Las dependencias **MUST** apuntar desde las capas de entrega hacia los casos
  de uso; la lógica reutilizable **MUST NOT** depender de HTTP ni de una UI.

## Contratos HTTP y errores

- Las respuestas satisfactorias **MUST** declarar un contrato explícito.
- Toda respuesta HTTP de error con cuerpo **MUST** seguir
  [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) y usar el media type
  `application/problem+json`.
- Cada Problem Details **MUST** incluir `type`, `title`, `status` y `detail`.
  `status` **MUST** coincidir con el estado HTTP; `type` **MUST** identificar
  de forma estable el tipo de problema; y `title` **MUST** permanecer estable
  para ese tipo, salvo localización.
- `detail` **MUST** ser una explicación accionable en español para esa
  ocurrencia y **MUST NOT** contener información de depuración. Los clientes
  **MUST NOT** necesitar interpretar `detail`; los datos procesables por
  máquina **MUST** exponerse mediante extensiones del problema.
- `instance` **SHOULD** identificar la ocurrencia concreta cuando exista un
  identificador seguro que pueda exponerse. Los campos estándar de RFC 9457
  **MUST NOT** redefinirse con otra semántica.
- Las respuestas de error **MUST NOT** revelar secretos, trazas internas,
  prompts, transcripciones completas ni respuestas crudas de proveedores.

## Integraciones y configuración

- Las operaciones de red usadas desde un flujo asíncrono **MUST** ser no
  bloqueantes. Si una dependencia es síncrona, su aislamiento **MUST** quedar
  explícito fuera del event loop.
- La configuración **MUST** centralizarse y entrar desde el entorno. Los
  secretos **MUST NOT** almacenarse en el código ni en archivos versionados.
- Los errores de infraestructura **MUST** convertirse en errores estables del
  límite de entrega sin exponer credenciales ni detalles sensibles.
- Un cambio incompatible de contrato **MUST** versionarse o acompañarse de una
  migración explícita.

## Logging y correlación

- El backend **MUST** emitir logs estructurados con, al menos, nivel, evento y
  contexto suficiente para diagnosticar la operación.
- Cada petición **MUST** aceptar o generar un identificador de correlación y
  **MUST** propagarlo por las capas y llamadas externas relacionadas.
- Los logs **MUST NOT** incluir secretos, credenciales, transcripciones
  completas, prompts completos ni cargas o respuestas crudas de proveedores.
- Los errores **MUST** registrarse una sola vez en la frontera que los gestiona
  con el contexto disponible; las capas inferiores **SHOULD** propagarlos sin
  producir registros duplicados.
- El código de aplicación **MUST NOT** usar `print` como mecanismo de logging.

## Verificación y documentación

- Toda verificación **MUST** seguir
  `@.harness/rules/testing-standards.md`.
- Todo cambio estructural del backend **MUST** actualizar
  `@docs/architecture-state.md` en la misma tarea.
- Si una responsabilidad no encaja claramente en una capa, el agente **MUST**
  pedir una decisión antes de crear una dependencia entre capas.

## Ejemplos actuales

- `app/main.py` ejemplifica un punto de composición breve.
- `app/routers/` ejemplifica adaptadores HTTP y `app/schemas/` sus contratos.
- `app/services/` ejemplifica lógica reutilizable por múltiples entradas.
