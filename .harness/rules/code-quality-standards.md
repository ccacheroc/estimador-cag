---
trigger: model_decision
---

# Convenciones transversales de calidad de código

Esta regla se aplica a todo el código del proyecto. Las convenciones propias de
cada capa permanecen en sus reglas especializadas.

## Tipado completo

- Todo código **MUST** estar completamente tipado. Toda función y método,
  incluidos los privados y los de prueba, **MUST** declarar los tipos de cada
  parámetro y del retorno.
- Los atributos y variables **MUST** llevar una anotación explícita cuando el
  tipo no pueda inferirse de forma inequívoca en la asignación.
- `Any` **MUST NOT** usarse para omitir el modelado de un tipo. Solo **MAY**
  aparecer en la frontera inevitable con una dependencia sin tipos y **MUST**
  validarse o estrecharse a un tipo concreto antes de entrar en el código del
  proyecto.
- Una supresión de Pyright **MUST** ser local, incluir una
  justificación verificable y **MUST NOT** ocultar errores ajenos a esa línea.
- Pyright es el comprobador de tipos canónico. Todo cambio de código **MUST**
  validarse con `uv run --no-sync pyright` y **MUST** respetar la configuración
  declarada en `pyproject.toml`.
- Pyright **MUST** ejecutarse en modo `strict` para todas las rutas incluidas;
  un agente **MUST NOT** reducir el nivel ni ampliar exclusiones para silenciar
  errores.

## Nombres

- Los nombres **MUST** expresar el concepto de dominio o la responsabilidad que
  representan y **MUST NOT** depender de abreviaturas ambiguas.
- Los módulos, funciones y variables **MUST** usar `snake_case`; las clases,
  `PascalCase`; y las constantes, `UPPER_SNAKE_CASE`.
- Los nombres **MUST** seguir `@.harness/rules/language-standards.md`.

## Repetición y abstracciones

- El código parecido **MUST NOT** abstraerse únicamente por similitud
  estructural. Una abstracción compartida **MUST** representar un mismo
  concepto y agrupar piezas que deban evolucionar juntas.
- Se aplica la Rule of Three: antes de crear una abstracción reutilizable
  **MUST** existir evidencia de, al menos, tres usos reales del mismo concepto.
- Cuando tres o más usos representen el mismo concepto y deban cambiar juntos,
  el agente **MUST** extraer la abstracción compartida más pequeña que preserve
  contratos y claridad.
- Si no está claro si los usos comparten concepto o ciclo de cambio, el agente
  **MUST** mantener la duplicación explícita y pedir una decisión antes de
  introducir la abstracción.
