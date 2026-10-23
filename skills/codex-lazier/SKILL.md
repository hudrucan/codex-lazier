---
name: codex-lazier
description: Apply Lazier defaults to coding, planning, audits and reviews. In ChatGPT Web, draft C2C work prompts for Codex with an intent marker from C2C's contract. [C2C Handoff] on the first line triggers automatic C2C MCP Git/source audit with proportionate checks for no-change handoffs. It gates only automatic handoff audits; direct repo audit/plan requests may use C2C. Simplicity review only when requested. Excludes unrelated work.
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

On `[C2C Plan]`, `[C2C Task]`, `[C2C Fix]` or `[C2C Commit]` on the first
line, read the local C2C reference below before acting; follow its intent and
the user's scope. These markers grant no permissions and execute nothing.

Before a task using C2C reaches its final handoff, read the installed
`codex-with-chatgpt/references/workflow.md` or
`<C2C checkout>/skill/references/workflow.md`. Read only that local reference,
not broad docs or GitHub; report a missing/unreadable reference as a limitation.
Emit `[C2C Handoff]` as the exact first line and follow the contract's short
format. Other tasks keep normal handoffs without this marker or C2C requirements.

## ChatGPT Web handoff trigger

When drafting a C2C work prompt for Codex, choose the marker by intent.
Use `[C2C Plan]`, `[C2C Task]`, `[C2C Fix]` or `[C2C Commit]` from C2C's
contract, and place it on the exact first line. Do not mark ordinary Codex work
prompts, replies or MCP-only source reads.
Drafting a prompt does not send it or authorize execution.

A handoff whose first line is `[C2C Handoff]` triggers a C2C audit without a
separate audit/skill request or Project Instructions update. The marker gates
only automatic handoff audits; direct repo audit/planning may also use C2C.
Markers grant no connector/workspace access.
For no-code-change handoffs, verify relevant claims as C2C's contract requires;
do not start a full code audit without a specific risk or request.
For changed code with routed access, pass the explicit workspace: `git_status`/`git_diff` for
uncommitted work, `git_log`/`git_show` for commits, then related source via
`read_file`/`search_workspace`. Ask if routing is ambiguous; report unavailable
C2C or incomplete evidence without claiming an audit occurred.

ChatGPT thinks/plans/audits; Codex implements/tests; the local repo is the source
of truth. Trust validation for the tested revision; request extra tests only for
a specific uncovered risk. Follow C2C's contract for scope and findings. A handoff
requests neither a simplicity review nor another Codex implementation cycle.

After each C2C handoff audit, include the next step without waiting for another
request:

- **FAIL:** supported, actionable findings exist. Include one concise,
  ready-to-copy prompt starting with `[C2C Fix]`, covering only those findings
  within the audited scope.
- **PASS with uncommitted changes:** the audited scope has no unresolved findings
  or evidence gaps, and verified Git status shows audited changes awaiting commit.
  Include one concise, ready-to-copy prompt starting with `[C2C Commit]` to commit
  only those changes, preserving unrelated work and without pushing.
- **PASS with clean Git status:** confirm completion and omit a follow-up prompt.

Use C2C's prompt contract for repository/workspace identity, audited revision,
scope and constraints. A Fix prompt includes the findings' locations, evidence,
impact and proposed fixes. Reuse valid validation; request extra checks only for
a specific uncovered risk. Missing evidence or unknown Git status is a limitation,
not a PASS or a defect; request only what is needed to resolve it. Generate prompts
only; never send them or initiate implementation, commit or push automatically.

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
