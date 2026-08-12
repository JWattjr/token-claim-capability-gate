# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts  
**Title:** Token Claim-Capability Coherence Gate

## Notes / Description

Built an MIT-licensed Token Claim-Capability Coherence Gate: a reusable GenLayer primitive that evaluates whether a launch manifesto is coherent with publicly evidenced token capabilities. It freezes bounded policy inputs and public HTTPS sources. Leader and validators independently evaluate the evidence; a custom equivalence function compares the consequential decision—CONSISTENT, DISCLOSURE_REQUIRED, BLOCKED, or UNVERIFIABLE—not JSON shape. The accepted decision can control listing, disclosure, or creator-bond policy. Malformed/private evidence, source failure, ambiguity, unauthorized calls, and validator disagreement fail closed. Includes pinned GenVM source, direct consensus tests, security audit, test matrix, StudioNet and Bradbury evidence.

## Evidence to add

1. GitHub Repository — https://github.com/JWattjr/token-claim-capability-gate
2. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/contracts/token_claim_capability_gate.py
3. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md
4. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md
5. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet.json
6. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/bradbury.json
7. GenLayer Explorer Contract — add the final Bradbury address from deployments/bradbury.json
