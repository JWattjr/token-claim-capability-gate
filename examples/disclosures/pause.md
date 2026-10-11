# Controlled source-consistent disclosure

Not written or endorsed by the real REN issuer. This describes the source-defined mechanism, not current key custody or the identity of the current owner.

Token: RepublicToken (REN), Ethereum chain 1, 0x408e41876cCCDC0F92210600ef50372656052a38.
Source: https://sourcify.dev/server/v2/contract/1/0x408e41876cCCDC0F92210600ef50372656052a38?fields=sources

## PAUSE: authorized role and effects

The `owner` address defined by `Ownable` can exercise PAUSE. `onlyOwner` requires `msg.sender == owner`. In `Pausable`, `pause()` is protected by `onlyOwner` and `whenNotPaused`, sets `paused = true`, and emits `Pause()`. `unpause()` is protected by `onlyOwner` and `whenPaused`, sets `paused = false`, and emits `Unpause()`.

`PausableToken` applies `whenNotPaused` (`require(!paused)`) to `transfer`, `transferFrom`, `approve`, `increaseApproval`, and `decreaseApproval`. While paused, these standard transfer and allowance-changing functions revert. Balance and allowance reads are not stopped. `BurnableToken.burn()` and the owner-only `RepublicToken.transferTokens()` are not pause-gated; `transferTokens()` moves the owner's tokens, not arbitrary holders' balances.

## Limits and conditions

Code-enforced limits: only the owner may pause/unpause, and the existing pause-state conditions must hold. The source defines no duration limit, automatic expiry, cooldown, or multisig approval requirement for PAUSE. Additional code-enforced temporal or approval limits: none. `transferOwnership(address)` lets the current owner transfer ownership to a nonzero address; the new owner then holds the pause authority.

This statement does not establish whether the owner address is currently a multisig, its members, or key custody. Those off-chain/deployment facts are not asserted. It also does not claim that every token operation stops during a pause.
