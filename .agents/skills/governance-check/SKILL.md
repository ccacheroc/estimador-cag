---
name: governance-check
description: Validates whether content belongs in a Rule, Skill, Hook, Template, or Agent, and executes the governance verification procedure and checklists before merging agentic changes. Use when reviewing, creating, or modifying agentic configuration files, AGENTS.md, or .agents/ artifacts.
---

# Governance Check

**Purpose:** Validate whether content belongs in a **Rule**, **Skill**, **Hook**, **Template**, or **Agent**, verify compliance with quality gates, and run the governance verification procedure and checklists before merging changes to the agentic system.

---

## When to use / When NOT to use

### Use this skill when:
- Reviewing, creating, or modifying files in `AGENTS.md`, `/.agents/`, or tool bridges (`.claude/`, `.github/`, `.cursor/`, `.gemini/`).
- Deciding whether a new requirement or convention should be a Rule, a Skill, a Hook, a Template, or an Agent.
- Verifying artifact scopes (global vs workspace), activation modes, and quality standards.
- Preparing the completion report for agentic configuration changes.

### Do NOT use this skill when:
- Performing ordinary code changes, bug fixes, or feature development that do not modify agentic architecture or `.agents/` configurations.
- Creating single non-agentic files (scripts, tests, routers, models).

---

## Guía de Decisión y Ubicación de Artefactos (Reference)

Para clasificar cualquier nuevo requerimiento, determinar el tipo exacto de artefacto a crear (**Rule**, **Workflow**, **Skill**, **Hook**, **Template**, **Agent Profile**, o **Canonical Documentation**), resolver la ruta canónica en `.agents/` o `docs/`, la convención de nombres y el modo de activación:

👉 **Consultar y seguir:** [resources/decision-guide.md](resources/decision-guide.md)

Este documento centraliza el árbol de decisión determinista, la matriz de rutas canónicas, las reglas de alcance (global vs workspace) y los ejemplos de mapeo directo ("petición X $\rightarrow$ artefacto y ruta"). No dupliques esta lógica; trátala como fuente única de verdad.

---

## Governance Verification Procedure

When running a governance check on proposed or requested changes:

### Step 1 — Collect Artifacts & Requirements
1. Identify all files added, modified, or deleted in `AGENTS.md`, `/.agents/`, or tool adapters, or the requirement **X** requested by the user.
2. Identify dependencies and references across the repository.
3. *Stop condition:* If artifact contents or user intent are missing or ambiguous, request clarification before proceeding.

### Step 2 — Classify Each Artifact & Resolve Location
For every artifact under review or creation:
- Determine or verify the exact artifact type (**Rule / Workflow / Skill / Hook / Template / Agent Profile / Canonical Doc**) using the decision tree in [resources/decision-guide.md](resources/decision-guide.md).
- Resolve the exact target path and file name adhering strictly to the Canonical Location Matrix in [resources/decision-guide.md](resources/decision-guide.md).
- Justify the choice referencing the criteria and examples in that guide.

### Step 3 — Validate Scope & Activation
For each artifact:
- Confirm whether it belongs to `global` (`~/.agents/`) or `workspace` (`.agents/`).
- If a **Rule**: ensure the least-powerful activation mode is configured (`manual`, `always_on`, `glob`, `model_decision`).
- Verify registration in `.agents/manifest.yaml` under `inventory:`.

### Step 4 — Validate Invocation & Structure
- **Rules:** Verify normative MUST / MUST NOT language and clean condition statements.
- **Workflows:** Verify sequential, ordered, verifiable steps with clear outputs.
- **Skills:** Verify frontmatter (`name`, `description`), triggering criteria, and modular resources.
- **Hooks / Templates / Agents:** Verify adherence to the specific format in [resources/decision-guide.md](resources/decision-guide.md).

### Step 5 — Run Checklists
Execute the relevant checklist from the section below. Record status as:
- ✅ **Pass**
- ⚠️ **Needs changes**
- ❌ **Fail**

### Step 6 — Validate Concision & Modularity
- Check for duplication across files; ensure references point to canonical sources.
- Verify clear MUST / MUST NOT normative wording for Rules.
- Verify no single file is overloaded ("mega-file").

### Step 7 — Verify Ambiguity Protocol
- Confirm the artifact provides explicit instructions to stop and ask questions when inputs are missing, rather than making unverified assumptions.

### Step 8 — Produce Governance Report
Generate the final report following the structure outlined in `Completion & Reporting`.

---

## Checklists

### A) Validation Checklist — RULE
- [ ] Expresses **constraints/norms** (not step-by-step processes).
- [ ] Uses normative language: **MUST / MUST NOT / SHOULD**.
- [ ] Is **unambiguous**: conditions are well-defined or require asking questions.
- [ ] Is **testable and verifiable** in the repository or PR.
- [ ] Assigned to the **correct scope** (global vs workspace).
- [ ] Uses the **least-powerful activation mode** required.
- [ ] Granular and focused (not a mega-rule).
- [ ] Avoids duplication by referencing canonical docs (`@mentions`).
- [ ] Contains no secrets, volatile tokens, or temporary URLs.

### B) Validation Checklist — WORKFLOW
- [ ] Contains title, description, and clearly **numbered or sequential steps**.
- [ ] Each step represents a **concrete verifiable action** with an expected outcome.
- [ ] Defines **checkpoints**, stop conditions, and resume/rollback criteria.
- [ ] Explicitly handles **missing information** (specifies what to ask before continuing).
- [ ] Avoids embedding permanent norms (delegates to Rules).
- [ ] Reuses existing skills/workflows without copy-pasting.
- [ ] Contains basic verification commands/steps.
- [ ] Safe: requires explicit gate/confirmation before any destructive action.

### C) Validation Checklist — SKILL
- [ ] Folder contains `SKILL.md` (mandatory).
- [ ] YAML Frontmatter is present and valid:
  - [ ] `name` matches the directory name.
  - [ ] `description` is specific, third-person, with reliable activation keywords.
- [ ] Body contains:
  - [ ] **When to use** / **When NOT to use**.
  - [ ] Concrete operational procedure.
  - [ ] Constraints, restrictions, and security limits.
  - [ ] Verification criteria.
- [ ] Any script in `scripts/` is documented with usage, inputs, outputs, and `--help`.
- [ ] Focused on a single distinct capability.
- [ ] Correct scope (global vs workspace).
- [ ] Free of secrets or credentials.

### D) Validation Checklist — HOOK
- [ ] Defines a clear, concrete lifecycle event trigger (pre-commit, post-task, etc.).
- [ ] Conditions for execution and termination are explicit.
- [ ] Validations are deterministic, fast, and idempotent.
- [ ] Does not embed heavy domain logic (delegates to a Skill if needed).
- [ ] Safe failure behavior: blocks or warns cleanly on violation.

### E) Validation Checklist — TEMPLATE
- [ ] Pure output structure with explicit `<placeholder>` fields.
- [ ] No executable logic or hidden instructions inside the template.
- [ ] Clearly documented purpose and usage guidelines.
- [ ] Granular and focused on a single type of document.

### F) Validation Checklist — AGENT PROFILE
- [ ] Defines a clear persona, role, and operational domain.
- [ ] Explicitly lists allowed tools, restricted tools, and boundary constraints.
- [ ] Thin: points to Rules, Skills, and Canonical Docs rather than duplicating long text.
- [ ] Defined model or reasoning preferences if applicable.

### G) General Quality Rules (All Artifacts)
1. **Zero operational ambiguity:** When interpretation diverges, require asking targeted questions.
2. **Dense and concise:** High information density, no filler.
3. **Verifiable:** Every assertion or requirement can be checked against code, tests, or logs.
4. **Single canonical source:** Never duplicate instructions across tool bridges or separate folders.

---

## Completion & Reporting

When completing a governance check, present the results using this format:

```markdown
### Governance Check Report

#### Summary
- Artifacts checked: <list of files>
- Overall status: ✅ Pass | ⚠️ Needs changes | ❌ Fail

#### Findings
- **<Artifact Path>**:
  - Type: Rule | Workflow | Skill | Hook | Template | Agent
  - Scope: Global | Workspace
  - Activation / Invocation: <mode or trigger>
  - Checklist result: ✅ | ⚠️ | ❌
  - Required changes:
    - <item>
  - Optional improvements:
    - <item>

#### Next Actions
- [If ✅]: Ready to merge / proceed.
- [If ⚠️ or ❌]: Prioritized patch plan.
```
