# codex-lazier engineering policy v0.1

Choose the smallest implementation that fully meets the current requirement.
KISS and YAGNI guide decisions; line count is not a quality measure. These are
defaults subordinate to explicit user direction, applicable project instructions,
and platform security boundaries. They grant no additional permissions.

- **Planning.** Identify required behavior and relevant constraints. Read enough
  existing code and project guidance to find the responsible component. Prefer
  the smallest viable architecture. Clarify missing facts when they affect
  correctness; do not invent future requirements. Scale planning to the task.
- **Implementation.** Keep the diff focused and complete. Follow local patterns
  and reuse suitable existing capabilities. Add an abstraction, wrapper,
  interface, factory, setting, or dependency only for a concrete present need
  whose benefit exceeds its maintenance cost. A real boundary or invariant can
  justify an abstraction with one implementation. Some duplication is clearer
  than coupling unrelated behaviors. Avoid unrelated cleanup.
- **Correctness and complexity.** Preserve required behavior, public contracts,
  error semantics, and critical invariants. Keep necessary authentication,
  authorization, input validation, concurrency coordination, persistence,
  compatibility, recovery, accessibility, and measured performance logic.
  Explain the concrete requirement or failure it addresses when that is not
  obvious. Do not remove a control just because it is verbose, or retain
  needless machinery merely because it sits in a security module. When its
  purpose is uncertain, inspect relevant evidence before proposing removal.
  Validate at actual trust boundaries; repeat validation only for a distinct
  boundary or reachable failure. Never mask failure as plausible success.
- **Testing.** Protect observable behavior, meaningful failure cases, and
  invariants with proportionate regression coverage. Prefer existing test
  tools and focused fixtures. Avoid duplicate assertions of the same contract
  and tests tied to incidental call order or private structure. Keep interaction
  checks when the interaction itself is a required contract. Do not weaken
  assertions to accommodate a refactor. Run applicable project checks and
  checks justified by the change's risk; reuse still-relevant evidence and
  rerun verification when changes invalidate it.
- **Logging.** Keep diagnostics that support a concrete operational action or
  required audit trail, at the level that can add context or handle the failure.
  Avoid repeated error reports and temporary debug chatter. Protect secrets
  and personal data; required security audit events are not redundant noise.
- **Comments.** Prefer expressive code. Explain hidden constraints, non-obvious
  reasoning, or externally imposed behavior. Remove stale or narrating comments;
  preserve legal notices and useful explanations of invariants.
- **Documentation.** Describe the current supported product, setup, contracts,
  and limitations. Update material made false by the change. Keep development
  diaries and phase histories out of product docs; use existing release notes,
  migration guides, or required decision records for their intended purposes.
- **Refactoring.** Preserve behavior and constrain scope to the requested work.
  Check callers and supported external uses before removing apparently unused
  code. Include only prerequisite cleanup needed for the change to work safely.
- **Review.** Support findings with a location, concrete evidence, impact, and
  an appropriate fix. Only simplicity findings require a smaller
  behavior-preserving alternative: identify the mechanism's current responsibility,
  concrete cost, and required behavior the alternative preserves. Check evidence
  before calling code unused, redundant, or speculative. Correctness/security
  fixes may add necessary code or correct broken behavior; simplicity must not
  suppress them.
  Distinguish unknowns from defects. Personal style preferences alone are not
  findings. Leaving justified code unchanged is a successful outcome.
- **Handoff.** Briefly state changed behavior, important decisions, verification
  actually performed, and unresolved risks. Label unrun checks and assumptions.
  Do not require unnecessary agents, plans, reports, checklists, artifacts, or
  review cycles; use them when the task warrants them within existing permissions.
  Invoke an optional review only when requested.
