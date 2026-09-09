# ASH-P1B-FIX-R3

# FULL-HYBRID VALID PROJECTION RETIREMENT
# + DIRECT BASE / ADAPTER CHECKPOINT SNAPSHOT AUTHORITY
# + FOUR PRODUCTION CALLSITE CUTOVER
# + INNER-MODULE WHOLE-MODEL CONVERSION NEGATIVE SEAL
# + SAME-FINGERPRINT LEGACY VALID CONTROL
# + CANONICAL RELEASE CLOSURE

## Revision

```text
Patch ID:
ASH-P1B-FIX-R3-FULL-HYBRID-VALID-PROJECTION-RETIREMENT

Short name:
P1B-FIX-R3

Direct code parent:
ASH_PASS3_P1B_FIX_R2_CF1_STALE_TEST_AUTHORITY_REPAIR_CODE_ONLY.zip

Physical parent FIX-R2 suite:
37624f59bdbdeb72327f564a244acf145dfb36f0886a3a546b53ecea92a1617a
```

Parent physical state:

```text
C0-adapter-only-gradients=BuildPass
C1-full-hybrid-negative=SameE0275
root-cause-status=FullHybridModuleVisitDemandRootConfirmed
C2-adapter-optimizer-step=BuildPass
canonical-release=SameE0275
final-status=RepairNotAdopted
```

## Production repair

FIX-R3 removes the four remaining production `HybridTrainModel::valid()` checkpoint conversions from `crates/base_train/src/training.rs`.

Before:

```rust
let valid = model.valid();
collect_full_checkpoint_snapshots_guarded(&valid.base, ...)?;
collect_trainable_lora_snapshots(&valid.adapters);
```

After:

```rust
collect_full_checkpoint_snapshots_guarded(&model.base, ...)?;
collect_trainable_lora_snapshots(&model.adapters);
```

Affected semantic sites:

```text
run_base_training_loop
  periodic checkpoint
  final checkpoint

run_base_training_loop_streaming
  periodic checkpoint
  final checkpoint
```

Static production seals:

```text
production model.valid() count = 0
direct &model.base count        = 4
direct &model.adapters count    = 4
R2 TrainableAdapterSet Adam init count = 2
R2 adapter-only from_grads count       = 2
```

R2 optimizer authority is unchanged.

## Same-revision A/B

Two default-OFF features are added:

```text
p1bfixr3-direct-checkpoint-snapshot
p1bfixr3-full-hybrid-valid-negative-control
```

Both inherit only `p1br1a4r1-prefix-p3-forward-loss`.

V0 direct witness contains direct `bundle.model.base` and `bundle.model.adapters` snapshot access and no `.valid()`.

V1 legacy negative control performs `let valid = bundle.model.valid();` then snapshots `valid.base` and `valid.adapters`.

Strong causal admission:

```text
V0=BuildPass
V1=exact FIX-R2 canonical SameE0275
=> FullHybridValidProjectionDemandRootConfirmed
```

## Parent FIX-R2 adoption

R3 explicitly loads:

```text
target/p1bfixr2/receipts/37624f59bdbdeb72327f564a244acf145dfb36f0886a3a546b53ecea92a1617a.json
```

The FIX-R2 suite digest is recomputed. Admission requires C0 BuildPass, C1 SameE0275, C2 BuildPass, canonical SameE0275, `FullHybridModuleVisitDemandRootConfirmed`, `RepairNotAdopted`, adapter-only production owner seals, stable parent fences and exact C1/canonical fingerprint equality.

## Execution authority

New command:

```text
current-full-hybrid-valid-projection-repair
```

Execution:

```text
preflight
-> FIX-R2 parent adoption
-> workspace metadata fence
-> V0 direct checkpoint build
-> V1 legacy full-valid negative build when V0 passes
-> canonical uncut release build only after strong root admission
-> final metadata/identity fence
-> compact FIX-R3 receipt
```

All observation Cargo children are `--locked`; release build witnesses use `-j 1` and structured JSON diagnostics. `cargo check` is not used as the E0275 predicate.

Result matrix:

```text
V0 BuildPass + V1 exact SameE0275
  => FullHybridValidProjectionDemandRootConfirmed

V0 SameE0275
  => DirectCheckpointAuthorityStillFails

V0 BuildPass + V1 BuildPass
  => HoldLegacyValidWitnessLost

V1 DifferentE0275
  => HoldLegacyValidFingerprintDivergence
```

Canonical result:

```text
BuildPass      => FullBaseTrainReleaseClosed
SameE0275      => SecondaryRepairNotSufficient
DifferentE0275 => CanonicalFingerprintChanged
other failure  => CanonicalE0275RepairedNewCompileBlockerPresent
```

R3 scope build budget is two builds for V0/V1. The canonical release is one final additional build after root admission.

## Production semantic delta

```text
production_body_changed = true
runtime_route_changed = false
default_feature_changed = false
vendor_changed = false
lockfile_changed = false
```

R3 changes checkpoint source authority only. It does not change loss, forward, backward, TrainableAdapterSet optimizer ownership, Burn/WGPU vendor source, Adam implementation, checkpoint format or Cargo.lock.

## Actual source delta

Relative to the CF1-corrected FIX-R2 full tree:

```text
ADD 1
MOD 7
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/fix_r3_valid_projection.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/base_train/Cargo.toml
crates/base_train/src/training.rs
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
```

```text
source-delta-digest:
29430d25f0784d18b391d0b25fff0b058984e84965e0aad8b6e9912a977376e5
```

## Current source seals

```text
required authority files: 15
required manifest digest:
5547bb7ed64e807cc60d3add45a94c39d783830321f2eca764547d0c168ebc80

authority-surface digest:
d4e86a63b0cf395f997741a395df4bbcdff20b36dc30199707dd6f9b4fcbbea9

sealed base_train forensic files: 1,230
sealed whole-tree digest:
b30be225c7e91b31d0869798324ecbe5699f54827c61e891926927b08550b2bc

OBS-R1 base_train source digest:
7b32f4be0e0a30a388e1329444be2988f4162dbae53b141c28c0bd3b8acd79bc

observer source files: 19
observer static source digest:
fd625b3f6258edea630c20f0e4198379c1fefdd1b130e51785a7fc6cba95c3e0
```

## Static qualification executed

```text
Cargo.toml parse                                 PASS
R3 features default-OFF                         PASS
R3 features inherit Q3 only                     PASS
production model.valid() count                  0
direct model.base count                         4
direct model.adapters count                     4
R2 adapter optimizer route retained             PASS
V0 direct base/adapter access                   PASS
V0 .valid()                                     ABSENT
V1 .valid()                                     PRESENT
R3 command dispatch                             PRESENT
R3 observation plans                            PRESENT
FIX-R2 parent suite recomputation               PRESENT
exact parent fingerprint gates                  PRESENT
V0/V1 scope budget                              2
canonical build path                            PRESENT
stage identity fences                           PRESENT
new positive if-token delta                     0
Rust delimiter/static balance                   PASS
ZIP CRC                                         PASS
```

Bake environment has no usable Cargo/rustc toolchain. Rust compile/tests, V0/V1 physical builds and canonical release build were NOT RUN. No COMPILE PASS, secondary-root promotion or canonical BuildPass is claimed by this bake.

## Artifacts

```text
Overlay:
ASH_P1B_FIX_R3_FULL_HYBRID_VALID_PROJECTION_RETIREMENT_OVERLAY_CODE_ONLY.zip
SHA-256:
539584e14ef4129ecaec045ea1093218fbb5e0511bf5bc50e8fc9d7e762f13a9
Files: 8
CRC: PASS

Full applied:
ASH_PASS3_P1B_FIX_R3_FULL_HYBRID_VALID_PROJECTION_RETIREMENT_CODE_ONLY.zip
SHA-256:
c8680930e561a3cd355ed04e596c02178b8fe22da2e6c48e4452c70ab62ad468
Files: 8,450
CRC: PASS
```

## Completion law

R3 closes only when the FIX-R2 physical parent is adopted, all four production whole-model valid callsites are retired, V0 builds, V1 reproduces the exact FIX-R2 canonical fingerprint, all fences stay stable, and the uncut canonical `base_train --lib --release --locked -j 1` build returns BuildPass.

`FullBaseTrainReleaseClosed` is the stop condition for the entire P1B E0275 investigation.