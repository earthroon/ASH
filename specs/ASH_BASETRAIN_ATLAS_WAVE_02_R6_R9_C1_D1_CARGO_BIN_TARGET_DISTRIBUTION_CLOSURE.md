# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D1

## Cargo Bin Target Distribution Closure / Overlay Cargo Surface Reapplication / C1 Logic Preservation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1`  
> Observed failure: `error: no bin target named ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate`  
> Failure class: overlay distribution surface omission  
> Runtime semantics: unchanged  
> Proof ledger: `HOLD`

## Observed state

The C1 full baked tree contains the canonical `[[bin]]` registration for:

```text
ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate
```

but the C1 overlay distributed only:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Applying that overlay onto a working tree whose `crates/orchestrator_local/Cargo.toml` predates the R6-R9 target leaves the source present but invisible to Cargo.

## Closure

The D1 overlay must atomically carry:

```text
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Required Cargo declaration:

```toml
[[bin]]
name = "ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate"
path = "src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs"
required-features = ["orchestrator_tcu_audit_bins"]
```

## Preserved C1 semantics

D1 does not change:

```text
first target layer = 2
max layer steps = 1
final weight layer = 2
final hidden layer = 3
weight generation 1 -> 2
hidden generation 2 -> 3
auto continuation = 0
no re-embedding
no all-layer preload
no next-layer prefetch
no payload readback
production inference / backward / optimizer blocked
```

No coordinator algorithm, decoder body, checkpoint loader, WGSL, authority transition, receipt schema, or CLI value is changed by D1.

## Distribution validation

```text
D1 overlay Cargo.toml present = true
R6-R9 bin target declaration present = true
required feature = orchestrator_tcu_audit_bins
C1 coordinator source present = true
C1 gate source present = true
C1 CLI present = true
.md in code ZIPs = 0
.sha256 in code ZIPs = 0
manifest JSON in code ZIPs = 0
artifacts/ in code ZIPs = 0
manifests/ in code ZIPs = 0
```

Cargo type-check and physical WGPU execution remain operator-side gates.

## Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## Seal

> C1-D1 changes only distribution completeness: if the R6-R9 gate source is present in an overlay, its Cargo bin target registration must travel with it atomically.
