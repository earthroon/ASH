# ASH-BP-DK-ACTIVE-FUSION-DETERMINISTIC-REPLAY-06

## Status

```text
Patch ID: ASH-BP-DK-ACTIVE-FUSION-DETERMINISTIC-REPLAY-06
Direct parent: ASH-BP-DK-FUSION-FISSION-PLANNER-05
Required upstream: 04 / 03B / 03A / 02 / 01 / 00
Purpose: deterministic replay closure for the already-active Local/Fused optimizer path
New fusion policy: none
New Delta-K formula: none
New WGPU kernel: none
Replay durable state authority: none
Precision authority: unchanged
Residency policy authority: unchanged
```

## Central SSOT

06 does not change which fusion decision is correct and does not change Muon mathematics. It verifies that the already-authoritative 05 path is reproducible from the same semantic source state.

```text
same source weight identity
+ same exact source momentum
+ same current 04 graph identity/evidence
+ same current 03B temporal candidate-state image
+ same committed 05 planner-state identity
+ same planner policy
+ same fused execution capability/backend/kernel identity
        -> same execution plan
        -> same Local/Fused domain assignment
        -> same candidate weight
        -> same candidate momentum
        -> same orthogonal update
```

Logical plan replay and physical candidate replay are separate gates.

## Replay modes

The runtime exposes an explicit verification mode:

```text
ASH_BP_DK_ACTIVE_FUSION_REPLAY_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_REPLAY_MODE=PLAN_ONLY
ASH_BP_DK_ACTIVE_FUSION_REPLAY_MODE=CANDIDATE_DIGEST
```

Absent environment configuration means `DISABLED`.

There is no silent mode downgrade. If `CANDIDATE_DIGEST` is requested and duplicate candidate execution cannot complete, the optimizer generation fails rather than quietly degrading to `PLAN_ONLY`.

`DISABLED` remains the normal zero-extra-compute control path.

## Canonical replay capsule

`AshActiveFusionReplayCapsule` binds:

```text
parameter_id
canonical_parameter_index
parameter_revision
optimizer_generation
bp_generation

source_weight_digest
source_momentum_digest

graph_topology_digest
graph_evidence_digest

bridge_temporal_state_digest
planner_state_digest
planner_policy_digest

capability_digest
backend_revision
fused_kernel_revision
norm_reduction_path
```

The capsule itself has a deterministic canonical SHA-256 digest.

### Source weight identity

06 reuses the exact source weight digest already carried by the 05/production lineage. It does not invent a pointer-identity or buffer-address authority.

### Source momentum identity

Source momentum is digested from canonical packed F32 values using exact `to_bits().to_le_bytes()` serialization. Same model weights with different optimizer momentum are therefore not considered the same replay source.

## Current 03B temporal state binding

The 06 callsite constructs a deterministic digest from `bp_dk_bridge_temporal.candidate_snapshot_states()` at the current PRE-optimizer generation. This intentionally includes the current generation's 03B pending candidate-state image because the current 04 graph and 05 plan are derived from those same current temporal observations.

The digest sorts typed pair keys and binds exact F32 bits for:

```text
ema_cosine
delta_k_ema
sample count
last parameter / optimizer / BP generation
source-weight identity
pair-evidence / source / observer / policy / topology revisions and digests
registry / optimizer-routing / local-observer policy identity
```

This current temporal image is verification input only. 06 creates no new temporal authority and no replay checkpoint sidecar.

## 05 planner-state binding

The execution plan already binds `committed_planner_state_digest`; 06 carries that exact digest into the replay capsule.

The real 05 planner runtime is cloned immediately before the primary `plan_parameter(...)` call when replay is enabled.

```text
primary planner runtime
    -> authoritative pending planner state

pre-call clone
    -> replay-only planner computation
    -> discarded after verification
```

The replay clone cannot advance or overwrite the production planner's pending/committed state.

## Exact plan replay

After the primary 05 planner creates its execution plan, the isolated planner clone receives the exact same:

```text
04 graph
full tile count
Fusion execution capability
planner configuration
pre-primary planner runtime snapshot
```

The resulting `AshBpDkFusionExecutionPlan` must be exactly equal to the primary plan.

Plan identity is discrete. There is no epsilon or approximate-plan comparison.

```text
same plan digest + different plan structure
-> StructuralContradiction

different plan digest / different plan
-> PlanMismatch
```

Any replay plan mismatch aborts the current pending 03B and 05 state and rejects the optimizer generation.

## Plan-only replay receipt

`PLAN_ONLY` emits a current-generation `AshActiveFusionReplayReceipt` containing:

```text
source capsule digest
primary plan digest
replay plan digest
Verified status
```

It contains no candidate-output digest fields and performs no duplicate physical Muon candidate execution.

Replay receipts are current-generation diagnostic/verification projections only. They are cleared on BP-generation advance and are not persisted as optimizer state.

## Candidate replay ordering

`CANDIDATE_DIGEST` is wired before the parent RAM momentum copy.

Production order:

```text
seal current replay source capsule

primary 05 plan
replay-clone plan
exact plan comparison

primary Local/Fused candidate computation

recheck source momentum digest
recheck plan digest

replay Local/Fused candidate computation

exact candidate digest comparison

only after replay verification:
    parent ProductionMuonRuntime momentum candidate adoption
```

This ordering prevents replay from using the already-mutated run-local RAM momentum candidate.

## Candidate replay physical path

The replay candidate uses the same `execute_fusion_execution_plan_candidate_internal(...)` implementation and the same:

```text
generation-bound packed gradient lease
source weight slice
source momentum slice
kernel profile
norm reduction path
Local/Fused execution plan
```

The primary wrapper calls the internal executor with production fused-counter recording enabled. The replay wrapper calls the same internal executor with those production fused counters disabled, so one verification duplicate does not masquerade as two production fusion decisions.

No new backend module and no new WGSL are introduced by 06.

## Parent 05 physical kernels preserved

The following 05 files are byte-preserved by the 06 bake:

```text
crates/ash_core/src/bp_dk_fusion_fission_planner.rs
SHA256 53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

crates/base_train/src/bp_delta_k_fusion_fission_planner.rs
SHA256 70e6d4f08e89d4693c1999ff4508ec09ad4fcfe9850e2bb914127702f5f618cc

crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
SHA256 cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_fused_pair_muon_16x32.wgsl
SHA256 4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
SHA256 2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

06 therefore tests the existing 05 physical implementation rather than changing the implementation under test.

## Exact candidate digests

Candidate replay compares exact F32-bit digests for:

```text
whole-parameter candidate weight
whole-parameter candidate momentum
whole-parameter orthogonal update
```

It also produces per-domain digests for every canonical 05 domain:

```text
Local
FusedRight
FusedDown
```

Domain digests are built from the canonical tile membership of each execution domain and exact `f32::to_bits()` values.

No numerical epsilon is applied to same-path replay.

## Replay receipt

`AshActiveFusionReplayReceipt` can contain:

```text
replay mode
source capsule digest
primary / replay plan digest
primary / replay candidate weight digest
primary / replay candidate momentum digest
primary / replay orthogonal-update digest
per-domain candidate output receipts
status
```

Only `Verified` receipts are retained by the successful current-generation production runtime.

A mismatch rejects the generation and is not converted into a last-good receipt.

## Mismatch and failure semantics

Explicit failure surfaces include:

```text
ASH_BP_DK_ACTIVE_FUSION_REPLAY_PLAN_MISMATCH
ASH_BP_DK_ACTIVE_FUSION_REPLAY_PLAN_STRUCTURAL_CONTRADICTION
ACTIVE_FUSION_REPLAY_SOURCE_STATE_CHANGED
ACTIVE_FUSION_REPLAY_CANDIDATE_WEIGHT_MISMATCH
ACTIVE_FUSION_REPLAY_CANDIDATE_MOMENTUM_MISMATCH
ACTIVE_FUSION_REPLAY_ORTHOGONAL_UPDATE_MISMATCH
ACTIVE_FUSION_REPLAY_DOMAIN_OUTPUT_MISMATCH
```

On replay mismatch/error, pending 03B temporal state and pending 05 planner state are aborted for the optimizer generation before the error propagates.

No replay mismatch can trigger:

```text
Local fallback
second-best pair selection
runtime replanning
epsilon widening
warning-only commit
```

## Source mutation boundary

The replay verifier does not write:

```text
active model weights
committed 05 planner state
committed 03B temporal state
canonical durable checkpoint state
```

`CANDIDATE_DIGEST` uses candidate scratch produced by the existing Local/Fused executors.

The parent 05 RAM-momentum caveat remains unchanged: after successful replay verification, the production runtime may copy the primary candidate momentum into its existing fail-stop run-local RAM candidate slab before final durable model commit. 06 does not introduce a second whole-model momentum slab.

## Derived cache effect boundary

Candidate replay intentionally calls the same physical executor a second time. The existing immutable/pipeline cache may therefore become warmer during verification mode. That cache is derived execution state, not model/optimizer semantic authority.

Consequently 06 makes no performance comparison or residency-efficiency claim from replay runs. Timing, cache-hit count, and queue churn observed under `CANDIDATE_DIGEST` are verification overhead and must not be used as production throughput evidence.

## No full-gradient D2H

06 reuses the exact same generation-bound packed gradient lease already consumed by the 05 path. It introduces no gradient readback API, no host gradient reconstruction, and no new GPU gradient reduction.

The replay duplicate can repeat existing candidate-output readback because the parent 05 execution path already materializes candidate weight/momentum/update products. This does not create full-gradient D2H authority.

## Replay telemetry

Production counters include:

```text
active_fusion_replay_run_count
active_fusion_plan_replay_count
active_fusion_plan_replay_mismatch_count
active_fusion_candidate_replay_count
active_fusion_weight_digest_mismatch_count
active_fusion_momentum_digest_mismatch_count
active_fusion_domain_mismatch_count
active_fusion_source_state_changed_count
active_fusion_unverifiable_count
active_fusion_structural_contradiction_count
active_fusion_replay_fallback_count
active_fusion_replay_runtime_replan_count
active_fusion_replay_local_domain_count
active_fusion_replay_fused_right_domain_count
active_fusion_replay_fused_down_domain_count
```

Successful authority closure requires:

```text
active_fusion_replay_fallback_count = 0
active_fusion_replay_runtime_replan_count = 0
```

Mismatch counters are fail-path telemetry; a successful final production receipt cannot be produced after the corresponding replay mismatch rejects the optimizer generation.

## Current-generation lifetime

Replay receipts are cleared when the current BP/Bridge generation advances together with the current 03A/03B/04/05 projection surfaces.

There is deliberately no:

```text
active_fusion_replay_state_manifest.json
active_fusion_replay_state.json
persist_active_fusion_replay
last-good replay authority
```

The replay proof is derived from the existing durable source state after restart rather than becoming another state machine that must itself be restored.

## Checkpoint/restart closure target

06 source wiring provides the digests and deterministic plan/candidate surfaces required to compare:

```text
uninterrupted run from committed generation N
vs
restart from the same committed generation N
```

Required physical comparison at N+1:

```text
same 03B current temporal evidence/state image
same 04 topology digest
same 04 evidence digest
same 05 committed planner-state digest
same 05 plan digest
same Local/Fused domain assignment
same candidate weight digest
same candidate momentum digest
same orthogonal-update digest
```

The bake environment cannot execute that physical restart harness, so checkpoint/restart parity remains a required user-local physical gate rather than a claimed result.

## Serial / ExactSubgroup32 boundary

06 same-path replay compares one physical path against itself:

```text
SerialLane0 -> SerialLane0
ExactSubgroup32 -> ExactSubgroup32
```

The capsule binds `norm_reduction_path`, backend revision, kernel revision, and capability digest.

Serial-vs-ExactSubgroup32 equivalence remains a separate numerical-oracle gate. 06 does not assume cross-kernel bitwise identity.

## Changed files

The 06 overlay contains exactly seven changed/new files:

```text
crates/ash_core/src/active_fusion_deterministic_replay.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_active_fusion_deterministic_replay.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_deterministic_replay_06_static.py
```

No 05 planner core/base implementation, fused backend, or fused WGSL file is modified.

## Static validation

New 06 gate:

```text
validate_ash_bp_dk_active_fusion_deterministic_replay_06_static.py
210/210 PASS
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
```

Revalidated Local Muon lineage:

```text
Local Muon optimizer                            101/101 PASS
FirstCandidate registry                          97/97 PASS
Multi-tile batch                                 61/61 PASS
Production callsite                              63/63 PASS
Registry canonical loader repair                 38/38 PASS
ExactSubgroup32 norm                            128/128 PASS
X PAD17                                          52/52 PASS
Generation-sealed immutable cache                66/66 PASS
Immutable-cache backend rebind                   35/35 PASS
```

06 is appended after the parent-preserving 05 validator append in the CF1 chain.

## Physical execution boundary

The bake environment does not provide `cargo`, `rustc`, `rustfmt`, a WGSL validator, or a physical WGPU device/runtime.

Therefore this bake does **not** claim:

```text
Rust compile success
physical plan replay execution success
FusedRight candidate replay parity
FusedDown candidate replay parity
checkpoint/restart physical parity
Serial/Subgroup cross-path numerical parity
training throughput behavior under replay
```

Correct current status:

```text
REPLAY_SOURCE_PATH_WIRED
STATIC_SOURCE_CONTRACT_CLOSED
PARENT_05_KERNELS_BYTE_PRESERVED
PHYSICAL_REPLAY_EXECUTION_UNVERIFIED
```

## Required user-local physical gates

```text
cargo fmt / cargo check
CF1 compile chain reaches 06

PLAN_ONLY exact plan replay
CANDIDATE_DIGEST Local exact candidate replay
CANDIDATE_DIGEST FusedRight exact candidate replay
CANDIDATE_DIGEST FusedDown exact candidate replay
mixed Local/Fused domain replay
fusion transition replay
fission transition replay
cooldown transition replay

replay occurs before parent momentum adoption
no full-gradient D2H
mismatch rejects generation
no Local fallback / no runtime replan

checkpoint restart vs uninterrupted plan parity
checkpoint restart vs uninterrupted candidate parity
```

## Packaging

The delivered bake is split into full-body and seven-file overlay ZIPs. Generated artifact/manifest/report directories and `*.sha256` sidecars are excluded from both ZIPs.

## Non-goals

```text
No new fusion threshold
No new fusion score
No planner matching change
No new Delta-K equation
No cross-parameter fusion
No larger fusion domain
No new Muon coefficients
No new fused WGSL
No replay persistent state
No silent replay downgrade
No Local fallback after replay mismatch
No runtime plan repair
No precision decision
No residency-policy decision
No performance promotion
```

## Natural successor

After user-local physical 06 replay gates pass, the correctness line proceeds to:

```text
ASH-BP-DK-ACTIVE-FUSION-POST-UPDATE-EFFECTIVENESS-LEDGER-07
```

07 can join:

```text
PRE local BP-DeltaK
PRE Bridge DeltaK
04 graph evidence
05 actual Local/Fused/Fission decision
06 replay-sealed execution identity
actual source -> candidate DeltaW
```

into a POST effectiveness ledger without changing the 05 planner policy yet.

## Promotion seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_DETERMINISTIC_REPLAY_06

05_ACTIVE_FUSION_AUTHORITY_PRESERVED
05_FUSED_BACKEND_BYTE_PRESERVED
05_FUSED_WGSL_BYTE_PRESERVED

EXPLICIT_REPLAY_MODE
NO_SILENT_REPLAY_DOWNGRADE

CANONICAL_REPLAY_CAPSULE
SOURCE_WEIGHT_DIGEST_BOUND
SOURCE_MOMENTUM_EXACT_F32_DIGEST_BOUND
04_GRAPH_TOPOLOGY_DIGEST_BOUND
04_GRAPH_EVIDENCE_DIGEST_BOUND
03B_CURRENT_TEMPORAL_STATE_IMAGE_BOUND
05_COMMITTED_PLANNER_STATE_DIGEST_BOUND
PLANNER_POLICY_DIGEST_BOUND
CAPABILITY_BACKEND_KERNEL_IDENTITY_BOUND

PLANNER_CLONE_ISOLATED_FROM_PRIMARY_STATE
EXACT_PLAN_REPLAY
NO_PLAN_EPSILON

PRIMARY_CANDIDATE_BEFORE_REPLAY_CANDIDATE
REPLAY_BEFORE_PARENT_RAM_MOMENTUM_ADOPTION

LOCAL_CANDIDATE_EXACT_DIGEST
FUSEDRIGHT_CANDIDATE_EXACT_DIGEST
FUSEDDOWN_CANDIDATE_EXACT_DIGEST
CANDIDATE_WEIGHT_EXACT_F32_DIGEST
CANDIDATE_MOMENTUM_EXACT_F32_DIGEST
ORTHOGONAL_UPDATE_EXACT_F32_DIGEST
PER_DOMAIN_OUTPUT_DIGEST

NO_REPLAY_ACTIVE_STATE_COMMIT
NO_REPLAY_DURABLE_STATE
NO_LAST_GOOD_REPLAY

REPLAY_MISMATCH_FAILS_CLOSED
PENDING_03B_ABORT_ON_REPLAY_FAILURE
PENDING_05_ABORT_ON_REPLAY_FAILURE
NO_LOCAL_FALLBACK
NO_RUNTIME_REPLAN

NO_NEW_GRADIENT_D2H
NO_NEW_GPU_GRADIENT_REDUCTION

NO_NEW_FUSION_POLICY
NO_NEW_DELTAK_FORMULA
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_POLICY_AUTHORITY_UNCHANGED

STATIC_06_210_OF_210_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_REPLAY_EXECUTION_UNVERIFIED
```
