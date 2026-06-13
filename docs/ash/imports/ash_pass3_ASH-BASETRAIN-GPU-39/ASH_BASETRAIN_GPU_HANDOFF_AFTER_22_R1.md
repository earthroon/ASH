# ASH-BASETRAIN-GPU-22-R1 Handoff

## Current SSOT

- Source patch: `ASH-BASETRAIN-GPU-22`
- Repair patch: `ASH-BASETRAIN-GPU-22-R1`
- Purpose: split one giant `serde_json::json!` top-level bundle into segmented section `Value` builders plus shallow `serde_json::Map` assembly.

## Fixed Blocker

```txt
compile_error = recursion limit reached while expanding `$crate::json_internal!`
blocker_scope = giant top-level json! receipt bundle
```

## Preserved Values

```txt
local_nll_loss = 7.624619041439192
local_logsumexp = 7.624618969470094
target_logit = -0.00000007196909734830115
formula_epsilon = 0.000000000001
payload_digest_hex = 856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052
```

## Boundary

```txt
new_loss_computed = false
new_gpu_dispatch = false
new_readback = false
backward = false
optimizer = false
safetensors_mutation = false
```

## Operator Commands

```powershell
cd "D:\1111113232\DUST\1\ash_pass3"
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"
cargo build -p base_train --bin ash_basetrain_gpu_22_loss_scalar_audit --jobs 1
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_22_loss_scalar_audit
```

## Next Step

If local build/run passes, proceed to:

```txt
ASH-BASETRAIN-GPU-23
Loss Repeatability Audit /
Repeated Local Window Target 1 Loss Scalar Stability No Backward No Optimizer Seal
```
