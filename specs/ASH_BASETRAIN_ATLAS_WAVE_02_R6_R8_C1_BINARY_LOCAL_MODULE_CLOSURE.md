# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8-C1

## Binary-Local Canonical Runtime Module Closure / Crate-Root Export Independence / Same-Process R6-R6→R6-R7→R6-R8 Chain Preservation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8` / Pass30  
> Failure class: Rust compile-surface export visibility  
> Runtime semantics: unchanged  
> Physical admission: `HOLD`

## Observed failure

```text
error[E0432]: unresolved import
orchestrator_local::base_train_atlas_wave_02_r6_r8_layer1_live_body
```

The distributed Pass30 archive contains the R6-R8 runtime source and the feature-gated `orchestrator_local/src/lib.rs` declaration. The operator-side build nevertheless resolved a library compile surface without that module.

## Closure

The R6-R8 gate no longer depends on the `orchestrator_local` library crate export. It directly declares the canonical runtime source files as binary-root modules:

```rust
#[path = "../base_train_atlas_wave_02_r6_r6_runtime.rs"]
mod base_train_atlas_wave_02_r6_r6_runtime;
#[path = "../base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs"]
mod base_train_atlas_wave_02_r6_r7_layer_weight_residency;
#[path = "../base_train_atlas_wave_02_r6_r8_layer1_live_body.rs"]
mod base_train_atlas_wave_02_r6_r8_layer1_live_body;
```

The gate imports the runner from the binary-local canonical module:

```rust
use self::base_train_atlas_wave_02_r6_r8_layer1_live_body::
    run_r6_r8_layer1_live_body_session;
```

## Authority preservation

This patch does not copy or fork the runtime implementation. It reuses the same canonical files and preserves the existing module chain:

```text
R6-R8 -> crate::R6-R7
R6-R7 -> crate::R6-R6
R6-R6 -> canonical artifact wave map
```

Preserved contracts:

```text
same process = true
same WGPU device/queue lineage = true
same weight residency slot = true
same hidden authority slot = true
subprocess count = 0
shadow runtime implementation count = 0
alternate state authority count = 0
```

## Changed source

Semantic change:

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate.rs
```

The overlay also carries the four canonical runtime dependency files atomically so the path declarations cannot target missing files.

## Preserved R6-R8 semantics

```text
resident layer-1 weight lease consumption
layer-1 hidden read lease consumption
re-embedding count = 0
weight reload count = 0
block rebuild count = 0
actual layer-1 RMSNorm/QKV/W5/W6/W7/OProj/MLP
GPU completion before lease release
layer-2 hidden single commit
payload readback count = 0
```

No WGSL, Cargo feature, CLI, parity tolerance, receipt schema or runtime state transition changes.

## Static validation

```text
binary-local R6 path declaration = PASS
binary-local R6-R7 path declaration = PASS
binary-local R6-R8 path declaration = PASS
orchestrator_local crate import in gate = 0
binary-local runner import = PASS
R6-R7 -> crate::R6-R6 reference = PASS
R6-R8 -> crate::R6-R7 reference = PASS
R6-R6 artifact wave-map path = PASS
R6-R6/R6-R7/R6-R8 runner presence = PASS
raw delimiter scan = PASS
semantic changed file count = 1
overlay dependency closure files = 5
```

Cargo, rustc and rustfmt were unavailable in the bake environment. Operator-side Cargo check and physical GPU execution remain admission gates.

## Commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p orchestrator_local
```

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r8.args"
```
