# Esquema de PRD

Usa este esquema como estructura por defecto cuando el repositorio no tenga una convención válida. No rellenes secciones sin evidencia; conserva las secciones relevantes del PRD existente.

```markdown
# Product Requirements Document

## 1. Product Overview
### Product
### Product Goal
### Problem
### Current Scope

## 2. Users and Actors
### [Role]
**Context** / **Primary job** / **Desired outcome** / **Relevant permissions**

## 3. Jobs, Pains and Desired Outcomes
## 4. Product Principles
## 5. Scope
### Current / MVP
### Later
### Future
### Explicitly Out of Scope

## 6. User Journeys and Main Flows
### FLOW-[AREA]-001 — [Flow name]
Actor, trigger, preconditions, main flow, successful outcome, alternative paths, failure paths.

## 7. Product Requirements
### REQ-[AREA]-001 — [Requirement name]
Status, actor, problem/job, expected outcome, requirement, priority, acceptance criteria, edge cases, dependencies, related flows/rules, validation target.

## 8. Business Rules
### RULE-[AREA]-001 — [Rule name]
Rule, reason, applies to, exceptions, related requirements.

## 9. Product Data Model
## 10. Roles and Permissions
## 11. UX Requirements
## 12. Analytics and Success
## 13. Validation
### HYP-[AREA]-001 — [Hypothesis]
## 14. Risks and Assumptions
## 15. Open Questions
## 16. Product Decisions
## 17. Change Log
```

Recommended stable ID prefixes: `REQ-`, `RULE-`, `FLOW-`, `HYP-`, and `METRIC-`. Deprecated IDs remain reserved.
