# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D2

## Atlas Parallel Streaming Wave Map Receipt Closure / serde_json Macro Recursion Retirement / Deterministic Lane Merge Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D1`  
> Observed failure: `recursion limit reached while expanding $crate::json_internal!` at the R6-R9 C1 final receipt  
> Failure class: monolithic artifact-construction macro expansion  
> Runtime decoder semantics: unchanged  
> Layer-2 canary window: unchanged  
> Proof ledger: `HOLD` until physical rerun

## 1. Failure

R6-R9 C1 built transaction, final receipt and local manifest with monolithic `serde_json::json!` objects. The final receipt crossed the compiler macro-recursion ceiling.

Increasing `#![recursion_limit]` is forbidden because it preserves the monolithic artifact constructor and merely moves the compiler ceiling.

## 2. Closure architecture

Add:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_artifact_wave_map.rs
```

Canonical builder:

```text
AtlasParallelStreamingWaveMap
AtlasWaveLane
```

Each lane serializes its typed entries before worker launch. Lanes in the same wave build JSON fragments in parallel workers. Fragments are joined fail-closed, sorted by lane ordinal, and merged into the root map streamingly. Waves must arrive in exact ordinal order.

Deterministic merge order:

```text
wave ordinal
  -> lane ordinal
  -> lexicographic key
```

Duplicate lane keys, lane ordinals, lane names, root keys and reserved `artifactWaveMap` collisions fail closed.

## 3. Transaction receipt waves

```text
wave 0 identity-and-weight-transition
  lane 0 identity
  lane 1 weight-transition

wave 1 hidden-transition-and-closure
  lane 0 hidden-transition
  lane 1 closure
```

Semantic field parity against C1-D1:

```text
old fields = 17
new fields = 17
missing = 0
extra semantic fields = 0
```

`artifactWaveMap` is construction metadata and is not counted as a pre-existing semantic field.

## 4. Final receipt waves

```text
wave 0 identity-and-window
  lane 0 identity
  lane 1 execution-window

wave 1 weight-and-hidden-authority
  lane 0 weight-authority
  lane 1 hidden-authority

wave 2 execution-and-residency
  lane 0 execution
  lane 1 residency

wave 3 provenance-and-admission
  lane 0 provenance
  lane 1 admission
```

Semantic field parity against C1-D1:

```text
old fields = 43
new fields = 43
missing = 0
extra semantic fields = 0
```

## 5. Local manifest waves

```text
wave 0 identity-and-window
  lane 0 identity
  lane 1 execution-window

wave 1 final-state-and-evidence
  lane 0 final-state
  lane 1 evidence-and-closure
```

Semantic field parity against C1-D1:

```text
old fields = 13
new fields = 13
missing = 0
extra semantic fields = 0
```

## 6. Forbidden workarounds

```text
#![recursion_limit = "256"] or larger = forbidden
monolithic replacement json! object = forbidden
unordered HashMap merge = forbidden
duplicate-key overwrite = forbidden
receipt field deletion = forbidden
manifest field deletion = forbidden
```

R6-R9 coordinator source must contain zero `json!(` macro sites after D2.

## 7. Preserved C1 runtime semantics

```text
first target layer = 2
max layer steps = 1
weight generation = 1 -> 2
hidden generation = 2 -> 3
final weight layer = 2
final hidden layer = 3
auto continuation = 0
re-embedding = 0
all-layer preload = 0
next-layer prefetch = 0
payload readback = 0
production inference = BLOCKED
backward = BLOCKED
optimizer = BLOCKED
```

D2 changes artifact construction only. It does not alter decoder execution, checkpoint loading, residency state transitions, Headwise W5/W6/W7, WGSL, or CLI values.

## 8. Revision identity

```text
patchId = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D2
buildRevision = r6-r9-c1-d2-atlas-parallel-streaming-wave-map-v1
waveMapSchema = ash.basetrain.atlas_wave.02.r6_r9.c1.artifact.parallel_streaming_wave_map.v1
waveMapRevision = R6-R9-C1-D2-atlas-parallel-streaming-wave-map-v1
```

## 9. Changed code surface

Semantic changes:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_artifact_wave_map.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
```

The overlay also carries the already-required atomic distribution surface:

```text
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

## 10. Static validation

```text
R6-R9 json! macro site count = 0
recursion_limit workaround count = 0
transaction semantic field parity = 17 / 17
final receipt semantic field parity = 43 / 43
manifest semantic field parity = 13 / 13
transaction wave count = 2
transaction lane count = 4
final receipt wave count = 4
final receipt lane count = 8
manifest wave count = 2
manifest lane count = 4
deterministic wave/lane/key merge = present
duplicate key fail-closed = present
Rust lexical delimiter scan = PASS
WGSL semantic changed file count = 0
```

Cargo, rustc and rustfmt are unavailable in the bake environment. Cargo type-check and physical WGPU execution remain operator-side gates.

## 11. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## Seal

> R6-R9 C1-D2 does not raise the macro ceiling. It removes the monolithic JSON constructor and replaces artifact assembly with parallel lane construction plus deterministic streaming wave merge while preserving every C1 semantic field.
