# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C5

## HeadwiseAtlasInputLayout Owner Import Repair

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C4`  
> Scope: Rust import ownership repair only  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Failure

```text
error[E0432]: unresolved import burn_webgpu_backend::HeadwiseAtlasInputLayout
```

Affected source:

```text
crates/model_core/src/headwise_texture_06_live_binding.rs
```

## 1. SSOT ownership

`HeadwiseAtlasInputLayout` is declared in:

```text
burn_webgpu_backend::headwise_atlas::HeadwiseAtlasInputLayout
```

It is not re-exported from the backend crate root.

The adjacent Texture06 runtime types remain valid crate-root exports:

```text
HeadwiseTexture06ChunkSlotGpu
HeadwiseTexture06ChunkUploadPipeline
NativeWgpuRuntimeHandles
PreparedAtlasInputs
RawWgpuBufferLease
```

## 2. Repair

```rust
use burn_webgpu_backend::{
    HeadwiseTexture06ChunkSlotGpu, HeadwiseTexture06ChunkUploadPipeline,
    NativeWgpuRuntimeHandles, PreparedAtlasInputs, RawWgpuBufferLease,
};
use burn_webgpu_backend::headwise_atlas::HeadwiseAtlasInputLayout;
```

No new crate-root re-export is introduced.

## 3. Semantic boundary

This patch changes one import path only. It does not change:

```text
BHQD/BQHD shape admission
BQHD direct texture-pack indexing
K/V source leases
Texture06 upload modes
W5/W6/W7 candidate behavior
R6 shadow behavior
Headwise writer authority
context or OProj parity
residual, MLP or next-layer HOLD
production or training promotion state
```

## 4. Static validation

```text
owner enum declaration present = PASS
invalid backend-root import count in changed ASH source = 0
owner-module import count = 1
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
