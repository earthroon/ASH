# 16AI-QW-38G-R6A-SAMPLER-04

## Runtime Candidate Trace Validation / Probe-to-Strict Promotion Gate Seal

### SSOT

- Semantic reference: `model_core::cpu_oracle_sampler`
- Runtime validation owner: `model_core::sampler_parity_validation`
- Input patch: `16AI-QW-38G-R6A-SAMPLER-03`

### Implemented

- Added `SamplerParityValidationMode`: `Off`, `ValidateProbe`, `PromoteStrictCandidate`.
- Added env gates: `ASH_SAMPLER_PARITY_VALIDATE`, `ASH_SAMPLER_PARITY_PROMOTE_STRICT`.
- Hooked SAMPLER-03 receipt append into SAMPLER-04 validation receipt append.
- Added validation receipt JSONL path and summary aggregation path.
- Preserved default no-overhead behavior: validation default is Off and Strict default is not changed.
- Added trace-readback blocking logic: missing GPU candidate trace marks strict promotion blocked rather than PASS.

### Promotion behavior

- `ValidateProbe`: writes validation receipts and keeps collecting.
- `PromoteStrictCandidate`: if receipts are pass-like and no trace readback failure is present, summary can report `STRICT_CANDIDATE_READY`.
- Any `FAIL_*`, `PARTIAL_*`, or missing trace readback blocks promotion.

### Artifacts

- `workspace/sampler04_runtime_validation_summary.json`
- `workspace/sampler04_runtime_validation_receipt_schema.json`
- `workspace/sampler04_runtime_validation_receipt.jsonl`
- `workspace/sampler04_validation_fixtures.json`
- `workspace/sampler04_static_checks.json`
- `workspace/sampler04.patch`
- `acceptance_reports/16AI-QW-38G-R6A-SAMPLER-04_acceptance.md`

### Non-scope

- No shader formula changes.
- No CPU oracle formula changes.
- No ΔK/QWave weighted Min-P.
- No tokenizer decode changes.

### Execution status

This container has no `cargo`, `rustc`, `rustfmt`, or WebGPU runtime. Static checks passed; execution checks are NOT_RUN.
