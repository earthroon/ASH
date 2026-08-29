# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-AND-PATH-INTEGRAL-POLICY-COMPILER-R8

## Immutable Router Policy / Fixed-Point Expert Cost / Deterministic Per-Job Assignment / Path-Integral Source Compilation / Homogeneous Active Materialization Boundary

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-AND-PATH-INTEGRAL-POLICY-COMPILER-R8`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-MIXED-PRECISION-EXECUTION-EXPERT-ABI-R7`

Runtime gates:

- `ASH_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_R8=1`
- `ASH_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_R8_MODE=SHADOW_ROUTER|ACTIVE_DETERMINISTIC_ROUTER`
- `ASH_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_R8_POLICY_SOURCE=<path>`
- `ASH_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_R8_QUALIFICATION_RECEIPT=<path>` for active production

### 1. Purpose

R8 turns the R7 expert catalog into one deterministic routing authority. Every canonical R6 TensorCube job receives a bounded quantized routing feature vector. One immutable compiled policy evaluates the qualified R7 expert set through fixed-point cost arithmetic and produces one expert assignment per job.

R8 does **not** mutate the policy while the epoch is executing, does not sample experts stochastically, and does not retry a failed low-precision job through another expert.

### 2. Source-derived physical correction

The current R6/Local-Muon execution substrate owns one resident Wave partition and one compact source/momentum Wave slab. Executing a heterogeneous `{E0,E1,E2}` assignment as separate expert buckets would currently require either:

1. host-side source/momentum repacking per expert bucket, which would regress the already-qualified host-scratch retirement contracts; or
2. a new GPU-resident gather/view and multi-expert resident-partition ABI, which is not present in the R7 parent.

Therefore R8 closes **per-job routing policy authority** now, but physical Active execution is limited to an assignment manifest whose jobs all select the same expert.

Required current declaration:

`heterogeneous_active_execution_materialized=false`.

A mixed expert assignment in `ACTIVE_DETERMINISTIC_ROUTER` fails with:

`E_MCU_R8_HETEROGENEOUS_EXECUTION_NOT_MATERIALIZED`.

This is not a silent downgrade to E0 and not a host repack fallback.

### 3. Core separation

- R6 = canonical TensorCube job identity and independent-work admission.
- R7 = execution expert definitions and qualification.
- R8 = deterministic expert assignment policy.
- later execution-materialization revision = GPU-resident heterogeneous expert bucketing.
- later escalation revision = failed low-precision attempt requeue.

Invariant:

`Job Identity != Expert Identity != Routing Policy != Execution Attempt`.

### 4. Parent admission

Any enabled R8 mode requires:

- R6 `QUEUE_WITHIN_WAVE` production qualification;
- R7 expert ABI enabled;
- mandatory E0 Safe F32 authority;
- exact subgroup32/R4/R5 parent chain already satisfied through R7.

Active R8 additionally requires a matching R8 qualification receipt.

Required failures:

- `E_MCU_R8_R6_PARENT_NOT_PRODUCTION_QUALIFIED`
- `E_MCU_R8_R7_PARENT_NOT_ADMITTED`
- `E_MCU_R8_PRODUCTION_ROUTER_QUALIFICATION_REQUIRED`

### 5. Qualified expert set

R8 derives its candidate mask from the **active R7 device-bound qualification state**.

Stable expert bits:

- bit 0 = E0 Safe F32
- bit 1 = E1 Mixed F16/F32
- bit 2 = E2 F16 SoftMatrix16

E0 must always be present. E1/E2 are routable only when active Device SHADER_F16 is present and the corresponding R7 expert receipt is valid.

Capability support alone never implies routability.

### 6. R7 expert-manifest binding

Every R8 policy qualification receipt binds the exact R7 expert manifest digest. If device capability changes and therefore the R7 manifest changes, the old R8 qualification receipt is stale.

Required failure:

`E_MCU_R8_QUALIFICATION_EXPERT_MANIFEST_MISMATCH`.

### 7. Router modes

`OFF`: no routing authority; R7 run-level selection remains authoritative.

`SHADOW_ROUTER`: calculate exact per-job decisions and manifests, but do not modify R6 descriptor expert IDs.

`ACTIVE_DETERMINISTIC_ROUTER`: calculate decisions, require a physically qualified policy, and materialize the selected expert only when the epoch assignment is homogeneous.

Default enabled mode is `SHADOW_ROUTER`.

### 8. Path-Integral policy source

R8 introduces a bounded source object:

`McuPathIntegralPolicySourceR8`.

It contains one policy generation ID, optional parent policy digest, deterministic base costs, queue/tail/safety cost coefficients, and an exact source digest.

The runtime never reads mutable Path-Integral/Hebbian state directly per job.

Flow:

`Path-Integral source snapshot -> R8 policy compiler -> immutable policy digest -> job routing`.

### 9. Genesis source

When no explicit policy source is supplied, R8 may construct one deterministic safe-first genesis source for **shadow/ABI qualification**.

The genesis source is explicitly identified as `R8-GENESIS-SAFE-FIRST` and has a canonical digest.

Production Active still requires an R8 qualification receipt bound to the resulting compiled policy digest.

### 10. Policy compiler

Compiler revision:

`ASH.MCU.PATH-INTEGRAL-POLICY-COMPILER.R8.V1`.

The compiled digest binds:

- compiler revision;
- feature ABI;
- fixed-point cost ABI;
- Path-Integral source digest;
- exact tie-break rule;
- stochastic-routing disabled;
- online mutation disabled.

Changing any input creates a new policy digest/generation authority.

### 11. No online policy mutation

Forbidden during an active policy generation:

- outcome-driven weight mutation;
- Hebbian update applied to current policy;
- previous job completion changing the next job decision;
- queue completion order changing expert costs.

Current outcomes may be recorded as **proposal input for a future policy generation** only.

### 12. Routing feature ABI

Feature revision:

`ASH.MCU.ROUTER.FEATURE-QUANTIZATION.R8.V1`.

Current source-materialized v1 features are deliberately bounded and available without new payload D2H:

- canonical job ordinal;
- parameter class bucket;
- valid logical element count;
- sealed Wave queue-pressure bucket;
- explicit availability mask.

R8 does not pretend gradient/momentum magnitude features exist when their compact producers have not yet been threaded into the queue authority.

### 13. Feature availability

Missing optional features are not represented as numeric zero. The feature vector carries an availability mask.

A future policy that requires a missing feature must fail with:

`E_MCU_R8_REQUIRED_ROUTING_FEATURE_MISSING`.

Current v1 policy compiles only against the source-materialized feature set.

### 14. No new D2H for routing

R8 v1 must not copy full gradient/weight/momentum tiles from GPU merely to decide precision.

Future richer feature revisions must add explicit compact GPU reductions or reuse already-authoritative summaries.

### 15. Queue-pressure snapshot

Queue pressure is derived from the sealed Wave epoch size against the 16,384-job per-page structural bound and quantized to a fixed 0..255 class.

It is not sampled live while jobs complete.

Thus GPU completion order cannot change routing decisions.

### 16. Parameter class

The initial parameter-class feature is a deterministic compact parameter-index class. It is an ABI placeholder for a richer registry-backed parameter-class authority in a later feature revision.

R8 does not claim this placeholder is a learned semantic model feature.

### 17. Cost ABI

Cost revision:

`ASH.MCU.ROUTER.COST-FIXEDPOINT.R8.V1`.

All runtime routing decisions use checked/saturating integer cost arithmetic. No unversioned host F32 sum decides the expert.

Cost components are represented explicitly as:

- numerical risk;
- latency cost;
- bandwidth cost;
- memory cost;
- history cost;
- safety cost;
- total cost.

Current v1 may leave some terms at zero when no authoritative producer exists.

### 18. Hard filtering before cost

R8 first derives the qualified candidate expert mask from R7. Only qualified experts can enter cost comparison.

Hard unavailability is not represented by an arbitrarily large penalty.

E0 absence is a hard routing failure.

### 19. Deterministic expert choice

For admissible experts:

`selected = minimum(total_cost_q, safety_rank, expert_id)`.

Safety rank:

- E0 = safest
- E1 = next
- E2 = most aggressive

Thus exact cost ties bias to safer precision deterministically.

No map/hash iteration order may decide ties.

### 20. No stochastic routing

R8 does not sample from `exp(-J/T)` and does not use random seeds in expert selection.

Path-Integral state informs the compiled deterministic action cost only.

Required final fields:

- `stochastic_routing_enabled=false`
- `online_policy_mutation_enabled=false`

### 21. Routing decision identity

Each routed job receives an `McuExpertRoutingDecisionR8` containing:

- canonical job ordinal;
- feature digest;
- policy generation/digest;
- candidate and admissible masks;
- selected expert and cost;
- runner-up expert and cost;
- typed reason code;
- decision digest.

No free-form hotpath diagnostic text is required.

### 22. Assignment manifest

One sealed R6 Wave epoch receives an `McuExpertAssignmentManifestR8` containing the deterministic decisions and compact counts for E0/E1/E2.

The manifest records:

- assignment count;
- E0/E1/E2 counts;
- whether the epoch assignment is homogeneous;
- homogeneous expert ID if any;
- manifest digest.

### 23. Shadow isolation

In `SHADOW_ROUTER`, the R8 assignment manifest is created but R6 descriptor `execution_backend_id` remains unchanged.

Shadow mode must never influence physical execution or candidate output.

### 24. Homogeneous Active execution

When `ACTIVE_DETERMINISTIC_ROUTER` produces one expert ID for the entire Wave:

1. R8 assigns that expert to the sealed R6 descriptor epoch.
2. R6 recomputes the descriptor manifest digest.
3. The Local Muon executor receives an explicit R8 expert override.
4. The already-materialized R7 expert pipeline executes the existing resident Wave payload.

This is a real physical execution path, not a shadow-only metadata claim.

### 25. Explicit expert executor override

The R7 executor now exposes a child R8 API allowing the caller to select an already-qualified E0/E1/E2 pipeline for one Wave execution without recompiling pipelines or rebuilding the executor.

It reuses the same:

- resident partition;
- source/momentum payload;
- R5 norm contract;
- canonical F32 candidate output ABI.

### 26. No per-Wave shader compilation

The R8 override selects among pipelines already built by the R7-capable executor. No shader compilation is performed per job or per Wave because of routing.

### 27. Heterogeneous assignment boundary

R8 **does calculate** heterogeneous per-job decisions in Shadow mode.

Current Active path **does not execute** mixed expert buckets because doing so would require a new resident source-view/bucket ABI.

Active mixed assignment hard-fails before execution.

No fallback to the R7 run-level expert is allowed.

### 28. Why host repack is forbidden

A trivial implementation could build E0/E1/E2 host vectors by copying each selected tile into new contiguous source/momentum buffers. R8 explicitly rejects that design because it would restore per-expert host payload materialization and defeat the host-scratch retirement work preceding R8.

The future heterogeneous materialization revision must remain GPU-resident or use exact resident subviews.

### 29. Canonical job identity preservation

R8 expert assignment changes only execution backend identity. It does not change:

- canonical job ordinal;
- TensorCube coordinate;
- Wave membership;
- Atlas partition digest;
- source generation;
- candidate generation;
- output destination identity.

### 30. R6 descriptor adoption

R6 exposes an R8 child API to:

- snapshot the immutable canonical descriptors for routing;
- apply one homogeneous expert ID to a sealed epoch;
- recompute the descriptor manifest digest.

Stale queue generation checks remain intact.

### 31. R7 child authority

R7 exposes child-safe queries for:

- qualified expert bitmask;
- expert manifest digest;
- expert qualification state;
- job accounting under an R8-selected expert.

R7's expert definitions themselves are unchanged.

### 32. R7 parent receipt

During an R8 run, the R7 receipt is emitted as `PARENT_PRESERVED_BY_R8`. It does not pretend that the old run-level selected expert remains the sole execution selector.

R7 expert arithmetic/qualification remains parent authority.

### 33. R6 parent receipt

During an R8 run, R6 is emitted as `PARENT_PRESERVED_BY_R8` with Path-Integral router presence visible.

R6 remains a scheduling parent and does not itself claim the child precision contract changed.

### 34. No automatic escalation

If the R8-selected E1/E2 expert fails:

- R8 records a failure;
- the job is not silently rerun through E0;
- the current policy does not mutate.

Required:

`automatic_precision_escalation_enabled=false`.

### 35. Policy qualification receipt

Active R8 requires `McuRouterPolicyQualificationReceiptR8` binding:

- R8 patch ID;
- exact compiled policy digest;
- feature ABI;
- exact R7 expert manifest;
- nonzero shadow fixture count;
- nonzero active homogeneous fixture count;
- zero routing replay divergence;
- zero unqualified selection;
- zero out-of-envelope selection;
- zero assignment duplicate/missing;
- `homogeneous_active_execution_materialized=true`.

The receipt also records whether heterogeneous active materialization exists. For R8 it must remain false.

### 36. Active qualification semantics

R8 production PASS proves:

- deterministic policy compiler closed;
- per-job routing replay closed;
- one or more Active homogeneous Waves executed through the R8-selected expert;
- no heterogeneous Wave was silently downgraded or host-repacked.

It does **not** prove heterogeneous multi-expert dispatch.

### 37. Router replay

Same:

- feature vector;
- policy digest;
- qualified expert mask;

must yield the same selected expert and decision digest.

No timing value participates in feature or policy digest.

### 38. Path-Integral source vs compiled policy

Required distinction:

`PathIntegralPolicySource != CompiledRouterPolicy`.

The source may represent current synapse/action-cost proposals. The compiled policy is the immutable execution authority.

### 39. No same-epoch feedback loop

Forbidden:

`E2 job finishes fast -> lower E2 cost -> route later same-Wave jobs to E2`.

The entire epoch is routed from the frozen policy and frozen feature snapshot before execution.

### 40. No online Hebbian mutation

R8 does not apply Hebbian/coactivation updates to the active policy. Observed execution outcomes may only become next-generation proposal evidence.

### 41. No neural router

R8 v1 does not add a learned neural precision classifier. The compiled policy is bounded fixed-point cost logic.

This keeps the first router auditable and replayable.

### 42. No full tensor router features

Full TensorCube values must not become router-state history or CPU policy input. Features remain compact.

### 43. R2-B lifetime preservation

Router decisions and manifests must not extend full ParameterTransient payload lifetime.

Required:

`parameter_lifetime_closure_preserved=true`.

### 44. R2-C compact-state preservation

Detailed assignment decisions are epoch-scoped routing evidence. They must not accumulate as an unbounded step history.

Required:

`step_compact_state_closure_preserved=true`.

### 45. R3 instrumentation preservation

Normal R8 does not print one line per cost term/job. One compact epoch-level routing witness is sufficient in normal execution.

### 46. R4/R5 preservation

R8 does not change SoftMatrix mapping or the deterministic F32 norm contract.

### 47. R6 preservation

R8 does not change mutable output ranges, Atlas geometry, queue capacity, or independent-work proof.

### 48. R7 preservation

R8 selects only existing R7 expert IDs. It does not modify E0/E1/E2 shader arithmetic or their qualification receipts.

### 49. Atlas limitation preserved

R8 does not solve R6's currently unavailable exact AW01 slot lease generation. The honest parent declaration remains:

`atlas_slot_lease_generation_available=false`.

### 50. Static validation

The R8 static validator must prove at least:

- R8 module/export exists;
- mode defaults to Shadow;
- Path-Integral source and compiled-policy digest exist;
- fixed feature ABI exists;
- integer/fixed-point cost exists;
- E0 safety tie-break is explicit;
- stochastic routing disabled;
- online mutation disabled;
- automatic escalation disabled;
- R7 expert manifest/qualification filters are used;
- R6 descriptor snapshot and homogeneous child adoption exist;
- executor has explicit R8 expert override;
- Shadow does not mutate descriptors;
- Active heterogeneous assignment fails with the exact materialization error;
- no host expert-bucket repack path is introduced;
- R6/R7 parent validators remain unchanged/passing.

### 51. Unit tests

Required source tests include:

- stable safety rank E0 < E1 < E2;
- genesis policy self-digest;
- same feature/policy -> same decision;
- unavailable expert filtered;
- exact cost tie chooses safer expert;
- Shadow manifest can be heterogeneous without execution mutation;
- Active heterogeneous manifest rejected;
- homogeneous Active expert override preserves job count/identity;
- stale R6 seal remains rejected;
- policy source digest drift rejected.

Physical toolchain execution is separate from bake-time static closure.

### 52. Physical qualification sequence

`R8 static -> R7/R6/R5/R4/R3/R2 static regressions -> cargo check -> Rust tests -> WGSL validation -> Shadow router replay fixtures -> homogeneous E0 Active fixture -> homogeneous E1 Active fixture if qualified -> homogeneous E2 Active fixture if qualified -> policy qualification receipt -> release build -> fresh Native CF1 -> fresh cross-release -> immutable Physical N2 -> Exact N8`.

Heterogeneous physical dispatch is **not** an R8 PASS requirement because it is intentionally not materialized in this revision.

### 53. Runtime witnesses

Per epoch compact witness:

`[ASH-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-R8]`

Minimum:

- queue generation/epoch;
- policy generation/digest;
- job count;
- E0/E1/E2 assignment counts;
- heterogeneous assignment boolean;
- assignment manifest digest;
- mode.

Final receipt:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-AND-PATH-INTEGRAL-POLICY-COMPILER-R8]`.

### 54. Final receipt minimum fields

- patch ID;
- mode;
- policy generation/digest;
- Path-Integral source digest;
- feature/cost ABI revisions;
- R7 expert manifest digest;
- qualified expert count;
- total routed jobs;
- E0/E1/E2 assignment counts;
- heterogeneous assignment epoch count;
- homogeneous Active execution epoch count;
- `heterogeneous_active_execution_materialized=false`;
- unknown/unqualified/out-of-envelope selection count = 0;
- replay divergence count = 0;
- assignment duplicate/missing count = 0;
- stochastic routing = false;
- online policy mutation = false;
- automatic escalation = false;
- canonical job identity preserved = true;
- verdict.

### 55. PASS token

Only physically qualified homogeneous Active routing may emit:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_AND_PATH_INTEGRAL_POLICY_COMPILER_R8`.

Shadow mode emits no production PASS token.

### 56. Explicit non-goals

R8 does not:

- execute heterogeneous expert buckets physically;
- host-repack source/momentum by expert;
- introduce persistent GPU work stealing;
- mutate Path-Integral/Hebbian policy online;
- sample experts stochastically;
- automatically requeue a failed expert to E0;
- change expert arithmetic;
- promote B05/B06 device commit;
- retire D2H or exact waits;
- enable ActiveAsync;
- change Atlas 16 MiB / 3-slot geometry;
- mutate Physical N2 or RAM36.

### 57. Next execution-materialization revision

The natural next revision after R8 is **not** precision escalation yet if heterogeneous assignments are observed in Shadow.

Recommended immediate child:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-AND-HETEROGENEOUS-DISPATCH-R8A`

R8A should provide:

- GPU-resident expert bucket index lists or resident subviews;
- no host source/momentum repack;
- stable per-expert bucket ordering;
- one canonical output destination map;
- R6 queue identity preservation;
- exact bucket coverage/duplicate gates.

Only after R8A physical closure should a precision-escalation/requeue revision be activated.

### 58. Later precision escalation

After heterogeneous dispatch is physically closed, a later revision may implement bounded attempt identities such as:

`E2 failure -> E1 -> E0`.

That remains outside R8.

### 59. Authority declaration

Before R8, R6 provides canonical jobs and R7 provides independently qualified execution experts, but there is no deterministic policy authority linking the two.

After R8, every R6 job can be evaluated against one immutable Path-Integral-derived fixed-point policy using one canonical feature ABI. The selected expert is reproducible from feature digest, policy digest, and qualified expert mask. Shadow mode can expose true heterogeneous per-job assignment distributions without changing execution. Active mode physically selects the routed expert only when the current Wave can be executed without introducing a new host repack or resident-partition topology.

Thus R8 closes **routing policy authority** without falsely claiming that the current R6 Wave-resident payload topology already supports heterogeneous multi-pipeline dispatch.

### 60. Center sentence

**R8 finally lets the MCU decide who should do the job, but it does not lie about the road from the dispatcher to the GPU. The policy can already say “this tile wants E0 and that tile wants E2”; Shadow records that exactly. Active execution is allowed only when the current resident Wave can honor the decision without resurrecting host repacking. The policy SSOT is closed now; heterogeneous GPU materialization gets its own receipt instead of being smuggled into the router.**
