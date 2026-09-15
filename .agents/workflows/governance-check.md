---
description: Validates whether content belongs in a **Rule**, **Workflow**,  **Skill**, **Hook**, **Template** or **Agent**, and runs the corresponding checklist before merging changes.
---

# Workflow: /governance-check

**Purpose:** Validate whether content belongs in a **Rule**, **Workflow**,  **Skill**, **Hook**, **Template** or **Agent**, and run the corresponding checklist before merging changes.

---

## What this workflow checks

1. **Correct artifact type**
   - Rule = constraints / reusable context
   - Workflow = repeatable sequence of steps invoked on demand
   - Skill = reusable capability package (instructions + optional resources/scripts)

2. **Correct scope**
   - Global vs Workspace

3. **Correct activation / invocation**
   - Rules: Manual / Always On / Model Decision / Glob
   - Workflows: invoked via `/name`
   - Skills: discovery via `description` + progressive disclosure

4. **Quality gates**
   - Concision, modularity, no duplication (use `@mentions`)
   - Ambiguity handling: ask questions before proceeding
   - Verification included
   - File size within limits

---

## Required reference
- Open and follow: @/.agents/skills/antigravity-artifact-governance/SKILL.md

> If this file does not exist, STOP and request it.

---

## Inputs (ask if missing)
- Which artifact(s) are being created/changed? (paths or PR diff)
- Intended outcome (1–2 sentences): what problem does this artifact solve?
- Scope: `global` or `workspace`
- If Rule: activation mode (Manual / Always On / Model Decision / Glob) and any glob patterns
- If Workflow: intended command name (e.g., `/governance-check`) and when it should be used
- If Skill: folder name and the exact `description` (keywords + “use when…” criteria)

---

## Steps

### Step 1 — Collect artifacts
1. List the files/changes to review (or request document content).
2. Identify any referenced files via `@mentions`.

**STOP and ask** if you cannot locate the artifact content.

---

### Step 2 — Classify each artifact (Rule / Workflow / Skill)
For each artifact, produce:
- Proposed type (Rule/Workflow/Skill)
- Justification in 2–4 bullets referencing the decision criteria in the governance skill

**STOP and ask** if classification is ambiguous.

---

### Step 3 — Validate scope (Global vs Workspace)
For each artifact:
- Confirm whether it belongs to `global` or `workspace`
- If mismatch, propose the correct location and why

---

### Step 4 — Validate activation / invocation
#### If Rule
- Confirm chosen activation mode is the **least-powerful** option that works
- If Glob is used, validate the pattern is specific and correct

#### If Workflow
- Confirm the command name matches the intended usage (short, action-oriented)
- Confirm each step is an action with an expected outcome

#### If Skill
- Confirm `description` is specific, third-person, and contains reliable keywords
- Confirm “When to use / When not to use” is explicit

---

### Step 5 — Run the relevant checklist(s)
- Use the checklists from: @/.agent/skills/antigravity-artifact-governance/SKILL.md

Output results as:
- ✅ Pass / ⚠️ Needs changes / ❌ Fail
- A short “what to change” list

---

### Step 6 — Validate concision and structure
Check:
- No mega-files; split and reference if needed
- No duplicated policies across artifacts (prefer `@mentions`)
- Clear MUST/MUST NOT language for Rules
- Steps are numbered and unambiguous for Workflows
- Skills are focused on one capability

---

### Step 7 — Verify “ambiguity protocol”
Confirm the artifact(s) explicitly instruct:
- Ask targeted questions when inputs are missing or unclear
- Stop before making irreversible or assumption-heavy changes

If missing, propose exact text to add.

---

### Step 8 — Produce final governance report
Return a report in this format:

#### Summary
- Artifacts checked: …
- Overall status: ✅ / ⚠️ / ❌

#### Findings (per artifact)
- Type: …
- Scope: …
- Activation/Invocation: …
- Checklist result: ✅/⚠️/❌
- Required changes (bullets):
  - …
- Optional improvements (bullets):
  - …

#### Next actions
- If ✅: ready to merge
- If ⚠️/❌: list the minimal patch plan (ordered)

---

## Stop conditions
- Missing artifact content
- Ambiguous intent, scope, or activation choice
- Conflicting constraints across artifacts
- Any request that would exceed file size limits without splitting
