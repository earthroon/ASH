# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-RESIDENT-POST-UPDATE-EVIDENCE-AND-DEVICE-SEGMENTED-SUCCESSOR-APPLICATION-CLOSURE-R1

## Physical candidate-arena ownership handoff / Muon segmented target generation / BP-DeltaK device evidence arena / exact capability decomposition / no false device-evidence or next-generation-source claim

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-RESIDENT-POST-UPDATE-EVIDENCE-AND-DEVICE-SEGMENTED-SUCCESSOR-APPLICATION-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CORE-MATERIALIZATION-AND-BP-DK-DEVICE-RESIDENT-POST-UPDATE-GATE-CLOSURE-R2`

PASS token reserved for full physical closure:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_BP_DK_DEVICE_RESIDENT_POST_UPDATE_EVIDENCE_AND_DEVICE_SEGMENTED_SUCCESSOR_APPLICATION_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_BP_DK_DEVICE_RESIDENT_POST_UPDATE_R1_STATIC`

## 1. Purpose

The parent R2 materialized the real bounded Production Muon pending queue core but correctly left the production cutover disabled because `AshBpDkPostUpdateStreamingBuilder::push_tile()` still requires host candidate weight, candidate momentum and orthogonal-update `f32` tiles.

The previous ActiveDevice child already preserves those three payloads on GPU. This revision begins the physical replacement of the host post-update path by moving Local Muon candidate arena ownership into stable device-side authorities.

The revision MUST NOT call that ownership handoff a complete BP-DeltaK device post-update implementation until the device reduction/digest producer and next-generation device-source Local Muon submit path both exist.

## 2. Source-derived correction

The source currently has no concrete `MuonDeviceSegmentedGenerationR1` owner. `DeviceTrainableConsumerCapability::DeviceSegmentedGenerationV1` is a B06 capability label, not proof that next-generation Muon weight and momentum physically exist under a persistent segmented owner.

The source also still accepts Local Muon source weight and momentum as host slices and uploads them. Therefore even after a target segmented generation exists, the next ActiveDevice generation cannot yet consume it directly.

These are separate physical gaps and MUST remain separately visible.

## 3. Capability decomposition

This revision defines four source-truth capabilities.

`TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_SEGMENTED_BACKING_HANDOFF_MATERIALIZED_R1 = true`

means real candidate weight/momentum arena ownership can leave the Local Muon successor and enter a stable segmented device backing while orthogonal update enters a separate evidence backing, without full D2H.

`TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_POST_UPDATE_REDUCTION_AND_DIGEST_MATERIALIZED_R1 = false`

means the device-side RMS/cosine reduction plus exact canonical f32 SHA256 producer is not yet materialized in this bake.

`TENSORCUBE_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_SUBMIT_MATERIALIZED_R1 = false`

means Local Muon cannot yet accept the previous segmented device generation directly as source weight/momentum without host H2D.

The aggregate:

`TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_RESIDENT_POST_UPDATE_CONSUMER_MATERIALIZED_R1`

is the logical AND of all three capabilities and is therefore false in this bake.

The parent R2 gate imports that aggregate instead of a literal `false` so later physical children can close the missing pieces without weakening the gate.

## 4. No capability override

None of these values may be forced by environment, CLI, receipt content or qualification fixtures.

## 5. Physical Local Muon handoff

`LocalMuonActiveDeviceSuccessorR1::into_device_segmented_handoff_r1()` consumes a B06-claimed ActiveDevice successor.

It requires:

- B06 successor ticket already claimed;
- successor state `SuccessorClaimed`;
- ActiveDevice zero-full-D2H transfer contract valid;
- target generation exactly source generation + 1.

It moves the existing candidate arena ownership. It does not copy candidate payloads to the host.

## 6. Stable segmented weight/momentum backing

`MuonDeviceSegmentBackingR1` owns:

- canonical parameter index;
- source generation;
- target generation;
- element count;
- candidate-weight physical allocation identity;
- candidate-momentum physical allocation identity;
- exact SubmissionEpoch set;
- exact P4 lease digest inherited from the producing Wave;
- candidate weight `ArenaLease` and WGPU buffer;
- candidate momentum `ArenaLease` and WGPU buffer;
- exact backing digest.

The backing is an actual GPU resource owner, not a metadata-only descriptor.

## 7. Temporary orthogonal-update evidence backing

`BpDkDeviceUpdateEvidenceBackingR1` separately owns:

- canonical parameter index;
- source and target generation;
- element count;
- update allocation identity;
- exact SubmissionEpoch set;
- exact P4 lease digest;
- update `ArenaLease` and WGPU buffer;
- exact backing digest.

Orthogonal update is evidence state, not part of the next model generation.

## 8. Ownership transfer

After `into_device_segmented_handoff_r1()` succeeds, the original `LocalMuonActiveDeviceSuccessorR1` no longer owns the candidate weight, candidate momentum or update arenas.

The resulting `LocalMuonDeviceSegmentedHandoffR1` owns exactly:

- one `MuonDeviceSegmentBackingR1`;
- one `BpDkDeviceUpdateEvidenceBackingR1`.

No duplicate physical owner is introduced.

## 9. Explicit release

Both backing types provide explicit release paths that reclaim only their own exact A02 arena leases using the original logical lease identity.

Dropping a live backing without explicit release emits a hard diagnostic. Drop is not silent successful retirement.

## 10. Muon target generation owner

`MuonDeviceSegmentedGenerationR1` is the runtime-local physical owner for one candidate Muon target generation.

It binds:

- source generation;
- target generation;
- expected parameter count;
- expected element count;
- exact per-parameter `MuonDeviceSegmentBackingR1` objects;
- published element count.

## 11. Generation invariants

Target generation MUST equal source generation + 1.

Each canonical parameter index may be published exactly once.

Each segment MUST match the generation owner's source and target generation.

Published element count may never exceed the expected count.

## 12. Generation publication receipt

`MuonDeviceSegmentedGenerationPublicationReceiptR1` records:

- source/target generation;
- expected/published/missing parameter counts;
- expected/published/missing element counts;
- full weight D2H bytes;
- full momentum D2H bytes;
- completeness;
- generation digest.

For the materialized handoff path, full weight and momentum D2H are zero.

A complete receipt requires exact parameter and element coverage with no missing state.

## 13. BP-DeltaK device update evidence arena

`BpDkDevicePostUpdateEvidenceArenaR1` owns per-parameter orthogonal-update backing for one source/target generation pair.

Each parameter may publish update evidence backing exactly once.

The evidence arena may release one parameter after its future device post-update finalization, or all remaining parameters during explicit failure/drain.

## 14. Combined publish helper

`publish_local_muon_segmented_handoff_r1()` atomically validates generation/parameter agreement between the segmented weight/momentum backing and update evidence backing before publishing them into their respective stable owners.

This helper does not perform BP-DeltaK numerical evidence production.

## 15. BP-DeltaK device post-update plan ABI

`BpDkDevicePostUpdatePlanR1` reserves the exact future physical contract for:

- canonical parameter index;
- source and target generation;
- expected tile count;
- expected pair count;
- host-oracle receipt digest;
- deterministic reduction policy `ASH.BP-DK.DEVICE.POST-UPDATE.REDUCTION.R1`;
- exact digest policy `ASH.BP-DK.DEVICE.POST-UPDATE.F32-SHA256.R1`;
- plan digest.

The ABI exists in this bake. The physical GPU producer does not yet.

## 16. Existing host BP-DeltaK receipt remains canonical

This revision does not replace `AshBpDkPostUpdateParameterReceipt`.

Future device-produced compact evidence must still reconstruct and validate the same semantic receipt, or explicitly re-qualify any changed contract in a later revision.

Planner feedback and post-update policy mutation remain zero.

## 17. Exact digest requirement remains open

The existing host path hashes canonical f32 candidate weight, candidate momentum and orthogonal update exactly.

The future device producer MUST emit exact equivalent SHA256 digests under the declared `ASH.BP-DK.DEVICE.POST-UPDATE.F32-SHA256.R1` framing.

This bake does not claim that producer exists.

Approximate statistics or allocation digests cannot substitute for those exact candidate digests.

## 18. RMS/cosine requirement remains open

The future device producer must compute the current BP-DeltaK tile RMS and pair cosine semantics with explicit finite and zero-norm classification.

Numerical parity/tolerance must be established physically against the existing host implementation.

This bake does not invent an unqualified tolerance.

## 19. P5 semantic consumer extension

`McuWaveConsumerKindR1` gains:

- `BpDkDevicePostUpdateEvidence`;
- `MuonSegmentedSuccessorApplication`.

These tokens reserve exact semantic lifetime identities for the later production cutover. They are not synthetic blanket counters.

## 20. P4 lifetime separation

P4 remains authority for ephemeral Atlas Wave residency.

A future production Wave may retire its P4 lease after candidate weight/momentum/update have moved into stable device owners and all Wave-local P5 consumers close.

The longer-lived target segmented generation and BP-DeltaK evidence arena then continue under their own resource ownership.

## 21. Production cutover remains disabled

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1` remains false.

The existing streaming loop still invokes host `post_update_builder.push_tile()` and writes host candidate momentum/state.

The aggregate BP-DeltaK device-resident consumer remains false, so the R2 ActiveAsync preflight continues to fail closed before the legacy Mirror-only host path.

## 22. Device-source next-generation blocker

The inspected Local Muon ActiveDevice submission still accepts source weight and momentum as host slices and creates H2D source uploads.

Therefore this bake MUST NOT claim that `MuonDeviceSegmentedGenerationR1(G+1)` is already consumed as the source for the next ActiveDevice generation.

The missing source capability is explicitly:

`TENSORCUBE_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_SUBMIT_MATERIALIZED_R1 = false`.

## 23. No fake next-generation evidence

A target segmented generation object alone is not proof of device-generation continuation.

Physical closure later requires at least one subsequent real Local Muon submission to bind the previous generation's weight/momentum device buffers directly and record zero source weight/momentum H2D for that path.

## 24. Closure receipt

`BpDkDeviceResidentPostUpdateClosureReceiptR1` records source-truth sub-capabilities independently from physical counters.

`structural_observed()` emits verdict `OBSERVED` and no PASS token.

It cannot produce a full PASS while device reduction/digest or device-source submit capabilities remain false.

## 25. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1_static.py`.

It verifies:

- exact revision identity;
- real `MuonDeviceSegmentBackingR1` physical owner;
- real update evidence backing owner;
- successor-consuming ownership transfer API;
- generation owner and publication receipt;
- evidence arena;
- deterministic reduction/digest ABI labels;
- P5 semantic consumer extensions;
- backing handoff capability true;
- GPU reduction/digest capability false;
- next-generation device-source submit capability false;
- aggregate capability not hardcoded true;
- production queue cutover remains false;
- existing host BP-DeltaK streaming callsite is still present and therefore remains the live blocker.

## 26. Current bake state

Materialized:

- physical candidate weight/momentum arena ownership transfer;
- physical orthogonal-update evidence ownership transfer;
- `MuonDeviceSegmentedGenerationR1` target owner;
- exact per-parameter target publication;
- target generation coverage receipt;
- `BpDkDevicePostUpdateEvidenceArenaR1`;
- deterministic future device evidence plan ABI;
- exact future SHA256 policy ABI;
- P5 semantic consumer ABI extension;
- R2 parent gate wired to the aggregate source-truth capability;
- static validator and parent validator adaptation.

Not materialized:

- actual GPU RMS/cosine BP-DeltaK reducer;
- actual GPU exact canonical f32 SHA256 producer;
- compact BP-DeltaK evidence readback/finalizer;
- Active Local Muon direct device-source weight/momentum submit;
- next-generation device-source reuse physical evidence;
- production pending-queue streaming-loop cutover;
- parent P5 physical PASS.

## 27. Required next physical child A

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-POST-UPDATE-REDUCTION-EXACT-DIGEST-AND-COMPACT-EVIDENCE-MATERIALIZATION-R1`

must implement the actual GPU producer for:

- tile RMS/delta RMS;
- pair cosine and zero-norm classification;
- exact canonical candidate-weight SHA256;
- exact canonical candidate-momentum SHA256;
- exact canonical orthogonal-update SHA256;
- compact evidence readback;
- reconstruction/validation against the canonical host BP-DeltaK receipt.

Only then may `TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_POST_UPDATE_REDUCTION_AND_DIGEST_MATERIALIZED_R1` become true.

## 28. Required next physical child B

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-DEVICE-SEGMENTED-SOURCE-DIRECT-SUBMIT-AND-NEXT-GENERATION-REUSE-CLOSURE-R1`

must allow the next ActiveDevice Local Muon submission to read source weight/momentum directly from `MuonDeviceSegmentedGenerationR1` device backing without full H2D.

Only then may `TENSORCUBE_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_SUBMIT_MATERIALIZED_R1` become true.

## 29. Aggregate gate after both children

When both missing physical capabilities are source-truth true, the aggregate BP-DeltaK device-resident consumer becomes true automatically.

The production queue cutover remains a separate subsequent source change and physical campaign.

## 30. AdamW full-model caveat

The current inspected source still needs independent verification of the AdamW Active device-candidate production staging path before claiming the entire full-model `DeviceSegmentedGenerationV1` successor authority.

Muon segmented generation closure does not silently imply AdamW closure.

## 31. Compile boundary

A release Rust compile is mandatory because this child moves `ArenaLease`, logical lease IDs and WGPU buffer ownership across new exported types.

The current assistant environment has no `cargo`, `rustc` or `rustfmt`; therefore this bake claims source/static validation only.

## 32. Packaging policy

Source ZIP excludes:

- this specification and all Markdown;
- `specs/`;
- patch notes;
- `BAKE_MANIFEST*`;
- generated receipts/evidence;
- runtime qualification JSON/JSONL;
- `current.json` and `publication_seal.json`;
- P3 runtime transaction artifacts;
- logs/review outputs;
- Python bytecode caches.

Implementation Rust/Python source remains included.

## 33. GitHub publication policy

GitHub publication is spec-only unless implementation publication is explicitly requested.

## 34. Structural PASS semantics for this bake

The source/static bake proves that the Local Muon ActiveDevice successor can physically surrender candidate weight/momentum/update arena ownership into stable device-side successor/evidence owners with exact generation, allocation, SubmissionEpoch and P4 lease identity preserved, while no full candidate D2H is introduced.

It also proves that the source refuses to call this a complete BP-DeltaK device post-update consumer before the device reduction/digest producer and next-generation device-source submit path exist.

## 35. Full revision PASS remains withheld

The revision PASS token is not valid until physical evidence proves the complete specification, including device BP-DeltaK evidence/digest parity and next-generation direct device-source reuse.

## 36. Center sentence

**이번 베이크는 다음 세대의 몸체를 먼저 만든다. Local Muon candidate weight와 momentum은 더 이상 successor object가 끝날 때 버려지지 않고 실제 segmented generation backing으로 ownership이 이동하고, update는 별도 device evidence arena로 간다. 하지만 몸체가 생겼다고 BP-DeltaK의 눈과 다음 step의 입력까지 생긴 것은 아니다. GPU reduction/SHA256 producer와 device-source submit가 실제로 생기기 전까지 aggregate gate는 false다.**