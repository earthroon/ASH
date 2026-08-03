# ASH-BASETRAIN-G202D-SHARED-ATTENTION-RUNTIME-01

## Decode TensorCube Runtime Reuse /
## BaseTrain Forward Candidate Admission /
## Shared Partition Planner /
## Exact Model Partition Binding /
## Device-Local Training Activation Lease /
## Legacy Training Writer Preservation /
## No Independent Training Attention Fork /
## No Decode Authority Mutation /
## No Weight·Gradient·Optimizer Mutation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-G202D-SHARED-ATTENTION-RUNTIME-01`  
> Build revision: `G202D-w9f-shared-attention-runtime-admission-r1`  
> Parent: `ASH-ATTN-DECODE-W9F-R1D`  
> Parent state: `PHYSICAL PASS`  
> Decode production writer: `TensorCube`  
> BaseTrain current writer: existing legacy training attention route  
> G202D candidate: shared TensorCube Stage10·11·12 runtime consumer  
> Backward authority: none  
> Gradient authority: none  
> Optimizer authority: none  
> Weight mutation authority: none

---

# 1. Goal

G202D admits BaseTrain forward as a candidate consumer of the already qualified Decode TensorCube runtime. It does not create a training-specific attention implementation.

Canonical path:

```text
BaseTrain prepared training invocation
  -> exact model/checkpoint/tokenizer binding
  -> shared partition planner
  -> shared TensorCube runtime holder
  -> Stage10 score statistics
  -> Stage11 global online softmax
  -> Stage12 weighted V accumulation
  -> device-local activation candidate
  -> quarantine and fence retirement
```

Required invariants:

```text
same WGPU device and queue
same partition planner implementation
same Stage10·11·12 implementation family
actual BaseTrain-owned training invocation and Q/K/V lineage
candidate activation remains non-committable
legacy training writer unchanged
Decode TensorCube writer unchanged
backward, gradient, optimizer, weight, checkpoint mutations = 0
```

---

# 2. Authority map

```text
Decode runtime writer
  TensorCube production authority

BaseTrain default writer
  existing legacy training attention

G202D shared TensorCube lane
  candidate only
  downstream commit forbidden
  backward forbidden
```

G202D PASS does not promote TensorCube as the BaseTrain default writer.

---

# 3. Shared runtime SSOT

The runtime identity binds:

```text
runtime holder
WGPU device
WGPU queue
model partition
exact device profile
partition planner implementation
Stage10 implementation
Stage11 implementation
Stage12 implementation
stage bundle
pipeline layout
shader bundle
```

Creating a second device, queue, persistent pipeline family, shader bundle, or training-only partition planner is forbidden.

The physical gate performs one native bootstrap and reuses that bootstrap for every BaseTrain candidate scenario and the W8 shared runtime runner.

---

# 4. BaseTrain source authority

Every candidate invocation is created through the BaseTrain crate and binds:

```text
training run id
forward step
microbatch
layer
model partition
checkpoint
tokenizer
vocabulary
causal mask snapshot
batch and sequence geometry
Q/K/V source generations
fixture seed used by the physical qualification harness
source surface = BaseTrainPreparedTrainingInvocation
```

Decode fixture sources, cross-layer Q/K/V, cross-microbatch generations, or mismatched model/checkpoint/tokenizer inputs are denied.

---

# 5. Shared partition planner

Decode and BaseTrain use the same planner implementation, chunk ordering, mask semantics, and GQA mapping. They do not share one mutable invocation instance.

Forbidden:

```text
training-only planner implementation
training-only chunk order
training-only mask interpretation
training-only GQA mapping
training-only Stage10·11·12 shaders
```

---

# 6. Physical dispatch

The candidate path executes the existing W8 physical runner with one shared native bootstrap.

Minimum scenario matrix:

```text
layers: first, middle, last
sequence lengths: 8 and 16
batch: 1
mask: causal
```

For every scenario the gate requires:

```text
Stage10 dispatch observed
Stage11 dispatch observed
Stage12 dispatch observed
device-local candidate activation live
activation shape/layout/dtype exact
non-finite count = 0
candidate output commit count = 0
full score matrix allocation = 0
full probability matrix allocation = 0
full context readback = 0
replay/global-state owners retire after fence
```

---

# 7. Writer preservation

Before and after the candidate matrix, the gate snapshots:

```text
BaseTrain legacy training writer
Decode TensorCube production writer
```

Both must remain byte-identical in semantic identity. Route epochs and production authority are not modified.

---

# 8. Mutation firewall

Required zero counters:

```text
base-weight mutation
LoRA-weight mutation
gradient buffer writes
optimizer state writes
checkpoint writes
training cursor commits
Decode route mutation
BaseTrain default route mutation
silent legacy fallback
```

A candidate failure is a gate failure. It cannot execute the legacy path and still emit a G202D PASS.

---

# 9. Crate-root ABI rule

W9F exposed repeated indirect-registry failures, so G202D uses explicit crate-root exports from the first revision.

```text
model_core
  direct pub mod + pub use

base_train
  direct pub mod + pub use

burn_webgpu_backend
  direct probe module and explicit function/type pub use

orchestrator_local
  direct pub mod declarations
```

Registry-only `include!` exports are forbidden for the G202D public ABI.

---

# 10. Implementation surface

```text
crates/model_core/src/base_train_g202d_shared_attention_runtime.rs
crates/base_train/src/base_train_g202d_shared_attention_runtime.rs
crates/burn_webgpu_backend/src/base_train_g202d_shared_runtime_probe.rs
crates/orchestrator_local/src/base_train_g202d_cli_registry.rs
crates/orchestrator_local/src/base_train_g202d_scenario_plan.rs
crates/orchestrator_local/src/bin/ash_basetrain_g202d_verification_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_g202d_physical_gate.rs
specs/cli/ash_basetrain_g202d_verification.args
specs/cli/ash_basetrain_g202d_physical.args
```

No new WGSL file is admitted. Existing Stage10·11·12 implementations are reused.

---

# 11. Verification gate

Binary:

```text
ash_basetrain_g202d_verification_gate
```

It verifies:

```text
CLI registry exactness
source and Cargo surface presence
no training-specific Stage10·11·12 shader files
first/middle/last scenario coverage
valid BaseTrain invocation identity
foreign source negative control
mutation firewall negative surface
runtime artifact atomic write and readback verification
```

Verification PASS token:

```text
PASS_ASH_BASETRAIN_G202D_SHARED_ATTENTION_RUNTIME_SOURCE_SURFACE_SHARED_PARTITION_PLANNER_ACTUAL_BASETRAIN_QKV_DEVICE_LOCAL_ACTIVATION_LEASE_NO_INDEPENDENT_TRAINING_ATTENTION_FORK_STATIC_VERIFICATION_SEALED
```

---

# 12. Physical gate

Binary:

```text
ash_basetrain_g202d_physical_gate
```

Physical phases:

```text
A. Verify W9F parent artifact and manifest
B. Bootstrap one native WGPU device and queue
C. Seal the shared runtime identity
D. Create BaseTrain-owned training invocation identities
E. Run W8 physical Stage10·11·12 for first/middle/last layers
F. Observe live device-local candidate activation
G. Deny candidate commit and all mutation authority
H. Retire replay and global-state owners after fence
I. Verify legacy training and Decode writer preservation
J. Publish G202D runtime artifact and no-fork seal
```

Physical PASS token:

```text
PASS_ASH_BASETRAIN_G202D_DECODE_TENSORCUBE_RUNTIME_REUSE_BASETRAIN_FORWARD_CANDIDATE_ADMISSION_SHARED_RUNTIME_HOLDER_SHARED_PARTITION_PLANNER_EXACT_MODEL_PARTITION_EXACT_CHECKPOINT_EXACT_TOKENIZER_ACTUAL_BASETRAIN_QKV_TRAINING_PREFILL_STAGE10_STAGE11_STAGE12_DEVICE_LOCAL_ACTIVATION_LEASE_FENCE_RETIREMENT_LEGACY_TRAINING_WRITER_PRESERVATION_DECODE_PRODUCTION_WRITER_PRESERVATION_NO_INDEPENDENT_TRAINING_ATTENTION_FORK_NO_TRAINING_SPECIFIC_ATTENTION_SHADER_NO_TRAINING_SPECIFIC_ATTENTION_PIPELINE_NO_DEFAULT_TRAINING_ROUTE_PROMOTION_NO_BACKWARD_NO_GRADIENT_WRITE_NO_OPTIMIZER_WRITE_NO_WEIGHT_MUTATION_NO_CHECKPOINT_WRITE_NO_FULL_SCORE_MATRIX_NO_FULL_PROBABILITY_MATRIX_NO_FULL_CONTEXT_READBACK_NO_SILENT_FALLBACK_SEALED
```

---

# 13. Runtime artifacts

```text
workspace/runtime/basetrain/g202d/
  ash_basetrain_g202d_verification_runtime_specification.json
  ash_basetrain_g202d_verification_runtime_artifact.json
  ash_basetrain_g202d_verification_local_manifest.json
  ash_basetrain_g202d_runtime_specification.json
  ash_basetrain_g202d_runtime_artifact.json
  ash_basetrain_g202d_local_manifest.json
  parent_authority_receipt.json
  shared_runtime_identity_receipt.json
  training_invocation_receipts.json
  mutation_firewall_receipt.json
  final_no_independent_training_attention_fork_seal.json
```

All runtime artifacts are produced by Rust and excluded from code ZIPs.

---

# 14. Completion state

```text
Decode Attention
  TensorCubeProductionWriter
  Unchanged

BaseTrain Attention
  LegacyWriterUnchanged
  SharedTensorCubeCandidateAdmitted

Runtime
  OneNativeBootstrap
  SharedDeviceAndQueue
  SharedPartitionPlanner
  SharedStage10·11·12

Training Candidate
  BaseTrainInvocationBound
  ExactModelPartitionBound
  DeviceLocalActivationProduced
  NonCommittable
  FenceRetired

Mutation
  BackwardDisabled
  GradientDisabled
  OptimizerDisabled
  WeightMutationDisabled
  CheckpointCommitDisabled

Safety
  NoIndependentTrainingAttentionFork
  NoDecodeAuthorityMutation
  NoSilentFallback
```

Next patch:

```text
ASH-BASETRAIN-G203D-FORWARD-PARITY-01

Legacy Training Attention Oracle /
Shared TensorCube Training Forward Candidate /
Full-Sequence Causal Prefill /
Activation Layout Parity /
Mask·GQA·Scale Parity /
Mixed-Precision Profile /
Layer Matrix /
No Gradient Authority Seal
```