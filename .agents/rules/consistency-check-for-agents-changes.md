---
trigger: always_on
---

# Rule: Consistency Check for `.agents` Changes

Whenever any file inside the `.agents` folder is created, modified, renamed, or deleted, the agent must verify that the change does not introduce contradictions, inconsistencies, or conflicts with the existing specifications in that folder.

This check must cover, at minimum:

- All rules defined in `.agents`
- All workflows defined in `.agents`
- All skills defined in `.agents`
- Any configuration, instruction, or metadata file that affects how agents behave
- Cross-references between rules, workflows, skills, hooks, MCPs, subagents, or other agent-related components

The agent must ensure that:

- No new instruction contradicts an existing instruction.
- No workflow step conflicts with an existing rule or skill.
- No skill defines behavior that violates an existing rule.
- No rule makes an existing workflow impossible to execute.
- No duplicated specification introduces ambiguity.
- No renamed or deleted file leaves broken references.
- Terminology remains consistent across the `.agents` folder.
- Priority, scope, and applicability of the affected specifications remain clear.

If the agent detects any contradiction, conflict, ambiguity, broken reference, or inconsistency, it must not silently resolve it.

Instead, it must:

1. Clearly notify the user that a consistency problem has been found.
2. Identify the affected files and specifications.
3. Explain the nature of the problem in concrete terms.
4. Describe the possible impact on agent behavior.
5. Ask the user what they want to do before applying any corrective change.

The agent may suggest possible resolutions, but it must not choose one automatically unless the user explicitly authorizes it.

If no inconsistencies are found, the agent may proceed with the requested change and briefly state that the `.agents` specifications remain consistent.