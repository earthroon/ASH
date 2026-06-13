# 16AI-QW-38G-R6A-DECODE-03A Acceptance

## Patch
Entropy / Confidence Metric Receipt Seal

## Status
STATIC_BAKE_DEFINED_NOT_RUN

## Confirmed static changes
- Added `crates/model_core/src/decode03a_entropy.rs`.
- Registered `mod decode03a_entropy` and public exports in `crates/model_core/src/lib.rs`.
- Added observe-only DECODE-03A append hook to `sampler_parity::append_receipt()`.
- Added CPU oracle entropy/top1/top2 fields to `CpuOracleCandidateTrace`.
- Propagated entropy/confidence seed fields through `CpuSamplerRuntimeTrace`.
- Added optional GPU entropy fields to `GpuSamplerRuntimeTrace`; GPU entropy remains optional for DECODE-03A.
- Added static workspace schema/summary/probe fixtures.

## Contract
- `behavior_change=false`.
- CPU oracle remains sampler SSOT.
- DECODE-03A does not enable dynamic sampling.
- DECODE-03A only writes entropy/confidence receipts when `ASH_DECODE03A_ENTROPY=receipt` or `strict`.

## Runtime not executed
The bake container does not provide `cargo`/`rustc`, so cargo check, unit tests, shader validation, and runtime smoke were not executed here.

## Required runtime command shape
```bash
ASH_SAMPLER_PARITY=probe \
ASH_SAMPLER05_PARITY=receipt \
ASH_DECODE03A_ENTROPY=receipt \
ASH_DECODE03A_REQUIRE_SAMPLER05=true \
ASH_DECODE03A_RECEIPT=workspace/decode03a_entropy_steps.jsonl \
ASH_DECODE03A_SUMMARY=workspace/decode03a_summary.json \
<existing inference command>
```

## Promotion rule
DECODE-03B PCI may start only after DECODE-03A runtime receipt has no NaN/Inf and no behavior-change evidence.
