# Antigravity — Decision & Quality Guide: Rules vs Workflows vs Skills

## Objective
This document defines **when** content should go into a **Rule** (and its scope), a **Workflow**, or a **Skill** in Antigravity, and establishes **quality requirements** + **checklists** to validate each artifact.

---

## Quick decision (30 seconds)

### Use a **Rule** when…
- It’s a **permanent constraint/criterion** (“MUST / MUST NOT”) that should influence *any* relevant generation or modification.
- It’s **reusable context** at prompt level: style, architecture, security, conventions, limits.
- It’s not a sequence; it’s a **norm**.

**Typical examples**
- “Don’t work directly on `main`; create feature/fix branches.”
- “Frontend: use semantic tokens, avoid hex values.”
- “Backend: use repositories; direct DB access from controllers is forbidden.”

### Use a **Workflow** when…
- It’s a **repeatable process** with **steps** (“first… then… finally…”) that you want to execute **on demand**.
- It should guide the **trajectory** of work (plan → actions → validation → close).
- It’s useful as a command-invokable “macro”.

**Typical examples**
- “/open-pr” (sync with main → green CI → push → open PR).
- “/respond-pr-comments” (read comments → group → apply changes → rerun tests).

### Use a **Skill** when…
- You want to extend capabilities with **knowledge + conventions + resources/scripts** in an **on-demand** way (not always loaded).
- The task requires **complex procedures**, templates, examples, helper scripts, or "know-how" that’s best encapsulated.
- You want the agent to automatically select the skill based on user intent (via its `description`).

**Typical examples**
- “Generate unit tests following your conventions (and run them).”
- “Scaffold endpoints + validations + contracts.”
- “Review PR with checklist + lint/format/test scripts.”

---

## 1) RULES

### What they are
Persistent constraints and guidelines (Markdown) that condition the agent’s behavior.

### Scope
- **Global Rule**: applies to all your workspaces.
- **Workspace Rule**: applies only to the current repo/workspace.

### When to choose Global vs Workspace
- **Global** if the rule reflects *your general way of working* (e.g., commit style, communication preferences, personal security policies).
- **Workspace** if it’s *project-specific* (tech stack, architecture, naming, routing, internal conventions).

### Activation modes (use the minimum needed)
- **Manual**: activated only when explicitly mentioned.
- **Always On**: always active (use only for truly universal rules).
- **Model Decision**: provide a description and the model decides if it applies (useful when context-dependent).
- **Glob**: applied via file patterns (useful for tech/layer-specific rules: `src/**/*.ts`, `backend/**`, etc.).

### What should NOT be in a Rule (anti-patterns)
- Long “step-by-step” processes (use Workflow instead).
- Procedures with many cases and resources (use Skill instead).
- Redundant text or huge templates (use `@mentions` to reference other files).

### Quality characteristics for Rules
- **Concise and testable**: each bullet should be verifiable.
- **Normative**: use clear formulations (“MUST”, “MUST NOT”, “SHOULD”).
- **Unambiguous**: if context-sensitive, define condition or move to Workflow/Skill.
- **Modular**: better to split into small rules than a giant “mega-rule”.
- **Referential**: use `@...` to point to source docs when needed (avoid duplication).

---

## 2) WORKFLOWS

### What they are
Processes (Markdown) with a **sequence of steps**, invokable via `/workflow-name`. Can call other workflows.

### Scope
- **Global Workflow**: reusable in all your workspaces.
- **Workspace Workflow**: tied to a repo/project.

### When to use Workflow (and not Rule)
- When the value lies in the **execution order** (checkpoints, validations, gates).
- When you want a “one-liner” command to launch a repeatable protocol.

### What should NOT be in a Workflow (anti-patterns)
- Permanent restrictions (use Rule instead).
- Heavy “domain knowledge” (use Skill instead).
- Steps that depend on unavailable data without specifying how to get it.

### Quality characteristics for Workflows
- **Step = verifiable action** (ideally with expected output/artifact).
- **Explicit checkpoints**: when to review, when to stop on error.
- **Mental idempotence**: re-running shouldn’t break things (or should explain how to resume).
- **Ambiguity handling**: *if info is missing for a step*, the workflow should say “ask X before continuing”.

---

## 3) SKILLS

### What they are
Packages (folders) with `SKILL.md` + optional resources (scripts, examples, templates). Loaded **only when relevant** based on their `description`.

### Scope
- **Global Skill**: available in all projects.
- **Workspace Skill**: specific to a repository.

### When to use Skill (and not Workflow)
- When the content is **reusable knowledge/procedure** that applies *across multiple tasks* with variations.
- When you have **assets** worth grouping: `scripts/`, `examples/`, `resources/`.
- When you want an “ability” the agent can choose based on user intent.

### Recommended minimal structure
- `SKILL.md` with:
  - **YAML Frontmatter** (`name`, `description`)
  - **Markdown body** with: goal, when to use, procedure, examples, constraints, verification
- Optional folders: `scripts/`, `examples/`, `resources/` 

> **Pro Tip:** To ensure compliance with this structure and quality gates, **use the `antigravity-skill-creator` skill** to scaffold new skills. It automatically generates the correct directory, `SKILL.md` template, and configuration. 

### Quality characteristics for Skills
- **Focused**: one skill = “does one thing well”.
- **Reliable activation**: `description` must have clear keywords and criteria (avoid vagueness).
- **Operational instructions**: concrete steps + expected outputs.
- **Scripts as black boxes**: explain how to run them and suggest `--help` if needed.
- **Decision tree** when multiple strategies exist.
- **Security**: explicit restrictions (e.g., no destructive actions, no exposed secrets).

---

## General quality rules (apply to all)

1. **Zero operational ambiguity**
   - If something can be interpreted in two ways, **require a question** (what data is missing, what preference to use).
2. **Concise but dense**
   - Less text, more precision. Avoid filler.
3. **Verifiable**
   - Every requirement should be checkable (via tests, CI, diff review, logs).
4. **No duplication**
   - If it exists elsewhere, reference (or delegate), don’t copy.
5. **Separation of responsibilities**
   - Rule = norm; Workflow = sequence; Skill = capability + resources.

---

# CHECKLISTS

## A) Validation checklist — RULE
- [ ] The rule expresses **constraints** (not step-by-step processes).
- [ ] Each point uses normative verbs: **MUST / MUST NOT / SHOULD**.
- [ ] It is **unambiguous**: includes conditions (“if X then Y”) or requires questions.
- [ ] It is **testable** (can be verified in the repo/PR).
- [ ] It’s in the **correct scope** (global vs workspace).
- [ ] Has **proper granularity** (not a mega-rule).
- [ ] Doesn’t repeat long texts: uses `@mentions` when appropriate.
- [ ] Doesn’t include volatile data (tokens, credentials, temporary URLs).
- [ ] Meets size limits (if applicable) and is bullet-readable.

## B) Validation checklist — WORKFLOW
- [ ] Has **title, description**, and a list of **numbered or clearly ordered steps**.
- [ ] Each step is a **concrete action** with an expected result.
- [ ] Defines **checkpoints** (review, stop conditions, rollback/resume).
- [ ] Handles **missing information**: states what to ask before continuing.
- [ ] Avoids encoding “permanent norms” (those go in Rules).
- [ ] Reuses other workflows/skills when appropriate (no duplication).
- [ ] Includes basic verification (tests, CI, smoke checks, etc.).
- [ ] Is safe: no destructive actions without an explicit gate.

## C) Validation checklist — SKILL
- [ ] Folder exists with `SKILL.md` (mandatory).
- [ ] Correct frontmatter:
  - [ ] `description` is **specific** and includes activation keywords.
  - [ ] `name` (if used) is unique, consistent, and **matches the folder name**.
- [ ] Body includes:
  - [ ] **When to use** / when NOT to use.
  - [ ] **Step-by-step procedure**.
  - [ ] **Input/output examples** (at least one).
  - [ ] **Constraints** (“do not”) and security limits.
  - [ ] **Verification** (how to confirm it worked).
- [ ] If there’s a `scripts/` folder:
  - [ ] Explains how to run them, suggests `--help`.
  - [ ] Clearly defines required inputs and expected outputs.
- [ ] The skill is not “do-everything”: **focused on a specific goal**.
- [ ] It’s in the **correct scope** (global vs workspace).
- [ ] No secrets or sensitive data are exposed.

---

## Final heuristic (if unsure)
- If you want it **always on** → Rule.
- If you want it **sometimes**, as a repeatable process → Workflow.
- If you want it **sometimes**, and it’s a “specialized capability” with resources → Skill.
