# Debt ledger

Collect every deliberate Ponytail shortcut marked by a `ponytail:` source-code
comment. Search the repository while excluding version-control metadata,
dependency directories, and generated build output. Recognize the comment
syntax used by the project's languages, such as `# ponytail:` or
`// ponytail:`.

Each marker should follow this convention:

`ponytail: <ceiling>, <upgrade path or trigger>`

Return one row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <limit>. upgrade: <trigger>.`

Tag a marker `no-trigger` when it provides no concrete upgrade path or trigger.
If the user asks for ownership information, derive it from version-control
history for that exact line.

End with `<N> markers, <M> with no trigger.` If none exist, return
`No ponytail: debt. Clean ledger.`

This workflow reads and reports only. Create or update a persistent ledger such
as `PONYTAIL-DEBT.md` only when the user explicitly requests it.
