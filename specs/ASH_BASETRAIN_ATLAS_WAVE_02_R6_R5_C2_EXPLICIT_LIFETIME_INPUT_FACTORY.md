# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C2

## Explicit Lifetime Input Factory Compile Closure

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C1`  
> Scope: Rust lifetime inference repair only  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

`AttentionInterconnectW8ContextCompareInput<'a>` borrows the invocation identity, Headwise context handle, TensorCube context handle and row-classification handle under one shared lifetime. R6-R5 must express that relationship explicitly in a named function signature.

## 1. Compile failure

```text
error: lifetime may not live long enough
```

The local closure accepted `identity: &str` and `reference: &HeadwisePreOutputProjectionContextHandle`, captured W7 references from the outer scope, and returned `AttentionInterconnectW8ContextCompareInput<'_>`. Rust inferred independent lifetimes for those references and could not prove that each one outlived the single lifetime required by the returned input type.

## 2. Repair

The closure is replaced with:

```rust
#[allow(clippy::too_many_arguments)]
fn make_w8_context_compare_input<'a>(
    reference: &'a HeadwisePreOutputProjectionContextHandle,
    tensorcube: &'a TensorCubeStage12ContextCandidateHandle,
    row_classification: &'a TensorCubeStage12ContextRowClassificationHandle,
    absolute_tolerance: f32,
    relative_tolerance: f32,
    relative_floor: f32,
) -> AttentionInterconnectW8ContextCompareInput<'a>
```

The invocation identity is borrowed from the same reference handle:

```rust
invocation_identity_digest: reference.invocation_identity_digest.as_str()
```

This prevents identity/context ownership drift and gives the compiler one explicit lifetime for every borrowed field in the W8 input.

## 3. Affected source

```text
crates/burn_webgpu_backend/src/attention_context_layout_compare.rs
```

## 4. Preserved semantics

```text
Headwise-R6 BHQD comparison unchanged
Headwise-W7 layout-aware comparison unchanged
R6-W7 layout-aware comparison unchanged
comparison pair count = 3
all tolerance values unchanged
context layout and stride contracts unchanged
context payload readback prohibition unchanged
OProj behavior unchanged
Headwise writer authority unchanged
residual/MLP/next-layer HOLD unchanged
production/training promotion state unchanged
```

## 5. Static validation

```text
local lifetime-returning closure removed = PASS
explicit named lifetime helper present = PASS
Headwise/TensorCube/row references share 'a = PASS
identity borrowed from Headwise reference handle = PASS
Rust delimiter count balance = PASS
ZIP integrity = PASS
```

The bake environment does not contain Rust tooling, so Rust type-check and physical GPU execution remain user-side gates.

## 6. Commands

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
