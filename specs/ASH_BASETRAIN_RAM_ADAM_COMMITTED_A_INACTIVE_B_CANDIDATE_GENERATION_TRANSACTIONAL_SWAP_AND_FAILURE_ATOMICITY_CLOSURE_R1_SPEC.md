# ASH-BASETRAIN-RAM-ADAM-COMMITTED-A-INACTIVE-B-CANDIDATE-GENERATION-TRANSACTIONAL-SWAP-AND-FAILURE-ATOMICITY-CLOSURE-R1

## Persistent Dual Physical RAM Adam M/V Slots / Logical Committed-A + Inactive-B Roles / Eve G→G+1 Identity / 02 + Legacy Direct-to-B / Validation-Before-Swap / RAM36 + Exact Inventory Admission / Failure-Atomic Source Preservation

## 0. Revision identity

Revision:
`ASH-BASETRAIN-RAM-ADAM-COMMITTED-A-INACTIVE-B-CANDIDATE-GENERATION-TRANSACTIONAL-SWAP-AND-FAILURE-ATOMICITY-CLOSURE-R1`

Parent:
`ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1`

Semantic parents:
- `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`
- `ASH-ADAMS-RIB-EVE-COMMON-ADAM-STATE-GEOMETRY-SUCCESSOR-ABI-AND-PROJECTION-PRIMITIVE-MATERIALIZATION-R1`
- `ASH-ADAMS-RIB-EVE-CANONICAL-ADAM-MATHEMATICAL-UPDATE-PRIMITIVE-AND-BACKEND-PARITY-MATERIALIZATION-R2`

Static PASS:
`PASS_ASH_BASETRAIN_RAM_ADAM_COMMITTED_A_INACTIVE_B_CANDIDATE_GENERATION_TRANSACTIONAL_SWAP_FAILURE_ATOMICITY_CLOSURE_R1_STATIC`

Physical HOLD:
`HOLD_ASH_BASETRAIN_RAM_ADAM_TRANSACTIONAL_AB_PHYSICAL_RAM36_AND_FAILURE_CAMPAIGN_PENDING_R1`

Full physical PASS is not claimed by this source bake.

## 1. Purpose

Before this child, `RamResidentAdamMv` owned one committed `m: Vec<f32>` and `v: Vec<f32>` pair, and production candidate construction could update that same resident state while G+1 was still incomplete. A failure mid-step could therefore leave one live RAM authority containing a mixture of G and G+1.

R1 materializes two persistent physical M/V slots. All source reads remain on logical Committed-A. Candidate G+1 is fully written and sealed in logical Inactive-B. Only after the outer target generation wins does a validated one-shot permit exchange the logical roles.

## 2. Current source truth after bake

```text
persistent second full M/V physical slot              true
logical Committed-A / Inactive-B roles                true
Eve G→G+1 candidate identity                          true
canonical sequential B writes                         true
streaming candidate M/V SHA256                        true
candidate completeness seal                           true
02 ActiveVerified direct-to-B                         true
legacy RAM candidate direct-to-B                      true
production direct committed update_slices call        false
full A→B clone per optimizer step                     false
swap-time full M/V allocation                         false
swap-time full M/V payload copy                       false
post-filesystem late-failure forward recovery         true
RAM36 Slot1 reservation                               true structurally
exact RAM inventory Slot1 registration                true structurally
new RAM A/B durable head                              false
V4 descriptor/head schema changed by this child       false
physical RAM36 PASS                                   false
physical failure-injection PASS                       false
release compile                                       not claimed
```

## 3. Existing owner remains the SSOT

`RamResidentAdamMv` remains the production RAM Adam owner. It now contains committed `m/v`, candidate `candidate_m/candidate_v`, and transactional role/generation metadata. No second independently authoritative RAM Adam manager is introduced.

New runtime identities include:

```rust
RamAdamMvPhysicalSlotIdR1::{Slot0, Slot1}
RamAdamMvCandidateStateR1::{Inactive, Filling, Complete}
RamAdamMvCandidateSealR1
RamAdamMvSwapPermitR1
RamAdamMvTransactionalReceiptR1
```

## 4. A/B are logical roles

Initial admission:

```text
Slot0 = Committed-A = source G
Slot1 = Inactive-B
```

After successful promotion:

```text
Slot1 = Committed-A = target G+1
Slot0 = Inactive-B = old G bytes until reused
```

The next target reuses the old committed physical slot. R1 does not create a third full M/V slot.

## 5. Actual transactional admission rule

No new user-facing config flag was added. A/B is enabled only when all existing authorities are active:

```text
admit_ram_resident_adam_mv
&& admit_ram36_process_budget_authority
&& ram36_process_cap_enforced
```

Configurations that do not satisfy this conjunction do not receive the transactional R1 claim. There is no silent claim that old in-place mutation became failure-atomic.

## 6. Slot1 materialization and RAM36

`enable_transactional_ab_r1()` allocates one candidate M Vec and one candidate V Vec whose byte cardinalities must exactly equal the manifest Adam M/V pack geometry.

The initial Slot1 allocation is zero-initialized by the current implementation. Correctness does not rely on zeroing during subsequent reuse. After swaps, the old committed slot is reused without a whole-slot source clone.

New RAM36 owners:

```text
HostRamOwner::AdamMCandidateResident
HostRamOwner::AdamVCandidateResident
```

Exact bytes are reserved before physical Slot1 materialization.

## 7. Exact inventory alignment

The exact RAM inventory now adds:

```text
BaseTrainRamCategory::AdamMCandidateResident
BaseTrainRamCategory::AdamVCandidateResident
```

through `register_adam_transactional_candidate_manifest_r1(...)`.

RAM36 and exact inventory therefore observe the same two physical Adam M/V slot pairs.

## 8. Eve generation identity

`begin_candidate_r1()` uses Eve R1 `AdamGenerationOrdinalR1` and `AdamGenerationIdentityR1`.

It requires the currently committed RAM generation to equal the outer source model/optimizer generation before admitting exact G→G+1 candidate construction.

## 9. Candidate state machine

Materialized state:

```text
Inactive → Filling → Complete → one-shot swap → Inactive
```

There is no separately stored `CommitArmed` enum state in this bake. The permit is created at the final outer promotion boundary and consumed directly.

## 10. Committed reads and candidate writes

`slices(...)` always reads the logical committed `m/v` handles.

Transactional production writes through `write_candidate_slices(...)`, which targets only `candidate_m/candidate_v` while state is `Filling`.

The historical `update_slices(...)` symbol remains as a compatibility wrapper, but current production scheduler callsites no longer directly use committed-state `resident.update_slices(...)` semantics.

## 11. Canonical full B generation

Candidate write offsets must equal the current byte cursor. M/V SHA256 is updated as canonical logical windows are written. Out-of-order writes fail closed in R1.

B is a complete physical M/V generation, not a sparse overlay that depends on A after promotion.

## 12. No full A→B clone

R1 does not begin every step with a whole-model clone of A. Existing candidate materialization already yields complete logical M/V windows containing AdamW successor state plus unchanged compatibility state. Those windows populate B exactly once.

`full_m_clone_count` and `full_v_clone_count` remain structural zero targets.

## 13. 02 ActiveVerified direct-to-B

The 02 bounded projection now sends its already-mapped complete logical M/V windows to `write_candidate_slices(...)`.

No second GPU readback exists solely for B. AdamW-owned M/V remains the real device successor; Muon-owned compatibility M/V remains exact copy-forward under the existing R6 contract.

## 14. Legacy RAM direct-to-B

Legacy RAM candidate paths also use `write_candidate_slices(...)`.

For partitioned Muon/AdamW parameters, the old partial residual write into resident state was removed. The code first forms the complete logical candidate M/V window and writes that complete window once into B.

## 15. Candidate sealing

`seal_candidate_r1(...)` requires full canonical byte coverage and exact equality between the streaming B M/V digests and the outer candidate manifest M/V SHA256 values.

`RamAdamMvCandidateSealR1` binds source/target model+optimizer generations, candidate byte counts, M/V SHA256, coverage digest, candidate physical slot ID, and seal digest.

A complete candidate is still not committed authority.

## 16. Abort semantics

Optimizer execution or seal failure invokes `abort_candidate_r1(...)`. Candidate metadata returns to Inactive; Committed-A is not reconstructed because it was never overwritten.

Stale bytes in the inactive allocation are non-authoritative and are replaced during later canonical reuse.

## 17. One-shot swap permit

`RamAdamMvSwapPermitR1` binds source/target generations, candidate seal digest, candidate M/V digests, outer generation commit identity, and permit digest.

The current scheduler builds the commit identity from the R1 revision plus target commit evidence including `training_state_digest`, candidate digest, target generation, and target optimizer step.

B cannot self-promote merely because it is Complete.

## 18. Actual outer ordering

Current production order places the RAM A/B role swap late, after the target filesystem commit and surrounding runtime/resident-weight target promotion work required by the existing generation flow.

All fallible permit/candidate validation occurs before role mutation. The swap itself exchanges Vec ownership handles and Slot0/Slot1 role metadata. It performs no full M/V allocation, file I/O, or payload copy.

## 19. Optimizer-step advancement

`mark_optimizer_step()` rejects use under transactional mode. The committed optimizer generation advances only when `commit_candidate_r1()` successfully promotes B.

An aborted candidate does not advance committed RAM Adam generation state.

## 20. Pre-swap failure atomicity

For failures before successful role swap:

```text
Committed A after failure
= Committed A before begin_candidate_r1
```

bit-for-bit by ownership structure. No rollback copy is required.

## 21. Failure after filesystem target wins

If a late RAM swap failure occurs after the filesystem target already became current, the implementation does not reverse-swap or heuristically roll back the target.

It preserves the candidate directory, activates the existing recovery fence with `TargetFilesystemCurrent`, writes the existing `AshGenerationLastDurableSeal`, and requires `FreshRestartFromTargetCurrent`.

This is forward recovery.

## 22. Durable SSOT remains unchanged

No A/B runtime slot identity is made durable. This child creates no slot head or training-state V5.

Durable restart authority remains the existing V4 chain:

```text
active_training_state.json
→ TrainableGenerationDurabilityDescriptorR1
→ canonical restart payloads
```

Fresh process hydration may always restore the committed generation into a fresh Slot0 and allocate Slot1 again.

## 23. Run-local policy remains intact

A/B does not reintroduce ordinary per-step full M/V disk writes. Existing run-local/deferred durable policy remains authoritative.

At real durable boundaries, candidate B logical M/V identity must agree with the durable Adam M/V payload identity used by the surrounding commit flow.

## 24. Receipt and physical HOLD

`RamAdamMvTransactionalReceiptR1` reports slot IDs/count, generation identity, candidate lifecycle counts, swap/reuse counts, candidate M/V write bytes, clone counts, committed-slot mutation count, coverage/digest failures, swap-permit rejects, final committed M/V digests, RAM36 hard limit, and `physical_ram36_pass_claimed`.

This bake leaves `physical_ram36_pass_claimed = false` and emits the physical HOLD token. Qualification receipts are evidence, not a new durable participant or source artifact.

## 25. New static validator

New:
`tools/validate_ash_basetrain_ram_adam_committed_a_inactive_b_candidate_generation_transactional_swap_failure_atomicity_closure_r1_static.py`

It verifies dual-slot materialization, A-only source reads, B-only production candidate writes, Eve generation identity, no full A→B clone, seal/permit topology, validation-before-swap, post-filesystem forward recovery, RAM36 candidate owners, exact inventory candidate categories, no new RAM durable head, and physical PASS withheld.

## 26. Historical validator evolution

Two historical validators were widened only for current source evolution:

- FullModel AdamW successor validator accepts the newer `candidate_result` error/abort topology.
- 02 durable projection validator expects `write_candidate_slices(...)` instead of direct committed `update_slices(...)` semantics.

Their historical semantic gates remain active.

## 27. Observed static regression state

Final source/static chain:

```text
RAM Adam transactional A/B R1                         PASS
Trainable Generation Durability Descriptor / V4       PASS
Eve R1 common Adam semantics                          PASS
Eve R2 canonical Adam math                            PASS
P1 AdamW pending scheduler                            PASS
B06 multi-segment ledger                              PASS
FullModel AdamW segmented successor                   PASS
02 bounded durable projection                         PASS
SubmissionEpoch ActiveAsync                           PASS
P3 active transactional commit/restart                PASS
Unified Atlas MCU control plane                       PASS
RAM36 remaining-underflow attribution                 PASS
RAM36 successor-weight ownership transition           PASS
Immutable N2 RAM36 exact-retry parent                 PASS

PASS = 14
FAIL = 0
```

## 28. Compile and physical boundary

This child changes Rust ownership and cross-module APIs, so real `cargo check`/release build and Rust tests remain mandatory. The assistant bake environment exposes no `cargo`, `rustc`, or `rustfmt`; compile is not claimed.

Full physical PASS additionally requires actual dual-slot RAM36 admission, G→G+1 and G+1→G+2 slot reuse, no third full slot, no RAM36 hard-limit violation/leak, intentional mid-candidate failure with unchanged committed-A digest, exact candidate/durable M/V parity, and fresh-process restart parity.

None of those physical claims are fabricated by this source bake.

## 29. Packaging policy

Implementation ZIP excludes specifications/Markdown, `specs/`, bake/generated manifests, generated receipts/evidence, runtime JSON/JSONL, runtime packs, logs, `target*`, `.git`, Python bytecode caches, and backup outputs. Rust/Python implementation source and source-controlled Cargo manifests remain included.

GitHub publication is specification-only.

## 30. Source truth after successful code bake

```text
RAM Adam persistent dual physical slots                 true
logical committed/inactive roles                        true
candidate B exact G→G+1 identity                        true
candidate B canonical full logical stream               true
candidate B streaming M/V hashes                        true
02 direct-to-B adoption                                 true
legacy direct-to-B adoption                             true
full per-step A→B clone                                 false
committed A production candidate mutation               false by current callsite structure
one-shot validated role swap                            true
swap payload allocation/copy                            false by structure
post-filesystem swap failure forward recovery           true
RAM36 second-slot ownership                             true structurally
exact RAM inventory second-slot ownership               true structurally
physical RAM36 capacity PASS                            not claimed
failure-injection physical atomicity PASS               not claimed
release compile                                         not claimed
```

## 31. Exact next durability child

After real A/B qualification, the next storage experiment should remain shadow-only:

`ASH-BASETRAIN-WEIGHT-SUCCESSOR-BIT-EXACT-JOURNAL-SHADOW-ENCODING-COMPRESSION-MEASUREMENT-AND-KEYFRAME-FEASIBILITY-R1`

It should compare RAW, XOR(previous,current), XOR+byte-shuffle+Zstd, and XOR+bit-plane-shuffle+Zstd while requiring exact reconstruction of canonical target weight bits before any current R6 payload retirement.

## 32. Center sentence

**RAM Adam의 G+1은 이제 committed M/V를 조금씩 덮어써서 만들어지지 않는다. Committed-A는 candidate 생애 동안 읽기 권위로 남고, 02와 legacy candidate stream은 완전한 target M/V를 Inactive-B에만 쓴다. B가 full coverage와 digest로 봉인돼도 스스로 current가 되지 않는다. target generation이 실제로 승리한 마지막 경계에서만 one-shot permit이 이미 완성된 두 물리 슬롯의 Vec ownership과 논리 역할을 바꾼다. 중간 실패는 A를 건드리지 않고, filesystem target이 이미 이긴 뒤의 실패는 역swap이 아니라 fresh-restart로 회복한다. RAM36와 exact inventory는 둘 다 두 번째 물리 슬롯을 별도로 본다.**
