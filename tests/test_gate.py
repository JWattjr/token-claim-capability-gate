import json

import pytest

SRC = "contracts/token_claim_capability_gate.py"
CLAIMS = {"claims": [
    {"id": "no_mint", "text": "No additional tokens can be minted."},
    {"id": "no_freeze", "text": "Holder balances cannot be frozen."},
    {"id": "fixed_fee", "text": "Transfer fee is fixed at 0%."},
]}
CONTEXT = {"chain": "eip155:1", "token_address": "0x0000000000000000000000000000000000000001"}
URLS = ["https://example.org/token-source"]


MAX_WAIT = "2099-01-01T00:00:00Z"


def _deploy(direct_deploy, claims=CLAIMS, urls=URLS, min_sources=1, max_wait=MAX_WAIT):
    return direct_deploy(SRC, "token", claims, CONTEXT, urls, min_sources, max_wait)


def _mock(direct_vm, states, status=200):
    direct_vm.mock_web(r".*", {"status": status, "body": "verified source"})
    direct_vm.mock_llm(r".*", json.dumps({"claim_states": states}))


ALL_HOLD = {"no_mint": "HOLDS", "no_freeze": "HOLDS", "fixed_fee": "HOLDS"}


def test_all_claims_hold_is_consistent_and_terminal(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, ALL_HOLD)
    assert c.review()["decision"] == "CONSISTENT"
    assert direct_vm.run_validator()
    direct_vm.clear_mocks()
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED"))
    assert c.review()["status"] == "CONSISTENT"
    assert c.get_state()["attempts"] == 1


def test_contradicted_claim_blocks_and_is_named(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED", fixed_fee="QUALIFIED"))
    result = c.review()
    assert result["decision"] == "BLOCKED"
    assert result["contradicted_claims"] == ["no_mint"]
    assert result["qualified_claims"] == ["fixed_fee"]


def test_qualified_claim_requires_disclosure_and_stays_retriable(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_freeze="QUALIFIED"))
    assert c.review()["decision"] == "DISCLOSURE_REQUIRED"
    assert not c.get_state()["terminal"]
    # The issuer publishes the disclosure; a re-review can now pass.
    direct_vm.clear_mocks()
    _mock(direct_vm, ALL_HOLD)
    assert c.review()["decision"] == "CONSISTENT"


def test_unclear_claim_is_unverifiable(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, fixed_fee="UNCLEAR"))
    assert c.review()["decision"] == "UNVERIFIABLE"


def test_missing_invented_and_invalid_claim_states_are_normalized(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, {"no_mint": "HOLDS", "no_freeze": "PROBABLY_FINE", "invented": "CONTRADICTED"})
    result = c.review()
    assert set(result["claim_states"]) == {"fixed_fee", "no_freeze", "no_mint"}
    assert result["claim_states"]["no_freeze"] == "UNCLEAR"
    assert result["decision"] == "UNVERIFIABLE"


def test_all_sources_unavailable_fails_closed(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, ALL_HOLD, status=503)
    result = c.review()
    assert result["decision"] == "UNVERIFIABLE" and result["source_coverage"] == 0


@pytest.mark.parametrize("body", ["", " ", "x" * 15001, b"\xff"])
def test_empty_oversized_or_invalid_evidence_is_not_counted(direct_vm, direct_deploy, body):
    c = _deploy(direct_deploy)
    direct_vm.mock_web(r".*", {"status": 200, "body": body})
    direct_vm.mock_llm(r".*", json.dumps({"claim_states": ALL_HOLD}))
    result = c.review()
    assert result["decision"] == "UNVERIFIABLE" and result["source_coverage"] == 0
    assert direct_vm.run_validator()


def test_validator_rejects_forged_vector_with_same_decision(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED"))
    honest = c.review()
    # Still BLOCKED, but blames a different claim.
    forged = dict(honest, claim_states=dict(ALL_HOLD, no_freeze="CONTRADICTED"), contradicted_claims=["no_freeze"])
    assert not direct_vm.run_validator(leader_result=forged)


def test_validator_rejects_decision_inconsistent_with_vector(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_mint="CONTRADICTED"))
    honest = c.review()
    assert not direct_vm.run_validator(leader_result=dict(honest, decision="CONSISTENT"))


def test_fewer_reachable_sources_than_min_sources_fails_closed(direct_vm, direct_deploy):
    c = _deploy(direct_deploy, urls=["https://example.org/a", "https://example.net/b"], min_sources=2)
    direct_vm.mock_web(r"example\.org", {"status": 200, "body": "verified source"})
    direct_vm.mock_web(r"example\.net", {"status": 503, "body": "down"})
    direct_vm.mock_llm(r".*", json.dumps({"claim_states": ALL_HOLD}))
    result = c.review()
    assert result["decision"] == "UNVERIFIABLE" and result["source_coverage"] == 1


def test_max_wait_freezes_retriable_state(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    _mock(direct_vm, dict(ALL_HOLD, no_freeze="QUALIFIED"))
    assert c.review()["decision"] == "DISCLOSURE_REQUIRED"
    direct_vm.warp("2100-01-01T00:00:00Z")
    direct_vm.clear_mocks()
    _mock(direct_vm, ALL_HOLD)
    state = c.review()
    assert state["status"] == "DISCLOSURE_REQUIRED" and state["terminal"]
    assert c.review()["attempts"] == 1


def test_max_wait_without_review_is_unverifiable(direct_vm, direct_deploy):
    c = _deploy(direct_deploy)
    direct_vm.warp("2100-01-01T00:00:00Z")
    state = c.review()
    assert state["status"] == "UNVERIFIABLE" and state["terminal"] and state["attempts"] == 0


@pytest.mark.parametrize("min_sources,max_wait,message", [
    (0, MAX_WAIT, "min_sources"),
    (2, MAX_WAIT, "min_sources"),
    (1, "2000-01-01T00:00:00Z", "future"),
    (1, "2099-01-01T00:00:00", "timezone"),
])
def test_constructor_rejects_bad_lifecycle(direct_vm, direct_deploy, min_sources, max_wait, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, min_sources=min_sources, max_wait=max_wait)


@pytest.mark.parametrize("claims,urls,message", [
    ({"claims": []}, URLS, "1-12"),
    ({"claims": [{"id": "a", "text": "x"}, {"id": "a", "text": "y"}]}, URLS, "unique"),
    ({"claims": [{"id": "a"}]}, URLS, "text"),
    (CLAIMS, ["https://10.0.0.1/a"], "publicly reachable"),
    (CLAIMS, ["https://service.internal/a"], "publicly reachable"),
    (CLAIMS, ["https://[::1]/a"], "invalid"),
    (CLAIMS, ["https://example.org:443/a"], "invalid"),
    (CLAIMS, ["https://example.org /a"], "invalid"),
    (CLAIMS, URLS + URLS, "unique"),
])
def test_constructor_rejections(direct_vm, direct_deploy, claims, urls, message):
    with direct_vm.expect_revert(message):
        _deploy(direct_deploy, claims=claims, urls=urls)
