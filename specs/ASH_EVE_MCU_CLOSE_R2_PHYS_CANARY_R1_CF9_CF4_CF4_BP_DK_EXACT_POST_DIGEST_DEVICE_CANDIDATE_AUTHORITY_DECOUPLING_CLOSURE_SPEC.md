# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF4

## BP-DK EXACT POST-DIGEST
## DEVICE-CANDIDATE AUTHORITY DECOUPLING CLOSURE

```text
+ EXACT POST-DIGEST REQUIREMENT DECOUPLED FROM COUNTERFACTUAL MODE
+ B05 ACTIVE-DEVICE-CANDIDATE EXACT DIGEST REQUIREMENT
+ CF4 DEVICE-COMPACT POST-UPDATE EXACT SHA AUTHORITY
+ PERSISTENT EXACT-CAPABLE PRODUCER SELECTION
+ SINGLE REDUCTION / SHA PIPELINE CONSTRUCTION
+ RUNTIME-IDENTITY HOTPATH PRESERVATION WHEN EXACT DIGEST NOT REQUIRED
+ CF3 TARGET / UPDATE EXACT SHA REUSE
+ NO PER-PARAMETER SHA PIPELINE REBUILD
+ NO SECOND REDUCTION PRODUCER
+ NO HOST DIGEST FALLBACK
+ NO CANDIDATE D2H
+ NO COUNTERFACTUAL ENABLEMENT SIDE EFFECT
+ C08 MIRROR PRESERVATION
+ NO P5 CUTOVER CLAIM
```

---

## 0. Revision identity

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF4

Direct code parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF3-CF1
FUSED-PAIR CALL SIGNATURE / PAIR ORDINAL COMPILEFIX

Semantic parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF3

Class:
BP-DK PRODUCER CAPABILITY /
EXACT POST-DIGEST AUTHORITY CLOSURE
```

CF4-CF4 changes producer capability admission only.

It does not change optimizer math, source/candidate values, CF4-CF2 backing lifetime, CF4-CF3 source observation semantics, C08 mode, P5 mode, or counterfactual policy.

---

## 1. Parent physical boundary

CF4-CF3 physically established the FreshGenesis source path:

```text
selected source authority = B04_ATLAS_WAVE_FRESH_GENESIS
source generation          = 0
target generation          = 1
source D2H                 = 0
source H2D                 = 0
source GPU copy            = 0
source read lease          = ACQUIRED -> RELEASED_AFTER_EXACT_COMPLETION
CF4-CF2 assembly seal      = admitted=true
source-target parity       = admitted=true
```

The first failure moved to:

```text
E_CF9_CF4_CF3_EXACT_DIGEST_PRODUCER_REQUIRED
```

Therefore source authority and candidate lifetime are not the current blocker.

---

## 2. Root cause

Before CF4-CF4, exact post-digest capability was decided only by counterfactual mode:

```rust
require_exact_post_digests =
    counterfactual_mode != Disabled;
```

For the current CANARY:

```text
counterfactual = Disabled
```

so the persistent BP-DK runtime selected:

```text
BpDkDevicePostUpdateRuntimeR1::new_hotpath(...)
digest capability = RuntimeIdentity
```

However the admitted CF4 path independently requires exact SHA-256:

```text
B05 = ActiveDeviceCandidate
P5 active = false
post-update authority = DeviceCompactCandidate
CF3 target/update exact digest = required
```

`hash_target_only_cf3()` correctly fails closed when its producer is not ExactSha256-capable.

The defect is therefore producer capability selection, not hash execution.

---

## 3. Core law

```text
EXACT POST-DIGEST REQUIREMENT
!=
COUNTERFACTUAL ENABLEMENT
```

Exact digest is a capability required by consumers.

At minimum two independent consumers exist:

```text
counterfactual exact-digest consumer
OR
device-compact active-device post-update consumer
```

Required SSOT:

```rust
require_exact_post_digests =
    counterfactual_requires_exact_digest
    || device_compact_requires_exact_digest;
```

---

## 4. DeviceCompact exact-digest admission

The current CF4 DeviceCompact authority is selected by the same physical mode relation already used by parameter execution:

```text
active_async_parameter_r2 =
    P5 pending-wave queue active
    AND
    B06 HybridDeviceCommit = ActiveVerified

DeviceCompactCandidate =
    !active_async_parameter_r2
    AND
    B05 = ActiveDeviceCandidate
```

Therefore:

```text
DeviceCompactCandidate
=> device_compact_requires_exact_digest = true
```

No host Vec state participates in this decision.

---

## 5. Counterfactual requirement preservation

The previous stored field is split semantically.

Old meaning:

```text
perf_r1_require_exact_post_digests
```

New stored meaning:

```text
perf_r1_counterfactual_requires_exact_post_digests
```

It records only the counterfactual consumer.

The final exact capability is calculated when the real persistent device runtime is constructed.

This prevents counterfactual policy from being used as a proxy for unrelated DeviceCompact capability.

---

## 6. No counterfactual side effect

CF4-CF4 does not modify:

```text
AshBpDkLocalCounterfactualMode
planner feedback
proposal apply
counterfactual receipts
counterfactual effect ledger
```

A Disabled counterfactual remains Disabled.

Exact SHA support does not promote policy behavior.

---

## 7. Persistent producer construction

`BpDeltaKPersistentDeviceRuntimeR1` remains the single persistent owner of the post-update producer.

Construction law:

```text
require_exact_post_digests = true
    -> BpDkDevicePostUpdateRuntimeR1::new(device)
    -> ExactSha256 producer

require_exact_post_digests = false
    -> BpDkDevicePostUpdateRuntimeR1::new_hotpath(device)
    -> RuntimeIdentity producer
```

The existing hotpath remains legal when no exact consumer is admitted.

---

## 8. Capability freeze

The persistent runtime records:

```text
exact_post_digests
producer_instance_id
pipeline_build_count
```

After construction the exact capability is immutable.

Every later `ensure_bp_delta_k_perf_r1_device_runtime()` recomputes the current requirement and requires:

```text
runtime.exact_post_digests()
==
require_exact_post_digests
```

Mismatch fails closed with:

```text
E_CF9_CF4_CF4_DIGEST_CAPABILITY_DRIFT
```

This prevents mid-run RuntimeIdentity -> ExactSha256 reconstruction.

---

## 9. Producer instance authority

A process-local monotonic `producer_instance_id` is assigned at persistent runtime construction.

This identity is telemetry/attribution only.

It does not participate in model semantics or digest framing.

Its purpose is to prove:

```text
same producer instance
across parameter execution
```

and detect accidental per-parameter producer construction from physical logs.

---

## 10. Pipeline construction count

Existing producer construction semantics are preserved:

```text
RuntimeIdentity:
    reduction pipelines = 2
    SHA pipeline        = 0
    pipeline_build_count = 2

ExactSha256:
    reduction pipelines = 2
    SHA pipeline        = 1
    pipeline_build_count = 3
```

CF4-CF4 constructs the persistent producer once.

Forbidden:

```text
for each parameter:
    new ExactSha256 producer
```

---

## 11. No second reduction producer

CF4-CF3 FreshGenesis observer already holds an `Arc` handle to the persistent producer.

CF4-CF4 reuses that same producer for:

```text
source-dependent compact reduction
CF3 hash_target_only()
```

No new producer is created for target hashing.

No duplicate reduction pipeline family is introduced.

---

## 12. CF3 hash execution preservation

The backend guard remains intentionally fail-closed:

```text
E_CF9_CF4_CF3_EXACT_DIGEST_PRODUCER_REQUIRED
```

CF4-CF4 does not weaken or remove this guard.

Instead it ensures the admitted DeviceCompact runtime is constructed with ExactSha256 capability before the CF3 observer receives its producer handle.

---

## 13. CF4-CF2 preservation

Candidate backing authority remains:

```text
CF4-CF2 parameter-local assembly
```

Preserved invariants:

```text
candidate W/M/update copied before wave reclaim
assembly SubmissionEpoch exact completion
gap_count = 0
overlap_count = 0
resident_graph_lookup = false
assembly seal admitted=true
```

No candidate backing lookup is reintroduced.

---

## 14. CF4-CF3 preservation

FreshGenesis source authority remains:

```text
B04_ATLAS_WAVE_FRESH_GENESIS
```

Preserved invariants:

```text
source W/M observed while live
source D2H = 0
source H2D = 0
source GPU copy = 0
source lease release after exact completion
```

CF4-CF4 does not add a source full digest or source copy.

---

## 15. Exact target/update SHA authority

After CF4-CF2 assembly seal, the exact digest producer hashes:

```text
candidate Weight
candidate Momentum
orthogonal Update
```

using the existing canonical SHA-256 implementation.

Required outputs remain:

```text
candidate_weight_sha256
candidate_momentum_sha256
orthogonal_update_sha256
```

No digest-of-digests scheme is introduced.

No wave-local hash framing is substituted.

---

## 16. No host digest fallback

Forbidden:

```text
candidate GPU -> host full Vec -> CPU SHA-256
```

Required:

```text
full_candidate_d2h_bytes = 0
host_candidate_materialization_count = 0
```

Only the already-admitted compact digest/readback payload may cross D2H.

---

## 17. Runtime witnesses

### Producer capability

```text
[ASH-BP-DK-CF9-CF4-CF4][producer-capability]
```

Fields include:

```text
counterfactual_requires_exact_digest
device_compact_requires_exact_digest
require_exact_post_digests
selected_digest_capability
producer_instance_id
producer_reused=false
```

Expected current CANARY:

```text
counterfactual_requires_exact_digest=false
device_compact_requires_exact_digest=true
require_exact_post_digests=true
selected_digest_capability=EXACT_SHA256
```

### Pipeline construction

```text
[ASH-BP-DK-CF9-CF4-CF4][pipeline-construction]
```

Expected:

```text
reduction_pipeline_constructed=true
sha_pipeline_constructed=true
pipeline_build_count=3
```

### Producer reuse

```text
[ASH-BP-DK-CF9-CF4-CF4][producer-reuse]
```

Expected:

```text
digest_capability=EXACT_SHA256
pipeline_rebuild=false
```

### Exact digest submit / complete

```text
[ASH-BP-DK-CF9-CF4-CF4][exact-digest-submit]
[ASH-BP-DK-CF9-CF4-CF4][exact-digest-complete]
```

Completion must show all three target digests present.

---

## 18. No C08/P5 promotion

Preserve current profile:

```text
C08 = MirrorVerified
```

CF4-CF4 does not claim:

```text
C08 ActiveAsync
P5 production cutover
all exact waits retired
```

The exact digest capability is orthogonal to scheduling promotion.

---

## 19. Static acceptance

Required source properties:

```text
counterfactual-only requirement stored separately
DeviceCompact requirement derived independently
final requirement = OR of admitted consumers
persistent runtime selects ExactSha256 when required
persistent runtime freezes capability
capability drift fails closed
one persistent producer instance
CF3 reuses existing producer handle
no per-parameter producer constructor
no second reduction producer
RuntimeIdentity path remains available
counterfactual policy unchanged
CF2/CF3 lifetime/source paths unchanged
```

---

## 20. Compile acceptance

Authoritative compile is the existing native CF1 release compile authority.

Required:

```text
base_train release PASS
CF1 release binary SHA == target/release/base_train.exe SHA
```

No separate preliminary `cargo build base_train` is required.

This bake environment does not contain a Rust toolchain, therefore this artifact is sealed as:

```text
SOURCE/STATIC CONFIRMED
COMPILE NOT RUN
PHYSICAL HOLD
```

until user CF1 evidence is supplied.

---

## 21. Physical acceptance

The current CANARY must show:

```text
[CF4-CF4][producer-capability]
selected_digest_capability=EXACT_SHA256
require_exact_post_digests=true

[CF4-CF4][pipeline-construction]
sha_pipeline_constructed=true
pipeline_build_count=3

[CF4-CF3][source-authority]
selected_authority=B04_ATLAS_WAVE_FRESH_GENESIS

[CF4-CF2][assembly-seal]
admitted=true

[CF4-CF3][source-target-parity]
admitted=true

[CF4-CF4][producer-reuse]
pipeline_rebuild=false

[CF4-CF4][exact-digest-complete]
candidate_weight_digest_present=true
candidate_momentum_digest_present=true
update_digest_present=true

[CF4][device-post-collect]
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0

[CF4][post-receipt]
observation_authority=DEVICE_COMPACT
```

---

## 22. Blocker retirement

The following current blocker must disappear:

```text
E_CF9_CF4_CF3_EXACT_DIGEST_PRODUCER_REQUIRED
```

Previous blockers must remain retired:

```text
BpDkPostUpdateCandidateCardinality
E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING
E_CF9_CF4_SOURCE_GENERATION_MISSING
```

---

## 23. Next-failure policy

If exact target SHA completes and another fail-closed gate becomes the first failure:

```text
record the new first failure
```

Do not broaden CF4-CF4 into unrelated downstream repair.

No Full ABC campaign before the 2-step CANARY crosses this boundary.

---

## 24. Code delta

Parent SHA-256:

```text
8d4a22c80db56c643d7e5539a1924a13525cd319c00a4ef21a0f54c743eb2558
```

Modified files only:

```text
c5a04c9b00f70e1f2dd3140785f469113a64a1ba2c1bf4f68abd940976217645
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs

c880e29bb07b122b85f37b371fe37700cab8166aed167dc9c0abf9471acccf7d
crates/base_train/src/bp_delta_k_persistent_device_runtime_r1.rs
```

```text
ADD 0
MOD 2
DEL 0
```

No WGSL change.

No vendor change.

No artifact/spec content is included in the code-only ZIPs.

---

## 25. Artifact seals

Full code-only ZIP:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF4_BP_DK_EXACT_POST_DIGEST_DEVICE_CANDIDATE_AUTHORITY_DECOUPLING_CLOSURE_CODE_ONLY.zip
SHA-256 1401456f03946ec2de49df9cac0b2ac6641d9b9cc210c5c070d68000102e37cd
FILES 8424
CRC PASS
```

Overlay code-only ZIP:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF4_BP_DK_EXACT_POST_DIGEST_DEVICE_CANDIDATE_AUTHORITY_DECOUPLING_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256 2f3200bc527af822200bbd83b93e3d00a3796ee242cfcbcc4f6b863b83d8b1a1
FILES 2
CRC PASS
```

---

## 26. PASS token

Recommended:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF4
```

Meaning:

> Exact post-update digest capability is admitted independently from counterfactual policy. The current DeviceCompact active-device path owns one persistent ExactSha256-capable BP-DK producer, reuses its reduction/SHA pipelines across parameters, performs no full candidate host materialization, and preserves CF4-CF2/CF3 physical authority and C08/P5 non-promotion.

---

## 27. Final law

> Counterfactual mode is not the authority for exact digest capability.

> DeviceCompact active-device BP-DK is an independent exact-digest consumer.

> The persistent BP-DK runtime chooses its digest capability once, before parameter use, and that capability cannot drift during the session.

> ExactSha256 capability is supplied by the same persistent producer already used by CF3 source observation. No parameter-local producer, no second reduction producer, no host digest fallback, and no candidate D2H are permitted.

> RuntimeIdentity hotpath remains legal when no admitted consumer needs exact SHA-256.
