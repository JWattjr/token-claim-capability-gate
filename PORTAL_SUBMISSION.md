# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Token Claim-Capability Coherence Gate

## Notes / Description

Built and deployed an MIT-licensed Token Claim-Capability Coherence Gate: a reusable GenLayer launchpad primitive that checks whether a token's public claims (for example "no additional minting" or "balances cannot be frozen") are coherent with what the token can actually do. The constructor freezes 1-12 uniquely identified claims, the capability context, public HTTPS evidence, a minimum number of sources that must be reachable, and a max-wait deadline. Leader and validators each judge every frozen claim as HOLDS, QUALIFIED, CONTRADICTED, or UNCLEAR; claim ids that were not frozen are dropped. The LLM never picks the listing decision: deterministic code derives CONSISTENT, DISCLOSURE_REQUIRED, BLOCKED, or UNVERIFIABLE from the vector and names the contradicted and qualified claims. The custom validator requires whole-result equality with its own independent evaluation, so the full per-claim vector, decision, named claims, and source coverage are all bound and nothing reaches state unverified. Uncertainty, or fewer reachable sources than the frozen minimum, fails closed to UNVERIFIABLE. CONSISTENT and BLOCKED are final; DISCLOSURE_REQUIRED stays retriable so an issuer can publish a disclosure, until the max-wait deadline makes the current state final. Review is permissionless over frozen inputs. Includes pinned GenVM source, 21 direct tests (including a leader that keeps BLOCKED but blames the wrong claim), a security audit, a test matrix, and StudioNet/Bradbury deployment records. It is a decision primitive and holds no funds.

## Evidence to add

1. GitHub Repository — https://github.com/JWattjr/token-claim-capability-gate
2. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/contracts/token_claim_capability_gate.py
3. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/tests/test_gate.py
4. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet.json
7. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/bradbury.json
8. GenLayer Explorer Contract — the final Bradbury address from deployments/bradbury.json
