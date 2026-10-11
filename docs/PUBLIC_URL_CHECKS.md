# Anonymous public URL checks

Checked 2026-10-11 14:44:30 UTC. All **27 URLs returned HTTP 200**.
Curl used no Authorization headers, cookies, browser session, credentials or GitHub
API token. Repository visibility was not modified.

Package was published at df40e0b796520aed0047f7302899149476820d46 before this run;
source and disclosure URLs remain pinned to 34be6640d96627dca84e35bf985c60f0e4fa2657.
This status report is published in a later documentation-only commit. HTTP 200
establishes public accessibility, not transaction success. RPC-backed finality,
leader execution, exact source identity and read-backs are in the current manifest.

| Evidence | HTTP | Raw response bytes |
| --- | ---: | ---: |
| [GenLayer Explorer Contract](https://explorer-studio.genlayer.com/address/0x6Ba50deF22213cbB020b66f88D4Bf1e0f7dbff2E) | 200 | 524684 |
| [GitHub Repository](https://github.com/JWattjr/token-claim-capability-gate) | 200 | 300064 |
| [GitHub File — deployed source](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/contracts/token_claim_capability_gate.py) | 200 | 639111 |
| [Other — source commit](https://github.com/JWattjr/token-claim-capability-gate/commit/34be6640d96627dca84e35bf985c60f0e4fa2657) | 200 | 604783 |
| [GitHub File — current manifest](https://github.com/JWattjr/token-claim-capability-gate/blob/main/deployments/studionet-release-2026-10-11.json) | 200 | 779144 |
| [GitHub File — disclosure protocol tests](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/tests/test_disclosure_protocol.py) | 200 | 715118 |
| [GitHub File — base tests](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/tests/test_gate.py) | 200 | 345016 |
| [GitHub File — audit](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/SECURITY_AUDIT.md) | 200 | 263471 |
| [GitHub File — test matrix](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/TEST_MATRIX.md) | 200 | 278026 |
| [GitHub File — distinctiveness comparison](https://github.com/JWattjr/token-claim-capability-gate/blob/main/DISTINCTIVENESS.md) | 200 | 234439 |
| [GitHub File — release verification](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/RELEASE_VERIFICATION.md) | 200 | 358787 |
| [GitHub File — exact constructor](https://github.com/JWattjr/token-claim-capability-gate/blob/34be6640d96627dca84e35bf985c60f0e4fa2657/docs/STUDIONET_RELEASE_CANDIDATE.md) | 200 | 249547 |
| [Other — commit-pinned vague disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/vague.md) | 200 | 186 |
| [Other — commit-pinned false-specific disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/pause-false.md) | 200 | 622 |
| [Other — commit-pinned truthful disclosure](https://raw.githubusercontent.com/JWattjr/token-claim-capability-gate/34be6640d96627dca84e35bf985c60f0e4fa2657/examples/disclosures/pause.md) | 200 | 1890 |
| [Other — deployment receipt](https://explorer-studio.genlayer.com/tx/0x72bc972bc1fdca22b2744d0aafcaa48c29cd7903dd0dacb26d6d3dbaf5696da8) | 200 | 22952 |
| [Other — a review](https://explorer-studio.genlayer.com/tx/0x45b971015451507194b200f47601751cca5e4504bffc54b23c0b991fcd26b2a0) | 200 | 22952 |
| [Other — b non issuer expected failure](https://explorer-studio.genlayer.com/tx/0x33cd0836209162724f8ae467cbed742ceda270a204deee3076290cc8b42f6066) | 200 | 22952 |
| [Other — c vague inadequate round 1](https://explorer-studio.genlayer.com/tx/0xb27a15a1a89c61e7ab23aead16f352b141c7a9c90269c51d0acf9b35399ed849) | 200 | 22952 |
| [Other — d false specific inadequate round 2](https://explorer-studio.genlayer.com/tx/0x4f1ee77ea6adcdef618ce7d3fa7b6678ecbaf09c6a22a8999e0592035526191b) | 200 | 22952 |
| [Other — e replay expected failure](https://explorer-studio.genlayer.com/tx/0x5a736be7a86814171277e83873bfe9328670f863b798638b96c0952004b40a30) | 200 | 22952 |
| [Other — f truthful adequate round 3](https://explorer-studio.genlayer.com/tx/0x2ddb6e3860dfd6bd59eeb715860afa228063a051ac353635b6dbfd2ef973247f) | 200 | 22952 |
| [Other — address-linked REN source](https://sourcify.dev/server/v2/contract/1/0x408e41876cCCDC0F92210600ef50372656052a38?fields=sources) | 200 | 10308 |
| [PORTAL_SUBMISSION.md](https://github.com/JWattjr/token-claim-capability-gate/blob/main/PORTAL_SUBMISSION.md) | 200 | 249242 |
| [APPEAL.md](https://github.com/JWattjr/token-claim-capability-gate/blob/main/APPEAL.md) | 200 | 218464 |
| [README.md](https://github.com/JWattjr/token-claim-capability-gate/blob/main/README.md) | 200 | 255483 |
| [PUBLIC_URL_CHECKS.md](https://github.com/JWattjr/token-claim-capability-gate/blob/main/docs/PUBLIC_URL_CHECKS.md) | 200 | 221810 |

## Content checks

- Three raw disclosures were complete UTF-8: vague 186 bytes, false-specific
  622 bytes, truthful 1,890 bytes. Each SHA-256 equals its stored on-chain
  disclosure-history digest.
- Full REN source API response was 10,308 bytes, SHA-256
  `262678d331fb9d8f0cf5b1603422020149449e555485dd8109bf8102e0d13478`.
  Canonically hashing its source id/URL/availability/body digest reproduces
  `7f62ff331cc5fd652397b314e65cbb5690c49324a7e6669361606775a75dcd6b`,
  the review and every disclosure source-evidence digest in the read-back.
- Explorer's address page actually links /tx/ routes for all seven recorded
  transactions. Returned titles identify GenLayer Studio Explorer and requested
  identifiers are present. A generic embedded Next.js notFound template is not
  a rendered 404. Transaction pages are client-rendered; their HTTP status is
  not used to infer execution success.
- GitHub files returned their named file/revision page rather than an
  authentication prompt or a rendered missing-page response.
- Dynamic HTML byte sizes/hashes can change between requests; they are not
  deployed-contract source hashes. Byte-for-byte GenLayer source identity was
  independently verified via gen_getContractCode against the Git blob.
