# ASH-BP-DK-FUSION-OBJECTIVE-LONG-HORIZON-TRAJECTORY-11

## Status

```text
Patch ID: ASH-BP-DK-FUSION-OBJECTIVE-LONG-HORIZON-TRAJECTORY-11
Direct parent: ASH-BP-DK-FUSION-LOCAL-ONE-STEP-OBJECTIVE-PROBE-10
Required upstream: 09 / 08B-R1 / 08B / 08A / 07 / 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: convert committed Fusion/Fission, POST update, counterfactual-update and one-step objective evidence into a bounded long-horizon diagnostic trajectory
New forward execution: none
New backward execution: none
New counterfactual execution: none
New gradient access/readback: none
New Fusion/Muon WGSL: none
New Delta-K formula: none
New Fusion policy: none
Automatic planner feedback: forbidden
Automatic threshold calibration: forbidden
Precision authority: unchanged
Residency authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

11 does not introduce another optimizer or probe path. It consumes already-existing committed evidence and attaches a bounded time axis to it:

```text
03B PRE Bridge evidence
        -> 05 actual Fusion/Fission transition
        -> 07 actual POST update evidence
        -> 09 physically witnessed actual-vs-Local update divergence
        -> 10 whole-step Actual-vs-Local objective probe
        -> 11 long-horizon diagnostic trajectory
```

The dependency remains one-way. 11 never feeds a decision back into 05.

The question answered by 11 is:

```text
How did a typed Fusion pair's PRE state, actual transition, actual update,
and physically witnessed Local-counterfactual divergence evolve over time,
and what whole-step objective context was observed on those generations?
```

11 is observation and health description only. It does not decide that Fusion is globally beneficial or harmful.

## Critical objective-attribution boundary

10 evaluates a **whole-step** model intervention:

```text
Actual whole-step candidate
vs
Actual candidate + sparse Local overrides for the full set of actually fused tiles
```

Therefore 10's:

```text
actual_minus_local objective
```

is a generation-level fused-set objective context. It is **not** a per-pair causal objective attribution.

11 deliberately does not copy the same 10 objective delta into every pair and call it that pair's effect.

Authority is separated as:

```text
Pair trajectory:
  PRE 03B / 03A evidence
  05 transition history
  07 pair POST history
  optional 09 pair counterfactual update divergence

Generation objective context:
  10 whole-step Source / Actual / Local objective
  10 actual_minus_local
  10 objective direction / qualification mode
```

Pair-level correlation with the generation objective context is descriptive co-observation only. It is not pair-level objective causality.

## Runtime modes

11 introduces:

```text
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_MODE=DISABLED
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_MODE=DECISION_AND_UPDATE
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_MODE=OBJECTIVE_OBSERVED
```

Default is `DISABLED`.

### DECISION_AND_UPDATE

Records committed 07 pair transition/POST history and enriches it with 09 counterfactual-update evidence when present. A 10 objective probe is optional.

This mode therefore continues to observe Fusion entry, retention, fission and cooldown even when objective probing is sparse.

### OBJECTIVE_OBSERVED

Requires 10 objective-probe mode to be enabled. A generation with no current 10 objective observation becomes an explicit observation gap for 11: the current 11 head is carried forward and no fake zero-objective sample is created.

There is no silent mode downgrade.

## Diagnostic thresholds

11 exposes explicit diagnostic-only thresholds:

```text
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_MIN_HEALTH_SAMPLES
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_OSCILLATION_REVERSALS
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_LOCAL_PREFERRED_STREAK
```

R1 defaults are:

```text
minimum health samples = 8
oscillation reversal threshold = 3
Local-preferred observed-probe streak threshold = 4
```

These values classify diagnostic evidence only. They are not Fusion/fission thresholds, optimizer hyperparameters, or planner policy authority.

All three values are explicit and must be positive. There is no hidden adaptive threshold mutation.

## Observation tiers

The pair sample tier is typed:

```text
PostUpdateObserved
CounterfactualUpdateObserved
ObjectiveObserved
ObjectiveQualified
```

### PostUpdateObserved

A committed 07 pair transition/POST sample exists.

### CounterfactualUpdateObserved

The same pair also exact-joins a committed 09 counterfactual-effect entry.

### ObjectiveObserved

The generation additionally has a committed 10 Observe objective context.

### ObjectiveQualified

The generation additionally has a committed 10 Qualification objective context.

Different tiers remain distinct. 11 does not pretend that a POST-only observation has objective or physically qualified counterfactual evidence.

## Typed pair identity

The trajectory key is derived from the existing typed `AshBpDkBridgePairIdentity` and binds:

```text
parameter id
canonical parameter index
pair ordinal
lhs tile ordinal
rhs tile ordinal
adjacency / orientation
```

No TensorCube ID string parsing or inferred topology is introduced.

The pair identity remains the 03A/04/05 typed identity authority.

## Pair transition history comes from 07

11 intentionally uses 07 pair POST history as the transition source, not 09 alone.

Reason:

```text
09 contains actual-vs-Local causal entries only for actually fused causal pairs.
```

A long-horizon planner trajectory must also see:

```text
SoftFission
HardFission
PolicyRebaselineLocal
CooldownLocal
```

which are represented in 07 actual POST transition history even when no current Fusion counterfactual exists.

11 therefore preserves the complete actual transition sequence:

```text
NewFusion
RetainedFusion
SoftFission
HardFission
PolicyRebaselineLocal
CooldownLocal
```

## Actual execution-kind validation

For `NewFusion` and `RetainedFusion`, the pair sample must carry an actual fused execution kind matching typed adjacency.

For:

```text
SoftFission
HardFission
PolicyRebaselineLocal
CooldownLocal
```

actual execution must be Local.

A contradictory transition/execution combination fails closed.

## Pair PRE evidence

When available from the committed 07 pair lineage, 11 carries:

```text
03A signed gradient cosine
03B I_BRIDGE
03B M_BRIDGE
03B DeltaK_BRIDGE_PRE raw
03B DeltaK_BRIDGE_PRE smoothed
```

All signs and optional-value semantics are preserved. No `abs()` rewrite and no fabricated zero is introduced.

## Pair counterfactual-update evidence

When an exact matching 09 pair exists, 11 binds descriptive counterfactual-update evidence including:

```text
mean weight-effect RMS
mean momentum-effect RMS
mean orthogonal-update-effect RMS

weight pair-coupling delta
momentum pair-coupling delta
orthogonal-update pair-coupling delta

09 physical witness tier
```

The effect evidence is admitted only with a counterfactual witness tier. A pair sample cannot carry counterfactual-effect RMS while claiming no counterfactual witness.

11 does not recompute 08B/09 vectors or execute Local/Fused Muon again.

## Generation-level objective context

When a current committed 10 entry exists, 11 stores one `AshBpDkFusionTrajectoryObjectiveContext` for the generation.

It binds:

```text
10 probe receipt identity
10 objective direction
10 probe mode / qualification level
J_source
J_actual
J_local
actual_minus_source
local_minus_source
actual_minus_local
```

This context belongs to the whole current fused intervention set, not to one pair.

Preference labels are scoped accordingly:

```text
ActualPreferredOnObservedProbe
LocalPreferredOnObservedProbe
EqualOnObservedProbe
```

The label means only which whole-step candidate was preferred by the observed probe objective under its explicit direction.

It is not named `FusionBeneficial`, `FusionHarmful`, or a success-rate authority.

## Exact zero semantics

For objective preference, exact zero remains:

```text
EqualOnObservedProbe
```

11 does not invent an epsilon-zero band.

Optional counterfactual metrics also preserve upstream undefined/absent semantics rather than replacing missing evidence with zero.

## Fusion lifetime

Per pair, the rolling state distinguishes:

```text
observed fused-generation streak
contiguous optimizer-generation fused streak
```

These are intentionally different.

Example:

```text
generation 100: RetainedFusion observed
generation 101: observation unavailable
generation 102: RetainedFusion observed
```

11 may state that Fusion was observed at 100 and 102. It does **not** infer that Fusion remained continuously active through 101.

The contiguous streak therefore resets across optimizer-generation gaps while broader observed history remains intact.

## State flips and oscillation

11 tracks fused-vs-local transition-class flips rather than treating every exact transition label change as an oscillation.

For example:

```text
NewFusion -> RetainedFusion
```

does not count as a fused/local state flip.

Transitions such as:

```text
Fused -> Fission/Local
Local/Cooldown -> Fusion
```

can increase state-flip history.

Diagnostic health can expose `OscillatoryObserved` when the explicit diagnostic reversal threshold is reached. This classification has no planner mutation authority.

## Fission and cooldown separation

Pair rolling state separately counts:

```text
Fusion entries
Retained Fusion observations
Soft Fission
Hard Fission
Policy rebaseline
Cooldown observations
```

Soft and Hard Fission are not collapsed because their upstream semantic causes differ.

## Objective sign persistence

The generation-global objective rolling state tracks preference and exact signed objective difference across observed objective generations.

It records information such as:

```text
Actual-preferred observed-probe count
Local-preferred observed-probe count
Equal observed-probe count
current preference streak
objective sign reversals
```

Because the objective is generation-global, these counts belong to the objective context and are not copied into every pair as if independent pair outcomes.

## Explicit observation gaps

11 never interpolates missing evidence.

Forbidden:

```text
zero fill
last value carry-forward as a sample
linear interpolation
nearest-generation matching
```

The head records last observed generation identity, and generation entries preserve previous-observed generation lineage.

A generation without an 11 observation carries the committed 11 head forward unchanged.

No fake trajectory sample is generated.

## Upstream head-only semantics

07, 09 and 10 may legitimately carry a committed head into a candidate checkpoint without producing a current-generation entry.

Therefore 11 treats:

```text
entry absent + head present
```

as a valid current-generation observation gap/carry-forward state.

It treats:

```text
entry present + head absent
```

as split authority and fails closed.

This is critical for 09/10 because counterfactual and objective observation are intentionally sparse.

## Rolling windows

11 uses fixed diagnostic observed-sample windows:

```text
8
32
128
```

with a bounded rolling capacity of 128 objective-context samples.

These are diagnostic aggregation windows, not optimizer thresholds.

Window metadata includes the actual observed sample count and generation span rather than pretending that an 8-sample window necessarily means eight contiguous optimizer generations.

## Bounded memory authority

11 does not retain unbounded full trajectory history in RAM.

Runtime state is compact and bounded by:

```text
current typed pair states
bounded generation-global objective rolling samples
running counters/statistics
active segment identity
previous trajectory head
```

Historical authority is represented through immutable generation entries / sidecars and hash-chain identity rather than a forever-growing in-memory vector.

## Running statistics

Pair and generation aggregates maintain bounded descriptive statistics such as:

```text
count
sum
sum of squares
min
max
mean
```

for finite observed values.

The numerical summaries are views over canonical observations. They do not replace the pair/generation receipt identities.

## Correlation observation

11 can produce descriptive correlations such as:

```text
PRE Delta-K vs whole-generation objective context
mean counterfactual weight-effect RMS vs whole-generation objective context
```

using only paired observed samples within the current bounded context.

Every correlation carries:

```text
paired_sample_count
missing_count
```

If fewer than two paired samples exist, or variance is zero, correlation remains unavailable.

Correlation is diagnostic only:

```text
correlation != causation
correlation != planner threshold proof
```

Most importantly, because 10 objective evidence is whole-step fused-set evidence, correlation with a pair PRE value is co-observation in the same generation, not a claim that the individual pair caused the whole objective delta.

## Segment boundaries

11 does not silently aggregate semantically different lineages into one window.

The active segment identity binds sets/identities including:

```text
planner/policy lineage
capability lineage
objective identity when observed
```

Changes produce an explicit segment boundary.

Intermittent absence of a 10 objective entry does **not** itself create an objective-identity boundary; the prior objective identity is preserved across an unobserved generation rather than resetting the segment merely because probing was sparse.

Policy/capability/objective segment identity is explicit in the trajectory head.

## Capability and policy boundaries

11 records boundary telemetry for:

```text
capability-set changes
policy-set changes
objective-identity changes
```

Numerical windows are not silently merged across those boundaries as if the experimental conditions were identical.

## Generation aggregate

Each observed 11 generation stores a compact aggregate including:

```text
pair sample count
actually fused pair count
counterfactual-observed pair count
mean PRE Delta-K when available
mean weight-effect RMS when available
mean momentum-effect RMS when available
mean orthogonal-effect RMS when available
```

All optional aggregate numerical fields must be finite and semantically valid.

This aggregate is descriptive and not a Fusion score.

## Diagnostic health

11 exposes only diagnostic labels:

```text
InsufficientEvidence
StableObserved
OscillatoryObserved
RepeatedActualNotPreferredOnProbe
MixedObserved
```

`InsufficientEvidence` is the correct state when the explicit minimum evidence count is not met.

The labels are review surfaces only. They do not feed 05, change thresholds, choose a candidate, or mutate Delta-K.

`RepeatedActualNotPreferredOnProbe` means the actual whole-step candidate repeatedly was not preferred by the observed one-step probe under the current objective contract. It does not mean training is globally worse.

## Trajectory ledger authority

11 owns a separate ledger:

```text
bp_dk_fusion_objective_long_horizon_trajectory_entry.json
bp_dk_fusion_objective_long_horizon_trajectory_head.json
```

It is distinct from:

```text
07 actual POST ledger
09 counterfactual-effect ledger
10 objective-probe ledger
```

The trajectory head stores at minimum:

```text
schema revision
trajectory sequence
last observed training/optimizer/BP generation
active segment sequence/digest
active policy-set digest
active capability-set digest
active objective digest
segment boundary count
bounded typed pair states
generation-global objective rolling state
rolling-state digest
ledger-head digest
```

## Hash chain

Observed 11 generations advance a canonical trajectory hash chain:

```text
TrajectoryHead_N
=
SHA256(
  previous trajectory head
  + canonical generation trajectory entry
)
```

Canonical semantic serialization, not pretty-printed JSON whitespace, is authority.

## Persistence ordering

The existing candidate persistence dependency is extended as:

```text
05 planner
-> 07 actual POST
-> 09 counterfactual-effect ledger
-> 10 objective-probe ledger
-> 11 trajectory ledger
```

11 consumes the already-persisted candidate upstream evidence.

If 11 is disabled or the selected trajectory mode has no current observation, the existing committed trajectory head is carried forward without creating a fake generation entry.

## Commit ordering

The in-memory commit chain is extended as:

```text
03B temporal state
-> 05 planner state
-> 07 actual POST head
-> 09 causal head
-> 10 objective-probe head
-> 11 trajectory head
```

Before promoting the pending 11 head, 11 verifies all upstream committed heads that are actually referenced by the pending trajectory entry.

A trajectory entry that references an uncommitted/mismatching upstream history fails closed and increments the upstream-commit-missing diagnostic surface.

## Abort semantics

`record_step_abort()` now aborts pending 11 state after upstream pending state.

An aborted actual training step therefore cannot become a committed 11 trajectory sample.

There is no last-good sample substitution and no record of an uncommitted candidate as if it were training history.

## Restore and legacy genesis

Pre-11 checkpoints without an 11 head enter an explicit deterministic legacy genesis.

11 does not reconstruct or invent historical 03B/05/07/09/10 trajectory samples that were never persisted by 11.

A restored trajectory head must not reference a future training or optimizer generation.

`entry present + head absent` is split authority and fails closed.

## No new physical compute

11 adds no:

```text
GPU dispatch
model forward
objective forward
backward
Local/Fused Muon execution
gradient readback
gradient GPU access
```

It consumes committed evidence only.

The required semantic counters remain zero:

```text
trajectory_gpu_dispatch_count = 0
trajectory_forward_count = 0
trajectory_gradient_access_count = 0
trajectory_planner_feedback_count = 0
trajectory_policy_mutation_count = 0
trajectory_benefit_claim_count = 0
```

## Telemetry

11 surfaces diagnostic telemetry including:

```text
generation-entry count
pair-sample count
POST-observed count
counterfactual-observed count
objective-observed count
objective-qualified count
Fusion-entry count
Retained-Fusion count
Soft-Fission count
Hard-Fission count
Cooldown count
objective-sign reversal count
state-flip count
capability-boundary count
policy-boundary count
objective-boundary count
insufficient-evidence count
state-commit count
state-abort count
legacy-genesis count
restore-head count
upstream-commit-missing count
```

Objective reversal/state-flip telemetry is incremented by current-generation deltas rather than repeatedly re-adding historical cumulative counts.

## Parent source preservation

11 preserves the 10/09/07 observation and physical execution mathematics and the Fusion backend.

Parent byte anchors validated by the new static gate include:

```text
10 core
63d56931d08c82cd15581233f49084e783c7a1473c30af61eb3c4952cca75133

10 base
c9e093c1d6f9ef402e8e45f1c3eb47922016ef964d5242fdf9994bf5a0aa00a8

09 core
6733f1b585d914b381470c37df9b8cb79a8513f43189729af2a863fd44dad888

09 base
c30352288a69605d39c121d0b2ec681544e25c81004081bd228cabcc3ef4c049

07 core
1683c07483f6fab106cb22cd63019cdf2a0d5a3f36389756ae4b51fbf4e78f59

07 base
3597593ac60c29813a477a28c037486acccc933aa20f8335e3af177aeae7bfc7

05 fused backend
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d

05 serial fused WGSL
4a84858058737977d8636491f58301d902b358c2c0c1d26623cf2632bf3bd6d6

05 ExactSubgroup32 fused WGSL
2ab9700df95b67fd4bd337392a8e6aef99195e1ae29f8e381cfd9d0e1c61e369
```

## Changed files

The 11 overlay contains exactly seven files relative to the 10 parent:

```text
crates/ash_core/src/fusion_objective_long_horizon_trajectory.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_fusion_objective_long_horizon_trajectory.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_objective_long_horizon_trajectory_11_static.py
```

No WGPU/Fusion/Muon shader or backend file is modified.

## Static validation

New gate:

```text
validate_ash_bp_dk_fusion_objective_long_horizon_trajectory_11_static.py
145/145 PASS
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
11 Long-Horizon Trajectory                      145/145 PASS
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

11 is appended after 10 in the existing CF1 static-validator chain without rewriting earlier validator-closure semantics.

## Packaging

The bake is delivered as:

```text
full-body bake: 19,004,472 bytes / 7,151 files
overlay bake:       66,163 bytes / exactly 7 files
```

Both ZIP archives pass archive integrity testing.

The archives contain zero:

```text
*.sha256
target directories
__pycache__
generated artifact directories
generated report directories
generated manifest directories
```

## Bake-environment boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU runtime/adapter
```

Therefore the following are **not** claimed by this bake:

```text
Rust compile success
live 11 persistence/commit success
live checkpoint/restart trajectory parity
actual multi-generation trajectory statistics
actual long-horizon health classification
actual correlation values
```

Correct status after baking is:

```text
11_LONG_HORIZON_TRAJECTORY_SOURCE_PATH_WIRED
11_BOUNDED_ROLLING_STATE_WIRED
11_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_00_10_AND_LOCAL_MUON_STATIC_LINEAGE_PASS
USER_LOCAL_LONG_HORIZON_RUNTIME_EXECUTION_UNVERIFIED
```

## Required user-local gates

Before runtime promotion:

```text
cargo fmt --check
cargo check
CF1 reaches 11

run multiple committed Fusion/Fission generations
verify 07 transition history is captured
verify 09 causal update evidence enriches matching fused pairs only
verify 10 whole-step objective remains generation-global context
verify objective is not copied into per-pair causal fields

verify DECISION_AND_UPDATE works with sparse/no 10 observations
verify OBJECTIVE_OBSERVED carries head across missing 10 generations
verify entry-absent/head-present upstream sidecars are treated as gaps
verify entry-present/head-absent sidecars fail closed

verify contiguous Fusion lifetime resets across generation gaps
verify observed Fusion history remains distinct from contiguous lifetime
verify Soft/Hard Fission and Cooldown counts remain separate

verify 8/32/128 windows remain bounded
verify capability/policy/objective boundaries segment the trajectory
verify intermittent objective absence does not create a false objective boundary

verify commit order 07 -> 09 -> 10 -> 11
verify failed actual step does not advance 11 head
verify checkpoint/restart restores identical rolling-state/head identity

verify 11 adds zero forward/GPU/gradient/Muon execution
verify 11 produces zero planner feedback/policy mutation
```

## Claim boundary after runtime evidence

With real multi-generation 11 evidence, the supported claims are descriptive, for example:

```text
This typed Fusion pair was observed fused for these generations,
under these explicit gaps and segment boundaries;
it later Soft/Hard-fissioned or entered cooldown as recorded;
its PRE Delta-K and actual-vs-Local update divergence followed the recorded trajectory;
and on generations with a 10 probe, the whole fused intervention set had the recorded objective preference/context.
```

Still forbidden:

```text
This individual pair caused the whole-step objective improvement.
Fusion is globally beneficial.
Fusion generalizes better.
The planner should automatically change thresholds.
The observed correlation proves a Delta-K threshold.
```

## Natural successor

After 11 accumulates runtime evidence, the next policy-facing revision is:

```text
ASH-BP-DK-FUSION-POLICY-CALIBRATION-RECOMMENDATION-12
```

12 may consume:

```text
03B PRE evidence
05 decision history
07 actual POST history
09 causal update divergence
10 objective-probe context
11 bounded long-horizon trajectory/health
```

and emit a **candidate policy recommendation** only.

The recommended control chain remains:

```text
11 evidence
-> 12 recommendation
-> 13 operator review gate
-> explicit human-approved promotion
```

No 11 observation directly mutates 05 policy.

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_11

10_DIRECT_PARENT
03B_PRE_EVIDENCE_BOUND
05_ACTUAL_TRANSITION_HISTORY_BOUND
07_ACTUAL_POST_HISTORY_BOUND
09_COUNTERFACTUAL_UPDATE_HISTORY_OPTIONALLY_BOUND
10_OBJECTIVE_CONTEXT_OPTIONALLY_BOUND

TYPED_PAIR_IDENTITY_ONLY
NO_PAIR_ID_STRING_PARSING

PAIR_PRE_AND_UPDATE_TRAJECTORY_SEPARATE_FROM_GENERATION_OBJECTIVE_CONTEXT
NO_PAIR_LEVEL_OBJECTIVE_ATTRIBUTION_FROM_WHOLE_STEP_PROBE

DECISION_AND_UPDATE_MODE
OBJECTIVE_OBSERVED_MODE
EXPLICIT_OBSERVATION_TIERS
EXPLICIT_OBSERVATION_GAPS

07_TRANSITION_HISTORY_DRIVES_FUSION_FISSION_COOLDOWN
NEW_FUSION_RETAINED_FUSION_SOFT_FISSION_HARD_FISSION_SEPARATED
POLICY_REBASELINE_AND_COOLDOWN_PRESERVED

OBSERVED_FUSION_LIFETIME_TRACKED
CONTIGUOUS_FUSION_LIFETIME_TRACKED_SEPARATELY
NO_GAP_CONTINUITY_INFERENCE

OBJECTIVE_PREFERENCE_IS_GENERATION_GLOBAL
OBJECTIVE_SIGN_PERSISTENCE_TRACKED
OBJECTIVE_SIGN_REVERSAL_TRACKED
NO_GLOBAL_BENEFIT_LABEL

COUNTERFACTUAL_WEIGHT_EFFECT_TRAJECTORY
COUNTERFACTUAL_MOMENTUM_EFFECT_TRAJECTORY
COUNTERFACTUAL_ORTHOGONAL_EFFECT_TRAJECTORY
PAIR_COUPLING_DELTA_TRAJECTORY

PRE_GRADIENT_COSINE_TRAJECTORY
PRE_BRIDGE_I_M_DELTAK_TRAJECTORY

CORRELATION_DIAGNOSTIC_ONLY
PAIRED_SAMPLE_COUNT_REQUIRED
MISSING_SAMPLE_COUNT_REQUIRED
CORRELATION_IS_NOT_CAUSATION

WINDOWS_8_32_128
ROLLING_CAPACITY_128
BOUNDED_RUNTIME_STATE
NO_UNBOUNDED_HISTORY_RAM

HEAD_ONLY_UPSTREAM_STATE_IS_VALID_OBSERVATION_GAP
ENTRY_WITHOUT_HEAD_FAILS_CLOSED
NO_ZERO_FILL
NO_INTERPOLATION
NO_RETROACTIVE_SILENT_FILL

POLICY_BOUNDARY_SEGMENTED
CAPABILITY_BOUNDARY_SEGMENTED
OBJECTIVE_IDENTITY_BOUNDARY_SEGMENTED
INTERMITTENT_OBJECTIVE_ABSENCE_DOES_NOT_FAKE_BOUNDARY

DIAGNOSTIC_HEALTH_ONLY
INSUFFICIENT_EVIDENCE_EXPLICIT
NO_AUTOMATIC_PLANNER_FEEDBACK
NO_AUTOMATIC_THRESHOLD_CALIBRATION

SEPARATE_11_TRAJECTORY_LEDGER
HASH_CHAINED_TRAJECTORY_HEAD
PERSIST_ORDER_07_09_10_11
COMMIT_ORDER_07_09_10_11
ABORTED_STEP_DOES_NOT_ADVANCE_11_HEAD

NO_NEW_FORWARD
NO_NEW_BACKWARD
NO_NEW_COUNTERFACTUAL_EXECUTION
NO_NEW_GRADIENT_ACCESS
NO_NEW_MUON_DISPATCH

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY
NO_NEW_WGSL
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_11_145_OF_145_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_LONG_HORIZON_RUNTIME_EXECUTION_UNVERIFIED
```
