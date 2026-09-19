---
trigger: model_decision
---

# Convenciones de idioma

Esta regla define el idioma canónico de los artefactos del proyecto. Un
contrato externo o una herramienta generadora **MAY** imponer otro idioma solo
en la superficie que controle.

## Inglés para artefactos técnicos

- Los identificadores de código, módulos, esquemas de datos, campos de API,
  nombres de tablas y columnas, claves de configuración y scripts **MUST**
  escribirse en inglés.
- Los comentarios, docstrings, nombres y descripciones de pruebas, mensajes y
  eventos de log **MUST** escribirse en inglés.
- Los términos técnicos que formen parte de un contrato externo **MUST**
  conservar el nombre definido por ese contrato.

## Español para comunicación y documentación

- La documentación del proyecto, incluidos README, guías, PRD y ADR,
  **MUST** escribirse en español, sin traducir identificadores ni términos
  técnicos cuando la traducción introduzca ambigüedad.
- Los mensajes visibles para el usuario y los detalles accionables de error
  **MUST** escribirse en español, salvo que el producto incorpore una política
  explícita de localización.
- Los mensajes de commit **MUST** escribirse en español y describir el cambio
  de forma concisa y trazable.
