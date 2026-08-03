# ASH-BASETRAIN-G203D-FORWARD-PARITY-01

## Legacy Training Attention Oracle /
## Shared TensorCube Training Forward Candidate /
## Exact Q·K·V Snapshot Dual Consumption /
## Full-Sequence Causal Prefill /
## Context·Activation ABI Parity /
## Mask·GQA·Scale Semantic Parity /
## Mixed-Precision Tolerance Profile /
## First·Middle·Last Layer Matrix /
## Deterministic Replay /
## No Gradient·Optimizer Authority /
## No Default Training Route Promotion Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-G203D-FORWARD-PARITY-01`  
> Build revision: `G203D-g202d-training-forward-parity-r1`  
> Parent: `ASH-BASETRAIN-G202D-SHARED-ATTENTION-RUNTIME-01`  
> Parent state: `PHYSICAL PASS`  
> Decode parent: `ASH-ATTN-DECODE-W9F-R1D`  
> Oracle authority: existing legacy BaseTrain attention  
> Candidate authority: shared TensorCube Stage10·11·12  
> Backward authority: none  
> Gradient authority: none  
> Optimizer authority: none  
> Weight mutation authority: none  
> Default training route promotion: forbidden

---

# 1. Goal

G203D proves that the G202D shared TensorCube training candidate is numerically equivalent to the existing BaseTrain legacy attention oracle when both consume one exact immutable training-forward input snapshot.

Canonical path:

```text
BaseTrain prepared training invocation
  -> immutable Q/K/V + mask + GQA + scale snapshot
  -> Legacy Training Attention Oracle
  -> Shared TensorCube Stage10·11·12 Candidate
  -> compact device-local parity receipt
  -> bounded qualification metrics
  -> quarantine
```

Required invariants:

```text
same Q/K/V content and generation
same mask snapshot
same causal and padding semantics
same GQA mapping
same attention scale semantics
same output shape/layout/dtype contract
context values within one digest-pinned tolerance profile
first/middle/last layer coverage
chunk-boundary coverage
deterministic replay
candidate commit count = 0
backward, gradient, optimizer, weight and checkpoint mutations = 0
```

---

# 2. Authority map

```text
Legacy BaseTrain attention
  numerical oracle
  current BaseTrain writer

Shared TensorCube candidate
  parity candidate only
  no residual commit
  no default-route promotion
  no backward authority

Canonical tolerance registry
  fixed for one gate run
  digest pinned
  auto widening forbidden
```

G203D PASS does not promote TensorCube as the BaseTrain default writer.

---

# 3. Exact input snapshot

Every parity scenario binds:

```text
training run and forward step
microbatch and layer
model partition
checkpoint
tokenizer and vocabulary
batch and sequence geometry
Q/K/V buffer identity, range, generation and content digest
mask snapshot
GQA mapping
attention scale semantics
precision profile
```

Oracle and candidate must reference the same snapshot digest. Any cross-layer, cross-microbatch or mutated snapshot is rejected.

The physical implementation binds the BaseTrain-owned invocation to the existing W8 exact physical runner. The W8 runner exports Q/K/V GPU fingerprints, source generations, compact Headwise-vs-TensorCube context parity metrics and candidate context digests.

---

# 4. Oracle contract

The oracle is the existing legacy BaseTrain attention path represented by the qualified W8 Headwise FullActive context surface. G203D must not implement a separate CPU or synthetic oracle.

The oracle receipt binds:

```text
input snapshot digest
oracle route and implementation identity
output shape/layout/dtype
finite and non-finite counts
compact context fingerprint
writer commit count
```

---

# 5. Candidate contract

The candidate reuses the G202D shared runtime holder and the existing W8 TensorCube route:

```text
same native WGPU bootstrap
same device and queue
same partition planner
same Stage10
same Stage11
same Stage12
```

The candidate remains shadow-only and non-committable.

---

# 6. Numerical parity

Every required scenario evaluates the existing compact W8 parity receipt:

```text
compared scalar count
mismatch count
oracle and candidate non-finite counts
all-masked nonzero counts
max absolute error
max relative error
layout guard violations
buffer bounds violations
GQA mapping violations
causal and mask snapshot violations
compare and finalize dispatch counts
compact status readback count
full context readback count
context materialization copy count
```

PASS requires all violation and mismatch counters to be zero and maximum errors to remain within the fixed tolerance profile.

No full score matrix, probability matrix or full context materialization is admitted.

---

# 7. Mask, GQA and scale semantics

Required mask profiles:

```text
causal full-valid
causal padded tail
all-masked row contract
chunk-boundary causal rows
```

All-masked rows must produce finite zero context.

The actual model Q-head to KV-head mapping and the existing attention scale contract are used. G203D may not introduce training-only mapping or scale semantics.

---

# 8. Physical matrix

Required layers:

```text
first
middle
last
```

Required sequence coverage:

```text
8
16
chunk_size - 1
chunk_size
chunk_size + 1
```

Each scenario group executes at least twice. Repeat receipts must preserve:

```text
Q digest
K digest
V digest
candidate context digest
mismatch count
max absolute error bits
max relative error bits
```

Execution uses one paired device-local Headwise/TensorCube invocation, preventing source drift between routes.

---

# 9. Tolerance registry

The canonical tolerance profile binds:

```text
absolute tolerance
relative tolerance
relative floor
profile source
auto-widen allowed = false
profile digest
```

Tolerance values are supplied by the sealed CLI profile and recorded in the runtime artifact. Runtime widening, fallback to a looser profile or silent precision downgrade is forbidden.

---

# 10. Replay and resource closure

Required replay properties:

```text
same snapshot across repeats
same Q/K/V GPU fingerprints
same candidate context digest
same compact error metrics
same PASS state
```

Scenario-local replay owners, global-state owners and compact readback buffers must retire after the submission fence. Unbounded context retention or monotonic VRAM growth is forbidden.

---

# 11. Mutation firewall

Required zero counters:

```text
candidate commit
default route promotion
backward dispatch
gradient write
optimizer write
base or LoRA weight mutation
checkpoint write
tolerance auto widening
silent fallback
```

Legacy BaseTrain writer and Decode TensorCube production writer must be unchanged before and after the matrix.

---

# 12. Implementation surface

```text
crates/model_core/src/base_train_g203d_forward_parity.rs
crates/base_train/src/base_train_g203d_forward_parity.rs
crates/orchestrator_local/src/base_train_g203d_cli_registry.rs
crates/orchestrator_local/src/base_train_g203d_scenario_plan.rs
crates/orchestrator_local/src/attention_interconnect_w8_physical_runner.rs
crates/orchestrator_local/src/bin/ash_basetrain_g203d_verification_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_g203d_physical_gate.rs
specs/cli/ash_basetrain_g203d_verification.args
specs/cli/ash_basetrain_g203d_physical.args
```

No new G203D WGSL file is admitted.

All G203D public modules use direct crate-root exports. Registry-only `include!` ABI publication is forbidden.

---

# 13. Verification gate

Binary:

```text
ash_basetrain_g203d_verification_gate
```

It verifies:

```text
G202D parent source surface
CLI registry exactness
Cargo bin registration
direct crate-root ABI
legacy oracle and TensorCube candidate surfaces
exact input snapshot validation
scenario matrix coverage
tolerance profile sealing
candidate-commit negative control
mutation firewall
no new training-attention WGSL
runtime artifact atomic write and readback
```

Verification PASS token:

```text
PASS_ASH_BASETRAIN_G203D_LEGACY_TRAINING_ATTENTION_ORACLE_SHARED_TENSORCUBE_CANDIDATE_EXACT_QKV_SNAPSHOT_MASK_GQA_SCALE_TOLERANCE_REGISTRY_ACTIVATION_ABI_REPLAY_SOURCE_SURFACE_STATIC_VERIFICATION_NO_DEFAULT_ROUTE_PROMOTION_SEALED
```

---

# 14. Physical gate

Binary:

```text
ash_basetrain_g203d_physical_gate
```

Physical phases:

```text
A. Verify G202D parent artifacts and PASS lineage
B. Bootstrap one native WGPU device and queue
C. Build BaseTrain-owned immutable training snapshots
D. Execute paired W8 Headwise oracle and TensorCube candidate
E. Run first/middle/last and chunk-boundary matrix
F. Validate compact numerical and semantic parity
G. Verify deterministic replay
H. Reject candidate commit and mutation fixtures
I. Verify legacy and Decode writer preservation
J. Retire resources and publish final parity seal
```

Physical PASS token:

```text
PASS_ASH_BASETRAIN_G203D_LEGACY_TRAINING_ATTENTION_ORACLE_SHARED_TENSORCUBE_TRAINING_FORWARD_CANDIDATE_EXACT_QKV_SNAPSHOT_DUAL_CONSUMPTION_EXACT_MASK_SNAPSHOT_CAUSAL_PADDING_ALL_MASKED_ROW_GQA_MAPPING_ATTENTION_SCALE_FULL_SEQUENCE_PREFILL_FIRST_MIDDLE_LAST_LAYER_CHUNK_BOUNDARY_MIXED_PRECISION_TOLERANCE_PROFILE_CONTEXT_VALUE_PARITY_ACTIVATION_SHAPE_LAYOUT_DTYPE_PARITY_DETERMINISTIC_REPLAY_EXECUTION_ORDER_STABILITY_VRAM_PLATEAU_LEGACY_TRAINING_WRITER_PRESERVATION_DECODE_PRODUCTION_WRITER_PRESERVATION_NO_TRAINING_SPECIFIC_ATTENTION_FORK_NO_CANDIDATE_COMMIT_NO_DEFAULT_TRAINING_ROUTE_PROMOTION_NO_BACKWARD_NO_GRADIENT_WRITE_NO_OPTIMIZER_WRITE_NO_WEIGHT_MUTATION_NO_CHECKPOINT_WRITE_NO_TOLERANCE_AUTO_WIDEN_NO_SILENT_FALLBACK_SEALED
```

---

# 15. Runtime artifacts

```text
workspace/runtime/basetrain/g203d/
  ash_basetrain_g203d_verification_runtime_specification.json
  ash_basetrain_g203d_verification_runtime_artifact.json
  ash_basetrain_g203d_verification_local_manifest.json
  ash_basetrain_g203d_physical_runtime_specification.json
  ash_basetrain_g203d_physical_runtime_artifact.json
  ash_basetrain_g203d_physical_local_manifest.json
  input_snapshot_receipts.json
  forward_parity_receipts.json
  replay_receipts.json
  mutation_firewall_receipt.json
  final_training_forward_parity_seal.json
```

Runtime artifacts are generated by Rust and excluded from code ZIPs.

---

# 16. Completion state

G203D PASS establishes:

```text
LegacyOracleLive
TensorCubeCandidateNumericallyQualified
ExactQKVSnapshot
ExactMaskGQAScaleSemantics
ContextValueParity
ActivationAbiParity
FirstMiddleLastLayerParity
ChunkBoundaryParity
DeterministicReplay
CandidateShadowOnly
NoDefaultPromotion
NoBackward
NoGradient
NoOptimizer
NoWeightMutation
NoCheckpointCommit
NoToleranceAutoWiden
NoSilentFallback
```

Next patch:

```text
ASH-BASETRAIN-G204D-FROZEN-PARTITION-BACKWARD-01

Forward Partition Generation Pinning /
Forward Activation Lineage /
Softmax Backward Global-State Replay /
Chunked dV·dP·dScore·dQ·dK /
QKV Projection Gradient Binding /
CPU-f64 Small Oracle /
No Full Attention Matrix Materialization /
No Stale Forward Receipt Passage /
No Optimizer Authority Seal
```
