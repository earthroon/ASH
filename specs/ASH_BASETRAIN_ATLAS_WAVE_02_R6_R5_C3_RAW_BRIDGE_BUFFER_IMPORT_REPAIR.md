# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C3

## Raw Bridge BackendBuffer Import Repair

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C2`  
> Scope: Rust import ownership repair only  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Failure

```text
error[E0432]: unresolved import burn_webgpu_backend::BackendBuffer
```

Affected source:

```text
crates/model_core/src/attention_context_layout_tag.rs
```

## 1. SSOT ownership

`BackendBuffer` is owned by:

```text
burn_webgpu_backend::raw_bridge::BackendBuffer
```

The following adjacent types remain valid crate-root re-exports:

```text
HeadwisePreOutputProjectionContextHandle
RawWgpuBufferLease
TensorCubeStage12ContextCandidateHandle
```

## 2. Repair

```rust
use burn_webgpu_backend::{
    HeadwisePreOutputProjectionContextHandle, RawWgpuBufferLease,
    TensorCubeStage12ContextCandidateHandle,
};
use burn_webgpu_backend::raw_bridge::BackendBuffer;
```

No crate-root re-export is added.

## 3. Semantic boundary

This patch changes one import path only. It does not change:

```text
context buffer type
layout or physical strides
source generation or completion
same-device adoption
context/OProj parity arithmetic
Headwise writer authority
residual, MLP or next-layer HOLD boundaries
production or training promotion state
```

## 4. Static validation

```text
canonical raw_bridge BackendBuffer alias present = PASS
model_core root BackendBuffer import count = 0
R6-R5 new source root BackendBuffer import count = 0
Rust delimiter balance = PASS
ZIP integrity = PASS
```

Rust type-check and physical GPU execution remain user-side gates.

## 5. Commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r5.args"
```
