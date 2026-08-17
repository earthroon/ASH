# ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-08B

## Status

```text
Patch ID: ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-08B
Direct parent: ASH-BP-DK-ACTIVE-FUSION-PHYSICAL-QUALIFICATION-08A
Required upstream: 07 / 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: compare the authoritative actual fused candidate with a non-committing production-Local candidate from the exact same source state
New fusion policy: none
New Delta-K formula: none
New Muon mathematics: none
New WGSL: none
Gradient D2H authority: none
Precision authority: unchanged
Residency policy authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

08B introduces the first same-source Local counterfactual branch for an actually fused 05 domain.

```text
same generation-bound packed gradient lease
+ same source weight
+ same source momentum
+ same optimizer hyperparameters
+ same 05 actual fused execution plan
        |
        +-> authoritative actual Fused candidate from 05
        |
        +-> non-committing production Local(A) + Local(B) counterfactual
                    |
                    -> exact 256-D tile comparison
                    -> actual-vs-Local update-divergence receipt
```

08B answers:

```text
How did Fusion change the optimizer update relative to Local from the same source?
```

It does not answer:

```text
Was Fusion better?
Did Fusion reduce loss?
Did Fusion improve long-horizon training quality?
```

Those remain later objective/trajectory questions.

## 08A qualification admission

08B binds an explicit 08A physical qualification receipt through:

```text
ASH_BP_DK_ACTIVE_FUSION_08A_QUALIFICATION_RECEIPT_PATH
```

The receipt must match the 08A patch/schema, have a valid qualification digest, and preserve the 08A authority seals:

```text
production fused backend reused
production fused WGSL reused
no new Fusion policy
no new Delta-K formula
no new Muon mathematics
```

08B distinguishes two counterfactual modes:

```text
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=OBSERVE
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=QUALIFICATION
```

Default is `DISABLED`.

### Observe admission

`OBSERVE` requires an 08A state that has at least physical numerical qualification:

```text
NumericalQualified
ReplayQualified
TransactionQualified
RestartQualified
FullyQualified
```

This matches the current 08A harness boundary: the existing low-level physical harness can directly produce `NumericalQualified`, while full scheduler transaction/restart evidence is a stronger later witness.

### Qualification admission

`QUALIFICATION` requires exactly the strongest 08A state:

```text
FullyQualified
```

There is no silent downgrade from Qualification to Observe.

## Actual candidate authority

The actual side is not recomputed by 08B.

```text
Actual = primary 05 candidate already produced by the authoritative Fusion/Fission execution plan
```

When 06 replay is enabled, the actual candidate can additionally carry the existing replay verification identity. 08B does not reinterpret 06 replay as Local counterfactual evidence.

## Counterfactual target scope

R1 creates counterfactuals only for domains actually executed as:

```text
FusedRight
FusedDown
```

Plain Local domains are not re-run as Local-vs-Local controls, and 08B does not construct a reverse counterfactual fused path for an actual fissioned/Local domain.

This prevents a hidden N^2 or whole-parameter alternate optimizer branch.

## Production Local executor reuse

The counterfactual branch uses the existing production `TensorCubeLocalMuonBatchExecutor::execute_with_norm_path()`.

For every actual fused pair:

```text
actual FusedRight(A,B)
-> counterfactual Local(A) + Local(B)

actual FusedDown(A,B)
-> counterfactual Local(A) + Local(B)
```

No approximate Local kernel, CPU fake Local implementation, reduced Newton-Schulz iteration path, or counterfactual-only WGSL is introduced.

The Local counterfactual uses the same active norm-reduction path and the exact parent kernel profile.

## Sparse canonical counterfactual workspace

The runtime collects only the canonical tile ordinals belonging to actual fused domains.

```text
fused pair tiles
-> sort canonical tile ordinals
-> deduplicate
-> build Local batch descriptors
-> gather only those source weight/momentum 16x16 tiles
-> execute production Local Muon
-> compare
-> release derived candidate evidence
```

The counterfactual workspace is therefore sparse over actual fused tiles rather than a second whole-model candidate slab.

This preserves the existing 36-GiB parent RAM authority and introduces no second whole-model momentum authority.

## Exact same-source binding

The same source is enforced operationally by passing the same references to both branches:

```text
same RawWgpuBufferLease packed gradient
same source_weight_packed slice
same source_momentum snapshot
same optimizer_step
same kernel profile
same norm reduction path
```

The counterfactual source capsule additionally binds:

```text
05 plan digest
source-weight digest
exact source-momentum F32 digest
packed-gradient lease label
raw-handle seam identity
vendor access path
primitive/stream identity when available
lease element/byte cardinality
offset/size
learning rate
momentum beta
weight decay
Newton-Schulz a/b/c/epsilon/steps
Nesterov flag
working dtype
```

No buffer pointer or allocator address is used as semantic identity.

The packed gradient is not read back merely to create a host digest. Exact branch identity is provided by consuming the same generation-bound lease in the same runtime operation.

## Source mutation guard

Before counterfactual execution the exact source-momentum digest is sealed.

The digest is checked after the primary counterfactual and again after counterfactual replay in Qualification mode.

Any drift is:

```text
ASH_BP_DK_COUNTERFACTUAL_SOURCE_STATE_CHANGED
```

or

```text
ASH_BP_DK_COUNTERFACTUAL_SOURCE_STATE_CHANGED_AFTER_REPLAY
```

and rejects the requested observation path.

## Planner and 03B state immutability

Immediately before Local counterfactual execution, 08B snapshots:

```text
05 planner candidate state
03B Bridge temporal candidate state
```

After the counterfactual branch, both snapshots must be exactly unchanged.

Failure surfaces:

```text
ASH_BP_DK_COUNTERFACTUAL_PLANNER_STATE_MUTATION
ASH_BP_DK_COUNTERFACTUAL_TEMPORAL_STATE_MUTATION
```

The counterfactual branch therefore has no fuse-streak, fission-streak, cooldown, Bridge EMA, or Delta-K temporal-state authority.

## Ordering relative to 06, 07 and parent momentum

The production order is:

```text
05 actual Local/Fused candidate
-> 06 replay verification when requested
-> 07 actual POST receipt construction
-> 08B same-source Local counterfactual
-> 08B receipt
-> stage 07 actual ledger parameter receipt
-> parent run-local RAM momentum candidate adoption
```

07 actual POST evidence therefore exists before 08B comparison, while its pending ledger state is not staged until the requested 08B observation has succeeded.

This avoids ghost 07 pending history if an explicitly requested counterfactual observation fails.

Most importantly:

```text
08B executes before self.momentum[...] receives the primary candidate momentum.
```

The Local what-if never observes a post-candidate momentum source.

## Actual POST and replay identity binding

Each 08B parameter receipt binds:

```text
07 actual POST parameter receipt digest
optional 06 actual replay receipt digest
```

The 07 digest indirectly seals the actual PRE-to-POST chain, including current graph/plan identity and the PRE Bridge evidence carried by the 07 pair receipts.

08B does not duplicate or fabricate missing PRE values.

## Canonical tile comparison

For each fused canonical 16x16 tile T, all 256 dimensions are used.

Actual weight update:

```text
DeltaW_actual = W_actual_candidate - W_source
```

Counterfactual Local weight update:

```text
DeltaW_local = W_local_candidate - W_source
```

Fusion-induced difference:

```text
E_W = DeltaW_actual - DeltaW_local
```

The same construction applies to momentum:

```text
DeltaM_actual
DeltaM_local
E_M
```

and the physical Muon orthogonal update:

```text
E_U = U_actual_fused - U_local_counterfactual
```

## Tile metrics

Each fused tile records:

```text
actual weight-delta RMS
Local weight-delta RMS
Fusion-effect weight RMS

actual momentum-delta RMS
Local momentum-delta RMS
Fusion-effect momentum RMS

actual orthogonal-update RMS
Local orthogonal-update RMS
Fusion-effect orthogonal RMS
```

No sketch, sampled rows, compressed direction vector, or scalar Fusion score replaces the exact 256-D vectors.

## Direction comparison

08B observes exact-vector cosine relationships:

```text
cos(DeltaW_actual, DeltaW_local)
cos(DeltaM_actual, DeltaM_local)
cos(U_actual, U_local)
```

Signs are preserved. There is no `abs()` conversion.

A zero-norm side remains explicit `UndefinedZeroNorm`; it is not rewritten as cosine zero.

## Magnitude ratios

08B can report:

```text
RMS(actual) / RMS(Local)
```

for weight delta, momentum delta and orthogonal update.

A zero Local baseline is represented as:

```text
UndefinedZeroBaseline
```

There is no epsilon denominator repair.

## Pair coupling change

For each actual fused pair A/B, 08B compares the pair relationship itself:

```text
actual pair weight-delta cosine
vs
Local counterfactual pair weight-delta cosine

actual pair momentum-delta cosine
vs
Local counterfactual pair momentum-delta cosine

actual pair orthogonal-update cosine
vs
Local counterfactual pair orthogonal-update cosine
```

When both cosines are defined, the receipt stores signed coupling delta:

```text
actual cosine - Local cosine
```

This is descriptive causal-update evidence, not a benefit score.

## Exact counterfactual replay

In `QUALIFICATION` mode the same selected Local counterfactual is executed twice from the same source.

Exact SHA-256 equality is required for F32-bit serialized:

```text
counterfactual candidate weight
counterfactual candidate momentum
counterfactual orthogonal update
```

A mismatch is:

```text
ASH_BP_DK_COUNTERFACTUAL_LOCAL_REPLAY_MISMATCH
```

There is no tolerance-based same-path replay repair.

## Counterfactual receipt

`AshBpDkSameSourceLocalCounterfactualParameterReceipt` binds:

```text
mode
parameter identity/revision/generation
source capsule digest
08A qualification state/capability/qualification digest
04 graph topology/evidence identity
05 execution-plan digest
05 planner-policy digest
07 actual POST receipt digest
optional 06 replay receipt digest
actual candidate weight/momentum/update exact digests
sparse Local candidate weight/momentum/update exact digests
counterfactual gradient D2H bytes
ordered actual fused-pair evidence
receipt digest
```

The receipt digest uses explicit F32 `to_bits().to_le_bytes()` hashing for the numerical evidence, explicit presence tags for optional F32 values, typed domain/status tags, and canonical pair order.

## Derived evidence lifetime

08B receipts are current-generation derived evidence only.

They are cleared when the current BP/Fusion generation advances.

There is deliberately no:

```text
counterfactual optimizer state
counterfactual planner state
counterfactual temporal state
counterfactual checkpoint authority
counterfactual active-model commit
counterfactual momentum commit
```

No `persist_counterfactual` or counterfactual state sidecar is introduced.

## Gradient D2H boundary

The selected Local counterfactual consumes the existing generation-bound packed gradient lease directly on GPU.

Required:

```text
counterfactual_gradient_d2h_bytes = 0
```

Candidate output readback follows the existing Local Muon candidate path and is allowed for derived comparison evidence.

## Telemetry

08B adds:

```text
counterfactual_run_count
counterfactual_pair_count
counterfactual_tile_count
counterfactual_fused_right_pair_count
counterfactual_fused_down_pair_count
counterfactual_local_dispatch_count
counterfactual_source_mismatch_count
counterfactual_nonfinite_count
counterfactual_zero_baseline_count
counterfactual_replay_run_count
counterfactual_replay_mismatch_count
counterfactual_gradient_d2h_bytes
counterfactual_active_weight_write_count
counterfactual_momentum_commit_count
counterfactual_planner_mutation_count
counterfactual_temporal_state_mutation_count
counterfactual_benefit_claim_count
counterfactual_policy_feedback_count
```

Hard-zero authority:

```text
counterfactual_gradient_d2h_bytes = 0
counterfactual_active_weight_write_count = 0
counterfactual_momentum_commit_count = 0
counterfactual_planner_mutation_count = 0
counterfactual_temporal_state_mutation_count = 0
counterfactual_benefit_claim_count = 0
counterfactual_policy_feedback_count = 0
```

## Failure semantics

If `OBSERVE` or `QUALIFICATION` is explicitly requested and the counterfactual branch cannot satisfy its contract, the current optimizer generation is rejected through the existing fail-stop line.

Pending 03B, 05 and 07 runtime state is aborted where applicable.

The runtime must not:

```text
silently disable the counterfactual
replace the counterfactual with a different Local kernel
reuse the actual fused candidate as the Local result
change the 05 decision
rewrite planner policy
commit the Local what-if
```

`DISABLED` leaves the existing 05/06/07 execution path unchanged.

## Parent source preservation

08B does not modify:

```text
08A physical qualification core/base/binary
06 replay core/base
07 POST ledger core/base
05 planner core/base
05 fused backend
05 serial fused WGSL
05 ExactSubgroup32 fused WGSL
```

Parent SHA anchors preserved in the 08B source tree include:

```text
08A core
1748d0ade9c84fc7af8320b1e74a4e82ba11b0f5819a1219de3f9cc3054354d8

08A base
a32b28d4181bb70c6e31f6c1e53c29ad305a991b5d1c6c51c3d65515146df2c5

08A physical binary
5e679219cb68296fa24797e5a5cf830e74f6d9701b1cd996010fffe033ab722b

06 replay core
4c92c48e5e5552837218471e2a441f706ebf3151a8d90badf73516ce09f6bbdb

06 replay base
6ed468023ae7756e55d45e7fa25e0a74b2e46105a1af347be25fcbbef65f55a5

07 POST core
1683c07483f6fab106cb22cd63019cdf2a0d5a3f36389756ae4b51fbf4e78f59

07 POST base
3597593ac60c29813a477a28c037486acccc933aa20f8335e3af177aeae7bfc7

05 planner core
53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

05 planner base
70e6d4f08e89d4693c1999ff4508ec09ad4fcfe9850e2bb914127702f5f618cc

fused backend
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

serial fused WGSL
4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

ExactSubgroup32 fused WGSL
2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

## Changed files

The 08B overlay contains exactly seven files:

```text
crates/ash_core/src/active_fusion_same_source_local_counterfactual.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_active_fusion_same_source_local_counterfactual.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_08b_static.py
```

No new WGSL or backend file is introduced.

## Static validation

New gate:

```text
validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_08b_static.py
221/221 PASS
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
Immutable-cache backend surface rebind           35/35 PASS
```

08B is appended to CF1 after 05, 06, 07 and 08A without rewriting the parent AllValidators closure.

## Bake-environment boundary

The bake environment does not provide `cargo`, `rustc`, `rustfmt`, or a physical WGPU adapter.

Therefore this bake does not claim:

```text
Rust compile success
actual counterfactual Local dispatch success
actual Fused-vs-Local physical divergence evidence
08B Qualification-mode replay success
training benefit
loss improvement
```

Current status is:

```text
08B_COUNTERFACTUAL_SOURCE_PATH_WIRED
08B_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_05_06_07_08A_PHYSICAL_SOURCES_PRESERVED
COUNTERFACTUAL_PHYSICAL_EXECUTION_PENDING_USER_LOCAL_RUN
```

## Required physical gates

For `OBSERVE`:

```text
08A NumericalQualified-or-stronger receipt admitted
actual fused domain exists
same packed gradient lease reused
same source weight/momentum reused
production Local counterfactual physically executes
no source-momentum drift
no 05 planner-state drift
no 03B temporal-state drift
zero gradient D2H
08B receipt seals
```

For `QUALIFICATION` additionally:

```text
08A FullyQualified receipt admitted
counterfactual Local primary/replay exact candidate-weight digest
counterfactual Local primary/replay exact candidate-momentum digest
counterfactual Local primary/replay exact orthogonal-update digest
```

## Claim boundary after 08B

Once physical 08B evidence exists, the permitted statement becomes:

```text
From this exact source state, the actual fused execution changed the optimizer update relative to production Local by the measured vector/magnitude/direction amounts.
```

Still forbidden:

```text
Fusion was better than Local.
Fusion improved the objective.
Fusion improves long-horizon training.
```

## Natural successor

The next correctness revision is:

```text
ASH-BP-DK-ACTIVE-FUSION-COUNTERFACTUAL-EFFECT-LEDGER-09
```

09 should bind the committed 07 actual POST ledger with the derived 08B same-source Local counterfactual evidence into a generation-level causal update-difference ledger, still without making a loss/benefit claim.

The later objective probe can then evaluate actual fused and counterfactual Local candidate models on the same evaluation microbatch.

## Bake seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_SAME_SOURCE_LOCAL_COUNTERFACTUAL_08B

08A_DIRECT_PARENT
08A_QUALIFICATION_RECEIPT_BOUND
OBSERVE_REQUIRES_NUMERICAL_QUALIFICATION_OR_STRONGER
QUALIFICATION_REQUIRES_FULLY_QUALIFIED
NO_SILENT_MODE_DOWNGRADE

05_ACTUAL_FUSED_CANDIDATE_PRESERVED
PRODUCTION_LOCAL_MUON_REUSED
NO_COUNTERFACTUAL_SPECIFIC_WGSL

ACTUAL_FUSED_DOMAINS_ONLY
NO_PLAIN_LOCAL_COUNTERFACTUAL_REEXECUTION
NO_REVERSE_FISSION_TO_FUSED_COUNTERFACTUAL

SAME_PACKED_GRADIENT_LEASE
SAME_SOURCE_WEIGHT
SAME_SOURCE_MOMENTUM
SAME_OPTIMIZER_STEP
SAME_KERNEL_PROFILE
SAME_NORM_PATH

COUNTERFACTUAL_BEFORE_PARENT_RAM_MOMENTUM_ADOPTION
SOURCE_MOMENTUM_DIGEST_RECHECKED
05_PLANNER_STATE_UNCHANGED
03B_TEMPORAL_STATE_UNCHANGED

EXACT_256D_WEIGHT_UPDATE_DIFFERENCE
EXACT_256D_MOMENTUM_UPDATE_DIFFERENCE
EXACT_256D_ORTHOGONAL_UPDATE_DIFFERENCE

FUSION_EFFECT_WEIGHT_RMS
FUSION_EFFECT_MOMENTUM_RMS
FUSION_EFFECT_ORTHOGONAL_RMS

ACTUAL_VS_LOCAL_WEIGHT_DIRECTION_COSINE
ACTUAL_VS_LOCAL_MOMENTUM_DIRECTION_COSINE
ACTUAL_VS_LOCAL_ORTHOGONAL_DIRECTION_COSINE

ACTUAL_PAIR_VS_LOCAL_PAIR_COUPLING_DELTA
SIGNED_RELATIONSHIP_PRESERVED
ZERO_BASELINE_IS_EXPLICIT
NO_EPSILON_DENOMINATOR_REPAIR

07_ACTUAL_POST_RECEIPT_DIGEST_BOUND
06_REPLAY_RECEIPT_IDENTITY_BINDABLE

COUNTERFACTUAL_CANDIDATE_NONCOMMITTING
NO_COUNTERFACTUAL_PLANNER_STATE
NO_COUNTERFACTUAL_03B_STATE
NO_COUNTERFACTUAL_CHECKPOINT_AUTHORITY
NO_COUNTERFACTUAL_ACTIVE_WEIGHT_WRITE
NO_COUNTERFACTUAL_MOMENTUM_COMMIT

NO_COUNTERFACTUAL_GRADIENT_D2H
NO_POLICY_FEEDBACK
NO_FUSION_BENEFIT_CLAIM
NO_LOSS_IMPROVEMENT_CLAIM

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY
NO_NEW_MUON_MATHEMATICS
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_08B_221_OF_221_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_COUNTERFACTUAL_EXECUTION_UNVERIFIED_IN_BAKE_ENVIRONMENT
```
