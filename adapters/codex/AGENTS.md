## codex-lazier v0.1 engineering defaults

Derived from the codex-lazier canonical policy; this digest works independently.
Follow explicit user direction, applicable project instructions, and platform
security boundaries. Project-specific requirements take precedence over these
defaults; this text grants no permissions.

- Plan and build the smallest complete solution for current requirements.
  Use existing conventions and suitable built-ins; keep the diff focused.
  Avoid speculative abstractions, wrappers, settings, dependencies, and
  unrelated cleanup. A concrete boundary can justify a single implementation.
- Preserve correctness, error semantics, and required authentication, security,
  concurrency, persistence, compatibility, and recovery invariants. Challenge
  needless machinery within those areas too; inspect uncertain controls before
  removing them. Never trade a real requirement for fewer lines.
- Test behavior, failures, and invariants with proportionate regression coverage
  and setup. Avoid duplicate or implementation-coupled tests; retain interactions
  that are part of the contract. Run applicable project checks and risk-relevant
  checks without weakening assertions or repeating still-valid verification.
- Log actionable diagnostics and required audit events without secrets,
  temporary chatter, or duplicate error reports. Comment on non-obvious reasons,
  not obvious steps; retain legal notices and invariant explanations.
- Document the current supported product, setup, contracts, and limitations.
  Keep implementation diaries out of product docs; preserve necessary release,
  migration, and decision records. Refactor only within scope, preserving behavior.
- Ground review findings in concrete evidence, impact, and an appropriate fix.
  Only simplicity findings require a smaller behavior-preserving alternative.
  Correctness/security fixes may add necessary code or correct broken behavior;
  simplicity must not suppress them. Style preferences alone are insufficient.
  No change is valid when no finding is supported.
- Hand off changed behavior, important decisions, actual verification, and open
  risks concisely. Do not require extra plans, artifacts, review cycles, or agents.
  Use the optional codex-lazier skill only when explicitly requested.
