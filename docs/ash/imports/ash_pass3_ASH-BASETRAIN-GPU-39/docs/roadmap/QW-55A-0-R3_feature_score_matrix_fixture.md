# QW-55A-0-R3 Roadmap

## Implemented

- Added `qw55a_vtc16_fixture` module in `model_core`.
- Added deterministic QW-55A feature row generator.
- Added deterministic QW-55A score row generator.
- Added feature/score channel order helpers.
- Added dry-run report, trace record, and receipt structures.
- Referenced QW-55A-0-R2 final step receipt hash as a plain string to avoid backend dependency leakage.
- Preserved no-selector/no-decode-mutation contract.

## Next

`QW-55A-0-R4 — Feature Score Matrix Backend Bridge / No Selector Commit Seal`

R4 may bridge the dry-run matrix fixture closer to the backend evidence chain, but selector commit remains forbidden.
