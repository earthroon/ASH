# ASH-BASETRAIN-GPU-70K-G208B0-R1 Lifetime Hotfix

PatchId: `ASH-BASETRAIN-GPU-70K-G208B0`  
HotfixId: `ASH-BASETRAIN-GPU-70K-G208B0-R1`  
SourcePackage: `ash_pass3_ASH-BASETRAIN-GPU-70K-G208B0_rc_evaluation_phase_entry_baked_no_artifacts_no_ps1_no_py.zip`  
TargetRuntimeBinary: `ash_basetrain_gpu_70k_g208b0_rc_evaluation_phase_entry`

## Purpose

R1 fixes Rust `E0521` borrowed data escaping from `artifact_payload(args, filename)` into `common_receipt(args, filename)`.

The original writer declared:

```rust
fn common_receipt(args: &Args, artifact: &'static str) -> Value
```

but `artifact_payload` passes `filename: &str`, whose lifetime is only valid inside the function body. Because `common_receipt` required `&'static str`, Rust correctly rejected the call.

## Fix

The receipt helper now accepts a normal borrowed string slice:

```rust
fn common_receipt(args: &Args, artifact: &str) -> Value
```

`artifact` is immediately copied into a JSON `Value::String` through `value_s(artifact)`, so no borrowed reference escapes into the returned JSON object.

## Scope

- No runtime artifact was prebaked.
- No CLI contract was changed.
- No PASS target was changed.
- No RC-1 policy was changed.
- No eval policy was changed.
- No deployment or quality claim was added.
- No checkpoint/safetensors/base weight mutation was added.

## Static Surface

```text
target_writer_json_macro_count=0
target_writer_recursion_limit_count=0
common_receipt_static_artifact_lifetime_count=0
common_receipt_str_artifact_signature=true
runtime_outputs_prebaked=0
```
