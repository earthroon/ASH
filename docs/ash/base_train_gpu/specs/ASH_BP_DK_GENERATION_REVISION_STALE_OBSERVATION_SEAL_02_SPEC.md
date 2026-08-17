# ASH-BP-DK-GENERATION-REVISION-STALE-OBSERVATION-SEAL-02

## Status

```text
Patch ID: ASH-BP-DK-GENERATION-REVISION-STALE-OBSERVATION-SEAL-02
Direct parent: ASH-BP-DK-LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01
Contract parent: ASH-BP-DK-OBSERVATION-CONTRACT-AND-AUTHORITY-SEPARATION-00
Observation domain: BackpropPre
Freshness authority: consumer-time exact lineage verification
Bridge Delta-K math: not yet
HiMuon fusion execution: forbidden
Precision / residency authority: unchanged / forbidden
```

## Central SSOT

Patch 01 produces a numerically valid local `DeltaK_BP_PRE`. Patch 02 does not change `GradientSketch16`, `I_BP`, `M_BP`, the `I * M^2` structural law, BP-local EMA coefficients, or cold-start behavior. It answers a separate question: whether an already-produced observation still belongs to the exact state the current consumer is about to judge.

The freshness result is exactly one of:

```text
Current
Stale
Unverifiable
Contradictory
```

Only `Current` can become `VerifiedCurrentBpDeltaKObservation`.

```text
Stale != false Delta-K
Unverifiable = evidence insufficient / judgment deferred
Contradictory != merely old evidence
```

## Parent decode and Muon preservation

The existing decode Delta-K authority remains byte-identical:

```text
crates/ash_core/src/delta_k.rs
SHA256 4c7d02ff7492f9c07ea9bd59c42085f8ccdad0f49866df600d0d535074cce836

crates/ash_core/src/delta_k_phase_projection.rs
SHA256 0313d1fe94988b31da423567547b14f443b869963a74d44bbb7865d7d8a758e4

crates/model_core/src/semantic_prior_scores.rs
SHA256 7db6e0b632b5265f62b1e5a9b3a4ff5cf25c8627eef3e293581d9bd94d675cc7

crates/model_core/src/qw_mcts_hdc_state_encoder.rs
SHA256 04799c9be0e6d88f0a946fa878698537a06efd6e8b3b56971155a381bfb4b8ff
```

Muon kernels also remain byte-identical:

```text
base_train_tensorcube_local_muon_16x16.wgsl
SHA256 3f08fa919cfde360722ab37706d0bbbb292d5e849afe6dd7c1b3014da36533d8

base_train_tensorcube_local_muon_16x16_exact_subgroup32_norm.wgsl
SHA256 ce7cfd586adf561600ea5e4f20f51114e6f8a01ef239f9a38c6cc1db2c9167b4
```

No Decode Delta-K state/mode, Muon momentum, Newton-Schulz, norm, X PAD17, matrix layout, or candidate-weight formula is changed.

## Typed BP observation lineage

`AshBpPreDeltaKObservation` now carries explicit typed freshness fields:

```text
tensorcube_id
parameter_id
parameter_region_id
parameter_revision
optimizer_generation
bp_generation
source_weight_digest
registry_digest
optimizer_routing_digest
observation_policy_digest
```

The envelope remains authoritative for:

```text
structural_law_revision
source_revision
observer_revision
observation_policy_revision
generation
step
```

Cross-field parity is mandatory:

```text
parameter_revision == envelope.identity.generation
bp_generation        == envelope.identity.step
```

No freshness code parses parameter/TensorCube identity from `source_ids` strings.

The canonical TensorCube ID remains the existing FirstCandidate `resolve_tile()` identity:

```text
muon16:<parameter_id>:r<row_start>:c<col_start>
```

## Observation policy digest

`TensorCubeBpDkLocalObserverPolicy::canonical_digest()` binds, in fixed order:

```text
observer revision
policy revision
epsilon f32 bits
sketch EMA alpha f32 bits
Delta-K EMA alpha f32 bits
warmup observation count
```

using SHA-256. `observation_policy_revision` and `observation_policy_digest` are distinct authorities. Consumer policy is deliberately excluded from freshness identity: changing a later fusion threshold does not retroactively change what a BP observation meant when produced.

## Freshness contract

New core source:

```text
crates/ash_core/src/delta_k_observation_freshness.rs
```

It defines typed observation lineage, typed consumer-time expectation, freshness reasons/receipts, and the only constructor path for `VerifiedCurrentBpDeltaKObservation`.

### Current

All mandatory TensorCube/parameter identities, generations, revisions, and digests match the expected current state. Only this state receives a verified wrapper.

### Stale

The observation is valid historical evidence but older than the current authority. Examples:

```text
older BP generation
older optimizer generation
older parameter revision
old registry/routing digest
old structural/source/observer revision
old observation-policy revision/digest
```

Stale observations are rejected for the current consumer. They are not recalculated under a new policy and are never substituted as last-good evidence.

### Unverifiable

Mandatory evidence is missing, such as parameter identity, source-weight digest, registry/routing digest, or policy digest. The result is judgment deferred, not guessed stale/current.

### Contradictory

The lineage cannot coherently represent the expected state. Examples:

```text
future BP/optimizer/parameter generation
TensorCube identity mismatch
parameter identity mismatch
same parameter revision + different source-weight digest
envelope / typed-lineage contradiction
```

A same-revision/different-weight-digest case fails closed because the revision SSOT would otherwise identify two different weight states.

## Freshness receipt

`AshBpDkFreshnessReceipt` records:

```text
status + reason
observed/expected BP generation
observed/expected optimizer generation
observed/expected parameter revision
source-weight digest match
registry digest match
routing digest match
structural-law revision match
source revision match
observer revision match
policy revision match
policy digest match
```

Freshness verification never mutates `I_BP`, `M_BP`, raw Delta-K, or smoothed Delta-K.

## Verified-current authority

`VerifiedCurrentBpDeltaKObservation` has private data fields. Downstream code obtains it only through `verify_bp_pre_observation_current(...)`. A raw `AshBpPreDeltaKObservation` therefore cannot be silently treated as verified current evidence.

## Deterministic current-generation ledger

Patch 02 replaces the temporary consumer-authority `Vec` surface with:

```rust
BTreeMap<String, AshBpPreDeltaKObservation>
```

keyed by canonical TensorCube ID.

This provides deterministic iteration order, one current observation per TensorCube ID, and explicit duplicate rejection. Insertion order has no semantic authority.

Generation advance creates an `AshBpDkLedgerRetirementReceipt`, clears the retired generation from the current raw observation map, and admits only the new generation. There is no previous-generation or last-good fallback.

`bp_dk_observations_for_generation()` remains diagnostic. Consumer-facing access is `verify_current_bp_dk_observations(...)`, which returns verified observations plus freshness receipts/telemetry.

Mandatory invariant:

```text
stale_observation_consumption_count = 0
```

## Observation freshness vs EMA-state continuity

These are separate authorities.

```text
Observation freshness:
Can this already-created Delta-K observation be consumed now?

Observer-state continuity:
Can previous EMA state be used to calculate the next observation?
```

A previous observation may be stale while compatible EMA state legitimately continues into the next training step.

Normal monotonic parameter/optimizer/BP progression can continue EMA when observer semantics are unchanged. A newer parameter revision may have a different weight digest. But the same parameter revision with a different source-weight digest is an explicit contradiction.

## Explicit state reinitialization

The resident observer metadata now binds:

```text
source revision
observer revision
policy revision
policy digest
registry digest
optimizer routing digest
last source-weight digest
```

Semantic drift is not allowed to reuse the old EMA silently. Reinitialization reasons include source, observer, policy revision/digest, registry, and routing changes.

`TensorCubeBpDkObserverStateReinitializationReceipt` records previous/next identities and requires:

```text
next_observation_must_warm = true
```

The numeric state is explicitly reinitialized and the next observation follows the existing `Warming` path. No fabricated `DeltaK = 0` is emitted.

TensorCube tile-count/geometry drift remains a structural error. Patch 02 does not silently resize/migrate the 80-byte-per-TensorCube numeric EMA state.

## GPU/host ownership

```text
GPU buffer = numeric EMA state SSOT
Host metadata = identity/revision/digest compatibility SSOT
```

No string revision/digest shadow is packed into the GPU numeric state.

## Durable observer-state snapshot

Patch 02 adds explicit checkpoint-bound state sidecars:

```text
bp_dk_observer_state_manifest.json
bp_dk_observer_state.bin
```

The manifest binds:

```text
schema + patch ID
checkpoint generation
optimizer generation
structural/source/observer revisions
policy revision + policy digest
registry + optimizer-routing digest
payload byte length + payload SHA-256
parameter state descriptors
```

Each parameter descriptor binds parameter ID, tile count, last parameter/optimizer/BP generations, initialized flag, last source-weight digest, payload offset/length, and per-parameter state SHA-256.

Snapshot entries are sorted by parameter ID. Duplicate/non-increasing IDs, gaps, overlaps, trailing payload bytes, and digest mismatches are rejected.

Backend restore prevalidates the entire snapshot set, including duplicate parameter IDs and byte/digest/revision contracts, before installing restored states. This prevents partial restore.

## Resume classification

```text
exact compatible manifest + payload
-> pending restore
-> GPU observer state restore at observer materialization

both sidecars missing on resume
-> explicit RestartRewarmReceipt
-> local optimizer remains available
-> BP-DK evidence starts from Warming

structural/source/observer/policy/registry/routing semantic mismatch
-> explicit RestartRewarmReceipt
-> old EMA not imported
-> Warming restart

payload length/digest corruption
checkpoint-generation contradiction
optimizer-generation contradiction
split sidecar
-> fail closed
```

`AshBpDkObserverRestartRewarmReceipt` records source generation, source optimizer generation, reason, and `next_observation_must_warm = true`.

## Readback boundary

The observer-state GPU readback exists only behind `snapshot_all_states(...)`, invoked by `persist_bp_dk_observer_state(...)` at the explicit checkpoint/candidate persistence boundary.

Normal observation remains:

```text
hot_path_state_readback_count = 0
```

Checkpoint state-readback bytes have a separate counter.

## Scheduler durability binding

The R6 candidate transaction persists BP-DK observer state alongside Muon momentum and records:

```text
bpDkObserverStateDurable
bpDkObserverStateSha256
bpDkObserverStateBytes
bpDkObserverPolicyDigest
```

The state is therefore bound to the same candidate generation/optimizer-step transaction rather than an unrelated snapshot.

## No fabricated model generation

The current runtime exposes canonical source weight generation, source optimizer generation, and BP/optimizer step. Patch 02 does not invent a separate model-generation field or silently rename parameter revision into one.

## Bridge-facing boundary

A future Bridge observer must consume `VerifiedCurrentBpDeltaKObservation`, not raw local observations. Bridge must not implement a second competing freshness system.

There is one important current runtime constraint: the existing callsite is still parameter-inline:

```text
parameter A local BP-DK observation
-> parameter A Muon execution
-> parameter B local BP-DK observation
-> parameter B Muon execution
```

Therefore a Bridge planner intended to control the same optimizer step must establish a deterministic PRE-optimizer collection/planner barrier before cross-parameter fusion admission. Patch 02 deliberately does not reorder optimizer execution.

## Static validation

New validator:

```text
tools/validate_ash_bp_dk_generation_revision_stale_observation_seal_02_static.py
243/243 PASS
```

Final parent gates:

```text
BP-DK observation contract 00                 149/149 PASS
BP-DK local observation 01                    134/134 PASS
R6 production scheduler                       112/112 PASS
TensorCube Local Muon optimizer               101/101 PASS
FirstCandidate registry                        97/97 PASS
Muon production callsite                       63/63 PASS
Muon registry canonical loader repair          38/38 PASS
Muon ExactSubgroup32 norm                     128/128 PASS
Generation-sealed immutable Muon cache         66/66 PASS
Muon immutable-cache backend rebind             35/35 PASS
```

The validator is wired into `tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1`. Existing Cargo/check/test commands are retained.

## Changed files

The baked overlay contains exactly 12 files:

```text
crates/ash_core/src/delta_k_observation_contract.rs
crates/ash_core/src/delta_k_observation_freshness.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_local_observation.rs
crates/base_train/src/bp_delta_k_stale_observation_seal.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_generation_revision_stale_observation_seal_02_static.py
tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py
```

The 01 validator update only recognizes the deterministic current-generation ledger as the successor to the temporary active-generation `Vec`; its BP-DK math/authority checks are not relaxed.

## Evidence boundary

```text
STATIC_BAKED_READY
NEW_STATIC_GATE_243_OF_243_PASS
PARENT_STATIC_GATES_PASS
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_UNIT_TEST_EXECUTION_CLAIM
NO_PHYSICAL_GPU_RESTORE_CLAIM
NO_PHYSICAL_CHECKPOINT_ROUNDTRIP_CLAIM
NO_BRIDGE_RUNTIME_CLAIM
```

The bake environment has no Cargo/rustc or physical WGPU execution authority. User-local Cargo/WGPU execution remains the physical SSOT.

## Physical verification targets

```text
cargo check ash_core PASS
cargo check base_train PASS
CF1 reaches 02 gate

exact lineage -> Current + VerifiedCurrent
older BP generation -> Stale
future BP generation -> Contradictory
older parameter revision -> Stale
same revision / different source weight digest -> Contradictory
missing required digest -> Unverifiable
old observer/policy/registry/routing -> Stale

semantic observer-state change -> explicit reinit receipt
post-reinit first sample -> Warming
no fabricated zero Delta-K
normal revision advance -> EMA continuity

checkpoint snapshot PASS
exact resume restore PASS
missing sidecar -> explicit rewarm
semantic mismatch -> explicit rewarm
corrupt payload -> fail closed
hot-path state readback = 0
stale observation consumption = 0
```

## Non-goals

```text
No Bridge Delta-K math
No gradient cosine
No temporal coupling persistence
No joint novelty
No fusion candidate graph
No fusion threshold
No HiMuon fusion execution
No fission/cooldown
No POST Delta-K formula
No Fisher implementation
No precision admission
No residency admission
No Decode Delta-K rewrite
No GradientSketch16 rewrite
No new TensorCube geometry
No last-good observation fallback
No silent observer-state migration
No optimizer execution reordering yet
```

## Natural next patch

```text
ASH-BP-DK-BRIDGE-COUPLING-OBSERVATION-03
```

If Bridge evidence is intended to control the current optimizer step, its physical implementation must include or be preceded by a deterministic PRE-optimizer local-observation collection barrier so all candidate member TensorCubes are observed and freshness-verified before local/fused topology commit.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_GENERATION_REVISION_STALE_OBSERVATION_SEAL_02

BP_DK_LOCAL_OBSERVATION_01_PRESERVED
OBSERVATION_CONTRACT_00_PRESERVED
DECODE_DELTA_K_AUTHORITY_PRESERVED
I_TIMES_M_SQUARED_LAW_PRESERVED
GRADIENT_SKETCH_16_PRESERVED

CURRENT_STALE_UNVERIFIABLE_CONTRADICTORY_DISTINCT
STALE_IS_HISTORICAL_NOT_FALSE
UNVERIFIABLE_IS_JUDGMENT_DEFERRED
FUTURE_LINEAGE_IS_CONTRADICTION

CANONICAL_TENSORCUBE_STRING_IDENTITY
EXPLICIT_PARAMETER_IDENTITY
EXPLICIT_SOURCE_WEIGHT_DIGEST
EXPLICIT_REGISTRY_DIGEST
EXPLICIT_OPTIMIZER_ROUTING_DIGEST
EXPLICIT_OBSERVATION_POLICY_DIGEST
NO_SOURCE_ID_STRING_PARSING

PARAMETER_REVISION_BINDING
OPTIMIZER_GENERATION_BINDING
BP_GENERATION_BINDING
STRUCTURAL_LAW_REVISION_BINDING
SOURCE_REVISION_BINDING
OBSERVER_REVISION_BINDING
OBSERVATION_POLICY_REVISION_BINDING
OBSERVATION_POLICY_DIGEST_BINDING
CONSUMER_POLICY_NOT_OBSERVATION_FRESHNESS

EXACT_CONSUMER_TIME_FRESHNESS_GATE
VERIFIED_CURRENT_BP_DK_OBSERVATION
PRIVATE_VERIFIED_CURRENT_CONSTRUCTION
RAW_OBSERVATION_DIAGNOSTIC_ONLY

DETERMINISTIC_CURRENT_GENERATION_LEDGER
BTREE_TENSORCUBE_ID_ORDER
DUPLICATE_TENSORCUBE_REJECTED
GENERATION_RETIREMENT_RECEIPT
NO_PREVIOUS_GENERATION_FALLBACK
NO_LAST_GOOD_DELTA_K_FALLBACK

OBSERVER_STATE_CONTINUITY_SEPARATED_FROM_OBSERVATION_FRESHNESS
NORMAL_PARAMETER_REVISION_ADVANCE_CAN_CONTINUE_EMA
SAME_REVISION_DIFFERENT_WEIGHT_DIGEST_CONTRADICTION
ZERO_CROSS_POLICY_EMA_REUSE
ZERO_CROSS_OBSERVER_EMA_REUSE
ZERO_CROSS_REGISTRY_EMA_REUSE
ZERO_CROSS_ROUTING_EMA_REUSE

EXPLICIT_STATE_REINITIALIZATION
REINITIALIZATION_RECEIPT
REINITIALIZATION_FORCES_WARMING
NO_SILENT_EMA_RESET
NO_FABRICATED_ZERO_DELTA_K

GPU_NUMERIC_EMA_AUTHORITY_PRESERVED
HOST_LINEAGE_AUTHORITY
CHECKPOINT_BOUND_OBSERVER_STATE_SNAPSHOT
DETERMINISTIC_PARAMETER_SORTED_SNAPSHOT
PER_PARAMETER_STATE_DIGEST
WHOLE_PAYLOAD_DIGEST
NO_PARTIAL_RESTORE
ZERO_HOT_PATH_OBSERVER_STATE_READBACK

EXACT_RESUME_VALIDATION
MISSING_STATE_EXPLICIT_REWARM
SEMANTIC_MISMATCH_EXPLICIT_REWARM
CORRUPT_PAYLOAD_FAIL_CLOSED
CHECKPOINT_GENERATION_BINDING
OPTIMIZER_GENERATION_BINDING_AT_SNAPSHOT

STALE_REJECTION_RECEIPT
ZERO_STALE_OBSERVATION_CONSUMPTION
BRIDGE_READY_VERIFIED_CURRENT_SURFACE

ZERO_BRIDGE_DELTA_K_MATH_02
ZERO_HIMUON_FUSION_EXECUTION
ZERO_PRECISION_COMMIT
ZERO_RESIDENCY_COMMIT
ZERO_PARAMETER_MUTATION
ZERO_GRADIENT_MUTATION

MUON_MATH_PRESERVED
DECODE_DELTA_K_PRESERVED
CF1_STATIC_GATE_WIRED
NO_LOCAL_COMPILE_CLAIM
SEALED
```