# StudioNet release candidate: REN disclosure protocol

This replaces the historical DAI constructor example. DAI and WETH9 manifests
are historical and do not verify the new protocol. Claims and disclosures here
are controlled hypothetical examples, not statements attributed to REN's issuer.

## Source preflight (2026-10-11)

- Token: Republic Token (REN), Ethereum chain 1, `0x408e41876cCCDC0F92210600ef50372656052a38`.
- Frozen source URL: https://sourcify.dev/server/v2/contract/1/0x408e41876cCCDC0F92210600ef50372656052a38?fields=sources
- curl returned HTTP 200 and **10,308 raw bytes**, complete UTF-8, one source
  file `RepublicToken.sol` (9,475 UTF-8 bytes, including original CRLF).
- Sourcify reports creation/runtime `match`, not `exact_match`. This is
  address-linked verification metadata, not proof of present role custody/state.
- Read the entire source before writing the disclosures. `owner`/`onlyOwner`
  control `pause()`/`unpause()`; `whenNotPaused` gates standard transfers and
  approval updates. `burn()` and owner-only `transferTokens()` are not gated.
  No token-code timer or multisig check exists. The truthful disclosure preserves
  these exceptions and conditions instead of claiming all operations stop.
- Deployment uses the existing StudioNet account moment-grid-studionet as the
  appointed demo issuer (not the real-world token issuer). The expected wrong
  issuer is the existing portal-five-release-new account.

## Exact constructor arguments (in order)

```json
[
  "ren-mainnet-hypothetical-holder-transfer",
  "{\"claims\":[{\"id\":\"holder_transfer\",\"text\":\"Ordinary token holders can use transfer to move their own tokens to a nonzero recipient whenever their balance covers the amount.\"}]}",
  "{\"chain\":\"eip155:1\",\"token_address\":\"0x408e41876cCCDC0F92210600ef50372656052a38\",\"name\":\"Republic Token (REN)\",\"scope\":\"Source-defined holder transfer; hypothetical example, not an issuer-attributed claim. No assertion about current owner identity or paused state.\"}",
  "[\"https://sourcify.dev/server/v2/contract/1/0x408e41876cCCDC0F92210600ef50372656052a38?fields=sources\"]",
  1,
  "2026-11-11T00:00:00Z",
  "0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92",
  3
]
```

## Bounded demo sequence

Deploy the committed source once using `genlayer deploy` on StudioNet. Verify
FINALIZED and leader SUCCESS separately, then byte-for-byte deployed-source
identity against the committed Git blob without normalization.

1. Permissionless review -> DISCLOSURE_REQUIRED, agenda [holder_transfer, PAUSE].
2. Wrong issuer submission -> expected execution error, unchanged read-back.
3. vague.md -> INADEQUATE, round 1 consumed.
4. pause-false.md -> INADEQUATE, round 2 consumed.
5. Replay vague.md URL -> expected execution error, unchanged read-back.
6. pause.md -> LISTED_WITH_DISCLOSURE, round 3 consumed, exact attestation.

Use raw.githubusercontent.com URLs pinned to the disclosure commit. Wait for
FINALIZED and read get_state after every transaction. If any judgment differs,
stop after that step: no retry or redeploy. Source or disclosure transport may
differ inside GenVM from local curl. Source outages do not use a round; an
unavailable disclosure uses a round, even if sources are also unavailable.
