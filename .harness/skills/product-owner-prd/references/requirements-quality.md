# Calidad de requisitos

## Requisito observable

Un requisito describe comportamiento verificable, no una tarea técnica. Debe aclarar, cuando sea relevante:

- actor;
- problema o job;
- resultado esperado;
- comportamiento observable;
- prioridad;
- criterios de aceptación;
- casos límite;
- reglas, permisos y dependencias;
- incertidumbre, si existe.

Preferir:

> Un propietario puede revocar una invitación pendiente antes de que sea aceptada. Tras revocarla, el enlace deja de permitir la incorporación.

Evitar:

> Crear un endpoint de revocación y un botón rojo.

## Criterios de aceptación

Usa Given/When/Then y cubre el flujo principal y los fallos relevantes:

```text
Given [precondición observable]
When [acción o evento]
Then [resultado observable]
And [regla, estado o efecto adicional]
```

Considera permisos, estados inválidos, acciones duplicadas, acciones destructivas, concurrencia, resultados vacíos, fallos de integración y recuperabilidad cuando afecten al producto.

## Alcance y MVP

Incluye una capacidad en el alcance actual solo si habilita el outcome principal, evita que el flujo falle, mitiga un riesgo inaceptable, responde a una restricción obligatoria o valida una hipótesis importante. Clasifica el resto como posterior, futuro o fuera de alcance.

## Incertidumbre

Distingue siempre:

- `FACT`: observable en el repositorio o producto.
- `EVIDENCE`: investigación, datos o feedback disponible.
- `DECISION`: elección intencional.
- `HYPOTHESIS`: creencia falsable.
- `ASSUMPTION`: elección o creencia aún no validada.
- `RISK`: condición que puede reducir valor o viabilidad.
- `OPEN QUESTION`: decisión de impacto aún sin resolver.

No inventes datos ni conviertas una implementación en evidencia de valor.

## Identificadores

Usa IDs estables como `REQ-AUTH-001`, `RULE-BILLING-001`, `FLOW-ONBOARDING-001` y `HYP-ACTIVATION-001`. No renumeres por estética; marca como deprecated lo obsoleto y enlaza su sustituto cuando sea necesario.
