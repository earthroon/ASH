# ASH-BASE-TRAIN-P1B-R1A3-R1-PROVIDER-CUT-RETIREMENT-CONSUMER-DEMAND-BOUNDARY-BISECTION

## PROVIDER-CUT RETIREMENT + CONSUMER DEMAND-BOUNDARY BISECTION + CRATE-WIDE EDGE LEDGER

### Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A3-R1-PROVIDER-CUT-RETIREMENT-CONSUMER-DEMAND-BOUNDARY-BISECTION

Direct parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A3_CURRENT_PRODUCTION_INTERNAL_CLASSIFICATION_CODE_ONLY.zip

Class:
DIAGNOSTIC ARCHITECTURE CORRECTION
PROVIDER-CUT RETIREMENT
CONSUMER DEMAND-BOUNDARY ATTRIBUTION
RUST-ONLY
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

### Parent evidence

R1A2-R1B already established `CanonicalBaseline=SameE0275`, `BisectControl=SameE0275`, `CurrentProductionCut=BuildPass`, `CurrentProductionClosureRequired`. R1A3 MCU/Muon/Scheduler provider-removal subcuts produced compile-time unresolved-import cascades and are classified `InvalidSlice`; the previous static closure claim is superseded by Rust compile evidence.

### Provider-cut retirement

The legacy features `p1br1a3-cut-current-mcu`, `p1br1a3-cut-current-muon`, and `p1br1a3-cut-current-scheduler-session` remain Cargo lineage names only. Their `lib.rs` module gates are removed and the observer rejects the retired `current-production-internal` path. Provider modules remain compiled.

### Crate-wide edge ledger

Added `crates/base_train/src/current_production_demand_edge_ledger_p1b_r1a3_r1.rs`. The committed Rust ledger contains 450 source-visible compile edges whose provider belongs to the 136-member CurrentProduction parent universe, combining direct `crate::module` paths, grouped `use crate::{...}` paths, and previously materialized root-symbol edges.

Correction to the earlier working hypothesis: under this source-visible ledger the observed consumers are inside the 136-member parent universe. The provider-cut failure is therefore attributed to low-resolution reverse-closure convergence inside the parent graph, not to a proven outside-parent consumer set.

### Demand-boundary candidates

Only two source-proven candidate boundaries are materialized:

```text
D001
feature: p1br1a3r1-cut-demand-001
consumer: pipeline::p1br1a3r1_run_streaming_train_backend_boundary
site: run_base_training_loop_streaming::<TrainBackend>

D002
feature: p1br1a3r1-cut-demand-002
consumer: pipeline::p1br1a3r1_run_batch_train_backend_boundary
site: run_base_training_loop::<TrainBackend>
```

`TrainBackend` remains `Autodiff<Wgpu<f32, i32>>`. Both boundaries are recorded as associated-type/generic backend monomorphization surfaces for `<Autodiff<Wgpu<f32, i32>> as Backend>::FloatTensorPrimitive` with demand class `SendSync`. No speculative D003 is added.

### Boundary law

Each new feature changes only the exact pipeline consumer boundary. The feature-enabled branch returns a typed diagnostic HOLD and does not substitute a second backend or runtime path. No MCU, Muon, scheduler, config, checkpoint, storage, or WGPU provider module is cfg-removed by the new features.

### Observer

Added `crates/ash_p1br1a2_release_observer/src/demand_r1a3_r1.rs` and CLI `current-production-demand`. The suite runs seven stages: dependency controls, canonical baseline, bisect control, CurrentProduction coarse anchor, D001, and D002. It inherits R1A2-R1B exact package/target identity, `--message-format=json`, source/toolchain/environment/metadata binding, canonical `SameE0275`, and `InvalidSlice` precedence.

Promotion law:

```text
exactly one boundary BuildPass
  -> ExactDemandBoundaryIsolated(D001|D002)

both BuildPass
  -> MultipleDemandBoundariesRemoveReproducer

both SameE0275
  -> DemandBoundarySetIncomplete

InvalidSlice/WrongTarget/other structural failure
  -> HoldInvalidBoundary

DifferentE0275
  -> HoldDifferentE0275
```

### E0282 hold

E0282 errors observed under invalid provider cuts remain `UNKNOWN` as independent defects. R1A3-R1 adds no type annotations for them; they are only promoted as separate bugs if reproduced in the normal graph or a structurally valid demand-boundary treatment.

### Actual source delta

```text
ADD 2
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/current_production_demand_edge_ledger_p1b_r1a3_r1.rs
crates/ash_p1br1a2_release_observer/src/demand_r1a3_r1.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

### Static qualification

```text
old provider-cut gates in lib.rs       0
new demand features                    2
crate-wide CurrentProduction edges     450
provider modules retained              PASS
D001/D002 exact feature surfaces       PRESENT
balanced braces/parens/brackets        PASS
external Python/PowerShell loader      0
```

These are SOURCE/STATIC checks only. Cargo/rustc are unavailable in the bake environment, so observer compile/tests and release treatments were not run.

### Artifacts

```text
Overlay:
ASH_BASE_TRAIN_P1B_R1A3_R1_PROVIDER_CUT_RETIREMENT_CONSUMER_DEMAND_BOUNDARY_OVERLAY_CODE_ONLY.zip
SHA-256: 16dea19eaae3c19277fbfb2d0eb9198b21902d275d3fe3fd457950b48ee7fa28
Files: 7
CRC: PASS

Full:
ASH_PASS3_BASE_TRAIN_P1B_R1A3_R1_PROVIDER_CUT_RETIREMENT_CONSUMER_DEMAND_BOUNDARY_CODE_ONLY.zip
SHA-256: f45e588993545601b17d3346c52b63f292617f642f290e072d0495a14c6aacea
Files: 8,563
CRC: PASS
```

Both ZIPs exclude generated `specs/`, `docs/`, `artifacts/`, `target/`, and `.ps1` paths. No new Python or PowerShell loader is included.

### User-side qualification

```powershell
cargo clean
cargo test -p ash_p1br1a2_release_observer --release
cargo test -p base_train --lib
cargo run -p ash_p1br1a2_release_observer --release -- current-production-demand
```

Expected progress is `[P1B-R1A3-R1][1/7]` through `[7/7]`. No boundary result is predeclared.

### Stop law

Once one exact demand boundary produces the canonical `SameE0275 -> BuildPass` relation under stable controls, broad bisection stops and the next revision repairs only that proven consumer boundary.
