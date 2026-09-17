# Guía de Decisión de Artefactos: Clasificación, Ubicación y Creación (Decision Guide)

Esta guía establece el protocolo operativo determinista para clasificar, ubicar y estructurar cualquier nuevo artefacto agéntico o cambio solicitado en el repositorio.

Cuando el usuario pida: **«Crea un artefacto que refleje X»**, esta guía define el algoritmo exacto para determinar qué tipo de artefacto crear, en qué ruta ubicarlo, cómo nombrarlo y cómo registrarlo.

---

## 1. Algoritmo Operativo de Clasificación (Árbol de Decisión)

Ante cualquier requerimiento **X**, evalúa las siguientes preguntas en orden secuencial:

```mermaid
flowchart TD
    A["Requerimiento o artefacto X"] --> B{"¿Debe aplicarse como una obligación<br/>estable al agente o al código?"}

    B -- "Sí" --> C["Rule document<br/>.agents/rules/<br/><br/>Ejemplos: architecture.md<br/>techstack.md<br/>testing.md<br/>git-conventions.md<br/>definition-of-done.md"]

    B -- "No" --> D{"¿Describe qué debe hacer<br/>el producto o una feature?"}

    D -- "Sí" --> E["Canonical Project Documentation<br/>docs/<br/>]

    D -- "No" --> F{"¿Explica por qué se tomó una decisión técnica?"}

    F -- "Sí" --> G["Architecture Decision Record<br/>docs/adr/<br/><br/>Context<br/>Alternatives<br/>Decision<br/>Rationale<br/>Consequences<br/>Status"]

    F -- "No" --> H{"¿Es un formato base o esqueleto<br/>para generar documentos?"}

    H -- "Sí" --> I["Template<br/>.agents/templates/"]

    H -- "No" --> J{"¿Debe ejecutarse código en un evento<br/>del ciclo de vida para validar,<br/>bloquear, transformar u observar?"}

    J -- "Sí" --> K["Hook<br/>.agents/hooks/"]

    J -- "No" --> L{"¿Define un rol especializado con<br/>herramientas, modelo o permisos propios?"}

    L -- "Sí" --> M["Agent Profile<br/>.agents/agents/"]

    L -- "No" --> N{"¿Es una capacidad reutilizable que<br/>requiere conocimiento especializado,<br/>variaciones, scripts, referencias,<br/>plantillas o carga progresiva?"}

    N -- "Sí" --> O["Skill<br/>.agents/skills/<nombre>/SKILL.md<br/><br/>Integra aquí el procedimiento ordenado<br/>cuando forma parte de esta capacidad"]

    N -- "No" --> P{"¿El valor principal está en una<br/>secuencia breve, fija y ordenada<br/>invocada explícitamente?"}

    P -- "Sí" --> Q["Standalone Workflow<br/>.agents/workflows/<nombre>.md<br/><br/>Proceso breve, autocontenido<br/>y ejecutable bajo demanda"]

    P -- "No" --> R["Detenerse y pedir<br/>aclaración al usuario"]


    class C rules
    class E docs
    class G adr
    class O skill
    class Q workflow
    class M Agent
    class K Hook
```

### Reglas de Descarte Rápido:
1. **¿Norma o restricción permanente transversal?** $\rightarrow$ **Rule**. No uses Workflow ni Skill si no hay pasos ni herramientas.
2. **¿Secuencia de pasos lineal sin código auxiliar?** $\rightarrow$ **Workflow**. No crees una Skill si solo son 4 o 5 pasos en texto.
3. **¿Procedimiento con lógica de dominio, scripts, plantillas o herramientas?** $\rightarrow$ **Skill**. Permite carga progresiva (*progressive disclosure*) y herramientas dedicadas.
4. **¿Control de calidad o validación previa/posterior a una acción?** $\rightarrow$ **Hook**.
5. **¿Estructura reutilizable de reporte o fichero?** $\rightarrow$ **Template**.
6. **¿Personalidad, permisos o modelo específico?** $\rightarrow$ **Agent Profile**.
7. **¿Conocimiento explicativo sobre el sistema que humanos y agentes deben consultar?** $\rightarrow$ **Documentación Canónica** en `docs/`.

---

## 2. Matriz de Ubicación Canónica y Convenciones

Todo artefacto agéntico en este repositorio debe ubicarse en su carpeta canónica bajo `.agents/` y seguir la convención de nomenclatura `kebab-case`:

| Tipo de Artefacto | Ruta Canónica de Destino | Convención de Fichero | Estructura Mínima Obligatoria |
| --- | --- | --- | --- |
| **Rule** | `.agents/rules/<nombre-en-kebab-case>.md` | `<nombre>.md` | Frontmatter con `trigger:` (`always_on`, `glob`, `model_decision`, `manual`) + Texto normativo con MUST/MUST NOT. |
| **Workflow** | `.agents/workflows/<nombre-en-kebab-case>.md` | `<nombre>.md` | Frontmatter con `description:` + Pasos numerados secuenciales con resultado esperado por paso. |
| **Skill** | `.agents/skills/<nombre-en-kebab-case>/SKILL.md` | Directorio `<nombre>/` y fichero `SKILL.md` | Frontmatter con `name:` y `description:` (con criterios de activación) + Cuándo usar/no usar, procedimiento y verificación. Opcional: `scripts/`, `resources/`. |
| **Hook** | `.agents/hooks/<nombre-en-kebab-case>.md` | `<nombre>.md` | Definición conceptual: evento detonante (trigger), condiciones, validación y acción de bloqueo en fallo. |
| **Template** | `.agents/templates/<nombre-en-kebab-case>.md` | `<nombre>.md` | Estructura con marcadores `<campo>` e instrucciones de uso. |
| **Agent Profile** | `.agents/agents/<nombre-en-kebab-case>.md` | `<nombre>.md` | Rol, responsabilidades, herramientas permitidas/excluidas y contexto de activación. |
| **Doc Canónica** | `docs/<area>/<nombre-en-kebab-case>.md` o `docs/decisions/ADR-XXX-<nombre>.md` | `<nombre>.md` | Contexto, decisión, justificación y consecuencias. |

> **Nota Crítica sobre Adaptadores Específicos:** Los ficheros en `.github/`, `.claude/`, `.cursor/` o `.gemini/` son únicamente **puentes mínimos**. NUNCA crees o dupliques reglas, skills o workflows directamente en esas carpetas; la fuente canónica siempre es `.agents/`.

---

## 3. Criterios de Selección Detallados por Tipo de Artefacto

### A. Rules (`.agents/rules/`)
- **Propósito:** Invariantes, restricciones éticas/arquitectónicas/estilísticas que condicionan la generación.
- **Cuándo elegirlo:**
  - Aplica siempre o bajo un patrón de fichero (`glob`) sin que el usuario tenga que pedirlo.
  - Define lo que el agente **DEBE** o **NO DEBE** hacer.
- **Determinación del modo de activación (Principio del Menor Privilegio):**
  - `glob`: Si aplica solo a ciertos ficheros o extensiones (ej. `app/routers/**/*.py`, `tests/**`).
  - `model_decision`: Si depende del contexto de la conversación pero no es universal.
  - `manual`: Si solo aplica cuando el usuario lo menciona explícitamente.
  - `always_on`: Úsalo únicamente para políticas verdaderamente universales del repositorio (ej. arquitectura base, seguridad, verificación de consistencia).

### B. Workflows (`.agents/workflows/`)
- **Propósito:** Protocolos paso a paso orientados a ejecución ordenada sobre demanda.
- **Cuándo elegirlo:**
  - El valor reside en el orden estricto de las operaciones (`Paso 1 -> Paso 2 -> Paso 3`).
  - El usuario lo invoca intencionalmente (ej. `/release`, `/deploy-staging`).
  - No requiere scripts en Python/Bash empaquetados ni recursos complejos (si los requiere, es una Skill).

### C. Skills (`.agents/skills/`)
- **Propósito:** Paquetes autónomos de capacidad especializada y conocimiento procedimental profundo.
- **Cuándo elegirlo:**
  - Se beneficia de carga bajo demanda progresiva (*progressive disclosure*): el agente lee la descripción corta y solo carga el cuerpo o recursos si la tarea lo requiere.
  - La capacidad contiene o necesita scripts auxiliares (`scripts/`), ejemplos o guías de decisión (`resources/`).
  - La tarea implica know-how técnico especializado (ej. estimación CAG, refactorización compleja, auditoría de seguridad).

### D. Hooks (`.agents/hooks/`)
- **Propósito:** Puntos de control y validación vinculados al ciclo de vida del agente o del desarrollo.
- **Cuándo elegirlo:**
  - Se debe disparar automáticamente antes o después de una acción (ej. pre-commit, post-task, pre-edición).
  - Define una barrera que detiene la ejecución si una condición no se cumple.

### E. Templates (`.agents/templates/`)
- **Propósito:** Esqueletos estandarizados de documentos o respuestas.
- **Cuándo elegirlo:**
  - Se requiere uniformidad estructural (ej. reportes de finalización, tickets de bug, ADRs).
  - No contiene instrucciones ejecutables por sí mismo, sino marcadores que el agente debe completar.

### F. Agent Profiles (`.agents/agents/`)
- **Propósito:** Definición de roles especializados o subagentes con acotación de alcance.
- **Cuándo elegirlo:**
  - Se necesita una perspectiva o persona especializada (ej. revisor de seguridad implacable, redactor de documentación).
  - Se requiere limitar el catálogo de herramientas disponibles para garantizar la seguridad.

---

## 4. Determinación del Ámbito (Global vs Workspace)

- **`workspace` (`.agents/...`)**:
  - Específico de este proyecto: stack FastAPI, modelo CAG, arquitectura hexagonal del repo, reglas internas del equipo.
  - **Ubicación:** Dentro de la raíz del proyecto en `.agents/`.
- **`global` (`~/.agents/...`)**:
  - Preferencias personales del desarrollador transversales a cualquier repositorio (estilo de comunicación, hábitos personales de git, credenciales de entorno global).
  - **Ubicación:** En el home del usuario (ej. `~/.agents/` o configuración de IDE).

---

## 5. Ejemplos Prácticos de Clasificación Directa ("Petición X -> Artefacto y Ruta")

| Petición del Usuario (X) | Tipo Determinado | Ruta Canónica Exacta | Justificación |
| --- | --- | --- | --- |
| *"Quiero que nunca se hagan commits directamente a main y que los mensajes sigan Conventional Commits"* | **Rule** | `.agents/rules/git-workflow.md` | Es una restricción normativa permanente (`trigger: always_on`). |
| *"Crea un artefacto para validar que todos los endpoints de FastAPI tengan response_model explícito"* | **Rule** | `.agents/rules/fastapi-endpoints.md` | Restricción arquitectónica de código (`trigger: glob: app/routers/**/*.py`). |
| *"Crea un artefacto para estimar historias de usuario usando el modelo CAG y generar el JSON final"* | **Skill** | `.agents/skills/cag-estimator/SKILL.md` | Capacidad especializada con instrucciones, ejemplos y posiblemente scripts auxiliares. |
| *"Crea un artefacto que defina la secuencia para preparar una release: tests, subir versión, changelog y tag"* | **Workflow** | `.agents/workflows/release-process.md` | Secuencia procedimental ordenada y ejecutable bajo demanda. |
| *"Crea un artefacto con la plantilla estándar para redactar ADRs (Architecture Decision Records)"* | **Template** | `.agents/templates/adr-template.md` | Estructura esqueleto reutilizable con campos a rellenar. |
| *"Crea un artefacto para un rol de auditor de seguridad que solo revise vulnerabilidades y no edite código"* | **Agent Profile** | `.agents/agents/security-auditor.md` | Definición de rol/persona con restricción de herramientas y foco específico. |
| *"Crea un artefacto que verifique que no se dejen contraseñas ni API keys antes de confirmar una tarea"* | **Hook** | `.agents/hooks/pre-commit-secrets-check.md` | Compuerta de validación en el ciclo de vida del agente. |
| *"Crea un artefacto que explique por qué elegimos FastAPI y Pydantic v2 en lugar de Django"* | **Doc Canónica** | `docs/decisions/ADR-001-fastapi.md` | Decisión de diseño arquitectónica y contexto para humanos y agentes. |

---

## 6. Procedimiento Obligatorio Post-Creación: Registro en `manifest.yaml`

Cada vez que se cree un nuevo artefacto en `.agents/`, se debe registrar en `.agents/manifest.yaml` bajo la sección correspondiente de `inventory`:

```yaml
inventory:
  rules:
    - id: mi-regla
      path: .agents/rules/mi-regla.md
      description: Breve descripción de la restricción.
      applies_to: [coding, git]
  skills:
    - id: mi-skill
      path: .agents/skills/mi-skill/SKILL.md
      description: Breve descripción de la capacidad y cuándo activarla.
```

Si el artefacto es un fichero temporal o no documentado, no debe integrarse en la arquitectura canónica sin pasar por este registro y por el checklist de gobernanza.

