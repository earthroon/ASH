# ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15

## Status

```text
Patch ID: ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
Direct parent: ASH-BP-DK-FUSION-POLICY-CANDIDATE-CANARY-QUALIFICATION-14
Purpose: explicitly transfer production 05 Fusion/Fission policy selection authority from the current source policy to the exact 14-qualified candidate through a durable restart-bound managed-policy transaction

Production activation authority: introduced here
Live in-process policy hot reload: unsupported R1
Mid-generation policy mutation: forbidden
Automatic activation from 14: forbidden
Automatic post-commit rollback: forbidden
New Delta-K formula: none
New Fusion/Fission predicate: none
New Muon mathematics: none
New Fusion/Muon WGSL: none
Precision authority: unchanged
Residency authority: unchanged
36-GiB RAM authority: unchanged
```

Current bake status:

```text
15_MANAGED_POLICY_AUTHORITY_SOURCE_PATH_WIRED
15_BOOTSTRAP_SOURCE_PATH_WIRED
15_DURABLE_POINTER_ACTIVATION_SOURCE_PATH_WIRED
15_MANAGED_PRODUCTION_LAUNCHER_SOURCE_PATH_WIRED
15_FIRST_PRODUCTION_GENERATION_WITNESS_SOURCE_PATH_WIRED
15_EXPLICIT_ROLLBACK_SOURCE_PATH_WIRED
15_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_00_14_AND_LOCAL_MUON_STATIC_LINEAGE_PASS
USER_LOCAL_RUST_AND_PRODUCTION_EXECUTION_UNVERIFIED
```

---

## 1. Direct-parent authority

15 admits only a valid 14 qualification lineage whose result is:

```text
qualification scope = BoundedTrainingCanary
qualification state = QualifiedForActivationReview
activation_review_eligible = true
```

The exact candidate policy digest must equal the candidate sealed by 14.

15 does not accept:

```text
CandidateRuntimeQualified only
ComparativeEvidenceInsufficient
ComparativeNotQualified
OfflineReplayQualified
ShadowQualificationUnavailableR1
```

and it does not substitute a similar candidate policy.

The production policy at activation time must still equal the 14 source-policy digest. A changed current policy makes the qualification stale and requires a new 12 -> 13 -> 14 lineage.

---

## 2. Second explicit operator decision

13 answers:

```text
may this exact candidate enter qualification?
```

15 separately answers:

```text
may this exact qualified candidate become production policy authority?
```

15 therefore defines an explicit production-activation decision surface:

```text
ActivateCandidate
RejectActivation
DeferActivation
```

No 14 result automatically calls `ActivateCandidate`.

No default/timeout/force acceptance route is introduced.

---

## 3. R1 is restart-bound, not live hot reload

15 R1 does not modify the running production trainer in the middle of a generation.

Canonical transition:

```text
source policy generation(s) committed
-> durable source checkpoint / activation barrier
-> trainer quiescent
-> atomic active-policy pointer transaction
-> managed BaseTrain restart
-> first candidate-policy production generation
```

The active pointer is resolved once by the 15 managed launcher before the existing BaseTrain child starts.

The pointer is not polled per parameter or per generation and is not hot-reloaded into a live child process.

`InProcessLivePolicyHotReload` is not claimed in R1.

---

## 4. Parent production code remains byte-preserved

15 deliberately does **not** patch the existing production BaseTrain engine, scheduler, TensorCube/Muon production callsite, 05 planner, 12 recommendation path, 13 review path, or 14 canary path.

Important preserved anchors include:

```text
crates/base_train/src/bin/base_train.rs
20c767d68b91e7b8aa4a0bee1f9fb356daebe1bbb4c6deef6784a08831863e54

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
33d096c9d2b6d90cef0e27d763eb1658cc56daa4d4c4d3988ff004deed120e99

crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
658057cb28df64ac35296cedae093f78e40ffb9087b55d88072596006be7e32c

05 planner core
53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

05 planner BaseTrain runtime
70e6d4f08e89d4693c1999ff4508ec09ad4fcfe9850e2bb914127702f5f618cc
```

Production integration is provided by a new 15 managed launcher that resolves the durable pointer and launches the existing BaseTrain binary under an exact child-process policy environment.

This preserves 14's isolation contract and avoids creating a second training implementation.

---

## 5. Policy semantics and policy selection are separate SSOTs

R1 separates:

```text
policy semantics SSOT
= immutable policy artifact

production selection SSOT
= active-policy pointer
```

Managed policy store:

```text
<policy-root>/
  policies/
    <canonical-policy-digest>.json

  active/
    bp_dk_fusion_active_policy.json
```

The policy artifact is immutable. Production activation does not edit an existing policy JSON in place.

The only intended mutable selection authority is the active pointer transaction.

---

## 6. One-time managed-authority bootstrap

The 14 parent predates the 15 active-pointer authority, so a first 15 candidate activation cannot assume a pointer already exists.

15 therefore provides a one-time explicit:

```text
bootstrap-managed-authority
```

Bootstrap does **not** change policy semantics.

It:

```text
validates the current source policy
validates a current activation barrier
writes the current source policy to the immutable digest-named store
creates active pointer revision 1 pointing to that same source policy
writes immutable bootstrap intent/receipt evidence
```

Candidate promotion occurs only after bootstrap and creates pointer revision 2 or later.

There is no hidden initialization of production policy authority.

### Legacy-trainer boundary

The 15 managed trainer/activation lock can mutually exclude 15-managed processes. A pre-15 unmanaged legacy trainer cannot retroactively honor a lock it did not know about.

Therefore the one-time migration into managed authority still requires the operator to have stopped any legacy direct-path trainer before sealing the bootstrap barrier. 15 does not claim magical visibility into an unrelated legacy process.

---

## 7. Active pointer schema and acyclic digest graph

`AshBpDkFusionActivePolicyPointer` binds:

```text
pointer revision
policy revision
policy canonical digest
relative immutable policy artifact path
activation intent digest
previous pointer digest
effective-after optimizer generation
pointer digest
```

The digest graph is intentionally acyclic.

The pointer binds the **activation intent digest**.

It does not bind the later pointer-commit receipt digest.

After the pointer is committed, `AshBpDkFusionPolicyActivationCommitReceipt` binds:

```text
activation intent digest
previous pointer digest
new active pointer digest
source policy digest
candidate policy digest
pointer revision
authorized pointer swap count
commit digest
```

This avoids a circular construction where pointer digest and commit digest would recursively depend on each other.

---

## 8. Immutable previous-pointer archive

A digest alone is not sufficient rollback authority because rollback needs the exact previous pointer bytes.

Before swapping the active pointer, activation archives:

```text
activations/<activation-intent-digest>/previous_pointer.json
activations/<activation-intent-digest>/committed_pointer.json
```

Rollback uses the exact archived previous pointer.

It does not reconstruct a historical pointer from scattered metadata.

---

## 9. Single managed trainer-authority lock

15 introduces one managed authority lock:

```text
runtime/bp_dk_fusion_managed_trainer_authority.lock
```

The lock uses exclusive `create_new` ownership.

The following 15-managed operations require the same lock:

```text
activation-barrier sealing
managed-authority bootstrap
activation prepare
active-pointer commit
managed production child execution
rollback
```

Thus a 15-managed trainer and a 15-managed activation transaction cannot simultaneously own production policy authority.

---

## 10. Activation barrier is measured, not asserted

15 does not accept a user-provided `trainerQuiescent=true` string as sufficient authority.

`seal_managed_activation_barrier()` acquires the managed trainer lock and derives the barrier from actual committed state.

The barrier binds:

```text
last committed training generation
last committed optimizer generation
last committed BP generation
source checkpoint authority digest
source policy digest
pending-state count
trainer-quiescent state
durable-checkpoint state
barrier digest
```

Pending `.partial`, `.tmp`, and `.staging` state is rejected.

The BP-generation boundary is verified against the committed 12 replay-evidence head.

If 12 replay evidence needed to seal the barrier is unavailable, 15 fails closed rather than inventing the BP boundary.

---

## 11. Bounded checkpoint authority witness

15 does not claim to recursively rehash every potentially huge checkpoint payload file.

The R1 checkpoint authority witness is deliberately bounded to the existing canonical active-state authority:

```text
training_state/active_training_state.json
active training/optimizer generations
active packed-state slot
packed_state_manifest.json physical file digest
active state's declared packed-manifest digest when present
active state's declared training-state digest when present
```

The resulting authority digest is used by the activation barrier and managed transition checks.

This is a precise bounded witness, not a false full-directory byte-integrity claim.

---

## 12. Prepare is not activation

`prepare`:

```text
validates exact 14 candidate lineage
validates source/current pointer freshness
validates the activation barrier
writes the immutable candidate policy artifact
writes a durable activation intent
```

and leaves the active pointer unchanged.

The intent binds at minimum:

```text
operator identity
14 qualification receipt digest
13 qualification ticket digest
13 review receipt digest
source policy digest
candidate policy digest
current pointer digest
activation barrier digest
pre-activation checkpoint digest
effective-after optimizer generation
intent digest
```

---

## 13. Atomic pointer commit

`activate` requires the exact prepared intent, exact current barrier and explicit:

```text
ACTIVATE_CANDIDATE
```

decision.

The transaction:

```text
reacquires the trainer-authority lock
revalidates the barrier against the current checkpoint
revalidates current pointer/source policy
loads and validates the immutable candidate policy
builds next pointer revision
archives old/new exact pointer bytes
writes a temporary pointer
syncs and rereads the staged pointer
atomically replaces the active pointer
syncs the active directory
rereads committed pointer
writes immutable pointer-commit receipt
```

On Windows, the replacement path uses `MoveFileExW` with replacement/write-through semantics. On Unix, the active-file replacement uses rename followed by directory sync.

There is no delete-then-create pointer gap.

---

## 14. Managed production launcher

15 adds a `run-managed-production` command rather than modifying the existing production BaseTrain binary.

The launcher:

```text
acquires the managed trainer-authority lock
rejects parent-process direct ASH_BP_DK_FUSION_POLICY_PATH authority
resolves the exact active pointer once
loads/validates the immutable policy artifact
validates resume-policy binding/transition authority
launches the existing BaseTrain child
injects exact branch-local ASH_BP_DK_FUSION_POLICY_PATH into the child only
requires 05 planner ACTIVE
waits for child completion
verifies pointer did not change during the run
writes checkpoint policy binding into the newly committed active state
```

The child still executes the existing BaseTrain/05/Muon/Fusion implementation.

15 owns selection authority, not optimizer mathematics.

---

## 15. No dual managed/direct policy authority

A managed production run rejects an externally inherited direct:

```text
ASH_BP_DK_FUSION_POLICY_PATH
```

before launching the child.

The managed launcher is responsible for setting the resolved exact policy artifact path inside the child process.

This prevents the parent environment and the active pointer from competing as two production-policy SSOTs.

---

## 16. Managed BaseTrain argument contract

`run-managed-production` requires the existing production multistep admission and an explicit resume state.

The managed output root must exactly match the BaseTrain `--output-dir` authority.

The wrapper does not silently invent a different production run topology.

Normal production horizon/N8 laws remain owned by the existing BaseTrain runtime.

---

## 17. Checkpoint policy binding

After a successful managed BaseTrain child run, 15 resolves the newly committed active training-state slot and writes:

```text
bp_dk_fusion_active_policy_binding.json
```

The binding seals:

```text
checkpoint training generation
checkpoint optimizer generation
active pointer digest/revision
policy revision/digest
activation intent digest
startup binding digest
binding digest
```

The canary/activation wrapper does not rewrite model state to make this binding true. It records the exact policy authority under which the committed state was produced.

---

## 18. Managed restart admission

Normal managed resume requires:

```text
checkpoint policy binding
== resolved active pointer policy
```

A checkpoint made under policy A cannot silently resume under currently active policy B.

### Explicit activation transition exception

The first restart after an activation may legitimately resume a pre-activation checkpoint whose binding is still the source policy.

That mismatch is permitted only when the launcher receives the exact activation intent and barrier and verifies:

```text
source checkpoint authority digest == intent pre-activation checkpoint digest
resume optimizer generation == barrier/effective boundary
source policy == intent source policy
active pointer == exact candidate pointer bound to the same intent
```

Legacy pre-15 checkpoints without a 15 binding use this same explicit transition authority. There is no silent “latest pointer wins” restart.

---

## 19. First production generation witness

A managed production launch may execute an N8-style multi-step span. Therefore the first candidate generation cannot be identified by simply taking the last captured 12 generation.

15 searches the committed replay evidence for the **first** generation satisfying:

```text
optimizer_generation
>
active_pointer.effective_after_optimizer_generation
```

That generation is the first candidate-policy production generation witness.

For every parameter plan in that generation:

```text
planner policy digest == candidate policy digest
```

must hold.

Any source/candidate mixture increments `mixed_policy_plan_count` and fails closure.

---

## 20. Activation closure

`close` requires the exact:

```text
14 qualification receipt
13 qualification ticket
13 review lineage
activation barrier
activation intent
pointer commit receipt
first production generation witness
```

The final production activation receipt reaches:

```text
ActivationClosed
```

only after the first candidate-policy production generation is physically present in committed branch evidence and its mixed-policy count is zero.

Pointer commit alone is not treated as proof that production execution succeeded.

---

## 21. 05 policy-change rebaseline remains canonical

15 does not implement a second Fusion/Fission planner-state reset algorithm.

When the candidate policy digest differs from the source policy digest, existing 05 policy-change/rebaseline semantics remain the planner authority.

15 changes which exact policy artifact is supplied to 05. It does not alter 05 Fusion/Fission predicates, candidate ordering, hysteresis or topology law.

---

## 22. R1 rollback support is deliberately bounded

During bake review, a false authority was explicitly removed: pointer rollback alone cannot truthfully claim that model checkpoint state was restored.

R1 physically supports only two rollback semantics.

### PreFirstCommitPointerRollback

Used after the candidate pointer was committed but before any candidate production generation committed.

It requires:

```text
exact activation commit receipt
no closed production-activation receipt
exact archived previous pointer
managed trainer lock
current active checkpoint digest == activation intent pre-activation checkpoint digest
current optimizer generation == activation effective boundary
```

If the optimizer generation has advanced, this mode fails closed.

This ensures the pointer is restored only while the durable model state is still the pre-activation source state.

### PolicyOnlyForwardRollback

Used after `ActivationClosed`.

It requires the exact closed activation receipt and matching activation commit/pointer lineage.

It restores the exact archived previous pointer, but explicitly records:

```text
model_state_contains_candidate_history = true
post_activation_generations_discarded = false
```

The current model/optimizer state is not pretended to have reverted.

---

## 23. Checkpoint-state rollback is explicit R1 non-support

`CHECKPOINT_STATE_ROLLBACK` is rejected by the 15 CLI with:

```text
ASH_BP_DK_FUSION_CHECKPOINT_STATE_ROLLBACK_UNAVAILABLE_R1
```

before a rollback pointer transaction is executed.

R1 does **not** create a receipt claiming model-state restoration when it has only swapped a policy pointer.

A future revision that supports checkpoint-state rollback must physically restore and verify the exact pre-activation model/optimizer/checkpoint authority before it may claim that semantic.

---

## 24. Rollback uses exact archived previous pointer

Both supported R1 rollback paths require:

```text
current_pointer.previous_pointer_digest
== exact target archived pointer digest
```

Rollback writes that exact pointer through the same staged active-file replacement and directory durability boundary.

It does not choose an arbitrary old policy file or reconstruct a pointer from a digest.

Rollback is explicit CLI authority. There is no automatic post-commit rollback.

---

## 25. Production authority counters

15 distinguishes legitimate activation from forbidden mutation.

An authorized atomic pointer swap is expected and is not counted as an authority violation.

Forbidden surfaces remain zero, including:

```text
unauthorized policy mutation
mid-generation policy mutation
dual policy authority
production hot reload
mixed-policy production generation
```

This differs intentionally from 14, where every production pointer mutation had to remain zero because 14 had no activation authority.

---

## 26. CLI surface

15 adds an offline/managed activation binary:

```text
crates/base_train/src/bin/
ash_bp_dk_fusion_policy_explicit_production_activation_15.rs
```

Subcommands:

```text
seal-barrier
bootstrap-managed-authority
prepare
activate
run-managed-production
verify-startup
verify-first-generation
close
rollback
```

No subcommand changes Fusion/Muon math or directly edits production model tensors.

---

## 27. Runner

15 adds:

```text
tools/run_ash_bp_dk_fusion_policy_explicit_production_activation_15.ps1
```

The runner assumes the overlay is already applied.

Its default `Validate` action runs:

```text
15 static validator
cargo fmt --all -- --check
cargo check of the 15 activation binary
```

Actual activation actions require an explicit `-Action` and explicit activation inputs.

No overlay ZIP search/application or `Expand-Archive` step is included.

---

## 28. Changed files

Relative to the 14 parent, the 15 bake differs in exactly eight files:

```text
crates/ash_core/src/fusion_policy_explicit_production_activation.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bin/ash_bp_dk_fusion_policy_explicit_production_activation_15.rs
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs
crates/base_train/src/lib.rs
tools/run_ash_bp_dk_fusion_policy_explicit_production_activation_15.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
```

No existing production scheduler/BaseTrain/TensorCube-Muon/05/12/13/14 implementation file is changed.

---

## 29. New 15 source anchors

```text
15 core
28b70cbf38c6700c36e7859cdf69ef4bd5096abd8812fcafd66130fd514709d5

15 BaseTrain activation runtime
a99c1b95ac0155494bcb42e057986b61cb7f7b7481b56ea32b2d0219a6f9bdba

15 activation binary
098924b591feca206b26330a96f377b176fa37d25f4dd7d1a229695bab73335f

15 runner
691aa15b5e4187aa62f77ff8b631129ccd2048f17d1007eeddada0b286469127

15 static validator
529266927a6e347d1957d7902a6247d476f15bd7558d04e8e6ab002f2da7389b
```

---

## 30. Static validation

New gate:

```text
validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
274/274 PASS
```

The gate seals, among other things:

```text
14/13/12/05 parent byte anchors
production BaseTrain/scheduler/callsite byte anchors
acyclic pointer/commit digest graph
one-time source-policy bootstrap
immutable policy store
single active pointer
managed trainer lock
bounded activation barrier/checkpoint witness
prepare-vs-activate separation
atomic active-pointer replacement
previous/committed pointer archive
managed BaseTrain child launch
no inherited direct policy authority
restart binding and explicit transition exception
first generation = first generation after effective boundary
zero mixed-policy plan authority
activation closure after physical first-generation witness
pre-first-commit rollback boundary
post-commit policy-only forward rollback boundary
checkpoint-state rollback explicit R1 non-support
no policy math duplication
no automatic objective/benefit logic
12 -> 13 -> 14 -> 15 CF1 order
```

---

## 31. Parent regression

After the final 15 rollback correction, the BP-DeltaK static lineage was rerun through 15 and remained PASS.

Counted gates include:

```text
01 Local BP-DK                                  134/134 PASS
05 Active Fusion/Fission Planner                293/293 PASS
06 Active Fusion Deterministic Replay           210/210 PASS
10 One-Step Objective Probe                     259/259 PASS
11 Long-Horizon Trajectory                      145/145 PASS
12 Policy Calibration Recommendation            227/227 PASS
13 Operator Review Gate                         247/247 PASS
14 Candidate Canary Qualification               347/347 PASS
15 Explicit Production Activation               274/274 PASS
```

All intermediate 00-14 validators also returned PASS.

Local Muon regression remained PASS:

```text
optimizer                                         101/101 PASS
FirstCandidate registry                            97/97 PASS
multi-tile batch                                   61/61 PASS
production callsite                                63/63 PASS
canonical-loader repair                            38/38 PASS
ExactSubgroup32 norm                              128/128 PASS
X PAD17                                            52/52 PASS
generation-sealed immutable cache                  66/66 PASS
immutable-cache backend rebind                     35/35 PASS
```

---

## 32. CF1 wiring

15 is appended after 14 in the existing static chain:

```text
12 recommendation
-> 13 operator review
-> 14 canary qualification
-> 15 explicit production activation
```

Earlier closure semantics remain intact.

---

## 33. Packaging

Delivered 15 artifacts:

```text
full-body bake
19,088,773 bytes
7,171 files
ZIP integrity PASS

overlay bake
44,380 bytes
exactly 8 files
ZIP integrity PASS
```

Both archives contain zero:

```text
target/
__pycache__/
*.sha256
generated artifact directories
generated report directories
generated manifest directories
```

No generated activation/bootstrap/rollback receipts are included because those artifacts must be produced from the user's real production authority and filesystem state.

---

## 34. Bake-environment boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU runtime/adapter
```

Therefore this bake does **not** claim:

```text
Rust compile success
real managed-authority bootstrap success
real trainer-lock behavior on the user's OS
real atomic production pointer swap
real BaseTrain managed restart
real first candidate production generation
real activation closure
real rollback execution
```

Static source-contract evidence is complete; user-local runtime evidence remains required.

---

## 35. Required user-local gates

Before declaring 15 physically qualified:

```text
cargo fmt --all -- --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_explicit_production_activation_15
CF1 reaches 15
```

Then validate in order:

```text
1. stop legacy direct-path trainer if migrating for the first time
2. seal activation barrier
3. bootstrap managed authority with the current source policy
4. verify pointer revision 1 still selects the same source policy
5. run source-policy managed production/resume and verify checkpoint binding

6. prepare exact 14 QualifiedForActivationReview candidate
7. verify prepare leaves active pointer unchanged
8. activate with explicit ACTIVATE_CANDIDATE
9. verify candidate pointer revision increments atomically
10. verify previous_pointer.json and committed_pointer.json match exact pointer bytes

11. run managed production from exact pre-activation checkpoint using intent + barrier transition authority
12. verify startup binding resolves candidate once
13. verify first optimizer generation greater than effective boundary uses candidate policy for every captured plan
14. verify mixed-policy plan count = 0
15. close activation only after physical first-generation witness
16. verify newly committed checkpoint carries exact candidate-policy binding

17. pre-first-commit failure fixture: restore exact previous pointer only while checkpoint digest/generation remain at pre-activation boundary
18. post-commit fixture: PolicyOnlyForwardRollback restores pointer but explicitly preserves candidate-trained model-state history
19. CHECKPOINT_STATE_ROLLBACK must fail with UNAVAILABLE_R1 and must not claim model restoration
```

---

## 36. Claim boundary after physical execution

After a real user-local `ActivationClosed` receipt, the supported statement is limited to:

```text
The exact 14-qualified candidate policy was explicitly activated through the 15 managed durable pointer authority at a committed production boundary, the managed BaseTrain restart bound to that exact candidate, and the first production generation after the effective boundary committed with zero mixed-policy plans.
```

This still does not establish:

```text
the candidate is universally better
the candidate improves generalization
the candidate can never require rollback
checkpoint-state rollback is implemented by 15 R1
live in-process hot reload is supported
```

---

## 37. Natural successor

The next observation stage is naturally:

```text
ASH-BP-DK-FUSION-POLICY-PRODUCTION-SOAK-AND-ROLLBACK-HEALTH-16
```

16 should monitor the activated policy over a production soak window, bind actual production trajectory/health to the 15 activation lineage, verify rollback readiness and keep activation history immutable.

It should not erase the fact that a candidate was once active even when a later rollback occurs.

---

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_POLICY_EXPLICIT_PRODUCTION_ACTIVATION_15

14_DIRECT_PARENT
QUALIFIED_FOR_ACTIVATION_REVIEW_REQUIRED
BOUNDED_TRAINING_CANARY_REQUIRED
EXACT_13_14_LINEAGE
SECOND_EXPLICIT_OPERATOR_ACTIVATION_DECISION

SOURCE_PRODUCTION_POLICY_FRESH
EXACT_CANDIDATE_POLICY_DIGEST
NO_CANDIDATE_SUBSTITUTION
NO_POLICY_DIFF_REBASE

RESTART_BOUND_ACTIVATION_R1
LIVE_IN_PROCESS_HOT_RELOAD_UNSUPPORTED_R1
NO_MID_GENERATION_POLICY_MUTATION

PRODUCTION_BASE_TRAIN_BYTE_PRESERVED
PRODUCTION_SCHEDULER_BYTE_PRESERVED
TENSORCUBE_MUON_PRODUCTION_CALLSITE_BYTE_PRESERVED
05_PLANNER_BYTE_PRESERVED
12_13_14_BYTE_PRESERVED

15_MANAGED_PRODUCTION_LAUNCHER
EXISTING_BASE_TRAIN_CHILD_REUSED

ONE_TIME_MANAGED_AUTHORITY_BOOTSTRAP
BOOTSTRAP_POLICY_SEMANTICS_UNCHANGED
BOOTSTRAP_POINTER_REVISION_1
LEGACY_TRAINER_STOP_REQUIRED_BEFORE_FIRST_MANAGED_BOOTSTRAP

IMMUTABLE_POLICY_ARTIFACT_STORE
SINGLE_ACTIVE_POLICY_POINTER
NO_IN_PLACE_POLICY_REWRITE
NO_DUAL_MANAGED_AND_DIRECT_POLICY_AUTHORITY

ACYCLIC_POINTER_COMMIT_DIGEST_GRAPH
POINTER_BINDS_ACTIVATION_INTENT
COMMIT_RECEIPT_BINDS_POINTER

MANAGED_TRAINER_AUTHORITY_LOCK
BARRIER_AND_TRAINER_MUTUALLY_EXCLUSIVE
BARRIER_DERIVED_FROM_ACTUAL_COMMITTED_STATE
ZERO_PENDING_PARTIAL_TMP_STAGING
12_REPLAY_HEAD_BP_BOUNDARY

BOUNDED_CHECKPOINT_AUTHORITY_WITNESS
NO_FULL_CHECKPOINT_PAYLOAD_TREE_HASH_CLAIM

PREPARE_DOES_NOT_ACTIVATE
IMMUTABLE_CANDIDATE_POLICY_ARTIFACT
DURABLE_ACTIVATION_INTENT

PREVIOUS_POINTER_EXACT_ARCHIVE
COMMITTED_POINTER_EXACT_ARCHIVE
TEMP_POINTER_STAGE
TEMP_POINTER_REREAD_VALIDATE
ATOMIC_ACTIVE_POINTER_REPLACE
ACTIVE_DIRECTORY_SYNC
NO_DELETE_THEN_CREATE_SWAP

MANAGED_RESTART_REQUIRES_EXACT_POLICY_BINDING
FIRST_ACTIVATION_TRANSITION_REQUIRES_EXACT_INTENT_AND_BARRIER
NO_ARBITRARY_LATEST_POINTER_RESTART

FIRST_PRODUCTION_GENERATION_IS_FIRST_GENERATION_AFTER_EFFECTIVE_BOUNDARY
N8_LAST_GENERATION_IS_NOT_MISTAKEN_FOR_FIRST
ALL_FIRST_GENERATION_PARAMETER_PLANS_USE_CANDIDATE_POLICY
MIXED_POLICY_PLAN_COUNT_ZERO

05_EXISTING_POLICY_CHANGE_REBASELINE_REUSED
NO_DUPLICATE_15_PLANNER_REBASELINE

ACTIVATION_CLOSURE_REQUIRES_FIRST_PHYSICAL_PRODUCTION_GENERATION
POINTER_SWAP_ALONE_IS_NOT_ACTIVATION_CLOSURE

PRE_FIRST_COMMIT_POINTER_ROLLBACK_SUPPORTED
PRE_FIRST_ROLLBACK_REQUIRES_EXACT_PRE_ACTIVATION_CHECKPOINT_AND_GENERATION
POLICY_ONLY_FORWARD_ROLLBACK_SUPPORTED_AFTER_ACTIVATION_CLOSED
POLICY_ONLY_ROLLBACK_PRESERVES_CANDIDATE_MODEL_HISTORY
CHECKPOINT_STATE_ROLLBACK_EXPLICITLY_UNAVAILABLE_R1
NO_FAKE_MODEL_STATE_RESTORE_CLAIM

ROLLBACK_RESTORES_EXACT_ARCHIVED_PREVIOUS_POINTER
NO_AUTOMATIC_POST_COMMIT_ROLLBACK

AUTHORIZED_POINTER_SWAP_IS_EXPLICIT_PRODUCTION_MUTATION
UNAUTHORIZED_POLICY_MUTATION_ZERO
MID_GENERATION_POLICY_MUTATION_ZERO
PRODUCTION_HOT_RELOAD_ZERO

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_TOPOLOGY
NO_NEW_MUON_MATHEMATICS
NO_NEW_FUSION_MUON_WGSL
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
36_GIB_RAM_AUTHORITY_UNCHANGED

STATIC_15_274_OF_274_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_RUST_AND_PRODUCTION_EXECUTION_UNVERIFIED

15_IS_EXPLICIT_PRODUCTION_ACTIVATION_AUTHORITY
```
