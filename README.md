# Token Claim-Capability Coherence Gate

Checks whether a token launch manifesto is coherent with publicly evidenced material capabilities.

## GenLayer-native decision

The contract makes the consensus-critical decision: **CONSISTENT, DISCLOSURE_REQUIRED, BLOCKED, or UNVERIFIABLE**. It
freezes bounded inputs and approved public evidence sources. The leader and
validators independently fetch/evaluate that evidence and compare the compact
decision fields using a custom equivalence function. After consensus, the
calling protocol deterministically controls launchpad listing, disclosure, and creator-bond policy.

The contract fails closed when evidence is unavailable, ambiguous, or
validator consensus does not support the same substantive result. It does not
use a frontend answer, a single backend, or format-only validation.

## Verify

Run: python -m genvm_linter.cli lint contracts/token_claim_capability_gate.py --json
Run: python -m pytest tests -v

See docs/SECURITY_AUDIT.md, docs/TEST_MATRIX.md, and PORTAL_SUBMISSION.md.
