# 16AI-QW-38G-R6A-STOP-01 Acceptance

## Status
STATIC_BAKE_DEFINED_NOT_RUN

## Accepted Static Contracts
- [x] STOP-01 module added.
- [x] Default mode is Off.
- [x] Controlled stop requires explicit mode + behavior permission.
- [x] EOS bias stop is not executed by default.
- [x] Output tail truncation is forbidden by contract.
- [x] Gate, execution, pre/post fingerprint, and summary structures are present.
- [x] STOP-01 append hook is wired after SALAD-03B.

## Not Run
- [ ] cargo check
- [ ] cargo test
- [ ] runtime stop smoke

## Next
STOP-02 — EOS Finalization / User-visible Stop Surface Seal.
