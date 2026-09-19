# AGENTS.md

## Propósito

Este repositorio utiliza una arquitectura multiagente basada en capacidades.

La fuente canónica de trabajo es:

    /AGENTS.md
    /.harness/

`AGENTS.md` es la puerta de entrada universal para cualquier agente de IA.

La carpeta `.harness/` contiene el contenido operativo real del proyecto:

- reglas;
- skills;
- perfiles de agente;
- hooks;
- workflows;
- plantillas.

Los ficheros específicos de herramientas como Claude Code, GitHub Copilot, Gemini CLI, Cursor, Codex, Windsurf o Devin deben funcionar solo como adaptadores mínimos. No deben duplicar instrucciones largas.

---

## Principios de diseño

1. Mantener la raíz del repositorio lo más limpia posible.
2. Usar `AGENTS.md` como punto de entrada universal.
3. Usar `.harness/` como fuente única de contenido operativo.
4. Evitar duplicar reglas, skills, agents, hooks o templates en carpetas específicas de proveedor.
5. Evitar symlinks. En su lugar, usar archivos puente mínimos cuando una herramienta exija una ruta concreta.
6. Usar hooks, pruebas y validaciones para controles que deban ser verificables.
7. No asumir convenciones del proyecto si no están documentadas.

---

## Estructura canónica

    .harness/
    ├── manifest.yaml   # Índice máquina-legible del sistema agéntico
    ├── rules/          # Reglas globales del repositorio
    ├── workflows/      # Procesos paso a paso
    ├── skills/         # Capacidades reutilizables
    ├── agents/         # Perfiles de agente especializados
    ├── hooks/          # Definiciones conceptuales de validación y control
    └── templates/      # Plantillas de planes, revisiones y reportes finales

---

## Orden de lectura obligatorio

Antes de iniciar una tarea, cualquier agente debe leer en este orden:

1. `/AGENTS.md`
2. `/.harness/manifest.yaml`
3. Las reglas relevantes en `/.harness/rules/`
4. El workflow aplicable en `/.harness/workflows/`
5. La skill necesaria en `/.harness/skills/`
6. El perfil de agente adecuado en `/.harness/agents/`, si procede
7. Los hooks relevantes en `/.harness/hooks/`, si la tarea modifica ficheros o genera artefactos
8. Las plantillas necesarias en `/.harness/templates/`

No es obligatorio cargar todos los documentos de `.harness/`.

El agente debe cargar solo los documentos relevantes para la tarea.

---

## Delegación obligatoria en agentes especializados

Ante cualquier solicitud del usuario, el agente de entrada debe consultar la
sección `inventory.harness` de `/.harness/manifest.yaml` antes de comenzar el
trabajo.

Si existe un perfil en `/.harness/agents/` especializado en la tarea solicitada:

1. Debe seleccionar el perfil cuyo ámbito coincida de forma más específica con
   la tarea.
2. Debe delegar en ese agente la tarea completa o la parte especializada,
   proporcionándole la solicitud del usuario, el contexto relevante del
   repositorio y las reglas, workflows y skills aplicables.
3. Debe esperar a que el agente delegado finalice y devuelva su resultado antes
   de redactar la respuesta final al usuario.
4. Debe verificar que el resultado respeta las instrucciones del repositorio,
   la evidencia disponible y la validación exigida antes de integrarlo.

La delegación no amplía permisos ni autoriza acciones fuera del alcance pedido
por el usuario. El agente de entrada conserva la responsabilidad sobre la
respuesta final y debe informar si el agente delegado queda bloqueado o no
puede validar una parte del trabajo.

Un agente especializado no debe delegar de nuevo la misma tarea a su propio
perfil. Puede delegar una parte distinta en otro perfil cuando exista una
especialización clara y no se cree un ciclo.

Si el entorno de ejecución no ofrece una capacidad real de delegación, el
agente no debe fingir que la ha realizado. Debe indicarlo brevemente, cargar el
perfil especializado y ejecutar sus instrucciones directamente como fallback.

---

## Precedencia documental

Si varios documentos contienen instrucciones relacionadas, aplicar esta precedencia:

1. Solicitud explícita del usuario
2. Reglas de seguridad y restricciones del entorno
3. `/AGENTS.md`
4. `/.harness/manifest.yaml`
5. `/.harness/rules/`
6. `/.harness/workflows/`
7. `/.harness/skills/`
8. `/.harness/agents/`
9. `/.harness/hooks/`
10. `/.harness/templates/`
11. Archivos puente específicos de herramientas

Los archivos puente de herramientas nunca deben prevalecer sobre `/AGENTS.md` ni sobre `.harness/`.

---

## Reglas globales de operación

Todo agente que trabaje en este repositorio debe cumplir estas reglas:

- No inventar convenciones del proyecto.
- No modificar ficheros protegidos, generados o de entrega oficial salvo que el workflow lo permita explícitamente.
- No duplicar instrucciones largas en carpetas específicas de proveedor.
- No crear nuevas carpetas, workflows, skills o scripts sin una razón clara.
- No realizar cambios destructivos sin confirmación.
- Antes de editar, identificar qué reglas y workflow aplican.
- Después de editar, ejecutar la validación mínima relevante.
- Si no se puede validar, indicarlo explícitamente.
- No afirmar que una validación se ha realizado si no se ha ejecutado realmente.
- Mantener los cambios pequeños, trazables y justificados.

---

## Contenido operativo actual

### Rules

Las reglas globales viven en:

    /.harness/rules/

La regla `/.harness/rules/ponytail.md` establece el criterio de implementar la
solución mínima necesaria, priorizando reutilización, capacidades nativas y la
corrección de la causa raíz.


---

### Workflows

Los workflows viven en:

    /.harness/workflows/



---

### Skills

Las skills viven en:

    /.harness/skills/

Cada skill debe seguir esta estructura general:

    skill-name/
    ├── SKILL.md
    ├── scripts/
    └── resources/



---

### Agent profiles

Los perfiles de agente viven en:

    /.harness/agents/


Estos perfiles son portables.

No pertenecen a una herramienta concreta.

El agente de entrada debe descubrirlos mediante `/.harness/manifest.yaml` y
aplicar la política de delegación definida en este documento.

---

### Hooks

Las definiciones conceptuales de hooks viven en:

    /.harness/hooks/



Importante: los hooks en `.harness/hooks/` son definiciones portables.

Cada herramienta puede requerir un adaptador propio para ejecutarlos realmente.

---

### Templates

Las plantillas viven en:

    /.harness/templates/



---

## Archivos puente por herramienta

Algunas herramientas requieren ficheros propios para cargar instrucciones.

Esos ficheros deben ser adaptadores mínimos hacia `/AGENTS.md` y `/.harness/`.

Actualmente están definidos los siguientes:

    /.claude/CLAUDE.md
    /.github/copilot-instructions.md
    /.github/agents/product-strategy-analyst.agent.md
    /.github/agents/backend-developer.agent.md
    /.github/agents/frontend-developer.agent.md
    /.github/agents/qa-analyst.agent.md
    /.gemini/settings.json
    /.cursor/rules/agents.mdc
    /.codex/agents/product-strategy-analyst.toml
    /.codex/agents/backend-developer.toml
    /.codex/agents/frontend-developer.toml
    /.codex/agents/qa-analyst.toml
    /.agent/rules/agents.md
    /.agent/workflows/abrir-sesion.md
    /.agent/workflows/cerrar-sesion.md
    

Los archivos puente deben limitarse a indicar:

1. que `/AGENTS.md` es el punto de entrada;
2. que `/.harness/` es la fuente canónica;
3. que `/.harness/manifest.yaml` debe usarse como índice operativo;
4. que no deben duplicarse instrucciones largas.

---
## Soporte para Codex

Codex utiliza directamente AGENTS.md como entrada del repositorio y descubre las skills en .harness/skills/.

No requiere un archivo puente de instrucciones.

Cuando Codex necesite ejecutar un perfil portable como subagente, puede usar un
adaptador mínimo en `/.codex/agents/`. El adaptador debe limitarse a identificar
el perfil canónico de `/.harness/agents/`; no debe duplicar sus instrucciones.

El agente debe consultar .harness/manifest.yaml y seguir el orden de lectura definido en este documento.


---

## Soporte para Antigravity

Antigravity busca sus especificaciones en la carpeta `/.agent/` (en singular).

Para mantener `/.harness/` como fuente canónica única sin duplicar instrucciones ni depender de symlinks, se utiliza `/.agent/` con adaptadores puente mínimos:

- `/.agent/rules/agents.md`: regla persistente (`trigger: always_on`) que instruye a Antigravity a leer `/AGENTS.md` y `/.harness/manifest.yaml`.
- `/.agent/workflows/`: adaptadores mínimos para invocar los workflows canónicos de `/.harness/workflows/` (ej. `/abrir-sesion`, `/cerrar-sesion`).
- `/.agent/skills/`: adaptadores con `SKILL.md` para el descubrimiento semántico de skills de `/.harness/skills/`.

---

## Política sobre duplicación

No duplicar en adaptadores específicos el contenido de:

    /.harness/rules/
    /.harness/workflows/
    /.harness/skills/
    /.harness/agents/
    /.harness/hooks/
    /.harness/templates/

Si una herramienta necesita un formato propio, crear un puente mínimo o generar un adaptador derivado desde `.harness/`.

---

## Política sobre symlinks

No usar symlinks como mecanismo principal de compatibilidad.

Motivos:

- pueden fallar en Windows o entornos corporativos;
- algunos IDEs, agentes o runners no los siguen de forma consistente;
- dificultan el diagnóstico cuando una herramienta ve un fichero y otra no;
- pueden introducir ambigüedad sobre cuál es la fuente real.

Preferir siempre archivos puente reales y mínimos.

---

## Criterios mínimos de finalización

Al terminar una tarea, el agente debe informar de forma breve:

1. Qué ha cambiado.
2. Qué ficheros ha modificado.
3. Qué comandos ha ejecutado.
4. Qué validación ha realizado.
5. Qué supuestos ha hecho.
6. Qué riesgos o dudas quedan.
7. Qué revisión humana recomienda, si procede.

Si no se ha modificado nada, debe indicarlo explícitamente.

Si no se ha podido validar, debe explicar por qué.

---
## Revisión de gobernanza

Antes de finalizar cambios en AGENTS.md, .harness/ o sus adaptadores
específicos de herramienta, seguir la skill:

.harness/skills/governance-check/SKILL.md

Aplicar las listas pertinentes y entregar el informe mediante:

.harness/templates/completion-report.md

Esta revisión no se exige para cambios ordinarios de código que
no afecten a la configuración agéntica.
---

## Uso recomendado por cualquier agente

Cuando un agente entre en este repositorio, debe actuar así:

1. Leer `/AGENTS.md`.
2. Leer `/.harness/manifest.yaml`.
3. Identificar la tarea solicitada y comprobar si existe un perfil especializado.
4. Seleccionar las reglas relevantes.
5. Seleccionar el workflow aplicable.
6. Cargar las skills necesarias y el perfil especializado, si procede.
7. Delegar la tarea o parte especializada con el contexto aplicable.
8. Aplicar los hooks conceptuales relevantes.
9. Esperar y verificar el resultado de cualquier delegación activa.
10. Ejecutar la validación mínima posible.
11. Entregar un reporte final siguiendo `/.harness/templates/completion-report.md`, si existe.

---

## Nota final

`AGENTS.md` no sustituye a las reglas, workflows ni skills.

Su función es orientar al agente hacia la fuente correcta.

La fuente operativa real del proyecto es:

    /.harness/
