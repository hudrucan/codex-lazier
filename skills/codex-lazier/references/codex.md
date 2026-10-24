## codex-lazier v0.5.0 — Codex

Read and apply the [shared policy](policy.md), including its optional Jev
guidance, to every coding task without a manual skill call.

For first-line `[C2C Plan]`, `[C2C Task]`, `[C2C Fix]` or `[C2C Commit]`,
load C2C's local contract before acting: the installed
`codex-with-chatgpt/references/workflow.md` or
`<C2C checkout>/skill/references/workflow.md`. Read its common contract and only
the active host/mode reference it selects,
without broad docs/GitHub lookup; disclose if unreadable. Reuse guidance already
read and still valid in this session, including the policy and this host reference;
reload only changed or missing guidance. Follow C2C intent/scope and ensure the
applicable contract was read before final handoff, using its short format and
exact first-line `[C2C Handoff]`. Other tasks keep normal handoffs.
Markers execute nothing and grant no permission. C2C owns the contract;
Lazier adds no runtime dependency.

- Prefer `rg` for precise, bounded searches; consider `ast-grep` for structural
  AST queries that `rg` cannot express well.
- Avoid repeated background-job polling with `sleep`, `ps`, `pgrep`, or `top`.
  Prefer completion notifications when the runtime supports them, or a bounded
  wait. Do not assume automatic wake-up; report timeouts and failures explicitly.

### Context Mode

- Use native tools for precise bounded searches/reads and edits; prefer installed
  `ctx_*` tools for large/unpredictable output and verbose tests.
- Discover as needed: `ctx_execute_file` analyzes files, `ctx_execute` handles one
  operation, `ctx_batch_execute` captures related output. Index/search only when
  repeated retrieval helps; avoid redundant indexing and capability/size probes.
- Capture full evidence; report exit status, failures and paths/lines. Never
  truncate before capture, filter away failures or re-index existing context.
  Preserve access and secret boundaries.
- Reuse the plugin without duplicate servers/hooks or copied code. Verify MCP,
  hook trust and actual routing separately; honor deny/rewrite decisions.
  Advisory instructions are not hard enforcement.
- If unavailable/failing, disclose once and use bounded native tools under the
  same evidence/permission rules; no endless retries or dependency installation
  merely to complete ordinary work.
