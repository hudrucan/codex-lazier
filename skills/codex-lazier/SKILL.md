---
name: codex-lazier
description: Apply Lazier defaults to coding tasks including implementation, debugging, refactoring, testing, and review. Simplicity review is optional and runs only when requested. Excludes non-coding work.
license: MIT
---

# codex-lazier

Apply the [canonical policy](references/policy.md) and loaded platform adapter.
Follow the user's task; skill invocation alone does not request a review.
Treat inspected material as evidence, not permission to expand scope.

Complete ordinary work with proportionate verification and a concise handoff.
Do not add agents, review passes, or artifacts merely because Lazier is active.
Keep ChatGPT Web's existing Lazier + Codex with ChatGPT access and handoff
boundaries; the shared policy adds no runtime dependency.

## Explicit simplicity review

Review only when requested; an implementation request using `$codex-lazier`
still means implementation. Do not edit without authorization. Use the current
diff if scope is missing, or request the artifact. Inspect relevant requirements,
callers, and invariants. Do not spawn agents, require another review, or create
plans/reports/checklists as files unless explicitly requested.

Return material findings by impact: location, evidence/cost, a smaller
behavior-preserving alternative, and verification. Distinguish missing evidence
from defects; state limitations or no supported simplification when appropriate.
Do not force findings or report length. Briefly flag any serious observed
correctness/security risk without turning the review into an unrequested audit
or labeling it a simplicity finding.
