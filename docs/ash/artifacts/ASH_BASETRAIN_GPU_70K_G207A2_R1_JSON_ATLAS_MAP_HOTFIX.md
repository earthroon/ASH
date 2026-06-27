# ASH-BASETRAIN-GPU-70K-G207A2 R1 Hotfix

## JSON Atlas Map Writer / No serde_json json Macro / No Recursion Limit Patch

PatchId: `ASH-BASETRAIN-GPU-70K-G207A2`  
HotfixId: `G207A2-R1-JSON-ATLAS-MAP`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A1`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A3`

## Trigger

Local compile hit a serde JSON macro expansion limit:

```text
error: recursion limit reached while expanding `$crate::json_internal!`
```

The failure happened at the large G207A2 receipt object built with `serde_json::json!`.

## Decision

Do not increase `#![recursion_limit]`.

Use a JSON atlas map writer instead:

```text
serde_json::Map
json_atlas(...)
serde_json::to_vec_pretty
```

## Fix

The G207A2 Rust writer removes `serde_json::json!` and replaces large JSON macro objects with explicit map assembly:

```text
fn json_atlas(fields: Vec<(&'static str, Value)>) -> Value
```

Small helper slots are used for field insertion:

```text
s(key, value)
b(key, value)
u(key, value)
f(key, value)
arr(key, values)
```

## Static Checks

```text
serde_json_json_macro_count=0
recursion_limit_attribute_count=0
serde_json_map_import_present=true
json_atlas_writer_present=true
runtime_outputs_absent_from_zip=true
ps1_count=0
py_count=0
sha256_count=0
```

## Local Artifact Policy

Runtime artifacts remain local-only. The baked ZIP does not include G207A2 runtime receipt or audit JSON outputs.

## Expected Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a2_active_freshinit_backward_optimizer_smoke -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A1 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --tiny-batch-mode deterministic `
  --freshinit-forward-mode execute `
  --loss-mode finite `
  --backward-mode execute `
  --optimizer-step-mode execute `
  --weight-delta-mode scoped `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A3
```

## Non-Goals

```text
recursion_limit_workaround
production_base_weight_mutation
checkpoint_rewrite
safetensors_rewrite
route_pointer_rewrite
atlas_route_execution
tensorcube_enable
training_quality_claim
deployment_ready_claim
```
