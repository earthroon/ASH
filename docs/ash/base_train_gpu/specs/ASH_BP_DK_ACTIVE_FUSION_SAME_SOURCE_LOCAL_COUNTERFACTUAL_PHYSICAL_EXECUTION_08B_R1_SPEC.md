# ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-PHYSICAL-EXECUTION-QUALIFICATION-08B-R1

## Status

```text
Patch ID:
ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-PHYSICAL-EXECUTION-QUALIFICATION-08B-R1

Direct parent:
ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-08B

Required upstream:
08A / 07 / 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00

Purpose:
turn the already-wired 08B Local counterfactual source path into an explicit user-local physical evidence surface

New Fusion policy: none
New Delta-K formula: none
New Muon mathematics: none
New WGSL: none
New gradient D2H authority: none
New counterfactual optimizer authority: none
Precision authority: unchanged
Residency authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

08B-R1 does not create another counterfactual algorithm. The authoritative algorithm remains 08B:

```text
same packed gradient lease
same source weight
same source momentum
same optimizer profile

actual 05 Fused candidate
vs
production Local(A) + Local(B) counterfactual
```

08B-R1 adds the physical witness and evidence publication boundary around that already-existing execution.

```text
08A qualification receipt
+ current WGPU device contract
+ actual 05 Fused candidate
+ actual 07 POST receipt
+ real 08B production-Local counterfactual dispatch
+ exact source/state pre/post seals
        -> capability-bound physical execution receipt
```

The state transition being closed is:

```text
08B_COUNTERFACTUAL_SOURCE_PATH_WIRED
STATIC_SOURCE_CONTRACT_CLOSED
COUNTERFACTUAL_PHYSICAL_EXECUTION_PENDING_USER_LOCAL_RUN

        -> user-local physical execution

COUNTERFACTUAL_PHYSICAL_EXECUTION_VERIFIED
```

Qualification-mode exact Local replay can further promote the observation to:

```text
COUNTERFACTUAL_PHYSICAL_EXECUTION_QUALIFIED
```

## Physical receipt is derived evidence, not optimizer state

The new JSON receipt is diagnostic/qualification evidence only.

It is not:

```text
checkpoint state
planner state
03B temporal state
07 actual ledger authority
active model authority
momentum authority
```

Generated physical receipts are written only when the explicit environment variable is configured:

```text
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_PHYSICAL_RECEIPT_ROOT
```

No counterfactual physical receipt sidecar is added to the BaseTrain checkpoint contract.

## 08A admission

The existing 08B mode authority remains:

```text
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=OBSERVE
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=QUALIFICATION
```

The existing qualification receipt path remains:

```text
ASH_BP_DK_ACTIVE_FUSION_08A_QUALIFICATION_RECEIPT_PATH
```

08B-R1 separately reloads and validates the same 08A physical receipt before evidence publication.

### Observe

`OBSERVE` accepts:

```text
NumericalQualified
ReplayQualified
TransactionQualified
RestartQualified
FullyQualified
```

### Qualification

`QUALIFICATION` requires:

```text
FullyQualified
```

There is no silent Qualification -> Observe downgrade.

## Current-device contract revalidation

08B-R1 does not merely copy the 08A capability digest into a new file.

Before the Local counterfactual executes, the current `BackendDevice` is checked against the admitted 08A receipt for all device information available from the production runtime:

```text
device feature bits
feature digest
compute/storage relevant limit digest
observed subgroup size
05 fused backend revision
05 fused kernel revision
serial fused WGSL digest
ExactSubgroup32 fused WGSL digest
```

The exact limit digest uses the same 08A fields:

```text
max_compute_workgroup_storage_size
max_compute_invocations_per_workgroup
max_compute_workgroup_size_x
max_compute_workgroups_per_dimension
max_storage_buffer_binding_size
max_buffer_size
observed_subgroup_size
```

The resulting current-device contract is itself digested into:

```text
device_contract_digest
```

The production runtime does not expose full adapter-name/vendor/driver metadata at this callsite, so 08B-R1 does not invent an adapter-level equality claim it cannot observe. A fresh 08A receipt generated on the intended user-local adapter remains the outer adapter identity authority.

## Actual candidate authority

The actual side remains the primary 05 candidate already produced by the authoritative execution plan.

08B-R1 does not execute a second Fused branch and call it Actual.

```text
Actual = 05 primary candidate
```

If 06 replay is active, its replay receipt remains additional deterministic evidence only.

## Physical Local counterfactual

The counterfactual path continues to use:

```text
TensorCubeLocalMuonBatchExecutor::execute_with_norm_path()
```

for only the canonical tiles belonging to actually fused domains.

No counterfactual-only WGSL, reduced Muon iteration path, CPU approximation, or fake Local oracle is introduced.

## Sparse batching and dispatch semantics

08B already batches the selected canonical Local tiles through one sparse Local batch description.

Therefore 08B-R1 deliberately does **not** assume:

```text
one Local tile == one GPU dispatch
```

For an actual fused pair there must be exactly two canonical Local counterfactual tiles, but those tiles may share one physical batch dispatch.

The hard physical invariants are:

```text
actual_fused_pair_count > 0
counterfactual_local_tile_count == 2 * actual_fused_pair_count
counterfactual_local_dispatch_count > 0
```

This preserves the existing production batch execution SSOT instead of manufacturing a dispatch-count invariant that the backend does not own.

## Physical execution ordering

The relevant production order is now explicitly observable as:

```text
05 actual candidate
-> 06 replay when requested
-> 07 actual POST receipt construction
-> 08B current-device contract check
-> 08B same-source production Local counterfactual
-> 08B actual-vs-Local receipt
-> 08B-R1 physical receipt seal/write
-> stage 07 actual parameter receipt
-> parent RAM momentum candidate adoption
```

Thus the physical receipt is generated before:

```text
self.momentum[...] = primary candidate momentum
```

and before 07 pending parameter state is staged.

## Exact source seals

08B-R1 captures exact F32-bit source digests before and after the counterfactual observation:

```text
source_weight_exact_digest_before
source_weight_exact_digest_after

source_momentum_exact_digest_before
source_momentum_exact_digest_after
```

Required:

```text
weight before == weight after
momentum before == momentum after
```

The existing 08B same-source capsule continues to bind the actual generation-bound gradient lease and optimizer profile.

## Planner-state seal

The existing 05 planner candidate snapshot is observed immediately before and after the Local what-if.

08B-R1 serializes those snapshots through deterministic JSON and SHA-256:

```text
planner_state_digest_before
planner_state_digest_after
```

Required:

```text
before == after
```

The counterfactual branch owns no fuse/fission/cooldown state transition.

## 03B temporal-state seal

Likewise:

```text
temporal_state_digest_before
==
temporal_state_digest_after
```

The Local what-if cannot advance Bridge EMA, Delta-K EMA, sample count, or temporal generation state.

## 07 actual ledger seal

08B-R1 captures the committed 07 ledger head before and after the counterfactual:

```text
committed_07_ledger_head_before
committed_07_ledger_head_after
```

Required:

```text
before == after
```

This distinguishes:

```text
07 = what actually happened
08B/08B-R1 = what Local would have produced from the same source
```

The counterfactual evidence cannot rewrite actual POST history.

## Physical receipt schema

`AshBpDkCounterfactualPhysicalExecutionReceipt` binds:

```text
08B-R1 patch/schema identity
physical qualification state
08A capability digest
08A qualification digest
current-device contract digest
current-device contract matched flag

optimizer generation
BP generation
08B source capsule digest
05 actual plan digest
07 actual POST receipt digest

actual fused pair count
Local counterfactual canonical tile count
Local counterfactual physical dispatch count

source weight exact digest before/after
source momentum exact digest before/after

05 planner snapshot digest before/after
03B temporal snapshot digest before/after
07 committed ledger head before/after

qualification replay observed
replay run count
replay mismatch count

counterfactual gradient D2H bytes
active weight write count
momentum commit count
planner mutation count
temporal state mutation count
benefit claim count
policy feedback count

full 08B parameter counterfactual receipt
physical execution digest
```

The nested 08B parameter receipt preserves the exact 256-D actual-vs-Local evidence already defined by 08B:

```text
weight effect RMS
momentum effect RMS
orthogonal-update effect RMS
actual-vs-Local direction cosines
magnitude ratios
actual-vs-Local pair coupling deltas
```

08B-R1 does not invent a second set of numerical formulas.

## Physical states

The new typed physical state surface includes:

```text
SourceContractReady
PhysicalObserveQualified
PhysicalQualificationQualified
UnsupportedCapability
InsufficientPhysicalEvidence
SourceMismatch
ReplayMismatch
StateMutationDetected
NonFiniteEvidence
StructuralContradiction
```

Successful runtime receipt construction currently emits only:

```text
OBSERVE       -> PhysicalObserveQualified
QUALIFICATION -> PhysicalQualificationQualified
```

Any violation fails before a successful receipt is sealed.

## Qualification replay

`QUALIFICATION` continues to execute the production Local counterfactual twice from the same source.

The parent 08B exact same-path rule remains authoritative:

```text
primary Local candidate weight digest
== replay Local candidate weight digest

primary Local candidate momentum digest
== replay Local candidate momentum digest

primary Local orthogonal-update digest
== replay Local orthogonal-update digest
```

08B-R1 requires:

```text
qualification_replay_observed = true
replay_run_count > 0
replay_mismatch_count = 0
```

No numerical tolerance is allowed for same-path replay.

## Hard-zero authority

Every successful physical receipt requires:

```text
counterfactual_gradient_d2h_bytes = 0
counterfactual_active_weight_write_count = 0
counterfactual_momentum_commit_count = 0
counterfactual_planner_mutation_count = 0
counterfactual_temporal_state_mutation_count = 0
counterfactual_benefit_claim_count = 0
counterfactual_policy_feedback_count = 0
replay_mismatch_count = 0
```

This is checked both by Rust receipt validation and by the user-local receipt validator.

## Physical evidence output

Generated files use:

```text
<receipt-root>/
  <08A-capability-digest>/
    generation-<optimizer-generation>/
      parameter-<canonical-index>-<physical-execution-digest>.json
```

Write semantics are diagnostic and collision-safe:

```text
create directory
write temporary JSON
rename into final evidence path
```

If the same path already exists with different bytes, execution fails rather than silently replacing evidence.

## User-local runner

08B-R1 adds:

```text
tools/run_ash_bp_dk_active_fusion_same_source_local_counterfactual_08b_r1.ps1
```

The runner expects the overlay to have already been applied by the user.

It performs no `Expand-Archive` or overlay discovery.

Required inputs:

```text
-QualificationReceiptPath <08A receipt>
-RunCommand <actual BaseTrain command that produces an active fused 08B observation>
```

Optional:

```text
-Mode OBSERVE | QUALIFICATION
-OutputRoot ...
-PythonExe ...
```

Runner sequence:

```text
validate 08A state admission
08B-R1 static validator
cargo fmt --check
cargo check base_train
clear current evidence output root
set 08B/08A/physical-evidence environment
execute user-provided physical training/qualification command
validate generated physical JSON receipts
require at least one receipt
```

The runner does not guess the user's training intake/model/checkpoint arguments. Those remain the existing BaseTrain runtime SSOT.

## Runtime receipt validation

The static validator also supports:

```text
--receipt-root <path>
--expected-mode OBSERVE|QUALIFICATION
```

For generated physical JSON it checks at minimum:

```text
patch/schema identity
mode/state correspondence
actual fused pair count
two canonical Local counterfactual tiles per pair
positive physical dispatch witness
current-device contract matched
source weight seal
source momentum seal
planner seal
temporal seal
07 committed ledger seal
all authority-leak counters zero
Qualification replay witness when requested
physical digest presence
```

The runtime itself validates and seals the SHA-256 receipt before writing; the Python layer is a user-local evidence sanity gate, not a second semantic hash authority.

## Parent source preservation

The following parent files remain byte-preserved in this bake:

```text
08B core
83c5705636159922adb8859026024fc6d0acfe1b15c09160daa76c8fcbb4ab39

08B base
e9f430d42fafcbf8ab047a361ec85d6f3556153bd79884e588afc15cb7437a2b

08A core
1748d0ade9c84fc7af8320b1e74a4e82ba11b0f5819a1219de3f9cc3054354d8

08A base
a32b28d4181bb70c6e31f6c1e53c29ad305a991b5d1c6c51c3d65515146df2c5

08A physical binary
5e679219cb68296fa24797e5a5cf830e74f6d9701b1cd996010fffe033ab722b

05 fused backend
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

05 serial fused WGSL
4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

05 ExactSubgroup32 fused WGSL
2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

The production callsite is extended only to capture/write the physical evidence wrapper around the already-existing 08B execution.

## Changed files

The 08B-R1 overlay contains exactly eight files:

```text
crates/ash_core/src/active_fusion_same_source_local_counterfactual_physical_execution.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_active_fusion_same_source_local_counterfactual_physical_execution.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_ash_bp_dk_active_fusion_same_source_local_counterfactual_08b_r1.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_physical_execution_08b_r1_static.py
```

No new WGSL, fused backend, planner core, 03B formula, 06 replay formula, 07 metric formula, or 08B counterfactual mathematics file is modified.

## Static validation

New gate:

```text
validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_physical_execution_08b_r1_static.py
146/146 PASS
```

Revalidated BP-DeltaK lineage:

```text
00 Observation Contract                         149/149 PASS
01 Local BP-DK                                  134/134 PASS
02 Generation/Revision/Stale Seal               243/243 PASS
03A Bridge Pair Evidence                        148/148 PASS
03B Bridge Temporal Coupling                    157/157 PASS
04 Fusion Candidate Graph                       235/235 PASS
05 Active Fusion/Fission Planner                293/293 PASS
06 Active Fusion Deterministic Replay           210/210 PASS
07 POST Update Effectiveness Ledger             206/206 PASS
08A Physical Qualification                      236/236 PASS
08B Same-Source Local Counterfactual            221/221 PASS
08B-R1 Counterfactual Physical Execution        146/146 PASS
```

Revalidated Local Muon lineage:

```text
Local Muon optimizer                            101/101 PASS
FirstCandidate registry                          97/97 PASS
Multi-tile batch                                 61/61 PASS
Production callsite                              63/63 PASS
Registry canonical-loader repair                 38/38 PASS
ExactSubgroup32 norm                            128/128 PASS
X PAD17                                          52/52 PASS
Generation-sealed immutable cache                66/66 PASS
Immutable-cache backend rebind                   35/35 PASS
```

08B-R1 is appended after the existing 08B validator in CF1 without changing the parent validator closure semantics.

## Bake environment boundary

The bake environment does not contain:

```text
cargo
rustc
rustfmt
physical WGPU adapter/runtime
```

Therefore this bake does **not** claim:

```text
Rust compile success
actual user-local FusedRight/Local physical counterfactual receipt
actual user-local FusedDown/Local physical counterfactual receipt
actual current-device contract runtime PASS
Qualification-mode Local replay runtime PASS
COUNTERFACTUAL_PHYSICAL_EXECUTION_VERIFIED
COUNTERFACTUAL_PHYSICAL_EXECUTION_QUALIFIED
```

Correct current status after baking is:

```text
08B_COUNTERFACTUAL_SOURCE_PATH_WIRED
STATIC_SOURCE_CONTRACT_CLOSED
08B_R1_PHYSICAL_EVIDENCE_WRITER_WIRED
08B_R1_USER_LOCAL_RUNNER_WIRED
COUNTERFACTUAL_PHYSICAL_EXECUTION_PENDING_USER_LOCAL_RUN
```

A user-local generated and validated physical receipt is required before changing that state.

## Packaging

Delivered code is split into:

```text
full-body bake
8-file overlay bake
```

Generated artifact/manifest/report directories, `target`, `__pycache__`, and `*.sha256` sidecars are excluded from the ZIPs.

Generated physical qualification JSON is intentionally not included in the bake because it must come from the user's actual hardware/run.

## Claim boundary after physical Observe verification

Once an `OBSERVE` physical receipt is produced and passes validation, this statement becomes supportable for that source/capability execution:

```text
The production Local counterfactual was physically executed from the same observed source state as the actual fused candidate, and the recorded 08B actual-vs-Local update divergence is physically witnessed.
```

Still forbidden:

```text
Fusion was better than Local.
Fusion reduced loss.
Fusion improves training quality.
Fusion thresholds are optimal.
```

## Claim boundary after Qualification verification

With:

```text
08A FullyQualified
08B mode = QUALIFICATION
counterfactual Local primary/replay exact
valid 08B-R1 physical receipt
```

the stronger state may be reported:

```text
COUNTERFACTUAL_PHYSICAL_EXECUTION_QUALIFIED
```

This still qualifies execution/reproducibility, not training benefit.

## Natural successor

After real 08B-R1 physical receipts exist, the next correctness revision is:

```text
ASH-BP-DK-ACTIVE-FUSION-COUNTERFACTUAL-EFFECT-LEDGER-09
```

09 can bind:

```text
07 committed actual POST history
+
08B/08B-R1 physically witnessed same-source Local counterfactual
```

into a generation-level causal update-difference ledger.

Only a later same-evaluation-batch objective probe should open benefit/loss claims.

## Bake seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_SAME_SOURCE_LOCAL_COUNTERFACTUAL_PHYSICAL_EXECUTION_08B_R1

08B_DIRECT_PARENT
08B_CORE_BYTE_PRESERVED
08B_BASE_MATH_BYTE_PRESERVED
08A_QUALIFICATION_SOURCE_BYTE_PRESERVED
05_FUSED_BACKEND_BYTE_PRESERVED
05_FUSED_WGSL_BYTE_PRESERVED

EXPLICIT_PHYSICAL_RECEIPT_ROOT
PHYSICAL_RECEIPT_IS_DERIVED_EVIDENCE_ONLY
NO_COUNTERFACTUAL_CHECKPOINT_AUTHORITY

08A_RECEIPT_IDENTITY_REVALIDATED
08A_RECEIPT_DIGEST_REVALIDATED
08A_AUTHORITY_SEALS_REVALIDATED

CURRENT_DEVICE_FEATURE_CONTRACT_REVALIDATED
CURRENT_DEVICE_LIMIT_CONTRACT_REVALIDATED
CURRENT_SUBGROUP_CONTRACT_REVALIDATED
CURRENT_KERNEL_AND_SHADER_CONTRACT_REVALIDATED

05_ACTUAL_FUSED_CANDIDATE_REMAINS_AUTHORITY
PRODUCTION_LOCAL_COUNTERFACTUAL_REUSED

SPARSE_FUSED_TILES_ONLY
TWO_CANONICAL_LOCAL_TILES_PER_FUSED_PAIR
POSITIVE_PHYSICAL_LOCAL_DISPATCH_WITNESS
NO_FALSE_ONE_TILE_ONE_DISPATCH_ASSUMPTION

SOURCE_WEIGHT_EXACT_PRE_POST_SEAL
SOURCE_MOMENTUM_EXACT_PRE_POST_SEAL
05_PLANNER_STATE_PRE_POST_SEAL
03B_TEMPORAL_STATE_PRE_POST_SEAL
07_COMMITTED_LEDGER_PRE_POST_SEAL

COUNTERFACTUAL_BEFORE_PARENT_RAM_MOMENTUM_ADOPTION
PHYSICAL_RECEIPT_BEFORE_07_PARAMETER_STAGING

OBSERVE_PHYSICAL_STATE_TYPED
QUALIFICATION_PHYSICAL_STATE_TYPED
QUALIFICATION_REQUIRES_08A_FULLY_QUALIFIED
QUALIFICATION_REPLAY_EXACT
NO_SILENT_MODE_DOWNGRADE

COUNTERFACTUAL_GRADIENT_D2H_ZERO
COUNTERFACTUAL_ACTIVE_WEIGHT_WRITE_ZERO
COUNTERFACTUAL_MOMENTUM_COMMIT_ZERO
COUNTERFACTUAL_PLANNER_MUTATION_ZERO
COUNTERFACTUAL_TEMPORAL_MUTATION_ZERO
COUNTERFACTUAL_BENEFIT_CLAIM_ZERO
COUNTERFACTUAL_POLICY_FEEDBACK_ZERO

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY
NO_NEW_MUON_MATHEMATICS
NO_NEW_WGSL
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_08B_R1_146_OF_146_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_PHYSICAL_EXECUTION_PENDING
```
