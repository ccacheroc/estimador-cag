# Repository audit

Audit the whole repository for over-engineering rather than limiting the scan
to a diff. Rank the largest defensible reductions first.

Look for dependencies that duplicate standard or platform capabilities,
single-implementation interfaces, factories with one product, wrappers that
only delegate, dead flags and configuration, speculative flexibility, and
hand-rolled standard-library behavior.

Use these tags:

- `delete:` remove dead code, unused flexibility, or speculative features.
- `stdlib:` replace custom code with a named standard-library feature.
- `native:` replace code or a dependency with a named platform feature.
- `yagni:` remove an abstraction without a current second use.
- `shrink:` express the same logic in fewer lines and show the shorter form.

Return one line per finding:

`<tag> <what to cut>. <replacement>. [path]`

End with `net: -<N> lines, -<M> deps possible.` If nothing should be cut,
return `Lean already. Ship.`

This is a read-only, one-shot complexity audit. Do not apply fixes. Correctness,
security, and performance are out of scope and require separate review passes.
