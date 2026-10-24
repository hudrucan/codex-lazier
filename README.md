# codex-lazier

Version 0.4.0. Always-on engineering defaults for Codex and ChatGPT Web:
build the smallest complete solution while preserving correctness and required
safeguards. Simplicity review is optional, with no finishing review pass.

## Activation

The [canonical policy](skills/codex-lazier/references/policy.md) defines shared
behavior. The adapters define platform activation:

- [Codex](adapters/codex/AGENTS.md): engineering defaults plus preferences for
  the installed Context Mode plugin; reads the local C2C contract before each
  C2C task's final handoff.
- [ChatGPT Web](adapters/chatgpt/project-instructions.md): Lazier + Codex with ChatGPT,
  without added runtime dependencies or tool integrations.

This repo's [AGENTS.md](AGENTS.md) loads the Codex adapter. Elsewhere, merge the
appropriate adapter into active Codex `AGENTS.md` or Web Project Instructions,
preserving existing guidance. For personal Codex defaults, use
`CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`); check for an active
`AGENTS.override.md`. Start a new chat and verify loaded instructions.

Install [the skill](skills/codex-lazier/SKILL.md) in a discovery location supported
by the host, such as `~/.agents/skills/` for Codex, or upload the ZIP where Web
supports skills. Its [metadata](skills/codex-lazier/agents/openai.yaml) retains
implicit invocation. The description covers Codex handoffs, planning, audits and
reviews. When available to Web with C2C routing already configured, a handoff
starting with `[C2C Handoff]` triggers a Git/source audit without a separate audit request or updates to
each Project's Instructions. Discovery
does not guarantee host invocation or grant connector access. A `$codex-lazier`
implementation request remains implementation, not a request for review.

After a C2C handoff audit, Web supplies the next step: a ready-to-copy
`[C2C Fix]` prompt for actionable findings, a `[C2C Commit]` prompt for a PASS
with audited uncommitted changes, or completion with no prompt for a PASS with
clean Git status. Incomplete evidence is reported as a limitation. Prompts do
not execute automatically; see the [Web skill guidance](skills/codex-lazier/SKILL.md#chatgpt-web-handoff-trigger).

Web follows the [canonical C2C workflow](https://github.com/hudrucan/codex-with-chatgpt/blob/main/skill/references/workflow.md). Project
instructions grant no local repository access and inherit no Codex runtime or
hooks. They do not change Codex with ChatGPT architecture, code, or license.

## Context Mode on Codex

Reuse the installed plugin; do not copy its code/hooks or register another MCP
server. Verify `codex plugin list --json`, responding `ctx_*` tools,
`ctx_doctor`, hook trust, and a harmless routing probe. Installation or a doctor
PASS alone does not prove interception. Trust review remains the host's job.

Runtime limits:

- In v1.0.169, selected HTTP/build branches emit deny/rewrite decisions; ordinary
  reads, searches, and diffs receive advisory guidance. Host-supported decisions
  are enforced; following advisory instructions remains the model's responsibility.
  Lazier adds no enforcement runtime.
- SQLite must support FTS5. Node version alone is insufficient; a working built-in
  backend avoids the native addon. Dependencies installed only inside versioned
  plugin cache can disappear when that cache is refreshed.
- Doctor may warn because plugin listing omits the runtime root even when the
  plugin is enabled and routing works. `ctx_stats` contains cumulative estimates;
  its host labels, pricing, and compaction claims are not verified benchmarks.

Follow the adapter's tool preferences and evidence rules. Small observations,
edits, and exact patch-source reads may stay native. On failure, report the limit
once and continue with bounded native tools under the same permissions.

## Package and validate

Original material remains [MIT licensed](LICENSE); no runtime dependency is added
by Lazier. Python 3.9+ and its standard library are used only for packaging.

```sh
python3 tools/test_package.py
python3 tools/package.py --build
python3 tools/package.py
git diff --check
```

On Windows use `py -3`. Build mode writes
`dist/codex-lazier-0.4.0.zip` and its `.sha256` sidecar; check mode writes nothing.
The six members under `codex-lazier/` are `SKILL.md`, `agents/openai.yaml`,
`references/policy.md`, `LICENSE`, and both adapters. Bundled adapters do not
install themselves as active instructions.

The [regression tests](tools/test_package.py) exercise metadata rejection,
adapter/license inclusion, reproducibility, stale sources, and checksum failures.
The [validator](tools/package.py) also checks local links, exact archive members,
CRCs, file modes, and source identity. These checks do not prove model compliance
or live Web compatibility; Web behavior remains untested.

[Research notes](RESEARCH.md) retain source/license provenance. Platform references:
[AGENTS.md loading](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide),
[skill metadata](https://developers.openai.com/plugins/deploy/submission-errors),
[plugin hooks](https://developers.openai.com/plugins/build/plugins),
[Project instructions](https://learn.chatgpt.com/docs/projects).
