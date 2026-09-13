# ASH-EVE-MCU-R3C-R2

## CONSUMING FULL-TRAINABLE GENERATION COMMIT AUTHORITY

```text
+ PRIVATE COMMIT PERMIT
+ NO EXTERNAL PREPARED DECOMPOSITION
+ SINGLE CONSUMING COMMIT ENTRY
+ MODEL / ADAM / MUON GENERATION BINDING
+ WEIGHT OWNERSHIP + DEVICE ROTATION PERMIT OWNERSHIP
+ CURSOR / SCHEDULER TRANSITION PREPARATION
+ PREPARE-AFTER-MUTATION DRIFT GUARD
+ COMMIT SEAL INTERNALIZATION
+ POST-COMMIT TARGET PROGRESS BINDING
+ NO SHA POLICY CHANGE
+ NO GPU COMPLETION LEASE YET
```

## 0. Revision

```text
Patch ID: ASH-EVE-MCU-R3C-R2
Direct parent: EVE-MCU-R3C-R1 RELEASE-SAFE PREPARED GENERATION TRANSITION
Class: CONSUMING FULL-TRAINABLE GENERATION COMMIT AUTHORITY
```

R1 parent evidence supplied by operator:

```text
cargo test -p base_train --lib --release --locked r3c_release_safe_prepared_generation_transition
PASS

cargo build -p base_train --bin base_train --release --locked -j 1
PASS
```

R2 does not reinterpret R1 evidence as R2 compile/runtime evidence.

## 1. Problem

Before R2, the production scheduler could decompose:

```text
FullTrainableGenerationCommitPermitR3C
    -> prepared.eve
    -> prepared.b06_permit
    -> prepared.muon
    -> external prepared_device_rotation
    -> external prepared_weight_ownership
    -> external precomputed seal
```

and then invoke Adam, Muon, Weight and seal mutation independently.

The generation numbers were checked, but the production callsite still held the subcommit capabilities separately.

R2 changes the authority boundary from:

```text
check shared generation
then perform several independent commits
```

to:

```text
prepare one opaque permit
revalidate source authority
consume one permit
perform internal no-fail tail
return one committed-generation result
```

This is an authority-structure change, not an optimizer-math change.

## 2. Private Permit Law

`FullTrainableGenerationCommitPermitR3C` is opaque.

Required implementation state:

```rust
pub struct FullTrainableGenerationCommitPermitR3C {
    prepared: FullTrainableGenerationPreparedR3C,
    permit_digest: String,
}
```

Public movable prepared fields are forbidden.

Read-only observation is permitted through accessors such as:

```text
permit_digest()
source_generation()
target_generation()
target_cursor_digest()
target_scheduler_step()
target_scheduler_profile_digest()
```

The final permit does not implement `Clone`.

## 3. Permit-Owned Commit Components

R2 binds the following into the private prepared authority:

```text
TrainableGenerationIdentityR3C
PreparedEveAdamCommitR3C
FullModelDeviceCommitPermit
B04PreparedFullModelPromotion
PreparedResidentWeightOwnershipPromotionR3C1
PreparedFullTrainableDeviceRotationR3C1
FullTrainableCoverageReceipt
TrainableSubmissionEpochUnionR3C
TrainableGenerationSourceSnapshotR3C2
PreparedTrainingProgressTransitionR3C2
TrainableGenerationCommitSealR3C
```

The scheduler no longer owns Weight ownership preparation and device rotation as independent commit capabilities after the final permit is formed.

## 4. Source Snapshot

R2 materializes:

```text
TrainableGenerationSourceSnapshotR3C2
```

which binds:

```text
source trainable generation
RAM Adam committed generation
Muon/hybrid committed generation
resident Weight generation
source cursor digest
source cursor next-batch ordinal
source scheduler step, when present
source scheduler profile digest, when present
```

Admission requires:

```text
Adam generation == source generation
Muon generation == source generation
Weight generation == source generation
```

No missing scheduler state is fabricated.

## 5. Cursor / Scheduler Transition

R2 materializes:

```text
PreparedTrainingProgressTransitionR3C2
```

which binds:

```text
source cursor digest
source next-batch ordinal
target cursor digest
target next-batch ordinal
source scheduler identity
target scheduler step
target scheduler profile digest
source generation
target generation
```

The target scheduler step must equal the target optimizer generation.

The actual cursor and scheduler payloads remain owned by the existing scheduler path. R2 binds their exact identities; it does not add a new dataset or scheduler storage format.

## 6. Prepared Digest Extension

The R3C prepared digest additionally covers:

```text
Weight ownership prepared digest
device rotation prepared digest
source snapshot digest
progress transition digest
```

The permit digest remains:

```text
R3C_PERMIT(prepared_digest)
```

No tensor content digest is redefined.

## 7. Commit Seal Internalization

The trainable generation commit seal is built inside the R3C preparation authority after the permit digest exists.

Ordering:

```text
component prepared identities
    -> prepared digest
    -> permit digest
    -> commit seal
    -> final opaque permit
```

The scheduler no longer reconstructs the final seal from loose subcommit digests.

## 8. Precommit Drift Guard

Immediately before the first irreversible mutation, the single commit authority re-observes:

```text
RAM Adam committed generation
Muon/hybrid committed generation
resident Weight generation
source cursor identity
source scheduler identity
```

and compares them with the sealed source snapshot.

Failure tokens include:

```text
E_R3C2_PRECOMMIT_ADAM_SOURCE_DRIFT
E_R3C2_PRECOMMIT_MUON_SOURCE_DRIFT
E_R3C2_PRECOMMIT_WEIGHT_SOURCE_DRIFT
E_R3C2_PRECOMMIT_CURSOR_SOURCE_DRIFT
E_R3C2_PRECOMMIT_CURSOR_GENERATION_DRIFT
E_R3C2_PRECOMMIT_CURSOR_ORDINAL_DRIFT
E_R3C2_PRECOMMIT_SCHEDULER_STEP_DRIFT
E_R3C2_PRECOMMIT_SCHEDULER_SOURCE_DRIFT
```

All such failures occur before the internal commit tail.

No silent source-generation repair is allowed.

## 9. Single Consuming Entry

Production scheduler uses exactly one mutation entry:

```text
commit_full_trainable_generation_r3c2(...)
```

The scheduler no longer directly invokes:

```text
commit_prepared_candidate_no_fail_r3c
commit_prepared_generation_parts_no_fail_r3c1
commit_resident_weight_ownership_no_fail_r3c1
install_trainable_generation_commit_seal_no_fail_r3c1
```

Those operations occur only inside the consuming R3C2 authority for the production path.

## 10. Internal Tail Ordering

After the precommit guard passes, R2 preserves the existing logical ordering:

```text
1. EVE / RAM Adam prepared commit
2. Muon prepared promotion
3. B06 hybrid metadata commit
4. full trainable device rotation
5. resident Weight ownership promotion
6. trainable generation seal installation
```

R2 does not introduce a performance-oriented reorder.

## 11. Committed Result

Successful commit returns:

```text
CommittedFullTrainableGenerationR3C2
```

containing:

```text
target generation
permit digest
commit seal
target cursor identity
target scheduler identity
source snapshot digest
progress transition digest
post-commit Weight retirement obligation
Muon promoted-parameter count
committed digest
```

The post-commit target progress validator rejects a cursor/scheduler identity that differs from the one already sealed into the permit.

## 12. Production Witness

R2 adds the compact witness:

```text
[ASH-EVE-MCU-R3C-R2]
source=<G:O>
target=<G:O>
permit=<digest>
sourceSnapshot=<digest>
progressTransition=<digest>
committed=<digest>
precommitDriftGuard=PASS
singleConsumingCommit=1
externalPreparedDecomposition=0
```

This is an authority witness, not tensor-content proof.

## 13. R1 Preservation

R2 preserves R1 semantics:

```text
EVE next-state transition occurs during prepare
no semantic mutation exists inside debug_assert!
release/debug generation transition semantics remain identical
commit installs already-prepared EVE state
```

`ram_resident_adam_mv.rs` is byte-preserved from the R1 bake.

## 14. SHA Policy Preservation

R2 does not modify:

```text
ExactSha256
RuntimeIdentity
candidate Weight digest policy
candidate Adam M/V digest policy
BP-DK exact digest policy
canary committed-step digest policy
checkpoint digest policy
```

No SHA performance claim is made by R2.

## 15. GPU Completion Non-Claim

R2 binds submission identity already present in R3C but does not introduce GPU completion typestate.

Therefore:

```text
submission recorded in permit
!= GPU completion proven by R3C2 type system
```

`Pending -> Completed -> Prepared` mutation lease authority remains a later R3G revision.

## 16. Residency / Numerical Non-Claims

R2 does not change:

```text
Muon math
Adam math
Weight update math
dtype
learning rate
BP-DK policy
allocator / arena policy
source-target VRAM residency
wait / submission scheduling
dense backward kernels
```

Performance remains unmeasured.

## 17. Static Acceptance

Baked source was statically checked for:

```text
permit public fields = 0
scheduler r3c_permit.prepared access = 0
scheduler direct EVE subcommit = 0
scheduler direct Muon subcommit = 0
scheduler direct Weight subcommit = 0
scheduler direct seal install = 0
scheduler consuming R3C2 commit entry = 1
R3C2 authority new if-statements = 0
modified Rust lexical delimiter balance = PASS
```

Two narrow unit tests were added:

```text
r3c_r2_source_snapshot_rejects_generation_drift
r3c_r2_progress_transition_binds_target_scheduler_step
```

These tests have not been executed in the bake environment because no Rust toolchain is installed there.

## 18. Compile / Runtime Acceptance

Required operator-side commands:

```powershell
cargo test -p base_train --lib --locked `
  r3c_r2_
```

```powershell
cargo test -p base_train --lib --release --locked `
  r3c_r2_
```

```powershell
cargo build -p base_train --bin base_train --release --locked -j 1
```

Promotion requires all three to pass.

Physical production promotion additionally requires a real R3C2 witness with:

```text
precommitDriftGuard=PASS
singleConsumingCommit=1
externalPreparedDecomposition=0
```

and exact source-to-target generation agreement across Adam, Muon and Weight.

## 19. Forbidden Repairs

```text
NO public permit prepared field
NO public into_parts decomposition
NO Clone on final permit
NO scheduler-side subcommit sequence
NO independently rebuilt scheduler-side commit seal
NO post-prepare target-generation rewrite
NO silent generation repair
NO synthetic source scheduler
NO early source retirement
NO SHA policy change
NO GPU completion claim
NO allocator change
NO optimizer math change
NO BP-DK policy change
```

## 20. Bake Seal

Code delta from R1 parent:

```text
ADD 0
MOD 3
DEL 0
```

Modified source SHA-256:

```text
8a5ad62bd05069f02c53391bc7ff1aa6cbd55ee6161ba189f1cfeb572711e54b  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
670209ea39785a3053edf95d31d5c7c58bb4931663e6f80d82b09763aaec2a88  crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
5097f7f5d67affcd226ff2d5a8bdba9369de344a6a5bafd69f52ab17ed720de4  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

R1 release-safe Adam source preserved:

```text
60a8d90cae0fb842039c5809c0cb45432dc3efb1e2e94de914c1f010296f7285  crates/base_train/src/ram_resident_adam_mv.rs
```

Full code-only ZIP:

```text
ASH_PASS3_EVE_MCU_R3C_R2_CONSUMING_FULL_TRAINABLE_GENERATION_COMMIT_AUTHORITY_CODE_ONLY.zip
SHA-256: 662e072fdf634e0466297cde96d26a04fd686482ce7b7f1e7e2769c489ccf443
files: 8424
CRC: PASS
```

Archive exclusions:

```text
top-level specs/    excluded
top-level artifacts/ excluded
runtime/data manifest payloads inherited as excluded from the R1 code-only parent
specification file itself is not inside the ZIP
```

## 21. Evidence Status

```text
SOURCE / STATIC   PASS
ARCHIVE CRC       PASS
COMPILE           UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME TEST      UNVERIFIED IN BAKE ENVIRONMENT
PHYSICAL          UNVERIFIED
PERFORMANCE       UNMEASURED
```

No higher evidence tier is claimed.

## 22. Completion Law

R2 is promoted only when:

```text
opaque non-Clone permit
+ no scheduler prepared decomposition
+ one consuming production commit entry
+ source Adam/Muon/Weight snapshot exact
+ cursor/scheduler transition bound before commit
+ precommit drift guard passes
+ commit result binds target cursor/scheduler identity
+ debug test PASS
+ release test PASS
+ release build PASS
```

Recommended static/compile promotion token:

```text
PASS_EVE_MCU_R3C_R2_CONSUMING_FULL_TRAINABLE_GENERATION_COMMIT_AUTHORITY
```

Physical campaign promotion remains separate.
