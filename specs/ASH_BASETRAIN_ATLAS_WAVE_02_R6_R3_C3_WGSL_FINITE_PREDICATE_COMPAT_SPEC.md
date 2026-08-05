# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C3

## WGSL Finite Predicate Compatibility Closure

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C2`  
> Runtime: `wgpu 26.0.1 / naga WGSL parser`  
> Production admission: blocked  
> Proof ledger: HOLD

## SSOT

R6-R3 Stage11 shaders must not call the undefined WGSL identifier `isFinite`. Every R6-R3 finite-value check is owned by one local IEEE-754 exponent predicate with identical NaN and infinity rejection semantics.

```wgsl
fn finite_f32(value: f32) -> bool {
    let exponent = bitcast<u32>(value) & 0x7f800000u;
    return exponent != 0x7f800000u;
}
```

## Patched shaders

```text
base_train_atlas_wave_02_r6_r3_stage11_candidate_merge.wgsl
base_train_atlas_wave_02_r6_r3_stage11_oracle_merge.wgsl
base_train_atlas_wave_02_r6_r3_stage11_global_verify.wgsl
base_train_atlas_wave_02_r6_r3_stage11_invariant_verify.wgsl
base_train_atlas_wave_02_r6_r3_stage11_known_vector_fixture.wgsl
```

## Required invariants

```text
R6-R3 isFinite identifier count = 0
finite_f32 helper count per patched shader = 1
NaN rejected = true
positive infinity rejected = true
negative infinity rejected = true
finite normal/subnormal/zero accepted = true
candidate/oracle predicate identity = exact
verifier/fixture predicate identity = exact
Stage11 algorithm and receipt ABI mutation = 0
```

## Forbidden substitutions

- increasing Rust recursion or macro limits
- using a host-side finite check instead of shader validation
- dropping nonfinite flags or verifier counters
- treating infinity as masked data outside the existing masked-record branch
- patching only the first shader that fails

## Build command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r3_stage11_online_softmax_merge_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r3.args"
```
