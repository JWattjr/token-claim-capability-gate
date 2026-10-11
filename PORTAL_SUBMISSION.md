# GenLayer Portal package (not submitted)

Contribution type: Builder → Intelligent Contracts
Title: Token Claim-Capability Coherence Gate

## Portal note (under 1,000 characters)

Token Claim-Capability Coherence Gate is a two-party GenLayer disclosure-and-attestation primitive. Permissionless review freezes a claim/power agenda; only the appointed issuer may answer. Validators independently fetch disclosure and frozen source URLs, checking power, holder and limits plus code consistency. Deterministic decisions and strict whole-result comparison bind an attestation; contradictions cannot be cured. The StudioNet REN-source demo finalized: vague and specific-but-false disclosures were INADEQUATE, non-issuer/replay calls rolled back, and truthful disclosure yielded LISTED_WITH_DISCLOSURE in round 3 (3 AGREE, 2 DISAGREE). Source bytes exactly match the Git blob; 124 direct tests and lint pass. Claims/disclosures are controlled hypotheticals, not REN issuer statements. Source is Sourcify Match, not Exact Match. No automatic listing, custody proof or prompt-injection guarantee is claimed.

## Evidence links and categories

- [GenLayer Explorer Contract](https://explorer-studio.genlayer.com/address/0x6Ba50deF22213cbB020b66f88D4Bf1e0f7dbff2E)
- [GitHub Repository](https://github.com/JWattjr/token-claim-capability-gate)
- [GitHub File — deployed source](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/contracts/token_claim_capability_gate.py)
- [Other — source commit](https://github.com/JWattjr/token-claim-capability-gate/commit/34be6640d96627dca84e35bf985c60f0e4fa2657)
- [GitHub File — current manifest](https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet-release-2026-10-11.json)
- [GitHub File — disclosure protocol tests](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/tests/test_disclosure_protocol.py)
- [GitHub File — base tests](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/tests/test_gate.py)
- [GitHub File — audit](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md)
- [GitHub File — test matrix](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md)
- [GitHub File — distinctiveness comparison](https://github.com/JWattjr/token-claim-capability-gate/blob/main/DISTINCTIVENESS.md)
- [GitHub File — release verification](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/RELEASE_VERIFICATION.md)
- [GitHub File — exact constructor](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/docs/STUDIONET_RELEASE_CANDIDATE.md)
- [Other — commit-pinned vague disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/vague.md)
- [Other — commit-pinned false-specific disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/pause-false.md)
- [Other — commit-pinned truthful disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/pause.md)
- [Other — deployment receipt](https://explorer-studio.genlayer.com/tx/0x72bc972bc1fdca22b2744d0aafcaa48c29cd7903dd0dacb26d6d3dbaf5696da8)
- [Other — a review](https://explorer-studio.genlayer.com/tx/0x45b971015451507194b200f47601751cca5e4504bffc54b23c0b991fcd26b2a0)
- [Other — b non issuer expected failure](https://explorer-studio.genlayer.com/tx/0x33cd0836209162724f8ae467cbed742ceda270a204deee3076290cc8b42f6066)
- [Other — c vague inadequate round 1](https://explorer-studio.genlayer.com/tx/0xb27a15a1a89c61e7ab23aead16f352b141c7a9c90269c51d0acf9b35399ed849)
- [Other — d false specific inadequate round 2](https://explorer-studio.genlayer.com/tx/0x4f1ee77ea6adcdef618ce7d3fa7b6678ecbaf09c6a22a8999e0592035526191b)
- [Other — e replay expected failure](https://explorer-studio.genlayer.com/tx/0x5a736be7a86814171277e83873bfe9328670f863b798638b96c0952004b40a30)
- [Other — f truthful adequate round 3](https://explorer-studio.genlayer.com/tx/0x2ddb6e3860dfd6bd59eeb715860afa228063a051ac353635b6dbfd2ef973247f)
- [Other — address-linked REN source](https://sourcify.dev/server/v2/contract/1/0x408e41876cCCDC0F92210600ef50372656052a38?fields=sources)

## Evidence interpretation

Current source commit: `34be6640d96627dca84e35bf985c60f0e4fa2657`.
Source Git blob: `75c644e39b0ff68b8a648a0eaeb5868d5b72a70d`.
Contract source SHA-256: `61262d820cecb622388c551bdbc885b5039a45eb4aed90eb877ec87e1a9a90da`.
Deployment FINALIZED + leader SUCCESS. All six demo transactions finalized;
four semantic steps SUCCESS; two guard failures ERROR/rollback, whole state unchanged.
Final listing: 3 AGREE / 2 DISAGREE, not unanimity. Full arguments, leader results,
votes and every latest-final read-back are in the manifest. Human-readable revert
reasons were absent from RPC; specific guards additionally have direct tests.

Anonymous accessibility: [public URL checks](docs/PUBLIC_URL_CHECKS.md).
HTTP 200 only proves accessibility; RPC receipts/read-back prove finality and
execution, and gen_getContractCode proves source identity. WETH9/DAI are historical.
[Appeal](APPEAL.md) is a draft only. No Portal or appeal submission was made.
