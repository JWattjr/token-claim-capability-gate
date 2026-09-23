# Test matrix: Token Claim-Capability Coherence Gate

| Scenario | Expected behavior | Test |
| --- | --- | --- |
| All claims hold | `CONSISTENT`; validator agrees | `test_all_claims_hold_is_consistent_and_terminal` |
| Repeat review after a final decision | Decision cannot flip; no new attempt recorded | `test_all_claims_hold_is_consistent_and_terminal` |
| Any contradicted claim | `BLOCKED`; contradicted and qualified claims named | `test_contradicted_claim_blocks_and_is_named` |
| Qualified claim, then disclosure published | `DISCLOSURE_REQUIRED`, stays retriable, then `CONSISTENT` | `test_qualified_claim_requires_disclosure_and_stays_retriable` |
| Any unclear claim | `UNVERIFIABLE` | `test_unclear_claim_is_unverifiable` |
| Omitted, invented, or invalid claim states | Normalized to frozen claim ids; invalid values become `UNCLEAR` | `test_missing_invented_and_invalid_claim_states_are_normalized` |
| All sources unavailable | LLM not called; `UNVERIFIABLE` with coverage 0 | `test_all_sources_unavailable_fails_closed` |
| Empty, oversized, or invalid UTF-8 HTTP 200 body | Does not count as coverage; `UNVERIFIABLE` | `test_empty_oversized_or_invalid_evidence_is_not_counted` (4 cases) |
| Leader keeps `BLOCKED` but blames a different claim | Validator rejects | `test_validator_rejects_forged_vector_with_same_decision` |
| Leader decision inconsistent with its own vector | Validator rejects | `test_validator_rejects_decision_inconsistent_with_vector` |
| Fewer complete sources than `min_sources` | `UNVERIFIABLE` without calling the LLM | `test_fewer_reachable_sources_than_min_sources_fails_closed` |
| `max_wait` passes on a retriable state | State frozen as final; later reviews change nothing | `test_max_wait_freezes_retriable_state` |
| `max_wait` passes with no review | `UNVERIFIABLE`, final | `test_max_wait_without_review_is_unverifiable` |
| Bad `min_sources` or `max_wait` | Constructor reverts | `test_constructor_rejects_bad_lifecycle` (4 cases) |
| Bad constructor input (claims, private/IPv6/ported/whitespace or duplicate URLs) | Constructor reverts | `test_constructor_rejections` (9 cases) |
| Finality | Listing actions wait for GenLayer finality | Consumer responsibility |
| Live StudioNet DAI example | Current source, byte-for-byte identity, one source, mixed vector, terminal `BLOCKED` after FINALIZED majority (3 AGREE, 2 DISAGREE) | `deployments/studionet-release-2026-09-23.json` |

The live example does not establish `QUALIFIED`, `UNVERIFIABLE`, retry/deadline,
or semantic prompt-injection behavior. Those paths have local direct-mode
coverage where listed above; mocked tests are not live validator proof.
