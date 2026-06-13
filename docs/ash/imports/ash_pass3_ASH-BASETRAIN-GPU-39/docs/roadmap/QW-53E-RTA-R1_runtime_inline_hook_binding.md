# QW-53E-RTA-R1 Roadmap

## Purpose

This patch does not add new risk math. It seals the runtime pipe: QW-53E-RTA must be bound to the real sampler-preselection point.

## Implemented Surfaces

- `crates/model_core/src/qw53e_rta_r1_runtime_hook_binding_audit.rs`
- `crates/model_core/src/bin/qw53e_rta_r1_runtime_hook_binding_audit_validate.rs`
- `crates/runtime/src/qw53e_rta_r1_runtime_hook_binding.rs`
- `crates/runtime/src/qw53e_rta_r1_sampler_handoff.rs`
- `crates/runtime/src/qw53e_rta_r1_no_lab_only_probe.rs`
- `crates/runtime/src/qw53e_rta_r1_wgpu_candidate_source.rs`
- WGPU sampler branch trace calls added to `crates/model_core/src/generation_sampling.rs`

## Local Verification

```bash
ASH_QW53E_RTA_R1_BINDING_TRACE=1 \
ASH_QW53E_RTA_R1_RECEIPT_DIR=. \
ASH_DECODE_PROFILE=subtitle_safe_sampled_v1 \
ASH_QW53E_RTA_MODE=explicit_lab_apply \
ASH_QW53E_RTA_EXPLICIT_ENABLE=1 \
cargo run -p runtime --example infer_only -- \
  --prompt-file workspace/probes/qw53e_rta_repeat_escape_probe.txt \
  --max-new-tokens 96

cargo run -p model_core --bin qw53e_rta_r1_runtime_hook_binding_audit_validate -- .
```

## Next

After this binding is verified locally, connect QW-54A live candidate Cheonjiin facade to this same sampler-preselection pipe.
