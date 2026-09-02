# ASH-TRAINABLE-GENERATION-DURABLE-REFERENCE-ADAM-RECOVERY-HEAD-AND-ORDINARY-STEP-FULL-MV-PAYLOAD-RETIREMENT-R3D

## 0. Revision

```text
Patch ID:
ASH-TRAINABLE-GENERATION-DURABLE-REFERENCE
-ADAM-RECOVERY-HEAD
-AND-ORDINARY-STEP-FULL-MV-PAYLOAD-RETIREMENT-R3D

Short name:
ADAM'S RIB EVE R3D
ORDINARY-STEP ADAM PAYLOAD RETIREMENT

Status:
STATIC DURABLE CONTRACT MATERIALIZATION RELEASE

Rust compile PASS: NOT CLAIMED
GPU physical PASS: NOT CLAIMED
Crash/restart physical PASS: NOT CLAIMED
N8 PASS: NOT CLAIMED
```

Source truth:

```rust
TRAINABLE_GENERATION_ADAM_PAYLOAD_RETIREMENT_MATERIALIZED_R3D = true
```

Physical token:

```text
HOLD_ASH_EVE_R3D_PHYSICAL_PENDING
```

## 1. Direct Parent

R3D inherits:

```text
ASH-EVE-HIMUON-FULL-TRAINABLE-GENERATION
-PRODUCTION-CALLSITE-ATOMIC-CUTOVER
-AND-LEGACY-PARTIAL-COMMIT-RETIREMENT-R3C1
```

R3C1 remains the live runtime generation authority joining Eve, HiMuon, Resident Weight, B06 metadata, and the full-device generation beneath `TrainableGenerationCommitSealR3C`.

R3D changes durable representation only. It does not change Adam mathematics, HiMuon mathematics, optimizer routing, parameter eligibility, or R3C/R3C1 generation identity.

## 2. Central Problem

Historical durable contracts still assume every target generation carries:

```text
MODEL_WEIGHT_PACK
ADAM_M_PACK
ADAM_V_PACK
MUON_MOMENTUM
```

`TrainableGenerationDurabilityDescriptorR1` and `PackedRuntimeStateManifestV1` bind those payloads explicitly.

R3D retires automatic ordinary-step Adam M/V payload duplication without mutating the meaning of those historical formats.

## 3. Central R3D Invariant

Under admitted R3D:

```text
candidate/adam_m.r6pack = ABSENT
candidate/adam_v.r6pack = ABSENT
```

For an ordinary non-anchor generation:

```text
ordinary Adam M payload bytes = 0
ordinary Adam V payload bytes = 0
ordinary Adam payload files   = 0
Adam durable GPU D2H bytes     = 0
```

Adam target identity is represented by exact Eve state digests plus explicit recovery-head lineage.

## 4. Versioning Rule

R3D preserves:

```text
TrainableGenerationDurabilityDescriptorR1
PackedRuntimeStateManifestV1
legacy P3 transactional prepare R1
```

It does not make historical Adam participant roles optional and does not create zero-byte fake Adam participants.

R3D introduces versioned R2/R3D contracts.

## 5. Materialized Source

New modules:

```text
crates/base_train/src/optimizer_generation_ref_r3d.rs
crates/base_train/src/adam_recovery_anchor_r3d.rs
crates/base_train/src/trainable_generation_durability_descriptor_r2.rs
crates/base_train/src/trainable_generation_adam_payload_retirement_r3d.rs
```

All are exported by `base_train/src/lib.rs`.

Integration changes include the production multistep scheduler, config, pipeline, and `bin/base_train.rs`.

## 6. Admission

New CLI:

```text
--admit-ordinary-step-adam-payload-retirement-r3d
--adam-recovery-anchor-interval-steps N
```

Defaults:

```text
R3D = false
anchor interval = 0
```

When R3D is admitted:

```text
N >= 1
```

is mandatory.

Required parents include R3C1, R3C, R3B, and RAM-resident Eve Adam M/V.

The first R3D cut explicitly rejects:

```text
admit_n8_deferred_durable_writeback = true
```

because Weight remains durable every generation in this revision.

## 7. OptimizerGenerationRefR3D

R3D materializes:

```rust
OptimizerGenerationRefR3D
```

binding:

```text
training generation
optimizer generation
Eve RAM authority
Eve layout digest
Eve range-set digest
Adam M state SHA-256
Adam V state SHA-256
Eve candidate seal digest
R3B receipt digest
Adam math profile digest
full-trainable generation digest
coverage digest
Adam recovery binding
reference digest
```

Filename:

```text
optimizer_generation_ref.r3d.json
```

The M/V state digests are adopted from the exact R3B CandidateComplete receipt. R3D does not perform another full Eve M/V scan merely to create the reference.

An optimizer reference is generation evidence, not a recovery payload.

## 8. Durability Descriptor R2

R3D materializes:

```rust
TrainableGenerationDurabilityDescriptorR2
```

with typed states:

```rust
TrainableDurabilityClassR3D {
    OrdinaryGenerationReference,
    AdamRecoveryAnchor,
}

OptimizerDurabilityStateR3D {
    RuntimeResidentWithRecoveryReference,
    ExactRecoveryAnchor,
}
```

Descriptor R2 binds the optimizer ref, Weight, Muon, recovery head, cursor, scheduler, parameter-set digest, Weight manifest digest, full generation digest, coverage digest, rollback distance, and exact-target-restart eligibility.

Filename:

```text
trainable_generation_durability_descriptor.r2.json
```

R2 does not use the R1 four-participant cardinality rule.

## 9. Weight-Only R3D Manifest

R3D materializes:

```rust
PackedRuntimeWeightManifestR3D
```

at:

```text
packed_runtime_weight_manifest.r3d.json
```

It contains Weight geometry/digests and the optimizer-generation-reference digest. It does not contain Adam M/V payload filenames.

Historical manifest V1 is retained for compatibility and retained recovery hydration.

## 10. Candidate Writer Cutover

The production scheduler derives:

```text
candidate_adam_pack_writeback = false
```

whenever R3D is enabled, including the final loop step.

Thus the generation candidate itself never receives ordinary physical Adam M/V pack files.

The historical Descriptor R1 path is likewise gated by `!r3d_enabled`.

## 11. R3D P3 Transaction

R3D materializes:

```text
prepare_active_transactional_commit_r3d
finalize_active_transactional_commit_r3d
```

The R3D prepare validates:

```text
Weight durable payload
Muon momentum durable payload
OptimizerGenerationRefR3D
TrainableGenerationDurabilityDescriptorR2
```

and explicitly requires absence of:

```text
adam_m.r6pack
adam_v.r6pack
```

The R3D finalize validates target active-state generation/ref/descriptor identities and does not reopen Adam pack files.

## 12. Active Training-State V5

R3D introduces:

```text
ash.basetrain.training_state.v5.r3d
```

The active state binds:

```text
Descriptor R2 identity
OptimizerGenerationRef digest
recoveryHeadGeneration
exactTargetRestartEligible
optimizerDurabilityState
```

Historical V3/V4 remain accepted as parent schemas.

## 13. Runtime Head vs Recovery Head

R3D separates:

```text
runtime head
exact recovery head
```

Example:

```text
runtime head  = G105
recovery head = G104
```

is valid.

The descriptor records `rollbackDistance` and the scheduler enforces:

```text
runtime head - recovery head < configured anchor interval
```

No hidden recovery-window extension is permitted.

## 14. Recovery Cadence

Current source chooses a recovery anchor when:

```text
target optimizer generation % interval == 0
```

or on final writeback.

If no R3D recovery head exists, the first admitted R3D target forces an anchor.

The source enum also contains explicit-checkpoint and graceful-shutdown reason identities, but a separate general graceful-shutdown interception path is not physically claimed in this bake.

## 15. Adam Recovery Anchor

R3D materializes:

```text
AdamRecoveryAnchorManifestR3D
PreparedAdamRecoveryAnchorR3D
AdamRecoveryHeadR3D
```

Anchor M/V bytes come from Eve CandidateComplete RAM through:

```text
RamResidentAdamMv::candidate_logical_slices_r3b
```

using bounded windows.

Default current window:

```text
16 MiB
```

There is no full temporary Adam M/V Vec and no Adam durable GPU D2H.

Anchor output alternates between:

```text
optimizer/adam/recovery_a
optimizer/adam/recovery_b
```

## 16. Recovery Head

Head file:

```text
optimizer/adam/adam_recovery_head.r3d.json
```

It binds:

```text
recovery generation
optimizer generation
anchor slot
anchor manifest digest
M/V digests
Eve layout digest
retained run root
head digest
```

Current ordering is:

```text
prepare anchor
prepare deterministic head identity
prepare optimizer ref + Descriptor R2
commit filesystem target
retain full recovery-generation bundle
persist recovery head
enter R3C1 live runtime commit
```

Power-loss behavior at every instruction boundary remains a physical qualification item.

## 17. Self-Contained Recovery Retention

R3D materializes:

```rust
RecoveryGenerationRetentionFenceR3D
retain_recovery_generation_bundle_r3d(...)
```

The retained root preserves the exact recovery generation against later A/B slot reuse.

It carries the generation's Weight, Muon momentum, active/control state, R3D metadata, and exact Adam recovery M/V.

The anchor M/V are copied into the retained slot under legacy `adam_m.r6pack` / `adam_v.r6pack` names solely so the existing verified RAM hydration reader can consume them.

Those files are recovery-anchor payload, not ordinary generation payload.

## 18. Fresh Resume Rule

For an admitted R3D V5 resume, `load_source` always follows:

```text
adam_recovery_head.r3d.json
        ↓
retained_run_root
        ↓
retained active training state
```

This is true even when runtime head equals recovery head.

R3D does not guess Adam files from the current generation directory.

Once recovery generation `D` is selected, the complete retained run root `D` is loaded. Mixed-generation restart is forbidden.

## 19. Ordinary Generation Durable Output

An ordinary R3D generation writes:

```text
Weight durable payload
Muon momentum durable payload
OptimizerGenerationRefR3D
PackedRuntimeWeightManifestR3D
TrainableGenerationDurabilityDescriptorR2
cursor/scheduler/control evidence
```

and no ordinary full Adam M/V payload.

## 20. Anchor Generation Durable Output

An anchor generation also keeps ordinary Adam packs absent from the generation candidate.

The separate recovery authority writes:

```text
recovery_[a|b]/adam_m.f32
recovery_[a|b]/adam_v.f32
recovery_[a|b]/anchor_manifest.r3d.json
```

then retains the full recovery generation and promotes the head.

## 21. Current Scope Limits

R3D does not yet reduce:

```text
Weight durable bytes
Muon momentum durable bytes
```

It also does not implement:

```text
Weight successor delta journal
Muon durable cadence reduction
historical arbitrary-generation Adam resume
per-step Adam delta journal
Device-Hot Eve
WGPU26 callback cutover
```

## 22. R3D Receipt

R3D materializes:

```rust
TrainableGenerationAdamPayloadRetirementReceiptR3D
```

with per-step fields including Weight/Muon bytes, optimizer-ref digest, Eve M/V digests, recovery head/age, rollback distance, anchor bytes, ordinary Adam bytes/file count, durable Adam GPU D2H, Descriptor R2 digest, and physical-pass claim.

Current admitted source constructs:

```text
ordinary_adam_m_payload_bytes = 0
ordinary_adam_v_payload_bytes = 0
ordinary_adam_payload_file_count = 0
adam_durable_gpu_d2h_bytes = 0
full_adam_host_candidate_allocation_count = 0
physical_pass_claimed = false
```

These remain source-level intended telemetry until a physical run verifies them.

## 23. R3C1 Binding

R3D durable evidence is prepared before the R3C1 live no-fail tail.

The R3C/R3C1 transaction consumes durable-parent identity rather than rewriting Adam durability after runtime commit.

After successful runtime commit:

```text
OptimizerGenerationRef target
==
TrainableGenerationCommitSealR3C target
```

must hold.

## 24. Static Validator

New:

```text
tools/validate_ash_trainable_generation_adam_payload_retirement_r3d_static.py
```

Result:

```text
41 / 41 PASS
```

Token:

```text
PASS_ASH_TRAINABLE_GENERATION_DURABLE_REFERENCE_ADAM_RECOVERY_HEAD_AND_ORDINARY_STEP_FULL_MV_PAYLOAD_RETIREMENT_R3D_STATIC
```

The gate verifies version separation, R3C1/R3B parents, optimizer ref, Descriptor R2, Weight-only manifest, ordinary Adam-pack suppression, P3 R3D no-Adam reopen, bounded Eve anchor streaming, A/B recovery head, retention bundle, fresh-resume redirect, V5 active schema, rollback-window enforcement, and zero ordinary Adam payload telemetry.

## 25. Parent Regression

R3D retained PASS for:

```text
Eve R1
Eve R2
Eve R3
R3A
R3B
R3C
R3C1
HiMuon route-sparse R1
packed/canonical bridge R1A
sparse overlay R1B
MCU AdamW pending scheduler
full-model device segmented successor
SubmissionEpoch active async
R3D static gate
```

Result:

```text
14 / 14 PASS
```

## 26. Existing Baseline Failures

Two historical validator families remain identical to the R3C1 parent.

RAM36 process budget:

```text
60 / 63 PASS

existing failures:
main release receipt gate
main exact binary gate
release cf1 parent required
```

Persistent Weight residency:

```text
existing failures:
[30] candidate builder digest
[32] candidate successor no second full digest scan
```

These are not new R3D regressions and are not reported as PASS.

## 27. Compile Boundary

The bake environment exposes no:

```text
cargo
rustc
rustfmt
```

All R3D-changed Rust files pass non-compiler balanced-delimiter and UTF-8 checks, and the new Python validator passes `py_compile`.

These checks are not Rust compilation.

No compile PASS is claimed.

## 28. Physical Qualification

A future ordinary-step physical canary must prove:

```text
candidate Adam M/V pack files absent
ordinary Adam bytes = 0
optimizer ref exact
Descriptor R2 exact
Weight/Muon durable
R3C1 runtime commit exact
recovery head unchanged
next step continues from Eve RAM
```

A future anchor canary must prove bounded Eve RAM streaming, exact anchor M/V digests, zero durable Adam GPU D2H, retained recovery generation, and atomic recovery-head promotion.

A crash test with runtime head ahead of recovery head must restart the complete retained recovery generation, never a mixed state.

The first-head bootstrap and every power-loss window remain physically unqualified in this static bake.

## 29. Physical PASS Token

Reserved:

```text
PASS_ASH_TRAINABLE_GENERATION_DURABLE_REFERENCE_ADAM_RECOVERY_HEAD_AND_ORDINARY_STEP_FULL_MV_PAYLOAD_RETIREMENT_R3D_PHYSICAL
```

Until then:

```text
HOLD_ASH_EVE_R3D_PHYSICAL_PENDING
```

## 30. Direct Successor

After R3D compile and physical qualification:

```text
ASH-BASETRAIN-WEIGHT-KEYFRAME
-AND-BIT-EXACT-SUCCESSOR-DELTA-JOURNAL-R3E
```

is the natural next storage-reduction revision.

R3E targets periodic full Weight keyframes plus exact G→G+1 successor journals with bit-exact reconstruction evidence.

## 31. Final Invariant

```text
Eve owns live Adam M/V.

Ordinary generations no longer re-bake Eve's entire M/V body into their generation directories.

OptimizerGenerationRefR3D records exactly which Eve state existed.

Adam recovery anchors contain the bytes required after process loss.

The recovery head retains the rest of that exact trainable generation so restart cannot mix generations.

Fresh R3D resume follows the explicit recovery head, never a filename heuristic.

Any gap between runtime head and recovery head is explicit bounded rollback.

Metadata is evidence.
Recovery anchor bytes are reconstruction.
The two are never silently conflated.
```

Final sentence:

> **R3D is the durable cut where Adam stops being re-baked into every ordinary training generation. Eve remains the live FP32 M/V authority in RAM, ordinary generations carry exact optimizer lineage, and only deliberate recovery anchors carry the full Adam bytes required for fresh-process reconstruction. Any gap between runtime head and recovery head is explicit bounded rollback, never fake exact resume.**
