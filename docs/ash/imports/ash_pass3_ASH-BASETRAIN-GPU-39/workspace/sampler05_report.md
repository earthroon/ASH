# 16AI-QW-38G-R6A-SAMPLER-05

## CPU Oracle / GPU Active Set Parity Seal

### Scope
- Input patch: `16AI-QW-38G-R6A-SAMPLER-04`
- Semantic SSOT: `model_core::cpu_oracle_sampler`
- GPU projection: `burn_webgpu_backend::gpu_sampling_topp_scan.wgsl`
- Default behavior change: `false`

### Implemented
1. Added `crates/model_core/src/sampler05_parity.rs`.
2. Exported SAMPLER-05 types/functions from `crates/model_core/src/lib.rs`.
3. Hooked existing SAMPLER-03 append path into SAMPLER-05 receipt append.
4. Patched `gpu_sampling_topp_scan.wgsl` so pre-min-p max uses `weighted_logit_at(i)`, not raw/scaled logits.
5. Added controlled top-k bypass policy in `gpu_sampling.rs` via `ASH_SAMPLER05_TOPK_POLICY=bypass_if_not_transition_aware`.
6. Added workspace fixture manifest, receipt schema/example, summary, static checks, and patch diff.

### Runtime env
```text
ASH_SAMPLER_PARITY=probe
ASH_SAMPLER05_PARITY=receipt
ASH_GPU_CANDIDATE_TRACE=1
ASH_SAMPLER05_TOPK_POLICY=bypass_if_not_transition_aware
ASH_SAMPLER05_FORBID_GLOBAL_FALLBACK=true
ASH_SAMPLER05_RECEIPT=workspace/sampler05_parity_steps.jsonl
ASH_SAMPLER05_SUMMARY=workspace/sampler05_summary.json
```

### Gate
- PASS requires runtime receipt, not schema example.
- Dynamic sampler / DECODE-03A promotion remains blocked until runtime parity probe executes.

### Container validation
`cargo` was not available in this container, so cargo check/test and WGPU shader compilation were not run here. Static file checks passed and are recorded in `workspace/sampler05_static_checks.json`.
