---
trigger: always_on
---

# Evolución y consistencia de especificaciones agénticas (AI Specs)

Esta regla define el proceso obligatorio para aprender del feedback del
usuario, proponer mejoras en las especificaciones del agente (`.harness/`) y
asegurar que ningún cambio introduzca contradicciones, inconsistencias o
referencias rotas en el sistema agéntico.

## 1. Captura de feedback y aprendizaje continuo

- El agente **MUST** analizar activamente las interacciones con el usuario
  (sugerencias, correcciones, aclaraciones o preferencias expresadas) para
  identificar oportunidades de mejora en las reglas, workflows o skills.
- El agente **MUST NOT** esperar únicamente instrucciones explícitas de cambio
  para detectar desalineaciones entre las reglas actuales y las expectativas del
  usuario.

## 2. Anti-patrones prohibidos en la modificación de especificaciones

El agente **MUST NOT** incurrir en ninguno de los siguientes comportamientos:

- **Modificación no autorizada (Skipping Approval Process):** Aplicar cambios
  en `.harness/` sin obtener previamente la revisión y aprobación explícita del
  usuario.
- **Propuestas desvinculadas (Unlinked Proposals):** Proponer modificaciones en
  las reglas sin vincularlas de forma clara y directa con el feedback o la
  lección aprendida durante la interacción.
- **Modificaciones imprecisas (Imprecise Modifications):** Proponer cambios
  vagos o genéricos sin identificar con exactitud el fichero de regla y la
  sección o directriz específica que se pretende modificar.
- **Feedback ignorado (Unaddressed Feedback):** No iniciar el proceso de
  propuesta cuando el usuario proporcione feedback relevante aplicable a las
  reglas del proyecto.
- **Desviación de alcance (Scope Creep):** Modificar o proponer cambios en
  múltiples reglas no relacionadas simultáneamente, o exceder el alcance del
  aprendizaje concreto.
- **Modificaciones espontáneas (Unprompted Rule Changes):** Alterar o crear
  reglas por iniciativa propia sin conexión causal con un feedback real o una
  necesidad operativa verificada.
- **Omisión de confirmación (Missing Update Confirmation):** No notificar al
  usuario de forma clara una vez que el cambio de regla aprobado haya sido
  implementado.

## 3. Protocolo de propuesta y aprobación de cambios

Cuando el agente identifique una oportunidad de mejora a partir del feedback:

1. **MUST** formular una propuesta concreta al usuario indicando:
   - El feedback o aprendizaje origen.
   - El archivo exacto dentro de `.harness/rules/` (o la categoría correspondiente)
     que se propone crear o modificar.
   - El texto o directriz normativa (MUST / MUST NOT) exacta a añadir, cambiar o
     eliminar.
2. **MUST** esperar la confirmación o ajuste por parte del usuario antes de
   tocar cualquier archivo en `.harness/`.
3. Tras la aprobación e implementación, **MUST** notificar explícitamente al
   usuario el cambio realizado.

## 4. Verificación de consistencia y no-contradicción

Siempre que se cree, modifique, renombre o elimine cualquier archivo dentro de
la carpeta `.harness/`, el agente **MUST** verificar que el cambio no introduce
conflictos ni contradicciones con el resto de especificaciones existentes.

Esta verificación **MUST** cubrir como mínimo:
- Que ninguna nueva instrucción contradiga una regla existente.
- Que ningún paso de un workflow entre en conflicto con una regla o skill.
- Que ninguna skill defina comportamientos que violen una regla vigente.
- Que ninguna regla imposibilite la ejecución de un workflow.
- Que no se introduzcan especificaciones duplicadas ni ambiguas.
- Que no queden enlaces o referencias rotas hacia archivos renombrados o
  eliminados.
- Que la terminología, el idioma ([`.harness/rules/language-standards.md`](language-standards.md))
  y el alcance sigan siendo coherentes en todo `.harness/`.

### Protocolo ante incoherencias detectadas

Si el agente detecta una contradicción, ambigüedad o referencia rota, **MUST NOT**
resolverla de forma silenciosa. En su lugar, **MUST**:
1. Informar claramente al usuario del conflicto detectado.
2. Identificar los archivos y especificaciones afectadas.
3. Explicar la naturaleza de la contradicción en términos concretos y su impacto.
4. Solicitar la decisión del usuario antes de aplicar cualquier cambio
   correctivo.
