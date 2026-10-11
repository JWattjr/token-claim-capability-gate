# Test matrix: current issuer-disclosure protocol

Verified 2026-10-11: **124 passed, 0 failed, 0 skipped** in 9.79s.
Source: 34be6640d96627dca84e35bf985c60f0e4fa2657.

Direct mode runs real contract methods with controlled web/model fixtures and
explicitly invokes the actual validator callbacks. Semantic responses are mocked:
false/specific cases assert both fetched bodies and the consistency rubric reach
the real prompt, not that a live model is always correct. The AST test is only a
supplement to behavioral mutations; it is not the consensus proof.

One row per test function (all parameterized cases pass). Names in test_disclosure_protocol.py
are the new protocol/follow-up regressions; test_gate.py retains/updates the base cases.

| Test | File | Cases | Expected invariant / result |
| --- | --- | ---: | --- |
| `test_qualified_agenda_is_sorted_by_claim_and_power` | test_disclosure_protocol.py | 1 | Canonical claim/power sorting; freezes exact agenda. |
| `test_review_remains_permissionless_and_unverifiable_can_retry` | test_disclosure_protocol.py | 1 | Any sender reviews; insufficient coverage may recover before an agenda. |
| `test_contradiction_precedes_unclear_with_sufficient_coverage_and_is_final` | test_disclosure_protocol.py | 1 | Sufficient coverage: contradiction beats UNCLEAR, remains BLOCKED, disclosure rejected. |
| `test_insufficient_coverage_cannot_judge_contradiction` | test_disclosure_protocol.py | 1 | Below threshold: all UNCLEAR, no evidenced contradiction judgment. |
| `test_nonissuer_disclosure_reverts_before_fetch_and_preserves_state` | test_disclosure_protocol.py | 1 | Non-issuer rejects before web/model and preserves whole state. |
| `test_vague_disclosure_uses_round_and_preserves_original_agenda` | test_disclosure_protocol.py | 1 | Vague mocked verdict uses one round; original review/agenda retained. |
| `test_reused_disclosure_url_reverts_before_consensus` | test_disclosure_protocol.py | 1 | Consumed URL replay rejects before consensus; state unchanged. |
| `test_specific_disclosure_lists_with_exact_attestation_and_retained_history` | test_disclosure_protocol.py | 1 | Specific consistent controlled disclosure lists; exact attestation/history; terminal survives deadline. |
| `test_pause_disclosure_cannot_blanket_satisfy_mint_pair` | test_disclosure_protocol.py | 1 | PAUSE adequacy cannot satisfy separate MINT pair. |
| `test_specific_but_source_inconsistent_disclosure_is_inadequate` | test_disclosure_protocol.py | 2 | Actual prompt includes fetched source and false time/multisig rubric; controlled verdict INADEQUATE. |
| `test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round` | test_disclosure_protocol.py | 5 | Five source failures: available disclosure, all UNCLEAR, SOURCES_UNAVAILABLE, rounds unchanged. |
| `test_round2_partial_frozen_sources_below_threshold_preserve_last_round` | test_disclosure_protocol.py | 1 | Partial source coverage below minimum preserves last available round. |
| `test_source_outage_can_retry_same_url_when_sources_recover` | test_disclosure_protocol.py | 1 | Unconsumed outage URL can retry and list after recovery. |
| `test_source_outage_history_is_bounded_and_preserves_consumed_url_replay` | test_disclosure_protocol.py | 1 | Repeated outages cap history at 9, preserve consumed replay entries and deadline guard. |
| `test_rounds_exhaustion_is_terminal_and_history_is_bounded` | test_disclosure_protocol.py | 3 | Round limits 1/2/3 exhaust to final rejection with retained history. |
| `test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds` | test_disclosure_protocol.py | 2 | At and after deadline: reject late submissions, preserve round counter. |
| `test_disclosure_before_deadline_can_complete` | test_disclosure_protocol.py | 1 | Submission strictly before deadline can complete. |
| `test_unavailable_disclosure_counts_round_and_never_becomes_adequate` | test_disclosure_protocol.py | 5 | Five disclosure failures consume a round and cannot become ADEQUATE. |
| `test_disclosure_transport_failure_consumes_last_round` | test_disclosure_protocol.py | 1 | Unavailable disclosure and source transport consume last round; final rejection. |
| `test_disclosure_cap_counts_raw_utf8_bytes` | test_disclosure_protocol.py | 2 | 15,000-byte complete UTF-8 accepted; 15,002-byte unavailable. |
| `test_contradicted_is_final_and_cannot_be_cured_by_disclosure` | test_disclosure_protocol.py | 1 | Final contradiction cannot be cured by disclosure. |
| `test_consistent_or_pending_cannot_accept_disclosures` | test_disclosure_protocol.py | 1 | Pending and final consistent states reject disclosures. |
| `test_invalid_disclosure_url_reverts_without_using_round` | test_disclosure_protocol.py | 6 | Invalid/private/ported/whitespace disclosure URLs reject without round use. |
| `test_round1_same_states_but_forged_power_is_rejected` | test_disclosure_protocol.py | 1 | Same states with forged power: actual validator rejects. |
| `test_round1_validator_rejects_mutation_of_every_result_field` | test_disclosure_protocol.py | 8 | Mutating any of eight review result fields: validator rejects. |
| `test_round1_validator_refetches_and_binds_complete_body_digest` | test_disclosure_protocol.py | 1 | Review validator refetches and binds full source-body digest. |
| `test_round2_same_decision_but_forged_per_pair_verdict_is_rejected` | test_disclosure_protocol.py | 1 | Same derived status with forged pair verdict: validator rejects. |
| `test_round2_validator_rejects_mutation_of_every_result_field` | test_disclosure_protocol.py | 8 | Mutating any of eight disclosure result fields: validator rejects. |
| `test_round2_validator_refetches_same_url_and_rejects_changed_body` | test_disclosure_protocol.py | 1 | Disclosure body changed at same URL: validator rejects. |
| `test_round2_same_verdicts_but_forged_source_evidence_digest_is_rejected` | test_disclosure_protocol.py | 1 | Same verdicts with forged frozen-source evidence digest: validator rejects. |
| `test_round2_validator_independently_refetches_frozen_source_bodies` | test_disclosure_protocol.py | 1 | Validator independently refetches frozen source bodies; changed source rejects. |
| `test_round2_validator_rejects_malformed_source_binding` | test_disclosure_protocol.py | 6 | Negative/excess/string coverage and malformed source digests reject. |
| `test_round2_validator_rejects_adequate_verdicts_with_insufficient_coverage` | test_disclosure_protocol.py | 1 | Forged ADEQUATE below min_sources rejects. |
| `test_round1_malformed_or_unknown_powers_revert_before_storage` | test_disclosure_protocol.py | 8 | Unknown/duplicate/malformed powers or claim state/maps reject before storage. |
| `test_round2_malformed_verdicts_revert_before_using_round` | test_disclosure_protocol.py | 8 | Missing/duplicate/invented pair, invalid enum or extra keys reject without round use. |
| `test_constructor_requires_integer_disclosure_round_bound` | test_disclosure_protocol.py | 4 | 0/4/bool/string round bound rejected. |
| `test_constructor_rejects_boolean_min_sources` | test_disclosure_protocol.py | 1 | Boolean min_sources rejected. |
| `test_constructor_rejects_zero_issuer` | test_disclosure_protocol.py | 1 | Zero issuer rejected. |
| `test_both_consensus_paths_pickle_only_ordinary_snapshots` | test_disclosure_protocol.py | 1 | Both nondeterministic closures pickle ordinary snapshots only. |
| `test_consensus_rejects_extra_leader_fields_and_malformed_payload` | test_disclosure_protocol.py | 2 | Extra leader fields/malformed payload reject in both callbacks. |
| `test_ast_every_leader_result_field_is_compared_in_both_paths` | test_disclosure_protocol.py | 1 | Supplementary AST check: both callbacks canonicalize whole results and equality. |
| `test_all_claims_hold_is_consistent_and_terminal` | test_gate.py | 1 | All HOLDS -> final CONSISTENT; terminal replay cannot flip it. |
| `test_contradicted_claim_blocks_and_is_named` | test_gate.py | 1 | Contradiction -> BLOCKED with exact named claims. |
| `test_qualified_claim_freezes_agenda_and_prevents_rereview` | test_gate.py | 1 | QUALIFIED freezes agenda and blocks re-review. |
| `test_unclear_claim_is_unverifiable` | test_gate.py | 1 | UNCLEAR -> retriable UNVERIFIABLE. |
| `test_missing_invented_and_invalid_claim_states_are_rejected` | test_gate.py | 1 | Missing/invented/invalid claim states reject, not normalize. |
| `test_all_sources_unavailable_fails_closed` | test_gate.py | 1 | All sources unavailable -> UNVERIFIABLE without model judgment. |
| `test_empty_oversized_or_invalid_evidence_is_not_counted` | test_gate.py | 4 | Empty/whitespace/oversized/invalid UTF-8 source does not count. |
| `test_validator_rejects_forged_vector_with_same_decision` | test_gate.py | 1 | Same decision with forged claim vector: validator rejects. |
| `test_validator_rejects_decision_inconsistent_with_vector` | test_gate.py | 1 | Decision inconsistent with vector: validator rejects. |
| `test_fewer_reachable_sources_than_min_sources_fails_closed` | test_gate.py | 1 | Below min_sources complete -> all UNCLEAR, no model call. |
| `test_max_wait_rejects_disclosure_required_state` | test_gate.py | 1 | Timeout open agenda -> terminal DISCLOSURE_REJECTED; no cure. |
| `test_max_wait_without_review_is_unverifiable` | test_gate.py | 1 | Never-reviewed timeout -> terminal UNVERIFIABLE. |
| `test_constructor_rejects_bad_lifecycle` | test_gate.py | 4 | Invalid coverage/deadline and timezone-naive constructor values reject. |
| `test_constructor_rejections` | test_gate.py | 9 | Empty/duplicate/malformed claims or unsafe/duplicate URLs reject. |

## Live evidence (separate from mocks)

[Current manifest](../deployments/studionet-release-2026-10-11.json) records exact
source identity, deployment and six demo transactions with every finalized read-back.
Review freezes holder_transfer/PAUSE; vague and source-false disclosures both
INADEQUATE; truthfully specific disclosure ADEQUATE and LISTED_WITH_DISCLOSURE
with attestation. Wrong issuer and replay both ERROR/rollback, state unchanged.
All protocol FINALIZED; successful steps have leader SUCCESS. Majority votes,
not unanimity: final listing 3 AGREE / 2 DISAGREE.

No live outage, timeout, multiple-power, malformed-leader or downstream consumer
execution demonstration was performed. Local checks do not prove prompt-injection
immunity, current token custody/state or universal interpretation correctness.
Old DAI/WETH9 and phase-one test reports are historical, not current-source proof.

Lint and SDK schema pass: 3 lint checks, 8 constructor parameters, 2 writes, 1 view.
Warning I200 reports a newer runner; requested pinned runner retained.
