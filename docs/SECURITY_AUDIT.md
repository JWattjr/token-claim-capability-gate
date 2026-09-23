# Security and consensus audit: Token Claim-Capability Coherence Gate

Audit updated: 2026-09-23
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

## Controls

| Area | Control |
| --- | --- |
| Consensus | Whole-result equality between the leader and an independent validator evaluation. |
| Determinism | The decision and claim lists are pure functions of the bound per-claim vector. |
| Evidence | DNS-hosted HTTPS only; IP literals, explicit ports, local/internal names, userinfo, backslashes, and whitespace are rejected. A source counts only for a nonempty, complete UTF-8 body of at most 15,000 bytes. |
| Prompt safety | Evidence is untrusted data; the model can only fill the frozen claim ids. This bounds output shape, not semantic prompt-injection resistance. |
| Failure mode | Uncertainty or outage becomes `UNVERIFIABLE`, never `CONSISTENT`. |
| Lifecycle | `CONSISTENT` and `BLOCKED` are final. `DISCLOSURE_REQUIRED` and `UNVERIFIABLE` are retriable so an issuer can publish a disclosure, until the frozen `max_wait` makes the current state final. |

## Residual risks

- Whole-result equality means genuinely ambiguous claims fail closed rather than list. This is deliberate.
- Because `DISCLOSURE_REQUIRED` is retriable until `max_wait`, a later review can reach `CONSISTENT` if the evidence at the frozen URLs changes. Integrators should act only when `terminal` is true.
- HTTPS does not prove source authority; the deployer chooses official sources (a verified contract source page, the issuer's docs).
- URL syntax checks cannot prevent DNS rebinding or prove the fetched source matches the token address. An address-linked exact-match source must be verified separately.
- The historical WETH9 URL serves a 36.8 KB file; the deployed source used a 15,000-byte prefix. That live result is not a full-source review. The local candidate now rejects the oversized body.
- Mocked direct tests do not prove semantic prompt-injection resistance or independent live-validator correctness.
- Listing actions must wait for GenLayer finality.
- `deployments/studionet.json` records historical commit `0d41f253db60f9a0739a7a2915a27b478bc307f6`. Current live evidence is in `deployments/studionet-release-2026-09-23.json` for commit `db3d97dc84f06fb84b9ffb72a0f1d2ff676f0ceb`.
- The current DAI StudioNet review finalized with 3 AGREE and 2 DISAGREE, terminal `BLOCKED`, and source coverage 1. This demonstrates one hypothetical two-claim case, not unanimous validator execution or semantic prompt-injection resistance. Sourcify reports a Match, not an Exact Match.
