# Phase 1 specification-fix results

Historical checkpoint at local commit 2d319151e117af099b2d826e189cc4c34f30ff80.
Its test count, source hashes, outage-budget policy and unapproved Phase 2
statements describe that checkpoint only. The current release manifest/audit
supersede them: available-disclosure source outages now preserve rounds and
fresh finalized protocol evidence exists.

Date: 2026-10-11. Local follow-up to commit `4ab487e`; no push or deployment.

## Changes

- Review precedence: insufficient complete source coverage -> UNVERIFIABLE;
  otherwise CONTRADICTED -> final BLOCKED; UNCLEAR -> UNVERIFIABLE;
  QUALIFIED -> DISCLOSURE_REQUIRED; else CONSISTENT.
- Both rounds reuse complete, nonempty UTF-8 HTTP-200 evidence fetching capped
  at 15,000 raw bytes. Round two independently refetches frozen source URLs
  as well as the disclosure, and supplies both to the real consistency prompt.
- ADEQUATE requires specificity AND no contradiction with fetched source
  evidence. Claimed code-enforced time/multisig limits absent from code are
  INADEQUATE under the rubric. Insufficient source coverage mechanically
  forces every pair to UNCLEAR, skips the model and consumes a round.
- Round-two result, history and successful attestation bind source_coverage
  and source_evidence_digest. Strict canonicalization validates them, whole
  result equality compares them, and storage revalidation checks them again.
- Public methods and constructor are unchanged. The pinned runner is unchanged.
- SECURITY_AUDIT now documents these controls, off-chain facts, source mutation,
  and the limits of mocked semantic tests. The old Phase 1 review is explicitly
  a historical checkpoint, not a current-source verification report.

## Verification

Command: `python -X utf8 -m genvm_linter.cli check contracts/token_claim_capability_gate.py --json`

Result: PASS; 3 lint checks, SDK validation of 8 constructor parameters,
2 write methods and 1 view. Warning I200 reports a newer runner; the requested
runner was retained. SDK validation needed access to the existing local SDK cache.

Command: `python -X utf8 -m pytest tests -vv --tb=short`

Result: **122 passed, 0 failed, 0 skipped** in 9.50 seconds (previous checkpoint: 102).
The full per-case list is below. The existing below-min_sources regression is
preserved. The mixed CONTRADICTED/UNCLEAR regression now proves final BLOCKED.

Contract Git blob: `ea81ede30c3b20dc00e52dbe8a17dfbd987d33c0`.
Contract SHA-256: `41a3441add84834d64d01aadd72de38db1bc02ca35e7446165ee4b94e4919e52`.
Contract: 27,155 bytes, LF-only (zero CR bytes). `git diff --check` passed.
Command/results are recorded locally in ignored `local-reports/SPEC_FIX_COMMAND_LOG.md`.

## Limits and Phase 2 conditions

- Off-chain key custody, multisig membership, current role holders and actual
  deployment/proxy configuration cannot be established from token source alone.
  The attestation is not proof of those facts or issuer identity.
- Frozen inputs are URLs, not immutable bodies. Round two's digest need not
  equal round one's; each round preserves its assessed-source digest. Body
  changes between leader and validator cause disagreement even with same verdicts.
- Source outages consume the issuer's disclosure budget, as explicitly requested,
  even for sources outside issuer control. They can cause terminal rejection.
- Code interpretation is still a model judgment. Controlled false/consistent
  fixtures require both fetched bodies and the consistency rubric in the actual
  prompt before returning mocked verdicts. They do not prove real LLM correctness
  or prompt-injection resistance. Validator callbacks are explicitly exercised;
  hosted consensus is not run. Direct tests are in-memory despite the plugin
  printing its configured default localnet URL; no network transactions occurred.
- Phase 2 remains unapproved. Before writing pause.md, inspect the selected token's
  actual source and describe its real role, pause behavior and limits truthfully.
  vague.md remains vague. A third false-specific live example is optional and
  must be clearly labeled a controlled hypothetical disclosure.
- Old receipts do not verify this source. No fresh receipt or live semantic
  evidence is claimed here; no push, deployment, appeal or Portal submission.

## Full test list

~~~text
tests/test_disclosure_protocol.py::test_qualified_agenda_is_sorted_by_claim_and_power PASSED [  0%]
tests/test_disclosure_protocol.py::test_review_remains_permissionless_and_unverifiable_can_retry PASSED [  1%]
tests/test_disclosure_protocol.py::test_contradiction_precedes_unclear_with_sufficient_coverage_and_is_final PASSED [  2%]
tests/test_disclosure_protocol.py::test_insufficient_coverage_cannot_judge_contradiction PASSED [  3%]
tests/test_disclosure_protocol.py::test_nonissuer_disclosure_reverts_before_fetch_and_preserves_state PASSED [  4%]
tests/test_disclosure_protocol.py::test_vague_disclosure_uses_round_and_preserves_original_agenda PASSED [  4%]
tests/test_disclosure_protocol.py::test_reused_disclosure_url_reverts_before_consensus PASSED [  5%]
tests/test_disclosure_protocol.py::test_specific_disclosure_lists_with_exact_attestation_and_retained_history PASSED [  6%]
tests/test_disclosure_protocol.py::test_pause_disclosure_cannot_blanket_satisfy_mint_pair PASSED [  7%]
tests/test_disclosure_protocol.py::test_specific_but_source_inconsistent_disclosure_is_inadequate[unenforced-time-limit] PASSED [  8%]
tests/test_disclosure_protocol.py::test_specific_but_source_inconsistent_disclosure_is_inadequate[unenforced-multisig] PASSED [  9%]
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_and_use_round[non-200] PASSED [  9%]
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_and_use_round[empty] PASSED [ 10%]
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_and_use_round[oversized] PASSED [ 11%]
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_and_use_round[invalid-utf8] PASSED [ 12%]
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_and_use_round[transport] PASSED [ 13%]
tests/test_disclosure_protocol.py::test_round2_partial_frozen_sources_below_threshold_use_last_round PASSED [ 13%]
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[1] PASSED [ 14%]
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[2] PASSED [ 15%]
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[3] PASSED [ 16%]
tests/test_disclosure_protocol.py::test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds[at-deadline] PASSED [ 17%]
tests/test_disclosure_protocol.py::test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds[after-deadline] PASSED [ 18%]
tests/test_disclosure_protocol.py::test_disclosure_before_deadline_can_complete PASSED [ 18%]
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[empty] PASSED [ 19%]
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[whitespace] PASSED [ 20%]
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[oversized] PASSED [ 21%]
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[invalid-utf8] PASSED [ 22%]
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[non-200] PASSED [ 22%]
tests/test_disclosure_protocol.py::test_disclosure_transport_failure_consumes_last_round PASSED [ 23%]
tests/test_disclosure_protocol.py::test_disclosure_cap_counts_raw_utf8_bytes[15000-bytes] PASSED [ 24%]
tests/test_disclosure_protocol.py::test_disclosure_cap_counts_raw_utf8_bytes[15002-bytes] PASSED [ 25%]
tests/test_disclosure_protocol.py::test_contradicted_is_final_and_cannot_be_cured_by_disclosure PASSED [ 26%]
tests/test_disclosure_protocol.py::test_consistent_or_pending_cannot_accept_disclosures PASSED [ 27%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[http://example.org/x] PASSED [ 27%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://127.0.0.1/x] PASSED [ 28%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://service.internal/x] PASSED [ 29%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://user@example.org/x] PASSED [ 30%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://example.org:443/x] PASSED [ 31%]
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://example.org /x] PASSED [ 31%]
tests/test_disclosure_protocol.py::test_round1_same_states_but_forged_power_is_rejected PASSED [ 32%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[decision] PASSED [ 33%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[claim_states] PASSED [ 34%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[powers_per_claim] PASSED [ 35%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[contradicted_claims] PASSED [ 36%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[qualified_claims] PASSED [ 36%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[source_coverage] PASSED [ 37%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[evidence_digest] PASSED [ 38%]
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[agenda] PASSED [ 39%]
tests/test_disclosure_protocol.py::test_round1_validator_refetches_and_binds_complete_body_digest PASSED [ 40%]
tests/test_disclosure_protocol.py::test_round2_same_decision_but_forged_per_pair_verdict_is_rejected PASSED [ 40%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[decision] PASSED [ 41%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[round] PASSED [ 42%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[disclosure_url] PASSED [ 43%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[disclosure_digest] PASSED [ 44%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[available] PASSED [ 45%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[verdicts] PASSED [ 45%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[source_coverage] PASSED [ 46%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[source_evidence_digest] PASSED [ 47%]
tests/test_disclosure_protocol.py::test_round2_validator_refetches_same_url_and_rejects_changed_body PASSED [ 48%]
tests/test_disclosure_protocol.py::test_round2_same_verdicts_but_forged_source_evidence_digest_is_rejected PASSED [ 49%]
tests/test_disclosure_protocol.py::test_round2_validator_independently_refetches_frozen_source_bodies PASSED [ 50%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[negative-coverage] PASSED [ 50%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[excessive-coverage] PASSED [ 51%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[string-coverage] PASSED [ 52%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[empty-digest] PASSED [ 53%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[nested-digest] PASSED [ 54%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[nonhex-digest] PASSED [ 54%]
tests/test_disclosure_protocol.py::test_round2_validator_rejects_adequate_verdicts_with_insufficient_coverage PASSED [ 55%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[unknown] PASSED [ 56%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[duplicate] PASSED [ 57%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[empty-qualified] PASSED [ 58%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[powers-for-holds] PASSED [ 59%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[string-powers] PASSED [ 59%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[nested-powers] PASSED [ 60%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[invalid-state] PASSED [ 61%]
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[extra-key] PASSED [ 62%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[missing] PASSED [ 63%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[duplicate] PASSED [ 63%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[invented-claim] PASSED [ 64%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[unknown-power] PASSED [ 65%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[bad-verdict] PASSED [ 66%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[extra-row-key] PASSED [ 67%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[extra-root-key] PASSED [ 68%]
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[malformed] PASSED [ 68%]
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[0] PASSED [ 69%]
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[4] PASSED [ 70%]
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[True] PASSED [ 71%]
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[2] PASSED [ 72%]
tests/test_disclosure_protocol.py::test_constructor_rejects_boolean_min_sources PASSED [ 72%]
tests/test_disclosure_protocol.py::test_constructor_rejects_zero_issuer PASSED [ 73%]
tests/test_disclosure_protocol.py::test_both_consensus_paths_pickle_only_ordinary_snapshots PASSED [ 74%]
tests/test_disclosure_protocol.py::test_consensus_rejects_extra_leader_fields_and_malformed_payload[1] PASSED [ 75%]
tests/test_disclosure_protocol.py::test_consensus_rejects_extra_leader_fields_and_malformed_payload[2] PASSED [ 76%]
tests/test_disclosure_protocol.py::test_ast_every_leader_result_field_is_compared_in_both_paths PASSED [ 77%]
tests/test_gate.py::test_all_claims_hold_is_consistent_and_terminal PASSED [ 77%]
tests/test_gate.py::test_contradicted_claim_blocks_and_is_named PASSED   [ 78%]
tests/test_gate.py::test_qualified_claim_freezes_agenda_and_prevents_rereview PASSED [ 79%]
tests/test_gate.py::test_unclear_claim_is_unverifiable PASSED            [ 80%]
tests/test_gate.py::test_missing_invented_and_invalid_claim_states_are_rejected PASSED [ 81%]
tests/test_gate.py::test_all_sources_unavailable_fails_closed PASSED     [ 81%]
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[empty] PASSED [ 82%]
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[whitespace] PASSED [ 83%]
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[oversized] PASSED [ 84%]
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[invalid-utf8] PASSED [ 85%]
tests/test_gate.py::test_validator_rejects_forged_vector_with_same_decision PASSED [ 86%]
tests/test_gate.py::test_validator_rejects_decision_inconsistent_with_vector PASSED [ 86%]
tests/test_gate.py::test_fewer_reachable_sources_than_min_sources_fails_closed PASSED [ 87%]
tests/test_gate.py::test_max_wait_rejects_disclosure_required_state PASSED [ 88%]
tests/test_gate.py::test_max_wait_without_review_is_unverifiable PASSED  [ 89%]
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[0-2099-01-01T00:00:00Z-min_sources] PASSED [ 90%]
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[2-2099-01-01T00:00:00Z-min_sources] PASSED [ 90%]
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[1-2000-01-01T00:00:00Z-future] PASSED [ 91%]
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[1-2099-01-01T00:00:00-timezone] PASSED [ 92%]
tests/test_gate.py::test_constructor_rejections[claims0-urls0-1-12] PASSED [ 93%]
tests/test_gate.py::test_constructor_rejections[claims1-urls1-unique] PASSED [ 94%]
tests/test_gate.py::test_constructor_rejections[claims2-urls2-text] PASSED [ 95%]
tests/test_gate.py::test_constructor_rejections[claims3-urls3-publicly reachable] PASSED [ 95%]
tests/test_gate.py::test_constructor_rejections[claims4-urls4-publicly reachable] PASSED [ 96%]
tests/test_gate.py::test_constructor_rejections[claims5-urls5-invalid] PASSED [ 97%]
tests/test_gate.py::test_constructor_rejections[claims6-urls6-invalid] PASSED [ 98%]
tests/test_gate.py::test_constructor_rejections[claims7-urls7-invalid] PASSED [ 99%]
tests/test_gate.py::test_constructor_rejections[claims8-urls8-unique] PASSED [100%]
~~~
