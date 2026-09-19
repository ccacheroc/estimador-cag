---
trigger: model_decision
---

# Ponytail

When this rule is active for a coding task, the agent **MUST** prefer the
smallest safe solution after understanding the affected flow. It **MUST** reuse
existing code, standard library features, native platform capabilities, and
installed dependencies before adding code, abstractions, boilerplate, or
dependencies.

The agent **MUST NOT** trade explicit requirements, root-cause correctness,
security, accessibility, data integrity, trust-boundary validation, or the
smallest relevant runnable check for a shorter diff.

When the request matches the Ponytail skill's activation criteria, the agent
**MUST** load and follow `@.harness/skills/ponytail/SKILL.md`. That skill is the
canonical source for workflow routing, levels, commands, deactivation,
procedures, and reporting; these details **MUST NOT** be duplicated in this
rule.

If the smallest safe option depends on ambiguous scope or a material tradeoff,
the agent **MUST** ask a targeted question before changing the implementation.
