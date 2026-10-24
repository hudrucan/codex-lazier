# codex-lazier engineering policy v0.3

Choose the smallest implementation that meets current requirements. KISS and
YAGNI guide decisions, not line counts. User direction, project requirements,
and platform security take precedence; this policy grants no permissions.

- **Activation.** Apply throughout every coding task without manual invocation.
  Simplicity review runs only when requested; no finishing review pass is required.
- **Planning.** Identify behavior and constraints, inspect project guidance and
  responsible code, and choose the smallest viable architecture. Clarify facts
  affecting correctness; do not invent future requirements. Scale planning to the task.
- **Implementation.** Keep changes complete, focused, and consistent with local
  patterns. After tracing the flow, prefer omitting work, reuse, standard library,
  native features, suitable installed dependencies, then direct implementation.
  Add abstractions, wrappers, settings, or dependencies only for a present benefit
  exceeding maintenance cost. One implementation can establish a real boundary;
  some duplication is clearer than coupling unrelated behavior. Avoid unrelated
  cleanup and needless wrappers.
- **Correctness.** Preserve required behavior, public contracts, error semantics,
  and necessary authentication, authorization, validation, concurrency, persistence,
  compatibility, recovery, accessibility, and measured performance logic. Explain
  non-obvious requirements. Neither verbosity nor a security label determines
  necessity; inspect uncertain controls before removal. Validate at actual trust
  boundaries; repeat only for a distinct boundary or reachable failure. Never
  mask failure as plausible success.
- **Testing.** Protect observable behavior, failure cases, and invariants with
  proportionate regression coverage, existing tools, and focused fixtures. Avoid
  duplicate assertions and incidental private/call-order checks; retain contractual
  interactions. Do not weaken assertions for a refactor. Run applicable and
  risk-relevant checks; reuse valid evidence and rerun when changes invalidate it.
- **Logging and comments.** Keep actionable diagnostics and required audit events
  where context is added or failure handled, without duplicate reports, temporary
  chatter, secrets, or personal data. Prefer expressive code; explain hidden
  constraints, reasoning, or external requirements. Remove stale/narrating comments;
  retain legal notices and invariant explanations.
- **Documentation.** Describe current setup, contracts, support, and limitations;
  update material made false by changes. Keep development diaries out of product
  docs; preserve useful release/migration guidance and required decision records.
- **Refactoring.** Stay within scope and preserve behavior. Check callers and
  supported external uses before removing apparently unused code. Include only
  prerequisite cleanup needed for the change.
- **Review.** Ground findings in location, evidence, impact, and a fix. Simplicity
  findings require a smaller alternative preserving required behavior; identify
  the mechanism's responsibility and cost. Verify claims of unused, redundant,
  or speculative code. Correctness/security fixes may add code or correct behavior.
  Distinguish unknowns from defects; style alone is not a finding. Leaving
  justified code unchanged is successful.
- **Handoff.** Briefly state changed behavior, decisions, actual verification,
  and open risks. Label assumptions and unrun checks. Do not require unnecessary
  agents, plans, reports, checklists, artifacts, or review cycles; use them only
  when warranted within existing permissions.

### Optional Jev advisor

- Lazier remains the primary engineering policy. Default to skipping the existing
  TypeSafe Jev MCP. Consider `evaluate` only when explicitly requested or material
  uncertainty remains between viable alternatives, after checking hard constraints
  and available evidence.
- Use `noul` for yes/no probabilities, `choice` for alternatives, and `score` for
  ordered rubric judgments; prefer one batched call with bounded, deliberately
  selected nonsecret state. Never automatically send private source, secrets, or
  credentials.
- Treat probabilities as advice, never correctness proofs or authorization. If the
  MCP is unavailable, fails, or abstains, continue the normal workflow. No Jev call
  is required for routine coding, C2C handoff audits, fixes, commits, or simplicity
  reviews. Add no extra review cycles or mandatory evaluation gates; reuse the
  existing MCP without new dependencies, hooks, agents, or runtime coupling.
