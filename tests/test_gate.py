import json
import pytest

def test_consensus_and_fail_closed(direct_vm, direct_deploy):
    c=direct_deploy("contracts/token_claim_capability_gate.py","token",{"claims":[{"id":"a","text":"No mint"}]},{"address":"0x1"},["https://example.org/source"])
    direct_vm.mock_web(r".*",{"status":200,"body":"official evidence"})
    direct_vm.mock_llm(r".*",json.dumps({"decision":"CONSISTENT","finding_codes":[]}))
    assert c.review()["decision"]=="CONSISTENT" and direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result={"decision":"BLOCKED","finding_codes":["UNDISCLOSED_MINT"]})

@pytest.mark.parametrize("url",["https://10.0.0.1/a","https://192.168.1.1/a","https://service.internal/a"])
def test_private_source_rejected(direct_deploy,url):
    with pytest.raises(Exception): direct_deploy("contracts/token_claim_capability_gate.py","token",{"claims":[{"id":"a","text":"No mint"}]},{},[url])
