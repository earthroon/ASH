# ASH-BP-DK-BRIDGE-TEMPORAL-COUPLING-OBSERVATION-03B

## Status

```text
Patch ID: ASH-BP-DK-BRIDGE-TEMPORAL-COUPLING-OBSERVATION-03B
Direct parent: ASH-BP-DK-BRIDGE-PAIR-EVIDENCE-SOURCE-CLOSURE-03A
Upstream: 02 Generation/Revision/Stale Seal, 01 Local BP-DK, 00 Observation Contract
Observation timing: BackpropPre, after 03A pair evidence and before Local Muon execution
Temporal state owner: canonical Bridge pair
Fusion authority: none
Physical fusion: none
Muon momentum mutation: none
Optimizer topology mutation: none
```

## Central SSOT

03B is the first Bridge-temporal Delta-K authority. It consumes only current, valid 03A pair evidence and adds pair-owned temporal history.

```text
current 03A pair evidence
+ previous committed state for the same typed canonical pair
+ independent Bridge policy
+ canonical Bridge topology digest
-> Bridge temporal observation
-> candidate next temporal state
```

The separation is mandatory:

```text
03A signed 256D gradient cosine = current spatial relation evidence
I_BRIDGE = temporal novelty of that signed relation
M_BRIDGE = joint local material pressure
DeltaK_BRIDGE_PRE = I_BRIDGE * M_BRIDGE^2
```

03B does not reinterpret the 03A cosine itself as Delta-K and does not create fusion permission.

## Pair-owned state

Temporal history belongs to the canonical pair rather than either endpoint TensorCube.

Typed key:

```text
canonical_parameter_index
pair_ordinal
adjacency Right|Down
lhs_tile_ordinal
rhs_tile_ordinal
```

No parameter-ID or TensorCube-ID string parsing is used to recover topology.

## Independent Bridge policy

R1 policy:

```text
cosine_ema_alpha = 0.125
delta_k_ema_alpha = 0.125
warmup_observation_count = 1
```

The numerical value matches the local observer's current R1 alpha but is owned by an independent Bridge policy revision and digest. A local-policy change does not silently become a Bridge-policy change.

## I_BRIDGE

Let:

```text
C_t = current 03A signed exact-256D gradient cosine
C_EMA_prev = previous committed signed cosine EMA
```

03B defines:

```text
cosine_delta = abs(C_t - C_EMA_prev)
I_BRIDGE = cosine_delta * 0.5
```

Therefore:

```text
0 <= I_BRIDGE <= 1
```

The previous cosine is not used as a denominator, avoiding artificial spikes near zero. Signed cosine history is preserved, so a +1 to -1 reversal produces maximal temporal novelty.

## M_BRIDGE

Let the two already-verified 03A endpoints provide local material terms:

```text
M_A
M_B
```

03B defines:

```text
M_BRIDGE^2 = M_A * M_B
M_BRIDGE = sqrt(M_A * M_B)
```

No arithmetic averaging of local material pressure is used. If either endpoint has weak material pressure, the joint material term is correspondingly weak.

## DeltaK_BRIDGE_PRE

For a Ready temporal sample:

```text
DeltaK_BRIDGE_PRE_raw
= I_BRIDGE * M_BRIDGE^2
= I_BRIDGE * M_A * M_B
```

Local endpoint I, M, and local Delta-K are retained as bound evidence only. They are not averaged or substituted into the Bridge formula.

## Signed cosine EMA

The previous committed EMA is always used for the current information calculation. EMA update occurs only after current formulas are evaluated.

```text
C_EMA_next
= alpha_C * C_t
+ (1 - alpha_C) * C_EMA_prev
```

R1:

```text
alpha_C = 0.125
```

Negative cosine is not absolutized or clamped into a positive relation.

## Delta-K EMA

First Ready temporal sample:

```text
DeltaK_smoothed = DeltaK_raw
```

Subsequent Ready samples:

```text
DeltaK_smoothed_next
= 0.125 * DeltaK_raw
+ 0.875 * DeltaK_smoothed_prev
```

## Cold start

The first valid 03A pair sample has no legitimate temporal predecessor.

Result:

```text
status = WARMING
candidate EMA cosine = current cosine
candidate sample_count = 1
candidate Delta-K EMA = none
```

No valid zero-valued Bridge Delta-K is fabricated.

## Generation continuity

Temporal comparison is valid only for contiguous BP generations.

```text
current.bp_generation
= previous.last_bp_generation + 1
```

Duplicate generation is a structural contradiction and fails closed.

Generation regression or parameter/optimizer lineage regression also fails closed.

A generation gap does not compare the new sample against stale history as though only one step elapsed. Instead:

```text
generation gap
-> explicit WARMING rebaseline
-> EMA cosine = current cosine
-> Delta-K EMA cleared
-> no Ready Bridge Delta-K for that generation
```

This covers gaps caused by missing/invalid 03A evidence, zero norm, nonfinite pair results, or unavailable Current endpoints.

## Semantic drift rewarm

A contiguous pair is explicitly re-warmed when any temporal semantic authority changes:

```text
Bridge source revision
Bridge observer revision
Bridge policy revision
Bridge policy digest
Bridge topology revision
Bridge topology digest
registry digest
optimizer routing digest
local observation policy digest
03A pair evidence schema revision
03A gradient source revision
```

No stale last-good reuse and no silent state migration is permitted.

## Bridge topology digest

03B computes a dedicated Bridge topology digest from the typed FirstCandidate registry and the complete canonical same-parameter Right/Down grid.

The digest includes deterministic canonical parameter/grid identity and ordered Right/Down edge identity. It does not alter FirstCandidate optimizer topology and does not use string parsing.

```text
optimizer topology authority != Bridge observation topology authority
```

## Candidate state before commit

03B separates observation from temporal-state durability.

```text
committed temporal state
+ current 03A evidence
-> current Bridge observation
+ pending candidate temporal state
```

The PRE observer does not immediately overwrite committed temporal history.

Implementation uses separate ordered maps for committed and pending pair state and binds pending state to one optimizer/BP generation.

Advancing into a different generation while a prior generation remains uncommitted fails closed.

## Whole-step commit boundary

The scheduler writes a candidate temporal snapshot into the candidate transaction directory, then commits the model active state. Only after `commit_active_state(...)` succeeds and the staging guard is marked committed does the in-memory Bridge temporal state advance.

```text
persist candidate snapshot
-> commit_active_state
-> staging committed
-> record_step_commit()
-> pending temporal state becomes committed
```

If `commit_active_state(...)` fails, `record_step_abort(target_step)` clears pending temporal state before the error propagates.

Therefore:

```text
COMPUTE TEMPORAL CANDIDATE != COMMIT TEMPORAL STATE
```

## Checkpoint authority

03B introduces runtime sidecars:

```text
bp_dk_bridge_temporal_state_manifest.json
bp_dk_bridge_temporal_state.json
```

The payload contains only the candidate committed-state image: current committed state overlaid with this generation's pending candidates. Pending state is never promoted in memory merely because the candidate snapshot was written.

Snapshot ordering is deterministic by the typed pair key. Payload length, state count, and SHA-256 are verified on restore.

A resume checkpoint with both valid 03B files restores pair history. A legacy checkpoint with neither 03B file explicitly cold-starts Bridge temporal history. Split sidecars or corrupt claimed 03B payload fail closed.

## Current observation surfaces

The production runtime exposes current-generation:

```text
current_bridge_temporal_observations()
current_bridge_temporal_warming_receipts()
```

These are current evidence surfaces for later shadow consumers. They are not fusion decisions and do not imply durable state has already committed.

## No fusion authority

03B does not define:

```text
fusion threshold
cosine threshold
Delta-K threshold
Fuse
Fission
Cooldown
connected components
logical fused TensorCube domain
physical fused TensorCube domain
```

It does not bind or mutate Muon momentum, candidate weights, Adam state, Newton-Schulz geometry, precision policy, residency policy, or optimizer routing.

Mandatory zero authorities remain enforced in production receipts:

```text
bridge_temporal_stale_state_reuse_count = 0
bridge_temporal_last_good_fallback_count = 0
bridge_temporal_fusion_decision_count = 0
bridge_temporal_physical_fusion_count = 0
bridge_temporal_muon_momentum_mutation_count = 0
bridge_temporal_optimizer_topology_mutation_count = 0
```

The 03A `bridge_delta_k_claim_count` remains zero because 03A itself still makes no Delta-K claim. 03B owns its new temporal Delta-K authority separately.

## Changed files

The 03B code overlay contains exactly eight changed/new implementation files:

```text
crates/ash_core/src/delta_k_bridge_temporal_observation.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_bridge_temporal_observation.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_bridge_temporal_coupling_observation_03b_static.py
```

No generated markdown report, artifact JSON, manifest directory, report directory, or `*.sha256` sidecar is required in the baked code ZIP.

## Validation

New static gate:

```text
validate_ash_bp_dk_bridge_temporal_coupling_observation_03b_static.py
157/157 PASS
```

Revalidated parent gates in the bake environment:

```text
BP-DK contract 00                                      149/149 PASS
BP-DK local observation 01                             134/134 PASS
BP-DK stale observation seal 02                        243/243 PASS
BP-DK Bridge pair evidence 03A                         148/148 PASS
Local Muon optimizer                                   101/101 PASS
FirstCandidate registry                                 97/97 PASS
Local Muon multi-tile batch                             61/61 PASS
Local Muon production callsite                          63/63 PASS
Muon registry canonical loader repair                   38/38 PASS
Muon ExactSubgroup32 norm                              128/128 PASS
Muon X PAD17                                            52/52 PASS
```

03B is appended to the existing CF1 static validator chain.

## Physical execution boundary

The bake environment does not provide `cargo`, `rustc`, `rustfmt`, or a physical WGPU runtime. Therefore this bake makes no local Rust compile, Cargo test, or physical GPU execution claim.

User-local physical verification remains required for:

```text
cargo fmt / cargo check
CF1 full compile chain
cold-start -> second-generation Ready transition
generation-gap rewarm
policy/topology drift rewarm
failed commit abort parity
checkpoint/restart parity
03B ON/OFF Local Muon candidate parity
```

Static evidence is sufficient for source-contract promotion, not for claiming physical execution success.

## Natural successor

```text
ASH-BP-DK-FUSION-CANDIDATE-GRAPH-04
```

04 may consume:

```text
VerifiedCurrent Local BP-DK
+ current 03A pair evidence
+ Ready 03B DeltaK_BRIDGE_PRE
```

but should still produce graph/shadow evidence only. Physical fusion remains later.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_BRIDGE_TEMPORAL_COUPLING_OBSERVATION_03B

03A_VERIFIED_PAIR_EVIDENCE_ONLY
PAIR_OWNED_TEMPORAL_STATE
SIGNED_COSINE_HISTORY_PRESERVED

I_BRIDGE_IS_TEMPORAL_COUPLING_NOVELTY
I_BRIDGE_BOUNDED_ZERO_TO_ONE
M_BRIDGE_IS_JOINT_LOCAL_MATERIAL_GEOMEAN
DELTAK_BRIDGE_PRE_EQUALS_I_TIMES_M_SQUARED

COLD_START_IS_WARMING
GENERATION_GAP_IS_REWARMING
SEMANTIC_DRIFT_IS_REWARMING
NO_STALE_LAST_GOOD
NO_FAKE_ZERO_DELTAK

TEMPORAL_CANDIDATE_SEPARATE_FROM_COMMITTED_STATE
OPTIMIZER_ACTIVE_COMMIT_PRECEDES_TEMPORAL_MEMORY_COMMIT
FAILED_ACTIVE_COMMIT_ABORTS_PENDING_TEMPORAL_STATE

DETERMINISTIC_CHECKPOINT_ORDER
CHECKPOINT_PAYLOAD_DIGEST_VERIFIED
LEGACY_CHECKPOINT_EXPLICIT_COLD_START
CORRUPT_CLAIMED_03B_STATE_FAILS_CLOSED

NO_FUSION_DECISION
NO_PHYSICAL_FUSION
NO_MUON_MOMENTUM_MUTATION
NO_OPTIMIZER_TOPOLOGY_MUTATION
```
