# ASH-BP-DK-FUSION-LOCAL-ONE-STEP-OBJECTIVE-PROBE-10

## Status

```text
Patch ID: ASH-BP-DK-FUSION-LOCAL-ONE-STEP-OBJECTIVE-PROBE-10
Direct parent: ASH-BP-DK-ACTIVE-FUSION-COUNTERFACTUAL-EFFECT-LEDGER-09
Required upstream: 08B-R1 / 08B / 08A / 07 / 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: evaluate Source, authoritative Actual whole-step candidate, and same-source Local counterfactual candidate on one exact objective probe without changing optimizer authority
New loss/objective mathematics: none
New Fusion/Muon WGSL: none
New Delta-K formula: none
New Fusion policy: none
Backward authority: none
Optimizer mutation authority: none
Precision authority: unchanged
Residency authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

09 closes update-space causality:

```text
actual Fused update
vs
physically witnessed same-source production-Local update
```

10 is the first objective-space observation stage:

```text
same committed source generation
same probe batch
same objective
same forward precision
same deterministic forward contract

Source model
Actual whole-step candidate
Local counterfactual whole-step candidate
        -> Source objective
        -> Actual objective
        -> Local objective
        -> signed one-step objective deltas
```

The allowed claim remains probe-local:

```text
On this exact one-step probe, the actual candidate objective differed from the Local counterfactual objective by X.
```

10 does not establish long-horizon training benefit, generalization benefit, or planner-policy optimality.

## Runtime mode

10 introduces:

```text
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_MODE=DISABLED
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_MODE=OBSERVE
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_MODE=QUALIFICATION
```

Default is `DISABLED`.

When 10 is enabled, 09 must also be enabled because the Local counterfactual overlay is admitted only through the current 09 causal evidence lineage.

`QUALIFICATION` requires 09 `REQUIRE_QUALIFIED` so the objective probe cannot silently strengthen an Observe-only counterfactual lineage.

## Probe batch source

10 supports explicit batch-source selection:

```text
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_BATCH_SOURCE=TRAINING_BATCH_REPLAY
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_BATCH_SOURCE=FIXED_PROBE_BATCH
```

For fixed probing, the ordinal is explicit through:

```text
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_FIXED_BATCH_ORDINAL
```

The Source, Actual, and Local branches use the exact same probe-batch identity. The batch identity binds the selected batch source, ordinal/range identity, input/target cardinality, and deterministic digest surface used by the existing BaseTrain runtime.

There is no same-dataset or nearest-batch substitution.

## Objective authority

10 does not add a new loss implementation.

It reuses the existing BaseTrain Atlas final real-loss path:

```text
atlas_runtime_final_output_real_loss
R1J_R2C active-slot objective authority
active-slot weighted loss_mean reduction
objective direction = Minimize
```

The probe config explicitly disables backward and optimizer commit.

The same canonical objective identity is used for Source, Actual, and Local evaluations.

10 records:

```text
J_source
J_actual
J_local

actual_minus_source = J_actual - J_source
local_minus_source  = J_local - J_source
actual_minus_local   = J_actual - J_local
```

Signs are preserved. The schema does not create `FusionBetter`, `BenefitScore`, or another scalar benefit authority.

## Objective direction

The core schema represents objective direction explicitly:

```text
Minimize
Maximize
```

The current adopted Atlas real-loss objective is `Minimize`.

This prevents the ledger schema from silently assuming that every future objective uses lower-is-better semantics.

## Stochastic policy

10 exposes:

```text
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_STOCHASTIC_POLICY=DETERMINISTIC_NO_STOCHASTICITY
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_STOCHASTIC_POLICY=EXACT_RNG_REPLAY
```

R1 physically supports only the deterministic-no-stochasticity path.

`EXACT_RNG_REPLAY` is intentionally fail-closed in this revision with:

```text
ASH_BP_DK_OBJECTIVE_PROBE_EXACT_RNG_REPLAY_UNAVAILABLE_R1
```

10 does not silently disable dropout/stochastic behavior or downgrade ExactRngReplay to another mode.

A later revision must provide a real RNG snapshot/restore authority before ExactRngReplay can be promoted.

## Whole-step Actual candidate authority

The existing R6 candidate path already materializes the completed whole-step model into the canonical packed candidate weight pack.

Therefore:

```text
ActualCandidateProjection
=
completed authoritative packed candidate weight pack
```

No second Actual model is constructed for probing.

The probe is admitted only after the whole parameter candidate set is complete. A mixed-generation or partially materialized candidate is not a valid objective-probe model.

## Local counterfactual model definition

The Local counterfactual is defined as:

```text
Actual whole-step candidate
+
read-only sparse Local weight overlay for tiles that were actually Fused
```

Equivalently, everything in the candidate remains identical to Actual except the 16x16 tiles for actual `FusedRight` / `FusedDown` domains, which are replaced by the 08B production-Local candidate weights from the same source state.

This isolates the Fusion intervention while preserving all other actual candidate changes, including ordinary Local and non-Fusion optimizer updates.

## No second whole-model counterfactual copy

10 does not clone the full candidate model and patch it.

The runtime stores only sparse tile overrides:

```text
AshBpDkObjectiveProbeSparseTileOverlay
```

Each overlay is keyed by typed parameter/tile/generation identity and carries exactly one canonical 16x16 Local candidate weight tile.

The required cardinality is:

```text
sparse overlay tile count == 2 * actual fused pair count
```

Duplicate tile ownership or missing fused-tile overlays fail closed.

## Read-only sparse weight projection

10 introduces:

```text
AshObjectiveProbeSparseWeightProjection
```

The Actual candidate pack remains immutable.

The projection maps each canonical 16x16 tile into its exact row byte ranges and overlays only those ranges during reads. It does not:

```text
overwrite the Actual candidate buffer
patch then restore candidate bytes
create a second whole-model candidate pack
commit counterfactual weights
```

The projected virtual whole-file digest and projected per-parameter/per-segment digests are recomputed from projected bytes so the forward runtime cannot accidentally treat the base Actual digest as the Local counterfactual digest.

## Projection-aware forward read path

To evaluate a sparse projected model without changing the model mathematics, 10 extends the existing Atlas weight-read plumbing through:

```text
base_train_atlas_wave_01_residency_coordinator
atlas_runtime_route_admission
device_limit_aware_micro_atlas_vocab_row_paging
atlas_runtime_forward_wave_execution
atlas_runtime_final_output_real_loss
```

The projection-aware path covers tensor segment reads, forward-wave reads, residency uploads, and the final-output tensor load.

Non-projected wrappers remain available and preserve the normal BaseTrain path.

This is a forward weight-read infrastructure extension, not a new Fusion/Muon shader or new model objective implementation.

## Projection identity

Three model identities are sealed:

```text
SourceModelProjectionDigest
ActualCandidateProjectionDigest
LocalCounterfactualProjectionDigest
```

The Local projection digest binds:

```text
Actual candidate projection identity
+ ordered sparse Local overlay identities/bytes
```

The projection path also validates that its base path and virtual source digest match the Atlas plan being evaluated.

## Exact current causal lineage

10 binds the current 09 causal parameter entries before probing.

The objective-probed generation must use the same current:

```text
optimizer generation
BP generation
07 actual POST lineage
08B/08B-R1 Local counterfactual lineage
09 causal parameter set
```

The sparse overlay is built only from the same actual fused tiles represented by that causal lineage.

No stale 09 entry or unrelated Local tile is admitted.

## No-Fusion observation gap

10 does not require every training generation to have an objective probe entry.

If 10 is enabled but the current generation contains no actual fused/counterfactual causal entries:

```text
09 current causal parameter set = empty
10 sparse overlay = empty
```

then the generation is treated as **unobserved by 10**.

The training generation is not failed and 10 does not create a fake objective delta of zero. The existing probe ledger head is carried forward unchanged.

This follows the same explicit-observation-gap rule used by 09.

## Three-way evaluation

For an observed generation, the scheduler constructs the exact same probe execution contract and evaluates in canonical primary order:

```text
Source
-> Actual
-> Local counterfactual
```

The same:

```text
probe batch identity
objective identity
forward precision identity
stochastic policy identity
```

is bound to all three branches.

The branch evaluator uses the existing final real-loss forward and requires its backward/optimizer/weight-mutation counters to remain zero.

## Forward-only authority

10 is observation only.

Required hard-zero semantic authority:

```text
probe backward count = 0
probe gradient write count = 0
probe gradient accumulation count = 0
probe optimizer mutation count = 0
probe planner feedback count = 0
probe policy mutation count = 0
probe Delta-K mutation count = 0
probe counterfactual commit count = 0
```

The probe objective never changes which candidate is committed.

Even if the Local objective is lower than the Actual objective under the current Minimize objective, the authoritative commit candidate remains the Actual candidate selected/generated by the existing optimizer path.

## Qualification replay

`QUALIFICATION` reruns the same three projections with the same batch/objective/forward contract:

```text
Source primary / Source replay
Actual primary / Actual replay
Local primary / Local replay
```

R1 requires exact objective bit equality through `to_bits()` for each same-path replay.

There is no tolerance auto-widening and no silent switch to an approximate comparison.

If the current backend/objective path cannot satisfy exact replay, Qualification fails rather than fabricating a weaker qualification state.

## Numerical evidence digest

The objective receipt digest canonically binds semantic identity plus exact bit representations of:

```text
J_source
J_actual
J_local
actual_minus_source
local_minus_source
actual_minus_local
```

No JSON decimal formatting becomes numerical hash authority.

All observed objective values and deltas must be finite.

## Objective-probe receipt

`AshBpDkOneStepObjectiveProbeReceipt` binds at minimum:

```text
schema/patch revision
mode
optimizer generation
BP generation
probe batch identity/digest
objective identity/digest/direction
stochastic policy identity
forward precision identity
source projection digest
actual projection digest
Local counterfactual projection digest
09 causal lineage identity
source objective
actual objective
Local objective
three signed deltas
hard-zero authority counters
receipt digest
```

The receipt is derived observation evidence, not model state.

## Separate objective-probe ledger

10 owns a ledger separate from 07 and 09:

```text
07 = actual POST ledger
09 = actual-vs-Local update causal ledger
10 = one-step objective probe ledger
```

Runtime sidecars are:

```text
bp_dk_one_step_objective_probe_entry.json
bp_dk_one_step_objective_probe_head.json
```

The head contains its own probe-ledger sequence and previous observed optimizer-generation identity so unprobed generations remain explicit gaps rather than zero-valued observations.

## Candidate persistence ordering

The candidate transaction preserves dependency order:

```text
07 actual POST state
-> 09 counterfactual-effect state
-> 10 objective-probe state
```

10 candidate persistence validates the already-written 09 candidate entry/head and the current causal parameter-set identity before sealing the probe entry/head.

For an unobserved generation, the previous committed 10 head is carried forward without creating a generation entry.

## Commit ordering

The existing commit chain is extended as:

```text
03B temporal commit
05 planner commit
07 actual POST ledger commit
09 causal-effect ledger commit
10 objective-probe ledger commit
```

10 verifies the exact current committed 09 head before promoting its pending in-memory head.

Therefore objective evidence cannot become committed history before the actual candidate and its 09 causal lineage are committed.

## Abort semantics

Any probe failure while 10 is explicitly observing/qualifying invokes the existing step-abort lifecycle before returning the error.

On active-step abort:

```text
pending 10 receipt/head discarded
committed 10 head unchanged
sparse counterfactual overlays cleared
```

There is no last-good objective receipt fallback.

## Restore and legacy genesis

Pre-10 checkpoints without a probe-ledger sidecar enter an explicit deterministic legacy genesis.

10 never invents historical objective probes for generations that predate adoption or were not observed.

A claimed 10 sidecar with contradictory schema/digest/generation lineage fails closed.

## Telemetry

10 adds observation telemetry including:

```text
objective probe run count
Source forward count
Actual forward count
Local forward count
replay count / replay mismatch count
batch mismatch count
objective mismatch count
RNG mismatch count
precision mismatch count
incomplete candidate count
overlay mismatch count
nonfinite count
backward count
gradient write count
optimizer mutation count
planner feedback count
policy mutation count
Delta-K mutation count
counterfactual commit count
state commit/abort/legacy-restore surfaces
```

Hard-zero mutation counters are part of success authority.

## Performance boundary

An Observe probe can add three full forward evaluations:

```text
Source + Actual + Local
```

Qualification can add their exact replays and therefore up to six forward evaluations.

This overhead is diagnostic/qualification cost. 10 does not claim improved throughput, lower memory use, or production performance benefit.

## Changed files

The 10 overlay contains exactly thirteen files:

```text
crates/ash_core/src/fusion_local_one_step_objective_probe.rs
crates/ash_core/src/lib.rs
crates/base_train/src/atlas_runtime_final_output_real_loss.rs
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/atlas_runtime_route_admission.rs
crates/base_train/src/base_train_atlas_wave_01_residency_coordinator.rs
crates/base_train/src/bp_delta_k_fusion_local_one_step_objective_probe.rs
crates/base_train/src/device_limit_aware_micro_atlas_vocab_row_paging.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_local_one_step_objective_probe_10_static.py
```

No Fusion/Muon WGSL file and no fused/local Muon backend mathematics file is added by 10.

## Static validation

New gate:

```text
validate_ash_bp_dk_fusion_local_one_step_objective_probe_10_static.py
259/259 PASS
```

The gate validates among other things:

```text
09 direct-parent lineage
07 / 08B / 08B-R1 authority preservation
no full counterfactual model copy
no Actual patch-and-restore
projection-aware weight-read coverage
same Source/Actual/Local batch/objective/forward identity
existing Atlas real-loss reuse
explicit objective direction
signed objective deltas
ExactRngReplay R1 fail-closed boundary
Qualification exact replay
09 -> 10 persist/commit ordering
observation-gap semantics
no probe-controlled candidate selection
no backward / optimizer / planner / Delta-K authority
no new Fusion/Muon WGSL or policy
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
09 Counterfactual Effect Ledger                 148/148 PASS
10 One-Step Objective Probe                     259/259 PASS
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

10 is appended to the existing CF1 static-validator chain after 09 without rewriting the older 04/05/06/07/08/09 closure semantics.

## Packaging

The baked output is split into:

```text
full-body bake: 18,606,409 bytes / 7,148 entries
overlay bake:      168,756 bytes / exactly 13 files
```

Both ZIP archives pass archive integrity testing.

Generated artifact/manifest/report directories, `target`, `__pycache__`, and `*.sha256` files are excluded from the delivered ZIPs.

## Bake-environment boundary

The bake environment does not contain:

```text
cargo
rustc
rustfmt
physical WGPU runtime/adapter
```

Therefore this bake does not claim:

```text
Rust compile success
projection-aware physical forward success
Source/Actual/Local physical objective values
Qualification exact objective replay on hardware
10 checkpoint/restart runtime parity
objective-level Fusion benefit
```

Correct current status is:

```text
10_OBJECTIVE_PROBE_SOURCE_PATH_WIRED
10_SPARSE_COUNTERFACTUAL_PROJECTION_WIRED
10_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_00_09_AND_LOCAL_MUON_STATIC_LINEAGE_PASS
PHYSICAL_OBJECTIVE_PROBE_EXECUTION_UNVERIFIED
```

## Required user-local gates

Before runtime promotion:

```text
cargo fmt --check
cargo check
CF1 reaches 10

08B-R1 physical receipt exists for actual fused generation
09 current causal entry exists and exact-joins it
whole 201-parameter candidate pack completes
sparse Local overlay cardinality = 2 * fused pair count

Source forward succeeds
Actual candidate forward succeeds
Local sparse-projection forward succeeds
same batch/objective/precision identity for all three
all objective values finite
all backward/gradient/optimizer mutation counters zero

Qualification mode:
Source primary/replay objective exact bits equal
Actual primary/replay objective exact bits equal
Local primary/replay objective exact bits equal

candidate persistence order 07 -> 09 -> 10
commit order 07 -> 09 -> 10
abort leaves committed 10 head unchanged
checkpoint restart restores deterministic probe head
```

## Claim boundary after physical verification

After a real user-local 10 receipt is generated and validated, the supported claim is limited to:

```text
For this exact source generation, probe batch, objective, precision and deterministic forward contract, the actual Fused candidate objective differed from the physically witnessed same-source Local counterfactual candidate objective by the recorded signed amount.
```

Still not established:

```text
Fusion improves training overall
Fusion generalizes better
Fusion is statistically superior
05 planner thresholds should change
```

## Natural successor

The next correctness/observation revision is:

```text
ASH-BP-DK-FUSION-OBJECTIVE-LONG-HORIZON-TRAJECTORY-11
```

11 should join over time:

```text
03B PRE Bridge Delta-K
05 Fusion/Fission decisions
07 actual POST update evidence
09 actual-vs-Local causal update divergence
10 one-step objective divergence
```

and observe persistence, sign reversals, oscillation, no-improvement windows, Fusion lifetime and Fission frequency without immediately feeding those observations back into 05 policy.

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_10

09_DIRECT_PARENT
07_ACTUAL_HISTORY_BOUND
08B_R1_PHYSICAL_COUNTERFACTUAL_LINEAGE_BOUND
09_CAUSAL_EFFECT_LINEAGE_BOUND

EXISTING_ATLAS_FINAL_REAL_LOSS_REUSED
ACTIVE_SLOT_WEIGHTED_LOSS_MEAN_REUSED
OBJECTIVE_DIRECTION_MINIMIZE_EXPLICIT
NO_NEW_OBJECTIVE_MATHEMATICS

TRAINING_BATCH_REPLAY_SUPPORTED
FIXED_PROBE_BATCH_SUPPORTED
EXACT_PROBE_BATCH_IDENTITY_SHARED

DETERMINISTIC_NO_STOCHASTICITY_SUPPORTED
EXACT_RNG_REPLAY_EXPLICITLY_UNAVAILABLE_R1
NO_SILENT_STOCHASTIC_FALLBACK

SOURCE_WHOLE_MODEL_PROJECTION_BOUND
ACTUAL_COMPLETED_201_PARAMETER_CANDIDATE_PACK_BOUND
LOCAL_COUNTERFACTUAL_READ_ONLY_SPARSE_PROJECTION_BOUND

ONLY_ACTUAL_FUSED_TILES_OVERLAID
TWO_LOCAL_TILES_PER_FUSED_PAIR
NO_SECOND_WHOLE_MODEL_COUNTERFACTUAL_COPY
NO_ACTUAL_CANDIDATE_PATCH_AND_RESTORE

PROJECTION_AWARE_RESIDENCY_READS
PROJECTION_AWARE_ROUTE_READS
PROJECTION_AWARE_PAGING_READS
PROJECTION_AWARE_FORWARD_READS
PROJECTION_AWARE_FINAL_OUTPUT_READ
PROJECTED_VIRTUAL_SOURCE_DIGEST_BOUND

SOURCE_OBJECTIVE_OBSERVED
ACTUAL_OBJECTIVE_OBSERVED
LOCAL_OBJECTIVE_OBSERVED
SIGNED_ACTUAL_MINUS_SOURCE
SIGNED_LOCAL_MINUS_SOURCE
SIGNED_ACTUAL_MINUS_LOCAL

QUALIFICATION_EXACT_OBJECTIVE_BIT_REPLAY
NO_TOLERANCE_AUTO_WIDEN

NO_FUSION_GENERATION_IS_EXPLICIT_OBSERVATION_GAP
NO_FAKE_ZERO_OBJECTIVE_EFFECT

FORWARD_ONLY
NO_BACKWARD
NO_GRADIENT_ACCUMULATION
NO_OPTIMIZER_MUTATION
NO_PLANNER_FEEDBACK
NO_POLICY_MUTATION
NO_DELTAK_MUTATION
NO_COUNTERFACTUAL_COMMIT

OBJECTIVE_RESULT_DOES_NOT_CHOOSE_COMMIT_CANDIDATE

SEPARATE_10_OBJECTIVE_PROBE_LEDGER
PERSIST_ORDER_07_09_10
COMMIT_ORDER_07_09_10
ABORT_DOES_NOT_ADVANCE_10_HEAD

NO_NEW_FUSION_MUON_WGSL
NO_NEW_FUSION_POLICY
NO_NEW_DELTAK_FORMULA
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_10_259_OF_259_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_OBJECTIVE_PROBE_EXECUTION_UNVERIFIED
```
