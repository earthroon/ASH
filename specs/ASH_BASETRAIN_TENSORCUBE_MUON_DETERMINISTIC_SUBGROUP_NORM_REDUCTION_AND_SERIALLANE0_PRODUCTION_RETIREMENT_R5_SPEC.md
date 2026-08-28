# ASH-BASETRAIN-TENSORCUBE-MUON-DETERMINISTIC-SUBGROUP-NORM-REDUCTION-AND-SERIALLANE0-PRODUCTION-RETIREMENT-R5

## ExactSubgroup32 Fixed Reduction Tree / F32 Norm Contract Revision / SerialLane0 Production Retirement / No Mixed Precision

### 0. Revision identity

Revision:

`ASH-BASETRAIN-TENSORCUBE-MUON-DETERMINISTIC-SUBGROUP-NORM-REDUCTION-AND-SERIALLANE0-PRODUCTION-RETIREMENT-R5`

Parent:

`ASH-BASETRAIN-TENSORCUBE-MUON-EXACT-SUBGROUP32-DEVICE-CAPABILITY-AND-SOFTMATRIX16-ABI-R4`

Runtime gate:

`ASH_TENSORCUBE_MUON_DETERMINISTIC_SUBGROUP_NORM_R5=1`

Production qualification receipt gate:

`ASH_TENSORCUBE_MUON_DETERMINISTIC_SUBGROUP_NORM_R5_QUALIFICATION_RECEIPT=<path>`

### 1. Purpose

R5 retires the 256-element SerialLane0 normalization loop from the production R4 SoftMatrix16 Local Muon path and replaces it with one versioned deterministic F32 ExactSubgroup32 reduction tree.

R5 changes reduction operation order. Therefore it is a new numerical contract even though every stored/working value remains F32.

### 2. Scope

R5 owns:

- per-lane norm ownership;
- local F32 partial accumulation order;
- fixed five-stage subgroup reduction tree;
- lane-0 sqrt/epsilon authority;
- norm broadcast;
- CPU F32 tree oracle contract;
- R4-vs-R5 compatibility authority;
- qualification receipt binding;
- SerialLane0 production retirement.

R5 does not own F16/BF16, mixed precision, Tensor Cores, global TensorCube scheduling, Path-Integral routing, B05/B06 promotion, bulk D2H retirement, exact-wait retirement, or async overlap.

### 3. Parent admission

R5 may activate only when:

- R4 is enabled;
- selected matrix backend is `F32_SUBGROUP_SOFTMATRIX16`;
- runtime subgroup probe reports exactly 32;
- working dtype is F32.

Otherwise fail with:

`E_TENSORCUBE_MUON_R5_R4_SOFTMATRIX32_PARENT_NOT_ADMITTED`

or

`E_TENSORCUBE_MUON_R5_PRECISION_CHANGE_FORBIDDEN`.

### 4. Parent SoftMatrix authority preservation

R5 preserves:

- `ASH.TENSORCUBE.MUON.SOFTMATRIX16.F32.SUBGROUP32.R4`;
- `LOGICAL_MOD32_SLOT_DIV32_R1`;
- 16x16 logical geometry;
- one subgroup per Local Muon matrix;
- R4 matrix multiplication mapping/order.

R5 does not alter the R4 matrix backend.

### 5. Core numerical distinction

R4 norm:

`logical 0 -> 255` sequential lane-0 sum.

R5 norm:

- 32 lane-local partials;
- 8 values per lane;
- five fixed cross-lane stages.

Required final declarations:

- `precision_contract_changed=false`;
- `reduction_order_changed=true`;
- `numerical_behavior_changed=true`.

R5 must not claim structural bit identity with R4 SerialLane0.

### 6. Norm equation

The mathematical equation remains:

`sum_sq = Σ x[i]^2`

`norm = sqrt(max(sum_sq, 0)) + eps`

`x_norm[i] = x[i] / norm`

R5 changes only how `sum_sq` is accumulated.

### 7. R5 numerical contract identity

Norm contract:

`ASH.TENSORCUBE.MUON.DETERMINISTIC.SUBGROUP32.NORM.F32.R5`

Compatibility contract:

`ASH.TENSORCUBE.MUON.R4-SERIAL-VS-R5-TREE32-NORM-COMPATIBILITY-R1`

The R5 contract digest binds the R4 SoftMatrix ABI, R4 lane mapping, subgroup size, values per lane, local addition count, tree stage count, root lane, and exact partner map.

### 8. Lane ownership

R5 reuses R4 ownership:

`logical = lane + 32 * slot`

where:

- `lane = 0..31`;
- `slot = 0..7`.

Each lane owns exactly eight logical F32 values.

### 9. Local accumulation order

Each lane processes slots exactly:

`0,1,2,3,4,5,6,7`.

For lane L the logical indices are:

`L, L+32, L+64, L+96, L+128, L+160, L+192, L+224`.

Local partial sum uses explicit left-to-right F32 additions.

### 10. Fixed tree

Stage 0:

`0+=1, 2+=3, ..., 30+=31`

Stage 1:

`0+=2, 4+=6, ..., 28+=30`

Stage 2:

`0+=4, 8+=12, 16+=20, 24+=28`

Stage 3:

`0+=8, 16+=24`

Stage 4:

`0+=16`

Final sum authority is lane 0.

### 11. Explicit subgroup exchange

R5 uses explicit `subgroupShuffle` source-lane exchanges for every tree stage.

A generic `subgroupAdd` collective is not the R5 numerical SSOT because implementation-selected reduction trees are not admitted.

### 12. No race-defined reduction

R5 forbids atomics, completion-order accumulation, or shared-memory races as the norm authority.

The addition graph is determined solely by the versioned lane/partner map.

### 13. One sqrt authority

Only lane 0 computes:

`1 / (sqrt(max(sum_sq, 0)) + eps)`.

The result is broadcast from lane 0 with subgroup exchange.

No lane independently recomputes sqrt or epsilon addition.

### 14. F32 only

R5 norm source, square, local partials, tree partials, sqrt input/output, epsilon addition, and normalized output are all F32.

R5 does not enable shader-f16 or BF16 emulation.

### 15. CPU F32 oracle

R5 source contains an explicit CPU F32 reference oracle that reproduces:

- 32 lanes;
- eight values per lane;
- slot-order local addition;
- five fixed tree stages.

The R5 execution oracle does not use generic iterator sum or F64 accumulation.

A separate F64 analysis oracle may be used later for error analysis but cannot replace the F32 tree oracle.

### 16. Error analysis

R5 records a structural rounding-chain depth of 13 operations for conservative compatibility analysis:

- square rounding;
- up to seven local additions;
- five tree additions.

The source exposes a `gamma(13)`-style F32 bound helper for analysis. This is not a corpus-tuned epsilon and is not by itself a physical promotion result.

### 17. Sum-of-squares domain

Squared contributions are nonnegative. Compatibility analysis should use the no-cancellation property rather than a generic signed-reduction heuristic.

Overflow, nonfinite values, or unqualified subnormal behavior are exceptional domains and must be classified separately.

### 18. Qualification receipt

Production PASS is not granted merely because R5 is enabled.

A production qualification receipt must bind:

- R5 patch ID;
- R5 norm contract digest;
- R4 SoftMatrix ABI;
- R4 mapping revision;
- observed subgroup size = 32;
- GPU-vs-R5-oracle parity PASS;
- R4-vs-R5 compatibility PASS;
- nonfinite semantics PASS;
- subnormal behavior classification;
- nonzero fixture count;
- first divergence count = 0;
- qualification receipt digest.

### 19. Qualification versus production

If R5 is enabled without a valid qualification receipt:

- the R5 backend may be exercised for qualification;
- final R5 verdict is `QUALIFICATION`;
- no R5 production pass token is emitted;
- production callsite finalization fails with `E_TENSORCUBE_MUON_R5_PRODUCTION_QUALIFICATION_REQUIRED`.

This prevents accidental N8 promotion of an unqualified numerical contract.

### 20. GPU shader

R5 adds a dedicated 32-thread SoftMatrix shader:

`base_train_tensorcube_local_muon_16x16_softmatrix16_subgroup32_f32_r5_norm.wgsl`

It preserves R4 matrix code and replaces only the SerialLane0 norm section with the R5 fixed tree.

### 21. Status semantics

R5 uses the ExactSubgroup32 status stride with an explicit subgroup/precision contract status word.

Subgroup width drift or non-F32 working mode fails before numerical execution proceeds.

### 22. No new host norm

R5 normal execution must not read matrix values back to CPU to compute norm.

The current MirrorVerified candidate/momentum/update readback remains unchanged because it is outside R5 scope.

### 23. No extra D2H

R5 must not introduce production D2H traffic solely for normalization.

Qualification fixtures may perform bounded explicit readback.

### 24. Backend selection

The existing Local Muon `ExactSubgroup32` path selector is reused as the execution selector, but its exact semantics depend on the matrix backend:

- legacy workgroup backend + ExactSubgroup32 = pre-existing legacy subgroup norm candidate;
- R4 SoftMatrix backend + ExactSubgroup32 = deterministic R5 tree shader.

The actual production authority is therefore the explicit R5 `TensorCubeMuonNormBackendR5::DeterministicSubgroup32R5` receipt, not the generic path string alone.

### 25. Fused-pair exclusion

R5 qualifies only the Local Muon SoftMatrix16 backend.

The existing fused-pair Muon ExactSubgroup32 shader still uses its older reduction contract. Therefore, when R5 is enabled, any fused-pair execution fails closed with:

`E_TENSORCUBE_MUON_R5_FUSED_PAIR_BACKEND_UNQUALIFIED`.

R5 does not silently mix two norm contracts in one optimizer step.

### 26. SerialLane0 retirement definition

Production retirement means successful qualified R5 execution has:

- `serial_norm_element_iteration_count=0`;
- `serial_lane0_normal_job_count=0`;
- one R5 norm job per Local Muon TensorCube;
- 32 lane partials per Local Muon TensorCube;
- five tree-stage reductions per Local Muon TensorCube.

The legacy SerialLane0 shader remains source-addressable for fixtures/reference only.

### 27. Cardinality gate

For a qualified R5 run:

`subgroup_partial_count == muon_tile_count * 32`

and

`tree_stage_reduction_count == muon_tile_count * 5`.

Mismatch is a hard R5 telemetry/contract failure.

### 28. Required backend witness

`[ASH-TENSORCUBE-MUON-NORM-BACKEND-R5]`

includes:

- backend ID;
- norm contract revision/digest;
- precision F32;
- subgroup size 32;
- values per lane 8;
- local add count 7;
- tree stage count 5;
- root lane 0;
- production qualification state.

### 29. Required retirement witness

`[ASH-TENSORCUBE-MUON-SERIALLANE0-RETIREMENT-R5]`

includes:

- production norm backend;
- SerialLane0 normal job count;
- subgroup norm normal job count;
- legacy reference fixture count;
- SerialLane0 production-retired boolean.

### 30. Parent R4 receipt under child authority

When R5 is active, R4 matrix authority remains the parent but R4's own `norm_reduction_changed=false` standalone PASS is no longer emitted as though nothing changed.

The R4 receipt is represented as `PARENT_PRESERVED_BY_R5`, with the same SoftMatrix ABI/mapping/capability authority and with the child norm revision explicitly visible.

This avoids falsely claiming the standalone R4 norm invariant during an R5 run.

### 31. R3 instrumentation preservation

R5 does not emit one normal console line per TensorCube or tree stage.

On failure, R3 semantic context/failure ring and R5 exact numerical divergence evidence may coexist.

### 32. Lifetime preservation

R5 subgroup partials are TensorCube-job transient values only.

No per-tile partial/history object may accumulate in ParameterTransient or StepTransient production state.

### 33. No Muon algorithm change

R5 preserves momentum, Nesterov, Newton-Schulz coefficients, NS step count, weight decay, learning rate, TensorCube geometry, parameter order, wave order, and commit order.

### 34. No Tensor Core claim

Required:

`tensor_core_execution_claimed=false`.

Subgroup shuffle execution is not Tensor Core/MMA execution.

### 35. No full-matrix claim

Required:

- `full_matrix_muon=false`;
- `tensorcube_local_muon=true`.

### 36. Static validation

The R5 static validator must prove:

- R5 backend/authority modules exist;
- R5 environment and qualification receipt gates exist;
- R4 parent is required;
- exact subgroup32 and F32 are required;
- SoftMatrix ABI and mapping revisions are unchanged;
- local slot order is explicit;
- five partner stages are explicit;
- R5 shader uses subgroupShuffle;
- R5 shader does not use subgroupAdd;
- lane 0 is unique norm root;
- norm broadcast comes from lane 0;
- R5 shader has no f16;
- R5 pipeline is materially constructed;
- R4 SoftMatrix + ExactSubgroup32 selects the R5 pipeline;
- unqualified production finalization is rejected;
- fused-pair execution is fail-closed under R5;
- R2/R3/R4 parent authorities remain present.

### 37. Unit tests

Required source tests include:

- exact tree partner map;
- exactly eight values owned per lane;
- X and -X squared norm equality;
- R4 exact subgroup parent requirement;
- non-F32 rejection;
- mapping preservation;
- fixed root lane and stage count.

Physical GPU tests remain separate.

### 38. Physical qualification sequence

`R5 static -> R4/R3/R2 parent static regressions -> cargo check -> Rust tests -> WGSL validation -> CPU F32 oracle fixtures -> R4-vs-R5 compatibility fixtures -> GPU-vs-R5 oracle fixtures -> full Muon fixtures -> qualification receipt generation -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

No stale binary-derived authority may be reused after R5 source changes.

### 39. First divergence

Physical qualification failure must identify the first known stage among:

- Square;
- LocalAdd1..7;
- TreeStage0..4;
- Sqrt;
- EpsilonAdd;
- Broadcast;
- Normalize.

A generic norm-parity failure without first-stage/lane/value evidence is insufficient for promotion.

### 40. Subnormal authority

The production qualification receipt must record observed subnormal behavior.

If it remains uncharacterized, the receipt cannot claim complete subnormal-sensitive numerical qualification.

### 41. Runtime final receipt

Required runtime receipt:

`[ASH-BASETRAIN-TENSORCUBE-MUON-DETERMINISTIC-SUBGROUP-NORM-REDUCTION-AND-SERIALLANE0-PRODUCTION-RETIREMENT-R5]`

It records at least:

- R5 patch ID;
- parent `F32_SUBGROUP_SOFTMATRIX16` backend;
- R4 SoftMatrix ABI/mapping;
- R5 norm backend/contract/digest;
- subgroup size 32;
- values per lane 8;
- local add count 7;
- tree stage count 5;
- root lane 0;
- F32 precision;
- qualification receipt identity;
- GPU oracle parity and R4/R5 compatibility status when qualified;
- SerialLane0 normal job count;
- subgroup normal job count;
- partial/tree cardinality;
- fused-pair R5 backend claimed = false;
- SerialLane0 production retirement state;
- `reduction_order_changed=true` when enabled;
- `numerical_behavior_changed=true` when enabled;
- `precision_contract_changed=false`;
- parent closure preservation fields;
- no historical 1 GiB owner claim;
- no Physical N2/RAM36/Atlas/execution authority change.

### 42. Production PASS token

Only a qualified R5 run may emit:

`PASS_ASH_BASETRAIN_TENSORCUBE_MUON_DETERMINISTIC_SUBGROUP_NORM_REDUCTION_AND_SERIALLANE0_PRODUCTION_RETIREMENT_R5`

An enabled but unqualified run emits no production PASS token.

### 43. Explicit non-goals

R5 does not:

- change R4 matrix multiply mapping;
- enable F16/BF16;
- use mixed precision;
- claim Tensor Cores;
- change NS coefficients/steps;
- convert to full-matrix Muon;
- qualify fused-pair R5 execution;
- introduce expert/MoE routing;
- connect Path-Integral Synapse;
- create global TensorCube scheduling;
- merge waves;
- batch across layers;
- promote B05/B06 authority;
- retire D2H or exact waits;
- activate async submission.

### 44. Handoff

After qualified R5:

- matrix primitive substrate = R4 SoftMatrix16 F32;
- norm substrate = R5 deterministic subgroup32 F32 tree;
- SerialLane0 production norm = retired.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GLOBAL-TENSORCUBE-JOB-QUEUE-AND-INDEPENDENT-WORK-ADMISSION-R6`

Mixed precision should follow scheduling closure so numerical and dispatch-topology changes remain separable.

### 45. Center sentence

**R5 does not replace SerialLane0 with an implementation-defined collective. It makes the reduction tree itself part of the optimizer execution contract: eight values per lane, seven local adds, five exact partner stages, one lane-0 sqrt, one broadcast. Because that is a different F32 operation graph, production promotion is impossible until a bound qualification receipt proves the new GPU path against the R5 oracle and the R4 compatibility contract.**
