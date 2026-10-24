<div align="center">

# codex-lazier

**Small changes. Complete solutions.**

Engineering defaults that keep Codex and ChatGPT focused on simple, correct work.

[![CI](https://github.com/hudrucan/codex-lazier/actions/workflows/ci.yml/badge.svg)](https://github.com/hudrucan/codex-lazier/actions/workflows/ci.yml)
[![Runtime dependencies: none](https://img.shields.io/badge/runtime_dependencies-none-3b82f6)](#why-lazier)
[![License: MIT](https://img.shields.io/badge/license-MIT-64748b)](LICENSE)

[Quick start](#quick-start) · [Examples](#in-practice) · [Integrations](#optional-integrations) · [Development](#development)

</div>

## Why Lazier?

A change should stay proportional to the problem it solves.

Lazier is a portable engineering policy for **Codex Local** and **ChatGPT Web**.
It guides agents to understand the existing system, make a focused change, and
verify the behavior that matters.

- **Keep it simple.** Reuse existing tools and patterns. Add machinery when a
  current requirement justifies its cost.
- **Keep it correct.** Preserve contracts, failure handling, security boundaries,
  and recovery behavior. Necessary safeguards stay.
- **Keep it grounded.** Base decisions and review findings on source evidence.
  Run relevant checks and state what remains unverified.

The package is instructions: one Skill, two host references, and a
[shared policy](skills/codex-lazier/references/policy.md). No daemon, custom hook,
or runtime dependency. Simplicity reviews run only when you ask.

## Quick start

### 1. Get the package

Download the ZIP and its matching `.sha256` file from
**[GitHub Releases](https://github.com/hudrucan/codex-lazier/releases)**.
Put the two files from the same release in an otherwise empty directory:

```sh
sha256sum --check codex-lazier-*.sha256
```

On macOS, use `shasum -a 256 -c codex-lazier-*.sha256`. No release available yet?
[Build from source](#development).

### 2. Choose your host

#### Codex Local

Extract into a skill directory supported by your host:

```sh
mkdir -p ~/.agents/skills
unzip codex-lazier-*.zip -d ~/.agents/skills
```

Then start a new session and use `$codex-lazier` in your request.

<details>
<summary><strong>Apply Lazier automatically to coding tasks</strong></summary>

Add an instruction to your repository's `AGENTS.md`, or your Codex home's
`AGENTS.md` (normally `~/.codex/AGENTS.md`), to read and apply the installed
Skill's `references/codex.md` once per chat for every coding task. Use its actual
absolute installed path. That reference loads `references/policy.md` itself;
no manual Skill invocation is needed for this bootstrap.
Preserve existing guidance and check for an active `AGENTS.override.md`.

Start a new session and ask Codex to summarize its loaded instructions.
Installing the Skill alone does not activate persistent instructions.
The [Codex reference](skills/codex-lazier/references/codex.md) owns C2C handoffs
and Context Mode preferences. For a legacy installation that copied Lazier into
`AGENTS.md`, replace only that Lazier block with the bootstrap above. Keep the
installed references together; do not maintain another policy copy.

</details>

#### ChatGPT Web

1. Where Skill uploads are supported, install the release ZIP as a ChatGPT Skill.
2. Start a new conversation and check that `codex-lazier` is available. The Skill
   loads its Web reference for coding and automatic C2C handoff audits.
3. Keep MCP connector, Hub and workspace routing in **Project Instructions**.
   Lazier behavior comes from the installed Skill.

For hosts without Skill support, optionally make the existing
[policy](skills/codex-lazier/references/policy.md) and
[Web reference](skills/codex-lazier/references/web.md) available as Project sources
and instruct the Project to apply both for coding and C2C work. Disclose if the
host cannot read them. Preserve existing Project guidance; no Lazier copy in
Project Instructions is needed. Installing the Skill neither connects a repository
nor grants access.

## In practice

### Implement a change

```text
Use $codex-lazier to add pagination to this endpoint.
Follow the existing API conventions and test the relevant behavior.
```

The agent traces the current flow, chooses a focused implementation, and
reports the checks it actually ran. No automatic simplicity-review cycle.

### Ask for a simplicity review

```text
Review this diff for unnecessary complexity.
Report supported simplifications; do not edit.
```

Findings need evidence and a smaller alternative that preserves required
behavior. Justified code can stay unchanged.

### Delegate through C2C

```text
[C2C Task]
Repo: <repository>; workspace: <registered workspace ID>.
Add pagination using the existing API conventions.
Run focused validation. Do not commit or push.
```

With C2C configured, Web plans and audits while Codex implements and tests
against local source. `[C2C Plan]` only plans; `[C2C Task]` implements within
scope. Markers and drafted prompts do not execute work or grant permissions.

## Optional integrations

Lazier works on its own. These integrations reuse tools you already have.

- **[Codex with ChatGPT](https://github.com/hudrucan/codex-with-chatgpt)** connects Web planning
  and audits with Codex implementation. It owns repository access and the
  [handoff contract](https://github.com/hudrucan/codex-with-chatgpt/blob/main/skill/references/workflow.md).
  The [Web reference](skills/codex-lazier/references/web.md) covers automatic
  handoff audits, manual Fix/Commit prompts and opt-in `async=true` callbacks.
  Async requires C2C runtime/OAuth support and an accepted MCP result received by
  the terminal; it does not authorize commits, pushes or rollout.
- **[Context Mode](https://github.com/mksglu/context-mode)** keeps large analysis
  output out of the conversation. The Codex reference prefers installed `ctx_*`
  tools and falls back to bounded native tools when unavailable. Small
  observations and edits can stay direct.
- **[TypeSafe Jev](https://docs.typesafe.ai/introduction/coding-agents)** offers
  a second opinion on substantial C2C decisions with meaningful technical
  trade-offs. Web normally asks once after inspecting constraints and evidence,
  or defers to Codex when fresh local inspection is needed. Reuse the advice;
  skip trivial or settled decisions.

Jev remains advisory. Never automatically forward private source, secrets,
or credentials. Unavailable or abstaining advice does not block the task.

## What to expect

Lazier guides engineering judgment; it does not enforce behavior or guarantee
correctness. User instructions, project requirements, and platform security take
precedence. A successful build or a model probability is not a correctness proof.

Host support determines Skill discovery and invocation. Optional integrations
need their own configuration and permissions; installing Lazier grants neither.
Context Mode installation alone does not prove routing or enforcement.

## Development

Python 3.9+ and its standard library are enough. From a source checkout:

```sh
python3 tools/test_package.py
python3 tools/package.py --build
python3 tools/package.py
git diff --check
```

No package installation or network access is needed. On Windows, use `py -3`.
Build first on a fresh checkout; check mode validates an existing build without
writing. ZIPs and checksums go into ignored `/dist/` and must not be committed.

<details>
<summary><strong>Package contract and release checks</strong></summary>

Every ZIP contains exactly six files under `codex-lazier/`:

```text
SKILL.md
agents/openai.yaml
references/policy.md
references/codex.md
references/web.md
LICENSE
```

Validation checks metadata, local links in the repository and installed package,
archive members, CRCs, permissions, source identity, and SHA-256. Host guidance
lives only in the Skill references; source and ZIP have no separate adapter tree. Tests cover
package link resolution, reproducibility, stale archives, and mismatched release
tags. These local checks do not prove live model or integration behavior.

The [workflow](.github/workflows/ci.yml) runs on pull requests, pushes to
`main`, and `v*` tags. It tests, builds, and compares reproducible output.
Only a successful version-tag build can publish the ZIP and checksum to
GitHub Releases. The tag must exactly match `v<VERSION>` in `tools/package.py`.
For a new version, update that value and the policy/host-reference headings before
tagging.

CI is read-only. Only the tag-only release job has repository write permission.
It uses SHA-pinned GitHub actions and the built-in token, with no custom secrets
or publishing service.

</details>

Contributions should stay focused, preserve the Skill contract, and include
checks appropriate to the change.

## License

[MIT](LICENSE). See [research and provenance](RESEARCH.md) for the references
behind the policy. Upstream implementations are not bundled.
