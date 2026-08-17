# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-EXACT-SUBGROUP32-NORM-PARALLEL-REDUCTION-AND-SERIAL-ORACLE-R1

## Status

```text
Patch ID:
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-EXACT-SUBGROUP32-NORM-PARALLEL-REDUCTION-AND-SERIAL-ORACLE-R1

Code parent SSOT:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-WG32-EXACT-SUBGROUP32-SINGLE-TOKEN-SCALARIZED-STATE-AND-Q-REGISTER-RESIDENCY-R3A1 full body

Muon registry repair preserved:
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-REGISTRY-CANONICAL-LOAD-VERIFY-SSOT-AND-UNCONDITIONAL-RECURSION-REPAIR-R1

Production default norm path:
SERIAL_LANE0

Candidate norm path:
EXACT_SUBGROUP32

Automatic promotion:
forbidden
```

## Central SSOT

The existing serial Muon norm kernel remains the physical GPU oracle. R1 adds a separate exact-subgroup32 candidate shader and pipeline.

```text
Current serial GPU path
    lane0 loops over 256 projected x elements
    -> FP32 sum of squares
    -> norm_inv

ExactSubgroup32 candidate
    256 invocations each own one projected x value
    -> 8 subgroup FP32 partial sums
    -> 8-entry workgroup partial surface
    -> subgroup0 final FP32 reduction
    -> same norm_inv formula
```

The norm formula is unchanged:

```text
sum_sq  = Σ x_i²
norm_inv = 1 / (sqrt(max(sum_sq, 0)) + epsilon)
```

There is no RMS divide, epsilon relocation, Newton-Schulz coefficient change, momentum change, registry change, or optimizer routing change.

## Serial GPU oracle preservation

The original shader remains physically separate:

```text
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16.wgsl
```

Its parent SHA-256 remains:

```text
3f08fa919cfde360722ab37706d0bbbb292d5e849afe6dd7c1b3014da36533d8
```

It still contains:

```wgsl
if i == 0u {
    var sum_sq = 0.0;
    for (var logical: u32 = 0u; logical < 256u; logical = logical + 1u) {
        ...
        sum_sq = sum_sq + x[logical_x_index] * x[logical_x_index];
    }
    let eps = bitcast<f32>(params.ns_epsilon_bits);
    norm_inv = 1.0 / (sqrt(max(sum_sq, 0.0)) + eps);
}
```

The serial shader contains no subgroup reduction and remains the default production path until an explicit physical promotion revision.

## ExactSubgroup32 candidate shader

New shader:

```text
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_exact_subgroup32_norm.wgsl
```

Candidate SHA-256 at this bake:

```text
ce7cfd586adf561600ea5e4f20f51114e6f8a01ef239f9a38c6cc1db2c9167b4
```

The workgroup remains:

```wgsl
@workgroup_size(256, 1, 1)
```

No Muon tile geometry is changed.

## Existing subgroup probe reuse

R1 does not create a new Muon subgroup probe.

The existing BaseTrain scheduler probe remains the pre-dispatch capability source:

```text
probe_r6_r2_r2_subgroup_size(...)
    -> r6a_r2_r2_subgroup_probe.observed_subgroup_size
    -> ProductionMuonRuntime::load_or_initialize(...)
    -> TensorCubeLocalMuonBatchExecutor capability
```

The scheduler already requires the existing probe receipt to pass before the Muon production runtime is created.

This is an important evidence boundary: the existing probe is the host pre-admission authority. The candidate shader also observes its own `@builtin(subgroup_size)` and writes a compact contract-failure status if that dispatch does not actually observe subgroup size 32. A mismatch fails the candidate execution; it does not trigger a same-dispatch serial retry.

## Execution path authority

```rust
pub enum TensorCubeLocalMuonNormReductionPath {
    SerialLane0,
    ExactSubgroup32,
}
```

Capability identity:

```text
TENSORCUBE_LOCAL_MUON_NORM_REDUCTION_R1
```

The backend records:

```text
subgroup feature availability
observed subgroup size
exact_subgroup32 admission
```

The exact candidate pipeline is materialized only when the executor was created with an admitted existing subgroup probe.

## Production default and explicit selection

`ProductionMuonRuntime::load_or_initialize()` receives the existing observed subgroup size and stores it as physical execution capability.

The runtime still starts with:

```text
TensorCubeLocalMuonNormReductionPath::SerialLane0
```

An explicit API exists:

```rust
select_norm_reduction_path(...)
```

Changing the path after the batch executor has materialized is rejected. This seals one norm-reduction path for the runtime executor and prevents a hidden mid-batch swap.

The scheduler does not call the exact-subgroup32 selection method in this R1. Therefore this bake does not automatically promote the candidate into production.

## Candidate reduction stage 1

The projected Muon working value remains the norm input:

```wgsl
let projected_u = working_project(u);
x[x_index] = projected_u;
```

Each of the 256 invocations computes exactly one local square:

```wgsl
let local_sum_sq = projected_u * projected_u;
let subgroup_sum_sq = subgroupAdd(local_sum_sq);
```

For exact subgroup32 this produces eight subgroup partial sums.

Each subgroup elected invocation writes its partial:

```wgsl
if subgroupElect() {
    if subgroup_id < 8u {
        norm_subgroup_partial[subgroup_id] = subgroup_sum_sq;
    }
}
```

Partial surface:

```wgsl
var<workgroup> norm_subgroup_partial: array<f32, 8>;
```

Additional declared workgroup storage:

```text
8 × FP32 = 32 bytes
```

Candidate workgroup storage authority:

```text
serial existing declared total: 6212 bytes
candidate declared total:        6244 bytes
```

Device workgroup-storage limits are checked against the selected path.

## Candidate reduction stage 2

After subgroup partial publication and one workgroup synchronization, subgroup0 performs the final reduction.

All subgroup0 lanes participate in the collective:

```wgsl
var final_input = 0.0;
if subgroup_lane < 8u {
    final_input = norm_subgroup_partial[subgroup_lane];
}
let final_sum_sq = subgroupAdd(final_input);
```

Therefore:

```text
lanes 0..7  -> eight subgroup partials
lanes 8..31 -> zero contribution
```

The collective is not placed inside the `subgroup_lane < 8` branch.

The elected invocation of subgroup0 writes:

```wgsl
norm_inv = 1.0 / (sqrt(max(final_sum_sq, 0.0)) + eps);
```

All 256 invocations then consume the shared `norm_inv` and continue into the unchanged Newton-Schulz path.

## Barrier accounting

The candidate does not add another pre-Newton-Schulz workgroup barrier compared with the serial shader.

Serial phase:

```text
projected x publication barrier
norm_inv publication barrier
normalized x publication barrier
```

Candidate phase:

```text
8 subgroup-partial publication barrier
norm_inv publication barrier
normalized x publication barrier
```

Because each candidate invocation squares its own `projected_u`, it does not need the serial path's full-workgroup x-ready barrier before the first reduction. That synchronization point is replaced by the subgroup-partial synchronization point.

This is a structural barrier-count statement, not a claim about realized GPU stall cycles.

## FP32 and BF16-emulated authority

The existing working profiles remain:

```text
F32
BF16_EMULATED_F32_ARITHMETIC
```

For BF16-emulated working arithmetic, norm input remains:

```text
u
 -> working_project(u)
 -> projected x
 -> square / norm reduction
```

The candidate does not norm the unprojected `u` value.

Subgroup partials, final reduction, `sum_sq`, and `norm_inv` are FP32 shader values.

## Momentum authority preservation

The momentum recurrence is unchanged and occurs before norm reduction:

```text
m = beta * m_prev + (1 - beta) * g
```

Candidate momentum output remains:

```text
candidate_momentum[packed_index] = m
```

This makes momentum parity a strong negative control. A serial-vs-subgroup momentum mismatch cannot be attributed to the changed norm reduction order.

## Newton-Schulz preservation

The following remain unchanged in both serial and candidate shaders:

```text
x LD = 17
next_x = 256 FP32
A = 256 FP32
AA = 256 FP32
B = 256 FP32
momentum_local = 256 FP32
```

The existing formulas are preserved:

```text
A      = X X^T
AA     = A A
B      = b A + c AA
next X = a X + B X
```

No `a_mat` or `b_mat` padding change is mixed into this R1.

## Weight update preservation

The final update remains:

```text
candidate = w * (1 - lr * weight_decay) - lr * update
```

No Muon optimizer math, decay, Nesterov, or learning-rate behavior is changed.

## Candidate subgroup contract status

The existing serial shader still uses its two status words:

```text
word0 = nonfinite / structural error
word1 = completion
```

The exact-subgroup32 candidate uses a third word:

```text
word2 = candidate subgroup-size contract failure
```

Host status stride is selected by norm path:

```text
SerialLane0     -> 2 u32 per tile
ExactSubgroup32 -> 3 u32 per tile
```

The public `tile_status: Vec<[u32; 2]>` ABI remains unchanged. The third candidate word is aggregated into `subgroup_contract_failure_count` and is required to remain zero.

There is no same-dispatch serial replay when this word is nonzero.

## Resident descriptor cache identity

Status stride changes the descriptor's `status_base_elements`. Therefore resident structural-cache identity now also binds:

```text
norm reduction path
status stride
```

This prevents a cached serial 2-word descriptor layout from being reused by an exact-subgroup32 3-word execution, or vice versa.

This is an SSOT requirement, not a performance feature.

## Executor API

Legacy/default methods remain serial:

```text
execute(...)
execute_resident(...)
```

Explicit candidate-capable APIs are added:

```text
execute_with_norm_path(...)
execute_resident_with_norm_path(...)
```

The path is selected before the physical batch loop. The same selected pipeline is used for all chunks in that execution.

## Runtime telemetry

The batch output now records:

```text
norm_reduction_path
norm_subgroup_probe_observed_size
serial_norm_element_iteration_count
subgroup_partial_count
final_subgroup_reduction_count
subgroup_contract_failure_count
mid_batch_reduction_swap_count
```

Logical accounting:

```text
SerialLane0:
    serial norm element iterations = 256 × tile count
    subgroup partials              = 0
    final subgroup reductions      = 0

ExactSubgroup32:
    serial norm element iterations = 0
    subgroup partials              = 8 × tile count
    final subgroup reductions      = 1 × tile count
```

These are structural logical counts, not hardware instruction counters.

Production callsite counters aggregate the same norm-path evidence and require:

```text
subgroup contract failures = 0
mid-batch reduction swaps = 0
```

## CPU and GPU reference hierarchy

References remain explicitly separated:

```text
CPU F64 reference
    = semantic high-precision reference

SerialLane0 GPU FP32
    = current physical GPU oracle / production baseline

ExactSubgroup32 GPU FP32
    = optimization candidate
```

Bit exact equality between serial and subgroup reduction is not assumed because FP32 addition order changes.

Physical parity must inspect at least:

```text
norm / norm_inv
orthogonal update
candidate weight
candidate momentum
nonfinite status
```

Candidate momentum is expected to remain exact because its computation precedes the changed norm path.

## Static validation

New validator:

```text
tools/validate_ash_basetrain_tensorcube_local_muon_exact_subgroup32_norm_parallel_reduction_serial_oracle_r1_static.py
128/128 PASS
```

Coverage includes:

```text
patch identity in backend
serial shader exact parent SHA
separate candidate shader
existing subgroup probe reuse
no duplicate Muon probe
serial default preserved
explicit candidate selection only before executor materialization
candidate subgroup builtins
8 partial surface / 32-byte scratch
one square per invocation
two subgroupAdd calls total
subgroup-elected partial owners
subgroup0 final reduction
full subgroup0 collective participation
candidate subgroup mismatch status
2-word vs 3-word status stride
no same-dispatch fallback
resident descriptor cache path/stride sealing
norm formula preservation
BF16 projected-input ordering
momentum / NS / weight formula preservation
telemetry closure
CF1 wiring
```

## Retained parent static gates

```text
TensorCube Local Muon optimizer              101/101 PASS
FirstCandidate registry                       97/97 PASS
Muon multi-tile batch                         61/61 PASS
Muon production callsite                      63/63 PASS
Muon registry recursion repair                38/38 PASS
Muon X PAD17                                  52/52 PASS
Generation-sealed immutable Muon cache        66/66 PASS
Muon immutable-cache backend rebind           35/35 PASS
R6 production scheduler                      112/112 PASS
```

Two historical immutable-cache validators were updated only to recognize `execute_resident_with_norm_path()` as the same resident-consumption authority as the pre-existing `execute_resident()` method. Their cache semantics were not relaxed.

## CF1 wiring

The new validator is added to:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The existing CF1 Cargo/check/test sequence remains unchanged.

## Changed files

Overlay contains exactly eight files:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/shaders/base_train_tensorcube_local_muon_16x16_exact_subgroup32_norm.wgsl
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_basetrain_tensorcube_local_muon_exact_subgroup32_norm_parallel_reduction_serial_oracle_r1_static.py
tools/validate_basetrain_tensorcube_generation_sealed_immutable_tensor_cache_muon_resident_consumption_r1_static.py
tools/validate_basetrain_tensorcube_muon_immutable_cache_backend_surface_rebind_r1_static.py
```

The serial Muon WGSL file is deliberately absent from the overlay because its bytes are unchanged.

Code ZIPs contain no Markdown, `*.sha256`, or Python cache artifacts.

## Evidence boundary

The bake environment does not provide Cargo/rustc or a physical WGPU device execution result for this patch.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_PHYSICAL_GPU_PARITY_CLAIM
NO_PHYSICAL_SPEEDUP_CLAIM
NO_OCCUPANCY_CLAIM
NO_BANK_CONFLICT_CLAIM
PHYSICAL_CARGO_AND_GPU_GATE_REQUIRED
```

## Physical verification targets

The next local physical gate should establish:

```text
cargo check base_train PASS
serial pipeline WGSL compile PASS
exact-subgroup32 pipeline WGSL compile PASS
existing subgroup probe observes 32
candidate shader contract failure count = 0
SerialLane0 F32 run PASS
ExactSubgroup32 F32 run PASS
SerialLane0 BF16-emulated run PASS
ExactSubgroup32 BF16-emulated run PASS
candidate momentum parity PASS
orthogonal update parity within explicit existing tolerance/receipt policy
candidate weight parity within explicit existing tolerance/receipt policy
multi-tile resident path PASS
serial-vs-candidate GPU timestamp distributions recorded
```

A faster candidate is not automatically production-promoted by this R1. Promotion requires a later explicit policy revision.

## Non-goals

```text
No a_mat padding
No b_mat padding
No AA layout mutation
No Kahan summation
No FP64 GPU norm accumulation
No RMS normalization
No norm formula replacement
No NS step change
No NS coefficient change
No momentum formula change
No weight-decay change
No registry schema change
No optimizer routing change
No RAM36 authority change
No automatic candidate promotion
No runtime autotuner
```

## Natural follow-up

After physical parity and timing evidence, the next action is evidence-driven:

```text
if ExactSubgroup32 norm is correct and materially faster:
    explicit production promotion revision

if Muon NS matrix loop becomes the top hotspot:
    measure shared/LDS conflict counters before considering A/B padding
```

The current R1 does not assume that `a_mat` or `b_mat` padding will be beneficial.

## Promotion seal

```text
PROMOTE_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_EXACT_SUBGROUP32_NORM_PARALLEL_REDUCTION_AND_SERIAL_ORACLE_R1

SERIAL_LANE0_GPU_NORM_ORACLE_PRESERVED
SERIAL_SHADER_EXACT_PARENT_SHA_PRESERVED
CPU_F64_SEMANTIC_REFERENCE_PRESERVED
EXACT_SUBGROUP32_CANDIDATE_SHADER_ADDED
EXISTING_BASETRAIN_SUBGROUP_PROBE_REUSED
NO_DUPLICATE_MUON_SUBGROUP_PROBE
PRODUCTION_DEFAULT_SERIAL_LANE0
NO_AUTOMATIC_PRODUCTION_PROMOTION
EXPLICIT_PRE_EXECUTOR_PATH_SELECTION
NO_MID_BATCH_REDUCTION_SWAP
NO_SAME_DISPATCH_SERIAL_FALLBACK
WORKGROUP256_PRESERVED
ONE_PROJECTED_X_ELEMENT_PER_INVOCATION
FP32_LOCAL_SQUARE
FP32_SUBGROUP_PARTIAL_REDUCTION
EIGHT_SUBGROUP_PARTIALS
32_BYTE_NORM_PARTIAL_SCRATCH
SUBGROUP0_FINAL_FP32_REDUCTION
FULL_SUBGROUP0_COLLECTIVE_PARTICIPATION
ZERO_CONTRIBUTION_FROM_FINAL_LANES_8_TO_31
CANDIDATE_SUBGROUP_SIZE_RUNTIME_CONTRACT_STATUS
SERIAL_STATUS_STRIDE_TWO
CANDIDATE_STATUS_STRIDE_THREE
PUBLIC_TILE_STATUS_ABI_PRESERVED
RESIDENT_DESCRIPTOR_CACHE_NORM_PATH_SEALED
RESIDENT_DESCRIPTOR_CACHE_STATUS_STRIDE_SEALED
NORM_FORMULA_UNCHANGED
EPSILON_PLACEMENT_UNCHANGED
F32_PROFILE_PRESERVED
BF16_EMULATED_F32_ARITHMETIC_PRESERVED
PROJECTED_X_NORM_INPUT_PRESERVED
MOMENTUM_FORMULA_PRESERVED
MOMENTUM_NEGATIVE_CONTROL_PRESERVED
NEWTON_SCHULZ_FORMULAS_PRESERVED
X_PAD17_PRESERVED
A_MAT_LAYOUT_PRESERVED
B_MAT_LAYOUT_PRESERVED
WEIGHT_UPDATE_FORMULA_PRESERVED
IMMUTABLE_CACHE_RESIDENT_PATH_PRESERVED
RAM36_AUTHORITY_PRESERVED
REGISTRY_AUTHORITY_PRESERVED
CF1_STATIC_GATE_WIRED
NO_UNMEASURED_SPEEDUP_CLAIM
SEALED
```