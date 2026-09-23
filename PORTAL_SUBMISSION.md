# GenLayer Portal submission

**Contribution type:** Builder → Intelligent Contracts
**Title:** Token Claim-Capability Coherence Gate

## Notes / Description (release candidate; do not paste until redeployed)

Token Claim-Capability Coherence Gate is an MIT-licensed, reusable GenLayer listing primitive for comparing frozen token claims with public capability evidence. The constructor freezes 1-12 claim IDs and texts, a capability context, evidence URLs, a minimum number of complete sources, and a max-wait deadline. Leader and validators independently classify each claim as HOLDS, QUALIFIED, CONTRADICTED, or UNCLEAR. Code—not the LLM—derives CONSISTENT, DISCLOSURE_REQUIRED, BLOCKED, or UNVERIFIABLE and the named claim lists; the validator compares the entire result. Unusable sources count as unavailable; fewer usable sources than the frozen minimum, or any unclear claim, yields UNVERIFIABLE. CONSISTENT and BLOCKED are terminal; other results can be retried until the deadline. The current release candidate has 28 passing focused direct tests, a pinned GenVM runner, security notes, and a test matrix. The prior finalized StudioNet result reached CONSISTENT on an excerpt of a WETH9 GitHub file, not a complete, address-matched source audit and not on this patched source. The contract holds no funds.

**Current live-proof status:** NOT READY. `deployments/studionet.json` is historical evidence for commit `0d41f253db60f9a0739a7a2915a27b478bc307f6`. A bounded, address-linked DAI constructor example is prepared in `docs/STUDIONET_RELEASE_CANDIDATE.md`; redeploy the patched contract on StudioNet, verify source identity and finality, then replace the live-proof paragraph and manifest.

## Evidence to add after publishing the candidate and collecting new live proof

1. GitHub Repository — https://github.com/JWattjr/token-claim-capability-gate
2. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/contracts/token_claim_capability_gate.py
3. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/tests/test_gate.py
4. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md
5. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md
6. GitHub File — https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/STUDIONET_RELEASE_CANDIDATE.md
7. GitHub File (historical source only) — https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet.json
8. GenLayer Explorer Contract (historical source only) — https://explorer-studio.genlayer.com/address/0x2044C9554407f96e4Fa1aD1374C9b969b182E136

Historical resolution transaction hash: `0xe654c4ded35e451639603d768431fe4e3aba5d4c63faf410ff16ee49422c8e2b`. Its direct Explorer URL could not be verified from this environment, so do not add an invented path.

## StudioNet release checklist

1. Recheck the DAI Sourcify API source in `docs/STUDIONET_RELEASE_CANDIDATE.md`: HTTP 200, complete UTF-8 response at most 15,000 bytes, chain/address and `match` fields, source content, and GenVM reachability. The historical 36.8 KB WETH9 file cannot be used by the patched contract. Sourcify reports a Match, not an Exact Match.
2. Commit and publish the patched source and tests. Record the exact commit and source hash; do not reuse the historical deployment as proof of it.
3. Deploy on **StudioNet only**, complete a permissionless `review()`, and verify both transactions are FINALIZED with successful execution and majority agreement. Read back the final state and compare it with the frozen constructor inputs.
4. Save a new manifest with address, release commit, constructor, transaction hashes, receipts, validator outcome, final state, and verified Explorer links. Then update the Portal text and evidence list.
