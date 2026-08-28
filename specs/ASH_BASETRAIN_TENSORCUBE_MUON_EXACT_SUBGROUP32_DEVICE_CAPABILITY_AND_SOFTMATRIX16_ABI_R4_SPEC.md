# ASH-BASETRAIN-TENSORCUBE-MUON-EXACT-SUBGROUP32-DEVICE-CAPABILITY-AND-SOFTMATRIX16-ABI-R4

## Exact Runtime Subgroup Probe / SoftMatrix16 F32 ABI / One-Subgroup-One-Matrix Ownership / SerialLane0 Norm Preservation

### 0. Revision identity

Revision:

`ASH-BASETRAIN-TENSORCUBE-MUON-EXACT-SUBGROUP32-DEVICE-CAPABILITY-AND-SOFTMATRIX16-ABI-R4`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-HOTPATH-INSTRUMENTATION-COMPRESSION-AND-SEMANTIC-FAILURE-RING-R3`

Environment gate:

`ASH_TENSORCUBE_MUON_SOFTMATRIX16_R4=1`

### 1. Purpose

R4 establishes a device-bound matrix execution authority for the existing 16x16 TensorCube Local Muon path. The Muon algorithm remains unchanged. Only the physical execution substrate of its F32 matrix primitives is allowed to change.

R4 introduces:

- exact runtime subgroup-size admission;
- a versioned `SoftMatrix16` F32 ABI;
- an F32 legacy backend;
- an F32 ExactSubgroup32 backend;
- one-subgroup-one-SoftMatrix16 ownership;
- backend receipts and parity fixtures.

R4 does not change normalization reduction, precision, optimizer routing, Atlas geometry, D2H policy, wait topology, or active execution authority.

### 2. Parent authority preservation

R4 preserves:

- R2-A allocation admission;
- R2-B Parameter Lifetime Closure;
- R2-C StepTransient compact-state closure;
- R3 semantic-context/failure-ring instrumentation;
- physical Atlas page = 16 MiB;
- Atlas slots = 3;
- existing MirrorVerified B05/B06 authority;
- canonical parameter and wave ordering;
- Physical N2 immutability;
- RAM36 authority.

### 3. Existing optimizer identity

R4 remains:

- `tensorcube_local_muon=true`;
- `full_matrix_muon=false`;
- `cross_cube_orthogonalization=false`;
- `global_orthogonality_claim=false`.

R4 is not a full-matrix Muon redesign.

### 4. Core invariant

`Matrix backend != Muon algorithm`.

Muon continues to own momentum, Nesterov, normalization, Newton-Schulz coefficient/iteration semantics, candidate update, and finite/status semantics.

SoftMatrix16 owns logical 16x16 representation and the physical implementation of matrix primitives only.

### 5. Capability authority source

The current production runtime already executes a device shader probe using `@builtin(subgroup_size)` before Local Muon runtime creation.

R4 reuses that physical probe as its capability parent.

Capability source:

`EXISTING_DEVICE_RUNTIME_SUBGROUP_SIZE_SHADER_PROBE`

R4 does not infer subgroup width from vendor name, GPU model, CUDA warp convention, or documentation defaults.

### 6. Current min/max limitation

The current Local Muon production call chain receives the exact observed runtime subgroup size, not adapter subgroup min/max metadata.

Therefore the R4 capability receipt explicitly records:

- `subgroup_min_size=None`;
- `subgroup_max_size=None`;
- `subgroup_min_max_unavailable=true`.

R4 does not fabricate min/max values from the one observed subgroup width.

### 7. ExactSubgroup32 admission

For the current R4 implementation:

`exact_subgroup32 = subgroup_feature_observed && observed_subgroup_size == 32`.

The subgroup feature is considered physically observed because the existing runtime shader probe successfully compiled/executed and returned a nonzero subgroup size.

If R4 is explicitly enabled and the observed subgroup width is not exactly 32, fail with:

`E_TENSORCUBE_MUON_EXACT_SUBGROUP32_CAPABILITY_MISSING_R4`.

No silent backend fallback is allowed after explicit R4 admission.

### 8. Capability witness

Required runtime witness:

`[ASH-TENSORCUBE-MUON-MATRIX-DEVICE-CAPABILITY-R4]`

Minimum fields:

- capability observation source;
- subgroup feature observed;
- observed subgroup size;
- min/max availability state;
- exact subgroup32;
- SoftMatrix16 eligibility;
- precision = F32;
- capability digest.

### 9. Matrix backend authority

R4 defines:

- `F32_WORKGROUP_LEGACY`;
- `F32_SUBGROUP_SOFTMATRIX16`.

Reserved future backends such as F16/BF16/hardware matrix/Tensor Core are outside this revision.

### 10. Selection authority

When R4 is disabled, the existing legacy backend remains selected.

When R4 is enabled:

- profile `ns_working_dtype` must be exactly `F32`;
- exact runtime subgroup32 must be physically admitted;
- selected backend becomes `F32_SUBGROUP_SOFTMATRIX16`.

The selected backend is immutable for the Local Muon runtime instance.

### 11. Precision gate

R4 requires F32.

If R4 is enabled under a non-F32 working profile, fail with:

`E_TENSORCUBE_MUON_R4_PRECISION_CHANGE_FORBIDDEN`.

R4 does not activate BF16-emulated working arithmetic, shader-f16, packed-half payloads, or mixed precision.

### 12. SoftMatrix16 ABI

ABI revision:

`ASH.TENSORCUBE.MUON.SOFTMATRIX16.F32.SUBGROUP32.R4`

Logical geometry:

- rows = 16;
- columns = 16;
- elements = 256;
- logical linear index = `row * 16 + col`.

### 13. Canonical lane ownership

Mapping revision:

`LOGICAL_MOD32_SLOT_DIV32_R1`

For logical element `L`:

- `lane = L % 32`;
- `register_slot = L / 32`.

Reverse mapping:

`L = lane + 32 * register_slot`.

Thus:

`32 lanes * 8 logical values/lane = 256 logical values`.

### 14. Mapping closure

Static/unit validation must prove:

- all logical indices 0..255 covered;
- no duplicate canonical owner;
- lane < 32;
- register slot < 8;
- mapping roundtrip exact.

### 15. Physical execution topology

The R4 subgroup shader uses:

`@workgroup_size(32, 1, 1)`.

Therefore one workgroup contains one exact subgroup32 and one subgroup owns one complete SoftMatrix16.

R4 deliberately does not describe the previous 256-thread workgroup as one subgroup.

### 16. One-subgroup-one-matrix rule

One Local Muon 16x16 TensorCube matrix job is owned by exactly one subgroup.

No SoftMatrix16 operation depends on implicit register exchange across multiple subgroups.

### 17. Four-quadrant execution

A 32-lane subgroup computes the full 16x16 output as four sequential 8x8 quadrants.

For each quadrant:

- lane low-row owner = `lane >> 3`;
- lane high-row owner = low row + 4;
- column = `lane & 7`;
- each lane accumulates two output values.

Four quadrants * 64 values = all 256 output values.

### 18. Subgroup data movement

The R4 backend uses `subgroupShuffle` to broadcast row/column seed values during matrix multiply.

The shader is not permitted to be a legacy workgroup implementation renamed as a subgroup backend.

### 19. Matrix primitive sequence

The existing Newton-Schulz sequence remains:

1. momentum/Nesterov source X;
2. normalize X;
3. `A = X * X^T`;
4. `AA = A * A`;
5. `B = b*A + c*AA`;
6. `next_X = a*X + B*X`;
7. repeat for existing NS step count;
8. candidate update.

R4 only changes how the matrix products are executed.

### 20. Accumulation order

For every output element, the intended logical accumulation order remains:

`k = 0 .. 15` ascending.

R4 does not intentionally change the mathematical accumulation tree.

### 21. FMA/physical lowering qualification

The WGSL source preserves the same logical operation order, but compiler/backend lowering may still fuse or schedule F32 operations differently.

Therefore actual bit parity must be established physically.

R4 does not claim bit-exact GPU parity from source inspection alone.

### 22. SerialLane0 norm preservation

R4 intentionally keeps normalization serial.

In the subgroup shader, lane 0 iterates logical elements `0..255` in ascending order and computes the same F32 sum-of-squares sequence before `sqrt` and epsilon addition.

Required:

- `norm_reduction_path=SERIAL_LANE0`;
- `norm_reduction_changed=false`.

Attempting to combine the R4 subgroup matrix backend with the existing ExactSubgroup32 norm path fails with:

`E_TENSORCUBE_MUON_R4_NORM_REDUCTION_CHANGE_FORBIDDEN`.

### 23. Why norm is separate

R4 must isolate matrix-backend effects.

Parallel norm reduction changes F32 addition order and therefore belongs to R5.

### 24. Working-state placement

R4 keeps full logical matrices in bounded workgroup state while assigning each lane eight canonical logical values and using subgroup shuffle for matrix exchange.

This revision does not claim that all Newton-Schulz state is permanently register-resident.

A later optimization may reduce workgroup staging without changing the SoftMatrix ABI.

### 25. No host matrix materialization

SoftMatrix intermediate matrices must not be materialized on CPU for normal R4 execution.

The current MirrorVerified candidate/momentum/update readback remains unchanged because its retirement belongs to later revisions.

### 26. Status semantics

The R4 shader preserves existing nonfinite and completion status semantics.

If runtime subgroup width is not exactly 32 or working dtype is not F32, the shader writes a hard status failure rather than continuing under an unqualified layout.

### 27. Tail and descriptor semantics

R4 reuses the existing TensorCube descriptor and packed range authority.

Parameter/TensorCube/wave identities, gradient base offsets, row strides, packed ranges, and status offsets remain unchanged.

### 28. Pipeline authority

The subgroup SoftMatrix shader/pipeline is materialized once with the Local Muon batch executor, not once per tile or wave.

Pipeline identity:

`tensorcube-local-muon-16x16-batch.softmatrix16-subgroup32-f32.pipeline`.

### 29. Legacy coexistence

The legacy pipeline remains available while R4 is disabled and for bounded qualification/reference use.

Enabling R4 does not delete legacy source or change R2/R3 parent receipts.

### 30. Backend witness

Required runtime witness:

`[ASH-TENSORCUBE-MUON-SOFTMATRIX16-BACKEND-R4]`

Minimum fields:

- backend ID;
- ABI revision;
- precision;
- matrix rows/columns;
- subgroup size;
- logical values per lane;
- mapping revision;
- norm path;
- Tensor Core claim = false;
- qualification state.

### 31. Tensor Core claim

R4 subgroup shuffle execution is not Tensor Core execution.

Required:

`tensor_core_execution_claimed=false`.

No cooperative-matrix/MMA claim is permitted in R4.

### 32. Full-matrix Muon claim

Required:

- `full_matrix_muon=false`;
- `tensorcube_local_muon=true`.

SoftMatrix16 is a local 16x16 execution abstraction, not full-parameter orthogonalization.

### 33. Backend telemetry

`TensorCubeLocalMuonBatchCandidateOutput` records:

- selected R4 matrix backend;
- SoftMatrix ABI revision;
- mapping revision;
- subgroup size;
- values per lane;
- Tensor Core claim false.

This is execution evidence, not a new optimizer state authority.

### 34. No execution-authority promotion

R4 does not promote B05/B06.

Current candidate/readback/commit authority remains unchanged.

Required final declaration:

`execution_authority_changed=false`.

### 35. No Atlas change

Required:

- physical page = 16 MiB;
- slots = 3;
- `atlas_geometry_changed=false`.

SoftMatrix16 does not redefine Atlas page geometry or logical clustering.

### 36. No lifetime regression

R4 must preserve:

- `parameter_lifetime_closure_preserved=true`;
- `step_compact_state_closure_preserved=true`;
- `hotpath_instrumentation_r3_preserved=true`.

No per-matrix diagnostic history may accumulate as StepTransient state.

### 37. Historical allocation authority

R4 must continue to state:

`historical_1044033536_owner_claimed=false`.

GPU backend changes do not retroactively attribute the historical host allocation.

### 38. Static validation

Required static validator proves at least:

- R4 patch/ABI/mapping identities exist;
- backend enum exists;
- exact32 derives from physical observed subgroup width;
- no vendor-based subgroup guess;
- explicit lane/slot mapping exists;
- subgroup shader workgroup size = 32;
- subgroup shader uses `subgroupShuffle`;
- subgroup-width hard guard exists;
- shader F32 gate exists;
- SerialLane0 norm loop remains;
- four-quadrant full matrix coverage exists;
- no f16 type in R4 shader;
- no Tensor Core/cooperative-matrix claim;
- actual R4 pipeline is created and selectable;
- production runtime constructs the R4 authority;
- production executor uses the R4 constructor when selected;
- R4 final receipt is produced;
- parent R2/R3 defaults remain present.

### 39. Unit tests

R4 source includes mapping tests for:

- 256-element coverage;
- exact mapping roundtrip;
- ExactSubgroup32 admission rejection when observed size is not 32.

Physical shader tests remain required locally because Rust/WGPU tooling is not available in the bake environment.

### 40. Source-level matrix mapping fixture

The four-quadrant matrix mapping must be compared against a canonical 16x16 reference for:

- `A * B`;
- `A * B^T` where used;
- every logical output coordinate.

The bake-time structural simulator may prove mapping/order equivalence but cannot substitute for GPU bit-parity qualification.

### 41. Physical parity fixtures

Required local GPU qualification should cover:

- zero matrix;
- identity-like matrix;
- signed finite matrix;
- small magnitude matrix;
- large finite matrix;
- structured low-rank cases;
- representative live TensorCube samples.

### 42. First-divergence witness

On physical parity failure, report:

`[ASH-TENSORCUBE-MUON-SOFTMATRIX16-FIRST-DIVERGENCE-R4]`

with:

- fixture ID;
- primitive/NS stage;
- row/column/logical index;
- expected F32 bits;
- observed F32 bits;
- lane;
- register slot;
- backend identity.

No arbitrary epsilon widening.

### 43. Qualification distinction

R4 distinguishes:

- capability admitted;
- shader/pipeline materialized;
- mapping statically valid;
- source-level matrix mapping valid;
- GPU primitive parity;
- full Muon fixture parity;
- Exact N8.

Earlier stages do not imply later PASS.

### 44. Physical qualification sequence

`R4 static -> parent static regressions -> cargo check -> Rust unit tests -> WGSL compile/validation -> GPU mapping/primitive fixtures -> Muon fixture parity -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

No stale binary-derived authority may be reused after R4 source changes.

### 45. Bake-environment status semantics

The bake environment may only claim what it observes.

If cargo/rustc/WGSL validator/GPU are unavailable, final bake audit must state those stages are unobserved rather than PASS.

### 46. Runtime final receipt

Required when R4 is enabled and physically successful:

`[ASH-BASETRAIN-TENSORCUBE-MUON-EXACT-SUBGROUP32-DEVICE-CAPABILITY-AND-SOFTMATRIX16-ABI-R4]`

Minimum fields include:

- patch ID;
- capability source;
- observed subgroup size;
- exact subgroup32;
- selected backend;
- ABI revision;
- matrix geometry 16x16;
- precision F32;
- lane mapping revision;
- mapping missing/duplicate counts = 0;
- norm path SerialLane0;
- norm changed = false;
- full matrix Muon = false;
- TensorCube Local Muon = true;
- Tensor Core claim = false;
- mixed precision = false;
- parent closures preserved;
- historical owner claim = false;
- Physical N2/RAM36/Atlas/execution/precision authorities unchanged;
- verdict PASS.

Required pass token:

`PASS_ASH_BASETRAIN_TENSORCUBE_MUON_EXACT_SUBGROUP32_DEVICE_CAPABILITY_AND_SOFTMATRIX16_ABI_R4`.

### 47. Explicit non-goals

R4 does not:

- parallelize norm reduction;
- activate the existing ExactSubgroup32 norm production path;
- enable F16/BF16/mixed precision;
- claim Tensor Core/cooperative matrix execution;
- convert to full-matrix Muon;
- introduce MoE/expert routing;
- connect Path-Integral Synapse policy;
- create a global TensorCube job queue;
- merge waves or cross-layer jobs;
- promote ActiveDeviceCandidate/ActiveVerified commit;
- retire bulk D2H;
- retire per-wave exact waits;
- enable ActiveAsync.

### 48. Handoff

Successful R4 establishes a stable F32 matrix ABI and exact subgroup32 execution substrate.

Recommended next revision:

`ASH-BASETRAIN-TENSORCUBE-MUON-DETERMINISTIC-SUBGROUP-NORM-REDUCTION-AND-SERIALLANE0-PRODUCTION-RETIREMENT-R5`

R5 may then change only normalization reduction topology while holding R4 matrix backend, F32 precision, and Muon algorithm fixed.

### 49. Authority declaration

Before R4, the Local Muon production path had real GPU matrix arithmetic and an existing subgroup probe/norm candidate, but matrix representation remained tied directly to the legacy 256-thread workgroup implementation.

After R4, exact runtime subgroup32 evidence can admit one versioned F32 SoftMatrix16 backend. One 32-lane subgroup owns all 256 logical values through an exact lane/slot mapping and computes the matrix products through deterministic four-quadrant subgroup exchange. The old SerialLane0 norm remains unchanged so matrix-backend qualification is isolated from reduction-order changes.

### 50. Center sentence

**R4 does not assume that an RTX-class GPU means warp 32. The already-existing device shader probe must physically return 32 before SoftMatrix16 is admitted. Once admitted, one subgroup owns one complete 16x16 Local Muon matrix, while F32 precision and the old serial norm remain frozen so any difference is attributable to the matrix backend alone.**
