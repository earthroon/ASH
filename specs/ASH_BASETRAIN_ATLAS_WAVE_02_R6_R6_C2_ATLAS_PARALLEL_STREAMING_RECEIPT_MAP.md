# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C2

## Atlas Parallel Streaming Receipt Map / Macro Recursion Retirement / Deterministic Wave-Lane Merge Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C1`  
> Observed failure: `recursion limit reached while expanding $crate::json_internal!`  
> Scope: final receipt and local manifest construction  
> BaseTrain live admission: `HOLD` until physical rerun

## 0. Failure

The R6-R6 live-body gate constructed the 56-field final receipt through one nested `serde_json::json!` invocation.

```text
error: recursion limit reached while expanding $crate::json_internal!
```

Increasing the crate recursion limit is rejected because it keeps the monolithic macro as the receipt SSOT and only moves the compiler ceiling.

## 1. Repair architecture

R6-R6 receives a dedicated artifact builder:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_artifact_wave_map.rs
```

Canonical builder:

```text
AtlasParallelStreamingWaveMap
AtlasWaveLane
```

Construction model:

```text
lane
  -> owns typed key/value entries
  -> serializes values before worker launch
  -> sorts keys lexicographically
  -> produces one independent JSON fragment

wave
  -> launches lane workers in parallel
  -> joins every lane fail-closed
  -> sorts fragments by lane ordinal
  -> merges fragments streamingly into the root map

artifact
  -> accepts waves in exact ordinal order
  -> rejects duplicate lane ordinal/name
  -> rejects duplicate root key
  -> adds artifactWaveMap construction receipt
```

Deterministic merge order:

```text
wave ordinal
  -> lane ordinal
  -> lexicographic key
```

## 2. Final receipt waves

```text
wave 0 identity-and-authority
  lane 0 identity
  lane 1 authority

wave 1 attention-and-body-dispatch
  lane 0 attention-dispatch
  lane 1 body-dispatch

wave 2 parity-and-replay
  lane 0 parity
  lane 1 deterministic-replay

wave 3 closure
  lane 0 closure
```

The pre-C2 final receipt contained 56 semantic fields. C2 contains the same 56 fields before adding `artifactWaveMap` and `receiptDigest`.

```text
missing fields = 0
extra semantic fields = 0
duplicate semantic fields = 0
```

## 3. Local manifest waves

```text
wave 0 identity-and-authority
  lane 0 identity
  lane 1 authority

wave 1 dispatch-and-parity
  lane 0 dispatch
  lane 1 parity-and-commit

wave 2 artifacts-and-closure
  lane 0 artifacts
  lane 1 closure
```

The pre-C2 manifest contained 56 semantic fields. C2 preserves all 56 fields before construction metadata and final sealing.

## 4. Fail-closed rules

```text
wave ordinal mismatch -> failure
empty wave -> failure
duplicate lane ordinal -> failure
duplicate lane name -> failure
duplicate key inside lane -> failure
duplicate key across lanes/waves -> failure
lane worker panic -> failure
reserved artifactWaveMap collision -> failure
missing final receipt digest -> failure
```

No duplicate key is overwritten silently.

## 5. Forbidden workaround

```text
#![recursion_limit = "256"] = forbidden
larger monolithic json! object = forbidden
manual key overwrite fallback = forbidden
unordered HashMap merge = forbidden
receipt field loss = forbidden
```

## 6. Changed source

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_artifact_wave_map.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
```

## 7. Preserved runtime semantics

```text
R6-R6 live writer authority unchanged
actual decoder block unchanged
QKV/W4/W5/W6/W7 unchanged
OProj and MLP unchanged
layer-1 hidden CAS unchanged
rollback contract unchanged
receipt field names and values unchanged
manifest field names and values unchanged
receiptDigest sealing unchanged
```

Only artifact construction and merge ownership change.

## 8. Static validation

```text
final semantic field parity = 56 / 56
manifest semantic field parity = 56 / 56
final duplicate semantic key count = 0
manifest duplicate semantic key count = 0
monolithic final json! count = 0
recursion_limit attribute count = 0
R6-R6 dedicated wave-map module present = PASS
Rust delimiter balance = PASS
ZIP integrity = PASS
.sha256 sidecar count = 0
```

Rust type-check and physical GPU execution remain user-side gates because the bake environment does not contain Cargo or rustc.

## 9. Commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args"
```
