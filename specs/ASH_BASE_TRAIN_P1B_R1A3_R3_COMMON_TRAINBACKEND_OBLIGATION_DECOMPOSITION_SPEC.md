# ASH-BASE-TRAIN-P1B-R1A3-R3-COMMON-TRAINBACKEND-OBLIGATION-DECOMPOSITION

## COMMON TRAINBACKEND OBLIGATION DECOMPOSITION
## + BACKEND WELL-FORMEDNESS BOUNDARY
## + AUTODIFFBACKEND BOUNDARY
## + FLOAT-TENSOR-PRIMITIVE ASSOCIATED-PROJECTION BOUNDARY
## + SEND / SYNC DEMAND SOURCE SPLIT

### Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A3-R3-COMMON-TRAINBACKEND-OBLIGATION-DECOMPOSITION

Short name:
P1B-R1A3-R3

Direct parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A3_R2_D001_D002_REDUNDANT_DEMAND_PAIR_INTERSECTION_CODE_ONLY.zip

Class:
TRAIT-OBLIGATION DECOMPOSITION
COMMON BACKEND SURFACE ATTRIBUTION
HIERARCHICAL RELEASE BISECTION
RUST-ONLY DIAGNOSTIC
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

### Parent promoted evidence

R2 authoritative suite established:

```text
burn-wgpu-local            = BuildPass
burn_webgpu_backend        = BuildPass
canonical-baseline         = SameE0275
bisect-control             = SameE0275
current-production-coarse  = BuildPass
demand-D001                = SameE0275
demand-D002                = SameE0275
demand-D001-D002           = BuildPass
pair-status                = CommonTrainBackendObligationRequired

parent suite digest:
6572c1efb7fc1313ba5e6119b5d985d4bf05464338c4115da171321520f43677
```

R3 therefore stops horizontal CurrentProduction discovery and decomposes the shared TrainBackend obligation vertically.

### Concrete backend identity

```text
TrainBackend      = Autodiff<Wgpu<f32, i32>>
InnerTrainBackend = Wgpu<f32, i32>
```

`pipeline.rs` and both R1 consumer boundaries remain unchanged by R3.

### Locked Burn generation

`Cargo.lock` is unchanged from R2 and resolves:

```text
burn           0.20.1
burn-backend   0.20.1
burn-autodiff  0.20.1
burn-tensor    0.20.1
burn-wgpu      0.20.1
```

R3 records the source-confirmed interpretation hierarchy:

```text
Backend                              -> Send
Backend                              -> Sync
BackendTypes::FloatTensorPrimitive   -> TensorMetadata + 'static
TensorMetadata                       -> Send
TensorMetadata                       -> Sync
AutodiffBackend                      -> Backend
AutodiffBackend::Gradients           -> Send
```

The Burn 0.20.1 Autodiff implementation maps its float primitive to an `AutodiffTensor<B>` wrapper over the inner backend. These are diagnostic contracts only; no Burn/vendor source is changed.

### Hierarchical decomposition law

Backend, AutodiffBackend, FloatTensorPrimitive, Send and Sync are not treated as independent sibling obligations.

```text
TrainBackend
├─ direct Self: Send
├─ direct Self: Sync
└─ Backend well-formedness
   └─ FloatTensorPrimitive: TensorMetadata
      ├─ Send
      └─ Sync

AutodiffBackend
└─ inherits Backend
   + autodiff-specific obligations
```

Associated-projection evidence is therefore a diagnostic path within Backend well-formedness, not a fake independent boolean treatment.

### R2 pair baseline inheritance

Every active R3 probe feature depends on:

```text
p1br1a3r2-cut-demand-d001-d002
```

D001 and D002 remain disabled while exactly one new trait witness is introduced.

### Active probes

Exactly five active probes are materialized:

```text
T001 TrainBackend Self Send
T002 TrainBackend Self Sync
T003 Inner Wgpu Backend well-formedness
T004 TrainBackend Backend well-formedness
T005 TrainBackend AutodiffBackend well-formedness
```

Features:

```text
p1br1a3r3-probe-trainbackend-send
p1br1a3r3-probe-trainbackend-sync
p1br1a3r3-probe-inner-wgpu-backend
p1br1a3r3-probe-trainbackend-backend
p1br1a3r3-probe-trainbackend-autodiffbackend
```

Each inherits the R2 pair feature and is default OFF.

### Probe authority module

Added:

```text
crates/base_train/src/current_trainbackend_obligation_decomposition_p1b_r1a3_r3.rs
```

It materializes probe IDs, availability, feature manifests, external-contract records, exact witness functions and deterministic authority identity.

T001 witnesses only `TrainBackend: Send`.
T002 witnesses only `TrainBackend: Sync`.
T003 witnesses `Wgpu<f32,i32>: Backend`.
T004 witnesses `TrainBackend: Backend`.
T005 witnesses `TrainBackend: AutodiffBackend`.

No provider is cfg-removed.

### Primitive direct split fail-closed

R3 intentionally adds no T006/T007 Cargo feature.

```text
ConcreteFloatPrimitiveSend -> CoupledByParentTrait
ConcreteFloatPrimitiveSync -> CoupledByParentTrait
```

The current authoritative primitive identity is an associated Backend projection, so a supposedly independent direct primitive probe would first force the parent Backend contract and contaminate the split. No new dependency is added merely to expose an internal Autodiff primitive type.

### Obligation-path annotation

The canonical R1A2 `SameE0275` classifier is unchanged. R3 only extends the E0275 fingerprint with non-authoritative path markers:

```text
Backend
AutodiffBackend
FloatTensorPrimitive
TensorMetadata
Send
Sync
```

They annotate an already-classified E0275 and do not weaken or replace the canonical fingerprint.

The canonical terminal remains:

```text
validation::NumericDimension: Sync
```

`FloatTensorPrimitiveMetadataSyncPathRequired` may be promoted only when T004 is canonical and its path contains FloatTensorPrimitive, TensorMetadata and the canonical NumericDimension Sync marker.

### Observer extension

Added:

```text
crates/ash_p1br1a2_release_observer/src/trainbackend_r1a3_r3.rs
```

New typed plans:

```text
ProbeTrainBackendSend
ProbeTrainBackendSync
ProbeInnerWgpuBackend
ProbeTrainBackendBackend
ProbeTrainBackendAutodiffBackend
```

Each plan requests exactly one top-level R3 feature. The individual R1 D001/D002 feature names are not enabled by these plans.

### Authoritative suite

New CLI:

```text
current-trainbackend-obligation
```

Eleven-stage suite:

```text
1  burn-wgpu-local
2  burn_webgpu_backend
3  canonical-baseline
4  bisect-control
5  current-production-coarse
6  demand-D001-D002
7  trainbackend-send
8  trainbackend-sync
9  inner-wgpu-backend
10 trainbackend-backend
11 trainbackend-autodiffbackend
```

Required control matrix:

```text
burn-wgpu-local          BuildPass
burn_webgpu_backend      BuildPass
CanonicalBaseline        SameE0275
BisectControl            SameE0275
CurrentProductionCoarse  BuildPass
D001+D002 pair baseline  BuildPass
```

Any control or pair drift holds attribution.

### Promotion hierarchy

Direct Self results have priority:

```text
T001 Same / T002 Build -> TrainBackendSelfSendPathRequired
T001 Build / T002 Same -> TrainBackendSelfSyncPathRequired
T001 Same / T002 Same  -> TrainBackendSelfSendSyncPathRequired
```

When T001/T002 both pass:

```text
T003 Same / T004 Same
    -> InnerWgpuBackendObligationSufficient

T003 Build / T004 Same
    -> AutodiffWrapperBackendConstructionRequired
       unless the T004 diagnostic path promotes the FloatTensorPrimitive/TensorMetadata Sync path

T003 Build / T004 Build / T005 Same
    -> AutodiffSpecificObligationRequired

T003 Build / T004 Build / T005 Build
    -> TrainingLoopGenericObligationBeyondBaseTraits
```

T004 Same + T005 Same is treated as inherited Backend failure, not proof of an Autodiff-specific obligation.

DifferentE0275 yields `HoldDifferentE0275`. Structural invalidity, wrong target or unrelated compiler failure yields `HoldInvalidProbe`.

### External contract identity

R3 records `external_contract_digest` over the unchanged workspace Cargo.lock plus the committed R3 authority source. This binds interpretation to the exact locked Burn generation without dependency changes.

### Production non-goals

R3 changes no pipeline training behavior, TrainBackend alias, WGPU provider, Autodiff provider, MCU/Muon runtime, scheduler/session ownership, optimizer state, checkpoint format or Device/Queue ownership.

No `unsafe impl Send`, `unsafe impl Sync`, Rc/Arc conversion, RefCell/Mutex conversion, recursion-limit increase, backend substitution or vendor patch is introduced.

### Actual source delta

```text
ADD 2
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/current_trainbackend_obligation_decomposition_p1b_r1a3_r3.rs
crates/ash_p1br1a2_release_observer/src/trainbackend_r1a3_r3.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/ash_p1br1a2_release_observer/src/fingerprint.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

Explicitly unchanged:

```text
Cargo.lock
crates/base_train/src/pipeline.rs
```

No new dependency.

### Static qualification actually executed

```text
Cargo.toml parse                               PASS
R3 active probe features                       5
all five probe features inherit R2 pair        PASS
T006 feature present                           false
T007 feature present                           false
old provider gates in lib.rs                   0
R3 authority module registered                 PASS
R3 observer CLI                                PASS
11-stage progress surface                      PASS
pipeline.rs parent/new                         UNCHANGED
Cargo.lock parent/new                          UNCHANGED
Burn 0.20.1 lock family                        VERIFIED
new `if` token delta                           0
Rust delimiter balance after string stripping  PASS
```

Bake environment has no usable Cargo/rustc. Observer compile/tests, base_train compile/tests, R3 probe release builds and the 11-stage suite are NOT RUN. No COMPILE or RELEASE PASS is claimed by the bake.

### Bake artifacts

```text
Overlay:
ASH_BASE_TRAIN_P1B_R1A3_R3_COMMON_TRAINBACKEND_OBLIGATION_DECOMPOSITION_OVERLAY_CODE_ONLY.zip
SHA-256: 457c9a9474950c05df1b4c4b4458783d609a707991b08ad869c788f55cc55524
Files: 7
CRC: PASS

Full:
ASH_PASS3_BASE_TRAIN_P1B_R1A3_R3_COMMON_TRAINBACKEND_OBLIGATION_DECOMPOSITION_CODE_ONLY.zip
SHA-256: 20946272b5369f43a71ff7420c20f507a6c8929d6c1b7ef6c9edba051b1d285f
Files: 8,440
CRC: PASS
```

Both ZIPs contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths. No new Python or PowerShell loader is included.

### User-side qualification

```powershell
cargo test -p ash_p1br1a2_release_observer --release
cargo test -p base_train --lib

cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r3-probe-trainbackend-send

cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r3-probe-trainbackend-sync

cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r3-probe-inner-wgpu-backend

cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r3-probe-trainbackend-backend

cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3r3-probe-trainbackend-autodiffbackend

cargo run -p ash_p1br1a2_release_observer --release -- current-trainbackend-obligation
```

### Stop law

R3 stops at the strongest valid hierarchical state and does not add neighboring probes merely for completeness. No repair occurs in R3; the next revision operates only on the narrowest obligation layer proven by the 11-stage same-source release suite.