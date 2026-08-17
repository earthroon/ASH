# ASH-BP-DK-ACTIVE-FUSION-COUNTERFACTUAL-EFFECT-LEDGER-09

## Status

```text
Patch ID: ASH-BP-DK-ACTIVE-FUSION-COUNTERFACTUAL-EFFECT-LEDGER-09
Direct parent: ASH-BP-DK-ACTIVE-FUSION-SAME-SOURCE-LOCAL-COUNTERFACTUAL-PHYSICAL-EXECUTION-QUALIFICATION-08B-R1
Required upstream: 08B / 08A / 07 / 06 / 05 / 04 / 03B / 03A / 02 / 01 / 00
Purpose: bind committed actual POST history to physically witnessed same-source Local counterfactual evidence in a separate causal update-effect ledger
New counterfactual compute: none
New WGPU dispatch: none
New gradient access/readback: none
New Muon mathematics: none
New Delta-K formula: none
New Fusion policy: none
Precision authority: unchanged
Residency authority: unchanged
Performance promotion: forbidden
```

## Central SSOT

09 does not recompute either branch.

```text
07 actual POST receipt / committed generation ledger
+
08B same-source Local counterfactual receipt
+
08B-R1 physically qualified execution receipt
        -> exact parameter join
        -> exact actual-vs-Local causal update evidence
        -> separate generation-level causal ledger
```

Authority separation remains explicit:

```text
05 = actual Fusion/Fission decision
07 = actual committed POST history
08B = same-source Local derived counterfactual
08B-R1 = physical witness for that counterfactual
09 = committed-generation causal comparison history
```

09 is descriptive update-level causal evidence. It does not classify Fusion as beneficial or harmful.

## Runtime mode

09 introduces:

```text
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_EFFECT_LEDGER_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_EFFECT_LEDGER_MODE=RECORD_OBSERVED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_EFFECT_LEDGER_MODE=REQUIRE_QUALIFIED
```

Default is `DISABLED`.

### RECORD_OBSERVED

Requires an active 08B counterfactual mode and 08B-R1 physical evidence output. It accepts either:

```text
PhysicalObserveQualified
PhysicalQualificationQualified
```

### REQUIRE_QUALIFIED

Requires:

```text
08B mode = QUALIFICATION
08B-R1 state = PhysicalQualificationQualified
```

There is no silent downgrade from `REQUIRE_QUALIFIED` to `RECORD_OBSERVED`.

## Physical receipt mandatory

09 never promotes a source-wired but physically unwitnessed counterfactual.

A parameter entry is created only from a validated `AshBpDkCounterfactualPhysicalExecutionReceipt` emitted by 08B-R1. The accepted witness tier is stored as:

```text
ObserveWitnessed
QualificationWitnessed
```

Source-contract-only, unsupported, insufficient-evidence, replay-mismatch, source-mismatch, or state-mutation states are inadmissible.

## Exact parameter join

`build_counterfactual_effect_parameter_entry()` validates exact identity between the 07 actual POST receipt and the nested 08B/08B-R1 receipt.

Required exact equality includes:

```text
parameter_id
canonical_parameter_index
parameter_revision
optimizer_generation
bp_generation

graph_topology_digest
graph_evidence_digest
05 plan_digest
05 planner_policy_digest

07 actual_post_receipt_digest
actual candidate weight digest
actual candidate momentum digest
actual orthogonal-update digest

08B source capsule identity
08B-R1 physical generation identity
```

Join failure is fail-closed. There is no nearest-generation, name-only, or partial-digest repair.

Explicit surfaces include:

```text
ASH_BP_DK_COUNTERFACTUAL_EFFECT_JOIN_PARAMETER_MISMATCH
ASH_BP_DK_COUNTERFACTUAL_EFFECT_JOIN_PLAN_MISMATCH
ASH_BP_DK_COUNTERFACTUAL_EFFECT_JOIN_POST_RECEIPT_MISMATCH
ASH_BP_DK_COUNTERFACTUAL_EFFECT_JOIN_ACTUAL_CANDIDATE_MISMATCH
ASH_BP_DK_COUNTERFACTUAL_EFFECT_JOIN_PHYSICAL_LINEAGE_MISMATCH
```

## No counterfactual re-execution

09 performs no new Local or Fused execution.

It does not import or call:

```text
RawWgpuBufferLease
TensorCubeLocalMuonBatchExecutor
TensorCubeFusedPairMuonExecutor
execute_with_norm_path
```

Therefore:

```text
09 GPU dispatch count = 0
09 gradient D2H bytes = 0
```

The 08B exact effect evidence is consumed as authority rather than re-derived from source/candidate tensors.

## Canonical causal tile evidence

The canonical unit remains one 16x16 TensorCube.

For every actually fused tile, 09 binds the 08B evidence:

```text
Fusion-effect weight RMS
Fusion-effect momentum RMS
Fusion-effect orthogonal-update RMS

actual-vs-Local weight direction cosine
actual-vs-Local momentum direction cosine
actual-vs-Local orthogonal direction cosine

actual/Local weight magnitude ratio
actual/Local momentum magnitude ratio
actual/Local orthogonal magnitude ratio
```

Zero-norm and zero-Local-baseline semantics are preserved from 08B:

```text
UndefinedZeroNorm
UndefinedZeroBaseline
```

No epsilon denominator repair is introduced.

## Pair causal evidence

09 records only pairs that were actually executed as:

```text
FusedRight
FusedDown
```

The matching 07 pair must be an actual Fusion transition:

```text
NewFusion
RetainedFusion
```

Fissioned/Plain-Local pairs are not silently converted into Fusion counterfactual entries.

Each pair binds:

```text
03A signed PRE gradient cosine
03B PRE I_BRIDGE
03B PRE M_BRIDGE
03B PRE DeltaK_BRIDGE raw
03B PRE DeltaK_BRIDGE smoothed

weight pair-coupling delta
momentum pair-coupling delta
orthogonal-update pair-coupling delta
```

Signed relationships remain signed. No `abs()` benefit conversion is introduced.

## Core schemas

09 adds:

```text
AshBpDkCounterfactualEffectTileEvidence
AshBpDkCounterfactualEffectPairEvidence
AshBpDkCounterfactualEffectParameterEntry
AshBpDkCounterfactualEffectGenerationEntry
AshBpDkCounterfactualEffectLedgerHead
```

All numerical evidence is canonically hashed using exact F32 `to_bits().to_le_bytes()` representation and explicit presence tags for optional values.

## Parameter entry identity

`AshBpDkCounterfactualEffectParameterEntry` binds:

```text
parameter/generation identity
04 graph topology/evidence digests
05 plan/policy digests
07 actual POST receipt digest
08B-R1 physical execution digest
08B counterfactual receipt digest
08B source capsule digest
actual candidate weight/momentum/update digests
08A capability digest
08A qualification digest
08B-R1 current-device contract digest
physical witness tier
ordered actual fused-pair causal evidence
entry digest
```

The parameter entry is derived evidence only and has no model/optimizer mutation authority.

## Generation ledger

09 owns a ledger separate from 07.

```text
07:
bp_dk_active_fusion_post_update_ledger_entry.json
bp_dk_active_fusion_post_update_ledger_head.json

09:
bp_dk_counterfactual_effect_ledger_entry.json
bp_dk_counterfactual_effect_ledger_head.json
```

The two ledgers are intentionally not merged because actual history and derived physically witnessed what-if comparison have different epistemic roles.

## Causal ledger sequence and observation gaps

Counterfactual observation may be disabled for some training generations. Therefore 09 does not require every optimizer generation to advance the causal ledger.

The causal head stores:

```text
causal_ledger_sequence
last_observed_training_generation
last_observed_optimizer_generation
last_observed_bp_generation
ledger_head_digest
```

Each generation entry additionally stores:

```text
previous_observed_optimizer_generation
```

Example:

```text
optimizer generation 100 = observed
optimizer generation 101 = counterfactual disabled
optimizer generation 102 = observed
```

is valid. The 102 entry explicitly points to 100 as the previous observed optimizer generation.

No fake zero-effect generation is created for 101, and no silent historical backfill occurs.

## Hash chain

For an observed generation:

```text
CausalHead_N
=
SHA256(
  previous causal head digest
  + canonical causal generation entry digest
)
```

The generation entry binds:

```text
training generation
optimizer generation
BP generation
causal ledger sequence
previous observed optimizer generation
07 generation-entry digest
07 target ledger-head digest
previous 09 causal-head digest
ordered parameter entries
```

## Candidate persistence ordering

The production candidate transaction is extended in this exact order:

```text
persist 05 Fusion/Fission planner state
persist 07 actual POST ledger
persist/carry-forward 09 causal ledger
```

09 finalization reads the just-written 07 candidate entry/head and validates:

```text
07 generation entry schema/digest
07 head schema/digest
07 generation identity
07 persisted parameter receipt digest for every 09 parameter entry
```

The 09 generation entry therefore cannot be finalized against a different 07 candidate generation.

## Actual commit before causal-head promotion

`record_step_commit()` retains the parent ordering and extends it as:

```text
03B temporal commit
05 planner commit
07 actual POST ledger commit
09 causal-effect ledger commit
```

Before 09 in-memory head promotion, `commit_pending()` verifies that the now-committed 07 head:

```text
last_optimizer_generation == target optimizer generation
ledger_head_digest == 09 entry actual_07_ledger_head_digest
```

Thus 09 cannot become committed causal history before the actual 07 generation is committed.

If this check fails, `causal_ledger_actual_commit_missing_count` increments and the run fails closed.

## Abort semantics

`record_step_abort()` aborts pending 09 entries/head in addition to the existing upstream pending state.

An aborted actual step therefore leaves:

```text
09 committed causal head unchanged
```

No actual trajectory means no committed causal comparison history.

## Checkpoint/restart and legacy genesis

The 09 causal head is persisted into each candidate checkpoint, even when the current generation has no counterfactual observation. In a no-observation generation the committed causal head is simply carried forward unchanged.

A pre-09 checkpoint with no causal sidecar starts from explicit deterministic legacy genesis. It does not invent historical causal entries.

An entry sidecar without its head is explicit split authority and fails closed.

A restored causal head may reference an observed optimizer generation older than the current source generation because observation gaps are legal, but it may never reference a future source generation.

## Telemetry

09 surfaces:

```text
causal_ledger_generation_entry_count
causal_ledger_pair_count
causal_ledger_tile_count
causal_ledger_observe_receipt_count
causal_ledger_qualified_receipt_count
causal_ledger_join_mismatch_count
causal_ledger_missing_physical_receipt_count
causal_ledger_nonfinite_reject_count
causal_ledger_actual_commit_missing_count
causal_ledger_gradient_d2h_bytes
causal_ledger_gpu_dispatch_count
causal_ledger_planner_feedback_count
causal_ledger_policy_mutation_count
causal_ledger_benefit_claim_count
causal_ledger_state_commit_count
causal_ledger_state_abort_count
causal_ledger_legacy_genesis_count
causal_ledger_restore_head_count
```

09 itself owns no physical execution. Required hard-zero semantic surfaces are:

```text
causal_ledger_gradient_d2h_bytes = 0
causal_ledger_gpu_dispatch_count = 0
causal_ledger_planner_feedback_count = 0
causal_ledger_policy_mutation_count = 0
causal_ledger_benefit_claim_count = 0
```

Join/nonfinite failures are counted before fail-closed return. A causal commit attempted without the exact committed 07 target head increments the actual-commit-missing counter before failing.

## Parent preservation

09 byte-preserves the direct 08B-R1 implementation and upstream counterfactual/POST implementations.

Static parent anchors include:

```text
08B-R1 core
a7a72d0b94a682671c44d011b1985b3e65335af256519ccae3dcc1ec076fa267

08B-R1 base
0116c1cc160e6a561ccbd05b1b2126051104cc8b2b9ec4d12041284c3e0ab4fd

08B core
83c5705636159922adb8859026024fc6d0acfe1b15c09160daa76c8fcbb4ab39

08B base
e9f430d42fafcbf8ab047a361ec85d6f3556153bd79884e588afc15cb7437a2b

07 core
1683c07483f6fab106cb22cd63019cdf2a0d5a3f36389756ae4b51fbf4e78f59

07 base
3597593ac60c29813a477a28c037486acccc933aa20f8335e3af177aeae7bfc7

05 fused backend
cebba82183a627d5c7d4a464398b56e63f833fff3ecd6b4b37c9c5ace970bc1d
```

No 05 fused WGSL or backend path is altered by 09.

## Changed files

The 09 overlay contains exactly seven files:

```text
crates/ash_core/src/active_fusion_counterfactual_effect_ledger.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_active_fusion_counterfactual_effect_ledger.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_active_fusion_counterfactual_effect_ledger_09_static.py
```

No new WGSL, WGPU backend, counterfactual Local kernel, or Fusion kernel file is introduced.

## Static validation

New gate:

```text
validate_ash_bp_dk_active_fusion_counterfactual_effect_ledger_09_static.py
148/148 PASS
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

## Bake environment boundary

The bake environment does not contain:

```text
cargo
rustc
rustfmt
physical WGPU adapter/runtime
```

Therefore this bake does not claim:

```text
Rust compile success
actual user-local 09 runtime transaction success
actual 08B-R1 physical receipt generation
actual causal checkpoint/restart parity
actual causal head promotion on a live training generation
```

Current status is:

```text
09_CAUSAL_LEDGER_SOURCE_PATH_WIRED
09_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_07_08B_08B_R1_SOURCES_PRESERVED
USER_LOCAL_TRANSACTION_EXECUTION_UNVERIFIED
```

09 contains no new physical compute, but the actual transaction/restore behavior still requires a user-local Rust execution before physical/runtime promotion is claimed.

## Required user-local gates

```text
cargo fmt --check
cargo check
CF1 reaches 09

08B-R1 physical receipt exists for an actually fused parameter
07 actual POST receipt exact-joins the physical counterfactual receipt
09 parameter entry stages
07 candidate ledger entry/head persists first
09 generation entry/head persists second

successful active commit:
07 head commits first
09 head commits only after exact 07 committed-head verification

failed active commit:
09 pending state aborts
09 committed head unchanged

checkpoint restart:
09 head restores
observation gaps preserve previous observed generation
same observed evidence produces deterministic next causal entry/head

09 additional GPU dispatch count = 0
09 gradient D2H bytes = 0
09 planner/policy feedback = 0
```

## Claim boundary

With a committed 09 causal entry, the permitted claim is:

```text
For this committed generation and physically witnessed same-source Local counterfactual, actual Fusion changed the optimizer update by the recorded weight/momentum/orthogonal magnitude, direction, and pair-coupling differences.
```

Still forbidden:

```text
Fusion was better than Local.
Fusion reduced loss.
Fusion improves training quality.
Fusion thresholds are optimal.
```

## Natural successor

The next correctness revision is:

```text
ASH-BP-DK-FUSION-LOCAL-ONE-STEP-OBJECTIVE-PROBE-10
```

10 should evaluate the actual Fused candidate model and same-source Local counterfactual candidate model against the exact same evaluation microbatch/objective without committing the counterfactual model. That is the first stage where an objective-level effect can be observed.

## Bake seal

```text
BAKE_ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_EFFECT_LEDGER_09

08B_R1_DIRECT_PARENT
08B_R1_PHYSICAL_RECEIPT_REQUIRED
NO_UNWITNESSED_COUNTERFACTUAL_PROMOTION

07_ACTUAL_POST_RECEIPT_EXACT_JOIN
05_PLAN_EXACT_JOIN
ACTUAL_CANDIDATE_WEIGHT_DIGEST_EXACT_JOIN
ACTUAL_CANDIDATE_MOMENTUM_DIGEST_EXACT_JOIN
ACTUAL_ORTHOGONAL_UPDATE_DIGEST_EXACT_JOIN

08A_CAPABILITY_DIGEST_BOUND
08A_QUALIFICATION_DIGEST_BOUND
08B_R1_DEVICE_CONTRACT_DIGEST_BOUND
08B_R1_PHYSICAL_EXECUTION_DIGEST_BOUND

CANONICAL_16X16_CAUSAL_EFFECT_EVIDENCE
WEIGHT_EFFECT_RMS_BOUND
MOMENTUM_EFFECT_RMS_BOUND
ORTHOGONAL_EFFECT_RMS_BOUND
SIGNED_DIRECTION_COSINE_BOUND
MAGNITUDE_RATIO_BOUND
PAIR_COUPLING_DELTA_BOUND
ZERO_NORM_SEMANTICS_PRESERVED
ZERO_LOCAL_BASELINE_SEMANTICS_PRESERVED

03A_PRE_GRADIENT_RELATION_BOUND
03B_PRE_I_M_DELTAK_BOUND
NEW_OR_RETAINED_ACTUAL_FUSION_ONLY

SEPARATE_07_ACTUAL_LEDGER
SEPARATE_09_CAUSAL_LEDGER
CAUSAL_LEDGER_SEQUENCE
EXPLICIT_PREVIOUS_OBSERVED_OPTIMIZER_GENERATION
NO_FAKE_ZERO_EFFECT_GAP
NO_RETROACTIVE_SILENT_FILL

07_CANDIDATE_LEDGER_PERSISTED_BEFORE_09
07_COMMITTED_HEAD_VERIFIED_BEFORE_09_MEMORY_PROMOTION
ABORTED_STEP_DOES_NOT_ADVANCE_09_HEAD

NO_COUNTERFACTUAL_REEXECUTION
NO_GPU_DISPATCH_IN_09
NO_GRADIENT_ACCESS_IN_09

NO_FUSION_BENEFIT_CLASSIFICATION
NO_LOSS_CLAIM
NO_POLICY_FEEDBACK
NO_THRESHOLD_CALIBRATION
NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY
NO_NEW_MUON_MATHEMATICS

PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_09_148_OF_148_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_TRANSACTION_EXECUTION_UNVERIFIED
```
