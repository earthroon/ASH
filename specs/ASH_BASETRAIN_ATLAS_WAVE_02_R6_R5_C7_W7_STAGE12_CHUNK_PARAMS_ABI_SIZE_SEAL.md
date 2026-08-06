# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C7

## W7 Stage12 Chunk Params ABI Size Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C6`  
> Observed runtime failure: `W7Stage12ChunkParamsAbiMismatch`  
> Scope: pipeline self-check constant repair only  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Root cause

C6 extended `TensorCubeStage12ChunkParams` with `input_layout_code` and three pad words.

The canonical Rust and WGSL layouts are:

```text
21 semantic u32 words
3 padding u32 words
24 total u32 words
24 * 4 bytes = 96 bytes
```

Both Stage12 shaders already declared the same 24-word `Params` layout. The pipeline identity also measured the Rust structure dynamically through `size_of::<TensorCubeStage12ChunkParams>()`.

The only stale surface was the runtime admission constant:

```rust
ensure!(identity.chunk_params_bytes == 80, "W7Stage12ChunkParamsAbiMismatch");
```

This rejected the correct 96-byte structure before any W7 dispatch.

## 1. Repair

```rust
ensure!(identity.chunk_params_bytes == 96, "W7Stage12ChunkParamsAbiMismatch");
```

## 2. Preserved surfaces

C7 does not change:

```text
W7 candidate shader
W7 oracle shader
W7 Q/K/V layout indexing
uniform field order
bind-group layout
dispatch geometry
W5/W6/W7 identity propagation
QKV source ownership
context or OProj parity
Headwise writer authority
residual, MLP or next-layer HOLD
production or training promotion state
```

## 3. Static validation

```text
Rust TensorCubeStage12ChunkParams words = 24
Rust TensorCubeStage12ChunkParams bytes = 96
candidate WGSL Params words = 24
candidate WGSL Params bytes = 96
oracle WGSL Params words = 24
oracle WGSL Params bytes = 96
stale 80-byte W7 check count = 0
96-byte W7 admission check count = 1
Rust/WGSL ABI static agreement = PASS
```

Rust type-check, WGSL module creation and physical GPU parity remain user-side gates.

## 4. Commands

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
