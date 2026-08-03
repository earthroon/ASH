# ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01

## G205D Optimizer Delta Preview Consumption /
## Selected Weight Addressability Closure /
## QKV Group Offset·Length·Stride Binding /
## Exact Target Weight Generation Pinning /
## Device-Local F32 Delta Materialization /
## Bitwise Preview-Slice Parity /
## Per-Group and Global Delta Digests /
## Immutable Delta Buffer Seal /
## Alias and Apply Firewall /
## No Resident Weight Mutation /
## No Pointer Swap·Commit·Checkpoint Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01`  
> Build revision: `G206D-g205d-isolated-weight-delta-materialization-r1`  
> Parent: `ASH-BASETRAIN-G205D-GRADIENT-ACCUMULATION-OPTIMIZER-CANDIDATE-01`  
> Parent state: `PHYSICAL PASS`  
> Materialization authority: selected Q/K/V weight-delta candidate only  
> Delta apply authority: none  
> Resident weight writer authority: none  
> Optimizer-state commit authority: none  
> Pointer-swap authority: none  
> Checkpoint authority: none

---

# 1. Goal

G206D promotes the numerically qualified G205D optimizer delta preview into a physically materialized, device-local, selected-weight delta candidate.

```text
fresh G205D optimizer candidate
  -> live optimizer delta preview buffer
  -> exact selected Q/K/V weight layout
  -> target weight generation pinning
  -> device-local u32 bit-pattern materialization
  -> per-group and global digest sealing
  -> finite and alias firewall
  -> immutable isolated delta buffer
  -> quarantine
```

G206D does not apply the delta, acquire a writer lease, mutate resident weights or optimizer state, swap pointers, write checkpoints, or commit a training cursor.

---

# 2. Parent authority

Required parent token:

```text
PASS_ASH_BASETRAIN_G205D_FRESH_G204D_SELECTED_QKV_PROJECTION_GRADIENT_BUNDLES_EXACT_ACCUMULATION_WINDOW_LINEAGE_CANONICAL_MICROBATCH_ORDINAL_ZERO_ONE_TWO_THREE_EXACT_SELECTED_PARAMETER_AUTHORITY_DEVICE_LOCAL_F32_TRANSACTIONAL_PING_PONG_ACCUMULATOR_GENERATIONS_LOSS_SCALE_UNSCALE_EXACTLY_ONCE_MEAN_BY_MICROBATCH_FINAL_NORMALIZATION_EXACTLY_ONCE_PER_BUNDLE_FINITE_SCAN_PER_GENERATION_FINITE_SCAN_FINAL_GRADIENT_FINITE_GLOBAL_SELECTED_GROUP_L2_NORM_DETERMINISTIC_PARTIAL_REDUCTION_GRADIENT_CLIP_CANDIDATE_CLIP_ACTIVE_AND_INACTIVE_ZERO_GRADIENT_CONTRACT_READ_ONLY_RESIDENT_WEIGHT_SNAPSHOT_READ_ONLY_RESIDENT_OPTIMIZER_STATE_SNAPSHOT_ATOMIC_ISOLATED_ADAM_OPTIMIZER_CANDIDATE_STEP_CANDIDATE_M_CANDIDATE_V_CANDIDATE_STEP_OPTIMIZER_DELTA_PREVIEW_CPU_F64_ACCUMULATION_NORM_CLIP_OPTIMIZER_ORACLE_DETERMINISTIC_REPLAY_VRAM_PLATEAU_DUPLICATE_MISSING_OUT_OF_ORDER_STALE_NONFINITE_GENERATION_DRIFT_NEGATIVE_CONTROLS_G106_G69_G107_LINEAGE_NO_HOST_ACCUMULATION_NO_FLOAT_ATOMIC_NO_FULL_MODEL_GRADIENT_SCOPE_NO_DYNAMIC_LOSS_SCALE_COMMIT_NO_RESIDENT_OPTIMIZER_STATE_WRITE_NO_G108_NO_WEIGHT_DELTA_MATERIALIZATION_NO_RESIDENT_WEIGHT_WRITE_NO_WEIGHT_COMMIT_NO_CHECKPOINT_WRITE_NO_CHECKPOINT_FINALIZE_NO_TRAINING_CURSOR_COMMIT_NO_DEFAULT_ROUTE_PROMOTION_NO_DECODE_ROUTE_MUTATION_NO_QUALITY_CLAIM_NO_SILENT_FALLBACK_SEALED
```

A previous-process digest is lineage evidence only. Physical materialization consumes a fresh live G205D delta-preview buffer in the current runtime.

---

# 3. Selected weight addressability

Required groups and order:

```text
attention.q_proj
attention.k_proj
attention.v_proj
```

Each range binds:

```text
group ID and ordinal
base scalar offset
scalar count
scalar and row stride
dtype and storage profile
target tensor identity digest
target weight generation
target weight snapshot digest
```

Initial profile:

```text
delta dtype       f32
target view       exact f32 master or isolated f32 shadow
scalar stride     1
packing           contiguous Q then K then V
```

Rejected:

```text
activation-gradient layout used as weight layout
unknown target tensor identity
overlap or gap
out-of-bounds or zero-length range
Q/K/V reorder
implicit f16, bf16, quantized conversion
weight generation or snapshot drift
```

---

# 4. Materialization semantics

The initial materializer is an identity-preserving bit copy.

```text
materialized_delta_bits[i] = source_delta_preview_bits[i]
```

It must not recompute or reapply:

```text
learning rate
weight decay
bias correction
clip coefficient
loss-scale unscale
microbatch normalization
sign inversion
dtype conversion
compression or quantization
```

Required zero counters:

```text
delta recompute
learning-rate reapply
weight-decay reapply
clip reapply
normalization reapply
```

---

# 5. Device-local kernel

Kernel:

```text
g206d_materialize
```

Bindings:

```text
uniform scalar count
read-only source delta bits array<u32>
write-only isolated destination bits array<u32>
integer finite-status word
```

WGSL finite predicate:

```wgsl
const F32_EXPONENT_MASK: u32 = 0x7f800000u;
```

NaN and ±Inf are rejected. `-0.0`, subnormal values and all finite payloads are preserved bitwise.

Required:

```text
one writer per destination scalar
float atomic writes = 0
host materialization = 0
source preview mutation = 0
resident weight writable binding = 0
```

---

# 6. Alias and ownership firewall

The destination is a newly allocated dedicated buffer and may not alias:

```text
source delta preview
resident weight
candidate m
candidate v
gradient accumulator
checkpoint staging
```

Lifecycle:

```text
Allocated
  -> Filling
  -> FiniteChecked
  -> DigestSealed
  -> ImmutableQuarantined
  -> Retired
```

The published candidate is immutable and has no apply authority.

---

# 7. Per-group and global parity

For each Q/K/V range:

```text
source slice digest
materialized slice digest
scalar count
range identity
bitwise mismatch count
non-finite count
```

PASS requires:

```text
source slice digest == materialized slice digest
bitwise mismatch count == 0
non-finite count == 0
```

Global digest binds the three group digests, selected layout digest, source optimizer candidate receipt, weight generation and optimizer-state generation.

---

# 8. Replay

Each scenario group executes at least twice. Replay compares semantic identity and:

```text
selected weight layout digest
source delta-preview digest
materialized delta digest
Q/K/V group digests
source weight generation
source optimizer-state generation
candidate step
```

Run-unique submission and receipt IDs are provenance, not tensor-content identity.

---

# 9. Physical matrix

Required scenarios:

```text
default equal-sized selected pack
unequal Q/K/V group sizes
signed zero and subnormal preservation
```

Each scenario runs at least twice.

Negative controls:

```text
range overlap
range gap
wrong group order
scalar-count mismatch
weight-generation drift
weight-snapshot drift
source digest mismatch
non-finite source
source/destination alias claim
G109 invocation
G77 apply invocation
resident write or pointer swap
```

---

# 10. Authority firewall

Required zero counters:

```text
optimizer-state write
G109 invocation
G77 apply
weight writer lease
weight writer lock
resident weight write
resident weight generation increment
pointer swap
weight commit
checkpoint write
checkpoint finalize
training cursor commit
default route promotion
Decode route mutation
quality claim
silent fallback
```

---

# 11. Implementation surface

```text
crates/model_core/src/base_train_g206d_isolated_weight_delta_materialization.rs
crates/base_train/src/base_train_g206d_isolated_weight_delta_materialization.rs
crates/burn_webgpu_backend/src/base_train_g206d_weight_delta_materialization_probe.rs
crates/burn_webgpu_backend/src/shaders/base_train_g206d_weight_delta_materialize.wgsl
crates/burn_webgpu_backend/src/base_train_g205d_optimizer_candidate_probe.rs
crates/orchestrator_local/src/base_train_g206d_cli_registry.rs
crates/orchestrator_local/src/base_train_g206d_scenario_plan.rs
crates/orchestrator_local/src/bin/ash_basetrain_g206d_verification_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_g206d_physical_gate.rs
specs/cli/ash_basetrain_g206d_verification.args
specs/cli/ash_basetrain_g206d_physical.args
```

The G205D optimizer output exposes the live delta-preview buffer in addition to the qualification readback vector. G206D consumes that buffer read-only.

---

# 12. Verification gate

Binary:

```text
ash_basetrain_g206d_verification_gate
```

It verifies direct exports, CLI exactness, implementation files, bit-pattern WGSL, finite predicate, zero float atomic, addressability validation, no apply surfaces and atomic runtime-artifact publication.

Verification PASS token:

```text
PASS_ASH_BASETRAIN_G206D_SELECTED_WEIGHT_ADDRESSABILITY_ISOLATED_DELTA_MATERIALIZATION_BITWISE_PARITY_ALIAS_FIREWALL_NO_APPLY_AUTHORITY_STATIC_VERIFICATION_SEALED
```

---

# 13. Physical gate

Binary:

```text
ash_basetrain_g206d_physical_gate
```

Physical phases:

```text
A. Verify G205D parent artifact and PASS token
B. Bootstrap one native WGPU runtime
C. Produce a fresh live G205D optimizer delta preview
D. Seal selected Q/K/V target weight ranges and generations
E. Dispatch device-local bitwise materialization
F. Verify finite status and bitwise source parity
G. Seal per-group and global digests
H. Verify deterministic replay
I. Verify alias and mutation firewalls
J. Publish immutable quarantined delta receipt
```

Physical PASS token:

```text
PASS_ASH_BASETRAIN_G206D_FRESH_G205D_OPTIMIZER_DELTA_PREVIEW_EXACT_SELECTED_WEIGHT_ADDRESSABILITY_QKV_GROUP_ORDER_OFFSETS_LENGTHS_STRIDES_TARGET_WEIGHT_GENERATIONS_DEVICE_LOCAL_F32_ISOLATED_WEIGHT_DELTA_MATERIALIZATION_BITWISE_PREVIEW_SLICE_PARITY_PER_GROUP_DIGESTS_GLOBAL_DIGEST_FINITE_GUARD_ALIAS_FIREWALL_IMMUTABLE_SEALED_DELTA_BUFFER_REPLAY_VRAM_PLATEAU_G108_LINEAGE_PHYSICAL_PROMOTION_NO_DELTA_RECOMPUTE_NO_LEARNING_RATE_REAPPLY_NO_WEIGHT_DECAY_REAPPLY_NO_OPTIMIZER_STATE_WRITE_NO_G109_NO_G77_APPLY_NO_WEIGHT_WRITER_LEASE_NO_WEIGHT_WRITER_LOCK_NO_RESIDENT_WEIGHT_WRITE_NO_POINTER_SWAP_NO_WEIGHT_COMMIT_NO_CHECKPOINT_WRITE_NO_CHECKPOINT_FINALIZE_NO_TRAINING_CURSOR_COMMIT_NO_DEFAULT_ROUTE_PROMOTION_NO_DECODE_ROUTE_MUTATION_NO_QUALITY_CLAIM_NO_SILENT_FALLBACK_SEALED
```

---

# 14. Completion state

G206D PASS establishes:

```text
FreshG205DLiveDeltaPreview
ExactSelectedWeightAddressability
ExactQKVOffsetsLengthsAndStrides
ExactTargetWeightGeneration
DeviceLocalBitwiseMaterialization
FiniteMaterializedDelta
PerGroupAndGlobalDigestSeal
ImmutableIsolatedDeltaBuffer
DeterministicReplay
NoDeltaRecompute
NoOptimizerStateWrite
NoG109
NoG77Apply
NoResidentWeightWrite
NoPointerSwap
NoWeightCommit
NoCheckpointCommit
```

Next patch:

```text
ASH-BASETRAIN-G207D-ISOLATED-SHADOW-WEIGHT-APPLY-CANDIDATE-01
```
