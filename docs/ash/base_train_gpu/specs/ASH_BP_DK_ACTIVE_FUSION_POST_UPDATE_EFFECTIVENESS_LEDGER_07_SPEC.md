# ASH-BP-DK-ACTIVE-FUSION-POST-UPDATE-EFFECTIVENESS-LEDGER-07

## Status

```text
Patch ID: ASH-BP-DK-ACTIVE-FUSION-POST-UPDATE-EFFECTIVENESS-LEDGER-07
Direct parent: ASH-BP-DK-ACTIVE-FUSION-DETERMINISTIC-REPLAY-06
Required upstream: 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: observe and hash-chain actual source-to-candidate Local/Fused/Fission update effects
New planner policy: none
New Delta-K formula: none
New WGPU observer: none
New gradient D2H: none
Muon mathematics: unchanged
Precision authority: unchanged
Residency policy authority: unchanged
```

## Central SSOT

07 records what the already-authoritative 05 execution actually produced. It does not decide whether fusion was beneficial.

```text
03A PRE signed gradient relation
+ 03B PRE Bridge I/M/DeltaK
+ 04 current graph identity
+ 05 actual Local/Fused/Fission execution plan
+ optional 06 replay verification identity
+ exact source weight/momentum
+ exact candidate weight/momentum/orthogonal update
        -> canonical 16x16 POST tile evidence
        -> actual fused/fission pair POST evidence
        -> generation-level hash-chained ledger entry
```

The claim boundary is explicit:

```text
Observed physical update effect != causal fusion benefit
Actual fused update != proof that fused was better than Local
06 replay != Local counterfactual
```

No counterfactual Local path is executed in 07.

## Observation timing

07 is wired after successful 05 candidate computation and, when requested, after successful 06 replay verification, but before the parent run-local RAM momentum candidate is updated.

```text
primary Local/Fused candidate
-> optional 06 replay verification
-> 07 POST source-to-candidate observation
-> stage 07 parameter receipt
-> parent RAM momentum candidate adoption
```

This preserves the exact source momentum used by 05 while POST deltas are measured.

## Canonical POST unit

Canonical evidence ownership remains one physical 16x16 TensorCube, even when 05 executes a logical 16x32 or transposed 32x16 fused domain.

Each tile receipt is built from exactly 256 F32 values:

```text
DeltaW[i] = candidate_weight[i] - source_weight[i]
DeltaM[i] = candidate_momentum[i] - source_momentum[i]
U[i]      = physical orthogonal_update[i]
```

and records:

```text
source weight RMS
candidate weight RMS
DeltaW RMS
source momentum RMS
candidate momentum RMS
DeltaM RMS
orthogonal-update RMS
```

All source/candidate inputs must be finite. No sampling, row sketch, compressed direction proxy, NaN repair, Inf clamp, or silent zero replacement is used.

## POST pair evidence

07 produces pair evidence only for actual 05 fused/fission/cooldown pair history. It does not scan every adjacent tile and does not reconstruct an N^2 pair space.

For pair A/B it observes exact 256-D canonical vector relationships:

```text
POST weight-delta cosine      = cosine(DeltaW_A, DeltaW_B)
POST momentum-delta cosine    = cosine(DeltaM_A, DeltaM_B)
POST orthogonal-update cosine = cosine(U_A, U_B)
```

A zero-norm vector produces explicit `UndefinedZeroNorm` with no semantic cosine value. It is not rewritten as cosine zero.

## PRE binding

When the current 04 graph still has the pair edge, the POST pair receipt binds:

```text
03A signed gradient cosine
03B I_BRIDGE
03B M_BRIDGE
03B DeltaK_BRIDGE_PRE raw
03B DeltaK_BRIDGE_PRE smoothed
```

Hard fission can occur precisely because the current Ready edge disappeared or capability/topology continuity broke. In that case the absent current PRE edge is represented as `None`; 07 does not fabricate zero PRE evidence.

## Transition identity from actual 05 state

07 does not infer transition type only from the current plan shape.

The production callsite captures:

```text
planner candidate snapshot immediately before 05 plan_parameter()
planner candidate snapshot immediately after 05 plan_parameter()
```

and joins those snapshots with the actual 05 execution plan.

Supported POST transition evidence includes:

```text
NewFusion
RetainedFusion
SoftFission
HardFission
PolicyRebaselineLocal
CooldownLocal
```

Retained fusion requires the pre-plan committed pair state to already be `Fused`. A selected pair that was not previously Fused is `NewFusion`.

Fission classification is fail-closed and considers current policy identity, Bridge topology identity, generation continuity, current graph edge availability, and physical fused-shape capability.

## Actual execution identity

Every tile receives exactly one execution-kind projection:

```text
Local
FusedRightLhs
FusedRightRhs
FusedDownLhs
FusedDownRhs
FissionedLocal
CooldownLocal
```

The 05 execution plan must cover every full Muon tile exactly once before POST evidence is admitted. Duplicate tile ownership or missing tile ownership is a structural failure.

## Replay binding

07 records the explicit 06 replay mode:

```text
Disabled        -> Not verified, no replay receipt digest
PlanOnly        -> verified replay receipt digest required
CandidateDigest -> verified replay receipt digest required
```

A requested replay mode with no verified receipt is rejected. 07 does not interpret primary-vs-replay execution as Fusion-vs-Local evidence.

For qualification runs, `CANDIDATE_DIGEST` remains the strongest replay seal. Production can explicitly run replay Disabled without pretending replay verification occurred.

## Parameter receipt

`AshBpDkPostUpdateParameterReceipt` binds:

```text
parameter identity / revision / optimizer generation / BP generation
04 graph topology digest
04 graph evidence digest
05 execution plan digest
05 planner policy digest
05 physical capability digest
06 replay binding when requested
candidate weight digest
candidate momentum digest
orthogonal-update digest
ordered canonical tile POST receipts
ordered fused/fission/cooldown pair receipts
parameter receipt digest
```

F32 evidence in the canonical parameter digest is serialized through exact `to_bits().to_le_bytes()` representation.

## No scalar effectiveness score

07 does not define:

```text
fusion_effectiveness_score
success_score
benefit_score
POST Delta-K
```

The dimensions remain separate evidence. There is no weighted collapse and no planner threshold feedback.

## No planner feedback authority

The dependency remains one-way:

```text
05 planner -> 07 ledger
```

There is no 07 code path that mutates:

```text
fusion policy
fuse streak
fission streak
cooldown
matching order
precision policy
residency policy
```

Hard-zero telemetry seals:

```text
post_update_planner_feedback_count = 0
post_update_policy_mutation_count = 0
post_update_gradient_d2h_bytes = 0
```

## Generation ledger

07 stages parameter receipts in canonical parameter-index order and creates one generation entry after the full optimizer candidate has been computed.

`AshBpDkPostUpdateGenerationEntry` binds:

```text
training generation
optimizer generation
BP generation
previous committed ledger-head digest
ordered parameter receipt digests
entry digest
```

The ledger head advances by hash chain:

```text
LedgerHead_N
= SHA256(
    ledger digest revision
    || LedgerHead_(N-1)
    || GenerationEntryDigest_N
  )
```

This avoids keeping the full historical ledger in RAM while preserving deterministic generation lineage.

## Candidate persistence and commit boundary

Runtime candidate sidecars are:

```text
bp_dk_active_fusion_post_update_ledger_entry.json
bp_dk_active_fusion_post_update_ledger_head.json
```

They are written into the candidate transaction directory through the existing `persist_candidate_state(...)` path.

In-memory ledger authority remains pending until the existing scheduler successfully executes:

```text
commit_active_state(...)
-> staging_guard.mark_committed(...)
-> ProductionMuonRuntime::record_step_commit()
```

`record_step_commit()` commits 03B temporal state, 05 planner state, and then the pending 07 ledger head. The scheduler source itself does not need a new alternate commit path.

If active commit fails, the existing `record_step_abort(target_step)` callback now also aborts pending 07 receipts/head state.

Therefore a candidate that was calculated but never promoted cannot become committed POST history.

## Legacy and restart authority

A checkpoint predating 07 and containing no ledger-head sidecar starts from an explicit deterministic genesis head and increments `legacy_genesis_count`.

A checkpoint containing a 07 ledger head validates:

```text
schema
source training generation
source optimizer generation
source BP generation
non-empty ledger-head digest
```

Partial or contradictory generation identity fails closed.

The first generation after legacy adoption does not invent prior POST entries.

## Parent execution preservation

07 does not modify the 06 replay core/base implementation, the 05 planner core/base implementation, the fused-pair backend, or either 16x32 fused WGSL file.

Parent-preserved SHA anchors in this bake include:

```text
active_fusion_deterministic_replay.rs
4c92c48e5e5552837218471e2a441f706ebf3151a8d90badf73516ce09f6bbdb

bp_delta_k_active_fusion_deterministic_replay.rs
6ed468023ae7756e55d45e7fa25e0a74b2e46105a1af347be25fcbbef65f55a5

bp_dk_fusion_fission_planner.rs
53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

tensorcube_fused_pair_muon.rs
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

base_train_tensorcube_fused_pair_muon_16x32.wgsl
4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

base_train_tensorcube_fused_pair_muon_16x32_exact_subgroup32_norm.wgsl
2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

## Changed files

The 07 overlay contains exactly seven changed/new code files:

```text
crates/ash_core/src/active_fusion_post_update_effectiveness.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_active_fusion_post_update_effectiveness.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_post_update_effectiveness_ledger_07_static.py
```

No scheduler, fused backend, or WGSL file is changed by 07.

## Static validation

New gate:

```text
validate_ash_bp_dk_active_fusion_post_update_effectiveness_ledger_07_static.py
206/206 PASS
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
```

Revalidated Local Muon lineage:

```text
Local Muon optimizer                            101/101 PASS
FirstCandidate registry                          97/97 PASS
Multi-tile batch                                 61/61 PASS
Production callsite                              63/63 PASS
Registry loader repair                           38/38 PASS
ExactSubgroup32 norm                            128/128 PASS
X PAD17                                          52/52 PASS
Generation-sealed immutable cache                66/66 PASS
Immutable-cache backend rebind                   35/35 PASS
```

07 is appended after 05 and 06 in the existing CF1 static-validator chain without rewriting the parent AllValidators closure.

## Physical execution boundary

The bake environment does not provide `cargo`, `rustc`, `rustfmt`, a WGSL validator, or a physical WGPU runtime.

Therefore this bake does not claim:

```text
Rust compile success
physical Local/Fused POST metric execution success
checkpoint/restart ledger parity
physical 06 replay-qualified POST parity
training-quality improvement
Fusion-vs-Local causal benefit
```

Current status is:

```text
POST_LEDGER_SOURCE_PATH_WIRED
STATIC_SOURCE_CONTRACT_CLOSED
PARENT_05_06_PHYSICAL_SOURCES_PRESERVED
PHYSICAL_POST_EXECUTION_UNVERIFIED
```

## Required user-local physical gates

```text
cargo fmt / cargo check
CF1 compile chain reaches 07

Local tile exact DeltaW / DeltaM / U RMS fixture
FusedRight two-tile POST receipt fixture
FusedDown two-tile POST receipt fixture
SoftFission -> two Local receipts + one pair transition receipt
HardFission with missing PRE edge -> no fabricated PRE values
zero-norm POST cosine -> UndefinedZeroNorm
06 CANDIDATE_DIGEST verified receipt binding
no gradient D2H
no planner feedback

candidate ledger sidecars written before active commit
active commit success -> ledger head commit
active commit failure -> pending ledger abort
checkpoint/restart -> same next generation entry/head digest
```

## Packaging

The delivered code bake is split into full-body and seven-file overlay ZIPs. Generated artifact/manifest/report directories and `*.sha256` files are excluded from the ZIP packaging. Runtime ledger sidecar filenames exist only as source/runtime contracts; generated runtime sidecar instances are not shipped in the bake.

## Non-goals

```text
No counterfactual all-Local execution
No causal Fusion benefit claim
No loss-improvement claim
No scalar effectiveness score
No POST Delta-K formula
No automatic planner calibration
No threshold mutation
No new WGPU observer
No new gradient D2H
No Muon math change
No planner matching change
No precision decision
No residency-policy decision
```

## Natural successor

07 closes the actual-execution observation line. The next correctness step should be an explicit same-source counterfactual comparison revision:

```text
ACTUAL FUSED candidate
vs
SAME-SOURCE COUNTERFACTUAL ALL-LOCAL candidate
```

Only that later authority can support statements about how Fusion changed an update relative to Local. A separate performance line can then remove the known 05 mixed-path resident-cache/upload debt without changing the 05 planner semantics.

## Promotion seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_POST_UPDATE_EFFECTIVENESS_LEDGER_07

05_ACTUAL_EXECUTION_BOUND
06_REPLAY_IDENTITY_BINDABLE

CANONICAL_16X16_POST_TILE_AUTHORITY
EXACT_256D_SOURCE_TO_CANDIDATE_WEIGHT_DELTA
EXACT_256D_SOURCE_TO_CANDIDATE_MOMENTUM_DELTA
EXACT_256D_ORTHOGONAL_UPDATE

POST_WEIGHT_DELTA_RMS
POST_MOMENTUM_DELTA_RMS
POST_ORTHOGONAL_UPDATE_RMS

FUSED_PAIR_POST_WEIGHT_DELTA_COSINE
FUSED_PAIR_POST_MOMENTUM_DELTA_COSINE
FUSED_PAIR_POST_ORTHOGONAL_UPDATE_COSINE
ZERO_NORM_IS_NOT_ZERO_COSINE

PLANNER_BEFORE_AND_AFTER_STATE_BOUND
NEW_FUSION_OBSERVED
RETAINED_FUSION_OBSERVED
SOFT_FISSION_OBSERVED
HARD_FISSION_OBSERVED
POLICY_REBASELINE_LOCAL_OBSERVED
COOLDOWN_LOCAL_OBSERVED

CURRENT_PRE_EDGE_BOUND_WHEN_AVAILABLE
MISSING_HARD_FISSION_PRE_EDGE_NOT_FABRICATED

NO_COUNTERFACTUAL_LOCAL_CLAIM
NO_FUSION_BENEFIT_CLAIM
NO_SCALAR_EFFECTIVENESS_SCORE
NO_POST_DELTAK_FORMULA

NO_PLANNER_FEEDBACK
NO_AUTOMATIC_THRESHOLD_CALIBRATION

GENERATION_LEVEL_HASH_CHAINED_LEDGER
PENDING_LEDGER_HEAD_SEPARATE_FROM_COMMITTED_HEAD
ACTIVE_MODEL_COMMIT_PRECEDES_LEDGER_MEMORY_PROMOTION
ABORTED_ACTIVE_COMMIT_ABORTS_PENDING_LEDGER

DETERMINISTIC_LEGACY_GENESIS
CHECKPOINT_HEAD_RESTORE_VALIDATION

NO_NEW_WGPU_OBSERVER
NO_NEW_GRADIENT_D2H
NO_MUON_MATH_CHANGE
NO_PLANNER_POLICY_CHANGE

STATIC_07_206_OF_206_PASS
PARENT_STATIC_LINEAGE_PASS
PHYSICAL_POST_EXECUTION_UNVERIFIED
```
