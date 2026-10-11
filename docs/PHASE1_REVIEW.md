# Phase 1 review — issuer disclosure and attestation protocol

Date: 2026-10-11 (Africa/Lagos client date).

Historical checkpoint: this report describes local commit `4ab487e` before the
two follow-up specification fixes. Its 102-test count and source hashes apply
only to that checkpoint. The precedence and specificity-only concerns below
were subsequently addressed; see [the updated audit](SECURITY_AUDIT.md) and
[follow-up results](PHASE1_SPEC_FIX_RESULTS.md). No checkpoint is newly deployed.

Scope completed locally: constructor additions, two consensus paths, frozen agenda,
issuer disclosure rounds, attestation, bounded history, direct tests, lint and schema.
Stop point: the requested local commit, awaiting approval before Phase 2.

The published README, SECURITY_AUDIT, TEST_MATRIX, PORTAL_SUBMISSION, deployment
script and old manifests describe the preceding one-round implementation.
Their Phase 2/3 replacements remain deferred under the supplied phased request.
Old transaction receipts do not demonstrate the new protocol.

## Implementation

- Constructor retains the six existing parameters and appends issuer_address
  and max_disclosure_rounds (strict integer, 1–3). Zero issuer addresses are
  rejected. The module POWER taxonomy is the seven labels in the request.
- review() remains permissionless. Every source must be HTTP 200 with complete,
  nonempty UTF-8 content of at most 15,000 raw bytes. Each successful body is
  hashed; a canonical source snapshot list is hashed into evidence_digest.
  Independently fetched bodies must therefore match, as well as classifications.
- Model outputs cover exactly the frozen claim IDs. Each QUALIFIED claim has
  nonempty, unique known powers, sorted in code; other claims have no powers.
  Unknown labels, missing/extra fields and malformed nested values revert.
- The round-one result stores a deterministic, sorted agenda of [claim_id, power]
  pairs when DISCLOSURE_REQUIRED is reached. review() then rejects further calls,
  including after disclosure completion or timeout. Round one cannot be relitigated.
- submit_disclosure(url) checks the immediate sender against issuer_address,
  lifecycle, bounded round count, URL syntax, and exact-string URL replay before
  consensus. The URL is fetched independently by leader and validators.
- Round two produces one ADEQUATE/INADEQUATE/UNCLEAR verdict per agenda pair.
  ADEQUATE requires the power, who holds/can exercise it, and its limits or
  conditions in the fetched text. Missing pairs, duplicate pairs, invented
  claims/powers and an unavailable body's purported ADEQUATE verdict are rejected.
- Both validators canonicalize the complete leader result, independently fetch
  and judge again, and compare the complete canonical dictionaries. Accepted
  output is canonicalized again before storage. Every consequential returned
  field has a behavioral mutation test; an AST regression guard ties result
  schemas and both validators to whole-result equality.
- Available but inadequate/unclear text consumes a round. Unavailable, oversized,
  empty, invalid UTF-8 and failed-fetch disclosures also consume a round, with
  empty digest and all UNCLEAR verdicts. A malformed model result reverts the
  transaction, so it creates no accepted round/history record.
- All adequate pairs produce LISTED_WITH_DISCLOSURE and an attestation containing
  token_id, the SHA-256 of canonical frozen claims, agenda, disclosure URL/body
  digest, round and per-pair verdicts. Otherwise the gate remains
  DISCLOSURE_REQUIRED until the final used round, which produces
  DISCLOSURE_REJECTED. Success on the last permitted round still succeeds.
- History is at most three records. attempts counts completed review rounds;
  rounds_used separately counts completed disclosure rounds.

## Deadline behavior

Before max_wait, open reviews/disclosures may proceed. At max_wait exactly
and afterward, get_state() reports a terminal timeout: DISCLOSURE_REJECTED
for an open agenda, UNVERIFIABLE for PENDING or retriable UNVERIFIABLE.

A view computes this status without writing storage. Late disclosure calls
revert before fetching or consuming a round. A review without an agenda may
materialize UNVERIFIABLE timeout; a review with an agenda always reverts.
Previously completed terminal outcomes remain unchanged after max_wait.
Time passing alone does not send a transaction.

## Schema-extracted public interface

~~~python
__init__(
    token_id: str,
    manifest_json: str,
    capability_context_json: str,
    source_urls_json: str,
    min_sources: int,
    max_wait_iso: str,
    issuer_address: Address,
    max_disclosure_rounds: int,
)
review() -> dict                       # write, permissionless
submit_disclosure(disclosure_url: str) -> dict  # write, issuer only
get_state() -> dict                    # view
~~~

The state exposes status/terminal, frozen claim states and powers, agenda,
source coverage/digest, issuer, rounds used/max, per-round history, attestation,
max_wait and review attempts.

## Toolchain and verification

- Python: 3.14.2, C:\Python314\python.exe.
- pytest: 9.0.2; genlayer-test: 0.29.2; genvm-linter: 0.11.1rc2;
  genlayer-py: 0.18.0; GenLayer CLI: 0.39.2; Node: 24.12.0.
- The original 28 tests were reproduced before editing with this toolchain.
- Final complete direct suite: 102 PASSED, 0 FAILED, 0 SKIPPED.
  See [the full test list](PHASE1_TEST_RESULTS.md).
- GenVM lint: 3 checks passed; SDK validation passed (8 constructor parameters,
  2 writes, 1 view). Schema extraction passed.
- Linter warning I200 reports a newer available runner; the requested runner
  remains unchanged.
- Runner: py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6.
  It matches the original committed source and the first line independently
  read from StudioNet gen_getContractCode for
  0x33445EEF1a870071D33D3141c512898c2AaeF3f0.
  This checks the old deployment's runner, not the identity of a new deployment.
- Contract on disk is LF-only (zero CR bytes), 24,878 UTF-8 bytes.
- Contract SHA-256: e0d2f314a1f4c8e8bda1d00436f5bcf9012154f6b304baa88649df90bc74c668.
- Contract Git blob: ebe30019cc2c10b0a264fb916bd4004893b5dede.
- Existing .gitattributes already has *.py, *.md and *.json text eol=lf;
  git check-attr confirms the rules.
- Command/result record: local-reports/PHASE1_COMMAND_LOG.md. This local log is
  ignored so the actual commit result and post-commit checks can be recorded
  without modifying the committed source or publishing machine-specific logs.

The direct suite invokes validator callbacks explicitly, using independent
mocked web/model calls and closure-pickling checks. It does not exercise hosted
consensus, prove real token/disclosure semantics or demonstrate injection immunity.
The plugin prints its default localnet configuration, but these direct tests
operate in memory and send no localnet or StudioNet transactions.

## Specification concerns and residual risks

1. The listed precedence places insufficient coverage/any UNCLEAR before any
   CONTRADICTED. Thus a mixed UNCLEAR+CONTRADICTED review remains retriable
   UNVERIFIABLE, despite the broad statement that any contradiction is final.
   The implementation follows the explicit ordered rules and tests this
   case. Once BLOCKED is actually reached, disclosure cannot cure it.
2. Round two's rubric assesses specificity. It does not refetch the original
   capability evidence to establish the factual truth of an issuer's stated
   role holder or limits. Explicit but false statements could satisfy the
   stated rubric. The attestation records a consensus judgment about the
   fetched disclosure, not a guarantee that its claims are true.
3. issuer_address is a deployer-appointed responder. Account authorization
   does not prove that it is the real-world token issuer. The constructor does
   not require deployer and issuer addresses to differ.
4. The replay rule compares exact URL strings, as specified. Aliases/query
   variants may point to the same body and are not prevented. Mutable URLs may
   later change; the attestation preserves the digest of the accepted body.
5. The reused HTTPS helper checks URL syntax; it cannot prove DNS/public routing
   or publisher authority. Retrieved text remains untrusted. Prompts instruct
   validators to ignore instructions in it, but mocked tests do not prove
   prompt-injection resistance.
6. Live source selection, byte-for-byte identity of a new deployment, hosted
   finality/execution, both disclosure examples and distinctiveness review
   remain Phase 2/3 work. The new protocol has no fresh transaction receipts.

Phase 1 has no remaining failing local check. Approval is still required by the
supplied request before any push, fresh deployment or demo transaction.
