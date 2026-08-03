# ASH-BASETRAIN-G205D-GRADIENT-ACCUMULATION-OPTIMIZER-CANDIDATE-01

## Device-Local Gradient Accumulation /
## Transactional Ping-Pong Generations /
## Exact-Once Loss-Scale Unscale /
## Exact-Once Mean Normalization /
## Global Selected-Group Norm and Clip /
## Isolated Adam Optimizer Candidate /
## CPU-f64 Oracle /
## No Resident State or Weight Mutation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-G205D-GRADIENT-ACCUMULATION-OPTIMIZER-CANDIDATE-01`  
> Build revision: `G205D-g204d-gradient-accumulation-optimizer-candidate-r1`  
> Parent: `ASH-BASETRAIN-G204D-FROZEN-PARTITION-BACKWARD-01`  
> Parent state: `PHYSICAL PASS`  
> Accumulation authority: selected Q/K/V projection gradients only  
> Optimizer authority: isolated candidate preview only  
> Resident optimizer-state authority: none  
> Resident weight authority: none  
> Checkpoint authority: none

---

# 1. Goal

G205D consumes fresh G204D selected Q/K/V projection-gradient bundles, accumulates them in device-local transactional generations, applies exact-once loss-scale unscale and exact-once mean normalization, computes the selected-group global L2 norm and clipping candidate, then evaluates an isolated Adam optimizer candidate against read-only weight and optimizer-state snapshots.

Canonical path:

```text
logical optimizer step
  -> accumulation window lease
  -> fresh G204D microbatch gradient bundles
  -> device-local transactional accumulation
  -> exact-once loss-scale unscale
  -> exact-once 1/N normalization
  -> finite scan
  -> global selected-group L2 norm
  -> gradient clip candidate
  -> read-only resident weight and optimizer-state snapshots
  -> isolated Adam m/v/delta preview
  -> CPU-f64 oracle
  -> quarantine
```

G205D must not invoke G108, create a weight-delta materialization candidate, mutate resident optimizer state or resident weights, write checkpoints, or commit the training cursor.

---

# 2. Parent authority

Required parent token:

```text
PASS_ASH_BASETRAIN_G204D_FRESH_G203D_QUALIFIED_FORWARD_BACKWARD_LEASE_EXACT_FORWARD_PARTITION_GENERATION_PINNING_EXACT_FORWARD_ACTIVATION_LINEAGE_EXACT_QKV_MASK_GQA_SCALE_GLOBAL_SOFTMAX_STATE_ACTUAL_BASETRAIN_UPSTREAM_DCONTEXT_CHUNKED_PROBABILITY_RECOMPUTE_BACKWARD_PASS1_DV_DP_ROWDOT_DETERMINISTIC_DV_REDUCTION_BACKWARD_PASS2_DSCORE_DQ_DK_DETERMINISTIC_DK_REDUCTION_GQA_SHARED_KV_GRADIENT_REDUCTION_CAUSAL_PADDING_ALL_MASKED_ZERO_GRADIENT_FIRST_MIDDLE_LAST_LAYER_CHUNK_BOUNDARY_MIXED_PRECISION_DQ_DK_DV_PARITY_SELECTED_QKV_PROJECTION_GRADIENT_BINDING_CPU_F64_SMALL_ORACLE_DIRECTIONAL_FINITE_DIFFERENCE_DETERMINISTIC_BACKWARD_REPLAY_VRAM_PLATEAU_NO_FULL_SCORE_MATRIX_NO_FULL_PROBABILITY_MATRIX_NO_FULL_DP_MATRIX_NO_FULL_DSCORE_MATRIX_NO_FLOAT_ATOMIC_NO_HOST_REDUCTION_NO_STALE_FORWARD_RECEIPT_NO_FULL_MODEL_GRADIENT_SCOPE_NO_GRADIENT_WEIGHT_ALIAS_NO_OPTIMIZER_CREATE_NO_OPTIMIZER_STEP_NO_G107_BRIDGE_NO_WEIGHT_DELTA_NO_WEIGHT_MUTATION_NO_CHECKPOINT_WRITE_NO_DEFAULT_ROUTE_PROMOTION_NO_DECODE_ROUTE_MUTATION_NO_SILENT_FALLBACK_SEALED
```

Every admitted microbatch bundle must bind a fresh G204D backward lease and selected Q/K/V projection-gradient receipt. A previous-process JSON artifact is not a live gradient lease.

---

# 3. Accumulation window lease

The lease binds:

```text
training run
logical optimizer step
expected microbatch count
canonical microbatch ordinal set
model partition
checkpoint
tokenizer and vocabulary
selected parameter-set digest
parameter layout digest
selected scalar count
loss-scale profile
normalization policy
optimizer profile
runtime/device/queue epoch
```

Duplicate, missing, out-of-order, stale, cross-window, cross-layout, cross-checkpoint or cross-selected-group bundles are rejected before accumulation.

---

# 4. Gradient bundle contract

Each bundle binds:

```text
window id
microbatch ordinal
G204D backward lease digest
selected QKV projection binding digest
BaseTrain invocation digest
source batch digest
token count
Q/K/V projection-gradient digests
selected scalar count
upstream loss scale
scaled-gradient digest
finite-scan result
upstream pre-divide flag
```

The canonical selected-group order is:

```text
attention.q_proj
attention.k_proj
attention.v_proj
```

Full-model gradient scope is forbidden.

---

# 5. Exact scaling semantics

Microbatch gradients are admitted without division by the accumulation count.

```text
G_sum = sum_i(unscale(G_i))
G_mean = G_sum / N
```

Required properties:

```text
one unscale per admitted bundle
one final normalization per window
normalization divisor = expected microbatch count
normalization divisor = admitted microbatch count
upstream pre-divide by accumulation count = false
normalization operation count = 1
```

Double normalization, missing normalization and mixed loss-scale profiles are rejected.

---

# 6. Transactional device-local accumulator

For each microbatch:

```text
stable generation A
  + admitted bundle
  -> candidate generation B
  -> finite scan
  -> submission fence
  -> publish B
  -> retire A
```

If the candidate contains non-finite values or violates lineage, B is discarded, A remains stable and the window is poisoned. Host accumulation and float atomic accumulation are forbidden.

---

# 7. Global norm and clipping

After exact-once normalization:

```text
sum_sq = deterministic_sum(g_j^2)
norm = sqrt(sum_sq)
clip_coefficient = min(1, max_norm / (norm + epsilon))
g_clipped = g_mean * clip_coefficient
```

The reduction uses deterministic device-local partials and canonical final reduction. Required scenarios include clip-active, clip-inactive and all-zero gradients.

---

# 8. Optimizer profile

The optimizer profile explicitly binds:

```text
algorithm = adam
learning rate
beta1
beta2
epsilon
bias correction
weight decay
weight decay mode
```

Allowed weight-decay modes:

```text
none
coupled_l2
adamw_decoupled
```

No implicit AdamW or silent decay-mode substitution is permitted.

---

# 9. Isolated optimizer candidate

The candidate consumes:

```text
clipped selected-group gradient
read-only resident weight snapshot
read-only resident m snapshot
read-only resident v snapshot
source optimizer step
sealed optimizer profile
```

It produces isolated candidate buffers only:

```text
m_candidate
v_candidate
optimizer delta preview
candidate step
```

Required counters:

```text
optimizer_delta_preview_created = 1
weight_delta_materialization_candidate_created = 0
resident_optimizer_state_write = 0
resident_weight_write = 0
G108 invocation = 0
```

The delta preview has no weight writer, pointer-swap, checkpoint or training-cursor authority.

---

# 10. CPU-f64 oracle

The oracle independently computes:

```text
microbatch unscale
window sum and mean
global L2 norm
clip coefficient
clipped gradient
Adam m candidate
Adam v candidate
bias correction
weight-decay semantics
optimizer delta preview
```

GPU results are compared with digest-pinned absolute, relative and relative-floor tolerances.

---

# 11. Replay

Every scenario group executes at least twice. Replay compares stable semantic lineage and:

```text
canonical bundle order digest
final accumulator digest
normalized gradient digest
norm and clip values
clipped gradient digest
m candidate digest
v candidate digest
delta preview digest
```

Run-unique submission and receipt identities are not tensor-content identity.

---

# 12. Physical matrix

Required groups:

```text
N=1, no clipping, zero optimizer state
N=2, mixed-sign gradients
N=4, clipping active
N=4, all-zero gradient
N=2, non-unit loss scale
N=4, nonzero resident m/v
```

Each group executes at least two repeats.

Negative controls:

```text
duplicate ordinal
missing ordinal
out-of-order ordinal
stale bundle
selected-group mismatch
parameter-layout mismatch
loss-scale mismatch
upstream pre-divide
double normalization
non-finite gradient
optimizer-state generation drift
weight generation drift
G108 invocation
resident state or weight mutation
checkpoint write
```

---

# 13. Mutation firewall

Required zero counters:

```text
resident optimizer-state write
resident optimizer-state generation increment
resident weight write
resident weight generation increment
weight-delta materialization candidate
G108 invocation
weight writer lease
weight writer lock
weight apply
weight commit
LoRA weight commit
checkpoint write
checkpoint finalize
checkpoint pointer update
training cursor commit
default route promotion
Decode route mutation
quality claim
silent fallback
```

---

# 14. Implementation surface

```text
crates/model_core/src/base_train_g205d_gradient_accumulation_optimizer_candidate.rs
crates/base_train/src/base_train_g205d_gradient_accumulation_optimizer_candidate.rs
crates/burn_webgpu_backend/src/base_train_g205d_gradient_accumulation_probe.rs
crates/burn_webgpu_backend/src/base_train_g205d_optimizer_candidate_probe.rs
crates/burn_webgpu_backend/src/shaders/base_train_g205d_gradient_accumulate.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_g205d_gradient_finalize.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_g205d_optimizer_candidate.wgsl
crates/orchestrator_local/src/base_train_g205d_cli_registry.rs
crates/orchestrator_local/src/base_train_g205d_scenario_plan.rs
crates/orchestrator_local/src/bin/ash_basetrain_g205d_verification_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_g205d_physical_gate.rs
specs/cli/ash_basetrain_g205d_verification.args
specs/cli/ash_basetrain_g205d_physical.args
```

All public surfaces use direct crate-root exports. Runtime artifacts are generated by Rust and excluded from code ZIPs.

---

# 15. Verification gate

Binary:

```text
ash_basetrain_g205d_verification_gate
```

Verification PASS token:

```text
PASS_ASH_BASETRAIN_G205D_GRADIENT_ACCUMULATION_WINDOW_TRANSACTIONAL_GENERATIONS_EXACT_ONCE_UNSCALE_NORMALIZATION_GLOBAL_NORM_CLIP_ISOLATED_OPTIMIZER_CANDIDATE_CPU_F64_ORACLE_NO_RESIDENT_STATE_OR_WEIGHT_MUTATION_STATIC_VERIFICATION_SEALED
```

---

# 16. Physical gate

Binary:

```text
ash_basetrain_g205d_physical_gate
```

Physical phases:

```text
A. Verify G204D parent artifact and manifest
B. Bootstrap one native WGPU runtime
C. Execute fresh G204D backward bundles
D. Validate accumulation-window lineage and ordinal sequence
E. Accumulate through transactional device-local generations
F. Unscale and normalize exactly once
G. Compute global norm and clipping candidate
H. Capture read-only weight and optimizer-state snapshots
I. Execute isolated Adam optimizer candidate
J. Compare accumulation, clip and optimizer outputs against CPU-f64 oracle
K. Verify replay, negative controls and VRAM plateau
L. Verify mutation firewall and publish final seal
```

Physical PASS token:

```text
PASS_ASH_BASETRAIN_G205D_FRESH_G204D_SELECTED_QKV_PROJECTION_GRADIENT_BUNDLES_EXACT_ACCUMULATION_WINDOW_LINEAGE_CANONICAL_MICROBATCH_ORDINAL_ZERO_ONE_TWO_THREE_EXACT_SELECTED_PARAMETER_AUTHORITY_DEVICE_LOCAL_F32_TRANSACTIONAL_PING_PONG_ACCUMULATOR_GENERATIONS_LOSS_SCALE_UNSCALE_EXACTLY_ONCE_MEAN_BY_MICROBATCH_FINAL_NORMALIZATION_EXACTLY_ONCE_PER_BUNDLE_FINITE_SCAN_PER_GENERATION_FINITE_SCAN_FINAL_GRADIENT_FINITE_GLOBAL_SELECTED_GROUP_L2_NORM_DETERMINISTIC_PARTIAL_REDUCTION_GRADIENT_CLIP_CANDIDATE_CLIP_ACTIVE_AND_INACTIVE_ZERO_GRADIENT_CONTRACT_READ_ONLY_RESIDENT_WEIGHT_SNAPSHOT_READ_ONLY_RESIDENT_OPTIMIZER_STATE_SNAPSHOT_ATOMIC_ISOLATED_ADAM_OPTIMIZER_CANDIDATE_STEP_CANDIDATE_M_CANDIDATE_V_CANDIDATE_STEP_OPTIMIZER_DELTA_PREVIEW_CPU_F64_ACCUMULATION_NORM_CLIP_OPTIMIZER_ORACLE_DETERMINISTIC_REPLAY_VRAM_PLATEAU_DUPLICATE_MISSING_OUT_OF_ORDER_STALE_NONFINITE_GENERATION_DRIFT_NEGATIVE_CONTROLS_G106_G69_G107_LINEAGE_NO_HOST_ACCUMULATION_NO_FLOAT_ATOMIC_NO_FULL_MODEL_GRADIENT_SCOPE_NO_DYNAMIC_LOSS_SCALE_COMMIT_NO_RESIDENT_OPTIMIZER_STATE_WRITE_NO_G108_NO_WEIGHT_DELTA_MATERIALIZATION_NO_RESIDENT_WEIGHT_WRITE_NO_WEIGHT_COMMIT_NO_CHECKPOINT_WRITE_NO_CHECKPOINT_FINALIZE_NO_TRAINING_CURSOR_COMMIT_NO_DEFAULT_ROUTE_PROMOTION_NO_DECODE_ROUTE_MUTATION_NO_QUALITY_CLAIM_NO_SILENT_FALLBACK_SEALED
```

---

# 17. Completion state

G205D PASS establishes:

```text
FreshG204DGradientBundles
ExactAccumulationWindowLineage
CanonicalMicrobatchOrdinalSequence
DeviceLocalTransactionalAccumulation
ExactOnceLossScaleUnscale
ExactOnceMeanNormalization
FiniteGlobalSelectedGroupNorm
GradientClipCandidate
ReadOnlyResidentWeightAndOptimizerSnapshots
IsolatedAdamOptimizerCandidate
CandidateMAndV
OptimizerDeltaPreview
CpuF64OraclePass
DeterministicReplay
NoHostAccumulation
NoFloatAtomic
NoResidentOptimizerStateWrite
NoG108
NoWeightDeltaMaterialization
NoResidentWeightWrite
NoWeightCommit
NoCheckpointCommit
```

Next patch:

```text
ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01
```
