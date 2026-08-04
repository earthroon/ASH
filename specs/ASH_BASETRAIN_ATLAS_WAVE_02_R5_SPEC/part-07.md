loss count                                  0
backward count                              0
optimizer count                             0
weight write count                          0
receipt overclaim count                     0
artifact readback failures                  0
```

---

# 28. PASS tokens

## 28.1 Canonical oracle PASS

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_WGPU26_WGSL_ABI_AUDIT_SAME_PROCESS_AW01_LIVE_RESIDENCY_ADOPTION_NO_HOST_WEIGHT_REUPLOAD_EXPLICIT_POSITION_ROPE_PARAMETER_BINDING_EMBEDDING_RMSNORM_QKV_ROPE_STAGE_SPLIT_CANONICAL_GPU_ORACLE_NAMING_SEPARATION_CPU_F64_FULL_NUMERICAL_PARITY_PADDING_QKV_CONTEXT_EXACT_ZERO_EXECUTED_POSITIVE_NEGATIVE_CONTROL_COUNTING_TENSORCUBE_LIVE_LEASE_HANDOFF_NO_RECEIPT_OVERCLAIM_NO_STAGE10_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_NO_WEIGHT_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

## 28.2 Stronger Headwise-adapter PASS

This token is permitted only if the actual adapter path executes:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_WGPU26_WGSL_ABI_AUDIT_SAME_PROCESS_AW01_LIVE_RESIDENCY_ADOPTION_NO_HOST_WEIGHT_REUPLOAD_EXPLICIT_POSITION_ROPE_PARAMETER_BINDING_EMBEDDING_RMSNORM_QKV_ROPE_STAGE_SPLIT_HEADWISE_TRAINING_ADAPTER_LIVE_DISPATCH_CPU_F64_FULL_NUMERICAL_PARITY_PADDING_QKV_CONTEXT_EXACT_ZERO_EXECUTED_POSITIVE_NEGATIVE_CONTROL_COUNTING_TENSORCUBE_LIVE_LEASE_HANDOFF_NO_RECEIPT_OVERCLAIM_NO_STAGE10_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_NO_WEIGHT_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

The oracle gate must never print the Headwise-adapter token.

---

# 29. Direct execution

Canonical oracle profile:

```powershell
cargo run --release `
  --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r5_physical_gate `
  -- `
  "@specs/cli/ash_basetrain_atlas_wave_02_r5.args"
```

Repair and execution wrapper:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\repair_aw02_r5_compile_and_run.ps1 `
  -RepoRoot . `
  -RunGate
```

The repair script must:

```text
validate required source files
validate response-file pair format
scan canonical WGSL for forbidden resource-pointer parameters
run real WGSL parser/validator where available
force source timestamps newer than stale metadata
set CARGO_INCREMENTAL=0
clean by orchestrator manifest
cargo check the exact R5 binary
run the exact R5 binary
```

---

# 30. Completion state

After canonical oracle PASS:

```text
AW-00 transaction
  Prepared
  immutable

AW-01 residency
  live in the same process during R5
  triple ring exact
  current resident bundle exact
  compute-bindable

AW-02 R5 stages
  embedding complete
  RMSNorm complete
  QKV complete
  RoPE complete
  canonical GPU oracle complete
  CPU-f64 full parity complete
  padding exact-zero complete

Executor authority
  CanonicalGpuOracle
  Headwise authority false
  production authority false

TensorCube
  live Q/K/V/context lease ready
  Stage10 not dispatched
  output authority false

Training mutation
  loss absent
  backward absent
  optimizer absent
  delta absent
  weight write absent
```

After the stronger Headwise-adapter PASS, only this line changes:

```text
Executor authority
  HeadwiseTrainingAdapter for selected-layer training context
  production decode authority false
```

---

# 31. Next patch boundary

Canonical next patch after R5 oracle PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6

Headwise Training Adapter Live Adoption /
Existing Dispatcher Same-Device Binding /
Training Admission Context /
No Decode Session Fabrication /
Oracle-vs-Headwise Context Parity /
Headwise Selected-Layer Output Authority /
TensorCube Handoff Authority Preservation /
No Loss·Backward·Optimizer Seal
```

If R5 already achieves the stronger Headwise-adapter PASS, the next patch becomes:

```text
ASH-BASETRAIN-ATLAS-WAVE-03

TensorCube Stage10 Live QK Binding /
Headwise or Oracle Context Parity /
Online Softmax Stage11 Admission /
V Weighted Accumulation Stage12 Admission /
No OProj·Loss·Backward Seal
```

R5 must not skip its own truth boundary merely to reach Stage10 earlier.

The accepted order is:

```text
live residency truth
  -> shader ABI truth
  -> explicit parameter truth
  -> staged arithmetic truth
  -> numerical truth
  -> executor naming truth
  -> live handoff truth
  -> TensorCube execution later
```
