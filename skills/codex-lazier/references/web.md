## codex-lazier v0.4.0 — ChatGPT Web

Read and apply the [shared policy](policy.md), including its optional Jev
guidance, to coding tasks, planning, audits, reviews and Codex repo handoffs
without a manual skill call.

For Codex with ChatGPT, follow its [canonical workflow](https://github.com/hudrucan/codex-with-chatgpt/blob/main/skill/references/workflow.md).
C2C owns repository access and handoff policy; Lazier adds no runtime dependency.

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

For manual C2C handoff audits, include the next step without waiting for another
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

### Opt-in async C2C v1

Planning remains Web-first. Omitted `async` means `async=false`: keep the manual
workflow above. Only explicit `async=true` enables bounded browser delivery.
For a newly sent `[C2C Handoff]` containing a `C2C_REQUEST` correlation line,
follow C2C's canonical async contract and return only a terminal audit frame,
without Markdown fences, ACKs, extra prose or Fix/Commit follow-up prompts:

```text
[C2C Audit v1]
{"taskId":"<exact taskId>","attemptId":"<exact attemptId>","workspaceId":"<exact workspaceId>","handoffId":"<exact handoffId>","status":"PASS","complete":true,"summary":"MCP audit outcome and inspection limits.","findings":[]}
[C2C Audit End v1]
```

Copy all four correlation values from this newly sent request, never history.
Audit through the routed connector and explicit workspace; missing/ambiguous
routing or insufficient evidence means `BLOCKED`. `PASS` requires a completed
MCP source audit with sufficient evidence. `FIX` requires findings with
repo-relative `file`, positive `line`, `evidence` and a concrete in-scope `fix`.
Other statuses use `findings:[]`. On the first MCP failure immediately return
`ERROR` with the actual error in `summary`; do not retry or return an old success.
Emit `complete:true` and the closing marker only when the audit is terminal.
Never accept stale, partial or late replies as evidence. Codex must verify local
source has not drifted before auto-applying a FIX. The task permits at most three
audits and two auto-fix rounds; lost/recreated handles fail closed per C2C's
contract. Never automatically commit, push, rollout or expand scope.
