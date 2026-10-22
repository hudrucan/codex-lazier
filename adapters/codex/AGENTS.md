## codex-lazier v0.2 — Codex

Apply these defaults to every coding task without a manual skill call. User
direction, project requirements, and platform security take precedence; no
permissions are granted. Simplicity review runs only when requested, with no
mandatory finishing pass.

- Trace the affected flow and build the smallest complete solution for current
  requirements. Prefer omitting work, reuse, standard library, native features,
  suitable installed dependencies, then direct implementation. Follow local
  conventions; avoid speculative abstractions and unrelated cleanup. A real
  boundary can justify a single implementation.
- Prefer `rg` for ordinary searches; consider `ast-grep` for structural AST
  queries that `rg` cannot express well.
- Preserve correctness, error semantics, and required security, concurrency,
  persistence, compatibility, and recovery invariants. Inspect uncertain controls
  before removing them; neither verbosity nor a security label decides necessity.
- Test behavior, failures, and invariants with existing tools and proportionate
  fixtures. Avoid duplicate or implementation-coupled assertions; retain required
  interactions. Run applicable checks without weakening assertions or repeating
  still-valid verification.
- Keep actionable diagnostics and required audit events; protect secrets and
  avoid duplicate reports or debug chatter. Explain non-obvious constraints in
  comments; retain legal notices and invariant explanations.
- Document current setup, contracts, and limitations rather than development
  diaries; preserve useful release, migration, and required decision records.
  Keep refactoring within scope and preserve behavior.
- Ground findings in evidence, location, impact, and a fix. Simplicity findings
  require a smaller behavior-preserving alternative; correctness/security fixes
  may add code or correct broken behavior. Style alone is not a finding.
  Leave justified code unchanged.
- Hand off changed behavior, decisions, actual checks, and open risks concisely.
  Add no unnecessary plans, artifacts, review cycles, or agents.

### Context Mode

- Prefer the installed plugin's `ctx_*` tools for analysis reads, searches, logs,
  diffs, verbose tests, and suitable tool output. Discover names as needed:
  `ctx_execute_file` for files, `ctx_execute` for one operation,
  `ctx_batch_execute` for related captures, `ctx_search` for indexed evidence.
- Keep known-small observations, edits/mutations, and exact patch-source reads
  direct when useful. Avoid per-command capability/size probes and extra indexing.
- Retain full captured evidence; report exit status, failures, and relevant
  paths/lines. Do not truncate before capture, mask failures with filters, or
  re-index output already in context. Preserve access and secret boundaries.
- Reuse the plugin without duplicate servers/hooks or copied code. Check MCP,
  hook trust, and actual routing separately; honor deny/rewrite decisions without
  bypassing them. Advisory guidance remains instructions, not hard enforcement.
- If unavailable or failing, report the limit once and use bounded native tools
  with the same evidence and permissions. Do not retry indefinitely or install dependencies
  merely to finish an ordinary task.
