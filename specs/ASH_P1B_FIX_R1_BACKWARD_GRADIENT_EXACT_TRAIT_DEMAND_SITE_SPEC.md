# ASH-P1B-FIX-R1

# BACKWARD-GRADIENT EXACT TRAIT-DEMAND SITE
# + BACKWARD-ONLY PHYSICAL WITNESS
# + GRADIENTS-PARAMS PROJECTION WITNESS
# + CANONICAL E0275 FINGERPRINT BINDING
# + EXACT ASSOCIATED-TYPE DEMAND EXTRACTION
# + MINIMAL COMPILE REPAIR

## Revision

```text
Patch ID:
ASH-P1B-FIX-R1-BACKWARD-GRADIENT-EXACT-TRAIT-DEMAND-SITE

Short name:
P1B-FIX-R1

Direct code parent:
ASH_PASS3_P1B_OBS_R1C_EXACT_IDENTITY_CODEGEN_CONTINUATION_CODE_ONLY.zip

Physical parent suite:
cf9e93fd2a9edb50420c327055fe368e2f4c1749b75f2a674a92af617b81615d

Physical parent phase-promotion seal:
b463c8a4c564dae16db8f9d244b3b0ed89c1fd8676cac8f50440c0b17884ee2f

Parent result:
BackwardGradientObligationRequired
```

## 1. Parent physical evidence

R1C established under stable source fences:

```text
parent canonical = ReusedPhysicalWitness:SameE0275
Q2 BatchTensor = ReusedPhysicalWitness:BuildPass
Q4 BackwardGradients = SameE0275
Q3 ForwardLoss = BuildPass
final-status = BackwardGradientObligationRequired
```

Therefore P0-P3 are cleared and P4 is the first outer phase that restores the canonical release E0275.

FIX-R1 stops outer observer expansion and splits only the two actual P4 source expressions.

## 2. Exact P4 cut

Current P4 surface:

```rust
let gradients = loss.backward();
let _params = GradientsParams::from_grads::<B, _>(gradients, &bundle.model);
```

FIX-R1 adds two default-OFF physical witnesses:

```text
B0 / p1bfixr1-backward-only
  Q3 setup
  + loss.backward()
  + returned gradients kept live by borrow
  - GradientsParams::from_grads
  - optimizer.step

B1 / p1bfixr1-gradients-params
  Q3 setup
  + loss.backward()
  + GradientsParams::from_grads::<B,_>
  - optimizer.step
```

Both features inherit only `p1br1a4r1-prefix-p3-forward-loss`, which remains bound to the D001+D002 pair baseline.

## 3. Build-only predicate

R1B physically established that `cargo check` does not exercise this E0275. FIX-R1 therefore uses release builds only:

```text
cargo build -p base_train --lib --release --locked -j 1 --message-format=json
```

Expression build budget is `MAX_EXPRESSION_BUILDS = 2`. B0 always runs first. B1 runs only when B0 is `BuildPass`.

## 4. Exact canonical fingerprint binding

FIX-R1 loads the exact R1C parent receipt from:

```text
target/p1br1a4r1/receipts/cf9e93fd2a9edb50420c327055fe368e2f4c1749b75f2a674a92af617b81615d.json
```

The R1C suite digest is recomputed from receipt contents. Adoption requires:

```text
schema = P1B-R1A4-R1+R3D+OBS-R1C
stored suite digest = requested suite digest
recomputed suite digest = requested suite digest
final-status = BackwardGradientObligationRequired
Q4 = SameE0275
terminal probe = Q3 ForwardLoss
Q3 = BuildPass
all R1C stage fences stable
phase-promotion seal = b463c8a4...
```

The canonical fingerprint object is taken from the physically failing R1C Q4 observation. A FIX-R1 witness is promoted only when its `P1bR1a2E0275Fingerprint` is exactly equal to that Q4 fingerprint. Merely observing error code E0275 is insufficient.

## 5. Diagnostic-only parent compatibility

FIX-R1 necessarily changes two diagnostic authority files:

```text
crates/base_train/Cargo.toml
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
```

Raw R1C `base_train` authority-surface digest equality is intentionally not required. Parent reuse is guarded by an exact stable experiment projection over workspace root Cargo.toml, Cargo.lock, Cargo/rustc toolchain identity, environment identity, required cargo-metadata projection, burn-wgpu-local source identity, burn_webgpu_backend source identity, and R1C build-contract identity.

The bake-time semantic delta is diagnostic-only:

```text
production training.rs delta = 0
pipeline.rs delta = 0
config.rs delta = 0
dataset.rs delta = 0
hybrid.rs delta = 0
root Cargo.toml delta = 0
Cargo.lock delta = 0
vendor/runtime delta = 0
default feature delta = 0
```

The only base_train additions are two default-OFF diagnostic features and two exact witness entry points in the existing diagnostic module.

## 6. Physical decision law

```text
B0 SameE0275 with exact parent fingerprint
  => BackwardCallDemandSiteRequired
  => culprit-expression=loss.backward()
  => B1 skipped

B0 BuildPass
B1 SameE0275 with exact parent fingerprint
  => GradientsParamsProjectionDemandSiteRequired
  => culprit-expression=GradientsParams::from_grads::<B,_>

B0 BuildPass
B1 BuildPass
  => HoldWitnessSurfaceMismatch

Any fingerprint mismatch
  => HoldFingerprintDivergence
```

No third broad expression witness is permitted before this boundary resolves.

## 7. Associated-type demand extraction law

This bake does not guess the repair before the physical B0/B1 result.

After `BackwardCallDemandSiteRequired`, extraction begins only from:

```text
Tensor::backward
→ AutodiffBackend::backward
→ concrete TrainBackend / Autodiff<Wgpu> primitive path
→ first source-visible associated-type projection entering the canonical WGPU Sync chain
```

After `GradientsParamsProjectionDemandSiteRequired`, extraction begins only from:

```text
GradientsParams::from_grads
→ from_module
→ GradientsParamsConverter
→ HybridTrainModel module visitation
→ concrete parameter/gradient associated-type projection
```

Previously cleared broad probes are not repeated: `TrainBackend: Send`, `TrainBackend: Sync`, `Wgpu: Backend`, `TrainBackend: Backend`, and `TrainBackend: AutodiffBackend`.

The extraction target is one source-grounded statement: expression E requires projection P because trait/function T introduces obligation U which normalizes through TrainBackend to the canonical `NumericDimension: Sync` chain.

## 8. Minimal repair law

No production repair is included in this pre-physical bake. This is intentional. Until B0/B1 resolves, speculative repairs are prohibited, including blanket `B::Gradients: Sync`, unsafe Send/Sync, recursion-limit increases, Burn/WGPU upgrades, optimizer rewrites, autodiff removal, blanket Arc/Mutex wrapping, or trait-solver flag workarounds.

Once the physical expression is confirmed, the next patch changes the smallest source authority that introduces the invalid natural obligation.

Final repair validation remains:

```text
culprit witness -> BuildPass
Q4 BackwardGradients -> BuildPass
uncut canonical base_train --lib --release --locked -j 1 -> BuildPass
```

Only the final canonical BuildPass closes P1B.

## 9. New execution command

```text
current-backward-gradient-exact-site
```

Normal path:

```text
preflight
→ R1C parent receipt adoption
→ workspace metadata fence
→ B0 physical build
→ optional B1 physical build
→ final metadata/identity fence
→ exact culprit status
```

No canonical rebuild, no Q3/Q4 replay, and no phase cargo-check is executed by FIX-R1.

## 10. Actual code delta

Relative to the canonical R1C full tree:

```text
ADD 1
MOD 7
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/fix_r1_backward_gradient.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
crates/ash_p1br1a2_release_observer/src/codegen_continuation_r1c.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
```

```text
source-delta-digest:
076b921ebe9d7304c75d349e4fccb095bbe7ce32cca23a62417fe8625560833b
```

## 11. Current source seals

```text
observer source files: 17
observer static source digest:
77dd2382f03bcbf4e01905bf929ab2bd52f47ec6fecc04529c997f8456c02104

required authority files: 15
required manifest digest:
cc8e245d5bc1ab059f308e3f69889d2f80491e4b3d055eadd1752c3b6c3c3449

canonical current authority-surface digest:
f22bebed8757fd81d91ecc14056ae936ab721f6cc963e149d65946eb107a8cf9

sealed base_train forensic files: 1,230
sealed whole-tree digest:
5faf03c4131552be3d551001b5e6a78eaf146e58bad68eb2d5489d2e6392129f
```

Changed diagnostic authority files:

```text
crates/base_train/Cargo.toml
SHA-256: 9b34c56b41412d384b1c195d6a4fe03deb20c7acb7070d2015d843dc91536645

crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
SHA-256: dfb6dc4916529fd29688ab3d970bfcf43d30338e8c4c8fa279c732cfa39c271b
```

## 12. Static qualification actually executed

```text
base_train Cargo.toml parse                         PASS
p1bfixr1-backward-only default-OFF                 PASS
p1bfixr1-gradients-params default-OFF              PASS
both FIX features inherit Q3 only                 PASS
B0 contains loss.backward                         PASS
B0 contains GradientsParams::from_grads           NO
B0 contains optimizer.step                        NO
B1 contains loss.backward                         PASS
B1 contains GradientsParams::from_grads           PASS
B1 contains optimizer.step                        NO
FIX observation plans use exactly one feature     PASS
FIX observation plans use --locked                PASS
FIX observation plans are Build/-j1 capable       PASS
R1C parent suite recomputation gate               PRESENT
R1C BackwardGradient final-status gate            PRESENT
R1C Q4 SameE0275 / Q3 BuildPass gates             PRESENT
exact fingerprint equality gate                   PRESENT
expression build budget                           2
third expression build fail-closed                PRESENT
stage fences                                      PRESENT
new `if` token delta                              0
Rust delimiter/static balance                     PASS
base_train production source delta                0
Cargo.lock delta                                  0
root Cargo.toml delta                             0
```

The bake environment has no usable Cargo/rustc toolchain. Rust compile/tests and physical B0/B1 release builds were NOT RUN. No COMPILE PASS, B0/B1 RESULT, ROOT PROJECTION, REPAIR PASS, or CANONICAL BUILD PASS is claimed by this bake.

## 13. ZIP freshness

```text
bake timestamp: 2026-09-08 23:01:06 Asia/Seoul
changed existing entries: 7 / 7 at bake mtime PASS
new entries: 1 / 1 at bake mtime PASS
unchanged parent entries: 8,440 / 8,440 parent mtime preserved PASS
```

## 14. Bake artifacts

```text
Overlay:
ASH_P1B_FIX_R1_BACKWARD_GRADIENT_EXACT_TRAIT_DEMAND_SITE_OVERLAY_CODE_ONLY.zip
SHA-256:
677d97e397fd6f019cf07e230843d529d76acd6d261f2b66ff937c9d7b382ddc
Files: 8
CRC: PASS

Full applied:
ASH_PASS3_P1B_FIX_R1_BACKWARD_GRADIENT_EXACT_TRAIT_DEMAND_SITE_CODE_ONLY.zip
SHA-256:
afd42d7c88b11ff9aac80e9568ade13e2cdcb2937b93dbfbda7f6ccca617aec5
Files: 8,448
CRC: PASS
```

Both contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths.

## 15. User-side qualification

Apply the FIX-R1 overlay over the R1C tree. Keep the existing R1C receipt under `target/p1br1a4r1/receipts/`. Do not run workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release --locked
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
cargo test -p ash_p1br1a2_release_observer --release --locked
cargo test -p base_train --lib --locked
```

Then execute only:

```powershell
.\target\release\ash_p1br1a2_release_observer.exe current-backward-gradient-exact-site
```

Decisive outputs are either:

```text
final-status=BackwardCallDemandSiteRequired
culprit-expression=loss.backward()
```

or:

```text
final-status=GradientsParamsProjectionDemandSiteRequired
culprit-expression=GradientsParams::from_grads::<B,_>
```

The resulting log is the authority for the immediate associated-type extraction and minimal repair patch.

## 16. Completion law

The isolation half of FIX-R1 is complete when B0/B1 produces one exact culprit-expression status under stable fences and the exact R1C fingerprint.

The full FIX-R1 objective closes only after the subsequent minimal repair makes the culprit witness, Q4, and finally the uncut canonical `base_train --lib --release --locked -j 1` build pass.

> FIX-R1 begins where the observer ends. It does not build another outer attribution system. It cuts the already-promoted BackwardGradients phase at the two actual Rust expressions, binds any failure to the exact physical R1C fingerprint, and refuses to guess a `Sync` repair before the failing expression is known.
