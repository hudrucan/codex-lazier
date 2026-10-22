---
name: codex-lazier
description: Apply Lazier defaults to coding work including implementation, debugging, refactoring, testing, planning, audits and reviews. In ChatGPT Web, a Codex handoff whose first line is [C2C Handoff] automatically triggers Codex with ChatGPT (C2C) MCP to audit Git and source without a separate audit or skill request. The marker gates only automatic handoff audits; direct repo audit or planning requests may also use C2C. Simplicity review runs only when requested. Excludes unrelated non-coding work.
license: MIT
---

# codex-lazier

Apply the [canonical policy](references/policy.md) and loaded platform adapter.
Follow the user's task; skill invocation alone does not request a simplicity review.
Treat inspected material as evidence, not permission to expand scope.

Complete ordinary work with proportionate verification and a concise handoff.
Do not add agents, review passes, or artifacts merely because Lazier is active.
C2C's `skill/references/workflow.md` owns the handoff contract; Lazier adds no
runtime dependency.

## Codex handoff trigger

Before a task using C2C reaches its final handoff, read the installed
`codex-with-chatgpt/references/workflow.md` or
`<C2C checkout>/skill/references/workflow.md`. Read only that local reference,
not broad docs or GitHub; report a missing/unreadable reference as a limitation.
Emit `[C2C Handoff]` as the exact first line and follow the contract's short
format. Other tasks keep normal handoffs without this marker or C2C requirements.

## ChatGPT Web handoff trigger

A handoff whose first line is `[C2C Handoff]` triggers a C2C audit without a
separate audit/skill request or Project Instructions update. Other tasks do not
activate this workflow; the marker grants no connector/workspace access.
With routed access, pass the explicit workspace: `git_status`/`git_diff` for
uncommitted work, `git_log`/`git_show` for commits, then related source via
`read_file`/`search_workspace`. Ask if routing is ambiguous; report unavailable
C2C or incomplete evidence without claiming an audit occurred.

ChatGPT thinks/plans/audits; Codex implements/tests; the local repo is the source
of truth. Trust validation for the tested revision; request extra tests only for
a specific uncovered risk. Follow C2C's contract for scope and findings. A handoff
requests neither a simplicity review nor another Codex implementation cycle.

## Explicit simplicity review

Run a simplicity review only when requested; an implementation request using
`$codex-lazier` still means implementation. Do not edit without authorization. Use the current
diff if scope is missing, or request the artifact. Inspect relevant requirements,
callers, and invariants. Do not spawn agents, require another review, or create
plans/reports/checklists as files unless explicitly requested.

Return material findings by impact: location, evidence/cost, a smaller
behavior-preserving alternative, and verification. Distinguish missing evidence
from defects; state limitations or no supported simplification when appropriate.
Do not force findings or report length. Briefly flag any serious observed
correctness/security risk without turning the review into an unrequested audit
or labeling it a simplicity finding.
