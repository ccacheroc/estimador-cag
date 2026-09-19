---
name: ponytail
description: >-
  Apply the smallest safe coding solution and route Ponytail workflows for
  minimal implementation, over-engineering review, whole-repository audit,
  deferred-shortcut debt, benchmark impact, or command help. Use for coding
  tasks that ask for Ponytail, YAGNI, less boilerplate, fewer dependencies, a
  simpler solution, or one of the Ponytail review, audit, debt, gain, or help
  workflows. Do not use for unrelated non-coding requests.
license: MIT
---

# Ponytail

Choose the workflow from the user's actual request and read only the linked
reference needed for that workflow. Treat the reference as procedure, while
preserving the user's explicit scope, requested behavior, and authorization
boundaries.

## Workflow routing

- For writing, changing, fixing, refactoring, or designing code with the
  simplest safe solution, read [minimal implementation](references/minimal-implementation.md).
  Use `full` unless the user requests `lite` or `ultra`.
- For reviewing the current diff only for unnecessary complexity, read
  [diff review](references/review.md). Report findings; do not apply fixes.
- For scanning the whole repository for removable complexity, read
  [repository audit](references/audit.md). Report findings; do not apply fixes.
- For collecting `ponytail:` comments into a debt ledger, read
  [debt ledger](references/debt.md). Do not create a persistent ledger unless
  the user asks for one.
- For the published benchmark scoreboard, read
  [benchmark gain](references/gain.md). Never present benchmark figures as
  measurements of the current repository.
- For an explanation of levels, workflows, commands, or deactivation, read
  [help](references/help.md).

Natural-language requests are equivalent to command-like names. For example,
"audit this repository for over-engineering" selects the audit workflow even
without `/ponytail-audit`.

If a request combines implementation with a specialized report, use the
minimal-implementation workflow for the change and the relevant reporting
workflow afterward. Review and audit cover complexity only; they never replace
a separate correctness, security, accessibility, or performance review.
