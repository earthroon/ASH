# ASH-BASETRAIN-BT-WGSL-DEVICE-LIMIT-AWARE-MICRO-ATLAS-VOCAB-ROW-PAGING-06C-R27-R1J-R6A-R2

## Revision / parent authority

- Patch: `ASH-BASETRAIN-BT-WGSL-DEVICE-LIMIT-AWARE-MICRO-ATLAS-VOCAB-ROW-PAGING-06C-R27-R1J-R6A-R2`
- Build: `bt-wgsl-device-limit-aware-micro-atlas-vocab-row-paging-06c-r27-r1j-r6a-r2`
- Code parent: Pass106 / R6A-R1 CF1.
- Physical parent: physically passed R5 generation3 / optimizer-step3 / cursor-next3.
- R6/R6A/R6A-R1 physical promotion before this patch: not established.
- Observed parent failure: `aw01.atlas.slot.0` requested `416317440` bytes while physical WGPU max buffer was `268435456` bytes.
- R6A-R2 is therefore a pre-promotion correction, not a post-R6 optimization claim.

## 1. Whole-tensor Atlas slot retirement

Logical tensor size and logical group size no longer determine physical Atlas buffer capacity. Production packed-runtime planning uses a fixed physical transport page of exactly `16,777,216` bytes (16 MiB). A logical tensor may map to multiple physical segments. A logical group may unfold into multiple physical pages.

The historical `slot_segment_index == 0` whole-tensor-only assumption is retired for R6A-R2 packed-runtime plans. `logical_element_start`, `logical_element_count`, and nonzero segment indices are active authority.

## 2. Device-limit preflight before storage mutation

After the internal native WGPU bootstrap and before packed migration/output mutation, R6A-R2 reads the physical device limits and requires:

- `16 MiB <= max_buffer_size`
- `16 MiB <= max_storage_buffer_binding_size`

There is no silent page-size shrink. Failure occurs before R5-to-packed migration.

R6A-R2-owned Atlas payload buffers are capped at 16 MiB. Oversize payload-buffer creation is rejected before WGPU validation is used as the failure mechanism.

## 3. Triple micro-atlas ring

R6A-R2 page transport uses three rotating 16 MiB physical slots. The R6A-R2 LM-head page ring and the micro-embedding backend both use three-slot wave rotation. Slots are selected deterministically by wave ordinal modulo three. Queue submission order preserves earlier consumers before a slot is reused.

The legacy `aw01.atlas.slot.*` route admission also receives the fixed 16 MiB plan capacity; micro-segmented admission seeds only the first physical slice rather than uploading the entire model merely to prove route admission.

## 4. Multi-segment tensor plan

Packed-runtime production plan materialization derives deterministic segments from tensor geometry. Rank-2 tensors are segmented on complete row boundaries whenever possible. No row is split across physical pages.

For every tensor, segment coverage is exact and continuous:

- first logical element start = 0
- next segment start = previous end
- final segment end = logical tensor element count
- segment gap count = 0
- segment overlap count = 0
- every segment byte length <= 16 MiB

The historical non-packed R2A plan builder remains available for its parent contract. The new micro-segment builder is selected for R6A packed runtime only.

## 5. Packed range segment digest authority

`PackedParameterOffsetEntryV1` retains whole-parameter identity and adds write-time weight segment digests. Segment records bind segment index, logical range, row range, absolute packed offset, byte length, and SHA256.

Segment digests are generated from the exact bytes while R5 generation3 is migrated or while the new candidate weight pack is written. R6A-R2 does not write a page and reopen it solely to hash it.

Runtime Atlas reads verify the exact segment digest. A physical page does not require reading the whole logical tensor to establish identity.

## 6. Vocab geometry

Current model authority:

- vocab size = 48,259
- hidden size = 2,048
- dtype = F32
- row bytes = `2048 * 4 = 8192`
- page bytes = 16 MiB
- rows/page = `16,777,216 / 8,192 = 2,048`
- page count = 24
- pages 0..22 = 2,048 rows each
- page 23 = 1,155 rows

Exact coverage: `23 * 2048 + 1155 = 48259`.

The final physical page reads/uploads only its real 1,155 rows. GPU slot capacity remains 16 MiB but source bytes are not padded on disk.

## 7. Sparse embedding page admission

The eight independent `batch_size=1` accumulation lanes preserve their original sequence semantics. Input token IDs from all eight lanes are converted to vocab-page indices, sorted and deduplicated.

Only unique required embedding pages are read from `weights.r6pack`. One physical embedding page is dispatched once and resolves all matching token positions from all eight lanes before the page is recycled. There is no random per-token HDD row fetch and no page reread merely because a token appears in another microbatch.

The existing micro-embedding compute path now owns three 16 MiB atlas slots rather than one repeatedly fence-waited slot.

## 8. LM-head forward vocab paging

The untied LM head is not materialized as one ~377 MiB Atlas payload. Forward loss traverses the exact 24 physical vocab pages.

For each page:

1. read exact packed range once;
2. upload to one 16 MiB ring slot;
3. fan the resident page across all eight independent lanes;
4. update each lane's streaming loss accumulator;
5. recycle the physical slot through deterministic ring rotation.

`R23LossAccumulator` retains stable streaming logsumexp semantics. Full logits are never materialized. The target logit is captured in the same page pass when its vocab ID belongs to that page, so no second target-row read is introduced.

## 9. LM-head backward vocab paging

Backward also traverses exactly 24 physical LM-head pages per optimizer transaction. One page is read/uploaded once, then lanes 0..7 execute page-local logit VJP, hidden-gradient contribution, and LM-head weight-gradient contribution against that resident page.

The page-local LM-head gradients feed the shared R6 FP32 accumulation authority. Full-vocab dlogits and full LM-head GPU residency remain closed.

Thus accumulation8 does not mean `24 pages * 8 lanes` physical weight reads. The page is the outer residency unit and the eight lanes are the inner fanout.

## 10. Decoder tensor micro-segmentation

Decoder tensors larger than 16 MiB are represented as multiple exact packed transport segments. Atlas planning and packed-range reads never create a decoder Atlas payload slot larger than the page budget.

Current R6A-R2 boundary: the existing proven decoder-block compute builder is retained. Transport segments for one decoder tensor are decoded in bounded pieces and concatenated on the host before the existing per-block compute tensor is constructed. This patch therefore proves **micro-segmented disk/Atlas transport and no oversize Atlas slot**, not permanent segment-only decoder compute residency. Decoder compute buffers remain subject to the physical device max-buffer limit.

This explicit boundary avoids silently claiming a shader ABI rewrite that R6A-R2 does not perform.

## 11. No full vocab residency

Production R6A-R2 requires:

- full embedding Atlas residency = 0
- full LM-head Atlas residency = 0
- full vocab weight buffer materialization = 0
- full logits materialization = 0
- runtime arena creation = 0

The prior `416,317,440`-byte mixed Atlas slot topology is unreachable in the R6A-R2 packed-runtime route.

## 12. R6A-R1 accumulation semantics preserved

R6A-R2 does not convert the eight lanes into `batch_size=8`. The existing batch-one G204D gate remains intact.

Unchanged authority:

- eight logical batch-one lanes per optimizer transaction
- native WGPU bootstrap before storage mutation
- same Burn/native device and queue lineage
- layer-wave outer loop and lane fanout inner loop
- shared active-loss-slot-weighted FP32 gradient accumulator
- one AdamW update per eight lanes
- cursor +8 per optimizer commit
- scheduler +1 per optimizer commit
- generation +1 / optimizer step +1 per commit
- packed ping-pong source/candidate ownership
- no partial-accumulator adoption
- no epoch/shuffle adoption
- checkpoint export closed

## 13. Disk I/O authority

R6A-R2 distinguishes work reads from migration, fresh-resume integrity, optimizer-state, and digest-only I/O.

Per production step, physical receipt records at least:

- sparse embedding unique page count/read count/read bytes
- LM-head forward page count
- LM-head backward page count
- LM-head sequential logical read bytes
- total packed-weight work-read bytes from the checkpoint-range read session
- source open/read/seek observations
- microbatch-induced page-refetch bytes

`microbatch_induced_page_refetch_bytes` must be zero. R6A's post-write digest reread remains zero.

R6A-R2 does not claim that HDD active time can never reach 100%; large sequential model/optimizer work and crash-safe packed-state writes remain legitimate disk traffic. It retires whole-vocab and per-microbatch read amplification.

## 14. Runtime receipt and structural authority

Runtime R6A-R2 receipt Atlas is exactly 80 waves. The runtime receipt binds device limits, page/ring geometry, segmentation, vocab geometry, sparse embedding page counts, 24-page LM forward/backward coverage, disk read accounting, zero-refetch seals, final generation/optimizer/cursor, and terminal HOLD authority.

Structural contract uses exactly 96 gates:

`--require-bt-wgsl-r27r1j-r6a-r2-contract-001=true` through `096=true`.

Structural receipt Atlas is exactly 80 semantic waves. R6A-R2 currently exposes 29 unique semantic negative canaries. Numeric filler canaries are prohibited.

Static validator:

`tools/validate_r27r1j_r6a_r2_device_limit_micro_atlas_vocab_row_paging_static.py`.

Parent validators are updated only for terminal-child succession and the explicitly adopted multi-segment transport contract.

## 15. N=2 physical harness

The first physical R6A-R2 run still starts from the physically passed R5 state:

- generation3
- optimizer step3
- cursor next3

Step4 consumes ordinals 3..10 and should commit generation4 / optimizer4 / cursor-next11.

Step5 consumes ordinals 11..18 and should commit generation5 / optimizer5 / cursor-next19.

For each optimizer step the current model must report:

- vocab row bytes = 8192
- vocab rows/page = 2048
- vocab pages = 24
- final vocab page rows = 1155
- LM forward page count = 24
- LM backward page count = 24
- embedding page read count = embedding unique page count
- no full embedding/LM-head residency
- no microbatch-induced page refetch
- no Atlas payload buffer above 16 MiB

## 16. Required physical PASS chain

1. `PASS_ASH_BASETRAIN_BT_WGSL_PRODUCTION_MULTI_STEP_LOOP_ACCUMULATION8_WARMUP_SCHEDULER_06C_R27_R1J_R6`
2. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_STATE_DISK_PRESSURE_RETIREMENT_06C_R27_R1J_R6A`
3. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_NATIVE_BOOTSTRAP_AND_ACCUMULATION_WAVE_RESIDENCY_06C_R27_R1J_R6A_R1`
4. `PASS_ASH_BASETRAIN_BT_WGSL_DEVICE_LIMIT_AWARE_MICRO_ATLAS_VOCAB_ROW_PAGING_06C_R27_R1J_R6A_R2`

Intended terminal HOLD:

`HOLD_ASH_BASETRAIN_R1J_R6A_R2_MICRO_ATLAS_VOCAB_PAGED_PRODUCTION_MULTISTEP_COMMITTED_LONG_HORIZON_TRAINING_PROMOTION_NOT_YET_ADMITTED`

An exit code 1 caused only after the complete PASS chain by this exact HOLD is intended.

## 17. PASS meaning

R6A-R2 PASS establishes that the packed-runtime training path no longer sizes GPU Atlas slots from whole logical tensors/groups. The physical transport unit is a device-admitted 16 MiB page. Large packed tensors carry exact multi-segment logical ranges and write-time segment digests. Embedding reads only unique required vocab pages. LM-head forward and backward each cover the 48,259-row vocabulary with 24 physical pages, with one page shared by all eight lanes. Full embedding/LM-head Atlas residency and full logits materialization remain absent.

## 18. Not proven

R6A-R2 does not establish:

- disk utilization guaranteed below 100%
- zero disk traffic
- full-model GPU or RAM residency
- permanent optimizer-state GPU residency
- decoder segment-only compute kernels after transport
- distributed training
- cross-device determinism
- epoch/shuffle authority
- long-horizon production promotion
- checkpoint retention policy

## SSOT seal

```text
DEVICE LIMIT FIRST
    -> 16 MiB PHYSICAL PAGE
    -> MULTI-SEGMENT PACKED RANGE
    -> THREE ROTATING MICRO-ATLAS SLOTS
    -> ONE PAGE RESIDENT
    -> EIGHT BATCH_SIZE=1 LANES FAN OUT
    -> RECYCLE

EMBEDDING:
8 lanes -> token pages -> sort/unique -> required pages only

LM HEAD:
48259 rows -> 2048 rows/page -> 24 pages
page -> eight lanes -> streaming logsumexp/target capture -> recycle
backward page -> eight lanes -> shared FP32 gradient accumulator -> recycle

NO 377 MiB VOCAB ATLAS SLOT
NO 397 MiB MIXED ATLAS SLOT
NO PER-MICROBATCH PAGE REFETCH
NO RUNTIME ARENA
NO POST-WRITE PAGE REHASH
```
