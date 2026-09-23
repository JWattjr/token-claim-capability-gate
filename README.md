# Token Claim-Capability Coherence Gate

A launchpad listing gate: are a token's public claims (for example "no additional
minting" or "balances cannot be frozen") coherent with what the token can actually do?

## How it decides

The deployer freezes 1-12 claims (unique id plus text), the capability context
(chain, token address, and so on), 1-6 public HTTPS evidence URLs, `min_sources`
(how many must be reachable to decide), and a `max_wait` deadline. Point evidence
at address-linked verified source where possible. A DNS-hosted HTTPS source
counts only if it returns a nonempty, complete UTF-8 body of at most 15,000
bytes; fetch errors, non-200 responses, oversized bodies, and IP-literal or
explicit-port URLs are rejected. A raw `.sol` file alone does not establish
that it is the code deployed at the address in the capability context.

1. Leader and validators each fetch the evidence and judge **every frozen claim**:
   - `HOLDS`: true, with no material power undercutting it
   - `QUALIFIED`: true in substance, but a material power must be disclosed
   - `CONTRADICTED`: an undisclosed power or fact directly contradicts it
   - `UNCLEAR`: the evidence is insufficient

   Claim ids that were not frozen are dropped; missing or invalid values become `UNCLEAR`.
2. Deterministic code derives the listing decision. The LLM never picks it:
   - any `UNCLEAR`, or fewer than `min_sources` reachable → `UNVERIFIABLE`
   - any `CONTRADICTED` → `BLOCKED`
   - any `QUALIFIED` → `DISCLOSURE_REQUIRED`
   - all `HOLDS` → `CONSISTENT`
3. The validator requires the **entire result** to match its own independent
   evaluation: the decision, the full per-claim vector, the contradicted and
   qualified claim lists, and source coverage.

`CONSISTENT` and `BLOCKED` are final. `DISCLOSURE_REQUIRED` and `UNVERIFIABLE`
can be re-reviewed after the issuer publishes a disclosure at the frozen URLs,
until `max_wait`; after it, whatever state the gate holds becomes final (a token
never reviewed becomes `UNVERIFIABLE`).
`review()` is permissionless. The contract holds no funds.

## Verify

    python -m genvm_linter.cli lint contracts/token_claim_capability_gate.py --json
    python -m pytest tests -v

See docs/SECURITY_AUDIT.md, docs/TEST_MATRIX.md, and the
[StudioNet constructor example](docs/STUDIONET_RELEASE_CANDIDATE.md).

## Current StudioNet evidence

[`deployments/studionet-release-2026-09-23.json`](deployments/studionet-release-2026-09-23.json)
is the **current submission evidence** for source commit
`db3d97dc84f06fb84b9ffb72a0f1d2ff676f0ceb`. The deployed source bytes
matched the published file's SHA-256 exactly. The [StudioNet contract](https://explorer-studio.genlayer.com/address/0x33445EEF1a870071D33D3141c512898c2AaeF3f0)
and its deployment and review transactions finalized with successful leader
execution and majority agreement. The review had **3 AGREE / 2 DISAGREE**;
read-back state is terminal `BLOCKED`, with `no_admin_mint = CONTRADICTED`,
`no_transfer_fee = HOLDS`, and source coverage 1.

The DAI claims are hypothetical examples, not statements attributed to the
issuer. Sourcify reports a functional-bytecode **Match**, not an Exact Match,
for the address-linked source. This live result demonstrates one bounded-source
claim comparison, not every lifecycle or security path in the local tests.

## Historical record

`deployments/studionet.json` remains historical evidence for source commit
`0d41f253db60f9a0739a7a2915a27b478bc307f6`. Its WETH9 input was a
36.8 KB GitHub file, but that deployment read only a 15,000-byte prefix. It
does not prove the current source or a complete address-matched WETH9 review.
