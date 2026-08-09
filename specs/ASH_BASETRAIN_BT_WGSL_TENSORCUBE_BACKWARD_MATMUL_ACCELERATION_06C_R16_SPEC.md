# ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-MATMUL-ACCELERATION-06C-R16

## 0. Revision identity

```text
Patch ID:
ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-MATMUL-ACCELERATION-06C-R16

Build revision:
bt-wgsl-tensorcube-backward-matmul-acceleration-06c-r16

Physical parent:
ASH-BASETRAIN-BT-WGSL-NEOX-ROPE-QKV-INPUT-RMSNORM-BACKWARD-06C-R15

Corrected source parent:
R15-R1 Forward Tape Allocator Owner Pinning

Proof ledger:
HOLD
```

## 1. Scope seal

```text
R15 Physical Parent /
R15 dInputHiddenTotal Canonical Authority Parent /
R15 Forward Tape Burn Allocator Owner Pin Parent /
Existing Backward Mathematics Frozen /
TensorCube Compute Candidate Introduction /
16x16x16 F32 TensorCube Tile Authority /
Workgroup-Local 16x16 Operand Staging /
F32 Input Weight and Accumulation Preservation /
No Precision Downgrade /
Seven Linear Backward Role Adoption /
OProj TensorCube Backward /
DownProj TensorCube Backward /
GateProj TensorCube Backward /
UpProj TensorCube Backward /
QProj TensorCube Backward /
KProj TensorCube Backward /
VProj TensorCube Backward /
DX TensorCube Compute /
DW TensorCube Compute /
Canonical OUT_IN Weight Layout Preservation /
Single Output Tile Owner /
Ordered Reduction-Chunk Accumulation /
Zero Float Atomic Gradient Reduction /
Zero Cross-Workgroup Gradient Accumulation /
2D TensorCube Coordinate Map /
Micro-Atlas Residency Preservation /
Zero Mega Tensor Atlas /
Zero Payload Replication /
Zero Host Shuttle /
Semantic Oracle Non-Publishing Replay /
TensorCube Candidate Publishing Replay /
Per-Role DX Bit-Exact Parity /
Per-Role DW Bit-Exact Parity /
End-to-End dInputHiddenTotal Bit-Exact Parity /
R14 RMSNorm Executor Preservation /
R15 NeoX Executor Preservation /
R12/R14 G204D Attention Backward Preservation /
R13 SwiGLU Backward Preservation /
R13 Add Executor Preservation /
Structural DeltaQ and Gate Carrier Preservation /
GPU Timestamp Measurement /
Oracle-vs-TensorCube Benefit Gate /
Jitter-Aware Promotion /
Correct-But-Slower Non-Promotion /
TensorCube Compute Authority Promotion /
Semantic Executor Historical Oracle Retention /
No Same-Operation Silent Fallback /
Gradient Tile Publication Preservation /
No Canonical Gradient Atlas /
No Parameter Mega Buffer /
Commit Before GC /
TensorCube Tile Generation Seal /
Fail-Closed Numerics /
Zero-Is-Observation Not Failure /
No NaN Clamp /
No Gradient Clamp /
No Gradient Fabrication /
Production Payload Readback Zero /
Compact Parity Timing Receipt Only /
Atlas Parallel Wave Streaming Receipt /
No Monolithic Final json Macro /
No Forward Recomputation /
No Checkpoint Reopen /
No Decoder Clone /
No Optimizer /
No Weight Mutation /
Final Loss Authority Still Deferred /
Double-Run TensorCube Reproducibility /
Proof Ledger HOLD Seal
```

## 2. One-line SSOT

R16 preserves every R13-R15 backward equation and authority boundary exactly, replaces only the seven canonical linear-backward matmul executions with deterministic F32 16x16x16 project-TensorCube tiled compute, stages both reduction operands through transient workgroup-local 16x16 pages while retaining the original ascending scalar reduction order, proves every candidate `dX` and `dW` against the existing semantic executor and proves the fully substituted backward chain against R15 canonical `dInputHiddenTotal`, then promotes TensorCube compute only when correctness, reproducibility, lifecycle safety, zero-readback constraints, and measured GPU benefit all close.

## 3. Parent authority

R16 requires the same-invocation R15 physical PASS and canonical selected-layer input gradient authority:

```text
r15_physical_parent = 1
r15_dinput_hidden_total_authority = 1
forward_tape_burn_owner_pins = 16
```

The sixteen R15-R1 Burn allocation owners remain pinned until both the semantic-oracle and TensorCube candidate replays finish. R16 may not reconstruct the forward tape, reopen the checkpoint, or clone a training decoder.

## 4. Current admitted geometry

```text
selectedLayerCount = 1
selectedLayer = final decoder layer
B = 1
Q = 32
M = B*Q = 32
hiddenWidth = 2048
intermediateWidth = 5632
qHeads = 32
kvHeads = 4
headDim = 64
qProjectionWidth = 2048
kProjectionWidth = 256
vProjectionWidth = 256
```

The planner derives dimensions at runtime, but the initial R16 physical PASS claims only the geometry actually exercised by the admitted R15 parent.

## 5. Frozen linear-backward semantics

For every role:

```text
X  : [M,K]
W  : [N,K]
dY : [M,N]

Y  = X * W^T
dX = dY * W
dW = dY^T * X
```

Canonical parameter layout remains:

```text
W[out, in]
```

R16 may change dispatch geometry, workgroup cooperation, transient tile staging, residency metadata, and scheduling. It may not change matrix orientation, weight layout, gradient equations, gradient scaling, reduction index order, zero policy, or R13-R15 authority lineage.

## 6. Seven admitted linear roles

TensorCube candidate compute covers exactly:

```text
DOWN_PROJ_ACTUAL
GATE_PROJ_ACTUAL
UP_PROJ_ACTUAL
OPROJ_ACTUAL
Q_PROJ_ACTUAL
K_PROJ_ACTUAL
V_PROJ_ACTUAL
```

No other operator is silently routed through TensorCube in R16.

## 7. Explicitly preserved non-TensorCube executors

The following remain the admitted semantic executors:

```text
R13 SwiGLU backward
R13 deterministic Add2
R14 post-attention RMSNorm backward
R15 input RMSNorm backward
R15 NeoX RoPE VJP
R12/R14 G204D attention backward
structural gate reduction and structural carriers
```

R16 is a linear-matmul acceleration patch, not a generalized backward rewrite.

## 8. Role geometry

### OProj

```text
M=32 K=2048 N=2048
W=[2048,2048]
```

### DownProj

```text
M=32 K=5632 N=2048
W=[2048,5632]
```

### GateProj / UpProj

```text
M=32 K=2048 N=5632
W=[5632,2048]
```

### QProj

```text
M=32 K=2048 N=2048
W=[2048,2048]
```

### KProj / VProj

```text
M=32 K=2048 N=256
W=[256,2048]
```

## 9. Project TensorCube tile authority

Initial canonical tile geometry:

```text
TC_M = 16
TC_N = 16
TC_K = 16
workgroup_size = [16,16,1]
```

This is an ASH project TensorCube execution geometry. R16 does not claim native NVIDIA Tensor Core instructions, WMMA, cooperative matrix lowering, or any vendor-specific hardware mapping without separate physical evidence.

## 10. Precision authority

```text
input precision        = f32
weight precision       = f32
gradient precision     = f32
accumulation precision = f32
```

Forbidden in R16:

```text
fp16 conversion
bf16 conversion
tf32 approximation
quantized backward
loss scaling
automatic mixed precision
```

## 11. Workgroup-local operand staging

Every TensorCube workgroup owns two transient 16x16 F32 operand pages:

```text
tile_a = 16*16*f32
tile_b = 16*16*f32
workgroup staging = 2048 bytes
```

The operand pages are workgroup-local only and die with dispatch completion. They are not persistent tensor copies and do not become a second parameter/gradient store.

Device preflight must admit:

```text
max_compute_invocations_per_workgroup >= 256
max_compute_workgroup_size_x >= 16
max_compute_workgroup_size_y >= 16
max_compute_workgroup_storage_size >= 2048
```

## 12. DX TensorCube mapping

For:

```text
dX[M,K] = dY[M,N] * W[N,K]
```

one workgroup owns one final 16x16 `dX` output tile:

```text
cubeX = k_tile
cubeY = m_tile
```

For each ascending reduction wave:

```text
reduction_start = 0,16,32,...
```

all 256 invocations cooperatively stage:

```text
dY[Mtile,Ntile]
W[Ntile,Ktile]
```

then each output invocation accumulates `inner=0..15` in ascending order before advancing to the next reduction wave.

This preserves the semantic executor's logical reduction sequence `0..N-1` while allowing each staged operand value to be reused across the 16x16 output tile.

## 13. DW TensorCube mapping

For:

```text
dW[N,K] = dY^T[N,M] * X[M,K]
```

one workgroup owns one final 16x16 `dW` output tile:

```text
cubeX = k_tile
cubeY = n_tile
```

For each ascending M reduction wave the workgroup stages:

```text
dY^T[Ntile,Mtile]
X[Mtile,Ktile]
```

and each output invocation accumulates the 16 token terms in ascending token order. With the current B1/Q32 geometry, `dW` has exactly two 16-wide reduction waves.

## 14. Single-owner and ordered-reduction rules

Each final `dX`/`dW` scalar has exactly one output workgroup owner.

Forbidden:

```text
multiple workgroups writing one output scalar
float atomicAdd gradient accumulation
unordered partial-gradient reduction
cross-workgroup reduction merge
reassociation of the semantic reduction index order
```

The candidate exact-parity target is bitwise equality, not epsilon proximity.

## 15. Tail geometry

Runtime dimensions that are not multiples of 16 use explicit valid masks. Out-of-range lanes stage zero but never read out-of-range storage and never write an output element. Valid output lanes still accumulate only existing semantic reduction indices and do so in the same ascending order.

## 16. Micro-Atlas / TensorCube lifecycle preservation

R16 retains the R13-R2 lifecycle contract:

```text
PLANNED
-> RESIDENT
-> DISPATCHED
-> GPU_COMPLETED
-> COMMITTED
-> GC_ELIGIBLE
-> RELEASED
```

plus explicit FAULTED termination.

Required:

```text
generation seal = true
commit before GC = true
premature release = 0
orphan resident page = 0
payload copy = 0
host shuttle = 0
mega tensor atlas = 0
```

The R16 2D TensorCube tile map references canonical input/output buffer ranges directly. Persistent payload replication is forbidden.

## 17. Semantic oracle

The admitted R13 linear-backward executor remains available in R16 as:

```text
SEMANTIC_ORACLE
publication authority = 0
optimizer = 0
weight mutation = 0
```

Its outputs are compared GPU-side and never become the R16 canonical publication when TensorCube promotion succeeds.

## 18. Candidate authority state

Before all gates close:

```text
TensorCubeComputeCandidate = 1
TensorCubeComputeAuthority = 0
```

Candidate publication cannot be promoted until local parity, E2E parity, finite/completion checks, lifecycle checks, double-run reproducibility, zero production readback, and performance promotion all close.

## 19. Seven-role local exact parity

For each of DOWN/GATE/UP/OPROJ/Q/K/V:

```text
semantic dX vs TensorCube dX
semantic dW tile(s) vs TensorCube dW tile(s)
```

are compared using the existing same-device exact parity pipeline.

Required:

```text
local_dx_mismatch = 0
local_dw_mismatch = 0
local_nonfinite = 0
production_payload_readback = 0
```

No tolerance envelope is introduced by R16.

## 20. Full TensorCube-substituted backward replay

R16 exercises TensorCube in the actual selected-layer topology:

```text
dFinalHidden
  -> TensorCube Down backward
  -> existing SwiGLU backward
  -> TensorCube Gate + Up backward
  -> existing deterministic merge
  -> existing Post-RMS backward
  -> TensorCube OProj backward
  -> existing actual G204D attention backward
  -> existing NeoX VJP
  -> TensorCube Q + K + V backward
  -> existing Q->K->V merge
  -> existing Input RMS backward
  -> existing residual merge
  -> candidate dInputHiddenTotal
```

No forward layer is rerun.

## 21. E2E canonical parity

Parent oracle:

```text
R15 canonical dInputHiddenTotal
```

Candidate:

```text
R16 fully TensorCube-substituted dInputHiddenTotal
```

Required on current geometry:

```text
e2e_dinput_compared = 65536
e2e_dinput_mismatch = 0
e2e_dinput_nonfinite = 0
```

The E2E parity gate remains mandatory even when all seven local linear-role comparisons pass.

## 22. Parameter-gradient tile authority

R16 preserves bounded parameter-gradient tiles for:

```text
DOWN -> GATE -> UP -> OPROJ -> Q -> K -> V
```

No whole-layer or whole-model gradient atlas is created. The canonical optimizer-facing gradient atlas remains future R19 scope.

## 23. Structural carrier isolation

R16 carries through unchanged:

```text
dDeltaQ_H1..H4Actual
dGate_H1..H4Actual
```

Required:

```text
structural_deltaq_consumed_by_r16 = 0
structural_gate_consumed_by_r16 = 0
structural_deltaq_mutation = 0
structural_gate_mutation = 0
```

R17 remains their backward consumer.

## 24. Forward tape owner pins

R15-R1 physical parent contract remains:

```text
burn_allocator_owner_pin_count = 16
release_before_r16_completion = 0
```

R16 may borrow the already pinned forward surfaces but may not create CPU mirrors, whole-tape shadows, or new persistent TensorCube copies.

## 25. Fail-closed numerics and zero policy

Any nonfinite candidate `dX`, `dW`, preserved intermediate chain output, or candidate `dInputHiddenTotal` blocks promotion.

Forbidden:

```text
NaN clamp
Inf clamp
gradient clamp
silent zeroing
sigma/log/lambda amplification
epsilon gradient fabrication
```

There is intentionally no `BTR16GradientZero`. A finite all-zero result after exact completion, coverage, lineage, parity, and reproducibility is a valid observation.

## 26. Production readback boundary

Forbidden CPU payload readback:

```text
semantic dX/dW
TensorCube dX/dW
candidate intermediate gradients
candidate dInputHiddenTotal
```

Allowed compact evidence:

```text
nonfinite count
completion count
parity mismatch count
Micro-Atlas lifecycle counters
digests
GPU timestamp samples
```

Required:

```text
production_gradient_payload_readback = 0
production_weight_payload_readback = 0
```

## 27. TensorCube reproducibility

The complete candidate backward chain executes twice without mutation.

Exact compare covers:

```text
all seven candidate dX surfaces
all seven candidate dW tile sets
candidate dInputHiddenTotal
```

Required:

```text
tensorcube_reproducibility_runs = 2
tensorcube_reproducibility_match = 1
```

## 28. GPU performance measurement authority

Correctness alone does not promote an acceleration backend.

R16 uses the already admitted WGPU timestamp-query path. The implementation timestamps the **real executor GPU command envelope** for each semantic/candidate linear-backward call. This includes GPU commands emitted by that executor such as status/dispatch command work, because those are part of the actual executable route. It does not use host wall-clock time as promotion authority and excludes unrelated forward, receipt serialization, disk I/O, RMSNorm, RoPE, attention, and other non-linear stages from the seven-role aggregate.

This executor-envelope measurement is intentionally stricter than a synthetic isolated-kernel benchmark.

Required feature authority:

```text
TIMESTAMP_QUERY
TIMESTAMP_QUERY_INSIDE_ENCODERS
```

## 29. Timing protocol

For each of seven roles and both implementations:

```text
warmup runs = 2
timed runs = 7
```

Sample order alternates candidate/oracle ordering to reduce systematic ordering bias.

Per-role receipt records:

```text
oracle samples ns
candidate samples ns
oracle median ns
candidate median ns
oracle MAD ns
candidate MAD ns
timestamp period
measurement margin ns
speedup ratio
performance verdict
```

## 30. Per-role jitter margin

```text
measurementMargin
= max(
    oracleMAD,
    candidateMAD,
    2 * timestampResolution
  )
```

A per-role receipt may report whether its candidate is individually promotable, but final authority is decided by the aggregate seven-role gate.

## 31. Aggregate performance gate

R16 computes:

```text
oracleLinearBackwardGpuNs
    = sum(per-role oracle median)

tensorCubeLinearBackwardGpuNs
    = sum(per-role candidate median)

measurementMarginNs
    = sum(per-role measurement margin)
```

Promotion requires:

```text
tensorCubeLinearBackwardGpuNs + measurementMarginNs
< oracleLinearBackwardGpuNs
```

There is no arbitrary fixed 10% or 20% threshold. The candidate must beat the observed timing noise envelope.

## 32. Performance verdicts

```text
FASTER_PROMOTABLE
CORRECT_BUT_NOT_MEASURABLY_FASTER
CORRECT_BUT_SLOWER
NUMERIC_MISMATCH
NONFINITE
UNSUPPORTED
```

Only `FASTER_PROMOTABLE` receives the R16 PASS seal and `TensorCubeBackwardComputeAuthority=1`.

A candidate that is exact but not faster is retained as correct evidence but remains unpromoted. The physical R16 admission command exits fail-closed with `BTR16PerformanceNotPromotable...`; this is a performance non-promotion, not a gradient-correctness failure.

## 33. Same-operation fallback prohibition

Candidate failure must not trigger:

```text
candidate fault
-> semantic executor rerun
-> canonical publication
-> R16 PASS
```

Allowed:

```text
candidate fault
-> candidate authority stays 0
-> R16 admission fails
```

The semantic executor remains separately callable as historical/audit authority.

## 34. Authority promotion

Only after all correctness, reproducibility, lifecycle, zero-readback, and performance gates close:

```text
tensorcube_backward_compute_authority = 1
semantic_oracle_publication = 0
tensorcube_candidate_publication = 1
same_operation_fallback = 0
```

## 35. No optimizer or final-loss escalation

R16 may publish actual parameter-gradient tiles under the inherited deterministic backward-fixture lineage, but it must not apply learning rate, weight decay, momentum, optimizer accumulation, parameter updates, or checkpoint writes.

Required:

```text
optimizer = 0
optimizer_step = 0
weight_mutation = 0
checkpoint_mutation = 0
final_loss_authority = 0
dfinal_deterministic_fixture_lineage = 1
proof_ledger = HOLD
```

TensorCube compute promotion changes execution authority only, not the upstream gradient-source authority.

## 36. Required receipts

```text
r16_parent_r15_receipt.json
r16_tensorcube_device_preflight_receipt.json
r16_tensorcube_tile_policy_receipt.json
r16_down_tensorcube_receipt.json
r16_gate_tensorcube_receipt.json
r16_up_tensorcube_receipt.json
r16_oproj_tensorcube_receipt.json
r16_q_tensorcube_receipt.json
r16_k_tensorcube_receipt.json
r16_v_tensorcube_receipt.json
r16_local_dx_parity_receipt.json
r16_local_dw_parity_receipt.json
r16_tensorcube_candidate_chain_receipt.json
r16_e2e_dinput_parity_receipt.json
r16_micro_atlas_lifecycle_receipt.json
r16_allocator_pin_preservation_receipt.json
r16_tensorcube_reproducibility_receipt.json
r16_down_tensorcube_timing_receipt.json
r16_gate_tensorcube_timing_receipt.json
r16_up_tensorcube_timing_receipt.json
r16_oproj_tensorcube_timing_receipt.json
r16_q_tensorcube_timing_receipt.json
r16_k_tensorcube_timing_receipt.json
r16_v_tensorcube_timing_receipt.json
r16_performance_promotion_receipt.json
r16_semantic_oracle_retirement_receipt.json
r16_tensorcube_compute_authority_receipt.json
bt_wgsl_tensorcube_backward_matmul_acceleration_06c_r16_final.json
```

## 37. Hard failures

```text
BTR16MissingR15PhysicalParent
BTR16R15DInputAuthorityMissing
BTR16ForwardTapeOwnerPinMissing
BTR16TensorCubeDeviceLimitUnsupported
BTR16TensorCubeTileGeometryInvalid
BTR16WeightLayoutMismatch
BTR16RoleGeometryMismatch
BTR16MultipleOutputTileOwners
BTR16FloatAtomicReductionDetected
BTR16UnorderedReductionDetected
BTR16TensorCubePayloadCopyDetected
BTR16HostShuttleDetected
BTR16MegaTensorAtlasDetected
BTR16DXWriteCompletionMismatch
BTR16DWWriteCompletionMismatch
BTR16CandidateNonFinite
BTR16LocalDXParityMismatch
BTR16LocalDWParityMismatch
BTR16E2EDInputParityMismatch
BTR16TensorCubeReproducibilityMismatch
BTR16PrematureTileRelease
BTR16OrphanTensorCubeTile
BTR16GenerationSealMismatch
BTR16ProductionPayloadReadbackDetected
BTR16SemanticOraclePublicationDetected
BTR16SameOperationFallbackDetected
BTR16PerformanceEvidenceMissing
BTR16PerformanceNotPromotable
BTR16StructuralCarrierMutationDetected
BTR16ForwardRecomputeDetected
BTR16CheckpointReopenDetected
BTR16TrainingDecoderCloneDetected
BTR16GradientAtlasDetected
BTR16OptimizerDetected
BTR16WeightMutationDetected
BTR16FinalLossAuthorityEscalationDetected
```

There is intentionally no `BTR16GradientZero` failure.

## 38. CLI gates

Exactly 54 R16 gates are required exactly once in both canonical 06C response files and in regenerated `resolved.args`:

```text
--require-bt-wgsl-r16-r15-physical-parent
--require-bt-wgsl-r16-r15-dinput-hidden-total-authority
--require-bt-wgsl-r16-forward-tape-owner-pins
--require-bt-wgsl-r16-tensorcube-device-preflight
--require-bt-wgsl-r16-tensorcube-16x16x16-f32
--require-bt-wgsl-r16-f32-accumulation
--require-bt-wgsl-r16-zero-precision-downgrade
--require-bt-wgsl-r16-downproj-tensorcube-backward
--require-bt-wgsl-r16-gateproj-tensorcube-backward
--require-bt-wgsl-r16-upproj-tensorcube-backward
--require-bt-wgsl-r16-oproj-tensorcube-backward
--require-bt-wgsl-r16-qproj-tensorcube-backward
--require-bt-wgsl-r16-kproj-tensorcube-backward
--require-bt-wgsl-r16-vproj-tensorcube-backward
--require-bt-wgsl-r16-dx-tensorcube-compute
--require-bt-wgsl-r16-dw-tensorcube-compute
--require-bt-wgsl-r16-canonical-out-in-layout
--require-bt-wgsl-r16-single-output-tile-owner
--require-bt-wgsl-r16-ordered-reduction-waves
--require-bt-wgsl-r16-zero-float-atomic-reduction
--require-bt-wgsl-r16-zero-cross-workgroup-gradient-merge
--require-bt-wgsl-r16-micro-atlas-residency-preserved
--require-bt-wgsl-r16-zero-payload-copy
--require-bt-wgsl-r16-zero-host-shuttle
--require-bt-wgsl-r16-zero-mega-tensor-atlas
--require-bt-wgsl-r16-seven-role-dx-exact-parity
--require-bt-wgsl-r16-seven-role-dw-exact-parity
--require-bt-wgsl-r16-e2e-dinput-exact-parity
--require-bt-wgsl-r16-tensorcube-double-run-reproducibility
--require-bt-wgsl-r16-rmsnorm-executor-preserved
--require-bt-wgsl-r16-neox-executor-preserved
--require-bt-wgsl-r16-g204d-attention-backward-preserved
--require-bt-wgsl-r16-swiglu-backward-preserved
--require-bt-wgsl-r16-add-executor-preserved
--require-bt-wgsl-r16-structural-carriers-preserved
--require-bt-wgsl-r16-gpu-timestamp-measurement
--require-bt-wgsl-r16-jitter-aware-benefit-gate
--require-bt-wgsl-r16-measured-performance-promotion
--require-bt-wgsl-r16-zero-same-operation-fallback
--require-bt-wgsl-r16-gradient-tile-publication-preserved
--require-bt-wgsl-r16-zero-gradient-atlas
--require-bt-wgsl-r16-commit-before-gc
--require-bt-wgsl-r16-generation-seal
--require-bt-wgsl-r16-fail-closed-numerics
--require-bt-wgsl-r16-zero-observation-not-failure
--require-bt-wgsl-r16-production-payload-readback-zero
--require-bt-wgsl-r16-atlas-wave-streaming-receipt
--require-bt-wgsl-r16-zero-monolithic-final-json
--require-bt-wgsl-r16-zero-forward-recompute
--require-bt-wgsl-r16-zero-checkpoint-reopen
--require-bt-wgsl-r16-zero-training-decoder-clone
--require-bt-wgsl-r16-zero-optimizer
--require-bt-wgsl-r16-zero-weight-mutation
--require-bt-wgsl-r16-final-loss-authority-deferred
```

The resolved-args repair utility must fail closed if any R16 key is missing or appears more than once.

## 39. Atlas final receipt

The final R16 receipt is built through a seven-wave parallel lane / streaming merge atlas rather than one monolithic `json!` macro.

Canonical merge order:

```text
wave ordinal
-> lane ordinal
-> lexicographic key
```

Required:

```text
receipt_atlas_waves = 7
parallel_receipt_lane_build = 1
streaming_receipt_merge = 1
deterministic_receipt_merge = 1
monolithic_final_json = 0
```

Duplicate lane/root/reserved keys are hard failures.

## 40. Expected physical summary

```text
[bt-wgsl-tensorcube-backward-matmul-acceleration-06c-r16]
r15_physical_parent=1
r15_dinput_hidden_total_authority=1
forward_tape_burn_owner_pins=16
tensorcube_role_count=7
tensorcube_tile_m=16
tensorcube_tile_n=16
tensorcube_tile_k=16
workgroup_operand_staging=1
workgroup_staging_bytes=2048
tensorcube_input_f32=1
tensorcube_weight_f32=1
tensorcube_accumulation_f32=1
precision_downgrade=0
downproj_tensorcube=1
gateproj_tensorcube=1
upproj_tensorcube=1
oproj_tensorcube=1
qproj_tensorcube=1
kproj_tensorcube=1
vproj_tensorcube=1
dx_tensorcube_compute=1
dw_tensorcube_compute=1
single_output_tile_owner=1
float_atomic_reduction=0
cross_workgroup_gradient_merge=0
ordered_reduction_waves=1
micro_atlas_residency=1
tensorcube_compute_candidate=1
payload_copy=0
host_shuttle=0
mega_tensor_atlas=0
local_dx_mismatch=0
local_dw_mismatch=0
local_gradient_nonfinite=0
candidate_dinput_hidden_total_published=1
e2e_dinput_compared=65536
e2e_dinput_mismatch=0
e2e_dinput_nonfinite=0
tensorcube_reproducibility_runs=2
tensorcube_reproducibility_match=1
gpu_timestamp_query=1
timed_oracle_runs=7
timed_candidate_runs=7
performance_verdict=FASTER_PROMOTABLE
tensorcube_backward_compute_authority=1
semantic_oracle_publication=0
same_operation_fallback=0
structural_deltaq_consumed=0
structural_gate_carrier_consumed=0
structural_carrier_mutation=0
rmsnorm_executor_preserved=1
neox_executor_preserved=1
g204d_executor_preserved=1
swiglu_executor_preserved=1
add_executor_preserved=1
page_commit_before_gc=1
premature_release=0
orphan_resident_page=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
forward_recompute=0
checkpoint_reopen=0
training_decoder_clone=0
gradient_atlas=0
optimizer=0
weight_mutation=0
final_loss_authority=0
dfinal_deterministic_fixture_lineage=1
receipt_atlas_waves=7
parallel_receipt_lane_build=1
streaming_receipt_merge=1
deterministic_receipt_merge=1
monolithic_final_json=0
proof_ledger=HOLD
```

## 41. Source surface

Relative to R15-R1, R16 changes exactly seven files:

```text
ADD crates/burn_webgpu_backend/src/base_train_r16_tensorcube_linear_backward.rs
ADD crates/burn_webgpu_backend/src/shaders/base_train_r16_tensorcube_linear_backward.wgsl
MOD crates/burn_webgpu_backend/src/lib.rs
MOD crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
MOD tools/repair_r13r2r2_resolved_args.ps1
```

The repair-script modification is CLI preflight safety only and does not alter numerical R16 semantics.

## 42. Static bake vs physical authority

The bake environment has no Rust toolchain, WGSL validator, or physical WGPU adapter. Bake authority is limited to source/diff/schema/cardinality/archive consistency checks.

The following remain operator-machine physical authority:

```text
Rust compile
WGSL compile
actual 16x16 workgroup dispatch
seven-role exact GPU parity
full candidate backward replay
R15 dInputHiddenTotal E2E parity
GPU timestamp samples
performance promotion verdict
final R16 PASS token
```

## 43. PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_TENSORCUBE_BACKWARD_MATMUL_ACCELERATION_06C_R16
```

The full runtime PASS token additionally seals R15 parent authority, sixteen tape-owner pins, frozen backward mathematics, seven TensorCube roles, 16x16x16 F32 tiled compute, workgroup operand reuse, single-owner outputs, ordered reductions, exact local/E2E parity, preserved non-linear executors, structural-carrier isolation, double-run reproducibility, GPU timestamp evidence, jitter-aware measurable acceleration, zero silent fallback, lifecycle closure, zero production readback, zero optimizer/weight mutation, final-loss authority deferred, and `proof_ledger=HOLD`.

## 44. R17 boundary

R17 remains:

```text
DeltaQ Projector Backward /
Gate Projector Backward /
Structural Projection Parameter Gradients /
Structural Carrier-to-Source Gradient Propagation
```

R16 carries the R14/R15 structural DeltaQ and gate-gradient carriers through unchanged. R17 may use R16 TensorCube acceleration only after its own structural projection equations are independently established and validated.

## Final SSOT

R16 is an execution-authority promotion, not a new backward model. Down/Gate/Up/OProj/Q/K/V retain the exact R13-R15 `dX`/`dW` equations and F32 `[out,in]` layout. Each candidate workgroup owns one 16x16 output tile, stages the corresponding two 16x16 reduction operands in transient workgroup memory, and traverses reduction chunks and scalar indices in the same ascending order as the semantic executor. The existing linear executor remains a non-publishing oracle. TensorCube outputs must be bit-exact locally and after a fully substituted selected-layer replay against R15 canonical `dInputHiddenTotal`. Even a correct candidate is not promoted unless the real executor GPU timestamp envelope demonstrates acceleration beyond the measured jitter margin. Only then does TensorCube become canonical linear-backward compute authority; gradient atlas, optimizer, weight mutation, structural projector backward, and final-loss authority remain outside R16.
