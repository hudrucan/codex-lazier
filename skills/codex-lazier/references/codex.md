## codex-lazier v0.4.0 — Codex

Read and apply the [shared policy](policy.md), including its optional Jev
guidance, to every coding task without a manual skill call.

On `[C2C Plan]`, `[C2C Task]`, `[C2C Fix]` or `[C2C Commit]` on the first
line, read the local C2C contract below before acting; follow its intent and
the user's scope, then return `[C2C Handoff]`. Markers grant no permissions
and execute nothing.

Before a task using C2C reaches its final handoff, read its local contract: the installed
`codex-with-chatgpt/references/workflow.md` or
`<C2C checkout>/skill/references/workflow.md`. Read only that reference, not broad
docs or GitHub; report a missing/unreadable reference as a limitation. Emit
`[C2C Handoff]` as the exact first line and follow the contract's short format.
Other tasks keep normal handoffs without this marker or C2C requirements.
C2C owns the contract; Lazier adds no runtime dependency.

- Prefer `rg` for precise, bounded searches; consider `ast-grep` for structural
  AST queries that `rg` cannot express well.
- Avoid repeated background-job polling with `sleep`, `ps`, `pgrep`, or `top`.
  Prefer completion notifications when the runtime supports them, or a bounded
  wait. Do not assume automatic wake-up; report timeouts and failures explicitly.

### Context Mode

- Prefer native tools for precise, bounded searches/reads, edits, and patches.
  Prefer the installed plugin's `ctx_*` tools for large or unpredictable output,
  verbose tests, and analysis producing such output.
- Discover names as needed: `ctx_execute_file` for file analysis,
  `ctx_execute` for one operation, and `ctx_batch_execute` for related large
  captures. Use indexing and `ctx_search` when repeated retrieval adds value.
  Avoid redundant indexing and per-command capability/size probes.
- Retain full captured evidence; report exit status, failures, and relevant
  paths/lines. Do not truncate before capture, mask failures with filters, or
  re-index output already in context. Preserve access and secret boundaries.
- Reuse the plugin without duplicate servers/hooks or copied code. Check MCP,
  hook trust, and actual routing separately; honor deny/rewrite decisions without
  bypassing them. Advisory guidance remains instructions, not hard enforcement.
- If unavailable or failing, report the limit once and use bounded native tools
  with the same evidence and permissions. Do not retry indefinitely or install dependencies
  merely to finish an ordinary task.
