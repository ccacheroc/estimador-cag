# Help

Return a compact explanation of the available workflows. Do not change mode,
edit files, or persist state.

## Levels

| Level | Use |
|---|---|
| `lite` | Implement the request and name a lazier alternative. |
| `full` | Apply the complete YAGNI → reuse → stdlib → native → minimum ladder. This is the default. |
| `ultra` | Prefer deletion and challenge speculative requirements while preserving explicit and safety-critical behavior. |

## Workflows

| Workflow | Purpose |
|---|---|
| `ponytail` | Produce the smallest safe implementation. |
| `ponytail review` | Review the current diff for removable complexity. |
| `ponytail audit` | Audit the entire repository for removable complexity. |
| `ponytail debt` | Collect `ponytail:` shortcuts into a ledger. |
| `ponytail gain` | Show the published benchmark scoreboard. |
| `ponytail help` | Show this reference. |

The exact invocation syntax depends on the host. Codex can explicitly invoke
the skill as `$ponytail`; natural-language requests also work. To deactivate
the behavior for the current task or conversation, say `stop ponytail` or
`normal mode`.

Project documentation and upstream examples:
https://github.com/DietrichGebert/ponytail
