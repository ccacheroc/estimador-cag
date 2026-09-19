---
trigger: model_decision
---

# Tecnologías del proyecto

Esta regla define la selección del stack, no la estructura concreta ni sus
convenciones de uso. El estado implementado se documenta en
`@docs/architecture-state.md`; las convenciones pertenecen a
`@.harness/rules/backend-standards.md` y
`@.harness/rules/frontend-standards.md`.

## Stack

- El código de aplicación **MUST** usar la versión de Python declarada en
  `pyproject.toml`.
- La API HTTP **MUST** usar FastAPI sobre ASGI y contratos Pydantic.
- La configuración tipada **MUST** usar Pydantic Settings.
- La integración con OpenAI **MUST** usar el SDK oficial y la API Responses.
- La interfaz web **MUST** usar Streamlit mientras no exista una decisión que
  sustituya esta tecnología.
- Las pruebas End-to-End (E2E) de navegador **MUST** usar Playwright
  (`pytest-playwright`), respaldadas por `@docs/decisions/ADR-002-playwright-e2e.md`.
- Las dependencias y comandos **MUST** gestionarse según
  `@.harness/rules/uv-dependency-management.md`; esta regla **MUST NOT**
  duplicar ese proceso.

## Evolución del stack

- Antes de incorporar un framework, proveedor o dependencia alternativos, el
  agente **MUST** comprobar que el stack existente no cubre el requisito.
- Sustituir una tecnología principal o añadir una nueva categoría de
  infraestructura **MUST** quedar respaldado por una decisión de arquitectura.
- Todo cambio del stack **MUST** actualizar `pyproject.toml`, `uv.lock` cuando
  corresponda y `@docs/architecture-state.md` en la misma tarea.
- Si el requisito no puede satisfacerse con el stack vigente y no existe una
  decisión aprobada, el agente **MUST** pedir confirmación antes de cambiarlo.

Las versiones declaradas tienen como fuentes canónicas `pyproject.toml` y
`uv.lock`; **MUST NOT** mantenerse una copia de esas versiones en esta regla.
