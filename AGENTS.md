# AGENTS.md

## Propósito

Este repositorio utiliza una arquitectura multiagente basada en capacidades.

La fuente canónica de trabajo es:

    /AGENTS.md
    /.agents/

`AGENTS.md` es la puerta de entrada universal para cualquier agente de IA.

La carpeta `.agents/` contiene el contenido operativo real del proyecto:

- reglas;
- workflows;
- skills;
- perfiles de agente;
- hooks;
- plantillas.

Los ficheros específicos de herramientas como Claude Code, GitHub Copilot, Gemini CLI, Cursor, Codex, Windsurf o Devin deben funcionar solo como adaptadores mínimos. No deben duplicar instrucciones largas.

---

## Principios de diseño

1. Mantener la raíz del repositorio lo más limpia posible.
2. Usar `AGENTS.md` como punto de entrada universal.
3. Usar `.agents/` como fuente única de contenido operativo.
4. Evitar duplicar reglas, workflows o skills en carpetas específicas de proveedor.
5. Evitar symlinks como mecanismo principal de compatibilidad.
6. Usar archivos puente mínimos cuando una herramienta exija una ruta concreta.
7. Usar hooks, pruebas y validaciones para controles que deban ser verificables.
8. No asumir convenciones del proyecto si no están documentadas.

---

## Estructura canónica

    .agents/
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
2. `/.agents/manifest.yaml`
3. Las reglas relevantes en `/.agents/rules/`
4. El workflow aplicable en `/.agents/workflows/`
5. La skill necesaria en `/.agents/skills/`
6. El perfil de agente adecuado en `/.agents/agents/`, si procede
7. Los hooks relevantes en `/.agents/hooks/`, si la tarea modifica ficheros o genera artefactos
8. Las plantillas necesarias en `/.agents/templates/`

No es obligatorio cargar todos los documentos de `.agents/`.

El agente debe cargar solo los documentos relevantes para la tarea.

---

## Precedencia documental

Si varios documentos contienen instrucciones relacionadas, aplicar esta precedencia:

1. Solicitud explícita del usuario
2. Reglas de seguridad y restricciones del entorno
3. `/AGENTS.md`
4. `/.agents/manifest.yaml`
5. `/.agents/rules/`
6. `/.agents/workflows/`
7. `/.agents/skills/`
8. `/.agents/agents/`
9. `/.agents/hooks/`
10. `/.agents/templates/`
11. Archivos puente específicos de herramientas

Los archivos puente de herramientas nunca deben prevalecer sobre `/AGENTS.md` ni sobre `.agents/`.

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

    /.agents/rules/


---

### Workflows

Los workflows viven en:

    /.agents/workflows/



---

### Skills

Las skills viven en:

    /.agents/skills/

Cada skill debe seguir esta estructura general:

    skill-name/
    ├── SKILL.md
    ├── scripts/
    └── resources/



---

### Agent profiles

Los perfiles de agente viven en:

    /.agents/agents/


Estos perfiles son portables.

No pertenecen a una herramienta concreta.

---

### Hooks

Las definiciones conceptuales de hooks viven en:

    /.agents/hooks/



Importante: los hooks en `.agents/hooks/` son definiciones portables.

Cada herramienta puede requerir un adaptador propio para ejecutarlos realmente.

---

### Templates

Las plantillas viven en:

    /.agents/templates/



---

## Archivos puente por herramienta

Algunas herramientas requieren ficheros propios para cargar instrucciones.

Esos ficheros deben ser adaptadores mínimos hacia `/AGENTS.md` y `/.agents/`.

Actualmente están definidos los siguientes:

    /.claude/CLAUDE.md
    /.github/copilot-instructions.md
    /.gemini/settings.json
    /.cursor/rules/agents.mdc
    

Los archivos puente deben limitarse a indicar:

1. que `/AGENTS.md` es el punto de entrada;
2. que `/.agents/` es la fuente canónica;
3. que `/.agents/manifest.yaml` debe usarse como índice operativo;
4. que no deben duplicarse instrucciones largas.

---
## Soporte para Codex

Codex utiliza directamente AGENTS.md como entrada del repositorio y descubre las skills en .agents/skills/.

No requiere un archivo puente de instrucciones.

El agente debe consultar .agents/manifest.yaml y seguir el orden de lectura definido en este documento.


---

## Política sobre duplicación

No duplicar en adaptadores específicos el contenido de:

    /.agents/rules/
    /.agents/workflows/
    /.agents/skills/
    /.agents/agents/
    /.agents/hooks/
    /.agents/templates/

Si una herramienta necesita un formato propio, crear un puente mínimo o generar un adaptador derivado desde `.agents/`.

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

Antes de finalizar cambios en AGENTS.md, .agents/ o sus adaptadores
específicos de herramienta, seguir:

.agents/workflows/governance-check.md

El workflow utiliza obligatoriamente:

.agents/skills/artifact-governance/SKILL.md

Aplicar las listas pertinentes y entregar el informe mediante:

.agents/templates/completion-report.md

Esta revisión no se exige para cambios ordinarios de código que
no afecten a la configuración agéntica.
---

## Uso recomendado por cualquier agente

Cuando un agente entre en este repositorio, debe actuar así:

1. Leer `/AGENTS.md`.
2. Leer `/.agents/manifest.yaml`.
3. Identificar la tarea solicitada.
4. Seleccionar las reglas relevantes.
5. Seleccionar el workflow aplicable.
6. Cargar las skills necesarias.
7. Usar el perfil de agente adecuado si la tarea lo requiere.
8. Aplicar los hooks conceptuales relevantes.
9. Ejecutar la validación mínima posible.
10. Entregar un reporte final siguiendo `/.agents/templates/completion-report.md`, si existe.

---

## Nota final

`AGENTS.md` no sustituye a las reglas, workflows ni skills.

Su función es orientar al agente hacia la fuente correcta.

La fuente operativa real del proyecto es:

    /.agents/