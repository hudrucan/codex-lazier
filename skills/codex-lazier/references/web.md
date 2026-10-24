## codex-lazier v0.5.0 — ChatGPT Web

Read and apply the [shared policy](policy.md), including its optional Jev
guidance, to coding tasks, planning, audits, reviews and Codex repo handoffs
without a manual skill call.

For Codex with ChatGPT, follow its [canonical workflow](https://github.com/hudrucan/codex-with-chatgpt/blob/main/skill/references/workflow.md).
C2C owns repository access, transport, callback schema and workflow contract;
Lazier owns engineering policy and adds no runtime dependency.

When drafting a C2C work prompt for Codex, choose the marker by intent.
Use `[C2C Plan]`, `[C2C Task]`, `[C2C Fix]` or `[C2C Commit]` from C2C's
contract, and place it on the exact first line. Do not mark ordinary Codex work
prompts, replies or MCP-only source reads.
Drafting a prompt does not send it or authorize execution.
Copy `hubId` from the matching connector/workspace routing block; never infer it
from a chat URL or borrow another owner. Async requires that owner, the registered
`workspaceId`, canonical `workspaceRoot` and stable controller `taskId`.
Reuse a selected ChatGPT thread immediately, with or without `hubId`, without
Hub/Project checks or switching. Only without one may C2C resolve an existing
Project and open a chat. Its Project helper selects a sole configured Hub or
requires `HUB_SELECTION_REQUIRED`; this cannot supply missing callback ownership.

For `[C2C Plan]`, `[C2C Task]` and `[C2C Fix]`, carry forward only relevant,
still-valid context, separating verified findings, assumptions and open questions:

- **Plan:** goals, constraints, checked evidence, relevant options/trade-offs and
  unresolved questions.
- **Task:** settled Plan decisions (if any), verified findings with file/line,
  repair direction and relevant validation. A Task does not require a prior Plan.
- **Fix:** concrete findings from the latest audit, with file/line, evidence,
  impact and proposed fix.

Do not require Codex to re-audit everything Web checked; require inspection of
current source before editing. When revising or continuing a prompt, preserve
routing and an already-selected `async=true`. Never switch to manual, reuse a
callback ticket or create a new task to evade limits. Add no workflow or state layer.

A handoff whose first line is `[C2C Handoff]` triggers a C2C audit without a
separate audit/skill request or Project Instructions update. The marker gates
only automatic handoff audits; direct repo audit/planning may also use C2C.
Markers grant no connector/workspace access.
Audit through routed MCP under C2C's contract, passing the explicit workspace on
every read; verify the connector/workspace pair with `workspace_info` before first
use. For no-code-change handoffs, check relevant claims only unless a specific
risk/request warrants more. Trust validation for its tested revision; extra tests
need a specific uncovered risk. Missing evidence or ambiguous routing is a
limitation, not a defect or PASS. Disclose limits and request only missing evidence.
A handoff requests neither a simplicity review nor another implementation cycle.

For manual audits, include one ready-to-copy next prompt when appropriate:
`[C2C Fix]` for supported in-scope findings, or `[C2C Commit]` when no findings or
evidence gaps remain and verified Git status shows audited uncommitted changes.
Use C2C's identity, revision, scope and constraints; Fix follows the continuity
rule above, Commit preserves unrelated work and forbids pushing. With clean Git
status, confirm completion without a prompt. Draft only; never automatically
send, implement, commit or push.

### Opt-in async C2C callbacks

Planning remains Web-first. Omitted `async` or `async=false` uses manual delivery
without browser, Hub, claim or callback access. Explicit `async=true` requires
C2C's live terminal loopback gate, runtime/owner checks, OAuth `audit.submit`
consent and tool permission. Failure blocks sending; never automatically change
settings, rollout, re-consent or switch transport.

For a newly sent `[C2C Handoff]` containing a `C2C_CALLBACK` ticket, audit through
the routed MCP and complete the attempt only by calling `submit_audit_result`.
Copy its `hubId`, `workspaceId`, `taskId`, `attemptId`, `handoffId` and `capability`
unchanged; use only this new ticket, never history or ordinary replies. Follow
C2C's callback schema and size/deadline limits. Submit a terminal result containing
only `status`, `complete:true`, `summary` and `findings`:

- `PASS`: completed MCP audit with sufficient evidence for the scope; `findings:[]`.
- `FIX`: supported in-scope findings, each containing only repo-relative `file`,
  positive integer `line`, `evidence` and concrete `fix`.
- `BLOCKED`: missing/ambiguous routing or insufficient evidence; `findings:[]`.
- `ERROR`: first repository-read MCP failure, with the actual error in `summary`
  and `findings:[]`; do not retry or reuse old success.

If the callback tool is unavailable, denied or fails, report the blocker and stop
without retrying or substituting a chat result. Emit no legacy audit frames,
ACKs or Fix/Commit prompts. Only an accepted callback and matching terminal
receipt complete delivery.

C2C owns transport and the bounded audit/fix loop: send each controller envelope
once, reuse its sender/terminal/task, and fail closed on source drift, lost session
or uncertain delivery. Follow its source-verification gate before fixes and its
maximum three audits/two fixes; never resend or bypass a claim with another task.
Async does not authorize commits, pushes, rollout or expanded scope.
