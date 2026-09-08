# ASH-P1B-OBS-R1C

# EXACT-IDENTITY CODEGEN CONTINUATION
# + PRIOR PHYSICAL WITNESS ADOPTION
# + CANONICAL REBUILD RETIREMENT
# + P3..P5 MIDPOINT Q4 BUILD
# + Q3 / Q5 TERMINAL DISCRIMINATOR
# + MAX-2 CONTINUATION BUILD CLOSURE
# + FINAL PHASE PROMOTION SEAL

## Revision

```text
Patch ID:
ASH-P1B-OBS-R1C-EXACT-IDENTITY-CODEGEN-CONTINUATION

Short name:
P1B-OBS-R1C

Direct code parent:
ASH_PASS3_P1B_OBS_R1B_LOCKFILE_IMMUTABILITY_CHECK_PREDICATE_QUALIFICATION_CODE_ONLY.zip

Class:
PHYSICAL WITNESS CONTINUATION
EXACT EXPERIMENT IDENTITY
PRIOR WITNESS ADOPTION
BUILD-ONLY PHASE ATTRIBUTION
CANONICAL/Q2 REBUILD RETIREMENT
MAX-2 CONTINUATION BUILDS
RUST-ONLY
NO TRAINING SEMANTIC CHANGE
```

## 1. Adopted R1B physical evidence

R1C continues the completed R1B physical suite:

```text
parent-suite:
a41ded6d206a4625d14db963fb58ac3ed98f390236b9803d27d5ec7ad4c9081e

obs-preflight=ReadyWithUnrelatedDrift
parent-seal-reuse=Admitted
stage-fences=7 stable=true
check-canonical-baseline=CheckPass
seal-canonical-baseline=SameE0275
seal-prefix-Q2-batch-tensor=BuildPass
check-predicate=Insufficient
codegen-status=Narrowed
codegen-interval=P3..P5
final-status=CodegenRequiredNarrowed
```

The parent physically established that `cargo check` is not a valid E0275 reducer for this lineage and that P0..P2 clear under a physical release build. Remaining interval is P3 ForwardLoss, P4 BackwardGradients, P5 OptimizerStep.

Observed parent timings are provenance only:

```text
canonical check: 64,178 ms
canonical build: 2,979,922 ms
Q2 build: 659,495 ms
```

## 2. Exact continuation identity is an experiment projection

R1C does not compare the R1B `source_set_digest` byte-for-byte because that digest includes observer source, and R1C necessarily changes the observer implementation.

Instead R1C materializes `P1bObsR1cExperimentIdentity` over experiment-defining state only:

```text
workspace root Cargo.toml SHA-256
Cargo.lock authority digest
base_train authority-surface digest
Cargo/rustc suite toolchain digest
environment digest
required cargo-metadata projection digest
burn-wgpu-local source digest
burn_webgpu_backend source digest
build-contract digest
```

Canonical workspace authorities remain:

```text
Cargo.toml SHA-256:
db8e37f7fc2e02f380abbacb34d932387f8918fb98fd6e061575072c07a0c2f5

Cargo.lock raw SHA-256:
ee21e9bd6385b639863465f221f76b6e353e65bb222e7b75d6820cd4d5b99f58

Cargo.lock R1A authority digest:
97b00989b10867b943e0e64cef7e268dc8de895568c2ec93baf75de9875c1668

R1C build-contract digest:
dfaccb11549f5dbbee9b933eab95d1b9351ed099dd82c3d3cfeb9f512117afb7
```

Observer source is independently compiled-vs-disk self-checked and schema compatibility is explicit, but observer source digest is not part of parent experiment equality.

## 3. Explicit parent receipt adoption

New CLI:

```text
current-training-body-obligation-codegen-continue <parent-suite-digest>
```

The parent digest is mandatory. R1C never scans for “latest” or auto-selects a receipt.

Resolution is restricted to:

```text
target/p1br1a4r1/receipts/<suite-digest>.json
```

The loaded receipt must deserialize as:

```text
P1B-R1A4-R1+R3D+OBS-R1B
```

R1C recomputes the exact R1B suite digest from receipt contents and requires:

```text
requested digest
== stored suite digest
== recomputed suite digest
```

The parent is admitted only when all of the following are true:

```text
freshness admitted
parent-seal-reuse=Admitted
canonical Check=CheckPass
canonical Build=SameE0275
check-predicate=Insufficient
Q2 Build=BuildPass
codegen-status=Narrowed
codegen-interval=P3..P5
final-status=CodegenRequiredNarrowed
final-build-budget=3 used=2
all parent stage fences stable
both dependency seals BuildPass
```

Missing or inconsistent evidence fails before a continuation build.

## 4. Parent physical witnesses are reused, not rerun

A successful adoption records the parent canonical and Q2 as `ReusedPhysicalWitness` provenance.

Valid R1C continuation executes:

```text
canonical check executions: 0
canonical build executions: 0
Q2 build executions: 0
phase cargo-check executions: 0
```

The historical R1B canonical and Q2 observations remain linked through their observation receipt digests and source suite digest.

## 5. Build-only continuation reducer

R1B physically sealed:

```text
CheckPass + SameE0275 Build
=> CheckPredicateInsufficient
```

Therefore R1C does not execute `cargo check` for phase discrimination.

```text
ADOPT canonical SameE0275
ADOPT Q2 BuildPass
        |
      BUILD Q4
       /    \
SameE0275  BuildPass
   |          |
 BUILD Q3   BUILD Q5
  /   \      /    \
E0275 Pass E0275  Pass
  |     |    |      |
 P3    P4    P5  TrainingCoreBodyCleared
```

Exact plans:

```text
Q3 = p1br1a4r1-prefix-p3-forward-loss
Q4 = p1br1a4r1-prefix-p4-backward-gradients
Q5 = p1br1a4r1-prefix-p5-optimizer-step
```

All physical probes remain `base_train --lib --release --locked -j 1 --message-format=json`.

## 6. Terminal promotion matrix

```text
parent Q2 BuildPass
Q4 SameE0275
Q3 SameE0275
=> ForwardLossObligationRequired

parent Q2 BuildPass
Q4 SameE0275
Q3 BuildPass
=> BackwardGradientObligationRequired

parent Q2 BuildPass
Q4 BuildPass
Q5 SameE0275
=> OptimizerStepObligationRequired

parent Q2 BuildPass
Q4 BuildPass
Q5 BuildPass
=> TrainingCoreBodyCleared
```

`DifferentE0275` produces `CodegenFingerprintDivergence`; structural/compiler/locked-resolution anomalies produce an explicit non-promotion state.

`TrainingCoreBodyCleared` means only that the synthetic P0..P5 materialized body does not reproduce the parent canonical failure. It does not claim canonical E0275 disappeared.

## 7. Continuation build budget

R1C materializes:

```text
MAX_CODEGEN_CONTINUATION_BUILDS = 2
```

Normal completion spends:

```text
Build 1: Q4
Build 2: Q3 or Q5
```

A third continuation phase build is rejected before spawn.

## 8. Stage identity fences and final identity closure

R1B `--locked` and stage-fence laws remain active.

R1C fences:

```text
workspace-metadata
Q4 build
Q3 or Q5 build
workspace-metadata-final
```

R1C additionally recomputes the experiment identity at the end of the continuation and requires:

```text
begin experiment identity
== end experiment identity
```

## 9. Dependency identity

R1C does not rerun dependency seals merely because observer source changed. It recomputes the two dependency package source digests and requires equality with the adopted R1B dependency witnesses:

```text
burn-wgpu-local
burn_webgpu_backend
```

Cargo.lock and metadata projection equality remain part of the experiment identity.

## 10. Phase promotion seal

R1C materializes `phase_promotion_seal_digest` over:

```text
parent suite digest
continuation experiment identity
adopted canonical observation receipt digest
adopted Q2 observation receipt digest
Q4 observation receipt digest
Q3/Q5 terminal observation receipt digest
final status
stage-fence digest
```

Suite schema advances to:

```text
P1B-R1A4-R1+R3D+OBS-R1C
```

## 11. Actual code delta

Relative to the canonical R1B full tree:

```text
ADD 1
MOD 4
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/codegen_continuation_r1c.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
```

No delta in `crates/base_train/**`, `Cargo.lock`, workspace root `Cargo.toml`, or production runtime/training source.

```text
source-delta-digest:
60fde3d51fefd67fd3e08b994ea180f8f00eb0e6c6cdb116c5f51df2a5a35478
```

## 12. Observer source self-check

```text
observer source files: 16
observer static source digest:
d8a4cd2a7dd85877a884b6f192304505fc592f12a2b028fb1529673f82bb457d
```

## 13. Static qualification actually executed

```text
source delta                                  ADD1 / MOD4 / DEL0
base_train source delta                       0
Cargo.lock delta                              0
root Cargo.toml delta                         0
observer source manifest                     16 files
parent receipt schema check                  PRESENT
parent R1B suite digest recomputation         PRESENT
parent canonical CheckPass gate               PRESENT
parent canonical SameE0275 Build gate         PRESENT
parent Q2 BuildPass gate                      PRESENT
parent P3..P5 interval gate                   PRESENT
parent stage-fence stable gate                PRESENT
parent dependency BuildPass gates             PRESENT
R1C cargo-check action in continuation         0
canonical/Q2 physical spawn in continuation   0
Q4 physical build path                        PRESENT
Q3/Q5 branch physical paths                   PRESENT
continuation build budget                     2
third build fail-closed                       PRESENT
all inherited observation argv                --locked
new `if` tokens in changed observer files     0
Rust delimiter/static balance                 PASS
ZIP CRC                                       PASS
generated/spec/docs/target/.ps1 paths         0
```

The bake environment has no usable Cargo/rustc toolchain. Rust compilation, observer tests, base_train tests, physical parent receipt adoption and Q4/Q3/Q5 execution were NOT RUN. No COMPILE PASS or PHYSICAL RELEASE PASS is claimed by this bake.

## 14. ZIP freshness

```text
bake timestamp: 2026-09-08 21:25:24 Asia/Seoul
changed/new entries: 5
changed/new entries at bake mtime: 5/5 PASS
unchanged parent entries: 8,442
unchanged parent mtimes preserved: 8,442/8,442 PASS
```

## 15. Bake artifacts

```text
Overlay:
ASH_P1B_OBS_R1C_EXACT_IDENTITY_CODEGEN_CONTINUATION_OVERLAY_CODE_ONLY.zip
SHA-256:
2e643e9cf0d5a3c28d3392c1a9d7bdc668204492a2bc0bb350c3959e0b0a5f89
Files: 5
CRC: PASS

Full applied:
ASH_PASS3_P1B_OBS_R1C_EXACT_IDENTITY_CODEGEN_CONTINUATION_CODE_ONLY.zip
SHA-256:
6765c8b150fd901b6dffa5bda07d1151187b442962a17e88a1b3d13902ec17e3
Files: 8,447
CRC: PASS
```

## 16. User-side qualification

Apply the R1C overlay over the R1B tree. Do not run workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release --locked
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
cargo test -p ash_p1br1a2_release_observer --release --locked
cargo test -p base_train --lib --locked
```

Then execute only the continuation with the exact R1B parent suite digest:

```powershell
.\target\release\ash_p1br1a2_release_observer.exe `
  current-training-body-obligation-codegen-continue `
  a41ded6d206a4625d14db963fb58ac3ed98f390236b9803d27d5ec7ad4c9081e
```

Do NOT rerun `current-training-body-obligation-fast` before this continuation.

## 17. Completion law

R1C closes operationally only when a physical run demonstrates:

```text
parent receipt digest/schema verified
parent canonical SameE0275 adopted
parent Q2 BuildPass adopted
experiment identity exact
canonical build count = 0
Q2 build count = 0
phase check count = 0
Q4 physical build completed
Q3 or Q5 physical build completed
all continuation stage fences stable
continuation builds <= 2
one final phase/clear status sealed
```

> P1B-OBS-R1C continues an already-sealed physical experiment instead of replaying it. The expensive R1B canonical and Q2 builds are adopted only through a verified receipt and exact experiment identity. The remaining P3..P5 interval is resolved with Q4 plus one terminal build, under a hard two-build budget. Once ForwardLoss, BackwardGradients, OptimizerStep, or TrainingCoreBodyCleared is physically sealed, outer phase bisection stops and the next attribution layer moves inside the promoted phase.
