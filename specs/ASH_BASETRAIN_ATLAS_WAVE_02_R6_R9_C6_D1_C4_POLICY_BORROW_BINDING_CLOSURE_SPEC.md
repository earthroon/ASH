# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6-D1

## C4 Policy Borrow Binding Closure / Planner API Reference Contract Preservation / No C6 Semantic Change Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6`  
> Failure class: Rust compile-time argument binding mismatch (`E0308`)  
> Runtime semantics: unchanged  
> C6 destructive transaction semantics: unchanged  
> C4 planner semantics: unchanged

### Observed compiler failure

```text
expected `&DecoderWeightAtlasWavePackingPolicy`
found `DecoderWeightAtlasWavePackingPolicy`
```

The canonical C4 planner API is:

```rust
pub fn plan_decoder_weight_atlas_waves(
    authority: &BaseTrainAtlasWave02R5CheckpointTensorSetAuthority,
    target_layer: u32,
    policy: &DecoderWeightAtlasWavePackingPolicy,
) -> Result<DecoderWeightAtlasWavePlan>
```

C6 incorrectly passed the local policy by value.

### Exact closure

Before:

```rust
let plan = plan_decoder_weight_atlas_waves(
    &runtime.checkpoint,
    c6_policy.target_layer,
    c4_policy,
)?;
```

After:

```rust
let plan = plan_decoder_weight_atlas_waves(
    &runtime.checkpoint,
    c6_policy.target_layer,
    &c4_policy,
)?;
```

### Semantic invariants

C6-D1 changes only ownership at the call boundary. It does not clone, mutate, replace, or rebuild the C4 policy.

Required unchanged behavior:

```text
fresh R6-R8 source session
source completion binding
C4 metadata-only preflight before destruction
exclusive destructive source extraction
source drop + device completion wait
VacantForRebind before C5 staging
C5 three-wave / nine-lane staging
nine-role complete seal
atomic Layer2 adoption
generation 1 -> 2
hidden Layer2 / generation2 unchanged
legacy full-layer loader = 0
legacy fallback = 0
target forward = 0
```

### Changed file

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c6_layer2_wave_rebind.rs
```

### Static closure

```text
C4 planner policy parameter type = &DecoderWeightAtlasWavePackingPolicy
C6 call passes &c4_policy = true
old by-value call count = 0
semantic changed line count = 1
C4 planner implementation change = 0
C5 staging implementation change = 0
residency state-machine change = 0
WGSL semantic change = 0
```

### Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

### Seal

> C6-D1 only restores the reference contract already owned by the C4 planner API: the C6 local packing policy is borrowed as `&c4_policy`; no runtime, planning, staging, rebind, recovery, or numerical semantics change.
