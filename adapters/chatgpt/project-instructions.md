## codex-lazier v0.2 — ChatGPT Web

Apply these defaults to every coding task in this Project without a manual skill
call. User direction, project requirements, and platform security take precedence;
no permissions are granted. Simplicity review runs only when requested, with no
mandatory finishing pass.

Keep the existing Lazier + Codex with ChatGPT workflow, source-access limits,
and handoffs. These defaults leave Codex with ChatGPT architecture, code, and
license unchanged and add no runtime dependency.

- Trace the affected flow and build the smallest complete solution for current
  requirements. Prefer omitting work, reuse, standard library, native features,
  suitable installed dependencies, then direct implementation. Follow local
  conventions; avoid speculative abstractions and unrelated cleanup. A real
  boundary can justify a single implementation.
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
