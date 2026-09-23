# StudioNet release candidate: DAI capability example

This is a constructor example for the **current local source**, not a deployment
record or a claim about a live GenLayer result. The claims below are deliberately
hypothetical; they are not statements attributed to the DAI issuer.

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

The expected interpretation is `no_admin_mint = CONTRADICTED` and
`no_transfer_fee = HOLDS`, yielding `BLOCKED` through deterministic derivation.
This is an expectation for the demo, not a mock-test result or a live consensus
claim. If validators disagree or the evidence is unavailable, record the actual
result rather than asserting the expected one.

After checking that the CLI network is `studionet`, run `genlayer deploy` from
this repository. `deploy/00_deploy_token.js` passes the JSON fields as strings,
prints the source SHA-256 and transaction hash, and uses the active CLI account.
Wait for a successful FINALIZED deployment receipt before calling `review()`.
