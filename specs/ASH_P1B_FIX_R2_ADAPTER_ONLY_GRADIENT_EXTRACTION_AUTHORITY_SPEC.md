# ASH-P1B-FIX-R2

# ADAPTER-ONLY GRADIENT EXTRACTION AUTHORITY
# + FULL-HYBRID MODULE VISIT RETIREMENT
# + TRAINABLE-LORA PARAMETER SCOPE MATERIALIZATION
# + GRADIENTS-PARAMS ADAPTER-ONLY PHYSICAL WITNESS
# + OPTIMIZER OWNER SCOPE CUTOVER
# + BASE-MODEL PARAMETER VISIT NEGATIVE SEAL
# + CANONICAL E0275 REPAIR BUILD

## Revision

```text
Patch ID:
ASH-P1B-FIX-R2-ADAPTER-ONLY-GRADIENT-EXTRACTION-AUTHORITY

Short name:
P1B-FIX-R2

Direct code parent:
ASH_PASS3_P1B_FIX_R1_BACKWARD_GRADIENT_EXACT_TRAIT_DEMAND_SITE_CODE_ONLY.zip

Physical parent FIX-R1 suite:
c7b1450a18e95ca92f6750fc311e37a384c861db2b79096e348b1b16c5816c98

Parent result:
GradientsParamsProjectionDemandSiteRequired
```

## 1. Parent physical authority

FIX-R1 physically established:

```text
B0 loss.backward() = BuildPass
B1 + GradientsParams::from_grads::<B,_> = SameE0275
culprit-expression = GradientsParams::from_grads::<B,_>
```

R2 therefore does not change backward or loss semantics. It repairs the module/optimizer authority supplied after backward.

## 2. Production repair

New optimizer owner in `crates/base_train/src/hybrid.rs`:

```rust
#[derive(Module, Debug)]
pub struct TrainableAdapterSet<B: Backend> {
    pub adapters: Vec<TrainableLoraSlot<B>>,
}
```

`TrainableAdapterSet` contains no `AshModel<B>` field. `HybridTrainModel<B>` remains forward-composition authority.

`HybridTrainModel::into_optimizer_parts()` moves the existing model into `AshModel<B> + TrainableAdapterSet<B>` without cloning base weights or adapter parameters. `TrainableAdapterSet::into_hybrid()` reassembles the same base with the optimizer-updated adapters.

Both production training loops now initialize `AdamConfig::new().init::<B, TrainableAdapterSet<B>>()` and perform backward, adapter-only `GradientsParams::from_grads`, adapter-only optimizer step, then reassembly. Production full-hybrid optimizer initialization count is zero and production gradient extraction is explicitly owned by `TrainableAdapterSet<B>` at both affected loops.

## 3. Physical same-revision A/B

Three default-OFF diagnostic features are added:

```text
p1bfixr2-adapter-only-gradients-params
p1bfixr2-full-hybrid-negative-control
p1bfixr2-adapter-optimizer-step
```

All inherit only the already-cleared Q3 forward-loss baseline.

C0 executes adapter-only gradient conversion and is expected to `BuildPass`.

C1 executes the legacy full-hybrid conversion under the same repaired revision and is expected to reproduce the exact FIX-R1 `SameE0275` fingerprint.

Only `C0=BuildPass + C1=exact SameE0275` promotes `FullHybridModuleVisitDemandRootConfirmed`.

C2 executes adapter-only `from_grads -> Adam<TrainableAdapterSet<B>>::step -> HybridTrainModel reassembly` and is expected to `BuildPass`.

## 4. Canonical closure

After strong root-cause admission and C2 BuildPass, the same command performs:

```text
cargo build -p base_train --lib --release --locked -j 1 --message-format=json
```

Expected final result is `BuildPass` and final status `FullBaseTrainReleaseClosed`.

If the original canonical fingerprint remains, final status is `RepairNotAdopted`. If the original E0275 disappears but another compiler blocker appears, status is `CanonicalE0275RepairedNewCompileBlockerPresent`; full release closure is not claimed.

## 5. Build budgets

```text
scope witness budget = 2
  C0 + optional C1

repair validation budget = 2
  C2 + canonical
```

No `cargo check` is used as an E0275 predicate.

## 6. Base-model parameter-visit negative seal

R2 requires:

```text
TrainableAdapterSet contains Vec<TrainableLoraSlot<B>>
TrainableAdapterSet contains no AshModel<B>
production Adam owner = TrainableAdapterSet<B>
production from_grads owner = TrainableAdapterSet<B>
production Adam<HybridTrainModel<B>> = absent
production from_grads(...,&model) = absent
```

The old full-hybrid path remains diagnostic only, including C1.

## 7. Optimizer/checkpoint scope

The current production loops do not serialize the local optimizer value into the checkpoint path, so R2 introduces no checkpoint-format migration. Model/checkpoint representation remains `HybridTrainModel`; the adapter wrapper is optimizer-transaction authority only. No adapter or base clone is introduced by the production cutover.

## 8. Observer command

New command:

```text
current-adapter-only-gradient-authority
```

Execution:

```text
preflight
→ FIX-R1 parent receipt adoption
→ workspace identity fence
→ C0
→ C1 when C0 passes
→ C2 only after strong A/B root admission
→ canonical release only after C2 passes
→ final identity fence
→ compact FIX-R2 receipt
```

The FIX-R1 parent receipt is recomputed and must prove B0 BuildPass, B1 SameE0275, final status `GradientsParamsProjectionDemandSiteRequired`, exact canonical fingerprint, and stable stage fences.

## 9. Production semantic authority

R2 intentionally changes production training semantics. `P1B_OBS_R1_PRODUCTION_SEMANTIC_DELTA.production_body_changed` is set to `true`; older observer parent-seal reuse paths must not treat R2 as diagnostic-only.

Production semantic delta is limited to optimizer owner scope, GradientsParams module owner scope, and adapter ownership split/rejoin around the optimizer transaction. Loss, forward, backward, WGPU, Burn vendor code, Adam implementation, and checkpoint format remain unchanged.

## 10. Actual source delta

Relative to FIX-R1 canonical full tree:

```text
ADD 1
MOD 9
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/fix_r2_adapter_authority.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/fix_r1_backward_gradient.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/base_train/Cargo.toml
crates/base_train/src/hybrid.rs
crates/base_train/src/training.rs
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
```

```text
source-delta-digest:
3de48ede29a1b78ef1bd7ddfe0d6d38d9a0c6173611568f9d1c844819a3d568d
```

## 11. Current source seals

```text
required authority files: 15
required manifest digest:
2a46adba98e9669345e06f1f5360826c0ade18a495b1f7c65167292cd48df940

canonical authority-surface digest:
6372ef5bd92abe8b6670806811f901ff29456b9ff137f5342d60b8458b970943

sealed base_train forensic files: 1,230
sealed whole-tree digest:
a26300ac9c8e48bbbc4dd00aeb99a99447971c0b7bedad5ccecb4a1417f8cc44

OBS-R1 whole base_train source digest:
5a111ab583d19357e8a2097d9071159df2ae0d37b61d9dc4d9769b906502b199

observer source files: 18
observer static source digest:
c7966b029738cfa6b6cd9166424479ab06a36585ed51a31c6574b2b2cd259a94
```

Key changed base_train hashes:

```text
crates/base_train/Cargo.toml
23eac5f3e5289702ba91275a27fea11670ddd9a85cdb35d20ae3b7efe0c374ef

crates/base_train/src/hybrid.rs
b9caf014fbfc9a676968e45d9866fe60bc05f80a93ca81ae72dc8fe2c89d8ec8

crates/base_train/src/training.rs
4a4f14d718781a868213168dcc9552dff8732e0221be8ff9a6d83714cda70a3f

crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
10af9eb3c0bd342ba18c3f93e5888f3aa1f77af5b4136fab45cac2b6dd3a35a7
```

## 12. Static qualification actually executed

```text
base_train Cargo.toml parse                         PASS
R2 diagnostic features default-OFF                 PASS
all R2 diagnostic features inherit Q3 only         PASS
production TrainableAdapterSet Adam init count     2
production adapter-only from_grads count           2
production HybridTrainModel Adam init count        0
production legacy_full_model_optimizer symbol      0
TrainableAdapterSet AshModel field                  0
C0 contains adapter-only from_grads                 PASS
C0 contains optimizer.step                          NO
C1 contains full-hybrid from_grads                  PASS
C1 contains optimizer.step                          NO
C2 contains adapter-only from_grads + optimizer     PASS
R2 observer command dispatch                        PRESENT
all R2 observation plans use --locked / Build -j1  PRESENT
FIX-R1 parent receipt recomputation gate            PRESENT
exact FIX-R1 fingerprint equality gate              PRESENT
C0/C1 scope build budget                            2
C2/canonical validation build budget                2
source identity stage fences                        PRESENT
new `if` token delta in changed source              0
Rust delimiter/static balance                       PASS
ZIP CRC                                             PASS
```

The bake environment has no usable Cargo/rustc toolchain. Rust compilation, tests, C0/C1/C2 physical release builds and canonical repair build were NOT RUN. No physical root-cause PASS or canonical BuildPass is claimed by this bake.

## 13. ZIP freshness

```text
bake timestamp: 2026-09-09 01:40:00 Asia/Seoul
changed/new entries: 10 / 10 at bake mtime PASS
unchanged parent entries: 8,439 / 8,439 parent mtime preserved PASS
```

## 14. Bake artifacts

```text
Overlay:
ASH_P1B_FIX_R2_ADAPTER_ONLY_GRADIENT_EXTRACTION_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256:
e1c496f6d18fa4861a745444f5fd16e279fedb270d477e281395e9dde4edb5d0
Files: 10
CRC: PASS

Full applied:
ASH_PASS3_P1B_FIX_R2_ADAPTER_ONLY_GRADIENT_EXTRACTION_AUTHORITY_CODE_ONLY.zip
SHA-256:
9f505b24997da4436e8c758bc61a08903548ccd01eb7e13280125feb0f08db2d
Files: 8,449
CRC: PASS
```

Both artifacts contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths.

## 15. User-side qualification

Apply the R2 overlay over the FIX-R1 tree and keep the FIX-R1 receipt under `target/p1bfixr1/receipts/`. Do not run workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release --locked
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
cargo test -p ash_p1br1a2_release_observer --release --locked
cargo test -p base_train --lib --locked
.\target\release\ash_p1br1a2_release_observer.exe current-adapter-only-gradient-authority
```

Strong expected closure:

```text
C0-adapter-only-gradients=BuildPass
C1-full-hybrid-negative=SameE0275
root-cause-status=FullHybridModuleVisitDemandRootConfirmed
base-model-parameter-visit-negative-seal=true
C2-adapter-optimizer-step=BuildPass
canonical-release=BuildPass
final-status=FullBaseTrainReleaseClosed
```

If C0 itself is SameE0275, stop this repair hypothesis and continue associated-type extraction inside adapter-only module visitation.

## 16. Final law

P1B-FIX-R2 repairs optimizer/module authority instead of forcing the traversed WGPU graph to satisfy a blanket Sync demand. HybridTrainModel remains forward authority and TrainableAdapterSet becomes the sole production gradient-extraction and optimizer owner. The same revision retains an explicit full-hybrid negative control. Only adapter-only BuildPass plus exact full-hybrid SameE0275 establishes strong causal attribution. After adapter-only optimizer-step validation, the uncut canonical release build is final authority. `FullBaseTrainReleaseClosed` closes the original P1B E0275 bug and no further observer expansion is required.