# ASH-BP-DK-LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01

## Status

```text
Patch ID: ASH-BP-DK-LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01
Parent: ASH-BP-DK-OBSERVATION-CONTRACT-AND-AUTHORITY-SEPARATION-00
Observation domain: BackpropPre
TensorCube geometry: existing canonical HiMuon 16x16 only
Execution mode: shadow observation
HiMuon fusion execution: forbidden
Precision commit: forbidden
Residency movement: forbidden
```

## 1. Central SSOT

R1 implements the first real training-domain Delta-K observer while preserving the existing decode Delta-K implementation.

```text
Decode Delta-K:
DeltaKComputer + decode I/M + decode EMA + compact/mix/reverb
= unchanged

BP Delta-K 01:
canonical 16x16 HiMuon TensorCube
+ committed R6 finalized gradient
+ pre-update parameter
+ BP-local observer state
-> I_BP
-> M_BP
-> DeltaK_BP_PRE = I_BP * M_BP^2
-> shadow evidence only
```

The shared structural law remains `DeltaK = I * M^2`. Observer input semantics and mutable state remain domain-owned.

## 2. Decode parent preservation

These files remain byte-identical to the parent:

```text
crates/ash_core/src/delta_k.rs
4c7d02ff7492f9c07ea9bd59c42085f8ccdad0f49866df600d0d535074cce836

crates/ash_core/src/delta_k_phase_projection.rs
0313d1fe94988b31da423567547b14f443b869963a74d44bbb7865d7d8a758e4

crates/model_core/src/semantic_prior_scores.rs
7db6e0b632b5265f62b1e5a9b3a4ff5cf25c8627eef3e293581d9bd94d675cc7

crates/model_core/src/qw_mcts_hdc_state_encoder.rs
04799c9be0e6d88f0a946fa878698537a06efd6e8b3b56971155a381bfb4b8ff
```

No BP code calls `DeltaKComputer::update()`. Decode EMA, thresholds, and `compact/mix/reverb` are not reused.

## 3. 00 contract correction: canonical TensorCube ID

The 00 shell used `tensorcube_id: u64`, but the actual FirstCandidate SSOT produces canonical IDs through `resolve_tile()`:

```text
muon16:<parameter_id>:r<row_start>:c<col_start>
```

R1 corrects `AshBpPreDeltaKObservation` and `AshUpdatePostDeltaKObservation` to:

```rust
tensorcube_id: String
```

No numeric hash or alternate registry is introduced. The 00 static validator is updated accordingly and remains 149/149 PASS.

## 4. Observation scope and route authority

R1 observes only parameters already classified by the existing FirstCandidate registry as HiMuon-capable (`muon_grid.is_some()`).

```text
existing semantic route
-> existing muon_grid
-> existing resolve_tile()
-> BP-DK observation
```

AdamW parameters are never promoted by Delta-K.

## 5. Gradient authority

The source is the existing GPU-resident `R6FinalizedGradient` produced after R6 accumulation finalize and nonfinite verification.

```text
8-microbatch accumulation
-> weighted finalize
-> R6FinalizedGradient GPU lease
-> existing TensorCubeLocalMuonGradientPacker
-> packed canonical 16x16 gradient tiles
-> BP-DK observation
```

The current R6 path has no separate canonical loss-scale-unscale or max-norm clip transform after finalize, so R1 does not invent a “post-clip” claim.

Existing accumulator authority remains:

```text
production_gradient_payload_readback_count = 0
full_gradient_host_materialization_count = 0
```

BP-DK also performs zero full gradient readback.

## 6. Pre-update parameter authority

R1 observes `packed_muon_weight` before the Muon optimizer kernel executes. The shader bindings are read-only:

```wgsl
@binding(1) var<storage, read> packed_gradient: array<f32>;
@binding(2) var<storage, read> packed_weight: array<f32>;
```

There is no candidate-weight, momentum, optimizer-state, precision, residency, or parameter-output binding in the observer shader.

### Explicit performance debt

R1 uploads the packed pre-update weight once more for BP-DK observation. This is measured by `bp_dk_parameter_upload_bytes` and is not hidden. A later optimization may share the existing Muon resident-weight lease without changing observation semantics.

## 7. Explicit BP policy R1

```text
observer revision: ASH_BP_DK_GRADIENT_SKETCH_ROW_MEAN_16_R1
policy revision:   ASH_BP_DK_LOCAL_OBSERVER_POLICY_R1
source revision:   R6_FINALIZED_GRADIENT_WEIGHTED_MEAN_F32_R1

epsilon                  = 1.0e-8
sketch_ema_alpha         = 0.125
delta_k_ema_alpha        = 0.125
warmup_observation_count = 1
```

These are BP-local policy values and are not inherited from decode Delta-K.

## 8. GradientSketch16

For each canonical `16x16` gradient tile `G`, R1 computes sixteen signed row means:

```text
S_r = (1/16) * sum_j G[r,j]
GradientSketch16 = [S_0 ... S_15]
```

This is an R1 bounded observer sketch, not a claim of equivalence to the full 256-D gradient direction.

## 9. Information term

R1 compares the current sketch against the previous BP-local EMA sketch before committing the current sample.

```text
sketch_delta_rms = RMS(current_sketch - previous_ema_sketch)
I_BP = sketch_delta_rms / (previous_ema_sketch_rms + epsilon)
```

Current-sample EMA mutation happens only after the candidate observation passes validation.

## 10. Material term

```text
gradient_rms  = sqrt(sum(g_i^2) / 256)
parameter_rms = sqrt(sum(w_i^2) / 256)
M_BP = scheduled_learning_rate * gradient_rms / (parameter_rms + epsilon)
```

`M_BP` is explicitly a first-order PRE displacement proxy. It does not consume Adam moments, Muon momentum, Newton-Schulz output, Nesterov output, weight decay, or post-update parameter deltas.

## 11. Delta-K

Ready observations compute:

```text
DeltaK_BP_PRE_raw = I_BP * M_BP * M_BP
```

The common 00 envelope validates the same structural law.

R1 also records BP-local smoothing:

```text
first Ready sample:
DeltaK_smoothed = DeltaK_raw

later samples:
DeltaK_smoothed = 0.125 * DeltaK_raw + 0.875 * previous_DeltaK_ema
```

Neither raw nor smoothed Delta-K controls fusion in R1.

## 12. Cold start

A new TensorCube has no prior observation state. R1 emits `WARMING` rather than fabricating Delta-K zero:

```text
information_term = None
material_term = None
delta_k_raw = None
delta_k_smoothed = None
```

The first valid sample seeds state. With `warmup_observation_count = 1`, the second valid observation can become Ready.

## 13. GPU-resident observer state

Per TensorCube:

```text
ema_sketch[16]   64 B
ema_sketch_rms    4 B
delta_k_ema       4 B
sample_count      4 B
state_epoch       4 B
----------------------
80 B / TensorCube
```

The authoritative numeric EMA state is GPU-resident. No host numeric EMA shadow is maintained.

R1 state is process/runtime resident only and is not checkpoint-durable. Restart/stale/durable observation semantics are intentionally deferred to patch 02.

## 14. Transactional state commit

```text
resident state_in
+ packed gradient
+ pre-update weight
-> candidate state
+ compact receipt
-> host receipt validation
-> PASS: GPU copy candidate state -> resident state
-> FAIL: no resident-state advancement
```

A failed observation cannot advance EMA state by itself.

## 15. Compact receipt

Each TensorCube readback is exactly 12 32-bit words = 48 B:

```text
gradient_rms
parameter_rms
sketch_rms
sketch_delta_rms
previous_ema_sketch_rms
information_term
material_term
delta_k_raw
delta_k_smoothed
scheduled_learning_rate
status
nonfinite_count
```

No gradient payload is read back.

## 16. GPU execution geometry

New shader:

```text
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_local_observe_16x16.wgsl
```

```text
1 workgroup = 1 TensorCube
workgroup size = 256
1 invocation = 1 gradient/weight element
```

R1 uses deterministic workgroup reductions and does not depend on exact subgroup32. Subgroup optimization is intentionally outside this correctness patch.

## 17. Nonfinite behavior

Gradient/weight nonfinite values fail closed. The observer does not silently repair NaN/Inf or clamp negative terms into a valid observation. Candidate state is not committed on failure.

## 18. Lineage binding

R1 binds current production lineage as:

```text
parameter_revision = source weight generation
optimizer_generation = source optimizer step
bp_generation = target optimizer/BP step receiving the finalized gradient
```

Observation IDs are deterministic descriptive IDs, not claimed cryptographic seals:

```text
dk.bp_pre:<canonical_tensorcube_id>:param<P>:opt<O>:bp<B>
```

`R6FinalizedGradient` currently has no canonical snapshot ID, so `source_snapshot_id = None` is explicit instead of inventing one.

## 19. Duplicate and active-generation rules

Per parameter, R1 rejects:

```text
same bp_generation twice
bp generation regression
parameter revision regression
optimizer generation regression
```

`ProductionMuonRuntime` keeps Ready observations only for the current active BP generation. On generation advance, the previous current-generation vector is cleared. Future Bridge Delta-K can consume this generation-bound surface.

## 20. Coverage invariants

At production receipt closure:

```text
warming_count + ready_count == eligible TensorCube observation count
eligible TensorCube observation count == Muon tile execution count
observer state commit count == Muon parameter invocation count
```

This rejects silent sparse observation and Atlas-segment double counting.

## 21. Shadow authority mandatory zeros

```text
bp_dk_full_gradient_readback_count = 0
bp_dk_full_gradient_readback_bytes = 0
bp_dk_gradient_mutation_count = 0
bp_dk_parameter_mutation_count = 0
bp_dk_optimizer_authority_leak_count = 0
bp_dk_decode_state_reuse_count = 0
bp_dk_adamw_route_promotion_count = 0
bp_dk_himuon_fusion_execution_count = 0
```

No precision or residency commit API is introduced.

## 22. Existing Muon preservation

The two current Muon norm shaders remain byte-identical:

```text
serial Muon shader
3f08fa919cfde360722ab37706d0bbbb292d5e849afe6dd7c1b3014da36533d8

ExactSubgroup32 norm shader
ce7cfd586adf561600ea5e4f20f51114e6f8a01ef239f9a38c6cc1db2c9167b4
```

R1 does not change Muon momentum, Newton-Schulz, X PAD17, A/B layout, candidate weight math, norm selection, registry routing, or RAM36 authority.

## 23. Static validation

```text
tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py
134/134 PASS
```

Parent gates:

```text
BP-DK observation contract 00           149/149 PASS
R6 production scheduler                 112/112 PASS
TensorCube Local Muon optimizer         101/101 PASS
FirstCandidate registry                  97/97 PASS
Muon production callsite                 63/63 PASS
Muon registry recursion repair           38/38 PASS
Muon ExactSubgroup32 norm               128/128 PASS
Generation-sealed immutable Muon cache   66/66 PASS
Muon immutable-cache backend rebind      35/35 PASS
```

The new validator is wired into `tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1`.

## 24. Changed files

Overlay contains exactly 12 files:

```text
crates/ash_core/src/delta_k_observation_contract.rs
crates/base_train/Cargo.toml
crates/base_train/src/bp_delta_k_local_observation.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_local_observe_16x16.wgsl
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py
tools/validate_ash_bp_dk_observation_contract_authority_separation_00_static.py
```

Code ZIPs contain no Markdown, `*.sha256`, or Python cache artifacts.

## 25. Evidence boundary

The bake environment has no Cargo/rustc and no physical WGPU execution authority.

```text
STATIC_BAKED_READY
NEW_STATIC_GATE_134_OF_134_PASS
PARENT_STATIC_GATES_PASS
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_PHYSICAL_GPU_OBSERVATION_CLAIM
NO_OBSERVER_OVERHEAD_CLAIM
NO_TRAINING_QUALITY_CLAIM
```

User-local Cargo/WGPU execution remains the physical SSOT.

## 26. Physical verification targets

```text
cargo check ash_core PASS
cargo check base_train PASS
new WGSL compile PASS
CF1 reaches BP-DK-01 gate

first observation -> WARMING
second observation -> READY
no fabricated cold-start Delta-K
I_BP finite
M_BP finite
DeltaK_raw = I_BP * M_BP^2
DeltaK_smoothed finite

full gradient readback = 0
same bp_generation duplicate -> reject
failed observation -> no EMA state commit
observer ON/OFF -> same parameter result
observer ON/OFF -> same Muon momentum result
observer ON/OFF -> same optimizer route
decode Delta-K behavior unchanged
```

Measure separately:

```text
BP-DK GPU time
additional weight upload bytes
compact receipt readback bytes
GPU observer-state bytes
```

## 27. Non-goals

```text
No Bridge Delta-K
No inter-TensorCube coupling/cosine
No fusion graph
No fusion threshold
No HiMuon fusion
No fission/cooldown
No POST Delta-K
No Fisher implementation
No full 256-D gradient EMA
No AdamW promotion
No precision admission
No residency admission
No observer-state checkpoint durability
No resident-weight lease sharing yet
No decode Delta-K rewrite
```

## 28. Natural next patch

```text
ASH-BP-DK-GENERATION-REVISION-STALE-OBSERVATION-SEAL-02
```

This must formalize stale/replay/durable observation validity across parameter revision, optimizer generation, BP generation, observer revision, and policy revision before Bridge coupling can consume Local BP Delta-K.

Then:

```text
ASH-BP-DK-BRIDGE-COUPLING-OBSERVATION-03
```

may create inter-TensorCube relationship evidence.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_LOCAL_TENSORCUBE_BP_DK_OBSERVATION_01
OBSERVATION_CONTRACT_00_ADOPTED
EXISTING_DECODE_DELTA_K_AUTHORITY_PRESERVED
DECODE_PARENT_BYTES_PRESERVED
I_TIMES_M_SQUARED_STRUCTURAL_LAW_PRESERVED
BACKPROP_PRE_DOMAIN
CANONICAL_TENSORCUBE_STRING_IDENTITY_CORRECTED
EXISTING_MUON16_RESOLVE_TILE_IDENTITY_REUSED
NO_NUMERIC_SHADOW_TENSORCUBE_ID
FIXED_TENSORCUBE_16X16
NO_RETILING
EXISTING_HIMUON_ROUTE_ONLY
ZERO_ADAMW_TO_HIMUON_PROMOTION
R6_FINALIZED_GRADIENT_GPU_LEASE_AUTHORITY
NO_FULL_GRADIENT_HOST_MATERIALIZATION
EXISTING_GPU_GRADIENT_PACKER_REUSED
PRE_UPDATE_PARAMETER_AUTHORITY
READ_ONLY_GRADIENT_BINDING
READ_ONLY_PARAMETER_BINDING
SCHEDULED_LEARNING_RATE_PRE_AUTHORITY
GRADIENT_SKETCH_ROW_MEAN_16_R1
OBSERVER_LOCAL_EMA_ONLY
NO_DECODE_EMA_REUSE
NO_DECODE_THRESHOLD_REUSE
PREVIOUS_STATE_FIRST_NOVELTY
BP_INFORMATION_TERM
GRADIENT_RMS_256
PARAMETER_RMS_256
FIRST_ORDER_RELATIVE_DISPLACEMENT
NO_ADAM_MOMENT_IN_M_TERM
NO_MUON_TRANSFORM_IN_M_TERM
NO_WEIGHT_DECAY_IN_M_TERM
DELTA_K_BP_PRE_EQUALS_I_TIMES_M_SQUARED
RAW_DELTA_K_PRESERVED
BP_LOCAL_SMOOTHED_DELTA_K
EXPLICIT_R1_POLICY
COLD_START_WARMING_EXPLICIT
NO_FABRICATED_ZERO_DELTA_K
GPU_RESIDENT_NUMERIC_STATE
80_BYTES_PER_TENSORCUBE_STATE
48_BYTES_PER_TENSORCUBE_COMPACT_RECEIPT
CANDIDATE_STATE_TRANSACTION
VALIDATE_BEFORE_RESIDENT_STATE_COMMIT
ZERO_FULL_GRADIENT_READBACK
CURRENT_GENERATION_READY_OBSERVATION_LEDGER
DUPLICATE_BP_GENERATION_REJECTED
NONFINITE_FAIL_CLOSED
OBSERVATION_COVERAGE_SEALED
STATE_COMMIT_CARDINALITY_SEALED
ZERO_GRADIENT_MUTATION
ZERO_PARAMETER_MUTATION
ZERO_OPTIMIZER_AUTHORITY_LEAK
ZERO_HIMUON_FUSION_EXECUTION
ZERO_PRECISION_COMMIT
ZERO_RESIDENCY_MOVEMENT
MUON_MATH_PRESERVED
REGISTRY_AUTHORITY_PRESERVED
RAM36_AUTHORITY_PRESERVED
EXTRA_BP_DK_WEIGHT_UPLOAD_TELEMETRY_EXPLICIT
NO_UNMEASURED_OVERHEAD_CLAIM
CF1_STATIC_GATE_WIRED
NO_LOCAL_COMPILE_CLAIM
SEALED
```
