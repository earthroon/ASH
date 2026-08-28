# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LARGE-TRANSIENT-ALLOCATION-OWNER-AND-PREALLOCATION-ADMISSION-R1

## 0. Revision Identity

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LARGE-TRANSIENT-ALLOCATION-OWNER-AND-PREALLOCATION-ADMISSION-R1`

Short name: `ASH MCU R2-A`.

Parent: `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-CONTROL-PLANE-R1`.

Admission environment:

`ASH_UNIFIED_ATLAS_MCU_ALLOCATION_ADMISSION_R2A=1`

Runtime PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ALLOCATION_ADMISSION_R2A`

Static PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ALLOCATION_ADMISSION_R2A_STATIC`

## 1. Purpose

R2-A establishes exact semantic attribution and pre-allocation admission for large BaseTrain hotpath allocations before later lifetime/reclamation revisions are allowed to change memory ownership.

It answers, before a covered raw allocation is requested:

- semantic owner;
- semantic role;
- allocation domain;
- lifetime class;
- execution phase;
- parameter index and parameter ID;
- source and target generation / optimizer step;
- requested bytes for explicitly admitted allocations;
- stable source callsite identity.

R2-A is an attribution/admission revision. It is not the lifetime reclamation revision.

## 2. Historical Physical Boundary

The current Exact N8 physical failure boundary remains:

- generation `7`;
- optimizer step `7`;
- parameter index `99`;
- parameter ID `model.layers.10.mlp.down_proj.weight`;
- raw host allocation request `1,044,033,536` bytes;
- failure occurs before the first Muon source-wave binding witness.

The active parameter does not prove allocation ownership.

The byte count does not prove allocation ownership.

The nearest log line does not prove allocation ownership.

`historical_1044033536_owner_claimed=false` remains authoritative until the exact physical request is observed inside one exact R2-A semantic allocation scope and the concrete allocation callsite is routed through explicit R2-A admission.

## 3. Core Ordering

Required:

`Semantic Request -> Owner/Role/Lifetime/Phase -> R2-A Admission -> Raw Allocation`

Forbidden:

`Raw Allocation -> OOM -> Guess Owner From Surrounding Logs`

## 4. Shared Large-Allocation Threshold

Canonical mandatory-observation threshold:

`16,777,216` bytes (`16 MiB`).

This is the existing Unified Atlas physical page size. The threshold does not mean every request above 16 MiB is invalid. It means large requests may not be anonymous.

## 5. Allocation Owner Namespace

R2-A uses typed semantic owners. The initial production owner namespace contains only owners needed by the wired pre-wave path:

- `Gradient`;
- `TensorCubeMuon`;
- `BpDeltaK`;
- `FusionPlanner`;
- `Evidence`;
- `RuntimeControl`.

A storage representation such as `Vec`, `Tensor`, `Buffer`, `Slice`, `Box`, `Arc`, `HostBuffer`, `Temp`, or `Scratch` is not an owner.

## 6. Allocation Role Namespace

The initial R2-A role namespace covers the current Muon pre-wave horizon:

- parameter tile descriptors;
- packed gradient;
- parameter pre-snapshot;
- current-observation projection;
- local observer;
- bridge pair plan;
- bridge pair descriptor batch;
- bridge pair evidence;
- bridge temporal state;
- fusion candidate graph;
- fusion planner snapshot;
- fusion execution plan;
- parameter control binding;
- fusion calibration replay capture;
- Muon wave execution.

Owner and role remain separate authorities.

## 7. Allocation Domain

Canonical domains:

- `Host`;
- `Device`;
- `HostVisibleTransfer`.

The historical `1,044,033,536`-byte request remains physically unattributed until a fresh run proves its domain and exact callsite.

## 8. Lifetime Vocabulary

R2-A establishes the vocabulary consumed by R2-B:

- `ImmutablePersistent`;
- `MutablePersistent`;
- `WaveTransient`;
- `ParameterTransient`;
- `StepTransient`.

R2-A classifies. R2-B reclaims.

R2-A does not introduce tracing GC, arena resets, parameter-terminal free policy, step-terminal free policy, slot-pool migration, or allocator trimming.

## 9. Phase Vocabulary

Canonical phases:

- `ParameterPreparation`;
- `PreWave`;
- `WavePreparation`;
- `WaveExecution`;
- `Completion`;
- `Commit`;
- `Retirement`.

The historical failure attribution horizon is the parameter-level execution entry through the first Muon source-wave binding.

## 10. Pre-Wave Scope Coverage

The R2-A bake must bracket the currently executed pre-wave surfaces with explicit semantic scopes, including where present:

- parameter tile descriptor construction;
- gradient packing;
- parameter pre-snapshot sealing;
- BP-Delta-K local observation;
- current observation projection;
- same-parameter bridge pair planning;
- bridge descriptor construction and pair observation;
- bridge evidence assembly;
- bridge temporal update;
- fusion candidate graph construction;
- fusion planner state snapshot;
- fusion execution planning;
- parameter snapshot/control binding;
- optional calibration replay capture.

A scope begin without a matching scope end in a process that terminates on allocation failure is a diagnostic locator, not by itself physical closure. The concrete allocation callsite found by that scope must then use explicit R2-A admission.

## 11. Explicit Pre-Allocation Admission

Directly controlled large-capacity Vec creation uses `try_reserve_exact_vec_r2a` rather than unchecked `Vec::with_capacity` on R2-A-covered paths.

The helper:

1. computes requested backing bytes with checked arithmetic;
2. emits a typed request/admission witness for requests at or above 16 MiB;
3. applies any explicit caller-owned maximum bound when one exists;
4. calls `try_reserve_exact` only after admission;
5. returns structured `anyhow::Result` on reserve failure instead of relying on an unchecked growth path.

R2-A does not invent a new general transient-memory budget. A bound is supplied only where an existing authority owns it.

## 12. Required Runtime Witnesses

Semantic scope begin:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-SCOPE-BEGIN-R2A]`

Semantic scope end:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-SCOPE-END-R2A]`

Explicit large request:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-REQUEST-R2A]`

Explicit admission decision:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-ADMISSION-R2A]`

Step-level receipt:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-STEP-R2A]`

Final R2-A runtime instrumentation receipt:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ALLOCATION-ADMISSION-R2A]`

## 13. Historical Owner Claim Rule

The implementation must not contain logic equivalent to:

`if bytes == 1_044_033_536 { owner = ... }`

or:

`if parameter_index == 99 { owner = ... }`

The historical owner claim may flip only after fresh physical evidence binds:

- exact byte request;
- exact active parameter identity;
- exact source/target generation and optimizer step;
- exact semantic scope;
- exact concrete allocation callsite;
- exact owner;
- exact role;
- exact lifetime class;
- exact admission disposition.

## 14. Physical Closure Semantics

Static PASS proves the R2-A authority, typed vocabularies, pre-wave scope coverage, and explicit checked reservation path exist in source.

Static PASS does not prove the historical owner.

A physical run may produce one of two useful outcomes:

1. the historical allocation is encountered through an already explicit R2-A admission path, allowing direct owner/role/request-size attribution; or
2. the process fails while one semantic scope is open, locating the opaque helper that still contains the unadmitted concrete allocation. That result is diagnostic progress but R2-A physical closure remains pending until the concrete callsite is converted to explicit admission.

The raw historical owner must never be guessed to force a PASS.

## 15. Data-Plane Authority Preservation

R2-A does not move ownership of:

- current weight (`ResidentWeightPack`);
- successor weight (`ResidentWeightPackBuilder`);
- Adam M/V (`RamResidentAdamMv`);
- gradient accumulator;
- persistent TensorCube Muon state;
- vocab / embedding / LM-head weights.

Required:

`data_plane_authority_changed=false`

`numerical_behavior_changed=false`

## 16. Geometry / Scheduling Preservation

R2-A preserves:

- physical Atlas page = 16 MiB;
- slot count = 3;
- MCU mode = `MirrorObservedLegacy`;
- legacy execution ownership;
- canonical commit behavior.

R2-A does not enable:

- 32 MiB two-wave cluster;
- async overlap;
- AdamW MCU execution ownership;
- TensorCube Muon MCU execution ownership;
- global wait retirement;
- candidate D2H retirement.

## 17. RAM36 Preservation

The RAM36 process hard authority remains unchanged:

`38,654,705,664` bytes.

R2-A must not raise, replace, bypass, or silently reinterpret RAM36.

## 18. Required Static Acceptance

The static validator must establish at least:

- R2-A module exported from `base_train`;
- canonical environment, patch ID, runtime/static PASS tokens;
- 16 MiB threshold and historical byte constant;
- typed owner, role, domain, lifetime and phase namespaces;
- semantic scope witnesses;
- explicit request/admission witnesses;
- checked `try_reserve_exact` path;
- parameter index + parameter ID + source/target generation binding;
- target generation passed from scheduler instead of locally guessed;
- pre-wave scope coverage for BP-DK / bridge / fusion / planner surfaces;
- step receipt wiring;
- no 32 MiB geometry mutation;
- no direct historical-size owner assignment;
- no parameter-99 owner assignment;
- previous MCU R1 wiring remains present.

## 19. Required Physical Acceptance

Physical closure requires a fresh BaseTrain binary, fresh Native CF1, fresh cross-release compatibility authority, immutable Physical N2 parent, existing RAM36 parent authority, and Exact N8.

The run must reach the generation-7 / optimizer-step-7 / parameter-99 historical boundary.

R2-A physical PASS requires the exact `1,044,033,536`-byte request to be attributable before backing allocation to one exact semantic owner and role at one concrete admitted allocation callsite.

If the run still terminates with raw allocation failure and only a scope locator is available, the physical verdict is `HOLD_EXACT_CALLSITE_IDENTIFIED` rather than PASS.

## 20. Closure Does Not Mean Parameter 99 Crossed

R2-A closure and parameter-99 crossing are separate gates.

R2-A may correctly reject or expose the offending allocation without the training run crossing parameter 99.

Actual historical-boundary crossing belongs to the later parameter-99 physical gate after R2-B lifetime repair.

## 21. Existing Closure Preservation

R2-A must preserve current closures including:

- immutable Physical N2 authority;
- RAM36 authority;
- BP-Delta-K target optimizer generation binding;
- Muon full candidate retirement;
- Muon full source scratch retirement;
- Muon host scratch slab reuse;
- per-tile heap churn retirement;
- vocab full-GPU-residency rejection;
- gradient full-host-materialization rejection;
- Unified Atlas MCU R1 geometry / wave / slot / commit namespaces.

## 22. No False Claims

R2-A does not claim:

- the historical owner before fresh physical evidence;
- the 1GB allocation has been eliminated;
- parameter 99 has been crossed;
- Exact N8 has passed;
- RAM pressure has been fixed;
- GPU utilization has improved;
- async overlap is active.

## 23. Next Revision

After exact allocation owner/lifetime attribution, proceed to:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-TENSOR-LIFETIME-CLASSIFICATION-AND-GENERATIONAL-RECLAMATION-R1`

R2-B consumes R2-A attribution and must not independently guess ownership.

## 24. Authority Statement

Before R2-A, a large allocation can occur during parameter processing and the runtime can die before producing a semantic statement of what requested the memory.

After R2-A, the pre-wave path is divided into typed semantic allocation scopes and direct large capacity reservations can be admitted with exact byte counts before raw allocation. A fresh physical run can therefore distinguish the exact owner/role boundary instead of inferring it from parameter identity or nearby logs. Physical closure is withheld until the concrete historical allocation callsite itself is explicitly admitted.
