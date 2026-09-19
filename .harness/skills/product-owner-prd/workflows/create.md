# CREATE — Crear un PRD

Usa este flujo cuando no exista un PRD autoritativo o el usuario pida crear uno desde el producto existente.

1. Inspecciona instrucciones, documentación de producto, README, código relevante y tests. No leas todo el repositorio por defecto.
2. Separa hechos observables, evidencia disponible, decisiones existentes, hipótesis, supuestos, riesgos y preguntas abiertas.
3. Define actor, problema o job, resultado observable, alcance mínimo y exclusiones. No conviertas automáticamente la solución propuesta en requisito.
4. Redacta `docs/product/PRD.md` siguiendo `references/prd-schema.md`. Omite secciones sin información útil; no rellenes boilerplate inventado.
5. Asigna IDs estables a requisitos, flujos, reglas, hipótesis y métricas. Usa criterios de aceptación Given/When/Then para los requisitos relevantes.
6. Si se toma una decisión material, registra también `docs/product/DECISIONS.md` usando `references/decision-log.md`.
7. Añade el cambio al changelog del PRD y verifica que el documento no describa como implementado lo que solo está planificado.

Resultado esperado: un PRD autoritativo, trazable y explícito sobre alcance, incertidumbre y comportamiento deseado.
