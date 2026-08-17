# ASH-BP-DK-BRIDGE-PAIR-EVIDENCE-SOURCE-CLOSURE-03A

## Status

```text
Patch ID: ASH-BP-DK-BRIDGE-PAIR-EVIDENCE-SOURCE-CLOSURE-03A
Direct parent: ASH-BP-DK-GENERATION-REVISION-STALE-OBSERVATION-SEAL-02
Local observation parent: ASH-BP-DK-LOCAL-TENSORCUBE-BP-DK-OBSERVATION-01
Contract parent: ASH-BP-DK-OBSERVATION-CONTRACT-AND-AUTHORITY-SEPARATION-00
Observation timing: BackpropPre before Local Muon parameter update
Bridge scope: same parameter only
Topology: canonical FirstCandidate 16x16 TensorCube grid
Adjacency: Right then Down only
Numerical evidence: exact aligned packed-gradient 256D cosine
Temporal Bridge state: forbidden
DeltaK_BRIDGE: not implemented
Fusion decision / physical fusion: forbidden
Precision / residency authority: unchanged
```

## Central SSOT

03A does not create Bridge Delta-K and does not alter Local Muon. It closes the source and identity boundary needed before later temporal coupling math can exist.

```text
VerifiedCurrent local BP-DK endpoint A
+ VerifiedCurrent local BP-DK endpoint B
+ same current generation-bound packed gradient
+ canonical same-parameter Right/Down adjacency
-> current Bridge pair evidence
```

The distinction is mandatory:

```text
Bridge pair evidence != Bridge Delta-K
canonical adjacency edge != fusion edge
signed gradient cosine != fusion decision
```

No `I_BRIDGE`, `M_BRIDGE`, `DeltaK_BRIDGE`, fusion threshold, fission threshold, or optimizer-topology policy is introduced.

## Parent preservation

03A preserves the existing decode Delta-K implementation, local BP Delta-K formula, freshness contract, FirstCandidate registry, Local Muon formula, Newton-Schulz path, momentum recurrence, optimizer routing, candidate commit authority, RAM36 authority, and generation-sealed resident cache.

Parent byte-preservation anchors remain:

```text
crates/ash_core/src/delta_k.rs
SHA256 4c7d02ff7492f9c07ea9bd59c42085f8ccdad0f49866df600d0d535074cce836

crates/ash_core/src/delta_k_phase_projection.rs
SHA256 0313d1fe94988b31da423567547b14f443b869963a74d44bbb7865d7d8a758e4

crates/model_core/src/semantic_prior_scores.rs
SHA256 7db6e0b632b5265f62b1e5a9b3a4ff5cf25c8627eef3e293581d9bd94d675cc7

crates/model_core/src/qw_mcts_hdc_state_encoder.rs
SHA256 04799c9be0e6d88f0a946fa878698537a06efd6e8b3b56971155a381bfb4b8ff

crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16.wgsl
SHA256 3f08fa919cfde360722ab37706d0bbbb292d5e849afe6dd7c1b3014da36533d8

crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_exact_subgroup32_norm.wgsl
SHA256 ce7cfd586adf561600ea5e4f20f51114e6f8a01ef239f9a38c6cc1db2c9167b4
```

## Production callsite ordering

For each HiMuon-admitted parameter, the physical order is now:

```text
R6 finalized gradient
-> existing TensorCubeLocalMuonGradientPacker
-> packed_gradient
-> local BP-DK observer
-> local Ready observation assembly
-> independent 02 freshness verification
-> VerifiedCurrent endpoint set
-> canonical same-parameter pair plan
-> exact 256D Bridge pair observer
-> compact pair receipts / typed pair evidence
-> existing Local Muon execute_resident_with_norm_path
```

Bridge observation occurs before Local Muon candidate execution and uses the exact packed gradient that Local Muon is about to consume. It does not reconstruct gradient evidence from candidate weights, momentum, post-update state, GradientSketch16, or local compact receipts.

## VerifiedCurrent admission

Only `VerifiedCurrentBpDeltaKObservation` may become a Bridge endpoint.

03A does not treat a raw `AshBpPreDeltaKObservation` as current. Immediately after a current parameter's Ready observation is assembled, the production path builds `AshBpDkFreshnessExpectation` independently from current runtime and registry authorities:

```text
resolved canonical TensorCube ID
route parameter ID
source weight generation
source optimizer generation
current BP/optimizer step
source weight digest
registry digest
optimizer routing digest
structural-law revision
local source revision
local observer revision
local policy revision
local policy digest
```

It then calls the existing 02 `verify_bp_pre_observation_current(...)` constructor path.

The expectation is not produced by copying lineage fields out of the observation under test. A raw observation therefore cannot manufacture its own Current proof.

Warming and any non-Current observation are absent from the Bridge endpoint set. No zero-valued fake endpoint or last-good fallback is introduced.

## Same-parameter topology authority

03A only permits:

```text
parameter P / TensorCube A <-> parameter P / TensorCube B
```

Cross-parameter, cross-layer, Q/K/V, or Gate/Up/Down Bridge coupling remains forbidden.

Topology comes only from the typed `FirstCandidateMuonGrid` and `resolve_tile()` authority. Bridge code does not parse `parameter_id`, `tensorcube_id`, `source_ids`, or observation strings to recover geometry.

The canonical TensorCube ID remains:

```text
muon16:<parameter_id>:r<row_start>:c<col_start>
```

but the string is identity only, never a topology parser input.

## Right/Down enumeration

For a canonical grid with `R = full_tile_rows` and `C = full_tile_cols`, row-major enumeration emits:

```text
if c + 1 < C: RIGHT (r,c) -> (r,c+1)
if r + 1 < R: DOWN  (r,c) -> (r+1,c)
```

RIGHT is emitted before DOWN for each source tile. Left/up duplicates, diagonals, wraparound, distance-2 pairs, and all-to-all pair scans do not exist in 03A.

Exact unfiltered candidate count:

```text
R * (C - 1) + (R - 1) * C
```

The implementation contains deterministic 2x2 ordering and 3x2 cardinality unit fixtures.

## Canonical pair identity

`AshBpDkBridgePairIdentity` binds:

```text
parameter_id
canonical_parameter_index
pair_ordinal
adjacency Right|Down
lhs/rhs canonical TensorCube IDs
lhs/rhs cube row/column
lhs/rhs canonical tile ordinals
```

`pair_ordinal` follows the canonical row-major Right-then-Down enumeration. Hash-map insertion order, GPU completion order, pointer identity, and string lexical order have no authority.

## Generation-bound packed gradient

03A reuses the existing `RawWgpuBufferLease packed_gradient` produced by `TensorCubeLocalMuonGradientPacker` for the current parameter. No second full gradient is created.

The host-side pair plan is bound by the current parameter/runtime lineage and the same registry/routing authority already used by Local Muon and local BP-DK.

No gradient-content digest is fabricated. Pointer identity is not promoted to content identity.

## Exact packed-gradient 256D cosine

Each canonical full TensorCube is 16 x 16 = 256 packed F32 gradient values.

For adjacent tiles A and B:

```text
dot(A,B)   = sum_i gA[i] * gB[i]
norm2(A)   = sum_i gA[i]^2
norm2(B)   = sum_i gB[i]^2
cosine     = dot(A,B) / sqrt(norm2(A) * norm2(B))
```

All 256 corresponding values participate. There is no GradientSketch16 substitution, row-mean substitution, sampling, top-k, random projection, sparsification, or dimensional truncation.

The existing local `GradientSketch16` remains local BP-DK observer evidence and is not reinterpreted as full-gradient direction.

## GPU observer topology

New backend observer:

```text
TensorCubeBpDkBridgePairObserver
```

New shader:

```text
base_train_bp_delta_k_bridge_pair_cosine_16x16.wgsl
```

Logical execution:

```text
one workgroup = one admitted pair
256 invocations = 256 aligned gradient dimensions
```

The gradient binding is read-only. Pair descriptors carry numeric pair ordinal and lhs/rhs packed bases. The GPU receives no parameter-ID strings and discovers no topology.

The reduction uses a fixed workgroup-local 256 -> 128 -> ... -> 1 tree for dot, lhs norm2, rhs norm2, and nonfinite count. No global unordered float atomic reduction or host gradient reduction is used.

## Zero norm and nonfinite semantics

`ZeroNorm` is distinct from cosine zero.

If either norm is nonpositive, the compact receipt is `ZeroNorm` and no `AshBpDkBridgePairEvidence` object is emitted. Transport padding values have no semantic cosine authority.

Nonfinite gradient inputs or nonfinite aggregate/cosine results produce `NonFinite`; they are not clamped, absolutized, or converted to zero evidence.

Valid cosine remains signed. Negative correlation remains negative.

## Compact readback / no gradient D2H

Only compact per-pair aggregate receipts are copied to MAP_READ buffers:

```text
dot
lhs norm2
rhs norm2
cosine
status
nonfinite count
pair ordinal
```

The 256-element gradient payload is never copied or mapped to host by the Bridge observer.

Mandatory counters remain:

```text
bridge_gradient_payload_readback_count = 0
bridge_gradient_payload_readback_bytes = 0
```

Compact receipt bytes are accounted separately.

## Local I/M/DeltaK binding

Each pair evidence object embeds two endpoint bindings copied from the already-verified local BP-DK observations:

```text
observation ID
TensorCube ID
parameter ID
I_BP
M_BP
DeltaK_BP_PRE raw
DeltaK_BP_PRE smoothed
parameter revision
optimizer generation
BP generation
source weight digest
registry digest
routing digest
observation policy digest
```

03A does not recompute local I, local M, or local Delta-K.

## Pair evidence contract

`AshBpDkBridgePairEvidence` binds:

```text
schema revision
canonical pair identity
lhs/rhs VerifiedCurrent endpoint projections
gradient source revision
parameter revision
optimizer generation
BP generation
source weight digest
registry digest
optimizer routing digest
gradient dot
lhs/rhs gradient norm2
signed exact 256D gradient cosine
```

It is a pair-evidence type. It is not `AshBpPreDeltaKObservation`, `AshUpdatePostDeltaKObservation`, or `DeltaKSnapshot`.

## Current-generation evidence lifetime

03A keeps only current-generation pair evidence in the production runtime. Advancing the BP generation explicitly clears the previous current-generation evidence vector. Generation regression fails closed.

This is not temporal Bridge state. There is no previous-cosine EMA, edge persistence, cooldown, Bridge age, historical ledger, checkpoint sidecar, or restart restoration for pair evidence.

The diagnostic/current consumer getter returns evidence deterministically sorted by canonical parameter index and pair ordinal.

## Physical batching

The Bridge observer builds its shader module, bind-group layout, and compute pipeline once per runtime observer instance.

Pair execution is device-limit-bounded using live:

```text
max_compute_workgroups_per_dimension
max_storage_buffer_binding_size
max_buffer_size
```

Many pair workgroups may execute in one physical batch. There is no mandatory one-submit/one-wait transaction per pair.

## No optimizer/fusion authority

The Bridge shader has no parameter-weight, candidate-weight, Muon momentum, Adam M/V, or optimizer-state binding.

Mandatory production invariants include:

```text
bridge_noncurrent_endpoint_consumption_count = 0
bridge_cross_parameter_pair_attempt_count = 0
bridge_gradient_payload_readback_count = 0
bridge_gradient_payload_readback_bytes = 0
bridge_gradient_mutation_count = 0
bridge_parameter_mutation_count = 0
bridge_muon_momentum_read_count = 0
bridge_muon_momentum_write_count = 0
bridge_delta_k_claim_count = 0
bridge_fusion_decision_count = 0
bridge_physical_fusion_execution_count = 0
bridge_optimizer_topology_mutation_count = 0
bridge_pair_omission_count = 0
bridge_pair_duplicate_count = 0
bridge_pair_order_drift_count = 0
```

Coverage closure also requires:

```text
Right evidence pairs + Down evidence pairs
= admitted Current pair count

Ready + ZeroNorm + NonFinite
= admitted Current pair count

Bridge workgroup count
= admitted Current pair count

Bridge dispatch count
= Bridge physical batch count

Bridge pipeline build count <= 1
```

No 16x32, 32x16, 32x32, or arbitrary fused optimizer domain is created.

## Changed files

The 03A code overlay contains exactly the following implementation surfaces:

```text
crates/ash_core/src/delta_k_bridge_pair_evidence.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bp_delta_k_bridge_pair_evidence.rs
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/bp_delta_k_bridge_pair_observer.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/base_train_bp_delta_k_bridge_pair_cosine_16x16.wgsl
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_bridge_pair_evidence_source_closure_03a_static.py
```

No markdown spec, generated manifest, artifact JSON, report JSON, or `*.sha256` sidecar is required in the code overlay ZIP.

## Static validation

New validator:

```text
tools/validate_ash_bp_dk_bridge_pair_evidence_source_closure_03a_static.py
148/148 PASS
```

Validated parent gates in the bake environment:

```text
BP-DK observation contract 00                    149/149 PASS
BP-DK local observation 01                       134/134 PASS
BP-DK stale observation seal 02                  243/243 PASS
Local Muon optimizer                             101/101 PASS
FirstCandidate registry                           97/97 PASS
Local Muon multi-tile batch                       61/61 PASS
Local Muon production callsite                    63/63 PASS
Muon registry canonical loader repair             38/38 PASS
Muon ExactSubgroup32 norm                        128/128 PASS
Muon X PAD17                                      52/52 PASS
Generation-sealed immutable Muon cache            66/66 PASS
Muon immutable-cache backend rebind               35/35 PASS
```

The 03A validator is appended to the existing CF1 static validator chain.

## Evidence boundary

```text
STATIC_BAKED_READY
NEW_STATIC_GATE_148_OF_148_PASS
PARENT_STATIC_GATES_PASS
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_CARGO_TEST_CLAIM
NO_PHYSICAL_WGPU_PAIR_COSINE_CLAIM
NO_PHYSICAL_LOCAL_VS_03A_PARITY_CLAIM
```

The bake environment does not provide `cargo` or `rustc`. User-local Cargo/WGPU execution remains the physical execution SSOT.

## Physical verification targets

```text
cargo check ash_core
cargo check burn_webgpu_backend
cargo check base_train
CF1 reaches 03A gate

2x2 grid -> exact 4-pair Right/Down order
3x2 grid -> exact formula cardinality
same source state -> deterministic pair order
GPU 256D cosine -> CPU 256D reference parity
identical gradient tiles -> cosine near +1
opposite tiles -> cosine near -1
orthogonal fixture -> cosine near 0
zero norm -> ZeroNorm / no fake zero-cosine evidence
nonfinite input -> NonFinite / no repaired evidence
Warming endpoint -> no Bridge pair evidence
Current + Current adjacent endpoints -> admissible pair
full gradient readback count = 0
Muon momentum Bridge access = 0
03A ON/OFF -> identical Local Muon candidate weight
03A ON/OFF -> identical Local Muon candidate momentum
```

## Non-goals

```text
No cross-parameter Bridge
No cross-layer Bridge
No Q/K/V or Gate/Up/Down Bridge
No GradientSketch16 cosine
No approximate/sampled cosine
No temporal Bridge state
No pair EMA
No Bridge history or checkpoint state
No I_BRIDGE
No M_BRIDGE
No DeltaK_BRIDGE
No fusion graph decision
No Fuse / Fission / Cooldown
No physical HiMuon fusion
No fused momentum
No fused Newton-Schulz domain
No POST update-direction observation
No precision admission
No residency admission
No Decode Delta-K rewrite
No Local BP-DK formula rewrite
No freshness contract rewrite
No FirstCandidate route change
No AdamW route change
No full gradient D2H
```

## Natural successor

```text
ASH-BP-DK-BRIDGE-TEMPORAL-COUPLING-OBSERVATION-03B
```

03B may consume only valid 03A pair evidence and must separately define temporal pair state, warmup, policy identity, persistence semantics, `I_BRIDGE`, `M_BRIDGE`, and `DeltaK_BRIDGE_PRE = I_BRIDGE * M_BRIDGE^2`. It must not retroactively rename the 03A cosine as Bridge Delta-K.

## Promotion seal

```text
PROMOTE_ASH_BP_DK_BRIDGE_PAIR_EVIDENCE_SOURCE_CLOSURE_03A

BP_DK_OBSERVATION_CONTRACT_00_PRESERVED
LOCAL_BP_DK_01_PRESERVED
FRESHNESS_SEAL_02_PRESERVED

VERIFIED_CURRENT_ENDPOINTS_ONLY
INDEPENDENT_FRESHNESS_EXPECTATION_AUTHORITY
SAME_PARAMETER_ONLY
CANONICAL_FIRSTCANDIDATE_GRID_AUTHORITY
RIGHT_DOWN_ADJACENCY_ONLY
NO_N2_PAIR_SCAN
NO_PARAMETER_ID_STRING_PARSING

EXACT_256D_PACKED_GRADIENT_COSINE
NO_GRADIENT_SKETCH_SUBSTITUTION
SIGNED_COSINE_PRESERVED
ZERO_NORM_IS_NOT_ZERO_COSINE

GENERATION_BOUND_PACKED_GRADIENT_SOURCE
FULL_GRADIENT_D2H_ZERO
LOCAL_I_M_DELTAK_BOUND_NOT_RECOMPUTED
CANONICAL_TYPED_PAIR_IDENTITY
DETERMINISTIC_PAIR_ORDER

BRIDGE_TEMPORAL_STATE_ABSENT
DELTAK_BRIDGE_ABSENT
FUSION_DECISION_ZERO
PHYSICAL_FUSION_EXECUTION_ZERO
MUON_MOMENTUM_READ_ZERO
MUON_MOMENTUM_WRITE_ZERO
OPTIMIZER_TOPOLOGY_MUTATION_ZERO
```
