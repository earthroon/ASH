# 16AI-QW-38G-R6A-MINP-C2B Acceptance Report

## Status
STATIC_PASS / EXECUTION_NOT_RUN

## Scope
- Added `model_core::minp_c2b_static_prior_enable`.
- Added static safe v1 controlled semantic prior profile.
- Gated CPU oracle semantic bias through RUN-01 / SAMPLER04 / MINP-C2A readiness.
- Gated GPU semantic prior buffers through the same controlled gate.
- Added no-source regression and prior-domination receipts.

## Confirmed static checks
- module/export present
- default enabled false
- weak weights 0.05 / 0.05 / 0.0 / 0.20
- CPU oracle uses controlled gate
- GPU config disables semantic prior when gate is not PASS
- no-source regression receipt exists

## Not run
- cargo check
- cargo test
- WGSL compile
- runtime controlled semantic prior execution

## Gate state
Current environment has RUN-01 / SAMPLER04 / MINP-C2A runtime evidence as NOT_RUN, therefore semantic_prior_effective is blocked by default.
