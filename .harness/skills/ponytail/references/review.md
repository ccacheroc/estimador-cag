# Diff review

Review the current diff exclusively for unnecessary complexity. The desired
result is a concise, evidence-based list of what can be removed or replaced.

## Finding format

Use one line per finding:

`L<line>: <tag> <what>. <replacement>.`

For multiple files, use:

`<file>:L<line>: <tag> <what>. <replacement>.`

Tags:

- `delete:` dead code, unused flexibility, or speculative functionality;
  replacement is nothing.
- `stdlib:` custom code already provided by the standard library; name the
  standard function or feature.
- `native:` dependency or code duplicating a platform feature; name it.
- `yagni:` abstraction with one implementation, unused configuration, or a
  layer with one caller.
- `shrink:` equivalent logic that can be expressed more directly; show the
  shorter form.

Rank findings by practical reduction. End with
`net: -<N> lines possible.` If there are no findings, return
`Lean already. Ship.`

## Boundaries

Cover only over-engineering and complexity. Correctness, security, and
performance require a separate review. Never flag a small smoke test or
`assert`-based self-check merely for existing. Do not apply fixes.
