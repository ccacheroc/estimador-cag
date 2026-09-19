---
trigger: model_decision
---

# Convenciones de testing

Esta regla define los criterios transversales para probar backend, frontend y
sus integraciones. Las herramientas y comandos **MUST** seguir
`@.harness/rules/uv-dependency-management.md`.

## Alcance y diseño

- Todo comportamiento nuevo y toda corrección de un defecto **MUST**
  desarrollarse mediante TDD estricto: primero se crea o modifica la prueba
  ejecutable más pequeña y se comprueba que falla por la razón esperada;
  después se escribe el mínimo código de producción que la hace pasar; por
  último se refactoriza manteniendo las pruebas en verde.
- El agente **MUST NOT** escribir el código de producción del nuevo
  comportamiento antes de observar el fallo esperado. Una prueba que falla por
  sintaxis, configuración o una causa ajena al comportamiento **MUST NOT**
  considerarse una fase roja válida.
- Una refactorización que no cambia comportamiento **MUST** partir de pruebas
  relevantes en verde y mantenerlas en verde; **MUST NOT** fabricar una prueba
  fallida artificialmente.
- Los cambios exclusivos de documentación o metadatos sin comportamiento
  ejecutable quedan fuera del ciclo rojo-verde-refactor, pero **MUST** ejecutar
  la validación estructural aplicable.
- Las pruebas **MUST** verificar comportamiento observable y contratos, no
  detalles internos que puedan cambiar sin alterar el resultado.
- Cada comportamiento modificado **MUST** cubrir el caso satisfactorio y los
  errores, límites o regresiones relevantes para su riesgo.
- Los nombres de las pruebas **MUST** describir el comportamiento y la
  condición comprobados. La preparación, ejecución y verificación **SHOULD**
  distinguirse con claridad sin comentarios ceremoniales.
- Los artefactos de prueba **MUST** cumplir
  `@.harness/rules/language-standards.md`.
- No se establece un porcentaje mínimo de cobertura. La cobertura **MAY**
  usarse para detectar zonas sin ejercitar, pero **MUST NOT** sustituir la
  verificación de escenarios significativos.

## Aislamiento y determinismo

- Las pruebas automatizadas **MUST NOT** depender de red real, credenciales,
  costes externos, hora no controlada, orden de ejecución ni estado global
  compartido.
- Los proveedores, bases de datos y otros límites externos **MUST** sustituirse
  en pruebas unitarias. Una prueba de integración que use infraestructura real
  **MUST** identificarse y ejecutarse de forma separada y explícita.
- Los dobles de prueba **MUST** respetar el contrato relevante y **MUST NOT**
  simular la unidad que se pretende verificar.
- Los datos de prueba **SHOULD** ser mínimos, legibles y representativos. La
  aleatoriedad **MUST** fijarse o controlarse para permitir reproducción.

## Fronteras del sistema

- Los casos de uso **MUST** probarse sin levantar una interfaz HTTP o visual.
- Los adaptadores HTTP **MUST** comprobar validación, delegación, contratos de
  respuesta, estados y errores RFC 9457, incluido `application/problem+json`.
- Los adaptadores frontend **MUST** sustituir el caso de uso y cubrir entrada,
  estado de sesión, carga, resultado y errores relevantes.
- Las pruebas End-to-End (E2E) de interfaz web **MUST** usar Playwright
  (`pytest-playwright`), ubicarse bajo `tests/e2e/` y ejecutarse en modo
  *headless* por defecto.
- Toda prueba E2E de navegador **MUST** interceptar o sustituir las llamadas a
  proveedores LLM externos para no incurrir en costes de API ni depender de red
  no determinista.
- El comportamiento asíncrono **MUST** esperarse de forma explícita; los
  rechazos, timeouts y cancelaciones **SHOULD** probarse cuando formen parte del
  contrato o del riesgo del cambio.

## Ejecución y mantenimiento

- El agente **MUST** usar el framework de pruebas ya presente. Incorporar otro
  framework **MUST** justificarse como cambio del stack.
- Las pruebas afectadas **MUST** ejecutarse antes de finalizar la tarea. Cuando
  el riesgo alcance varias capas, **SHOULD** ejecutarse la suite completa.
- Una prueba inestable **MUST** corregirse o aislarse con una causa y un plan de
  resolución explícitos; **MUST NOT** ignorarse silenciosamente.
- Si los criterios de aceptación o el comportamiento esperado son ambiguos, el
  agente **MUST** pedir aclaración antes de codificar la prueba.
