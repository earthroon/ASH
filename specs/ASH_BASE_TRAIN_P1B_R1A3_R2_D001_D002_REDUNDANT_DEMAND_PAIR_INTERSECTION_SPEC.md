# ASH-BASE-TRAIN-P1B-R1A3-R2-D001-D002-REDUNDANT-DEMAND-PAIR-INTERSECTION

## D001 / D002 REDUNDANT DEMAND-PAIR INTERSECTION
## + COMMON TRAINBACKEND OBLIGATION ATTRIBUTION
## + PROVIDER-PRESERVING JOINT TREATMENT

### 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A3-R2-D001-D002-REDUNDANT-DEMAND-PAIR-INTERSECTION

Short name:
P1B-R1A3-R2

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A3_R1_PROVIDER_CUT_RETIREMENT_CONSUMER_DEMAND_BOUNDARY_CODE_ONLY.zip

Class:
DEMAND-BOUNDARY INTERSECTION BISECTION
REDUNDANT CONSUMER ATTRIBUTION
COMMON CONCRETE BACKEND OBLIGATION SEARCH
RUST-ONLY RELEASE DIAGNOSTIC
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

### 1. Parent release evidence

R1A3-R1 authoritative suite produced:

```text
burn-wgpu-local          = BuildPass
burn_webgpu_backend      = BuildPass
canonical-baseline       = SameE0275
bisect-control           = SameE0275
current-production-coarse= BuildPass
demand-D001              = SameE0275
demand-D002              = SameE0275
demand-status            = DemandBoundarySetIncomplete

suite-digest:
c6ce0c01a4e96f2a2bbd00f6e31fd2b64f4ff391b98ae55de39eb9283f2eec29
```

Therefore neither D001 nor D002 individually removes the canonical E0275. This does not prove either is causally irrelevant because both instantiate the same concrete `TrainBackend` surface.

### 2. Existing demand boundaries preserved

```text
D001
pipeline::p1br1a3r1_run_streaming_train_backend_boundary
-> run_base_training_loop_streaming::<TrainBackend>

D002
pipeline::p1br1a3r1_run_batch_train_backend_boundary
-> run_base_training_loop::<TrainBackend>
```

Current concrete alias:

```text
TrainBackend = Autodiff<Wgpu<f32, i32>>
```

The R1 ledger records both against the same associated projection:

```text
<Autodiff<Wgpu<f32, i32>> as Backend>::FloatTensorPrimitive
```

with demand class `SendSync`.

### 3. R2 question

R2 fills only the missing truth-table quadrant:

```text
D001 ON  / D002 ON   -> SameE0275
D001 OFF / D002 ON   -> SameE0275
D001 ON  / D002 OFF  -> SameE0275
D001 OFF / D002 OFF  -> R2 treatment
```

No D003 is introduced.

### 4. Joint feature

Added to `crates/base_train/Cargo.toml`:

```text
p1br1a3r2-cut-demand-d001-d002 = ["p1br1a-release-bisect"]
```

Default OFF.

The pair feature is one explicit Cargo feature. It does not depend on the two R1 individual feature names.

### 5. Pipeline pair semantics

`pipeline.rs` exact D001 predicate becomes:

```text
not(any(
    p1br1a3r1-cut-demand-001,
    p1br1a3r2-cut-demand-d001-d002
))
```

and the HOLD branch uses the corresponding `any(...)` predicate.

D002 uses the same pair-feature integration with its own individual feature.

Therefore pair treatment changes exactly D001 + D002 while preserving:

```text
pipeline module
TrainBackend alias
run_base_training_loop_streaming definition
run_base_training_loop definition
MCU providers
Muon providers
scheduler providers
Burn/WGPU providers
```

No alternate backend or runtime fallback is introduced.

### 6. Pair authority module

Added:

```text
crates/base_train/src/current_production_demand_pair_p1b_r1a3_r2.rs
```

Materialized:

```text
P1bR1a3R2DemandPairId::D001D002
P1bR1a3R2DemandPairState
P1bR1a3R2CommonObligationState
P1bR1a3R2DemandPairManifest
P1bR1a3R2CommonDemandSurface
P1BR1A3_R2_PAIR_MANIFEST
p1br1a3r2_common_surface()
p1br1a3r2_pair_digest()
```

The common surface binds D001, D002, `Autodiff<Wgpu<f32, i32>>`, and the shared R1 associated projection.

### 7. Pair observer plan

R1A2 observer adds typed plan:

```text
DemandD001D002Pair
```

Its exact treatment args contain one feature only:

```text
--no-default-features
--features p1br1a3r2-cut-demand-d001-d002
--message-format=json
```

It does not enable either individual R1 feature.

### 8. R2 observer suite

Added:

```text
crates/ash_p1br1a2_release_observer/src/demand_pair_r1a3_r2.rs
```

New CLI:

```text
current-production-demand-pair
```

Eight-stage same-source suite:

```text
1 burn-wgpu-local
2 burn_webgpu_backend
3 canonical-baseline
4 bisect-control
5 current-production-coarse
6 demand-D001
7 demand-D002
8 demand-D001-D002
```

Progress header:

```text
[P1B-R1A3-R2][n/8]
```

Receipt path:

```text
target/p1br1a3r2/receipts/<suite-digest>.json
```

Runtime receipt output is not packaged in code ZIPs.

### 9. Promotion law

Control gate requires:

```text
burn-wgpu-local          BuildPass
burn_webgpu_backend      BuildPass
CanonicalBaseline        SameE0275
BisectControl            SameE0275
CurrentProductionCoarse  BuildPass
```

Single-boundary revalidation additionally requires:

```text
D001 SameE0275
D002 SameE0275
```

Then pair result maps:

```text
Pair BuildPass
    -> CommonTrainBackendObligationRequired

Pair SameE0275
    -> PairNoEffect

Pair DifferentE0275
    -> PairChangesToDifferentE0275

Pair InvalidSlice / WrongTarget / other invalid observation
    -> HoldInvalidPairObservation
```

If either D001 or D002 no longer reproduces `SameE0275` under the R2 source, pair promotion is held as `HoldSingleBoundaryDrift`.

### 10. Claim boundary

`CommonTrainBackendObligationRequired` permits:

```text
CONFIRMED:
D001 and D002 are individually redundant with respect to the canonical reproducer.

CONFIRMED:
removing both exact consumer boundaries removes the canonical reproducer under stable controls.

SUPPORTED:
the common concrete TrainBackend obligation surface shared by both consumers is the next justified locus.
```

It does not yet identify the exact associated type or trait declaration.

No claim is made yet that `FloatTensorPrimitive`, `TensorMetadata`, Burn Wgpu, or WGPU itself must change Send/Sync semantics.

### 11. Provider-cut retirement preserved

Legacy provider-cut features remain non-authoritative and no `lib.rs` provider-module gates are reintroduced.

R2 adds no:

```text
MCU provider cut
Muon provider cut
Scheduler provider cut
TrainBackend alias cut
backend crate removal
```

### 12. E0282 hold preserved

E0282 observed only under invalid provider cuts remains `UNKNOWN` as an independent defect. R2 adds no type annotations for those diagnostics.

### 13. Actual source delta

Relative to R1A3-R1 parent:

```text
ADD 2
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/current_production_demand_pair_p1b_r1a3_r2.rs
crates/ash_p1br1a2_release_observer/src/demand_pair_r1a3_r2.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

No Cargo.lock change and no new dependency.

### 14. Static qualification actually executed

```text
pair Cargo feature                         PRESENT
pair feature depends only on R1A bisect   PASS
pipeline D001 pair predicate               PRESENT
pipeline D002 pair predicate               PRESENT
pair authority module registered           PASS
observer pair module registered             PASS
observer pair CLI                           PRESENT
observer pair plan uses one feature         MATERIALIZED
old provider gates in lib.rs                0
new `if` count in R2-specific new logic     0
pipeline existing `if` count parent/new     29 / 29
balanced braces/parens/brackets             PASS
```

These are SOURCE/STATIC checks only.

Bake environment exposes no Cargo/rustc, therefore:

```text
observer compile/tests      NOT RUN
base_train compile/tests    NOT RUN
pair release treatment     NOT RUN
8-stage suite              NOT RUN
```

No COMPILE or RELEASE PASS is claimed by this bake.

### 15. Packaging law

Both delivered code ZIPs exclude generated:

```text
specs/
docs/
artifacts/
target/
*.ps1
```

No new Python or PowerShell loader is added.

### 16. Bake artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A3_R2_D001_D002_REDUNDANT_DEMAND_PAIR_INTERSECTION_OVERLAY_CODE_ONLY.zip
SHA-256:
759347e9a27f460da4e0f24a0145e5016c2bf8422f61249002a8c0b16add9042
Bytes: 36,304
Files: 7
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A3_R2_D001_D002_REDUNDANT_DEMAND_PAIR_INTERSECTION_CODE_ONLY.zip
SHA-256:
913f2c097f932b067004264c0023cede8b09469ac2da0af6aeab16f0478d6ce2
Bytes: 22,001,581
Files: 8,565
CRC: PASS
```

### 17. User-side qualification

First observer tests:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
```

Then base_train library tests:

```powershell
cargo test -p base_train --lib
```

Manual pair supporting build:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r2-cut-demand-d001-d002
```

Authoritative R2 suite:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production-demand-pair
```

### 18. Stop law

If the pair result is `BuildPass`, stop crate-wide demand candidate expansion and move to common TrainBackend obligation decomposition.

If the pair remains `SameE0275`, retire D001/D002 as no-effect candidates and resume demand-ledger discovery elsewhere.

No D003 is introduced in R2.
