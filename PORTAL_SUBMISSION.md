# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Token Claim-Capability Coherence Gate

## Notes / Description (ready to paste)

Token Claim-Capability Coherence Gate is an MIT-licensed GenLayer listing primitive. A deployer freezes token claims, capability context, public HTTPS evidence, minimum source coverage, and a deadline. Leader and validators independently classify each claim; deterministic code derives CONSISTENT, DISCLOSURE_REQUIRED, BLOCKED, or UNVERIFIABLE and binds the full result through exact validator comparison. The current source was deployed and reviewed on StudioNet against Sourcify's address-linked DAI source (Match, not Exact Match). For two explicitly hypothetical claims, validators found no-admin-mint CONTRADICTED and no-transfer-fee HOLDS. The FINALIZED review had successful leader execution and 3 AGREE / 2 DISAGREE, producing terminal BLOCKED with coverage 1. Deployed source identity was verified byte-for-byte; 28 focused tests pass. The example does not attribute these claims to the DAI issuer or prove prompt-injection resistance.

## Current submission proof

- **Current manifest:** `deployments/studionet-release-2026-09-23.json`
- **Source commit:** `db3d97dc84f06fb84b9ffb72a0f1d2ff676f0ceb`
- **StudioNet contract:** `0x33445EEF1a870071D33D3141c512898c2AaeF3f0`
- **Deployment transaction:** `0x33184430e8f0ff16bede50a3c79c6378dc3076ea8671687e6996140925db51a7` — FINALIZED, leader SUCCESS, MAJORITY_AGREE (3 AGREE, 2 IDLE after quorum).
- **Review transaction:** `0xfb2e134f5a966de6eb25acf25488cbe41842d9900848070527c512e58147772c` — FINALIZED, leader SUCCESS, MAJORITY_AGREE (3 AGREE, 2 DISAGREE).
- **Read-back state:** `BLOCKED`, terminal, `no_admin_mint = CONTRADICTED`, `no_transfer_fee = HOLDS`, coverage 1, attempts 1.

## Evidence to add to the Portal

1. GenLayer Explorer Contract — https://explorer-studio.genlayer.com/address/0x33445EEF1a870071D33D3141c512898c2AaeF3f0
2. GitHub Repository — https://github.com/JWattjr/token-claim-capability-gate
3. GitHub File (current release manifest) — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet-release-2026-09-23.json
4. GitHub File (deployed source commit) — https://github.com/JWattjr/token-claim-capability-gate/blob/db3d97dc84f06fb84b9ffb72a0f1d2ff676f0ceb/contracts/token_claim_capability_gate.py
5. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/tests/test_gate.py
6. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md
7. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md
8. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/STUDIONET_RELEASE_CANDIDATE.md
9. Other (deployment receipt) — https://explorer-studio.genlayer.com/tx/0x33184430e8f0ff16bede50a3c79c6378dc3076ea8671687e6996140925db51a7
10. Other (review receipt) — https://explorer-studio.genlayer.com/tx/0xfb2e134f5a966de6eb25acf25488cbe41842d9900848070527c512e58147772c
11. Other (verified DAI source record) — https://repo.sourcify.dev/1/0x6B175474E89094C44Da98b954EedeAC495271d0F

`deployments/studionet.json` and its WETH9 Explorer address are **historical**;
they are not proof of this current source or DAI result.

The live example covers a bounded source and one mixed claim vector. The
QUALIFIED, UNVERIFIABLE, retry, deadline, and injection paths are not proven
by this live transaction; consult the local test matrix and security audit for
their separate scope. Submit only after the current manifest and evidence URLs
are publicly readable at the published revision.
