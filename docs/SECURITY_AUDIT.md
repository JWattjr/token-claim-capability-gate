# Security and consensus audit

Updated 2026-10-11 for source commit 34be6640d96627dca84e35bf985c60f0e4fa2657.
Scope: contracts/token_claim_capability_gate.py. Engineering review, not formal
verification, financial advice, or a guarantee of semantic correctness.

## Findings and implemented controls

| ID | Finding | Current control / evidence |
| --- | --- | --- |
| TC-01 | Status-only validation allowed unbound findings. | Independent whole canonical-result equality in both callbacks; storage revalidation. Every result field has behavioral mutation tests. |
| TC-02 | Model chose final status. | Deterministic precedence, derived agenda/claim lists/round decisions; inconsistent leader metadata rejected. |
| TC-03 | Invented/malformed references. | Exact claim maps, known unique powers, exact agenda pairs/root/row keys, strict integer coverage/round (not bool), digests and count validation. |
| TC-04 | Issuer controlled first judgment. | Permissionless review(); issuer-only submit_disclosure(), checked before fetch. |
| TC-05 | Unbounded inputs/retries. | Bounded constructor, 1–3 consumed rounds, UTC max_wait, <=9 history records; consumed entries never evicted. |
| TC-06 | Partial evidence implied confidence. | Only complete nonempty UTF-8 HTTP-200 <=15,000 raw bytes count. Below threshold all findings UNCLEAR without model calls. |
| TC-07 | Silent truncation. | Oversized evidence is unavailable, never prefix-classified. Full REN response measured 10,308 bytes. |
| TC-08 | Deployer context treated as proof. | Review prompt prefers evidence; source authenticity/configuration remains externally verified responsibility. |
| TC-09 | UNCLEAR masked contradiction. | With sufficient coverage, CONTRADICTED before UNCLEAR -> final BLOCKED; no disclosure cure. |
| TC-10 | Specific disclosure might contradict code. | Validators independently refetch frozen URLs; ADEQUATE requires specificity AND consistency. Live false-specific INADEQUATE; truthful ADEQUATE. |
| TC-11 | Forged second-round source metadata. | source_coverage/source_evidence_digest bound in both consensus and storage schemas. Same-verdict altered-digest test rejects. |
| TC-12 | Source outages exhausted issuer budget. | Available disclosure + below-threshold sources -> SOURCES_UNAVAILABLE, no round used, same URL retry before deadline. Unavailable disclosure consumes even if both fail. |
| TC-13 | Repeat URL rerolled verdict. | Exact consumed-URL replay rejected; all consumed records retained. Different URLs serving identical text remain possible. |
| TC-14 | Successful listing lacked bound justification. | Attestation binds claims digest, frozen agenda, URL/body digest, verdicts, round and source snapshot; original review result retained. |

## Consensus boundary

Review: exactly decision, claim_states, powers_per_claim, contradicted_claims,
qualified_claims, source_coverage, evidence_digest, agenda.
Disclosure: exactly decision, round, disclosure_url, disclosure_digest, available,
verdicts, source_coverage, source_evidence_digest.
Verdict rows: exactly claim_id, power, verdict. Missing/extra keys, invalid enums,
wrong types, malformed nested values, counts and inconsistent derived metadata
reject. Invalid wrappers/payloads reject. Closures capture ordinary snapshots,
not storage-backed values.

Each source snapshot digest covers id, URL, availability and full-body SHA-256.
Validators refetch rather than trust leader metadata. Frozen URLs are not frozen
bodies: round-two digests need not equal round one's; history preserves each
assessed snapshot.

## Lifecycle, failures and finality

max_wait is timezone-aware, UTC-normalized and strictly future at construction.
Deterministic message datetime drives boundaries. Eligible disclosures can submit
strictly before max_wait. At/after it writes reject and views project terminal
DISCLOSURE_REJECTED for an open agenda, otherwise unfinished review UNVERIFIABLE.
Completed terminal outcomes survive timeout. Time alone does not transact/mutate.

DNS-hosted HTTPS syntax rejects IP literals, explicit ports, local/internal names,
userinfo, backslashes and whitespace. Exceptions, non-200, empty/invalid UTF-8 or
oversized bodies fail closed. Syntax checks are not DNS/redirect isolation;
HTTPS does not prove authority.

Available disclosure + insufficient frozen sources -> all UNCLEAR, no attestation,
SOURCES_UNAVAILABLE, unchanged rounds_used. Unavailable disclosure ->
DISCLOSURE_UNAVAILABLE and consumed round, including simultaneous source outage.
History retains all consumed records and recent outages <=9 entries; only old
unconsumed attempts evict. Outage retries are time-bounded, not count-bounded.

Consumers must require protocol FINALIZED AND successful execution AND an allowed
terminal outcome. The contract cannot infer its own finality. No consumer listing,
funds custody, mint restriction or automatic asset protection is implemented.

## Current live proof

124 direct tests; lint/SDK schema passes. Deployment FINALIZED, leader SUCCESS,
5 AGREE. gen_getContractCode bytes exactly match committed blob: 28,471 bytes,
zero CR, no normalization. Review and three semantic disclosures finalized with
successful execution. Wrong-issuer and replay transactions finalized as leader
ERROR/rollback with whole state unchanged. RPC gave no human-readable revert
reason; individual guards also have direct behavioral tests. Truthful listing
had 3 AGREE / 2 DISAGREE, not unanimity.
[Full receipts/read-backs](../deployments/studionet-release-2026-10-11.json).

## Residual risks

- Source and issuer-written disclosure are untrusted text. Prompts mitigate
  embedded instructions, but mocked tests and one live case do not prove
  prompt-injection resistance or general semantic correctness.
- Exact equality binds judgments, not truth. A majority can agree incorrectly;
  the live false/true cases are not universal correctness evidence.
- Off-chain key custody and multisig membership cannot be verified from source
  code. Roles do not prove present holders, paused state, proxy configuration or
  real-world issuer identity. Demo issuer is a test account, not REN's issuer.
- Sourcify reports Match, not Exact Match. Complete files can lack imports/state;
  chosen REN record contains relevant source but present token state was not read.
- Source bodies may mutate between rounds; per-round digests need not equal the
  review digest. Changes during validator refetch can prevent agreement. Digests
  identify assessed text, not immutable truth or historical as-of boundaries.
- Exact-string replay permits different URLs with identical content, bounded by
  1–3 consumed rounds. Outage attempts can repeat until max_wait; only recent
  unconsumed history is retained, not a complete attempt archive.
- Attestation has no automatic revocation/expiry refresh for later token/external
  changes. Consumers must assess whether scope remains relevant and await finality.
- Deployer-selected claims/context can omit material issues; disclosure adequacy
  is not an investment-safety or solvency assessment.
- No live outage/deadline/all-power/consumer-execution proof; controlled fixtures
  exercise those specified paths. No downstream action has been demonstrated.

## Historical proof

Old WETH9/DAI manifests and phase-one reports are historical only. WETH9 read a
15,000-byte prefix of a 36.8 KB file; DAI identity used newline normalization.
Neither verifies this source or issuer-disclosure mechanism.
