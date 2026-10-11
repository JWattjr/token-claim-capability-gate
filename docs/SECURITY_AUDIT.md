# Security and consensus audit: Token Claim-Capability Coherence Gate

Audit updated: 2026-10-11 (local issuer-disclosure protocol; not yet deployed).
Scope: contracts/token_claim_capability_gate.py

This is an engineering audit, not formal verification, and not financial or legal advice.

## Remediated findings

| ID | Severity | Finding | Remediation |
| --- | --- | --- | --- |
| TC-01 | High | The validator compared only `decision`. `finding_codes` was written to state and exposed through `get_state()` unbound, so validators could agree to block a token while persisting different reasons. | The validator requires whole-result equality with its own independent evaluation. |
| TC-02 | High | The LLM chose the listing decision directly. | The LLM judges each frozen claim; deterministic code derives the decision and the named claim lists. |
| TC-03 | Medium | Finding codes were free-form labels, and an outage stored `SOURCES_UNAVAILABLE` as if it were a finding. | Results reference only frozen claim ids; outages are reported through `source_coverage`. |
| TC-04 | Medium | Review was owner-gated, so the party seeking a listing controlled when the gate spoke. | `review()` is permissionless over frozen inputs. |
| TC-06 | Medium | One reachable source out of six was enough to decide. | Frozen `min_sources`; fewer reachable sources fail closed to `UNVERIFIABLE` without calling the LLM. |
| TC-07 | Medium | Retriable states had no end, so a listing could be re-reviewed indefinitely. | Frozen `max_wait` deadline after which the current state is final; a never-reviewed token becomes `UNVERIFIABLE`. |
| TC-08 | Medium | A 6,000-character read cut real verified-source pages off before the relevant functions. | The current candidate rejects bodies over 15,000 bytes instead of silently deciding on a prefix. Choose bounded complete source files. |
| TC-09 | Low | The deployer-supplied capability context was trusted over the evidence. | The prompt instructs validators to trust evidence where the two conflict. |
| TC-05 | Low | Claim ids were not unique and claim text and sources were unbounded. | Unique 1-40 character ids, 1-300 character text, a bounded capability context, and unique public HTTPS sources. |
| TC-10 | High | An evidenced contradiction could be masked by another UNCLEAR claim. | With sufficient complete source coverage, CONTRADICTED takes priority and produces final BLOCKED. Below min_sources, no model judgment is attempted and all claims are UNCLEAR. |
| TC-11 | High | Round two checked specificity without checking the disclosure against source evidence. | Leader and validators independently refetch the frozen source URLs and judge specificity AND consistency. Claimed code-enforced limits contradicted by source are INADEQUATE. Below min_sources in round two, every pair is mechanically UNCLEAR and the round is consumed. This does not prove model judgments correct. |
| TC-12 | High | Round-two source metadata was not part of consensus. | Exact result keys include source_coverage and source_evidence_digest; coverage is a bounded strict integer (not bool), and digest is canonical lowercase SHA-256. Validators compare whole canonical results after independent refetch. Accepted results are revalidated before history/attestation persistence. |

## Controls

| Area | Control |
| --- | --- |
| Consensus | Both paths require whole canonical result equality with an independent validator evaluation; review binds states, powers, coverage and source snapshot digest; disclosure binds URL, body digest, availability, pair verdicts, round, source coverage and source snapshot digest. |
| Determinism | Review precedence: insufficient coverage -> UNVERIFIABLE; otherwise any CONTRADICTED -> BLOCKED; any UNCLEAR -> UNVERIFIABLE; any QUALIFIED -> DISCLOSURE_REQUIRED; else CONSISTENT. Disclosure decision derives from coverage, availability, bound verdicts and round limit. |
| Evidence | DNS-hosted HTTPS only; IP literals, explicit ports, local/internal names, userinfo, backslashes, and whitespace are rejected. A source counts only for a nonempty, complete UTF-8 body of at most 15,000 bytes. |
| Prompt safety | Sources and issuer disclosure are untrusted data; output references only frozen claim/power pairs. This bounds output shape, not semantic prompt-injection resistance. |
| Failure mode | Insufficient source coverage produces all UNCLEAR without a model call in either round. Review is UNVERIFIABLE; disclosure consumes a round, stays open or exhausts to DISCLOSURE_REJECTED, never lists. |
| Lifecycle | CONSISTENT, BLOCKED, LISTED_WITH_DISCLOSURE and DISCLOSURE_REJECTED are final. A frozen agenda locks review(); only the appointed issuer may submit bounded disclosure rounds before max_wait. At/after max_wait a view projects terminal DISCLOSURE_REJECTED for an open agenda, otherwise terminal UNVERIFIABLE. Time alone does not write storage. |
| Attestation | History and successful attestation preserve source coverage/digest for each accepted disclosure round, separately from the original review evidence_digest. Exact-string URL replay is rejected before consensus. |

## Residual risks

- Whole-result equality means genuinely ambiguous claims fail closed rather than list. This is deliberate.
- Once an agenda is frozen, review() cannot relitigate it. Before an agenda exists, UNVERIFIABLE can be re-reviewed until max_wait. Integrators must require terminal outcomes AND protocol finality before acting.
- Off-chain facts such as key custody and multisig membership cannot be verified from source code. A source may enforce a role without establishing who currently controls it. An attestation is a consensus judgment about fetched text and code, not proof of issuer identity, custody, actual deployment configuration, or safety.
- Source URL configuration is frozen, not source bodies. Round two refetches those URLs; it does not require its source digest to equal round one's. Mutable content may change between rounds, and changing content between leader and validator causes disagreement. Per-round digests preserve the evidence actually assessed.
- Code consistency remains a semantic model judgment. Complete byte coverage and exact validator agreement do not prove correct interpretation, factual truth, or prompt-injection resistance. Missing imports, proxy implementation/state, or deployment-specific access controls can leave a complete individual file insufficient; validators should return UNCLEAR when they cannot judge.
- Unavailable frozen sources consume an issuer round by the requested policy, even when the issuer does not control those sources. Outages can therefore exhaust the round budget to DISCLOSURE_REJECTED.
- The issuer address is deployer-appointed, not independently authenticated as the real issuer. Exact-string URL replay does not prevent different URLs serving the same disclosure body.
- HTTPS does not prove source authority; the deployer chooses official sources (a verified contract source page, the issuer's docs).
- URL syntax checks cannot prevent DNS rebinding or prove the fetched source matches the token address. An address-linked exact-match source must be verified separately.
- The historical WETH9 URL serves a 36.8 KB file; the deployed source used a 15,000-byte prefix. That live result is not a full-source review. The local candidate now rejects the oversized body.
- Mocked direct tests do not prove semantic prompt-injection resistance or independent live-validator correctness.
- Listing actions must wait for GenLayer finality.

## Historical deployment evidence (not this protocol)

- `deployments/studionet.json` records historical commit `0d41f253db60f9a0739a7a2915a27b478bc307f6`; `deployments/studionet-release-2026-09-23.json` records the preceding one-round contract at `db3d97dc84f06fb84b9ffb72a0f1d2ff676f0ceb`. Neither verifies the issuer-disclosure protocol or these fixes.
- That historical DAI StudioNet review finalized with 3 AGREE and 2 DISAGREE, terminal BLOCKED, and source coverage 1. It demonstrates one hypothetical two-claim case, not unanimity or prompt-injection resistance. Sourcify reported a Match, not an Exact Match.
- Historical deployed identity was checked after CRLF-to-LF normalization; raw SHA-256 hashes differ because the deployed file had 213 CRLF sequences while Git stored LF. Phase 2 must instead verify new deployed source against the committed blob byte-for-byte, without normalization.
- No new transactions, push, deployment or live semantic check were performed for the local follow-up fixes. Controlled false-specific/consistent fixtures assert both fetched bodies and the consistency rubric reach the real prompt, then return mocked verdicts. They do not prove an actual LLM can recognize the contradiction.
