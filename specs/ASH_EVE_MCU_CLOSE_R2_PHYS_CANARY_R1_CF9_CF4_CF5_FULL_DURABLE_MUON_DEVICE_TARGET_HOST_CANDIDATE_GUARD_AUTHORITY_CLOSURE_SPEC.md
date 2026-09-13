# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF5

## FULL-DURABLE MUON DEVICE-TARGET
## HOST-CANDIDATE GUARD AUTHORITY CLOSURE

```text
+ FULL-DURABLE GUARD DECOUPLED FROM ACTIVE-ASYNC FLAG
+ B05 DEVICE-COMPACT MUON TARGET PUBLICATION AUTHORITY
+ EXACT PARAMETER SEGMENT PUBLICATION WITNESS
+ SOURCE / TARGET GENERATION PARITY
+ CANONICAL PARAMETER INDEX PARITY
+ PUBLISHED ELEMENT COUNT PARITY
+ DEVICE TARGET PHYSICAL ALLOCATION IDENTITY
+ HOST CANDIDATE VEC ZERO PRESERVATION
+ CF4-CF2 SEGMENTED HANDOFF AUTHORITY REUSE
+ FULL TRAINABLE DEVICE GENERATION ASSEMBLY PRESERVATION
+ NO candidate_weight_device_generation_only FAKE PROMOTION
+ NO C08 ACTIVE-ASYNC CLAIM
+ NO P5 CUTOVER CLAIM
+ NO HOST CANDIDATE MATERIALIZATION
+ NO DUPLICATE DEVICE TARGET
```

## 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF5
Direct parent: ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF4
Class: FULL-DURABLE MUON TARGET AUTHORITY / HOST-CANDIDATE GUARD REALIGNMENT
```

Parent CF4 is physically crossed: DeviceCompactCandidate produced exact SHA digests, canonical BP-DK post receipt, optimizer-generation binding PASS, zero full-candidate D2H, and zero host-candidate materialization.

Current first failure before CF5:

```text
E_MCU_FULL_DURABLE_R1_MUON_HOST_CANDIDATE_REACHED
```

The host candidate Vec is actually empty. The obsolete guard fails because it also requires `candidate_weight_device_generation_only == true`; that flag tracks ActiveAsync/P5 execution shape and is not durable target ownership proof.

## 1. Authority law

```text
DURABLE MUON TARGET AUTHORITY != ACTIVE-ASYNC EXECUTION MODE
```

`candidate_weight_device_generation_only` remains an execution-shape witness only. CF5 does not force or reinterpret it.

The durable SSOT is the existing canonical publication:

```text
runtime.mcu.physical_generation.muon_target
```

CF4-CF2 already publishes exact candidate segments through `publish_local_muon_segmented_handoff_r1(...)`. CF5 does not allocate, copy, or republish a second target.

## 2. Host-candidate guard correction

The legacy error is retained only for actual host Weight candidate presence:

```text
candidate_weight_packed.is_empty() == false
  -> E_MCU_FULL_DURABLE_R1_MUON_HOST_CANDIDATE_REACHED
```

The universal durable guard no longer requires `candidate_weight_device_generation_only == true`.

In-place/streamed legacy shapes remain rejected from this full-durable path rather than silently converted.

## 3. Exact published-target admission

CF5 adds the typed view:

```text
FullDurableMuonTargetAdmissionCf5
```

It resolves the exact existing `muon_target.segment(canonical_parameter_index)` and fail-closes unless:

```text
B05 mode == ActiveDeviceCandidate

target_generation == source_generation + 1

generation.source_generation == requested source_generation
generation.target_generation == requested target_generation

segment.canonical_parameter_index == requested canonical parameter
segment.source_generation == requested source_generation
segment.target_generation == requested target_generation
segment.element_count == expected Muon element count

Weight/Momentum PhysicalAllocationId device identity is exact
segment backing digest is present
```

Physical allocation ordinals are witnesses, not standalone lifetime authority.

## 4. Durable authority classification

For diagnostics:

```text
candidate_weight_device_generation_only=true
  -> ACTIVE_ASYNC_DEVICE_GENERATION

candidate_weight_device_generation_only=false
  -> DEVICE_COMPACT_PUBLISHED_TARGET
```

Both require an actual published canonical Muon target segment.

Current CF7 CANARY should show:

```text
candidate_weight_device_generation_only=false
p5_active=false
c08_mode=MirrorVerified
selected_durable_authority=DEVICE_COMPACT_PUBLISHED_TARGET
```

No C08 ActiveAsync or P5 cutover claim is made.

## 5. Required witnesses

```text
[ASH-MCU-FULL-DURABLE-CF9-CF4-CF5][muon-target-authority]
[ASH-MCU-FULL-DURABLE-CF9-CF4-CF5][muon-target-publication]
[ASH-MCU-FULL-DURABLE-CF9-CF4-CF5][generation-parity]
[ASH-MCU-FULL-DURABLE-CF9-CF4-CF5][parameter-parity]
[ASH-MCU-FULL-DURABLE-CF9-CF4-CF5][admission]
```

The publication witness carries exact parameter/generation/element identity plus Weight/Momentum physical allocation ordinals. The admission witness must report:

```text
host_candidate_zero=true
muon_target_published=true
parameter_identity_exact=true
generation_exact=true
element_count_exact=true
physical_identity_present=true
admitted=true
```

Strong current proof:

```text
candidate_weight_device_generation_only=false
selected_durable_authority=DEVICE_COMPACT_PUBLISHED_TARGET
host_candidate_zero=true
muon_target_published=true
admitted=true
```

## 6. Preserved boundaries

CF5 preserves:

```text
CF4-CF2 Atlas-wave pre-reclaim candidate handoff
CF4-CF3 FreshGenesis source authority
CF4-CF4 persistent ExactSha256 producer
CF4 DEVICE_COMPACT BP-DK receipt
BP-DK target optimizer-generation binding PASS
FullTrainableDeviceGenerationR1 assembly authority
AdamW device-target authority
transactional commit/abort ordering
```

Previous blockers remain retired:

```text
BpDkPostUpdateCandidateCardinality
E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING
E_CF9_CF4_SOURCE_GENERATION_MISSING
E_CF9_CF4_CF3_EXACT_DIGEST_PRODUCER_REQUIRED
```

## 7. Forbidden repairs

```text
NO candidate_weight_device_generation_only fake promotion
NO C08 ActiveAsync promotion
NO P5 enablement solely for durable admission
NO host candidate reconstruction
NO zero-filled compatibility Vec
NO D2H durable fallback
NO second Muon device target
NO target republish after CF4-CF2
NO receipt digest used as Buffer lifetime proof
NO PhysicalAllocationId-only lifetime inference
NO speculative resource-ceiling increase
```

## 8. Full generation preservation

After per-parameter Muon and AdamW targets are complete, existing authority remains:

```text
assemble_full_trainable_device_generation_r1(target_generation)
```

CF5 introduces no alternate full-generation type and no full-size GPU allocation.

## 9. Acceptance

Static:

```text
host-candidate error guards actual non-empty host Vec only
candidate_weight_device_generation_only no longer gates durable ownership
exact muon_target segment lookup exists
parameter/generation/element parity checks exist
physical Weight/Momentum identity witness exists
no duplicate target allocation
no host fallback
CF2/CF3/CF4 semantics unchanged
```

Compile:

```text
base_train release PASS
```

Bake environment has no Rust toolchain; native CF1 release compile on the campaign machine remains compile authority.

Physical CF5 boundary:

```text
CF4 DEVICE_COMPACT receipt
BP-DK generation-binding PASS
selected_durable_authority=DEVICE_COMPACT_PUBLISHED_TARGET
candidate_weight_device_generation_only=false
muon_target_published=true
host_candidate_zero=true
parameter/generation/element exact
CF5 admission admitted=true
execution passes the old full-durable Muon guard
```

Recommended token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF5
```

Non-claims:

```text
NO C08 ActiveAsync claim
NO P5 production cutover claim
NO full R1B closure claim
NO full transaction commit claim
NO A/B/C promotion claim
```

## 10. Bake seal

```text
ADD 0
MOD 2
DEL 0
```

Modified source SHA-256:

```text
04247bdadbd13fc10f8185f29177b6f35712dd91e8c49ec1e358344ddb7bf5e4  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
27b400a4a1f7ea8235109e394dc2786643611269087558c2590df878d7d97691  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

Full code-only ZIP SHA-256:

```text
18911ad90d11e426d2589f3f5de83cfd676e9d537f33d4fc95c0da1e3c0e08b3
```

Overlay code-only ZIP SHA-256:

```text
8ee723dfc3f62bb81350076a827b1c2bc9dc0a08bc0802a1b54bcf0911a59181
```

Full ZIP: 8424 files. Both ZIPs CRC-clean. Code ZIPs contain no `specs/` or `artifacts/` payload.