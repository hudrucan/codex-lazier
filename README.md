# codex-lazier

Version 0.1.0. Small engineering defaults for OpenAI Codex and ChatGPT Web:
build the smallest sufficient solution while preserving correctness, security,
compatibility, and maintainability. Language and framework agnostic.

## Contents

```text
codex-lazier/
├── README.md
├── LICENSE
├── RESEARCH.md
├── adapters/
│   ├── codex/AGENTS.md
│   └── chatgpt/project-instructions.md
├── skills/codex-lazier/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/policy.md
├── evals/
│   ├── scenarios.json
│   └── results.md
├── tools/
│   ├── package.py
│   └── test_package.py
└── dist/
    ├── codex-lazier-0.1.0.zip
    └── codex-lazier-0.1.0.sha256
```

**One policy, two adapters, one optional skill.** The
[canonical policy](skills/codex-lazier/references/policy.md) lives inside
the skill so the installed folder and ZIP remain self-contained without a
second policy copy. Each adapter is an intentionally repeated, short digest;
neither needs the policy file or skill to apply its defaults. The skill adds
a requested review workflow, not a mandatory finishing pass.

There are no runtime dependencies, services, hooks, MCP servers, or automatic
installation. Python 3.9+ and its standard library are needed only to rebuild
or check the archive. [Research and source decisions](RESEARCH.md) include
license provenance. Original package material is [MIT licensed](LICENSE).

## Optional installation: Codex

These are manual steps; building this package does not perform them.

1. Locate your Codex home: `CODEX_HOME` if configured, otherwise `~/.codex`
   (`%USERPROFILE%\.codex` on Windows). Back up the instruction file you edit.
2. Merge the contents of [the Codex adapter](adapters/codex/AGENTS.md) into
   that directory's existing `AGENTS.md`, or create it if absent. Preserve
   existing instructions. If a non-empty `AGENTS.override.md` exists there,
   it takes precedence: integrate deliberately into the active file rather
   than assuming `AGENTS.md` will load. Project and nested instructions keep
   their project-specific authority. Start a new Codex session afterward.
3. Optionally extract `dist/codex-lazier-0.1.0.zip` into
   `~/.agents/skills/` (`%USERPROFILE%\.agents\skills\` on Windows). The result
   must be `codex-lazier/SKILL.md` with its `agents/` and `references/`
   siblings. Alternatively copy the entire source skill folder. Do not
   overwrite an existing skill of the same name. Current documented discovery
   uses `.agents/skills`; do not assume `CODEX_HOME/skills` is equivalent.
4. Restart if discovery has not refreshed, then invoke
   `$codex-lazier` with a diff, file, or design to review. Metadata sets
   `allow_implicit_invocation: false`; ordinary coding does not invoke it.

Check the loaded instruction sources in a new session and try one scenario
from [the evaluation set](evals/scenarios.json). To remove the package later,
remove only the text you added and the optional skill folder.

## Optional installation: ChatGPT Web

1. Open the intended Project's instructions editor. Back up its current text,
   then merge [the Web adapter](adapters/chatgpt/project-instructions.md),
   preserving project-specific requirements. Start a new chat in that Project.
   No skill upload is needed for these defaults.
2. If personal Skill upload is available, open ChatGPT **Plugins → Skills →
   Create → Upload from your computer** and select
   `dist/codex-lazier-0.1.0.zip`. Then explicitly select the uploaded
   `codex-lazier` skill for a review. Live Web upload and invocation have
   **not yet been verified on this account**; availability and ZIP acceptance
   remain unverified. No plugin or MCP server is required by this package.
3. If upload is unavailable or the ZIP is not accepted, attach `SKILL.md` and
   `references/policy.md` from
   the source folder as ordinary files (or paste their contents), then ask:
   “Use the attached codex-lazier instructions to review this diff only.”
   Supply the diff and relevant project instructions too. This is a manual
   prompt workflow, not native skill installation; `$codex-lazier` alone
   does not register a skill on the Web.

A Project does not gain access to local repositories from these instructions.
Upload or connect the relevant source explicitly. Adding an `AGENTS.md` as a
Project file does not recreate Codex's automatic instruction discovery.

## Compatibility and limits

Documentation checked on **2026-10-20**; actual account installation was not
performed. “Documented” below means supported by the linked documentation,
not a live client test.

| Surface | Status and boundary |
| --- | --- |
| Codex global instructions | [Documented](https://learn.chatgpt.com/docs/agent-configuration/agents-md): Codex-home `AGENTS.md`, override selection, and more specific project guidance. Loading this adapter in a fresh client remains untested. |
| Codex optional skill | [Documented](https://learn.chatgpt.com/docs/build-skills): local skill discovery, required manifest fields, and explicit-only invocation metadata. The folder and ZIP are checked locally; native invocation remains untested. |
| ChatGPT Web defaults | [Documented](https://learn.chatgpt.com/docs/projects): Project instructions apply to Project chats. Exact editor controls and account availability were not inspected. |
| ChatGPT Web personal skill | When available, use Plugins → Skills → Create → Upload from your computer as described above. Live upload, ZIP acceptance, and invocation have not yet been verified on this account. The [general skill documentation](https://learn.chatgpt.com/docs/build-skills) describes plugin distribution but does not establish this account's personal upload availability. Attach/paste remains the fallback. |
| ZIP portability | One top-level folder follows the [Agent Skills format](https://agentskills.io/specification) and [OpenAI API ZIP layout](https://developers.openai.com/api/docs/guides/tools-skills). This verifies packaging, not Web upload support or an API upload test. |

Instructions influence model behavior; they do not enforce it or replace
platform permissions. ChatGPT Web's handling of `agents/openai.yaml` is not
claimed. The skill's description and body also restrict it to explicit review
requests. macOS validation does not establish live Windows or Linux behavior.

## Validation and evaluation

From this directory, on macOS/Linux run `python3 tools/package.py --build`,
then `python3 tools/package.py`. On Windows use `py -3` instead of `python3`.
Build mode writes only the two files in `dist/`; check mode writes nothing.
Both validate metadata, local Markdown links, archive contents, policy
inclusion, CRCs, byte identity, and the SHA-256 sidecar. Rebuilding unchanged
inputs produces the same ZIP bytes.

The manifest validator deliberately accepts only plain, single-line string
values starting with an ASCII letter, without `:` or `#`, control characters,
or YAML boolean/null keywords. Quoted and multiline values are unsupported;
this restricted subset avoids a YAML parser dependency. Run the unquoted-colon
regression with `python3 tools/test_package.py`.

The [12 scenarios](evals/scenarios.json) and [recorded results](evals/results.md)
exercise both adapters independently and the explicitly requested skill.
Results are author-assessed reasoning exercises, not independent model runs
or a cross-platform benchmark. The replay procedure makes that distinction
explicit and measures both false positives and false negatives.
