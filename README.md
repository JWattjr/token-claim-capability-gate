# Token Claim-Capability Coherence Gate

A reusable GenLayer issuer disclosure-and-attestation primitive. It holds no funds,
executes no listing and imposes no token restrictions. Permissionless review
compares frozen claims with source code. Qualified claims freeze a power-specific
agenda; only an appointed issuer can answer it. A second, different judgment
checks disclosure specificity AND source consistency and produces an attestation.

## Frozen specification

Eight constructor inputs: token_id, manifest_json, capability_context_json,
source_urls_json, min_sources, max_wait_iso, issuer_address, max_disclosure_rounds.
Bounds: 1–12 unique claims, ids 1–40 characters, texts 1–300, token id 1–120,
context JSON at most 4,000 characters, 1–6 unique HTTPS URLs <=500 characters,
and 1–3 consumed rounds. Timezone-aware deadlines normalize UTC; deterministic
message datetime drives comparisons. The issuer is appointed, not authenticated.

Power taxonomy: MINT, PAUSE, FREEZE, BLACKLIST, UPGRADE, FEE_CHANGE,
OWNERSHIP_TRANSFER. QUALIFIED requires nonempty unique known powers; other
claim states require no powers. Invented/missing ids and malformed values reject,
not silently normalize. First-review precedence:

1. Below min_sources complete sources -> UNVERIFIABLE; all claims UNCLEAR.
2. Any CONTRADICTED -> final BLOCKED, even if another claim is UNCLEAR.
3. Any UNCLEAR -> UNVERIFIABLE.
4. Any QUALIFIED -> DISCLOSURE_REQUIRED and freeze sorted (claim_id, power) agenda.
5. Otherwise -> final CONSISTENT.

CONTRADICTED is an explicit denial of an evidenced power; silence can qualify a
substantially true claim. BLOCKED cannot be cured. UNVERIFIABLE can retry before
max_wait, but an existing agenda locks review().

## Issuer response and lifecycle

submit_disclosure(disclosure_url) requires issuer authorization, an open agenda,
remaining round budget, an unused consumed-round URL and time strictly before
max_wait. ADEQUATE names each power, its holder/role and conditions/limits
(including explicit absence), and contradicts nothing in refetched source code.
Specific but code-false assurances are INADEQUATE. Each pair is judged separately.

All ADEQUATE -> terminal LISTED_WITH_DISCLOSURE. Otherwise a consumed round stays
DISCLOSURE_REQUIRED, or becomes terminal DISCLOSURE_REJECTED at exhaustion.
Attestation binds token id, claims digest, agenda, disclosure URL/body digest,
round, pair verdicts, source coverage and source evidence digest.

Complete evidence requires nonempty HTTP-200 UTF-8 <=15,000 raw bytes. Oversized
bodies reject, never truncate. Transport/status/decoding/empty failures do not
count. Both consensus paths independently fetch, canonicalize, compare every
result field exactly and revalidate before persistence. Evidence and disclosure
instructions are untrusted; these checks do not guarantee semantic correctness
or prompt-injection resistance.

Available disclosure + too few frozen sources -> all UNCLEAR, SOURCES_UNAVAILABLE
history, no round used; same URL may retry before max_wait. Unavailable disclosure
uses a round even if sources also fail, with DISCLOSURE_UNAVAILABLE history.
History retains all consumed rounds plus recent outage attempts, at most 9;
only old unconsumed attempts may be evicted. Consumed URL replay remains blocked.

At/after max_wait, unfinished agendas project terminal DISCLOSURE_REJECTED;
other unfinished reviews project terminal UNVERIFIABLE. Completed terminal results
persist. Time alone neither sends a transaction nor changes storage. Consumers
must require protocol FINALIZED, successful execution and allowed terminal status;
terminal is not protocol finality.

## Verified StudioNet release: 2026-10-11

[Manifest](deployments/studionet-release-2026-10-11.json) records eight arguments,
seven receipts, every latest-final read-back, votes, runner and toolchain.
Deployed source equals Git blob at
`34be6640d96627dca84e35bf985c60f0e4fa2657` byte-for-byte without normalization.
[Contract](https://explorer-studio.genlayer.com/address/0x6Ba50deF22213cbB020b66f88D4Bf1e0f7dbff2E).

Evidence is real address-linked REN Sourcify source, 10,308 complete raw bytes,
Match not Exact Match. The transfer claim and all disclosures are controlled
hypothetical examples, not REN issuer statements. Appointed issuer is a test
account. Truthful pause.md names actual owner/onlyOwner, pause()/unpause(),
whenNotPaused and ungated burn()/transferTokens() exceptions, without custody claims.

| Step | FINALIZED leader execution | Read-back | AGREE / DISAGREE / IDLE |
| --- | --- | --- | --- |
| Deploy | SUCCESS | PENDING | 5 / 0 / 0 |
| review | SUCCESS | DISCLOSURE_REQUIRED; holder_transfer/PAUSE | 3 / 0 / 2 |
| Wrong issuer | Expected ERROR/rollback | Entire state unchanged | 5 / 0 / 0 |
| vague.md | SUCCESS | INADEQUATE; round 1 | 3 / 0 / 2 |
| pause-false.md | SUCCESS | INADEQUATE; round 2 | 3 / 1 / 1 |
| Replay vague URL | Expected ERROR/rollback | Entire state unchanged | 3 / 0 / 2 |
| pause.md | SUCCESS | LISTED_WITH_DISCLOSURE; attestation; round 3 | 3 / 2 / 0 |

Majority is not unanimity. This live case does not establish every outage, deadline,
power, interpretation or injection path.

## Checks and submission package

```powershell
python -X utf8 -m pytest tests -vv --tb=short
python -X utf8 -m genvm_linter.cli check contracts/token_claim_capability_gate.py --json
```

124 passed; none failed/skipped. Lint/SDK schema passed: 8 constructor parameters,
2 writes and 1 view. Warning I200 notes a newer runner; pinned 1jb45 retained.

- [Test matrix](docs/TEST_MATRIX.md) and [audit](docs/SECURITY_AUDIT.md).
- [Release verification](docs/RELEASE_VERIFICATION.md) and [constructor](docs/STUDIONET_RELEASE_CANDIDATE.md).
- [Distinctiveness](DISTINCTIVENESS.md), [Portal package](PORTAL_SUBMISSION.md), [appeal draft](APPEAL.md).

Old WETH9 deployments/studionet.json and one-round DAI
deployments/studionet-release-2026-09-23.json are historical. Neither verifies
this protocol. Old phase-one reports preserve checkpoint counts/policies only.
No Portal or appeal submission was made.
