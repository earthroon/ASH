# ASH-BASETRAIN-G204D-FROZEN-PARTITION-BACKWARD-01

## Forward Partition Generation Pinning /
## Forward Activation Lineage /
## Softmax Backward Global-State Replay /
## Chunked dV·dP·dScore·dQ·dK /
## QKV Projection Gradient Binding /
## CPU-f64 Small Oracle /
## No Full Attention Matrix Materialization /
## No Stale Forward Receipt Passage /
## No Optimizer Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-G204D-FROZEN-PARTITION-BACKWARD-01`  
> Build revision: `G204D-g203d-frozen-partition-backward-r1`  
> Parent: `ASH-BASETRAIN-G203D-FORWARD-PARITY-01`  
> Parent state: `PHYSICAL PASS`  
> Backward authority: selected attention Q/K/V candidate gradients only  
> Optimizer authority: none  
> Weight mutation authority: none  
> Checkpoint authority: none

---

# 1. Goal

G204D opens the first bounded backward authority after G203D forward parity. It executes a fresh G203D-qualified forward invocation, pins the exact forward partition and activation lineage, replays the global softmax state, and produces quarantined dQ/dK/dV plus selected QKV projection-gradient candidates.

Canonical path:

```text
fresh G203D-qualified forward
  -> exact BaseTrain invocation binding
  -> forward/backward lease
  -> pinned partition generation
  -> pinned Q/K/V, mask, GQA, scale and global softmax state
  -> actual BaseTrain upstream dContext
  -> GPU backward dQ + row-dot dispatch
  -> GPU backward dK + dV dispatch
  -> CPU-f64 oracle
  -> directional finite difference
  -> selected QKV projection-gradient candidate
  -> quarantine
```

G204D must not invoke optimizer creation, optimizer step, weight delta, weight mutation, checkpoint commit or the G107 optimizer bridge.

---

# 2. Parent authority

Required parent token:

```text
PASS_ASH_BASETRAIN_G203D_LEGACY_TRAINING_ATTENTION_ORACLE_SHARED_TENSORCUBE_TRAINING_FORWARD_CANDIDATE_EXACT_QKV_SNAPSHOT_DUAL_CONSUMPTION_EXACT_MASK_SNAPSHOT_CAUSAL_PADDING_ALL_MASKED_ROW_GQA_MAPPING_ATTENTION_SCALE_FULL_SEQUENCE_PREFILL_FIRST_MIDDLE_LAST_LAYER_CHUNK_BOUNDARY_MIXED_PRECISION_TOLERANCE_PROFILE_CONTEXT_VALUE_PARITY_ACTIVATION_SHAPE_LAYOUT_DTYPE_PARITY_DETERMINISTIC_REPLAY_EXECUTION_ORDER_STABILITY_VRAM_PLATEAU_LEGACY_TRAINING_WRITER_PRESERVATION_DECODE_PRODUCTION_WRITER_PRESERVATION_NO_TRAINING_SPECIFIC_ATTENTION_FORK_NO_CANDIDATE_COMMIT_NO_DEFAULT_TRAINING_ROUTE_PROMOTION_NO_BACKWARD_NO_GRADIENT_WRITE_NO_OPTIMIZER_WRITE_NO_WEIGHT_MUTATION_NO_CHECKPOINT_WRITE_NO_TOLERANCE_AUTO_WIDEN_NO_SILENT_FALLBACK_SEALED
```

A JSON artifact from a previous process is not an activation lease. G204D must execute a fresh forward in the current runtime and receive live device-local Q/K/V and Stage11 global state.

---

# 3. Forward/backward lease

The lease binds:

```text
parent G203D artifact digest and PASS token
W8 invocation identity
BaseTrain training invocation digest
model partition
checkpoint
tokenizer
Q/K/V source generations
forward context identity
partition generation
partition digest
canonical chunk order
Q/K/V snapshot digest
mask snapshot
GQA mapping
attention scale
global softmax state lineage
Q/K/V geometry
runtime epoch
```

Any stale, consumed, retired, cross-layer, cross-microbatch, cross-checkpoint or cross-partition lease is rejected before backward dispatch.

---

# 4. Shared forward source surface

The W8 live continuation exposes:

```text
raw prepared Q lease
raw prepared K lease
raw prepared V lease
host fixture Q/K/V values for qualification oracle
Stage11 candidate global-state buffer
partition generation and digest
canonical chunk-order digest
Q and KV sequence geometry
Q and KV position bases
attention scale
```

The same prepared Q/K/V used by Headwise and TensorCube forward are consumed by G204D backward. No training-only forward fork is admitted.

---

# 5. Backward mathematics

For a visible query/key pair:

```text
P_ij = exp(S_ij - global_max_i) / global_denominator_i

dP_ij = dot(dContext_i, V_j)
row_dot_i = sum_j(P_ij * dP_ij)
dScore_ij = P_ij * (dP_ij - row_dot_i) * attention_scale

dQ_i += dScore_ij * K_j
dK_j += dScore_ij * Q_i
dV_j += P_ij * dContext_i
```

The GPU path does not materialize complete score, probability, dP or dScore matrices.

---

# 6. GPU dispatch ownership

Two compute dispatches are used:

```text
Dispatch A: backward_dq_rowdot
  one workgroup owns one query-row and Q-head
  writes one row-dot value
  writes the complete dQ row

Dispatch B: backward_dkdv
  one workgroup owns one key-row and KV-head
  iterates Q-heads in canonical ascending order
  iterates query rows in canonical ascending order
  writes complete dK and dV rows
```

Required properties:

```text
cross-workgroup f32 atomic gradient writes = 0
host gradient reduction = 0
unordered gradient reduction = 0
one owner per output element
```

---

# 7. GQA backward

The actual model mapping is fixed at the current qualification geometry:

```text
Q heads = 32
KV heads = 4
GQA group size = 8
head dimension = 64
```

For one KV head, gradients from sharing Q heads are accumulated in ascending Q-head order. Forward and backward GQA mappings must have the same digest.

---

# 8. All-masked semantics

An all-masked row has no visible key and must produce:

```text
row-dot = 0
dQ = 0
dK contribution = 0
dV contribution = 0
NaN = 0
Inf = 0
```

The physical matrix includes an explicit all-masked scenario by assigning a KV position base beyond all query positions.

---

# 9. BaseTrain dContext source

BaseTrain owns the upstream attention-context gradient candidate. The source surface is:

```text
BaseTrainLossToAttentionContextGradientCandidate
```

The dContext candidate binds the BaseTrain invocation, layer and context element count. The GPU backend consumes dContext but does not create loss, optimizer or weight authority.

---

# 10. Selected QKV projection gradient binding

G204D binds dQ/dK/dV digests to these selected groups:

```text
attention.q_proj
attention.k_proj
attention.v_proj
```

The binding receipt requires:

```text
selected-group scope only
full-model gradient scope = false
optimizer consumable = false
G107 bridge invocation count = 0
gradient/weight alias count = 0
```

---

# 11. CPU-f64 oracle

For each physical scenario, an independent scalar f64 implementation computes:

```text
probability
dP
row-dot
dScore
dQ
dK
dV
```

GPU dQ/dK/dV are compared using digest-pinned absolute, relative and relative-floor tolerances.

A directional finite-difference check is also required:

```text
[L(Q + epsilon*u) - L(Q - epsilon*u)] / (2*epsilon)
vs
dot(dQ, u)
```

Analytic and finite-difference values must match within the configured directional tolerance.

---

# 12. Replay

Every scenario group runs at least twice. Replay compares stable input lineage and:

```text
dQ digest
dK digest
dV digest
maximum absolute parity errors
```

Run-unique submission, transaction and receipt identities are not used as tensor-content identity.

---

# 13. Physical matrix

Required groups:

```text
first layer, Q8/K8 causal full-valid
middle layer, Q16/K32 exact chunk boundary
last layer, Q16/K33 boundary plus one
middle layer, Q8/K8 all-masked
```

Each group executes at least two repeats.

---

# 14. Resource contract

Forbidden allocations and behavior:

```text
full score matrix
full probability matrix
full dP matrix
full dScore matrix
float atomic gradient writes
host gradient reduction
unbounded gradient retention
optimizer object creation
optimizer-state write
weight delta
weight mutation
checkpoint write
```

Qualification-only dQ/dK/dV readback is allowed for CPU-f64 parity and digest sealing, then retired.

---

# 15. Mutation firewall

Required zero counters:

```text
optimizer create
optimizer step
optimizer-state write
G107 bridge invocation
weight delta
base-weight mutation
LoRA-weight mutation
checkpoint write
training cursor commit
default training-route promotion
Decode-route mutation
silent fallback
```

Legacy BaseTrain writer and Decode TensorCube production writer remain unchanged.

---

# 16. Implementation surface

```text
crates/model_core/src/base_train_g204d_frozen_partition_backward.rs
crates/base_train/src/base_train_g204d_frozen_partition_backward.rs
crates/burn_webgpu_backend/src/base_train_g204d_attention_backward_probe.rs
crates/burn_webgpu_backend/src/shaders/base_train_g204d_attention_backward.wgsl
crates/orchestrator_local/src/attention_interconnect_w8_physical_runner.rs
crates/orchestrator_local/src/base_train_g204d_cli_registry.rs
crates/orchestrator_local/src/base_train_g204d_scenario_plan.rs
crates/orchestrator_local/src/bin/ash_basetrain_g204d_verification_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_g204d_physical_gate.rs
specs/cli/ash_basetrain_g204d_verification.args
specs/cli/ash_basetrain_g204d_physical.args
```

Public surfaces use direct crate-root module declarations and explicit exports. Registry-only include publication is forbidden.

---

# 17. Verification gate

Binary:

```text
ash_basetrain_g204d_verification_gate
```

The verification gate checks:

```text
parent G203D artifact and PASS lineage
CLI registry exactness
Cargo bin registration
direct crate exports
fresh forward/backward lease surfaces
actual BaseTrain dContext surface
backward shader entrypoints
no float atomic gradient writes
no full-matrix surfaces
scenario matrix and all-masked coverage
selected QKV gradient binding
mutation firewall
atomic runtime artifact publication
```

Verification PASS token:

```text
PASS_ASH_BASETRAIN_G204D_FORWARD_PARTITION_GENERATION_PINNING_ACTIVATION_LINEAGE_GLOBAL_SOFTMAX_REPLAY_CHUNKED_DQ_DK_DV_SELECTED_QKV_GRADIENT_CPU_F64_ORACLE_NO_STALE_FORWARD_RECEIPT_NO_OPTIMIZER_AUTHORITY_STATIC_VERIFICATION_SEALED
```

---

# 18. Physical gate

Binary:

```text
ash_basetrain_g204d_physical_gate
```

Physical phases:

```text
A. Verify G203D parent artifact and manifest
B. Bootstrap one native WGPU runtime
C. Create BaseTrain-owned training invocation and dContext candidate
D. Execute fresh W8 Headwise/TensorCube forward
E. Pin partition, Q/K/V, mask, GQA, scale and global state
F. Execute backward_dq_rowdot
G. Execute backward_dkdv
H. Compare dQ/dK/dV against CPU-f64 oracle
I. Run directional finite difference
J. Bind selected QKV projection-gradient candidate
K. Verify replay and all-masked zero gradients
L. Verify mutation firewall and publish artifacts
```

Physical PASS token:

```text
PASS_ASH_BASETRAIN_G204D_FRESH_G203D_QUALIFIED_FORWARD_BACKWARD_LEASE_EXACT_FORWARD_PARTITION_GENERATION_PINNING_EXACT_FORWARD_ACTIVATION_LINEAGE_EXACT_QKV_MASK_GQA_SCALE_GLOBAL_SOFTMAX_STATE_ACTUAL_BASETRAIN_UPSTREAM_DCONTEXT_CHUNKED_PROBABILITY_RECOMPUTE_BACKWARD_PASS1_DV_DP_ROWDOT_DETERMINISTIC_DV_REDUCTION_BACKWARD_PASS2_DSCORE_DQ_DK_DETERMINISTIC_DK_REDUCTION_GQA_SHARED_KV_GRADIENT_REDUCTION_CAUSAL_PADDING_ALL_MASKED_ZERO_GRADIENT_FIRST_MIDDLE_LAST_LAYER_CHUNK_BOUNDARY_MIXED_PRECISION_DQ_DK_DV_PARITY_SELECTED_QKV_PROJECTION_GRADIENT_BINDING_CPU_F64_SMALL_ORACLE_DIRECTIONAL_FINITE_DIFFERENCE_DETERMINISTIC_BACKWARD_REPLAY_VRAM_PLATEAU_NO_FULL_SCORE_MATRIX_NO_FULL_PROBABILITY_MATRIX_NO_FULL_DP_MATRIX_NO_FULL_DSCORE_MATRIX_NO_FLOAT_ATOMIC_NO_HOST_REDUCTION_NO_STALE_FORWARD_RECEIPT_NO_FULL_MODEL_GRADIENT_SCOPE_NO_GRADIENT_WEIGHT_ALIAS_NO_OPTIMIZER_CREATE_NO_OPTIMIZER_STEP_NO_G107_BRIDGE_NO_WEIGHT_DELTA_NO_WEIGHT_MUTATION_NO_CHECKPOINT_WRITE_NO_DEFAULT_ROUTE_PROMOTION_NO_DECODE_ROUTE_MUTATION_NO_SILENT_FALLBACK_SEALED
```

---

# 19. Runtime artifacts

```text
workspace/runtime/basetrain/g204d/
  ash_basetrain_g204d_verification_runtime_specification.json
  ash_basetrain_g204d_verification_runtime_artifact.json
  ash_basetrain_g204d_verification_local_manifest.json
  ash_basetrain_g204d_physical_runtime_specification.json
  ash_basetrain_g204d_physical_runtime_artifact.json
  ash_basetrain_g204d_physical_local_manifest.json
  scenarios/*/g204d_backward_scenario_receipt.json
```

All runtime artifacts are generated by Rust and excluded from code ZIPs.

---

# 20. Completion state

G204D PASS establishes:

```text
FreshForwardBackwardLease
ExactForwardPartitionPinned
ExactActivationLineagePinned
GlobalSoftmaxStateReplayed
ActualBaseTrainDContextBound
GpuDQDKDVProduced
SelectedQKVGradientCandidateBound
CpuF64OraclePass
DirectionalFiniteDifferencePass
DeterministicBackwardReplay
AllMaskedZeroGradient
NoFullMatrixMaterialization
NoFloatAtomicGradientWrite
NoHostGradientReduction
NoStaleForwardReceipt
NoOptimizerAuthority
NoWeightMutation
NoCheckpointCommit
```

Next patch:

```text
ASH-BASETRAIN-G205D-GRADIENT-ACCUMULATION-OPTIMIZER-CANDIDATE-01
```
