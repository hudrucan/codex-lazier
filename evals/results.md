# v0.1 evaluation results

Assessment date: 2026-10-20. Evaluator: the authoring Codex assistant in this
chat. These are **manual reasoning exercises with known expectations**, not
independent or blinded model executions. No fixture code was executed, no
native client was installed, and no ChatGPT Web behavior was observed.

## Reproduce

Use [scenarios.json](scenarios.json); each case includes a complete prompt,
an expected decision, required outcomes, and forbidden shortcuts. No runner,
API credentials, external dependencies, or additional agents are needed.

For a stronger behavioral replay, use a fresh chat per case and profile:

1. **Codex defaults:** provide only `adapters/codex/AGENTS.md` and the case's
   `prompt`. Do not provide the optional skill or full policy.
2. **Web defaults:** provide only `adapters/chatgpt/project-instructions.md`
   and the prompt. Do not provide a local path as though Web can read it.
3. **Optional skill:** provide the skill manifest and bundled policy with the
   explicit codex-lazier prompts S01–S11. For S12, expose only the
   manifest's discovery description and invocation metadata: this is a negative
   routing test, so do not instruct the model to invoke the skill.

Keep `expected_action`, `required`, and `forbidden` out of the tested prompt.
Record the response before comparing it to the rubric. Pass a case only if
all required outcomes are addressed and none of the forbidden actions is
recommended. Do not grade by word matching, line count, or exact formatting.
Record model/version and surface when running an actual client replay.

For decision scoring, a positive is a justified simplification: proposing one
on an expected `keep` case is a false positive; missing one on an expected
`simplify` case is a false negative. Also check the full rubric: an answer that
finds a real simplification but removes a necessary control still fails.
`keep` means no justified simplification in the supplied scope, not necessarily
no task work (S12) or a claim that unseen code is sound (S10).

## Recorded decisions

Each cell records the author-assessed response for that profile. Both adapters
were considered independently, without relying on the optional policy file.
The shared outcomes are intentional: the adapter texts are identical.

| Case | Codex defaults response | Web defaults response | Optional skill / routing response |
| --- | --- | --- | --- |
| S01 | Simplify: call the existing mailer directly; retain mail error propagation and signup regression coverage. | Simplify: use one welcome-email operation; keep failure behavior and its regression protection. | Finding at design.md: registry/factory have no present selection or policy role; replace them with the mailer operation without changing the failure contract. |
| S02 | Simplify: remove only forward_total and call calculate_total, preserving its validation and result. | Simplify: the private forwarder adds no boundary; retain calculate_total's behavior. | Finding at total.py: confirmed single-use argument forwarding adds a maintenance hop; direct call preserves validation. This does not condemn all single-use helpers. |
| S03 | Simplify lines 10–18's noise and redundant catch; preserve the boundary log, redacted audit event, invariant comment, and thrown error. | Simplify the narrating comment, debug message, and context-free repeated report; keep the distinct audit and invariant explanations. | Findings at handler.py: remove redundant narration and duplicate reporting; let the unchanged failure reach the handling boundary. Keep lines 21–22. |
| S04 | Simplify README's phase/day entries; retain setup and JSON support, migration guidance, and project-required release notes. | Simplify product docs to current behavior; keep migration and release records in their existing locations. | Finding at README.md: abandoned phases obscure the supported setup/JSON contract. Remove diary entries without creating another diary or deleting useful migration records. |
| S05 | Simplify duplicate amount coverage and private call-order assertions; keep public outcomes, durable-write-before-ack tests, and existing fixtures. | Simplify only redundant and incidental assertions; the recovery ordering is contractual and stays. | Findings at tests/test_receipt.py: deduplicate the same amount case and remove incidental helper ordering; retain the crash-recovery interaction assertion and coverage strength. |
| S06 | Simplify the proposed patch to the CSV fix and regression; preserve unrelated user changes in any working-tree edit. | Simplify patch scope by omitting unnecessary reformatting and renaming; retain the fix and test. | Finding in the unrelated 40-file diff: maintenance/review cost has no dependency on the delimiter fix. Exclude those proposed edits safely, without blindly reverting files. |
| S07 | Keep: TenantStore enforces resource isolation separately from authentication; the demonstrated cross-tenant failure justifies the wrapper and tests. | Keep the single-implementation boundary, token validation, and tenant authorization; do not remove protection as duplication. | No supported simplification. The wrapper has a present isolation responsibility, backed by the raw-store regression; middleware does not replace it. |
| S08 | Keep the transaction, stock condition, durable uniqueness, and concurrency regression; a read then write permits the demonstrated race. | Keep atomic persistence and durable deduplication; process-local checks or cache do not satisfy the contract. | No supported simplification. reserve.sql/reservation.py's mechanisms protect separate required invariants under simultaneous workers; retain the regression evidence. |
| S09 | Keep both version parsers and contract tests; external version 1 support remains a current requirement despite no local callers. | Keep version 1 until the published support contract changes; local search alone cannot establish dead code. | No supported simplification. decode.py implements a documented external compatibility target; removing it would change supported behavior. |
| S10 | No supported finding from length or classes alone; request source and requirements without claiming correctness or test success. | Insufficient evidence for simplification; request reconcile.py and its contract instead of endorsing an arbitrary split. | No supported simplification can be established. The supplied size/style preference supports neither severity nor a redesign; source and requirements are missing. |
| S11 | Keep bounded retries, deadline, permanent-error behavior, shared delay helper, terminal diagnostic, and recovery test; do not return success-shaped emptiness. | Keep documented recovery and distinct failure semantics; the one useful report and helper serve current needs. | No supported simplification. sync.py's bounded recovery has regression evidence and current consumers; the proposed catch-all default destroys the error contract. |
| S12 | Change only the label and required accessibility record; run the existing UI check, reporting its actual result. No optional review or agents. | Apply the requested text fix and local record requirement; use existing verification without extra review artifacts. | Do not activate: the task is ordinary implementation and explicitly excludes review. Apply the adapter/local requirements without loading a review workflow. |

All 36 manual decisions satisfy their case rubrics in this author assessment.
This is a design sanity check, not evidence that a deployed model will always
follow the policy.

| Profile | True positives | True negatives | False positives | False negatives | Full rubric passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Codex defaults | 6 | 6 | 0 | 0 | 12/12 |
| Web defaults | 6 | 6 | 0 | 0 | 12/12 |
| Optional skill / routing | 6 | 6 | 0 | 0 | 12/12 |

The six positive cases check missed opportunities. The six negative cases
check overreach into security, atomic persistence, supported compatibility,
unsupported findings, recovery, and unrequested workflows. S03–S05 also check
that a valid simplification preserves necessary logging, comments, records,
and contractual interaction tests.

## Verification boundary

Local structural verification is reproducible with `python3 tools/package.py`.
Validation environment: macOS, Python 3.14.7. The behavioral results above are
manual assessments, separate from executable packaging checks.

| Check | Observed result |
| --- | --- |
| `python3 tools/package.py --build` and default check mode | PASS: restricted plain-string YAML frontmatter, required interface metadata, explicit-only invocation policy, local links, four allowed archive members, CRCs, byte identity with the current LICENSE and skill sources, and checksum. |
| `python3 tools/test_package.py` | PASS: changed interface text is accepted; missing/blank interface fields, malformed quoted strings, implicit invocation, and unquoted-colon frontmatter are rejected without reporting PASS. |
| Scenario data | 12 unique IDs, six positive and six negative decisions, each with required and forbidden outcomes. |
| Adapter comparison and text hygiene | Identical adapters; text files have final newlines and no trailing whitespace. |

The skill ZIP contains four files and is 4,429 bytes. Its SHA-256 is
`2fd9e5009b83ece7fb9b648a4cd956040ace222f4d2ad69716dab877f25536f9`.
The README lists the platform claims supported by official documentation.

Not yet verified: native discovery/invocation, instruction loading in a fresh
Codex client, Web Project behavior, actual API ZIP upload, personal Web Skill
upload/invocation on this account, Windows/Linux execution, independent graders,
and blinded model responses. Packaging validation does not establish live
platform compatibility.
