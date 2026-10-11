# Release verification: 2026-10-11

## Reviewed source and checks

Source/disclosure commit: 34be6640d96627dca84e35bf985c60f0e4fa2657.
Git blob: 75c644e39b0ff68b8a648a0eaeb5868d5b72a70d.
Raw source SHA-256: 61262d820cecb622388c551bdbc885b5039a45eb4aed90eb877ec87e1a9a90da.
Runner: py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6.
Contract: 0x6Ba50deF22213cbB020b66f88D4Bf1e0f7dbff2E; StudioNet chain 61999 only.
All eight constructor receipt arguments equal the deployment configuration.
gen_getContractCode bytes equal git cat-file blob without normalization:
28,471 bytes, zero CR.
[Full manifest](../deployments/studionet-release-2026-10-11.json).

Step 0 commit: d344ca9fb98bddc63e3c1516aa334ad8ed110b88.
Available disclosure plus source outage preserves rounds and records
SOURCES_UNAVAILABLE; unconsumed URL can retry. Unavailable disclosure consumes
even when both fail. History <=9; all consumed records retained.

Full suite: 124 passed, 0 failed/skipped, 9.79s. Lint/SDK: ok:true, 3 checks,
8 constructor parameters, 2 writes, 1 view. Warning I200: newer runner available;
requested pinned runner retained. SDK cache access was needed.
Toolchain: CLI 0.39.2, Node 24.12.0, Python 3.14.2, pytest 9.0.2,
genlayer-test 0.29.2, genvm-linter 0.11.1rc2, genlayer-py 0.18.0, genlayer-js 1.1.8.

## Real-source preflight and truth

Anonymous curl: REN Sourcify API HTTP 200, complete 10,308 raw bytes, valid UTF-8.
One RepublicToken.sol, 9,475 UTF-8 bytes including original CRLF. Chain 1,
0x408e41876cCCDC0F92210600ef50372656052a38; Match, not Exact Match.
Entire source read before drafting:

- owner/onlyOwner control pause() whenNotPaused and unpause() whenPaused.
- whenNotPaused gates transfer, transferFrom, approve, increaseApproval,
  decreaseApproval; reads remain possible.
- burn() and owner-only transferTokens() are not pause-gated. transferTokens()
  moves only owner's balance, not arbitrary holders' balances.
- transferOwnership changes pause authority. No token-code multisig or expiry.
- Current owner, custody, multisig membership and paused state were not verified.

Claim and disclosures are controlled hypothetical examples, not REN issuer
statements. Appointed issuer is an existing StudioNet test account. Truthful
pause.md preserves real conditions/exceptions; false-specific invents 3-of-5
approval and 72-hour expiry; vague stays vague. Three commit-pinned disclosure
URLs returned anonymous HTTP 200 before transactions.

## Finalized transaction proof

| Step | Hash | Leader execution | AGREE / DISAGREE / IDLE |
| --- | --- | --- | --- |
| deployment | `0x72bc972bc1fdca22b2744d0aafcaa48c29cd7903dd0dacb26d6d3dbaf5696da8` | SUCCESS | 5 / 0 / 0 |
| a_review | `0x45b971015451507194b200f47601751cca5e4504bffc54b23c0b991fcd26b2a0` | SUCCESS | 3 / 0 / 2 |
| b_non_issuer_expected_failure | `0x33cd0836209162724f8ae467cbed742ceda270a204deee3076290cc8b42f6066` | ERROR (expected rollback) | 5 / 0 / 0 |
| c_vague_inadequate_round_1 | `0xb27a15a1a89c61e7ab23aead16f352b141c7a9c90269c51d0acf9b35399ed849` | SUCCESS | 3 / 0 / 2 |
| d_false_specific_inadequate_round_2 | `0x4f1ee77ea6adcdef618ce7d3fa7b6678ecbaf09c6a22a8999e0592035526191b` | SUCCESS | 3 / 1 / 1 |
| e_replay_expected_failure | `0x5a736be7a86814171277e83873bfe9328670f863b798638b96c0952004b40a30` | ERROR (expected rollback) | 3 / 0 / 2 |
| f_truthful_adequate_round_3 | `0x2ddb6e3860dfd6bd59eeb715860afa228063a051ac353635b6dbfd2ef973247f` | SUCCESS | 3 / 2 / 0 |

All seven transactions FINALIZED. ACCEPTED and FINALIZED timestamps are separately
preserved from RPC lifecycle history; leader execution independently recorded.
Every read used latest-final. Two rollback states were whole-object equal to
preceding states. CLI “successfully executed” is not proof of execution SUCCESS:
negative calls were ERROR/rollback; RPC returned no human-readable revert reason.

Agenda exactly [[holder_transfer, PAUSE]]. Vague round 1 INADEQUATE;
false-specific round 2 INADEQUATE; truthful round 3 ADEQUATE, terminal
LISTED_WITH_DISCLOSURE with attestation and three retained consumed rounds.
No unexpected judgment, no retry or redeploy. No further wallet transaction.

## Read-only reproduction

CLI already configured for StudioNet:

```powershell
genlayer receipt 0x72bc972bc1fdca22b2744d0aafcaa48c29cd7903dd0dacb26d6d3dbaf5696da8 --status FINALIZED
genlayer receipt 0x2ddb6e3860dfd6bd59eeb715860afa228063a051ac353635b6dbfd2ef973247f --status FINALIZED
git -c safe.directory="<full repo path>" cat-file blob 34be6640d96627dca84e35bf985c60f0e4fa2657:contracts/token_claim_capability_gate.py
```

Check all hashes in the manifest separately. status_name FINALIZED is not the
leader receipt execution_result. Negative cases should remain ERROR/rollback.

With genlayer-js 1.1.8 available in Node module resolution, this unsigned snippet
reads finalized state and compares deployed bytes from the project directory:

```javascript
const {createClient, chains} = require("genlayer-js");
const cp = require("node:child_process");
const crypto = require("node:crypto");
(async () => {
  const client = createClient({chain: chains.studionet});
  const address = "0x6Ba50deF22213cbB020b66f88D4Bf1e0f7dbff2E";
  const state = await client.readContract({
    address, functionName: "get_state", args: [],
    transactionHashVariant: "latest-final"
  });
  console.log(JSON.stringify(state, (_,v) => typeof v === "bigint" ? v.toString() : v));
  const raw = await client.request({method: "gen_getContractCode", params: [address]});
  const deployed = Buffer.from(raw, "base64");
  const git = cp.spawnSync("git", ["-c", "safe.directory="+process.cwd(),
    "cat-file", "blob", "34be6640d96627dca84e35bf985c60f0e4fa2657:contracts/token_claim_capability_gate.py"]);
  if (git.status !== 0) throw new Error(git.stderr.toString());
  console.log("bytes_equal", deployed.equals(git.stdout));
  console.log("sha256", crypto.createHash("sha256").update(deployed).digest("hex"));
})().catch(e => { console.error(e); process.exitCode=1; });
```

RPC outage means verification pending, not proof of contract failure.
Explorer URLs were confirmed as actual anchor targets on the current contract
page. Anonymous HTTP 200 proves accessibility, not execution.
[Public checks](PUBLIC_URL_CHECKS.md).

## Three gates and limitations

Technical PASS: tests/lint, exact-source finalized deployment, complete ordered
demo and stored attestation. Distinctiveness PASS for implemented two-party
agenda/second-judgment/attestation changes; reviewer acceptance not guaranteed.
Evidence gate requires anonymous accessibility of the pushed package, recorded
in PUBLIC_URL_CHECKS.md. No actual REN issuer/custody/token-state, general semantic
correctness/injection immunity or downstream listing integration is verified.
No visibility change, Portal or appeal submission occurred.

Every command/result preserved locally in ignored
local-reports/RELEASE_COMMAND_LOG.md. [Test matrix](TEST_MATRIX.md) covers all
functions; historical checkpoints keep their original counts/policies.

## Full direct-test cases (all passed)

```text
tests/test_disclosure_protocol.py::test_qualified_agenda_is_sorted_by_claim_and_power PASSED
tests/test_disclosure_protocol.py::test_review_remains_permissionless_and_unverifiable_can_retry PASSED
tests/test_disclosure_protocol.py::test_contradiction_precedes_unclear_with_sufficient_coverage_and_is_final PASSED
tests/test_disclosure_protocol.py::test_insufficient_coverage_cannot_judge_contradiction PASSED
tests/test_disclosure_protocol.py::test_nonissuer_disclosure_reverts_before_fetch_and_preserves_state PASSED
tests/test_disclosure_protocol.py::test_vague_disclosure_uses_round_and_preserves_original_agenda PASSED
tests/test_disclosure_protocol.py::test_reused_disclosure_url_reverts_before_consensus PASSED
tests/test_disclosure_protocol.py::test_specific_disclosure_lists_with_exact_attestation_and_retained_history PASSED
tests/test_disclosure_protocol.py::test_pause_disclosure_cannot_blanket_satisfy_mint_pair PASSED
tests/test_disclosure_protocol.py::test_specific_but_source_inconsistent_disclosure_is_inadequate[unenforced-time-limit] PASSED
tests/test_disclosure_protocol.py::test_specific_but_source_inconsistent_disclosure_is_inadequate[unenforced-multisig] PASSED
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round[non-200] PASSED
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round[empty] PASSED
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round[oversized] PASSED
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round[invalid-utf8] PASSED
tests/test_disclosure_protocol.py::test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round[transport] PASSED
tests/test_disclosure_protocol.py::test_round2_partial_frozen_sources_below_threshold_preserve_last_round PASSED
tests/test_disclosure_protocol.py::test_source_outage_can_retry_same_url_when_sources_recover PASSED
tests/test_disclosure_protocol.py::test_source_outage_history_is_bounded_and_preserves_consumed_url_replay PASSED
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[1] PASSED
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[2] PASSED
tests/test_disclosure_protocol.py::test_rounds_exhaustion_is_terminal_and_history_is_bounded[3] PASSED
tests/test_disclosure_protocol.py::test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds[at-deadline] PASSED
tests/test_disclosure_protocol.py::test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds[after-deadline] PASSED
tests/test_disclosure_protocol.py::test_disclosure_before_deadline_can_complete PASSED
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[empty] PASSED
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[whitespace] PASSED
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[oversized] PASSED
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[invalid-utf8] PASSED
tests/test_disclosure_protocol.py::test_unavailable_disclosure_counts_round_and_never_becomes_adequate[non-200] PASSED
tests/test_disclosure_protocol.py::test_disclosure_transport_failure_consumes_last_round PASSED
tests/test_disclosure_protocol.py::test_disclosure_cap_counts_raw_utf8_bytes[15000-bytes] PASSED
tests/test_disclosure_protocol.py::test_disclosure_cap_counts_raw_utf8_bytes[15002-bytes] PASSED
tests/test_disclosure_protocol.py::test_contradicted_is_final_and_cannot_be_cured_by_disclosure PASSED
tests/test_disclosure_protocol.py::test_consistent_or_pending_cannot_accept_disclosures PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[http://example.org/x] PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://127.0.0.1/x] PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://service.internal/x] PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://user@example.org/x] PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://example.org:443/x] PASSED
tests/test_disclosure_protocol.py::test_invalid_disclosure_url_reverts_without_using_round[https://example.org /x] PASSED
tests/test_disclosure_protocol.py::test_round1_same_states_but_forged_power_is_rejected PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[decision] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[claim_states] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[powers_per_claim] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[contradicted_claims] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[qualified_claims] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[source_coverage] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[evidence_digest] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_rejects_mutation_of_every_result_field[agenda] PASSED
tests/test_disclosure_protocol.py::test_round1_validator_refetches_and_binds_complete_body_digest PASSED
tests/test_disclosure_protocol.py::test_round2_same_decision_but_forged_per_pair_verdict_is_rejected PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[decision] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[round] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[disclosure_url] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[disclosure_digest] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[available] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[verdicts] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[source_coverage] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_mutation_of_every_result_field[source_evidence_digest] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_refetches_same_url_and_rejects_changed_body PASSED
tests/test_disclosure_protocol.py::test_round2_same_verdicts_but_forged_source_evidence_digest_is_rejected PASSED
tests/test_disclosure_protocol.py::test_round2_validator_independently_refetches_frozen_source_bodies PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[negative-coverage] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[excessive-coverage] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[string-coverage] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[empty-digest] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[nested-digest] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_malformed_source_binding[nonhex-digest] PASSED
tests/test_disclosure_protocol.py::test_round2_validator_rejects_adequate_verdicts_with_insufficient_coverage PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[unknown] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[duplicate] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[empty-qualified] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[powers-for-holds] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[string-powers] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[nested-powers] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[invalid-state] PASSED
tests/test_disclosure_protocol.py::test_round1_malformed_or_unknown_powers_revert_before_storage[extra-key] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[missing] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[duplicate] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[invented-claim] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[unknown-power] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[bad-verdict] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[extra-row-key] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[extra-root-key] PASSED
tests/test_disclosure_protocol.py::test_round2_malformed_verdicts_revert_before_using_round[malformed] PASSED
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[0] PASSED
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[4] PASSED
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[True] PASSED
tests/test_disclosure_protocol.py::test_constructor_requires_integer_disclosure_round_bound[2] PASSED
tests/test_disclosure_protocol.py::test_constructor_rejects_boolean_min_sources PASSED
tests/test_disclosure_protocol.py::test_constructor_rejects_zero_issuer PASSED
tests/test_disclosure_protocol.py::test_both_consensus_paths_pickle_only_ordinary_snapshots PASSED
tests/test_disclosure_protocol.py::test_consensus_rejects_extra_leader_fields_and_malformed_payload[1] PASSED
tests/test_disclosure_protocol.py::test_consensus_rejects_extra_leader_fields_and_malformed_payload[2] PASSED
tests/test_disclosure_protocol.py::test_ast_every_leader_result_field_is_compared_in_both_paths PASSED
tests/test_gate.py::test_all_claims_hold_is_consistent_and_terminal PASSED
tests/test_gate.py::test_contradicted_claim_blocks_and_is_named PASSED
tests/test_gate.py::test_qualified_claim_freezes_agenda_and_prevents_rereview PASSED
tests/test_gate.py::test_unclear_claim_is_unverifiable PASSED
tests/test_gate.py::test_missing_invented_and_invalid_claim_states_are_rejected PASSED
tests/test_gate.py::test_all_sources_unavailable_fails_closed PASSED
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[empty] PASSED
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[whitespace] PASSED
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[oversized] PASSED
tests/test_gate.py::test_empty_oversized_or_invalid_evidence_is_not_counted[invalid-utf8] PASSED
tests/test_gate.py::test_validator_rejects_forged_vector_with_same_decision PASSED
tests/test_gate.py::test_validator_rejects_decision_inconsistent_with_vector PASSED
tests/test_gate.py::test_fewer_reachable_sources_than_min_sources_fails_closed PASSED
tests/test_gate.py::test_max_wait_rejects_disclosure_required_state PASSED
tests/test_gate.py::test_max_wait_without_review_is_unverifiable PASSED
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[0-2099-01-01T00:00:00Z-min_sources] PASSED
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[2-2099-01-01T00:00:00Z-min_sources] PASSED
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[1-2000-01-01T00:00:00Z-future] PASSED
tests/test_gate.py::test_constructor_rejects_bad_lifecycle[1-2099-01-01T00:00:00-timezone] PASSED
tests/test_gate.py::test_constructor_rejections[claims0-urls0-1-12] PASSED
tests/test_gate.py::test_constructor_rejections[claims1-urls1-unique] PASSED
tests/test_gate.py::test_constructor_rejections[claims2-urls2-text] PASSED
tests/test_gate.py::test_constructor_rejections[claims3-urls3-publicly reachable] PASSED
tests/test_gate.py::test_constructor_rejections[claims4-urls4-publicly reachable] PASSED
tests/test_gate.py::test_constructor_rejections[claims5-urls5-invalid] PASSED
tests/test_gate.py::test_constructor_rejections[claims6-urls6-invalid] PASSED
tests/test_gate.py::test_constructor_rejections[claims7-urls7-invalid] PASSED
tests/test_gate.py::test_constructor_rejections[claims8-urls8-unique] PASSED
```
