# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R5

## Headwise Active Route Adoption / TensorCube Incremental Consumer Handoff / Same-Device KV Ownership / Stage-Scoped Feature Activation / Exact Prior-Stage Fallback / Cross-Layer Generation Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R4
PARENT_VERDICT=PASS
SOURCE_SCIENTIFIC_TERMINAL=PASS_OR_HOLD_AS_BOUND_BY_R2_R4
RUN_SCOPE=headwise-active-baseline-adoption-plus-tensorcube-stage0-handoff-v1
DEFAULT_VERDICT=HOLD
REFERENCE_ROUTE=existing-production-headwise-reference-v1
HEADWISE_ROUTE=gqa4-cluster-production-canary-v1
HEADWISE_TARGET_STATE=HeadwiseActive
TENSORCUBE_STAGE_ID=tensorcube-stage-0-consumer-ready-v1
TENSORCUBE_FEATURE_MASK=none
ROUTE_ADOPTION_POLICY=explicit-headwise-active-baseline-with-reference-rollback-v1
HANDOFF_POLICY=typed-same-device-zero-copy-incremental-consumer-contract-v1
KV_OWNERSHIP_POLICY=single-device-single-generation-single-writer-v1
STAGE_POLICY=one-new-tensorcube-feature-per-child-stage-v1
ACTIVATION_POLICY=stage-scoped-explicit-activation-v1
FALLBACK_POLICY=exact-prior-stage-chain-v1
GENERATION_POLICY=cross-layer-monotonic-generation-v2
PAYLOAD_POLICY=zero-host-materialization-zero-host-upload-zero-readback-v1
ADMISSION_POLICY=headwise-functional-adoption-without-performance-verdict-rewrite-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R2-R5 adopts the validated headwise path as the active attention baseline for this lineage. It does not rewrite the R1-R2 scientific PASS or HOLD result. It then installs a TensorCube stage registry and a typed consumer handoff with every TensorCube feature disabled at Stage 0.

R2-R5 is the boundary between headwise-only execution and incremental TensorCube activation. The first TensorCube feature is enabled by a child stage, not by R2-R5.

---

## 1. Purpose

R2-R5 must prove all of the following:

```text
1. The R2-R4 evidence and replay graph remains exact and immutable.
2. The headwise route is functionally adopted as the active baseline.
3. Functional adoption does not rewrite the scientific performance terminal.
4. The previous reference route remains an exact rollback target.
5. Headwise dispatches execute through the adopted active route.
6. Headwise output and KV post-state satisfy the existing reference parity policy.
7. TensorCube receives a typed Stage 0 consumer descriptor from HeadwiseActive.
8. TensorCube Stage 0 enables no TensorCube computational feature.
9. Q/K/V, KV-cache, output, producer, and consumer remain on one physical device.
10. KV ownership remains single-writer and generation-bound.
11. Host materialization, host upload, payload readback, and cross-device copy remain zero.
12. Every future TensorCube stage has exactly one declared parent stage.
13. Every future TensorCube stage falls back to the immediately prior sealed stage.
14. Headwise failure falls back exactly to the preserved reference route.
15. Device loss, generation drift, route drift, or ownership ambiguity fails closed.
```

---

## 2. Scope boundary

R2-R5 includes:

```text
ReferenceActive -> HeadwisePrepared -> HeadwiseActive
HeadwiseActive -> TensorCubeStage0ConsumerReady
TensorCube feature registry creation
TensorCube feature mask=none
exact HeadwiseActive -> ReferenceActive rollback proof
future prior-stage fallback chain definition
```

R2-R5 excludes:

```text
TensorCube feature 1 activation
TensorCube kernel dispatch
TensorCube performance promotion
multiple TensorCube features enabled together
historical conflict reinterpretation
scientific PASS/HOLD rewrite
fleet or installed-runtime rollout
```

Expected child sequence:

```text
R2-R6 = HeadwiseActive + TensorCube Stage 1 feature
R2-R7 = HeadwiseActive + sealed Stage 1 + TensorCube Stage 2 feature
R2-R8 = HeadwiseActive + sealed Stage 1..2 + TensorCube Stage 3 feature
...
```

Each child may introduce at most one new TensorCube feature bit.

---

## 3. Frozen parent authority

Required direct parent:

```text
R2-R4 pass=true
runtime/replay parity rows=78/78
f64 authority mismatches=0
replay repeat equal=true
key-order independent=true
raw pairs=8/8
sessions=16/16
timestamp samples=32768/32768
queue records=32768/32768
boundaries=32/32
reproductions=16/16
paired units=24/24
parent evidence graph immutable=true
```

R2-R5 must import and bind:

```text
R2-R4 runtime artifact
R2-R4 local manifest
R2-R4 source binding
R2-R4 source digest closure
R2-R4 runtime/replay parity receipt
R2-R4 determinism receipt
R2-R4 admission receipt
R2-R4 atlas digest
R1-R2 scientific terminal pair
R2-R3 generation lineage
reference route identity and manifest
headwise producer identity and runtime profile
```

All parent artifacts must remain SHA-256 exact before and after R2-R5.

---

## 4. State ownership and SSOT

The following state domains are independent.

### 4.1 HeadwiseEvidenceState

```text
owner=R1-R2 scientific runtime artifact
values=PASS|HOLD
mutable_by_R2_R5=false
meaning=scientific performance and localization evidence
```

### 4.2 AttentionRouteState

```text
owner=R2-R5 attention route manifest
values=ReferenceActive|HeadwisePrepared|HeadwiseActive|Quarantined
initial=ReferenceActive
target=HeadwiseActive
```

### 4.3 TensorCubeStageState

```text
owner=TensorCube stage manifest
values=Unregistered|Stage0ConsumerReady|StageNPrepared|StageNActive|StageNFallback|Quarantined
R2_R5_target=Stage0ConsumerReady
R2_R5_feature_mask=none
```

### 4.4 TensorCubeFeatureState

```text
owner=TensorCube feature registry
per_feature_values=Disabled|Prepared|Enabled|Quarantined
R2_R5_all_features=Disabled
one_new_enabled_feature_per_child_stage=true
```

### 4.5 KVOwnershipState

```text
owner=runtime device registry plus KV allocation receipt
values=Unbound|HeadwiseOwned|TensorCubeReadBorrowed|TensorCubeWriteLeased|Released
single_writer=true
```

### 4.6 FallbackChainState

```text
owner=stage fallback manifest
R2_R5=HeadwiseActive -> ReferenceActive
future=TensorCubeStageN -> TensorCubeStageN-1
future=TensorCubeStage1 -> HeadwiseActive
```

### 4.7 RoutePointerState

```text
owner=attention route registry
initial=REFERENCE_ROUTE
after_headwise_commit=HEADWISE_ROUTE
writes_allowed=exactly_one successful compare-and-swap
rollback_target=REFERENCE_ROUTE
```

No state domain may substitute for another. In particular:

```text
HeadwiseEvidenceState=HOLD does not imply AttentionRouteState=ReferenceActive
AttentionRouteState=HeadwiseActive does not imply HeadwiseEvidenceState=PASS
TensorCubeStageState=Stage0ConsumerReady does not imply any TensorCube feature is enabled
```

---

## 5. Headwise active route adoption

The headwise route identity must be frozen before activation.

Required identity:

```text
route_id=HEADWISE_ROUTE
producer_patch_id=<exact R1-R2 source patch>
producer_binary_sha256=<exact>
producer_runtime_profile_sha256=<exact>
producer_cli_sha256=<exact>
producer_device_identity=<exact>
producer_adapter_identity=<exact>
producer_generation=<exact>
output_layout_id=<exact>
kv_layout_id=<exact>
dtype_contract=<exact>
head_count=<exact>
kv_head_count=<exact>
head_dim=<exact>
page_size=<exact>
stride_contract=<exact>
```

Required adoption transition:

```text
ReferenceActive
-> HeadwisePrepared
-> HeadwiseActive
```

`HeadwisePrepared` requires:

```text
parent R2-R4 exact
headwise route identity exact
reference route identity exact
same-device contract exact
headwise output parity exact
headwise KV post-state parity exact
rollback receipt prepared
route compare-and-swap precondition exact
```

`HeadwiseActive` requires:

```text
active route compare-and-swap succeeded exactly once
previous route ID=REFERENCE_ROUTE
new route ID=HEADWISE_ROUTE
route generation advanced exactly once
headwise dispatches>0
reference dispatches=0 after commit except explicit rollback tests
no partial output publication
terminal route receipt complete
```

A scientific HOLD remains visible in the runtime artifact and manifest after functional adoption.

---

## 6. Headwise activation matrix

Minimum required HeadwiseActive tests:

```text
nominal decode
minimum declared KV
target KV 384
target KV 512
maximum declared KV
unsupported shape rollback
unsupported dtype rollback
insufficient capacity rollback
generation mismatch rejection
ownership mismatch rejection
device identity mismatch rejection
route identity mismatch rejection
partial-commit prevention
```

Each test reports:

```text
classification
headwise dispatch count
reference rollback dispatch count
commit state
active route before and after
route generation before and after
KV generation before and after
KV ownership before and after
host materialization counters
readback counters
output parity
KV post-state parity
```

Classifications:

```text
HeadwiseSupported
ExactReferenceRollbackRequired
ContractViolation
```

`ContractViolation` is terminal HOLD.

---

## 7. Headwise numerical and state parity

R2-R5 must compare:

```text
Headwise output vs reference output
Headwise KV-cache post-state vs reference KV-cache post-state
Headwise route metadata vs frozen route identity
Reference rollback output vs original reference output
Reference rollback KV-cache state vs original reference post-state
```

Authority uses the existing project bit-authority receipt policy where applicable.

No new tolerance may be introduced without a separately named policy and negative-control family.

Required:

```text
headwise output parity=true
headwise KV post-state parity=true
reference rollback output parity=true
reference rollback KV post-state parity=true
f64 bit-authority mismatches=0 where applicable
```

---

## 8. TensorCube Stage 0 consumer handoff

After `HeadwiseActive` is committed, R2-R5 creates a typed Stage 0 handoff descriptor.

Required descriptor fields:

```text
handoff_id
stage_id=tensorcube-stage-0-consumer-ready-v1
parent_attention_route_id=HEADWISE_ROUTE
parent_stage_id=headwise-active-baseline-v1
feature_mask=none
producer_device_id
consumer_device_id
producer_generation
consumer_registry_generation
q_buffer_id
k_buffer_id
v_buffer_id
kv_cache_id
output_buffer_id
q_offset_bytes
k_offset_bytes
v_offset_bytes
kv_offset_bytes
output_offset_bytes
q_length_bytes
k_length_bytes
v_length_bytes
kv_length_bytes
output_length_bytes
q_stride
k_stride
v_stride
kv_stride
output_stride
dtype
head_count
kv_head_count
head_dim
sequence_length
batch_size
read_only_inputs
single_writer_output
```

Stage 0 means:

```text
TensorCube consumer ABI registered=true
TensorCube stage registry installed=true
TensorCube feature mask=none
TensorCube computational dispatches=0
TensorCube KV writes=0
TensorCube output publication=0
Headwise remains the active execution route
```

Stage 0 must not contain a hidden identity kernel, no-op GPU kernel, or silent TensorCube fallback dispatch.

---

## 9. Incremental TensorCube stage model

Every child TensorCube stage must declare:

```text
stage_id
parent_stage_id
new_feature_id
inherited_feature_mask
new_feature_mask
producer_route_id=HEADWISE_ROUTE
consumer_binary_sha256
runtime_profile_sha256
device_identity
open_generation
commit_generation
fallback_stage_id
```

Required feature transition:

```text
Stage 0 mask = none
Stage 1 mask = feature_1
Stage 2 mask = feature_1 + feature_2
Stage N mask = inherited mask + exactly one new feature
```

Forbidden:

```text
enabling two new feature bits in one child stage
disabling an inherited sealed feature without quarantine receipt
skipping a parent stage
using ReferenceActive as TensorCube Stage 2+ direct parent
rewriting HeadwiseEvidenceState
rewriting an earlier stage artifact
```

---

## 10. Same-device contract

The following identities must be equal:

```text
Headwise producer physical_device_id
TensorCube consumer registry physical_device_id
Q buffer physical_device_id
K buffer physical_device_id
V buffer physical_device_id
KV-cache physical_device_id
output buffer physical_device_id
runtime registry physical_device_id
queue lineage physical_device_id
```

The following must also match:

```text
adapter identity
backend identity
queue identity lineage
runtime generation lineage
allocation generation lineage
```

Cross-device migration is forbidden in R2-R5.

---

## 11. KV ownership

Headwise adoption transition:

```text
Unbound
-> HeadwiseOwned
```

Stage 0 handoff transition:

```text
HeadwiseOwned
-> TensorCubeReadBorrowed
-> HeadwiseOwned
```

Because Stage 0 enables no computational feature:

```text
TensorCubeWriteLeased count=0
TensorCube KV write count=0
TensorCube output write count=0
```

Future Stage N ownership:

```text
HeadwiseOwned
-> TensorCubeReadBorrowed
-> optional TensorCubeWriteLeased for declared output only
-> HeadwiseOwned or next-stage-owned after atomic commit
```

Forbidden transitions:

```text
HeadwiseOwned -> CPUOwned
TensorCubeReadBorrowed -> HostMirrored
TensorCubeReadBorrowed -> DifferentDeviceOwned
Released -> TensorCubeReadBorrowed
multiple simultaneous writers
write lease without declared feature ownership
ownership transfer without generation increment
```

---

## 12. Zero-copy and zero-host contract

Required counters:

```text
q_host_materializations=0
k_host_materializations=0
v_host_materializations=0
kv_host_materializations=0
output_host_materializations=0
host_uploads=0
payload_readbacks=0
buffer_map_read_calls=0
buffer_map_write_calls=0
staging_buffer_roundtrips=0
cross_device_copies=0
```

Permitted host-visible data:

```text
opaque buffer IDs
byte lengths
offsets
strides
generation IDs
device IDs
route IDs
stage IDs
feature-mask IDs
status enums
bounded counters
```

Raw tensor payload is forbidden in every receipt.

---

## 13. Stage-scoped activation

R2-R5 activation requirements:

```text
explicit Headwise adoption CLI flag=true
explicit TensorCube Stage 0 registration flag=true
parent R2-R4 exact=true
headwise route prepared=true
headwise numerical parity=true
headwise KV parity=true
same device=true
KV ownership valid=true
shape contract supported=true
dtype contract supported=true
capacity sufficient=true
reference rollback prepared=true
TensorCube feature mask=none
```

R2-R5 result:

```text
AttentionRouteState=HeadwiseActive
TensorCubeStageState=Stage0ConsumerReady
TensorCube features enabled=0
Headwise dispatches>0
TensorCube computational dispatches=0
```

Activation may not be inferred from:

```text
parent scientific PASS
absence of conflict tuples
GPU feature availability alone
TensorCube binary presence
benchmark success
fallback success
```

---

## 14. Exact prior-stage fallback chain

Fallback chain:

```text
TensorCubeStageN -> TensorCubeStageN-1
TensorCubeStage1 -> HeadwiseActive
HeadwiseActive -> ReferenceActive
```

R2-R5 directly proves:

```text
HeadwiseActive -> ReferenceActive
```

R2-R5 also publishes the immutable fallback-chain schema that every child stage must inherit.

Prior-stage fallback requirements:

```text
same input identity
same physical device
same logical KV state
same decode step
same parent generation
same output layout
no stale child-stage output reuse
no partial child-stage commit
no hidden feature-mask mutation
```

Headwise rollback requirements:

```text
reference route ID exact
reference manifest digest exact
same logical KV pre-state
same decode step
no stale Headwise output reuse
no partial Headwise commit
route pointer restored by exact compare-and-swap
route generation advanced by declared rollback receipt only
```

Forbidden:

```text
Stage N falling directly to ReferenceActive while Stage N-1 is healthy
fallback after partial output publication
fallback using mutated KV state
fallback through CPU materialization
fallback on another device
fallback counted as child-stage success
fallback that silently changes the scientific terminal
```

---

## 15. Commit boundaries

### 15.1 Headwise commit boundary

Before commit:

```text
Headwise output provisional
KV writes provisional or isolated
ReferenceActive remains visible
rollback available
```

At commit:

```text
all Headwise submissions complete
required fences satisfied
no device loss
no generation drift
ownership valid
output receipt complete
KV parity complete
route compare-and-swap precondition exact
```

After commit:

```text
HeadwiseActive visible
route generation advances exactly once
ReferenceActive retained only as rollback target
```

### 15.2 TensorCube Stage 0 commit boundary

Before commit:

```text
consumer descriptor provisional
feature registry provisional
feature mask must equal none
```

At commit:

```text
consumer identity exact
same-device receipt exact
ownership borrow receipt complete
feature registry digest complete
fallback-chain schema complete
TensorCube computational dispatch count=0
```

After commit:

```text
Stage0ConsumerReady visible
all TensorCube feature states remain Disabled
HeadwiseActive remains active route
```

Partial commit is forbidden at both boundaries.

---

## 16. Cross-layer generation seal

Parent R2-R4 terminal generation:

```text
20
```

R2-R5 generations:

```text
Headwise prepare open=21
Headwise active commit=22
TensorCube Stage 0 registry open=23
R2-R5 terminal=24
```

Required relations:

```text
parent_terminal_generation=20
headwise_prepare_generation=21
headwise_active_generation=22
tensorcube_stage0_generation=23
terminal_generation=24
```

Every descriptor and receipt carries:

```text
parent_generation
route_generation
stage_generation
allocation_generation
ownership_generation
terminal_generation
```

Future TensorCube child stages must increment generations monotonically and may not reuse 21..24.

Forbidden:

```text
generation reuse
generation decrement
skipped generation without receipt
producer generation different from buffer generation
consumer generation different from stage owner
fallback reusing provisional child-stage generation
```

---

## 17. Device loss and drift handling

Before Headwise commit, the following trigger exact reference rollback or terminal HOLD according to the failure matrix:

```text
device lost
adapter identity drift
runtime registry reset
buffer generation drift
KV ownership drift
route identity drift
runtime profile drift
producer binary identity drift
fence timeout
capacity drift
```

After Headwise commit but before Stage 0 commit:

```text
HeadwiseActive remains active only if its commit receipt is unambiguous
Stage 0 registration fails closed
no TensorCube feature is enabled
```

After any ambiguous publication:

```text
terminal HOLD
route quarantine
no automatic retry
```

---

## 18. Route-pointer rules

R2-R5 permits exactly one successful active-route adoption write:

```text
REFERENCE_ROUTE -> HEADWISE_ROUTE
```

Required compare-and-swap fields:

```text
expected route ID
expected route digest
expected route generation
new route ID
new route digest
new route generation
writer patch ID
commit receipt digest
```

Forbidden pointer writes:

```text
TensorCube Stage 0 becoming active attention route
TensorCube feature route becoming active in R2-R5
unknown previous route replacement
blind overwrite
multiple successful adoption writes
stable alias mutation without receipt
installed production pointer mutation outside the declared attention registry
```

The reference route artifact and binary must remain available for exact rollback.

---

## 19. Atlas parallel group map

R2-R5 runtime artifact uses a thin typed streaming root with exactly 18 authority groups:

```text
identity
parent_binding
parent_terminal
evidence_preservation
reference_route
headwise_route
headwise_adoption
headwise_parity
tensorcube_stage_registry
tensorcube_consumer
handoff_descriptor
same_device
kv_ownership
zero_copy
fallback_chain
cross_layer_generation
route_pointer
verdict
```

Each group contains:

```text
group_id
schema
field_count
canonical_payload_json
canonical_payload_sha256
group_digest
fields mirror
```

Canonical payload is authoritative. `fields` is a non-authoritative mirror under the existing projection policy.

Runtime root serialization must use typed streaming serialization. A full root `serde_json::Value` tree is forbidden.

---

## 20. Required artifacts

```text
*_parent_binding.json
*_parent_terminal_binding.json
*_evidence_preservation.json
*_reference_route_identity.json
*_headwise_route_identity.json
*_headwise_adoption_receipt.json
*_headwise_dispatch_receipts.json
*_headwise_parity.json
*_reference_rollback_receipts.json
*_tensorcube_stage_registry.json
*_tensorcube_consumer_identity.json
*_stage0_handoff_descriptor.json
*_same_device_receipt.json
*_kv_ownership_receipt.json
*_zero_copy_receipt.json
*_fallback_chain.json
*_commit_boundary_receipts.json
*_cross_layer_generation.json
*_route_pointer_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

The local manifest closes:

```text
all child artifacts
all parent artifact digests
all atlas group digests
atlas digest
runtime profile digest
CLI digest
reference binary identity
headwise producer binary identity
TensorCube consumer binary identity
reference route digest
HeadwiseActive route digest
Stage 0 registry digest
fallback-chain digest
active route pointer digest
```

---

## 21. CLI contract

Required policy keys include:

```text
--gqa4-r2f-r6-r5-r1-r2-r5-parent-r2-r4-artifact
--gqa4-r2f-r6-r5-r1-r2-r5-parent-r2-r4-manifest
--gqa4-r2f-r6-r5-r1-r2-r5-reference-route-id
--gqa4-r2f-r6-r5-r1-r2-r5-headwise-active-route-id
--gqa4-r2f-r6-r5-r1-r2-r5-tensorcube-stage-id
--gqa4-r2f-r6-r5-r1-r2-r5-tensorcube-feature-mask
--gqa4-r2f-r6-r5-r1-r2-r5-route-adoption-policy
--gqa4-r2f-r6-r5-r1-r2-r5-handoff-policy
--gqa4-r2f-r6-r5-r1-r2-r5-kv-ownership-policy
--gqa4-r2f-r6-r5-r1-r2-r5-stage-policy
--gqa4-r2f-r6-r5-r1-r2-r5-activation-policy
--gqa4-r2f-r6-r5-r1-r2-r5-fallback-policy
--gqa4-r2f-r6-r5-r1-r2-r5-generation-policy
--enable-gqa4-r2f-r6-r5-r1-r2-r5-headwise-active-adoption
--enable-gqa4-r2f-r6-r5-r1-r2-r5-tensorcube-stage0-registration
--require-gqa4-r2f-r6-r5-r1-r2-r5-tensorcube-feature-mask-none
--require-gqa4-r2f-r6-r5-r1-r2-r5-same-device
--require-gqa4-r2f-r6-r5-r1-r2-r5-zero-host-materialization
--require-gqa4-r2f-r6-r5-r1-r2-r5-zero-host-upload
--require-gqa4-r2f-r6-r5-r1-r2-r5-zero-readback
--require-gqa4-r2f-r6-r5-r1-r2-r5-single-writer-output
--require-gqa4-r2f-r6-r5-r1-r2-r5-headwise-route-commit-exact
--require-gqa4-r2f-r6-r5-r1-r2-r5-exact-reference-rollback
--require-gqa4-r2f-r6-r5-r1-r2-r5-prior-stage-fallback-schema
--require-gqa4-r2f-r6-r5-r1-r2-r5-parent-terminal-preserved
--require-gqa4-r2f-r6-r5-r1-r2-r5-cross-layer-generation-exact
```

Unknown, duplicate, missing, wrong-value, and wrong-polarity keys are terminal HOLD.

---

## 22. Negative controls

R2-R5 adds at least 44 groups of 10 negative controls:

```text
new negative controls >=440
```

Required groups include:

```text
parent artifact mutation
parent terminal rewrite attempt
reference route ID mutation
headwise route ID mutation
blind route pointer overwrite
route compare-and-swap expected-ID mismatch
route compare-and-swap generation mismatch
multiple route adoption writes
Headwise activation without explicit flag
Headwise output parity corruption
Headwise KV parity corruption
reference rollback route mutation
reference rollback after partial Headwise commit
Stage 0 feature mask non-empty
Stage 0 hidden TensorCube dispatch
Stage 0 hidden TensorCube KV write
consumer route ID mutation
producer/consumer device mismatch
Q device mismatch
K device mismatch
V device mismatch
KV-cache device mismatch
output device mismatch
ownership double-writer
stale ownership token
buffer generation drift
route generation drift
stage generation drift
host materialization injection
host upload injection
payload readback injection
buffer map read injection
buffer map write injection
cross-device copy injection
unsupported shape misclassified as supported
unsupported dtype misclassified as supported
capacity overflow
fallback-chain parent skip
Stage 1 direct fallback to reference while HeadwiseActive is healthy
missing Headwise commit receipt
missing Stage 0 commit receipt
ambiguous device-loss publication
atlas group mutation
atlas digest mutation
manifest omission
canonical args mutation
binary identity mutation
```

Every negative control must fail for the intended reason and leave a deterministic route and ownership state.

---

## 23. PASS

PASS requires all of the following:

```text
parent R2-R4 PASS exact
parent scientific terminal pair preserved exact
parent artifacts immutable
reference route identity exact
headwise route identity exact
HeadwisePrepared reached
HeadwiseActive committed exactly once
active route pointer changed REFERENCE_ROUTE -> HEADWISE_ROUTE exactly once
headwise dispatches>0
headwise output parity exact
headwise KV post-state parity exact
reference rollback output parity exact
reference rollback KV post-state parity exact
TensorCube Stage 0 registry exact
TensorCube consumer identity exact
typed Stage 0 handoff descriptor complete
TensorCube feature mask=none
TensorCube computational dispatches=0
TensorCube KV writes=0
TensorCube output writes=0
same physical device across producer, consumer, Q/K/V, KV-cache, and output
single-writer ownership exact
zero host materialization
zero host upload
zero payload readback
zero buffer maps
zero cross-device copies
exact HeadwiseActive -> ReferenceActive rollback proven
future prior-stage fallback schema sealed
cross-layer generations 20->21->22->23->24 exact
18/18 atlas groups exact
all required artifacts present
manifest closure exact
all new negative controls pass
```

R2-R5 PASS means:

```text
Headwise is the active attention baseline.
TensorCube is registered as a Stage 0 consumer.
No TensorCube computational feature is enabled yet.
The next child may enable exactly one TensorCube feature.
```

R2-R5 PASS does not imply:

```text
scientific performance PASS
TensorCube production performance superiority
multiple TensorCube features may be activated together
reference rollback may be removed
```

---

## 24. HOLD

HOLD occurs on any:

```text
parent identity or digest mismatch
parent terminal rewrite
reference route identity drift
headwise route identity drift
Headwise output parity failure
Headwise KV parity failure
route compare-and-swap mismatch
multiple active-route writes
partial Headwise commit
reference rollback mismatch
TensorCube Stage 0 feature mask not empty
hidden TensorCube computational dispatch
hidden TensorCube KV or output write
consumer identity drift
same-device mismatch
ownership ambiguity
multiple writers
host materialization
host upload
payload readback
buffer mapping
cross-device copy
unsupported input accepted as HeadwiseSupported
fallback-chain parent skip
generation mismatch
device-loss ambiguity
atlas mismatch
manifest mismatch
negative-control failure
```

No automatic retry, silent downgrade, route substitution, feature-mask repair, or state repair is allowed.

---

## 25. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R5_HEADWISE_ACTIVE_ROUTE_ADOPTION_TENSORCUBE_INCREMENTAL_CONSUMER_HANDOFF_SAME_DEVICE_KV_OWNERSHIP_STAGE_SCOPED_FEATURE_ACTIVATION_EXACT_PRIOR_STAGE_FALLBACK_AND_CROSS_LAYER_GENERATION_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R5_HEADWISE_ADOPTION_TENSORCUBE_STAGE0_HANDOFF_DEVICE_OWNERSHIP_FALLBACK_OR_GENERATION_NOT_PROVEN
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r5][summary]
parent_r2_r4=PASS
parent_scientific_terminal=<PASS|HOLD>
parent_terminal_preserved=true
reference_route_bound=true
headwise_route_prepared=true
headwise_route_active=true
active_route_before=REFERENCE_ROUTE
active_route_after=HEADWISE_ROUTE
route_pointer_writes=1/1
headwise_dispatches=<exact>/<exact>
headwise_output_parity=true
headwise_kv_parity=true
reference_rollback_output_parity=true
reference_rollback_kv_parity=true
tensorcube_stage=Stage0ConsumerReady
tensorcube_feature_mask=none
tensorcube_features_enabled=0
tensorcube_compute_dispatches=0
tensorcube_kv_writes=0
tensorcube_output_writes=0
same_device=true
kv_ownership_valid=true
host_materializations=0
host_uploads=0
payload_readbacks=0
buffer_maps=0
cross_device_copies=0
fallback_chain=headwise-to-reference-plus-stage-n-to-stage-n-minus-1
generations=20/21/22/23/24
atlas_groups=18/18
new_negative=<passed>/<expected>
pass=true
```

---

## 26. Final seal

```text
preserved R2-R4 replay authority
+ preserved parent scientific PASS or HOLD terminal pair
+ exact reference route identity
+ immutable headwise route identity
+ functional HeadwisePrepared validation
+ exact HeadwiseActive route commit
+ headwise dispatches through the adopted route
+ exact headwise output and KV parity
+ exact reference rollback
+ TensorCube Stage 0 consumer registry
+ typed same-device handoff descriptor
+ TensorCube feature mask none
+ zero TensorCube computational dispatch at Stage 0
+ single-device Q/K/V/KV-cache/output ownership
+ single-writer discipline
+ zero host materialization
+ zero host upload
+ zero payload readback
+ exact prior-stage fallback schema
+ one-new-feature-per-child-stage rule
+ cross-layer generation lineage
= proof that Headwise is now the active attention baseline and TensorCube can be enabled one feature at a time without losing exact rollback, state ownership, or evidence integrity
```
