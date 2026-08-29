# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-MIXED-PRECISION-EXECUTION-EXPERT-ABI-R7

## Versioned Precision Experts / Mandatory F32 Safety Expert / F16 Capability Gating / Independent Qualification / No Routing Policy

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-MIXED-PRECISION-EXECUTION-EXPERT-ABI-R7`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GLOBAL-TENSORCUBE-JOB-QUEUE-AND-INDEPENDENT-WORK-ADMISSION-R6`

Runtime gates:

- `ASH_UNIFIED_ATLAS_MCU_MIXED_PRECISION_EXECUTION_EXPERT_R7=1`
- `ASH_UNIFIED_ATLAS_MCU_MIXED_PRECISION_EXECUTION_EXPERT_R7_MODE=E0_ONLY|FORCE_E1|FORCE_E2|SHADOW_E1|SHADOW_E2`
- `ASH_UNIFIED_ATLAS_MCU_MIXED_PRECISION_EXECUTION_EXPERT_R7_E1_QUALIFICATION_RECEIPT=<path>`
- `ASH_UNIFIED_ATLAS_MCU_MIXED_PRECISION_EXECUTION_EXPERT_R7_E2_QUALIFICATION_RECEIPT=<path>`

### 1. Purpose

R7 gives the R6 execution-backend field an exact expert ABI. A canonical R6 TensorCube job may be executed by one of several independently versioned precision experts without changing job identity, Wave membership, Atlas binding, or canonical F32 output layout.

R7 defines experts and their numerical contracts only. It does not contain an AUTO router, Path-Integral policy, learned selection, or automatic fallback.

### 2. Parent requirements

Any enabled R7 production mode requires:

- R5 deterministic norm production qualification;
- R6 `QUEUE_WITHIN_WAVE` production qualification;
- exact subgroup size 32;
- R4 `F32_SUBGROUP_SOFTMATRIX16` parent;
- one mandatory E0 Safe F32 expert.

If R6 is still shadow-only, R7 production fails with `E_MCU_R7_R6_PARENT_NOT_PRODUCTION_QUALIFIED`.

### 3. Core separation

`Job identity != execution expert != routing policy`.

R6 owns canonical job identity and bounded queue admission. R7 owns execution expert definitions. A later R8 revision may choose an expert for a job.

Changing an expert ID must not change canonical job ordinal, parameter generation, Wave identity, TensorCube coordinates, Atlas residency binding, or destination ranges.

### 4. Initial expert set

R7 defines:

- `E0_SAFE_F32`
- `E1_MIXED_F16_F32`
- `E2_F16_SOFTMATRIX16`

Stable backend IDs are 1, 2, and 3 respectively. R6 backend ID 1 remains the existing qualified R5 F32 path, preserving binary/semantic continuity for E0.

### 5. E0 Safe F32

Revision:

`ASH.MUON.EXPERT.E0.SAFE_F32.R7`

E0 preserves the qualified R4/R5 path exactly:

- SoftMatrix working state F32;
- matrix multiply F32;
- matrix accumulation F32;
- R5 deterministic subgroup32 norm F32;
- candidate weight F32;
- candidate momentum F32;
- orthogonal update F32;
- persistent weight and Muon momentum F32.

E0 is mandatory and is the production semantic reference for E1/E2 qualification.

### 6. F16 capability authority

Portable low precision in R7 is WGSL F16 only. R7 makes no portable BF16 claim.

F16 eligibility is derived from the active `wgpu::Device`:

`device.features().contains(wgpu::Features::SHADER_F16)`.

Adapter/vendor/model guesses are forbidden. If SHADER_F16 is supported by hardware but not enabled on the active device, R7 treats F16 as unavailable for that device authority.

### 7. E1 conservative mixed F16/F32

Revision:

`ASH.MUON.EXPERT.E1.MIXED_F16_F32.R7`

Numerical contract:

`ASH.MUON.EXPERT.E1.F16_STORAGE_SHUFFLE.F32_MUL_ACC.NORM_F32.R7`

E1 preserves F32 source/momentum combination, R5 norm, Newton-Schulz scalar coefficients, candidate update, and persistent state. It changes the matrix substrate as follows:

- matrix workgroup storage: F16;
- subgroup matrix exchange: F16;
- matrix operands: quantized F16;
- matrix multiplication operands promoted to F32 at multiply;
- matrix accumulation: F32;
- completed matrix primitive result quantized back to F16 before the next matrix stage;
- final orthogonal update/candidate: F32.

E1 therefore targets storage/exchange footprint first, without combining that change with F16 accumulation.

### 8. E2 aggressive F16 SoftMatrix

Revision:

`ASH.MUON.EXPERT.E2.F16_SOFTMATRIX16.R7`

Numerical contract:

`ASH.MUON.EXPERT.E2.F16_STORAGE_SHUFFLE_MUL_ACC.NORM_F32.R7`

E2 preserves R5 norm, scalar combination, final candidate, and persistent state in F32, but uses:

- F16 matrix storage;
- F16 subgroup exchange;
- F16 matrix multiplication;
- F16 matrix accumulation.

E2 is independently qualified. E1 PASS never implies E2 PASS.

### 9. Common persistent/output authority

All initial experts share one canonical persistent/output ABI:

- persistent weight: F32;
- persistent Muon momentum: F32;
- candidate weight output: F32;
- candidate momentum output: F32;
- orthogonal update output: F32;
- existing status buffer authority.

R7 does not create E0/E1/E2-specific persistent weight forks.

### 10. R5 norm preservation

All R7 experts use the R5 deterministic subgroup32 F32 norm tree. R7 does not introduce an F16 norm accumulator or a new norm mapping.

The R4 logical mapping remains `LOGICAL_MOD32_SLOT_DIV32_R1`, and the R5 five-stage tree remains the norm SSOT.

### 11. Named conversion boundaries

E1/E2 may quantize only at explicit matrix-stage boundaries. The shaders expose F32-to-F16 constructors at those boundaries and retain F32 output storage.

If an F32 matrix-stage value exceeds finite F16 range, the expert increments the existing contract-failure status word. It is not clamped to a safe finite value. Qualification treats such range loss as an expert failure.

### 12. No divergent early-exit repair

Per-lane F16 range failures do not cause a lane-local early return across later workgroup barriers. The status path records the failure while preserving structurally uniform synchronization. This avoids turning numerical failure handling into a divergent-barrier execution bug.

### 13. Expert pipeline identity

R7 materializes distinct pipelines:

- E0: existing R5 F32 SoftMatrix pipeline;
- E1: `tensorcube-local-muon-16x16-batch.r7-e1-mixed-f16-f32.pipeline`;
- E2: `tensorcube-local-muon-16x16-batch.r7-e2-f16.pipeline`.

Precision is not switched through one hidden mutable shader flag. Pipelines are built once per active executor/device authority, never once per job.

### 14. Expert qualification receipt

E1/E2 production qualification is independent and device-bound. A receipt binds:

- R7 patch ID;
- expert ID/revision;
- expert numerical contract digest;
- active device capability digest;
- deterministic fixture-plan digest;
- E0 reference identity/digest;
- maximum observed error;
- mathematically/contractually derived allowed error;
- nonfinite divergence count;
- overflow divergence count;
- first divergence count;
- subnormal behavior classification;
- nonzero fixture count;
- receipt digest.

Production low-precision execution is forbidden without a valid matching receipt.

### 15. Derived error, no magic epsilon

E1/E2 receipts may not qualify using an arbitrary empirical epsilon. The allowed error must be derived from the expert's exact F16 conversion/multiply/accumulation pipeline and the repeated Newton-Schulz stages.

E0 is the production semantic reference. F64 may be used only as a mathematical analysis oracle.

### 16. Subnormal authority

A low-precision expert receipt must classify F16 subnormal behavior. `UNQUALIFIED` cannot receive ProductionQualified status.

R7 source does not infer flush/preserve behavior from vendor identity.

### 17. Run-level modes

R7 has no AUTO mode.

- `E0_ONLY`: execute E0 only.
- `FORCE_E1`: execute E1 only, requiring E1 production qualification.
- `FORCE_E2`: execute E2 only, requiring E2 production qualification.
- `SHADOW_E1` / `SHADOW_E2`: preserve E0 as selected production expert while declaring a qualification target.

The current base-train integration does **not** automatically double-execute shadow targets. `automatic_shadow_execution_enabled=false`. Physical E1/E2 shadow/fixture qualification is performed by an explicit qualification harness/receipt path rather than hidden in normal training.

### 18. No automatic fallback

R7 distinguishes expert execution failure from canonical job failure, but it does not implement:

`E2 -> E1 -> E0`

fallback. An expert failure remains visible. GPU-side precision escalation belongs to a later revision.

### 19. R6 descriptor integration

R6 retains fixed canonical job identity while allowing the descriptor `execution_backend_id` to take the R7 expert backend ID.

R6 exposes a child-aware seal method for R7. Every descriptor in a sealed epoch must carry the same explicit run-level expert ID in R7. Descriptor-to-executor translation validates that the sealed backend ID has not drifted.

R7 does not yet assign heterogeneous experts per job automatically.

### 20. R6 parent receipt under R7

R6's standalone production receipt says `mixed_precision_enabled=false`. During an R7 child run, R6 is emitted as `PARENT_PRESERVED_BY_R7` with the selected child backend visible rather than falsely reasserting the standalone R6 precision invariant.

R6's own queue qualification is still required before the child receipt is emitted.

### 21. Device capability binding

The R7 authority is created before the lazy Muon executor exists, but F16 capability is bound only when the actual `BackendDevice` reaches the Local Muon executor construction point.

Capability drift across the same authority instance fails with `E_MCU_R7_DEVICE_CAPABILITY_DRIFT`.

FORCE_E1/E2 additionally verify that the qualification receipt's device capability digest matches the active device authority.

### 22. R7 job accounting

R7 tracks only compact scalar job counts for E0/E1/E2. It does not retain per-job precision histories in StepTransient state.

The executor returns the actual execution expert identity with every batch output, and the control runtime verifies it matches the run-level selected expert.

### 23. Fused-pair exclusion

R6/R5 already fail closed for the unqualified fused-pair path. R7 does not add a fused-pair low-precision expert and does not weaken that exclusion.

### 24. No Path-Integral router

R7 does not use softmax, Gibbs/path action cost, Hebbian weights, queue pressure, memory pressure, or tensor statistics to choose an expert.

Those signals become inputs to R8 after expert qualification exists.

### 25. No automatic precision escalation

`automatic_precision_escalation_enabled=false`.

A failed E1/E2 execution is not silently rerun through E0 by R7.

### 26. Numerical semantics

For E0 relative to qualified R5:

- `precision_contract_changed=false`;
- `numerical_behavior_changed=false`.

For E1/E2:

- `precision_contract_changed=true`;
- `numerical_behavior_changed=true`.

The final receipt reports these according to the selected run expert rather than one global claim for the entire expert manifest.

### 27. Expert manifest

R7 derives an immutable expert manifest digest from:

- expert ABI revision;
- subgroup size;
- active device F16 capability;
- E0/E1/E2 numerical contract digests;
- qualification state;
- E1/E2 qualification receipt digests where present.

Expert definitions do not mutate mid-run.

### 28. Expert states

Semantically, an expert may be unavailable, capability-eligible, fixture/shadow-qualified, or production-qualified. In the current runtime representation:

- E0 ProductionQualified follows qualified R5;
- E1/E2 ProductionQualified require both active SHADER_F16 and a matching R7 qualification receipt.

Capability support alone never implies qualification.

### 29. Common output/status behavior

Both low-precision shaders retain F32 candidate/momentum/update storage and the R5 status stride. F16 range loss is reported through the existing contract-failure status word so R7 does not create a second unbounded per-expert status ledger.

### 30. Static validation

The R7 validator must prove:

- R6 production parent is required;
- E0/E1/E2 ABI identities exist;
- E0 is mandatory F32;
- E1/E2 require SHADER_F16;
- portable BF16 claim is false;
- E1 uses F16 storage/shuffle with F32 matrix multiply/accumulation;
- E2 uses F16 storage/shuffle/multiply/accumulation;
- both low-precision shaders keep the R5 F32 norm and F32 outputs;
- neither low-precision shader uses generic `subgroupAdd` for norm;
- distinct E1/E2 pipelines are actually materialized;
- production callsite binds active-device SHADER_F16;
- R6 descriptor backend IDs are activated by R7;
- no AUTO router or automatic fallback is introduced;
- persistent state remains F32.

### 31. Unit/fixture requirements

Source tests cover stable expert IDs, F16 capability requirements, distinct numerical contract digests, E0 default selection, and R6 expert-backend consistency.

Physical qualification must additionally cover:

- E0 vs R5 bit parity;
- E1 F16 conversion/range fixtures;
- E1 multi-iteration NS error fixtures;
- E2 aggressive F16 multiply/accumulate fixtures;
- finite/nonfinite parity;
- F16 max-range behavior;
- subnormal behavior;
- deterministic live TensorCube samples.

### 32. Physical qualification sequence

`R7 static -> R6/R5/R4/R3/R2 regressions -> cargo check -> Rust tests -> WGSL validation -> active-device SHADER_F16 observation -> E0-vs-R5 parity -> E1 fixtures/shadow -> E1 receipt -> E2 fixtures/shadow -> E2 receipt -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

No stage may be claimed PASS if it was not observed.

### 33. Exact N8 modes

Exact N8 identifies run-level expert mode explicitly. No ambiguous AUTO mixed run exists in R7.

E0-only N8 can qualify the ABI base. FORCE_E1/FORCE_E2 N8 requires the corresponding low-precision qualification receipt and active SHADER_F16.

### 34. Final runtime receipt

Required:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-MIXED-PRECISION-EXECUTION-EXPERT-ABI-R7]`

Minimum fields include:

- patch/ABI revision;
- run mode and selected expert;
- optional shadow target;
- expert manifest digest;
- E0/E1/E2 capability/qualification state;
- active SHADER_F16 observation;
- portable BF16 claimed false;
- automatic expert routing false;
- automatic precision escalation false;
- Path-Integral router false;
- automatic shadow execution false;
- persistent/output dtypes F32;
- per-expert job counts;
- mixed-precision job count;
- selected-expert precision/numerical-change booleans;
- PASS or QUALIFICATION verdict.

Base PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_MIXED_PRECISION_EXECUTION_EXPERT_ABI_R7`

Expert-specific promotion tokens:

- `PASS_ASH_MCU_R7_E1_MIXED_F16_F32_EXPERT`
- `PASS_ASH_MCU_R7_E2_F16_SOFTMATRIX16_EXPERT`

The base R7 PASS does not imply that E1 or E2 has qualified.

### 35. Explicit non-goals

R7 does not:

- dynamically choose experts per job;
- enable a Path-Integral router;
- update Hebbian routing weights;
- automatically fall back to E0;
- create GPU precision-escalation queues;
- change R6 admission scope;
- remove Wave identity;
- promote B05/B06 device commit authority;
- retire bulk D2H or exact waits;
- enable ActiveAsync;
- convert persistent weights or Muon momentum to F16;
- claim portable BF16;
- claim Tensor Core/cooperative-matrix execution.

### 36. Handoff

After qualified R7, R6 has one canonical execution identity and R7 provides several independently qualified expert implementations. The next revision may compile a deterministic expert-selection policy without redefining either job or expert.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-AND-PATH-INTEGRAL-POLICY-COMPILER-R8`

### 37. Center sentence

**R7 is the expert licensing layer, not the router. E0 is the mandatory F32 safe authority. E1 is F16 storage/exchange with F32 matrix math, while E2 additionally moves matrix multiply/accumulate into F16. Both still return F32 canonical candidates and preserve the R5 F32 norm. No low-precision expert may execute merely because the GPU probably supports half precision: the active Device must expose SHADER_F16 and the exact expert must carry its own device-bound qualification receipt.**
