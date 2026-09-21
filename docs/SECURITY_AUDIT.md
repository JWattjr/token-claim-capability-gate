# Security and consensus audit: Token Claim-Capability Coherence Gate

Audit date: 2026-09-21
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
| TC-08 | Medium | A 6,000-character read cut real verified-source pages off before the relevant functions. | 15,000 characters per source; the README directs deployers to raw source files. |
| TC-09 | Low | The deployer-supplied capability context was trusted over the evidence. | The prompt instructs validators to trust evidence where the two conflict. |
| TC-05 | Low | Claim ids were not unique and claim text and sources were unbounded. | Unique 1-40 character ids, 1-300 character text, a bounded capability context, and unique public HTTPS sources. |

## Controls

| Area | Control |
| --- | --- |
| Consensus | Whole-result equality between the leader and an independent validator evaluation. |
| Determinism | The decision and claim lists are pure functions of the bound per-claim vector. |
| Evidence | HTTPS only. Rejects localhost, internal domains, non-public IPv4 ranges, userinfo, and backslashes. Bounded body size. |
| Prompt safety | Evidence is untrusted data; the model can only fill the frozen claim ids. |
| Failure mode | Uncertainty or outage becomes `UNVERIFIABLE`, never `CONSISTENT`. |
| Lifecycle | `CONSISTENT` and `BLOCKED` are final. `DISCLOSURE_REQUIRED` and `UNVERIFIABLE` are retriable so an issuer can publish a disclosure, until the frozen `max_wait` makes the current state final. |

## Residual risks

- Whole-result equality means genuinely ambiguous claims fail closed rather than list. This is deliberate.
- Because `DISCLOSURE_REQUIRED` is retriable until `max_wait`, a later review can reach `CONSISTENT` if the evidence at the frozen URLs changes. Integrators should act only when `terminal` is true.
- HTTPS does not prove source authority; the deployer chooses official sources (a verified contract source page, the issuer's docs).
- Listing actions must wait for GenLayer finality.
