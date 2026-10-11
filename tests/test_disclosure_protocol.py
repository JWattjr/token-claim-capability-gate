"""Controlled direct-mode fixtures; no token issuer or live disclosure is represented."""

import ast
import copy
import hashlib
import json
import re
from pathlib import Path

import pytest

from test_gate import ALL_HOLD, CLAIMS, ISSUER, SRC, _deploy, _mock


OTHER = b"\x03" * 20
TRANSFER_CLAIMS = {"claims": [{"id": "transfer", "text": "Holders can transfer tokens freely."}]}
VAGUE = "Administrators retain some operational controls."
# Synthetic minimal source, not a live token or issuer statement.
SOURCE_CODE = """contract ControlledToken {
    address public pauser;
    bool public paused;
    constructor(address appointedPauser) { pauser = appointedPauser; }
    function pause() external { require(msg.sender == pauser); paused = true; }
    function unpause() external { require(msg.sender == pauser); paused = false; }
    function transfer(address, uint256) external { require(!paused); }
}"""
SPECIFIC = (
    "The pauser account can exercise PAUSE at any time through pause(). While paused, "
    "transfers stop. The same pauser can call unpause(). No time limit or multisig "
    "approval is enforced by this code."
)
URL = "https://example.org/disclosures/one"


def qualified(direct_vm, direct_deploy, powers=("PAUSE",), max_rounds=3, max_wait=None):
    kwargs = {"claims": TRANSFER_CLAIMS, "max_rounds": max_rounds}
    if max_wait is not None:
        kwargs["max_wait"] = max_wait
    c = _deploy(direct_deploy, **kwargs)
    _mock(direct_vm, {"transfer": "QUALIFIED"}, powers={"transfer": list(powers)}, body=SOURCE_CODE)
    return c, c.review()


def disclosure_mock(direct_vm, agenda, verdict="ADEQUATE", body=SPECIFIC, status=200,
                    source_body=SOURCE_CODE, source_status=200, prompt_pattern="Judge issuer disclosure adequacy"):
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"/disclosures/", {"status": status, "body": body})
    if source_body is not None:
        direct_vm.mock_web(r"/token-source$", {"status": source_status, "body": source_body})
    rows = [] if verdict is None else [
        {"claim_id": c, "power": p, "verdict": verdict[(c, p)] if isinstance(verdict, dict) else verdict}
        for c, p in agenda
    ]
    if verdict is not None:
        direct_vm.mock_llm(prompt_pattern, json.dumps({"verdicts": rows}))
    return rows


def submit(direct_vm, c, url=URL):
    with direct_vm.prank(ISSUER):
        return c.submit_disclosure(url)


def consistency_prompt(body):
    """Mock only matches if the real prompt binds both fetched bodies and the rubric.

    The returned semantic verdict is controlled; this is not a live LLM proof.
    """
    return (
        r"(?s)Judge issuer disclosure adequacy"
        + r"(?=.*" + re.escape(json.dumps(body)) + r")"
        + r"(?=.*Frozen source evidence:)"
        + r"(?=.*" + re.escape(json.dumps(SOURCE_CODE)) + r")"
        + r"(?=.*states nothing that contradicts the frozen source evidence)"
        + r"(?=.*limits the code does not enforce is INADEQUATE)"
    )


def test_qualified_agenda_is_sorted_by_claim_and_power(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_freeze="QUALIFIED", fixed_fee="QUALIFIED"),
          powers={"no_mint": [], "no_freeze": ["PAUSE", "BLACKLIST", "FREEZE"],
                  "fixed_fee": ["FEE_CHANGE"]})
    result = c.review()
    assert result["powers_per_claim"]["no_freeze"] == ["BLACKLIST", "FREEZE", "PAUSE"]
    assert c.get_state()["agenda"] == [
        ["fixed_fee", "FEE_CHANGE"], ["no_freeze", "BLACKLIST"],
        ["no_freeze", "FREEZE"], ["no_freeze", "PAUSE"],
    ]
    assert direct_vm.run_validator()


def test_review_remains_permissionless_and_unverifiable_can_retry(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, ALL_HOLD, status=503)
    with direct_vm.prank(OTHER):
        assert c.review()["decision"] == "UNVERIFIABLE"
    direct_vm.clear_mocks()
    _mock(direct_vm, ALL_HOLD)
    with direct_vm.prank(OTHER):
        assert c.review()["decision"] == "CONSISTENT"
    assert c.get_state()["attempts"] == 2


def test_contradiction_precedes_unclear_with_sufficient_coverage_and_is_final(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED", no_freeze="UNCLEAR"))
    result = c.review()
    assert result["decision"] == "BLOCKED" and direct_vm.run_validator()
    before = c.get_state()
    assert before["agenda"] == [] and before["terminal"]
    direct_vm.clear_mocks()
    assert c.review() == before  # Final, with no refetch or model call.
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure(URL)
    assert c.get_state() == before


def test_insufficient_coverage_cannot_judge_contradiction(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED", no_freeze="UNCLEAR"), status=503)
    result = c.review()
    assert result["decision"] == "UNVERIFIABLE" and result["source_coverage"] == 0
    assert set(result["claim_states"].values()) == {"UNCLEAR"}
    assert result["contradicted_claims"] == [] and not c.get_state()["terminal"]
    assert direct_vm.run_validator()


def test_nonissuer_disclosure_reverts_before_fetch_and_preserves_state(direct_vm, direct_deploy):
    c, _ = qualified(direct_vm, direct_deploy)
    before = c.get_state()
    direct_vm.clear_mocks()  # No fetch/model response exists: authorization must run first.
    with direct_vm.prank(OTHER):
        with direct_vm.expect_revert("only issuer_address"):
            c.submit_disclosure(URL)
    assert c.get_state() == before


def test_vague_disclosure_uses_round_and_preserves_original_agenda(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=VAGUE)
    result = submit(direct_vm, c)
    assert result["decision"] == "DISCLOSURE_REQUIRED"
    assert result["verdicts"] == [{"claim_id": "transfer", "power": "PAUSE", "verdict": "INADEQUATE"}]
    assert direct_vm.run_validator()
    state = c.get_state()
    assert state["rounds_used"] == 1 and state["max_disclosure_rounds"] == 3
    assert state["claim_states"] == first["claim_states"]
    assert state["powers_per_claim"] == first["powers_per_claim"]
    assert state["evidence_digest"] == first["evidence_digest"]
    assert state["agenda"] == first["agenda"] and state["attestation"] == {}
    assert state["disclosure_history"] == [{
        "round": 1, "url": URL, "digest": hashlib.sha256(VAGUE.encode()).hexdigest(),
        "available": True, "verdicts": result["verdicts"],
        "source_coverage": 1, "source_evidence_digest": result["source_evidence_digest"],
        "round_consumed": True, "marker": "ASSESSED",
    }]


def test_reused_disclosure_url_reverts_before_consensus(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=VAGUE)
    submit(direct_vm, c)
    before = c.get_state()
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("already been submitted"):
            c.submit_disclosure(URL)
    assert c.get_state() == before


def test_specific_disclosure_lists_with_exact_attestation_and_retained_history(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=VAGUE)
    submit(direct_vm, c)
    old_history = copy.deepcopy(c.get_state()["disclosure_history"])
    disclosure_mock(direct_vm, first["agenda"], prompt_pattern=consistency_prompt(SPECIFIC))
    result = submit(direct_vm, c, "https://example.org/disclosures/two")
    assert result["decision"] == "LISTED_WITH_DISCLOSURE" and direct_vm.run_validator()
    claims_digest = hashlib.sha256(
        json.dumps(TRANSFER_CLAIMS["claims"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    state = c.get_state()
    assert state["status"] == "LISTED_WITH_DISCLOSURE" and state["terminal"]
    assert state["rounds_used"] == 2 and state["attempts"] == 1
    assert state["disclosure_history"][:1] == old_history
    assert state["attestation"] == {
        "token_id": "token", "claims_digest": claims_digest, "agenda": first["agenda"],
        "disclosure_url": "https://example.org/disclosures/two",
        "disclosure_digest": hashlib.sha256(SPECIFIC.encode()).hexdigest(),
        "round": 2, "verdicts": result["verdicts"],
        "source_coverage": 1, "source_evidence_digest": result["source_evidence_digest"],
    }
    assert result["source_evidence_digest"] == first["evidence_digest"]
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure("https://example.org/disclosures/three")
    with direct_vm.expect_revert("agenda"):
        c.review()
    direct_vm.warp("2100-01-01T00:00:00Z")
    assert c.get_state() == state  # A completed attestation survives the deadline.


def test_pause_disclosure_cannot_blanket_satisfy_mint_pair(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy, powers=("PAUSE", "MINT"))
    rows = disclosure_mock(direct_vm, first["agenda"],
                           verdict={("transfer", "PAUSE"): "ADEQUATE", ("transfer", "MINT"): "INADEQUATE"})
    result = submit(direct_vm, c)
    assert result["verdicts"] == rows and result["decision"] == "DISCLOSURE_REQUIRED"
    assert c.get_state()["attestation"] == {} and direct_vm.run_validator()


@pytest.mark.parametrize("false_limit", [
    "The pauser account can exercise PAUSE, stopping transfers, but pause() enforces a 24-hour time limit.",
    "The pauser account can exercise PAUSE, stopping transfers, but pause() enforces approval by a 2-of-3 multisig.",
], ids=["unenforced-time-limit", "unenforced-multisig"])
def test_specific_but_source_inconsistent_disclosure_is_inadequate(direct_vm, direct_deploy, false_limit):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=false_limit,
                    prompt_pattern=consistency_prompt(false_limit))
    result = submit(direct_vm, c)
    assert result["available"] and result["source_coverage"] == 1
    assert result["verdicts"] == [{"claim_id": "transfer", "power": "PAUSE", "verdict": "INADEQUATE"}]
    assert result["decision"] == "DISCLOSURE_REQUIRED" and direct_vm.run_validator()
    assert c.get_state()["rounds_used"] == 1 and c.get_state()["attestation"] == {}


@pytest.mark.parametrize("body,status", [
    ("offline", 503), ("", 200), ("x" * 15001, 200), (b"\xff", 200), (None, 200),
], ids=["non-200", "empty", "oversized", "invalid-utf8", "transport"])
def test_round2_unavailable_frozen_sources_force_all_unclear_without_using_round(direct_vm, direct_deploy, body, status):
    c, first = qualified(direct_vm, direct_deploy, powers=("MINT", "PAUSE"))
    disclosure_mock(direct_vm, first["agenda"], verdict=None, source_body=body, source_status=status)
    # Failure is mechanical; no semantic model answer exists.
    result = submit(direct_vm, c)
    assert result["available"] and result["source_coverage"] == 0
    assert all(v["verdict"] == "UNCLEAR" for v in result["verdicts"])
    assert result["decision"] == "DISCLOSURE_REQUIRED" and direct_vm.run_validator()
    state = c.get_state()
    assert state["rounds_used"] == 0 and state["attestation"] == {}
    assert state["disclosure_history"][0]["marker"] == "SOURCES_UNAVAILABLE"
    assert state["disclosure_history"][0]["round_consumed"] is False
    assert state["disclosure_history"][0]["source_evidence_digest"] == result["source_evidence_digest"]
    assert result["source_evidence_digest"] != first["evidence_digest"]


def test_round2_partial_frozen_sources_below_threshold_preserve_last_round(direct_vm, direct_deploy):
    c = _deploy(direct_deploy, claims=TRANSFER_CLAIMS, max_rounds=1, min_sources=2,
                urls=["https://example.org/token-source", "https://example.net/token-source"])
    _mock(direct_vm, {"transfer": "QUALIFIED"}, powers={"transfer": ["PAUSE"]}, body=SOURCE_CODE)
    first = c.review()
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"example\.org/token-source$", {"status": 200, "body": SOURCE_CODE})
    direct_vm.mock_web(r"example\.net/token-source$", {"status": 503, "body": "offline"})
    direct_vm.mock_web(r"/disclosures/", {"status": 200, "body": SPECIFIC})
    result = submit(direct_vm, c)
    assert result["source_coverage"] == 1 and result["available"]
    assert result["verdicts"] == [{"claim_id": "transfer", "power": "PAUSE", "verdict": "UNCLEAR"}]
    assert result["decision"] == "DISCLOSURE_REQUIRED" and direct_vm.run_validator()
    assert not c.get_state()["terminal"] and c.get_state()["rounds_used"] == 0
    assert c.get_state()["agenda"] == first["agenda"] and c.get_state()["attestation"] == {}


def test_source_outage_can_retry_same_url_when_sources_recover(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy, max_rounds=1)
    disclosure_mock(direct_vm, first["agenda"], source_status=503, verdict=None)
    assert submit(direct_vm, c)["decision"] == "DISCLOSURE_REQUIRED"
    assert c.get_state()["rounds_used"] == 0
    disclosure_mock(direct_vm, first["agenda"])
    assert submit(direct_vm, c)["decision"] == "LISTED_WITH_DISCLOSURE"
    assert c.get_state()["rounds_used"] == 1
    assert [r["round_consumed"] for r in c.get_state()["disclosure_history"]] == [False, True]


def test_source_outage_history_is_bounded_and_preserves_consumed_url_replay(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=VAGUE)
    submit(direct_vm, c)
    for i in range(12):
        disclosure_mock(direct_vm, first["agenda"], source_status=503, verdict=None)
        submit(direct_vm, c, f"https://example.org/disclosures/outage-{i}")
    state = c.get_state()
    assert len(state["disclosure_history"]) == 9 and state["rounds_used"] == 1
    assert state["disclosure_history"][0]["url"] == URL
    assert all(r["marker"] == "SOURCES_UNAVAILABLE" for r in state["disclosure_history"][1:])
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("already been submitted"):
            c.submit_disclosure(URL)
    direct_vm.warp("2100-01-01T00:00:00Z")
    assert c.get_state()["status"] == "DISCLOSURE_REJECTED"
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("before max_wait"):
            c.submit_disclosure("https://example.org/disclosures/late-outage")


@pytest.mark.parametrize("max_rounds", [1, 2, 3])
def test_rounds_exhaustion_is_terminal_and_history_is_bounded(direct_vm, direct_deploy, max_rounds):
    c, first = qualified(direct_vm, direct_deploy, max_rounds=max_rounds)
    for i in range(max_rounds):
        disclosure_mock(direct_vm, first["agenda"], verdict="INADEQUATE", body=VAGUE)
        result = submit(direct_vm, c, f"https://example.org/disclosures/round-{i}")
        assert result["decision"] == ("DISCLOSURE_REJECTED" if i + 1 == max_rounds else "DISCLOSURE_REQUIRED")
    before = c.get_state()
    assert before["terminal"] and before["rounds_used"] == max_rounds
    assert len(before["disclosure_history"]) == max_rounds
    assert before["attestation"] == {}
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure("https://example.org/disclosures/four")
    assert c.get_state() == before


@pytest.mark.parametrize("at", ["2030-01-01T00:00:00Z", "2030-01-01T00:00:01Z"],
                         ids=["at-deadline", "after-deadline"])
def test_disclosure_deadline_is_terminal_and_late_calls_preserve_rounds(direct_vm, direct_deploy, at):
    direct_vm.warp("2029-12-31T00:00:00Z")
    c, _ = qualified(direct_vm, direct_deploy, max_wait="2030-01-01T00:00:00Z")
    direct_vm.warp(at)
    direct_vm.clear_mocks()
    state = c.get_state()
    assert state["status"] == "DISCLOSURE_REJECTED" and state["terminal"]
    assert state["rounds_used"] == 0
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("before max_wait"):
            c.submit_disclosure(URL)
    assert c.get_state() == state


def test_disclosure_before_deadline_can_complete(direct_vm, direct_deploy):
    direct_vm.warp("2029-12-31T00:00:00Z")
    c, first = qualified(direct_vm, direct_deploy, max_wait="2030-01-01T00:00:00Z")
    direct_vm.warp("2029-12-31T23:59:59Z")
    disclosure_mock(direct_vm, first["agenda"])
    assert submit(direct_vm, c)["decision"] == "LISTED_WITH_DISCLOSURE"


@pytest.mark.parametrize("body,status", [("", 200), (" ", 200), ("x" * 15001, 200),
                                         (b"\xff", 200), ("offline", 503)],
                         ids=["empty", "whitespace", "oversized", "invalid-utf8", "non-200"])
def test_unavailable_disclosure_counts_round_and_never_becomes_adequate(direct_vm, direct_deploy, body, status):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"], body=body, status=status)
    result = submit(direct_vm, c)
    assert result["available"] is False and result["disclosure_digest"] == ""
    assert all(v["verdict"] == "UNCLEAR" for v in result["verdicts"])
    assert result["decision"] == "DISCLOSURE_REQUIRED"
    assert c.get_state()["rounds_used"] == 1 and c.get_state()["attestation"] == {}
    assert c.get_state()["disclosure_history"][0]["marker"] == "DISCLOSURE_UNAVAILABLE"
    assert c.get_state()["disclosure_history"][0]["round_consumed"] is True
    assert direct_vm.run_validator()


def test_disclosure_transport_failure_consumes_last_round(direct_vm, direct_deploy):
    c, _ = qualified(direct_vm, direct_deploy, max_rounds=1)
    direct_vm.clear_mocks()  # Missing web mock simulates a transport exception.
    result = submit(direct_vm, c)
    assert result["available"] is False and result["decision"] == "DISCLOSURE_REJECTED"
    assert c.get_state()["rounds_used"] == 1 and c.get_state()["terminal"]


@pytest.mark.parametrize("chars,available", [(7500, True), (7501, False)], ids=["15000-bytes", "15002-bytes"])
def test_disclosure_cap_counts_raw_utf8_bytes(direct_vm, direct_deploy, chars, available):
    c, first = qualified(direct_vm, direct_deploy)
    text = "é" * chars
    disclosure_mock(direct_vm, first["agenda"], body=text)
    result = submit(direct_vm, c)
    assert result["available"] is available
    assert result["decision"] == ("LISTED_WITH_DISCLOSURE" if available else "DISCLOSURE_REQUIRED")
    if available:
        assert result["disclosure_digest"] == hashlib.sha256(text.encode()).hexdigest()


def test_contradicted_is_final_and_cannot_be_cured_by_disclosure(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED"))
    assert c.review()["decision"] == "BLOCKED"
    before = c.get_state()
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure(URL)
    assert c.review() == before
    assert c.get_state()["attestation"] == {} and c.get_state()["agenda"] == []


def test_consistent_or_pending_cannot_accept_disclosures(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure(URL)
    _mock(direct_vm, ALL_HOLD)
    c.review()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert("open DISCLOSURE_REQUIRED"):
            c.submit_disclosure(URL)


@pytest.mark.parametrize("url", ["http://example.org/x", "https://127.0.0.1/x", "https://service.internal/x",
                                 "https://user@example.org/x", "https://example.org:443/x", "https://example.org /x"])
def test_invalid_disclosure_url_reverts_without_using_round(direct_vm, direct_deploy, url):
    c, _ = qualified(direct_vm, direct_deploy)
    direct_vm.clear_mocks()
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert():
            c.submit_disclosure(url)
    assert c.get_state()["rounds_used"] == 0 and c.get_state()["disclosure_history"] == []


def test_round1_same_states_but_forged_power_is_rejected(direct_vm, direct_deploy):
    c, honest = qualified(direct_vm, direct_deploy)
    forged = copy.deepcopy(honest)
    forged["powers_per_claim"]["transfer"] = ["MINT"]
    forged["agenda"] = [["transfer", "MINT"]]
    assert forged["decision"] == honest["decision"] and forged["claim_states"] == honest["claim_states"]
    assert not direct_vm.run_validator(leader_result=forged)


@pytest.mark.parametrize("field", ["decision", "claim_states", "powers_per_claim", "contradicted_claims",
                                  "qualified_claims", "source_coverage", "evidence_digest", "agenda"])
def test_round1_validator_rejects_mutation_of_every_result_field(direct_vm, direct_deploy, field):
    _, honest = qualified(direct_vm, direct_deploy)
    forged = copy.deepcopy(honest)
    mutations = {
        "decision": "CONSISTENT", "claim_states": {"transfer": "HOLDS"},
        "powers_per_claim": {"transfer": ["MINT"]}, "contradicted_claims": ["transfer"],
        "qualified_claims": [], "source_coverage": True, "evidence_digest": "0" * 64,
        "agenda": [["transfer", "UPGRADE"]],
    }
    forged[field] = mutations[field]
    assert not direct_vm.run_validator(leader_result=forged)


def test_round1_validator_refetches_and_binds_complete_body_digest(direct_vm, direct_deploy):
    _, honest = qualified(direct_vm, direct_deploy)
    direct_vm.clear_mocks()
    direct_vm.mock_web(".*", {"status": 200, "body": "changed verified source"})
    direct_vm.mock_llm("Judge each token claim", json.dumps({
        "claim_states": {"transfer": "QUALIFIED"}, "powers_per_claim": {"transfer": ["PAUSE"]},
    }))
    assert not direct_vm.run_validator(leader_result=honest)


def test_round2_same_decision_but_forged_per_pair_verdict_is_rejected(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy, powers=("MINT", "PAUSE"))
    disclosure_mock(direct_vm, first["agenda"],
                    verdict={("transfer", "MINT"): "INADEQUATE", ("transfer", "PAUSE"): "ADEQUATE"})
    honest = submit(direct_vm, c)
    forged = copy.deepcopy(honest)
    forged["verdicts"][1]["verdict"] = "INADEQUATE"
    assert honest["decision"] == "DISCLOSURE_REQUIRED"
    assert not direct_vm.run_validator(leader_result=forged)


@pytest.mark.parametrize("field", ["decision", "round", "disclosure_url", "disclosure_digest", "available", "verdicts",
                                  "source_coverage", "source_evidence_digest"])
def test_round2_validator_rejects_mutation_of_every_result_field(direct_vm, direct_deploy, field):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    forged = copy.deepcopy(honest)
    mutations = {
        "decision": "DISCLOSURE_REQUIRED", "round": True, "disclosure_url": "https://example.org/forged",
        "disclosure_digest": "0" * 64, "available": 1,
        "verdicts": [{"claim_id": "transfer", "power": "MINT", "verdict": "ADEQUATE"}],
        "source_coverage": True, "source_evidence_digest": "0" * 64,
    }
    forged[field] = mutations[field]
    assert not direct_vm.run_validator(leader_result=forged)


def test_round2_validator_refetches_same_url_and_rejects_changed_body(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    disclosure_mock(direct_vm, first["agenda"], body=SPECIFIC + " Edited after retrieval.")
    assert not direct_vm.run_validator(leader_result=honest)


def test_round2_same_verdicts_but_forged_source_evidence_digest_is_rejected(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    forged = dict(honest, source_evidence_digest="0" * 64)
    assert forged["verdicts"] == honest["verdicts"] and forged["decision"] == honest["decision"]
    assert not direct_vm.run_validator(leader_result=forged)


def test_round2_validator_independently_refetches_frozen_source_bodies(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    disclosure_mock(direct_vm, first["agenda"], source_body=SOURCE_CODE + " // changed source")
    assert not direct_vm.run_validator(leader_result=honest)


@pytest.mark.parametrize("field,value", [
    ("source_coverage", -1), ("source_coverage", 2), ("source_coverage", "1"),
    ("source_evidence_digest", ""), ("source_evidence_digest", ["0" * 64]),
    ("source_evidence_digest", "G" * 64),
], ids=["negative-coverage", "excessive-coverage", "string-coverage", "empty-digest", "nested-digest", "nonhex-digest"])
def test_round2_validator_rejects_malformed_source_binding(direct_vm, direct_deploy, field, value):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    assert not direct_vm.run_validator(leader_result=dict(honest, **{field: value}))


def test_round2_validator_rejects_adequate_verdicts_with_insufficient_coverage(direct_vm, direct_deploy):
    c, first = qualified(direct_vm, direct_deploy)
    disclosure_mock(direct_vm, first["agenda"])
    honest = submit(direct_vm, c)
    forged = dict(honest, source_coverage=0, decision="DISCLOSURE_REQUIRED")
    assert not direct_vm.run_validator(leader_result=forged)


@pytest.mark.parametrize("kind", ["unknown", "duplicate", "empty-qualified", "powers-for-holds",
                                 "string-powers", "nested-powers", "invalid-state", "extra-key"])
def test_round1_malformed_or_unknown_powers_revert_before_storage(direct_vm, direct_deploy, kind):
    c = _deploy(direct_deploy, claims=TRANSFER_CLAIMS)
    payload = {"claim_states": {"transfer": "QUALIFIED"}, "powers_per_claim": {"transfer": ["PAUSE"]}}
    if kind == "unknown":
        payload["powers_per_claim"]["transfer"] = ["SEIZE"]
    elif kind == "duplicate":
        payload["powers_per_claim"]["transfer"] = ["PAUSE", "PAUSE"]
    elif kind == "empty-qualified":
        payload["powers_per_claim"]["transfer"] = []
    elif kind == "powers-for-holds":
        payload["claim_states"]["transfer"] = "HOLDS"
    elif kind == "string-powers":
        payload["powers_per_claim"]["transfer"] = "PAUSE"
    elif kind == "nested-powers":
        payload["powers_per_claim"]["transfer"] = [["PAUSE"]]
    elif kind == "invalid-state":
        payload["claim_states"]["transfer"] = "FINE"
    else:
        payload["extra"] = "forged"
    direct_vm.mock_web(".*", {"status": 200, "body": "verified source"})
    direct_vm.mock_llm("Judge each token claim", json.dumps(payload))
    with direct_vm.expect_revert():
        c.review()
    assert c.get_state()["attempts"] == 0 and c.get_state()["agenda"] == []


@pytest.mark.parametrize("kind", ["missing", "duplicate", "invented-claim", "unknown-power", "bad-verdict",
                                 "extra-row-key", "extra-root-key", "malformed"])
def test_round2_malformed_verdicts_revert_before_using_round(direct_vm, direct_deploy, kind):
    c, first = qualified(direct_vm, direct_deploy, powers=("MINT", "PAUSE"))
    rows = disclosure_mock(direct_vm, first["agenda"])
    payload = {"verdicts": copy.deepcopy(rows)}
    if kind == "missing":
        payload["verdicts"].pop()
    elif kind == "duplicate":
        payload["verdicts"][1] = payload["verdicts"][0]
    elif kind == "invented-claim":
        payload["verdicts"][0]["claim_id"] = "invented"
    elif kind == "unknown-power":
        payload["verdicts"][0]["power"] = "SEIZE"
    elif kind == "bad-verdict":
        payload["verdicts"][0]["verdict"] = True
    elif kind == "extra-row-key":
        payload["verdicts"][0]["extra"] = 1
    elif kind == "extra-root-key":
        payload["extra"] = 1
    else:
        payload["verdicts"] = {"PAUSE": "ADEQUATE"}
    direct_vm.clear_mocks()
    direct_vm.mock_web(".*", {"status": 200, "body": SPECIFIC})
    direct_vm.mock_llm("Judge issuer disclosure adequacy", json.dumps(payload))
    with direct_vm.prank(ISSUER):
        with direct_vm.expect_revert():
            c.submit_disclosure(URL)
    assert c.get_state()["rounds_used"] == 0 and c.get_state()["disclosure_history"] == []


@pytest.mark.parametrize("max_rounds", [0, 4, True, "2"])
def test_constructor_requires_integer_disclosure_round_bound(direct_vm, direct_deploy, max_rounds):
    with direct_vm.expect_revert("max_disclosure_rounds"):
        _deploy(direct_deploy, max_rounds=max_rounds)


def test_constructor_rejects_boolean_min_sources(direct_vm, direct_deploy):
    with direct_vm.expect_revert("min_sources"):
        _deploy(direct_deploy, min_sources=True)


def test_constructor_rejects_zero_issuer(direct_vm, direct_deploy):
    with direct_vm.expect_revert("issuer_address"):
        _deploy(direct_deploy, issuer=b"\x00" * 20)


def test_both_consensus_paths_pickle_only_ordinary_snapshots(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    c, first = qualified(direct_vm, direct_deploy)
    assert direct_vm.run_validator()
    disclosure_mock(direct_vm, first["agenda"])
    assert submit(direct_vm, c)["decision"] == "LISTED_WITH_DISCLOSURE"
    assert direct_vm.run_validator()


@pytest.mark.parametrize("round_number", [1, 2])
def test_consensus_rejects_extra_leader_fields_and_malformed_payload(direct_vm, direct_deploy, round_number):
    c, first = qualified(direct_vm, direct_deploy)
    honest = first
    if round_number == 2:
        disclosure_mock(direct_vm, first["agenda"])
        honest = submit(direct_vm, c)
    assert not direct_vm.run_validator(leader_result=dict(honest, unchecked="forged"))
    assert not direct_vm.run_validator(leader_result=["not", "an", "object"])


def test_ast_every_leader_result_field_is_compared_in_both_paths():
    """Structural regression guard, supplemented by per-field behavioral mutation tests."""
    tree = ast.parse(Path(SRC).read_text(encoding="utf-8"))
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    klass = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    methods = {n.name: n for n in klass.body if isinstance(n, ast.FunctionDef)}
    constants = {
        n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id in ("REVIEW_RESULT_FIELDS", "DISCLOSURE_RESULT_FIELDS")
    }
    for mode in ("review", "disclosure"):
        derive = functions["_derive_" + mode]
        returns = [n for n in ast.walk(derive) if isinstance(n, ast.Return)]
        assert len(returns) == 1 and isinstance(returns[0].value, ast.Dict)
        fields = {ast.literal_eval(k) for k in returns[0].value.keys}
        assert fields == set(constants[mode.upper() + "_RESULT_FIELDS"])
        judge_returns = [n for n in ast.walk(functions["_judge_" + mode]) if isinstance(n, ast.Return)]
        assert all(isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                   and n.value.func.id == "_derive_" + mode for n in judge_returns)
        consensus = methods["_consensus_" + mode]
        validator = next(n for n in consensus.body if isinstance(n, ast.FunctionDef) and n.name == "validator_fn")
        assignments = {n.targets[0].id: n.value for n in ast.walk(validator)
                       if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
        leader = assignments["canonical_leader"]
        independent = assignments["independent"]
        assert leader.func.id == independent.func.id == "_canonical_" + mode + "_result"
        assert isinstance(leader.args[0], ast.Attribute) and leader.args[0].attr == "calldata"
        assert isinstance(leader.args[0].value, ast.Name) and leader.args[0].value.id == "leader_result"
        assert isinstance(independent.args[0], ast.Call) and independent.args[0].func.id == "leader_fn"
        comparisons = [n.value for n in ast.walk(validator)
                       if isinstance(n, ast.Return) and isinstance(n.value, ast.Compare)]
        assert any(isinstance(c.left, ast.Name) and c.left.id == "canonical_leader"
                   and len(c.ops) == 1 and isinstance(c.ops[0], ast.Eq)
                   and isinstance(c.comparators[0], ast.Name) and c.comparators[0].id == "independent"
                   for c in comparisons)
        canonical = functions["_canonical_" + mode + "_result"]
        assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "_exact"
                   and isinstance(n.args[1], ast.Name)
                   and n.args[1].id == mode.upper() + "_RESULT_FIELDS" for n in ast.walk(canonical))
