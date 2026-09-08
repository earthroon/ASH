# ASH-BASE-TRAIN-P1B-R1A4-R1-R3D-FAST-OBSERVER-TRAINING-BODY-PHASE-BISECTION

## TWO-TIER FAST OBSERVER
## + RELEASE CHECK SWEEP
## + FINAL BUILD SEAL
## + DEPENDENCY CACHE PRESERVATION
## + TRAINING-LOOP BODY OBLIGATION PHASE BISECTION
## + MODEL / OPTIMIZER / BATCH / FORWARD / BACKWARD / STEP PREFIX AUTHORITY

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A4-R1-R3D-FAST-OBSERVER-TRAINING-BODY-PHASE-BISECTION

Short name:
P1B-R1A4-R1 + P1B-R1A3-R3D

Direct code parent:
P1B-R1A3-R3C1 diagnostic-lifecycle corrected source tree

Class:
TRAINING-BODY TRAIT-OBLIGATION BISECTION
TWO-TIER FAST OBSERVER
CACHE-PRESERVING RELEASE ATTRIBUTION
RUST-ONLY DIAGNOSTIC
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

---

# 1. Parent promoted release evidence

R3 authoritative machine suite already established:

```text
burn-wgpu-local             = BuildPass
burn_webgpu_backend         = BuildPass
canonical-baseline          = SameE0275
bisect-control              = SameE0275
current-production-coarse   = BuildPass
demand-D001-D002            = BuildPass
TrainBackendSend            = BuildPass
TrainBackendSync            = BuildPass
InnerWgpuBackend            = BuildPass
TrainBackendBackend         = BuildPass
TrainBackendAutodiffBackend = BuildPass

r3-status = TrainingLoopGenericObligationBeyondBaseTraits

parent suite digest:
0d68023dd8b3a25d888428b62bff438b6d91fd851b529b9459599102e3858f77
```

Therefore R1A4 does not continue Backend / AutodiffBackend / direct TrainBackend Send/Sync decomposition. The remaining justified locus is the concrete body of the two redundant training-loop monomorphizations.

---

# 2. Combined execution architecture

This bake materializes R3D and R1A4 together.

```text
TIER A
cargo check --release
    -> exact Cargo JSON
    -> CheckPass / SameE0275 / structural failure
    -> adaptive binary prefix narrowing

TIER B
cargo build --release -j 1
    -> fixed control spine
    -> last passing / first failing prefix witness
    -> final release seal
```

`CheckPass` is distinct from `BuildPass`. A check-only result cannot become a final promotion.

---

# 3. Cargo action SSOT

`P1bR1a3R3dCargoAction` is added to the existing observer command builder:

```text
Check -> cargo check
Build -> cargo build
```

Both retain:

```text
-p <package>
--lib
--release
--message-format=json
```

Only final Build mode adds:

```text
-j 1
```

Existing `observe_plan()` remains the historical Build path. New fast suites call `observe_plan_with_action()` explicitly.

---

# 4. No global clean

The fast observer never executes:

```text
cargo clean
```

and does not delete Cargo target artifacts between stages. Cargo owns freshness and the dependency cache remains warm.

Manual observer-package clean remains a user-side stale-binary recovery action only.

---

# 5. Exact dependency seal cache

Added observer authority:

```text
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
```

Final dependency BuildPass seals for:

```text
burn-wgpu-local
burn_webgpu_backend
```

may be reused only when the exact cache key matches:

```text
package source digest
Cargo.lock digest
Cargo toolchain digest
rustc toolchain digest
environment digest
required metadata projection digest
package role / plan identity
```

Cache location:

```text
target/p1br1a3r3d/cache/
```

Only receipt JSON is cached. No `.rlib`, `.rmeta`, object or executable is copied manually.

Malformed, missing or identity-drifted cache records fail open to fresh execution, never to a guessed PASS.

---

# 6. Training-loop body phase authority

Added:

```text
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
```

Six source-bound phases:

```text
P0 ModelConstruction
P1 OptimizerInitialization
P2 BatchTensorMaterialization
P3 ForwardLoss
P4 BackwardGradients
P5 OptimizerStep
```

Six nested prefixes:

```text
Q0 = P0
Q1 = P0..P1
Q2 = P0..P2
Q3 = P0..P3
Q4 = P0..P4
Q5 = P0..P5
```

Each prefix feature inherits:

```text
p1br1a3r2-cut-demand-d001-d002
```

so the natural D001/D002 callsites remain disabled while one committed body witness is introduced.

---

# 7. Prefix features

Added to `crates/base_train/Cargo.toml`:

```text
p1br1a4r1-prefix-p0-model
p1br1a4r1-prefix-p1-optimizer-init
p1br1a4r1-prefix-p2-batch-tensor
p1br1a4r1-prefix-p3-forward-loss
p1br1a4r1-prefix-p4-backward-gradients
p1br1a4r1-prefix-p5-optimizer-step
```

All are default OFF and depend only on the R2 D001+D002 pair baseline.

No Cargo.lock change and no new dependency.

---

# 8. Real body operation lineage

The committed witnesses reuse real production types and operations:

```text
AshModel::<B>::new
build_hybrid_train_model
AdamConfig::init::<B, HybridTrainModel<B>>
BaseBatchCpu::to_backend::<B>
causal_lm_loss
loss.backward
GradientsParams::from_grads::<B, _>
optimizer.step
```

`causal_lm_loss` receives a visibility-only change from private to `pub(crate)` so the diagnostic witness calls the exact existing implementation rather than duplicating it.

No runtime behavior is changed.

---

# 9. Diagnostic module lifecycle

The new R1A4 authority module is compiled only under:

```text
cfg(test)
or one of the six R1A4 prefix features
```

It is not directly gated by CurrentProduction or Atlas coarse features.

This preserves the historical R1A coarse-manifest SSOT:

```text
CurrentProduction exact module count = 136
AtlasCheckpoint exact module count    = 153
```

The new diagnostic module is not a member of either production closure manifest.

---

# 10. Provider preservation

R1A4 prefix treatments do not cfg-remove:

```text
pipeline
TrainBackend
AshModel
HybridTrainModel
Adam
Burn WGPU backend
MCU / Muon / scheduler providers
```

No provider-cut strategy is revived.

---

# 11. Fast control spine

Before prefix narrowing, the fast suite checks:

```text
canonical-baseline             -> SameE0275
bisect-control                 -> SameE0275
current-production-coarse      -> CheckPass
demand-D001-D002               -> CheckPass
trainbackend-autodiffbackend    -> CheckPass
```

The final seal re-runs current-source base_train controls as full builds:

```text
canonical-baseline             -> SameE0275
bisect-control                 -> SameE0275
current-production-coarse      -> BuildPass
demand-D001-D002               -> BuildPass
```

---

# 12. Adaptive binary narrowing

The observer does not check Q0 through Q5 linearly.

First:

```text
Q2
```

If Q2 is canonical E0275, search P0-P2 using Q0 then Q1.

If Q2 passes, check Q4.

If Q4 is canonical E0275, check Q3 to distinguish ForwardLoss from BackwardGradients.

If Q4 passes, check Q5 to distinguish OptimizerStep from post-optimizer body.

Typical fast prefix count is therefore 2-3 checks, with a maximum small subset rather than all six.

---

# 13. Fast candidates

```text
ModelConstructionCandidate
OptimizerInitializationCandidate
BatchTensorMaterializationCandidate
ForwardLossCandidate
BackwardGradientsCandidate
OptimizerStepCandidate
PostOptimizerBodyCandidate
DifferentE0275
Invalid
```

No fast candidate is a final release promotion.

---

# 14. Minimal final witness sets

Final Build mode seals only adjacent boundaries:

```text
P0: PairBaseline BuildPass -> Q0 SameE0275
P1: Q0 BuildPass -> Q1 SameE0275
P2: Q1 BuildPass -> Q2 SameE0275
P3: Q2 BuildPass -> Q3 SameE0275
P4: Q3 BuildPass -> Q4 SameE0275
P5: Q4 BuildPass -> Q5 SameE0275

Core clear:
Q5 BuildPass
```

This is the first-failing-phase authority.

---

# 15. Check/build parity

Every plan executed in both tiers records:

```text
CheckPass <-> BuildPass
SameE0275 <-> SameE0275
```

Any divergence derives:

```text
HoldCheckBuildDivergence
```

No phase promotion is permitted.

---

# 16. Final states

```text
ModelConstructionObligationRequired
OptimizerInitializationObligationRequired
BatchTensorMaterializationObligationRequired
ForwardLossObligationRequired
BackwardGradientObligationRequired
OptimizerStepObligationRequired
TrainingCoreBodyCleared
```

Hold states cover control/source/toolchain/environment/metadata/authority drift, invalid observation, DifferentE0275 and final witness drift.

---

# 17. New preferred CLI

```text
current-training-body-obligation-fast
```

The historical slow R3 command remains:

```text
current-trainbackend-obligation
```

and is not deleted.

---

# 18. Expected console shape

```text
[P1B-R1A4-R1][DEPENDENCY] burn-wgpu-local
[P1B-R1A4-R1][DEPENDENCY] burn_webgpu_backend

[P1B-R1A4-R1][CHECK] canonical-baseline
[P1B-R1A4-R1][CHECK] bisect-control
[P1B-R1A4-R1][CHECK] current-production-coarse
[P1B-R1A4-R1][CHECK] demand-D001-D002
[P1B-R1A4-R1][CHECK] trainbackend-autodiffbackend

[P1B-R1A4-R1][CHECK] prefix-Q2-batch-tensor
... adaptive branch only ...

[P1B-R1A4-R1][SEAL] canonical-baseline
[P1B-R1A4-R1][SEAL] bisect-control
[P1B-R1A4-R1][SEAL] current-production-coarse
[P1B-R1A4-R1][SEAL] demand-D001-D002
... adjacent witness seal ...
```

Final summary header:

```text
[P1B-R1A4-R1+R3D]
```

Receipt location:

```text
target/p1br1a4r1/receipts/<suite-digest>.json
```

---

# 19. Existing observer authority preserved

Both Check and Build tiers retain:

```text
--message-format=json
exact package identity
exact lib target identity
canonical SameE0275 fingerprint
InvalidSlice precedence
source/toolchain/environment/metadata identity
```

No stderr diagnostic fallback is added.

---

# 20. Production non-goals

No change to:

```text
TrainBackend alias
pipeline runtime routing
model math
optimizer math
WGPU Device / Queue ownership
MCU / Muon behavior
checkpoint format
Burn / CubeCL / WGPU vendor source
```

No:

```text
unsafe impl Send
unsafe impl Sync
Rc -> Arc
RefCell -> Mutex
recursion_limit increase
backend substitution
GPU observer fiction
```

is introduced.

---

# 21. Actual source delta

Relative to the R3C1-corrected parent tree:

```text
ADD 3
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/training.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

Explicitly unchanged:

```text
Cargo.lock
crates/base_train/src/pipeline.rs
crates/ash_p1br1a2_release_observer/Cargo.toml
```

---

# 22. Static qualification actually executed

```text
base_train Cargo.toml parse                         PASS
six prefix features exact pair inheritance         PASS
new Rust delimiter balance                         PASS
Current coarse parser count                        136
Atlas coarse parser count                          153
R1A4 diagnostic module in coarse manifests         false
Check action = cargo check                          PRESENT
Build action = cargo build                         PRESENT
Check action -j1                                   ABSENT BY BUILDER LAW
Build action -j1                                   PRESENT BY BUILDER LAW
new observer normal cargo clean execution          ABSENT
Cargo.lock parent/new                              UNCHANGED
pipeline.rs parent/new                             UNCHANGED
observer Cargo.toml parent/new                     UNCHANGED
new-file `if` token count                          0
ZIP CRC                                             PASS
```

Bake environment exposes no usable Cargo/rustc, therefore:

```text
base_train unit tests                  NOT RUN
observer unit tests                    NOT RUN
cargo check prefix sweep               NOT RUN
final release build seal               NOT RUN
physical/runtime training              NOT RUN
```

No COMPILE or RELEASE PASS is claimed by this bake.

---

# 23. Bake artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A4_R1_R3D_FAST_OBSERVER_TRAINING_BODY_PHASE_BISECTION_OVERLAY_CODE_ONLY.zip
SHA-256:
d985d15502e8f9a12c46ccbaeae54d010d19ecf8f40ffad44df750a3dec100b8
Files: 8
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A4_R1_R3D_FAST_OBSERVER_TRAINING_BODY_PHASE_BISECTION_CODE_ONLY.zip
SHA-256:
6cfff239347d46bc6f39d0d92771563eef31e83ecb52c3512e1343f17390dbeb
Files: 8,443
CRC: PASS
```

Both ZIPs contain zero generated:

```text
specs/
docs/
artifacts/
target/
*.ps1
```

No Python or PowerShell loader is added to the code bake.

---

# 24. User-side qualification

First:

```powershell
cargo test -p base_train --lib
cargo test -p ash_p1br1a2_release_observer --release
```

Do not run a workspace-wide `cargo clean`.

When the observer binary itself is stale only:

```powershell
cargo clean -p ash_p1br1a2_release_observer
cargo build -p ash_p1br1a2_release_observer --release
```

Authoritative fast suite:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-training-body-obligation-fast
```

---

# 25. Completion law

R1A4-R1 + R3D closes when:

```text
fast controls are valid
adaptive prefix candidate is derived
final controls are release-sealed
last-pass / first-fail witness pair is release-sealed
check/build parity holds
one final phase status is emitted
```

Once one phase is sealed, broad body bisection stops and the next revision descends only inside that phase.

---

# 26. Final law

> R3 has already cleared the standalone TrainBackend Send/Sync, Backend and AutodiffBackend trait layers.
>
> This bake therefore moves the attribution boundary into the real training-loop body rather than continuing trait-declaration probes.
>
> The six body phases are represented as nested natural operation prefixes over the proven D001+D002 BuildPass baseline.
>
> The observer first uses `cargo check --release` to locate the candidate phase without paying full code-generation cost for every probe.
>
> Full `cargo build --release -j 1` remains the final authority and runs only the fixed control spine plus the adjacent prefix witnesses needed to seal the chosen boundary.
>
> Exact dependency BuildPass seals may be reused under a fail-closed identity key, while the Cargo target tree is intentionally preserved and no global clean occurs.
>
> No provider, backend, optimizer implementation, WGPU ownership contract or Send/Sync implementation is modified by this revision.
