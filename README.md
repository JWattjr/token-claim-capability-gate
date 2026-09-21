# Token Claim-Capability Coherence Gate

A launchpad listing gate: are a token's public claims (for example "no additional
minting" or "balances cannot be frozen") coherent with what the token can actually do?

## How it decides

The deployer freezes 1-12 claims (unique id plus text), the capability context
(chain, token address, and so on), 1-6 public HTTPS evidence URLs, `min_sources`
(how many must be reachable to decide), and a `max_wait` deadline. Point evidence
at raw verified source (Sourcify or a raw `.sol` file); up to 15,000 characters per source are read.

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

See docs/SECURITY_AUDIT.md and docs/TEST_MATRIX.md.
