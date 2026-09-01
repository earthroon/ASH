# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1

## Full Trainable Device Generation / Bounded Device-to-R6 Durable Projection / ActiveVerified Host Candidate Retirement / Existing R6 Restart Contract Preservation

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-ACTIVE-DEVICE-PENDING-GENERATION-PRODUCTION-SCHEDULER-AND-MULTI-SEGMENT-COLLECT-CLOSURE-R1`

Static/source PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_FULL_TRAINABLE_DEVICE_GENERATION_BOUNDED_DURABLE_PACK_PROJECTION_OUTER_HOST_SCATTER_RETIREMENT_R1_STATIC`

Full physical PASS is reserved and is not claimed by this source bake.

## 1. Purpose

P1 closes real AdamW ActiveDevice production submission, real `SubmissionEpoch`, bounded pending ownership, later collect, partitioned AdamW fragments and the real B06 device-generation stage callsite.

The remaining current-format boundary is durable materialization. Before this child, a GPU G+1 generation may win execution while the outer optimizer still reconstructs the same G+1 candidate through host-side AdamW/Muon materialization for the existing R6 writer.

This child makes the already-produced device generation the ActiveVerified durable candidate source while preserving the existing R6 restart contract.

## 2. Source truth after this bake

```text
AdamW ActiveDevice production scheduler                   true
AdamW real B06 device-generation stage                    true
Muon ActiveAsync device generation                        true
FullTrainableDeviceGenerationR1 production owner          true
Bounded device-to-current-R6 projection                   true
ActiveVerified duplicate host AdamW G+1 compute           retired by branch structure
ActiveVerified host Muon G+1 full scatter                 retired by branch structure
Candidate weight/m/v D2H                                  zero by candidate contract
Durable projection D2H                                    separately classified
Current weights.r6pack / adam_m.r6pack / adam_v.r6pack    preserved
PackedRuntimeStateManifestV1                              preserved
RUN_LOCAL_RAM_MV ordinary-step no-full-MV-write           preserved
active_training_state.json sole durable head              preserved
Direct G+1 -> G+2 full-model device-source reuse          false
Weight journal/keyframe redesign                          false
Release compile                                           not claimed
RTX physical PASS                                         not claimed
```

## 3. Center invariant

```text
MuonDeviceSegmentedGenerationR1 G+1
+
AdamWDeviceSegmentedGenerationR1 G+1
+
exact optimizer coverage
↓
FullTrainableDeviceGenerationR1 G+1
↓
bounded logical projection
↓
existing R6 durable contract
↓
existing P3 durable commit
```

The CPU may consume bounded durability windows, hash them and write them, but it must not rerun the optimizer to create another G+1 authority.

## 4. Durable SSOT remains unchanged

The canonical payload names remain:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

The canonical manifest remains `PackedRuntimeStateManifestV1`.

The sole current durable generation head remains:

`training_state/active_training_state.json`

No `active_generation.json`, GPU-specific durable head, alternate pack family, keyframe or journal format is introduced here.

## 5. New child module and capabilities

New module:

`crates/base_train/src/unified_atlas_mcu_full_trainable_device_durable_projection_r1.rs`

Source capabilities:

```text
FULL_TRAINABLE_DEVICE_GENERATION_PRODUCTION_OWNER_MATERIALIZED_R1 = true
BOUNDED_DEVICE_TO_R6_PACK_PROJECTION_MATERIALIZED_R1 = true
ACTIVE_OUTER_HOST_ADAMW_COMPUTE_RETIRED_R1 = true
ACTIVE_OUTER_HOST_MUON_SCATTER_RETIRED_R1 = true
CURRENT_R6_DURABLE_CONTRACT_PRESERVED_R1 = true
FULL_MODEL_DIRECT_NEXT_STEP_DEVICE_SOURCE_REUSE_MATERIALIZED_R1 = false
```

The historical parent constant reporting durable projection false is left unchanged as historical revision truth.

## 6. Full-trainable generation ownership

`ProductionMuonRuntime::assemble_full_trainable_device_generation_r1(...)` consumes the completed Muon and AdamW target owners and constructs one `FullTrainableDeviceGenerationR1`.

Required:

```text
Muon target generation = G+1
AdamW target generation = G+1
Muon publication complete = true
AdamW generation complete = true
Muon written elements = registry Muon expected elements
AdamW written elements = registry AdamW expected elements
Muon + AdamW written elements = total trainable elements
```

The full generation carries an exact `FullTrainableCoverageReceipt`. Missing, overlapping, unclassified or generation-split ownership rejects projection.

## 7. Single target owner

The full generation is constructed by moving the separate completed target owners into `FullTrainableDeviceGenerationR1`.

After assembly, durable projection reads through that owner. The design does not retain three independently mutable owners for the same G+1 physical state.

## 8. Commit and abort ownership

After a successful ActiveVerified durable commit, `rotate_full_trainable_device_generation_after_active_commit_r1(...)` consumes the full target and installs its Muon and AdamW parts as the next committed device-source generation owners.

Prior source generations are retired only when source-reader counts are zero.

An uncommitted full target is released through the existing generation retirement rules. A still-pending AdamW scheduler may not be silently discarded.

## 9. ActiveVerified outer cutover

Both production entrypoints now contain an early ActiveVerified branch:

```text
optimizer_candidate_packed(...)
→ optimizer_candidate_packed_active_device_projection_r1(...)

optimizer_candidate_ram_resident(...)
→ optimizer_candidate_ram_resident_active_device_projection_r1(...)
```

The return occurs before the legacy host candidate loops.

The dedicated ActiveVerified helpers do not call legacy `r6_adamw_candidate*` APIs and do not execute the legacy CPU Muon G+1 full-candidate scatter path.

Mirror/off compatibility paths remain available. Projection failure in ActiveVerified does not fall back to those paths.

## 10. Muon ActiveAsync device-only output

The existing Muon ActiveAsync execution path is admitted directly when the production pending-wave cutover is active and B06 mode is `ActiveVerified`.

The result can report:

`candidate_weight_device_generation_only = true`

with no host G+1 candidate vector.

The existing BP-DK/local observer may still require source-generation G Muon values in packed host scratch. That scratch is pre-update source observation, not a G+1 durable candidate authority.

## 11. AdamW execution authority

AdamW-owned spans continue through P1 `submit_adamw_active_device_pending_segment_r1(...)`.

Partitioned Muon/AdamW parameters preserve exact `canonical_parameter_index / element_start / element_count` routing.

After all parameter work:

```text
finalize AdamW pending generation
→ pending = 0
→ require complete AdamW G+1
→ require complete Muon G+1
→ assemble FullTrainableDeviceGenerationR1
→ project durable state
```

## 12. Projection plan and bounded staging

The implementation reuses `FullTrainableDeviceDurableProjectionPlanR1`.

The existing logical stream chunk is:

`R6_STREAM_CHUNK_BYTES = 16 MiB`

One projection operation may contain:

```text
logical weight window
+
AdamW M bytes for AdamW-owned spans
+
AdamW V bytes for AdamW-owned spans
```

Worst-case aggregate staging is therefore bounded by 3 x the existing 16 MiB logical window, or 48 MiB for this revision.

`FullTrainableDeviceDurableProjectionReceiptR1::seal()` requires:

```text
bounded_staging_peak_bytes <= configured_transfer_window_bytes
```

The configured window already represents the aggregate bound and is not multiplied again at receipt time.

## 13. Physical projection mechanism

This bake does not add a new WGSL optimizer/projection shader.

It uses existing WGPU buffer-copy capability:

```text
copy_buffer_to_buffer
→ existing submit_with_leases(...)
→ real SubmissionEpoch
→ poll_nonblocking_and_refresh(...)
→ submission_completed_nonblocking(...)
→ map_async(MAP_READ)
→ bounded mapped-byte consumption
→ unmap
→ release_submission_leases(...)
```

The projection creates no second Device, Queue or completion authority.

There is no ordinary `wait_for_submission_exact` in the new projection path.

The current source processes bounded projection windows without claiming multi-window physical overlap. Any overlap/performance claim requires later physical evidence.

## 14. Weight projection source

For Muon-owned logical ranges, G+1 weight bytes come from the Muon device-generation weight buffer. The existing registry `packed_index_for_logical(...)` mapping is used to map logical positions to Muon packed storage, and contiguous routed spans are checked for packed-index continuity.

For AdamW-owned logical ranges, G+1 weight bytes come from the exact covering `AdamWActiveDeviceCandidateSegmentR1` weight buffer.

No second durable routing table is introduced. `route_span(...)` and the existing canonical registry remain the routing SSOT.

## 15. Adam M/V projection source

For AdamW-owned ranges:

```text
G+1 Adam M = AdamW device candidate M buffer
G+1 Adam V = AdamW device candidate V buffer
```

No host AdamW recomputation is used to create those bytes.

For Muon-owned ranges, the current R6 schema still requires Adam M/V bytes although Muon has no active AdamW successor there. Therefore those inactive M/V bytes are copied forward exactly from the source R6/RAM authority.

Muon-owned inactive M/V is not zero-filled and Muon momentum is not substituted into Adam state.

## 16. Packed durable path

In packed mode:

```text
Muon/AdamW device G+1 weight
→ weights.r6pack

AdamW device M + Muon inactive-M copy-forward
→ adam_m.r6pack

AdamW device V + Muon inactive-V copy-forward
→ adam_v.r6pack
```

Output order remains the existing R6 logical parameter order, not GPU completion or packed Muon order.

`SequentialPackWriter`, streaming SHA256, parameter offsets and `PackedRuntimeStateManifestV1` semantics remain intact.

## 17. RAM-resident durable path

In RAM-resident Adam M/V mode:

- projected AdamW M/V ranges update the existing `RamResidentAdamMv` authority by exact bounded offsets;
- Muon-owned M/V ranges preserve the resident source values;
- projected weight bytes may feed the existing `ResidentWeightPackBuilder`;
- `RUN_LOCAL_RAM_MV` ordinary steps do not regain full Adam M/V disk rewrites;
- final durable writeback occurs only under the existing final-writeback policy.

This child does not introduce the later Adam A/B inactive-candidate-slot transaction.

## 18. Candidate D2H versus durable D2H

Existing device-candidate counters retain their P1 meaning:

```text
candidate weight D2H = 0
candidate M D2H = 0
candidate V D2H = 0
```

02 separately classifies expected filesystem egress:

```text
durable_projection_weight_d2h_bytes
durable_projection_adam_m_d2h_bytes
durable_projection_adam_v_d2h_bytes
```

Durable D2H is permitted because the current R6 filesystem writer is CPU-visible. It must not be counted as candidate D2H.

## 19. Projection receipt

`FullTrainableDeviceDurableProjectionReceiptR1` records at least:

- source/target generation;
- full-generation digest;
- coverage digest;
- projection-plan digest;
- canonical layout digest;
- projected weight/M/V byte counts;
- durable D2H bytes by class;
- inactive Muon M/V source-read bytes;
- configured aggregate transfer-window bytes;
- observed staging peak;
- projection-window count;
- projection `SubmissionEpoch` count;
- Active host AdamW/Muon candidate counters;
- unclassified transfer counters;
- completion bit and receipt digest.

The receipt is evidence, not a second durable head.

## 20. Existing R6 manifest and P3 contract preserved

The durable output remains current `PackedRuntimeStateManifestV1` with existing F32, little-endian, uncompressed pack semantics and current parameter/optimizer digests.

The current P3 durable-state requirement is not weakened.

A device generation cannot publish `active_training_state.json` merely because GPU execution completed. Required current-format durability must complete first.

## 21. Static validator

New validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_full_trainable_device_generation_bounded_durable_pack_projection_outer_host_scatter_retirement_r1_static.py`

It verifies:

- exact child revision and module export;
- materialized child capability constants;
- full-generation production ownership;
- existing durable projection plan use;
- finite bounded staging;
- existing SubmissionEpoch/map lifecycle reuse;
- Muon logical-to-packed mapping;
- AdamW device weight/M/V projection;
- inactive Muon M/V copy-forward;
- RAM-resident update path and `RUN_LOCAL_RAM_MV` preservation;
- existing R6 writer/manifest preservation;
- ActiveVerified early branch cutover;
- absence of legacy AdamW candidate calls in dedicated Active helpers;
- absence of legacy Muon G+1 full scatter in those helpers;
- candidate/Durable-D2H classification separation;
- no new durable head or journal.

## 22. Observed static regression chain

After the final staging-bound correction, the bake observed PASS for all eight static validators:

```text
02 Full Trainable Device Durable Projection R1
P1 AdamW Pending Generation Scheduler R1
B06 AdamW Multi-Segment Ledger R1
Full-Model AdamW ActiveDevice Successor parent
Local Muon Production Pending-Wave ActiveAsync Cutover R2
SubmissionEpoch ActiveAsync Completion / P5
Active Transactional Commit and Restart / P3
Unified Atlas MCU Control Plane R1
```

The new validator also passed Python compilation. A delimiter-balance sanity scan passed for all modified/new Rust modules.

These are static/source gates only.

## 23. Exact implementation diff

Compared with the P1 full-source parent, this bake changes exactly six implementation/validator files:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
crates/base_train/src/unified_atlas_mcu_full_trainable_device_durable_projection_r1.rs
tools/validate_ash_basetrain_unified_atlas_mcu_full_trainable_device_generation_bounded_durable_pack_projection_outer_host_scatter_retirement_r1_static.py
```

## 24. Compile and physical boundary

This child changes Rust ownership, outer optimizer control flow, Muon ActiveAsync output semantics, WGPU readback flow, RAM-resident projection and commit-time generation rotation.

A real release compile is mandatory.

The assistant bake environment exposes no `cargo`, `rustc` or `rustfmt`, therefore release compile is not claimed.

The bake also does not claim RTX execution, live D2H/staging measurements, bit-parity against projected packs, fresh-process restart, next-step parity or full direct G+1 -> G+2 device-source reuse.

## 25. Required physical qualification

Full physical PASS requires at minimum:

```text
full-generation coverage complete
missing/overlap/unclassified/duplicate elements = 0
Active host AdamW candidate compute count = 0
Active host Muon G+1 scatter count = 0
full host candidate Vec count = 0
candidate weight/m/v D2H = 0
unclassified projection bytes = 0
staging peak <= configured aggregate bound
weight projection bit mismatch = 0
Adam M projection bit mismatch = 0
Adam V projection bit mismatch = 0
inactive Muon M/V copy-forward mismatch = 0
canonical R6 pack/manifest validation PASS
fresh-process restart PASS
```

Physical projection overlap or speedup is not claimed unless a later campaign observes more than one real projection window outstanding and records timing evidence.

## 26. Packaging policy

Delivered implementation ZIP excludes:

- this specification and all Markdown;
- `specs/`;
- bake manifests;
- generated manifests/receipts/evidence;
- qualification/runtime artifacts;
- runtime JSON/JSONL;
- runtime pack/bin outputs;
- logs;
- `target` and `target_*`;
- `.git`;
- Python bytecode/cache;
- source backups.

The overlay ZIP contains only the six changed implementation/validator files listed above.

## 27. GitHub publication policy

GitHub publication for this bake is specification-only. Implementation source remains in the delivered baked ZIP.

## 28. Exact next child

After release compile and physical current-format restart qualification, the next durable-architecture child is:

`ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1`

That revision may bind an immutable durability descriptor/seal to the existing `active_training_state.json` head without creating a competing head.

The later sequence remains:

```text
RAM-resident Adam inactive candidate slot
weight keyframe + bit-exact successor journal
dual-write fresh-process replay
ordinary full-pack retirement
```

## 29. Center sentence

**02는 저장 포맷을 바꾸는 패치가 아니다. GPU에서 이미 확정된 G+1을 디스크에 쓰기 위해 CPU에서 다시 G+1을 계산하고 조립하는 중복 권위를 끝내는 패치다. Muon과 AdamW의 실제 device successor를 하나의 `FullTrainableDeviceGenerationR1`로 묶고, 기존 16 MiB R6 logical stream을 기준으로 최대 48 MiB aggregate staging 안에서 현재 R6 pack contract로 투영한다. AdamW M/V는 device successor에서 오고, Muon-owned inactive Adam M/V는 현재 R6 schema를 보존하기 위해 source authority에서 exact copy-forward된다. ActiveVerified에서는 host AdamW 재계산과 host Muon G+1 scatter가 candidate authority가 아니며, 실패 시 host fallback으로 도망가지 않는다. `PackedRuntimeStateManifestV1`, P3, `active_training_state.json`은 그대로 restart authority로 남는다.**