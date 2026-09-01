# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-ACTIVE-DEVICE-PENDING-GENERATION-PRODUCTION-SCHEDULER-AND-MULTI-SEGMENT-COLLECT-CLOSURE-R1

## AdamW ActiveDevice Pending Generation / Bounded Multi-Segment Submission / Nonblocking Later Collect / Partitioned Muon-AdamW Range Preservation / Real B06 Device-Generation Stage Callsite / Durable Host Projection Still Pending

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-ACTIVE-DEVICE-PENDING-GENERATION-PRODUCTION-SCHEDULER-AND-MULTI-SEGMENT-COLLECT-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-MULTI-SEGMENT-DEVICE-GENERATION-B06-BACKING-LEDGER-AND-PRODUCTION-STAGING-CLOSURE-R1`

Reserved full physical PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ADAMW_ACTIVE_DEVICE_PENDING_GENERATION_PRODUCTION_SCHEDULER_AND_MULTI_SEGMENT_COLLECT_CLOSURE_R1`

Observed source/static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ADAMW_ACTIVE_DEVICE_PENDING_GENERATION_PRODUCTION_SCHEDULER_MULTI_SEGMENT_COLLECT_R1_STATIC`

## 1. Purpose

The parent materially provides the ActiveDevice AdamW producer, real SubmissionEpoch-backed pending handle, GPU-resident candidate weight/m/v, multi-segment B06 generation ledger, generation ticket builder and `ProductionMuonRuntime::stage_b06_adamw_device_candidate_generation_r1(...)` stage surface.

The exact remaining execution blocker was the outer production scheduler. `optimizer_candidate_packed` and `optimizer_candidate_ram_resident` still produced AdamW synchronously through host-output candidate operations and never retained a bounded set of real `PendingAdamWActiveDeviceCandidateR1` handles across production segments.

This child materially adds that missing scheduler and routes the real production optimizer into the B06 device-generation stage.

## 2. Source truth after this bake

```text
AdamW ActiveDevice backend                                true
AdamW real SubmissionEpoch pending handle                 true
AdamW bounded production pending-generation scheduler     true
AdamW nonblocking later collect                           true
AdamW partitioned multi-fragment generation assembly      true
AdamW multi-segment B06 backing ledger                    true
Real B06 device-generation stage callsite                 true
ActiveVerified outer B06 host-stage fallback              false
Candidate weight/m/v D2H in device ticket                 zero by contract
Ordinary exact per-segment wait in device scheduler       zero by structure
Legacy/current durable host candidate computation         still present
Durable device-to-pack projection                         false
Outer host scatter retirement                             false
Full trainable device-generation durable cutover          false
Release compile in assistant bake environment             not available
RTX physical PASS                                         not claimed
```

## 3. New production scheduler owner

New module:

`crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs`

New owner:

`AdamWActiveDevicePendingGenerationSchedulerR1`

One scheduler owns exactly one transition:

```text
source generation G
→ target generation G+1
```

It owns:

- exact source/target generation identity;
- expected AdamW parameter cardinality;
- expected AdamW element cardinality;
- one `AdamWActiveDeviceCandidateProducerR1`;
- bounded pending map;
- complete target `AdamWDeviceSegmentedGenerationR1` assembly;
- duplicate/overlap admission history;
- submission/collect counters.

## 4. Bounded pending topology

Default R1 capacity:

`ADAMW_ACTIVE_DEVICE_PENDING_GENERATION_DEFAULT_MAX_IN_FLIGHT_R1 = 4`

The scheduler rejects configurations below two in-flight segments.

The production shape is:

```text
submit segment A → Pending A
submit segment B → Pending B
submit segment C → Pending C
submit segment D → Pending D
capacity reached
→ nonblocking poll/collect ready entries
→ submit later segments
```

No unbounded pending queue is introduced.

## 5. Real physical submission identity

Every pending candidate originates from:

`AdamWActiveDeviceCandidateProducerR1::submit(...)`

which uses the existing `a01_submit_with_leases(...)` path and returns a real `SubmissionEpoch`.

The scheduler does not fabricate a private completion ordinal and does not use host loop position as physical completion authority.

## 6. No ordinary exact wait

The scheduler uses:

`try_collect(...)`

through nonblocking completion refresh.

`wait_for_submission_exact` is absent from the new scheduler and from the ActiveDevice AdamW backend.

Capacity pressure and terminal collection yield the host thread when no completion progress is observed. Both loops have finite stall guards and fail closed rather than silently converting the hot path into an exact per-segment wait.

## 7. Post-submit ownership invariant

After a real submit succeeds, the pending object is inserted into the scheduler-owned pending map before post-submit identity assertions are evaluated.

Therefore a post-submit validation failure does not discard the physical pending owner.

Likewise `finalize_and_stage_b06_adamw_pending_generation_r1(...)` keeps the scheduler inside `ProductionMuonRuntime` while `finish_collection(...)` is fallible. The runtime removes the scheduler only after the pending map has fully drained and generation completeness has been proven.

This closes the prior ownership hole where a fallible collect could otherwise cause a local scheduler value to drop while real GPU work still existed.

## 8. Duplicate admission is no-mutation

Canonical key:

`AdamWDeviceCandidateSegmentKeyR1`

with:

```text
canonical_parameter_index
element_start
element_count
```

The scheduler checks the persistent submitted-key set and overlap geometry before physical submission.

An exact duplicate is rejected with:

`E_MCU_ADAMW_PENDING_R1_DUPLICATE_SEGMENT_ADMISSION`

without replacing the original pending owner.

## 9. Partitioned Muon/AdamW routing discovered in production source

Source inspection showed that current production routing includes `PARTITIONED_MUON_ADAMW` parameters.

Therefore the parent assumption that one AdamW physical segment equals one whole parameter is not sufficient for the real production scheduler.

A single parameter may contain:

```text
Muon-owned interior range
+
AdamW-owned edge/residual ranges
```

The device AdamW generation must preserve those exact fragments.

## 10. AdamW segmented generation widening

`AdamWDeviceSegmentedGenerationR1` now stores:

`BTreeMap<AdamWDeviceCandidateSegmentKeyR1, AdamWActiveDeviceCandidateSegmentR1>`

instead of a one-entry-per-parameter map.

This permits multiple non-overlapping physical AdamW fragments under one canonical parameter while preserving deterministic ordering.

The generation separately exposes:

- published segment count;
- unique published parameter count;
- published element count.

Generation completeness is:

```text
unique AdamW parameters == expected AdamW parameter count
AND
published AdamW elements == expected AdamW element count
```

## 11. Fragment overlap rejection

For every canonical parameter, each new segment is checked against already published ranges.

Overlapping fragments fail with:

`E_MCU_FULL_MODEL_R1_ADAMW_SEGMENT_OVERLAP`

Exact duplicate fragments fail before mutation.

## 12. B06 ledger parameter-count / segment-count separation

`AdamWDeviceCandidateGenerationLedgerR1` now carries both:

- `expected_parameter_count`;
- `expected_segment_count`.

The ledger validates:

```text
physical segment count == expected_segment_count
unique canonical parameter count == expected_parameter_count
written elements == expected_element_count
```

This prevents a partitioned parameter from being incorrectly treated as multiple parameters while still preserving every physical backing triplet and SubmissionEpoch.

## 13. Exact route admission before submit

`ProductionMuonRuntime::submit_adamw_active_device_pending_segment_r1(...)` validates every requested range against the canonical first-candidate routing registry.

It requires:

- canonical parameter index identity;
- AdamW ownership for the parameter;
- segment in parameter bounds;
- every point crossed by the submitted segment to be non-Muon according to `route_span(...)`.

A Muon-owned range submitted to AdamW fails with:

`E_MCU_ADAMW_PENDING_R1_MUON_OWNED_RANGE_SUBMITTED`.

## 14. Packed production path adoption

`optimizer_candidate_packed(...)` now receives the production Muon runtime when available and constructs the existing source-record-ordinal to canonical-parameter-index bridge.

In `ActiveVerified`, every normal packed chunk is intersected with the canonical Muon/AdamW routing spans.

Only AdamW-owned subranges are sent to the pending scheduler.

The existing host candidate operation remains temporarily present because the existing R6 pack writer is still the durable projection authority in this revision.

## 15. RAM-resident production path adoption

`optimizer_candidate_ram_resident(...)` adopts the scheduler in both AdamW cases:

1. partitioned Muon parameters: exact AdamW edge/residual fragments are submitted;
2. explicit AdamW parameters: existing RAM-resident segment work items are submitted directly.

The scheduler receives the exact source weight/m/v slice and the existing GPU gradient lease when present.

Zero-gradient gaps use the existing ActiveDevice zero-gradient contract.

## 16. Transitional source upload truth

The current production adoption seeds each AdamW source segment from the exact current host/RAM source window through `AdamWDeviceSourceSegmentR1::seed_from_host(...)` before ActiveDevice execution.

This is not a host candidate → GPU ticket bridge. The uploaded data is source generation G, not a host-computed G+1 candidate.

However, produced G+1 AdamW buffers are not yet reused as the direct G+1 → G+2 source across production steps in this child. That physical reuse remains unclaimed.

## 17. Candidate transfer contract

The ActiveDevice candidate generation ticket remains:

```text
candidate weight D2H = 0
candidate M D2H      = 0
candidate V D2H      = 0
host candidate Vec materialization in device ticket = 0
ordinary exact wait  = 0
```

Only compact status evidence is read back by the device-candidate backend.

These counters describe the device candidate authority only. They do not claim that the legacy durable R6 pack writer has already been retired.

## 18. Production generation finalization

At the end of each optimizer candidate pass in `ActiveVerified`:

```text
finish nonblocking pending collection
→ require complete AdamW device generation
→ build B06 multi-segment generation ticket
→ validate exact source/target TrainableGenerationId
→ bind current B06 ownership digest
→ bind current canonical layout digest
→ bind canonical row-map digest
→ bind full-trainable coverage digest
→ retain device generation buffers in ProductionMuonRuntime
→ stage_b06_adamw_device_candidate_generation_r1(ticket)
```

The actual production callsite therefore reaches the existing B06 device-generation API.

## 19. Device generation lifetime

`ProductionMuonExecutionRuntime` now owns:

- pending AdamW scheduler;
- committed/source AdamW device generation;
- target AdamW device generation;
- last scheduler receipt.

The target generation remains alive through B06 commit so the ticket cannot outlive its physical candidate buffers.

After active commit, the target generation is rotated into the source-generation owner.

A prior source generation may be released only when its active source-reader count is zero.

## 20. ActiveVerified B06 host-stage retirement boundary

The outer post-optimizer B06 stage now branches explicitly on `HybridDeviceCommitRuntimeMode`.

```text
Off
→ no B06 AdamW stage

MirrorVerified
→ existing stage_b06_adamw_host_candidate(...)

ActiveVerified
→ require successful pending-generation receipt
→ do not call host B06 AdamW stage
```

There is no ActiveVerified fallback from a failed device generation to host B06 staging.

## 21. Durable host computation remains intentionally separate

This child does not remove the existing host-output AdamW computation used by current pack/RAM durable state construction.

That host work is no longer the B06 ActiveVerified execution ticket, but it still exists as the current durable projection path.

Therefore this child does not claim:

```text
outer host scatter retired
per-step host durable candidate materialization = 0
bounded device-to-pack projection complete
```

Those belong to the exact next child.

## 22. Abort behavior

If generation abort reaches B06 while an AdamW scheduler still owns submitted pending work, abort refuses to discard the scheduler and reports:

`E_MCU_ADAMW_PENDING_R1_TERMINAL_DRAIN_REQUIRED`

A fully collected, uncommitted AdamW target generation may be dropped during abort because its physical submissions have already completed and source leases have been released.

The committed/source device generation is not silently discarded by target-generation abort cleanup.

## 23. Scheduler receipt

`AdamWPendingGenerationSchedulerReceiptR1` records at least:

- source and target generation;
- expected AdamW parameter/elements;
- submitted and collected segment count;
- real SubmissionEpoch count;
- peak pending count;
- configured in-flight bound;
- collect errors;
- duplicate rejects;
- post-submit orphan count field;
- ordinary exact wait count;
- device candidate weight/m/v D2H bytes;
- device candidate host-Vec materialization count;
- final pending count;
- final active source-reader count;
- final published parameter/segment/element count;
- generation-complete flag;
- deterministic receipt digest.

## 24. Static validator

New validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_adamw_active_device_pending_generation_production_scheduler_multi_segment_collect_r1_static.py`

It checks:

- exact child revision and module export;
- bounded in-flight scheduler;
- real pending owner map;
- real ActiveDevice producer submit;
- nonblocking later collect;
- no exact wait in scheduler/backend;
- post-submit owner insertion before fallible identity validation;
- scheduler retention across fallible final collect;
- terminal-drain abort guard;
- fragment-keyed AdamW generation;
- fragment overlap rejection;
- separate B06 parameter and segment counts;
- runtime route ownership guard;
- runtime generation-ticket builder;
- actual runtime B06 generation-stage call;
- packed and RAM production submit callsites;
- packed and RAM finalization callsites;
- ActiveVerified host B06 bypass;
- MirrorVerified host stage preservation;
- durable projection still false.

## 25. Observed regression static gates

The bake environment observed PASS for:

```text
new AdamW pending-generation scheduler R1
parent AdamW multi-segment B06 ledger R1
full-model AdamW ActiveDevice successor parent
Local Muon production pending-wave cutover R2
Local Muon device segmented source direct submit R1
SubmissionEpoch active-async completion R1
active transactional commit/restart R1
Unified Atlas MCU control plane R1
```

These are static/source validators only.

## 26. Compile boundary

A release compile remains mandatory because this child changes:

- cross-module Rust ownership;
- `AdamWDeviceCandidateGenerationLedgerR1` structure;
- AdamW generation fragment ownership;
- outer optimizer function signature/control flow;
- `ProductionMuonExecutionRuntime` state;
- production B06 stage callsite.

The assistant bake environment did not expose `cargo`, `rustc` or `rustfmt`.

Therefore:

```text
release compile = not claimed
```

## 27. Physical PASS withheld

This source bake does not claim:

- RTX 3080 execution;
- peak pending count physically observed >= 2;
- physical completion order different from canonical order;
- numerical parity between transitional host durable AdamW output and GPU ActiveDevice successor;
- produced G+1 AdamW device generation reused directly as G+1 → G+2 source;
- physical source-reader/orphan counters from a live campaign;
- full durable pack projection from device buffers;
- full-model outer host-scatter retirement;
- parent P5 full production PASS.

## 28. Packaging policy

The implementation source ZIP excludes:

- `specs/` and Markdown;
- bake manifests;
- generated manifests/receipts/evidence;
- qualification artifacts;
- runtime JSON/JSONL;
- runtime pack/bin payloads;
- logs;
- `target*` build trees;
- `.git`;
- Python bytecode caches;
- source backup files.

Rust/WGSL/TypeScript/Python implementation and validator source remain included.

## 29. GitHub publication policy

GitHub publication for this bake is specification-only.

Implementation source remains in the delivered baked ZIP and is not committed to the ASH GitHub repository by this revision.

## 30. Exact next child

The next boundary remains:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`

That child must eliminate the duplicate host durable AdamW candidate path by projecting the already-produced device generation into the existing R6 pack/manifest contract through bounded staging, while preserving exact restart semantics.

## 31. Center sentence

**이번 child에서 바뀐 것은 AdamW 수식이 아니라 세대의 소유권이다. production optimizer는 이제 AdamW-owned range를 실제 GPU submission으로 여러 개 outstanding 상태에 두고, real SubmissionEpoch가 끝난 segment만 later-collect하여 canonical G→G+1 device generation으로 조립한다. PARTITIONED_MUON_ADAMW 파라미터는 하나의 whole-parameter ticket으로 뭉개지 않고 실제 edge/residual fragment 그대로 ledger에 들어간다. 완성된 generation만 B06 ActiveVerified ticket이 되며 host B06 fallback은 없다. 다만 기존 R6 durable pack writer는 아직 host candidate를 필요로 하므로 그 계산은 이번 revision에서 제거하지 않는다. 다음 child가 바로 그 마지막 host scatter를 bounded device-to-pack projection으로 걷어내는 단계다.**