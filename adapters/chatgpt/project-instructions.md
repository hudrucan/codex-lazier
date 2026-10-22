## codex-lazier v0.2 — ChatGPT Web

Apply these defaults to coding tasks, planning, audits, reviews and Codex repo
handoffs without a manual skill call. User direction, project requirements,
and platform security take precedence;
no permissions are granted. Simplicity review runs only when requested, with no
mandatory finishing pass.

For Codex with ChatGPT, follow its [canonical workflow](https://github.com/hudrucan/codex-with-chatgpt/blob/main/skill/references/workflow.md).
C2C owns repository access and handoff policy; Lazier adds no runtime dependency.

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
