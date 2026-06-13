# 16AI-QW-38G-R6A-DECODE-02B Report

## Scope
- Added `model_core::decode_transition_validation`.
- Added runtime transition probe receipt and probe-to-on summary gate.
- Extended sampler parity traces with selected transition action/reason/risk fields and candidate trace version.
- Connected sampler parity receipt append to DECODE-02B validation receipt append.

## Important limitation
`probe` mode before/after logit and candidate mask counters are not instrumented in this patch. DECODE-02B therefore records `PARTIAL_PROBE_INTEGRITY_COUNTER_NOT_AVAILABLE` and blocks `TRANSITION_ON_CANDIDATE_READY` until a later counter patch provides direct before/after evidence.

## Static checks
```json
{
  "decode_transition_validation_module_exists": true,
  "lib_declares_decode_transition_validation": true,
  "transition_validation_mode_exists": true,
  "probe_integrity_status_exists": true,
  "sampler_parity_calls_decode02b_validation": true,
  "candidate_trace_version_field": true,
  "selected_transition_fields_gpu": true,
  "selected_transition_entry_extracted": true,
  "reason_mask_helper": true,
  "json_artifacts": true
}
```

## Execution
- cargo check: NOT_RUN
- cargo test: NOT_RUN
- rustfmt: NOT_RUN
- WebGPU runtime transition validation: NOT_RUN
