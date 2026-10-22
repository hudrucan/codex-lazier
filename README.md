# codex-lazier

Version 0.2.0. Always-on engineering defaults for Codex and ChatGPT Web:
build the smallest complete solution while preserving correctness and required
safeguards. Simplicity review is optional, with no finishing review pass.

## Activation

The [canonical policy](skills/codex-lazier/references/policy.md) defines shared
behavior. Both adapters are self-contained:

- [Codex](adapters/codex/AGENTS.md): engineering defaults plus preferences for
  the installed Context Mode plugin.
- [ChatGPT Web](adapters/chatgpt/project-instructions.md): Lazier + Codex with ChatGPT,
  without added runtime dependencies or tool integrations.

This repo's [AGENTS.md](AGENTS.md) loads the Codex adapter. Elsewhere, merge the
appropriate adapter into active Codex `AGENTS.md` or Web Project Instructions,
preserving existing guidance. For personal Codex defaults, use
`CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`); check for an active
`AGENTS.override.md`. Start a new chat and verify loaded instructions.

Optionally install [the skill](skills/codex-lazier/SKILL.md) in a supported
discovery directory such as `~/.agents/skills/`. Its
[metadata](skills/codex-lazier/agents/openai.yaml) permits implicit invocation;
discovery alone does not guarantee always-on loading. A `$codex-lazier`
implementation request remains implementation, not a request for review.

Web retains the existing Codex with ChatGPT source-access and handoff workflow. Project
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
`dist/codex-lazier-0.2.0.zip` and its `.sha256` sidecar; check mode writes nothing.
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
