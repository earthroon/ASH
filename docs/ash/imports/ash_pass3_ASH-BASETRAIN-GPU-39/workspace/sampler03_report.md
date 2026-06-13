# 16AI-QW-38G-R6A-SAMPLER-03 — GPU Candidate Trace Buffer / Full Candidate-Set Parity Seal

## Status

Baked as static patch over SAMPLER-02. Runtime execution was not run because cargo/rustc/WebGPU runtime are unavailable in this container.

## What changed

- Added GPU candidate trace header and entry buffers to the multistage sampler path.
- Added WGSL trace bindings to `gpu_sampling_topp_scan.wgsl` at bindings 7 and 8.
- The shader records active candidate token IDs and final candidate token IDs in shader scan order.
- Rust readback parses candidate trace header/entries into `GpuCandidateTrace`.
- `GpuSamplingResult` now carries `candidate_trace: Option<GpuCandidateTrace>`.
- `sampler_parity` now compares sorted CPU/GPU active and final ID sets.
- Receipt path moved to `workspace/sampler03_full_candidate_parity_receipt.jsonl`.

## Important caveat

The implementation is static-baked. Candidate buffer readback and WGSL compilation still need actual cargo/WebGPU verification. Overflow is not treated as PASS; it becomes `WARN_TRACE_TRUNCATED`.

## Strict mode

Strict `FAIL_*` parity status now returns the CPU oracle selected token on CPU-row GPU sampling paths and records `cpu_oracle_strict_demotion` telemetry. Same-device raw GPU paths still require a materialized CPU row before strict demotion can be applied.
