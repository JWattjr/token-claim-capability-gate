# StudioNet release candidate: DAI capability example

This is the frozen constructor example used for the current StudioNet release.
The live deployment and review proof is in
[`deployments/studionet-release-2026-09-23.json`](../deployments/studionet-release-2026-09-23.json).
The claims below are deliberately hypothetical; they are not statements
attributed to the DAI issuer.

## Public evidence checked on 2026-09-23

- Contract: Ethereum mainnet DAI at `0x6B175474E89094C44Da98b954EedeAC495271d0F`.
- Frozen evidence URL: `https://sourcify.dev/server/v2/contract/1/0x6B175474E89094C44Da98b954EedeAC495271d0F?fields=sources`
- Human-readable [Sourcify contract record](https://repo.sourcify.dev/1/0x6B175474E89094C44Da98b954EedeAC495271d0F).
- Read-only HTTPS GET returned HTTP 200, `application/json; charset=utf-8`,
  and 8,603 response bytes. The response identified chain `1`, the same address,
  one source file (`Dai.sol`, 7,965 UTF-8 bytes), and `match: "match"`.
- Sourcify's **Match** means the recompiled functional bytecode matches the
  deployed code apart from its metadata hash; it is not an Exact Match. See
  [Sourcify's match definitions](https://docs.sourcify.dev/docs/exact-match-vs-match/).
- In that source, `mint(address,uint)` requires the `auth` modifier, `auth`
  permits addresses in `wards`, and `rely` can grant that permission. Successful
  `transferFrom` subtracts `wad` from the sender and adds `wad` to the recipient.

The API URL is the single frozen evidence source. Unlike the historical WETH9
GitHub URL, it returns the full address-linked source record within the current
15,000-byte limit. Recheck status, response size, address, match type, source
count, and relevant code immediately before deployment; API content and access
from GenVM may differ from this local preflight.

## Exact constructor arguments (in order)

```json
[
  "dai-mainnet-illustrative-claims",
  "{\"claims\":[{\"id\":\"no_admin_mint\",\"text\":\"No privileged address can mint additional DAI.\"},{\"id\":\"no_transfer_fee\",\"text\":\"The token contract deducts no fee from a successful transfer: the amount debited from the sender is credited in full to the recipient.\"}]}",
  "{\"chain\":\"eip155:1\",\"token_address\":\"0x6B175474E89094C44Da98b954EedeAC495271d0F\",\"name\":\"Dai Stablecoin\"}",
  "[\"https://sourcify.dev/server/v2/contract/1/0x6B175474E89094C44Da98b954EedeAC495271d0F?fields=sources\"]",
  1,
  "2027-12-31T00:00:00Z"
]
```

The live StudioNet review produced `no_admin_mint = CONTRADICTED` and
`no_transfer_fee = HOLDS`, yielding terminal `BLOCKED` through deterministic
derivation. Its receipt finalized with successful leader execution and a
3 AGREE / 2 DISAGREE majority. This does not attribute either claim to DAI's
issuer or establish behavior for other claim vectors.

The release used `genlayer deploy` on `studionet`.
`deploy/00_deploy_token.js` passes JSON fields as strings and prints the source
SHA-256 and transaction hash. Running it again would create a new contract;
the current address and receipts are in the release manifest.
