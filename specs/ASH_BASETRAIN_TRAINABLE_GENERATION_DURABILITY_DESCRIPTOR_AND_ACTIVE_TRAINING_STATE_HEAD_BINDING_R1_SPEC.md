# ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1

## Immutable Successful-Generation Durability Descriptor / Existing R6 Restart Payload Binding / Eve R2 Adam Math Lineage / Muon Momentum Lineage / 02 Device-Projection Provenance / P3 Fifth Durable Participant / `active_training_state.json` Sole-Head V4 Binding / One-Way V3 Root Migration / Fresh-Reopen Closure

## 0. Revision identity

Revision:

`ASH-BASETRAIN-TRAINABLE-GENERATION-DURABILITY-DESCRIPTOR-AND-ACTIVE-TRAINING-STATE-HEAD-BINDING-R1`

Parents:

- `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`
- `ASH-ADAMS-RIB-EVE-CANONICAL-ADAM-MATHEMATICAL-UPDATE-PRIMITIVE-AND-BACKEND-PARITY-MATERIALIZATION-R2`

Static/source PASS token:

`PASS_ASH_BASETRAIN_TRAINABLE_GENERATION_DURABILITY_DESCRIPTOR_ACTIVE_TRAINING_STATE_HEAD_BINDING_R1_STATIC`

Full release/fresh-process physical PASS is not claimed by this source bake.

## 1. Purpose

The existing production path already materializes durable candidate payloads and P3 transaction evidence before a target generation becomes current. The remaining missing authority is one immutable normal-generation object that binds the exact source state, target generation, restart payload set, Muon state lineage, Eve R2 Adam mathematical profile, 02 device-projection provenance and runtime continuation identity before the current head is published.

This revision materializes that object as `TrainableGenerationDurabilityDescriptorR1` and binds it into the existing `active_training_state.json` head without introducing a competing generation pointer.

## 2. Center invariant

The durable chain becomes:

```text
canonical restart payloads
→ TrainableGenerationDurabilityDescriptorR1
→ active_training_state.json V4
→ P3 commit/finalize lineage
```

The sole mutable current-generation head remains:

`training_state/active_training_state.json`

No `active_generation.json`, `current_generation.json`, `generation_head.json` or equivalent competing head is introduced.

## 3. Successful descriptor is not the existing failure seal

Current source already has `AshGenerationLastDurableSeal` for failed-transition/recovery disposition.

R1 keeps the two authorities separate:

```text
TrainableGenerationDurabilityDescriptorR1
= successfully materialized candidate-generation lineage

AshGenerationLastDurableSeal
= failure / last-good / restart-disposition lineage
```

The normal descriptor does not absorb failure classification and the failure seal does not become the normal-generation head.

## 4. New module and canonical file

New module:

`crates/base_train/src/trainable_generation_durability_descriptor_r1.rs`

Descriptor schema:

`ash.basetrain.trainable_generation_durability_descriptor.r1`

Candidate-local immutable filename:

`trainable_generation_durability_descriptor.r1.json`

The descriptor lives inside the exact candidate slot whose payloads it describes.

## 5. Materialized capabilities

Source capabilities are:

```text
TRAINABLE_GENERATION_DURABILITY_DESCRIPTOR_MATERIALIZED_R1 = true
ACTIVE_TRAINING_STATE_DESCRIPTOR_BINDING_MATERIALIZED_R1 = true
P3_DESCRIPTOR_PARTICIPANT_MATERIALIZED_R1 = true
FRESH_RESTART_DESCRIPTOR_REOPEN_MATERIALIZED_R1 = true
LEGACY_V3_TO_DESCRIPTOR_BOUND_V4_MIGRATION_MATERIALIZED_R1 = true
ACTIVE_TRAINING_STATE_REPLACED_AS_SOLE_HEAD_R1 = false
```

The last flag is deliberately false because the existing head is preserved rather than replaced.

## 6. Exact descriptor identity

`TrainableGenerationDurabilityDescriptorR1` binds:

- schema and revision;
- source and target training generations;
- source and target optimizer generations;
- source training-state digest;
- optional parent descriptor digest;
- parent-binding mode;
- candidate slot;
- candidate parameter-set digest;
- optimizer-state digest;
- packed-state manifest digest;
- canonical restart payload participant set;
- restart payload manifest digest;
- Muon durability binding;
- Eve R2 Adam mathematical-profile binding;
- materialization authority;
- optional 02 device-projection binding;
- dataset cursor digest;
- scheduler profile digest;
- current immutable bundle digest and pointer generation;
- P2 promotion receipt digest;
- durable restart completeness;
- descriptor semantic digest.

## 7. Generation successor contract

Required:

```text
target training generation = source training generation + 1
target optimizer generation = source optimizer generation + 1
```

Overflow, same-generation overwrite, rewind and generation gaps fail closed.

## 8. Source state is bound by digest

The descriptor binds `source_training_state_digest` in addition to the source generation ordinal.

This prevents generation number alone from standing in for the exact source state that produced the candidate.

## 9. Parent binding modes

New enum:

`TrainableGenerationParentBindingModeR1`

with:

```text
LEGACY_V3_ROOT
DESCRIPTOR_BOUND
```

A descriptor with `LEGACY_V3_ROOT` must have no parent descriptor digest.

A descriptor with `DESCRIPTOR_BOUND` must carry a valid parent descriptor digest.

## 10. Actual migration boundary discovered and enforced

The production scheduler retains the exact schema of the source `SourceState`.

The first descriptor-bound commit is allowed only when the source head is actually:

`ash.basetrain.training_state.v3`

and has no descriptor parent.

Failure:

`E_TRAINABLE_DURABILITY_R1_LEGACY_V3_ROOT_REQUIRED`

Once a source is descriptor-bound, its source schema must be V4 and its parent descriptor digest must be present.

Failure:

`E_TRAINABLE_DURABILITY_R1_DESCRIPTOR_BOUND_V4_PARENT_REQUIRED`

This bake does not fabricate descriptors for older V2/V3 history and does not silently infer a parent chain.

## 11. No V4 to V3 downgrade

`commit_active_state()` now rejects a source that already owns a descriptor digest if the target commit omits the next descriptor binding.

Failure:

`E_TRAINABLE_DURABILITY_R1_V4_TO_V3_DOWNGRADE_FORBIDDEN`

After the descriptor chain begins, it cannot silently reset.

## 12. Current canonical restart payload set remains four underlying payloads

The descriptor's `restart_payload_participants` are exactly the current P3 restart payload roles:

```text
MODEL_WEIGHT_PACK
ADAM_M_PACK
ADAM_V_PACK
MUON_MOMENTUM
```

R1 does not silently widen this canonical underlying restart set with unrelated transaction-side diagnostic/observer files.

## 13. Participant ABI

Each `TrainableGenerationDurabilityParticipantR1` binds role, candidate-local logical identity, target training generation, target optimizer generation, byte length and SHA-256.

Path escaping, zero-length payloads and invalid SHA values fail closed. Participant roles and logical identities must be unique.

## 14. Canonical restart payload manifest digest

`restart_payload_manifest_digest_r1(...)` sorts participants deterministically by role then logical identity and hashes that canonical participant set.

The descriptor itself is not included in this digest, preventing a recursive self-hash.

## 15. Descriptor becomes the fifth P3 participant

The P3 transaction participant set is widened from the existing four restart payloads to include:

`TRAINABLE_GENERATION_DURABILITY_DESCRIPTOR`

P3 now requires at least five participants and explicitly requires all five canonical roles.

The descriptor participant uses the descriptor file's physical byte length and SHA-256.

## 16. Digest layers remain distinct

The following are not collapsed:

```text
restart_payload_manifest_digest
= four underlying restart payloads

descriptor_digest
= canonical descriptor semantic identity

descriptor file SHA-256
= exact persisted descriptor bytes

P3 participant set / prepare digest
= transaction-level binding including descriptor as fifth participant
```

## 17. Muon durability binding

`TrainableGenerationMuonDurabilityBindingR1` is materialized from the existing `ProductionMuonMomentumManifest` and binds generation, optimizer step, momentum SHA-256, momentum byte length, registry digest, optimizer-routing digest and profile digest.

No new Muon state authority is created. The Muon generation and optimizer step must equal the descriptor target identities.

## 18. Eve R2 Adam math lineage binding

The descriptor persists `AdamMathProfileIdentityR2` from `아담의_갈비뼈_이브` R2.

The profile is recomputed and validated before descriptor acceptance. Its optimizer step must equal the descriptor target optimizer generation.

This durably binds which canonical Adam expression revision and exact hyperparameter bits produced the AdamW portion of the target generation without moving WGPU execution into Eve.

## 19. 02 device-projection provenance binding

When `FullTrainableDeviceDurableProjectionReceiptR1` exists, the descriptor materializes `TrainableGenerationDeviceProjectionBindingR1` containing source generation, target generation, full-trainable generation digest, coverage digest, projection plan digest, canonical layout digest and projection receipt digest.

The projection receipt must be complete and its generation transition must match the descriptor.

## 20. Materialization authority classification

New enum:

`TrainableGenerationMaterializationAuthorityR1`

with:

```text
FULL_TRAINABLE_DEVICE_GENERATION_R1
LEGACY_HOST_CANDIDATE
```

If a device-projection receipt exists, the authority is `FULL_TRAINABLE_DEVICE_GENERATION_R1` and the device-projection binding is mandatory.

If no device-projection receipt exists, the authority is `LEGACY_HOST_CANDIDATE` and a fake device-projection binding is forbidden.

## 21. Dataset and scheduler continuation identity

The descriptor binds dataset cursor digest and scheduler profile digest.

This prevents a model/optimizer payload from being treated as exact restart state while continuation position or scheduler profile silently differs.

## 22. Immutable bundle and P2 lineage

The descriptor also binds current immutable bundle digest, current bundle pointer generation and P2 promotion receipt digest.

These are lineage bindings only. The descriptor does not become their configuration or publication authority.

## 23. Descriptor self digest

`descriptor_digest` is computed by cloning the descriptor, clearing `descriptor_digest`, serializing the canonical value, and hashing it with SHA-256.

The self digest is semantic object identity. It is distinct from the persisted file SHA-256.

## 24. Physical file binding

`TrainableGenerationDurabilityDescriptorFileBindingR1` binds exact filename, semantic descriptor digest, file byte length and file SHA-256.

This allows the head and P3 transaction to prove both semantic identity and exact persisted bytes.

## 25. Descriptor persistence is immutable and fail-closed

Persistence order is:

```text
validate descriptor
→ serialize to .partial
→ write
→ flush
→ sync_all
→ rename to canonical filename
→ best-effort directory sync
→ reopen
→ validate self digest
→ compute physical file binding
```

If the final descriptor already exists, only an exact semantic-digest idempotent retry is accepted.

Conflicting replacement fails with:

`E_TRAINABLE_DURABILITY_R1_DESCRIPTOR_IMMUTABILITY_CONFLICT`

## 26. Descriptor precedes transaction validation and P3 prepare

Actual scheduler order is:

```text
restart payloads ready
→ descriptor build
→ descriptor persist/reopen
→ transaction.validated.json
→ transaction.ready_for_commit.json
→ P3 prepare
→ active-head commit
```

The head writer does not invent the descriptor.

## 27. `commit_active_state()` is a descriptor consumer

`commit_active_state(...)` now accepts an optional prevalidated `TrainableGenerationDurabilityDescriptorFileBindingR1`.

For descriptor-bound commits it inserts the descriptor binding into the target training-state object before calculating `trainingStateDigest`.

It does not build or persist the descriptor itself.

## 28. Training-state V4

New descriptor-bound current-state schema:

`ash.basetrain.training_state.v4`

Existing V3 remains accepted as the one-way migration source.

The canonical files remain unchanged:

```text
training_state/active_training_state.json
training_state/committed_training_state_step_XXXXXX.json
```

## 29. New V4 head bindings

V4 includes:

```text
trainableGenerationDurabilityDescriptorSchema
trainableGenerationDurabilityDescriptorFile
trainableGenerationDurabilityDescriptorDigest
trainableGenerationDurabilityDescriptorFileSha256
```

These fields are inserted before `trainingStateDigest` is computed, so the current head digest transitively binds the descriptor.

## 30. Historical state is not rewritten

Pre-R1 committed V3 history is not retroactively modified.

The first V4 target roots in the exact V3 source training-state digest. Subsequent V4 targets chain through the previous descriptor digest.

## 31. V4 resume reopens the descriptor

On resume, a V4 head reconstructs `TrainableGenerationDurabilityDescriptorFileBindingR1` from the head plus physical descriptor metadata and reopens the candidate-local descriptor.

The resume path verifies at least descriptor physical identity, descriptor semantic digest, target training generation, target optimizer generation, candidate slot, candidate parameter-set digest, optimizer-state digest, packed-state manifest digest, dataset cursor digest and scheduler profile digest.

The validated descriptor digest is retained in `SourceState` as the parent for the next generation.

## 32. P3 prepare binding

`McuActiveTransactionalPrepareInputsR1` now requires a descriptor file binding.

Before preparing the transaction, P3 reopens the descriptor and validates target generation, target optimizer generation, candidate parameter-set digest and packed-state manifest digest.

The prepare record stores descriptor filename, descriptor semantic digest, descriptor file bytes, descriptor file SHA-256 and restart payload manifest digest.

## 33. P3 finalize binding

`finalize_active_transactional_commit_r1(...)` verifies that the active head contains the same descriptor filename, semantic digest and physical file SHA-256 recorded by P3 prepare.

It reopens the descriptor again and requires its restart-payload manifest digest to equal the prepare record.

## 34. P3 restart rebind binding

`validate_restart_rebind_r1(...)` performs the same descriptor/head/prepare cross-check in the fresh-restart authority path and then validates the complete five-participant P3 set.

Descriptor corruption or missing descriptor is not repaired by inference from packs.

## 35. `SourceState` owns schema and parent descriptor identity

Production `SourceState` now retains:

```text
training_state_schema
durability_descriptor_digest
```

This is the state-ownership location that prevents V4→V3 chain loss during the next generation.

No global mutable descriptor registry is introduced.

## 36. No automatic orphan adoption

A valid descriptor and target payloads do not make a candidate current by themselves.

Only successful publication of `active_training_state.json` promotes the target generation. Finding the newest descriptor on disk is not an adoption rule.

## 37. Failure ordering remains fail-closed

If descriptor creation or persistence fails before P3 prepare, the source active head remains current and P3 target prepare is not admitted.

If the descriptor exists but active-head publication has not completed, the descriptor remains unadopted candidate evidence.

If a valid V4 head has already been durably published and later in-memory work fails, the filesystem target remains the durable authority under the existing fresh-restart recovery semantics.

## 38. Existing failure seal remains authoritative for failures

`AshGenerationLastDurableSeal` is not deleted, aliased or replaced.

It continues to describe failure/recovery disposition around the durable head. The new descriptor remains normal successful-generation provenance.

## 39. No payload-format migration

This revision does not change `weights.r6pack`, `adam_m.r6pack`, `adam_v.r6pack`, `PackedRuntimeStateManifestV1` or Muon momentum payload format.

The descriptor sits above the existing restart representation.

## 40. No journal or keyframe in R1

This revision does not introduce XOR or bit-plane weight journals, keyframe cadence, Zstd successor transport, ordinary full-pack retirement or RAM Adam A/B candidate slots.

The current representation is first given an immutable generation-level lineage identity.

## 41. No fake RNG binding

The inspected current source does not expose a separate canonical durable RNG-state object at this boundary.

R1 does not invent one merely to make the descriptor look more comprehensive. A future explicit restart-critical RNG authority must be added through its own grounded binding.

## 42. Static validator

New:

`tools/validate_ash_basetrain_trainable_generation_durability_descriptor_active_training_state_head_binding_r1_static.py`

It verifies exact descriptor revision/schema/filename, four canonical restart payload roles, Eve R2 Adam profile binding, 02 device-projection lineage binding, source and parent lineage, cursor/scheduler/bundle/P2 bindings, self digest and immutable persistence, descriptor-before-transaction ordering, P3 fifth participant, V4 head descriptor fields, V3 migration source support, V4→V3 downgrade rejection, fresh-reopen wiring, sole-head preservation, failure-seal separation and absence of GPU/RAM/pack-writer authority migration into the descriptor module.

## 43. Observed static regression state

The final source bake observed PASS for all ten source/static gates:

```text
Trainable Generation Durability Descriptor / Head Binding R1
Eve R1 common semantic materialization
Eve R2 canonical Adam math/parity materialization
P1 AdamW pending-generation scheduler
B06 multi-segment device-generation ledger
FullModel AdamW segmented successor
02 bounded durable projection / host-scatter retirement
SubmissionEpoch ActiveAsync completion
P3 active transactional commit/restart
Unified Atlas MCU control plane
```

## 44. Diff boundary

Parent R2 full-source to this child changes exactly five implementation/integration files:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/trainable_generation_durability_descriptor_r1.rs
crates/base_train/src/unified_atlas_mcu_real_production_parameter_wave_active_transactional_commit_and_restart_r1.rs
tools/validate_ash_basetrain_trainable_generation_durability_descriptor_active_training_state_head_binding_r1_static.py
```

## 45. Compile boundary

A real release compile remains mandatory because the bake changes `SourceState`, training-state schema handling, `commit_active_state()` signature, P3 prepare inputs and prepare record, P3 participant count, P3 finalize/restart validation and new cross-module descriptor types.

The assistant bake environment exposes no `cargo`, `rustc` or `rustfmt`.

Therefore release compile is not claimed.

## 46. Fresh-process physical boundary

A full physical PASS still requires at least:

```text
release compile PASS
real durable V3→V4 commit
real descriptor write/sync/reopen
real P3 five-participant prepare/finalize
active_training_state.json V4 publication
fresh-process restart from V4
all payload/descriptor SHA checks PASS
next-generation V4→V4 parent descriptor chain PASS
```

No such physical fresh-process PASS is claimed by this source bake.

## 47. Packaging policy

The baked implementation ZIP excludes this specification and all Markdown, `specs/`, bake manifests, generated runtime descriptors, generated transaction/P3 receipts, qualification evidence, runtime JSON/JSONL outputs, R6 runtime pack payloads, logs, `target/` and `target_*`, `.git/`, Python bytecode caches and source backup files.

Implementation source, Cargo source metadata and static validators remain included.

## 48. GitHub publication policy

GitHub publication for this revision is specification-only.

Implementation source remains in the delivered baked source ZIP unless implementation publication is separately requested.

## 49. Source truth after this bake

```text
TrainableGenerationDurabilityDescriptorR1          true
candidate-local immutable descriptor               true
semantic descriptor digest                         true
physical descriptor file binding                   true
four underlying restart payload bindings           true
Muon momentum lineage binding                      true
Eve R2 Adam math profile binding                    true
02 device-projection provenance binding             true
cursor/scheduler/bundle/P2 lineage binding          true
P3 descriptor fifth participant                    true
active_training_state sole head                     true
training-state V4 descriptor binding                true
actual V3-root first descriptor guard               true
V4 descriptor parent-chain guard                    true
V4→V3 downgrade                                     forbidden
fresh V4 descriptor reopen wiring                   true
existing failure seal preserved                     true
weight journal                                      false
RAM Adam A/B candidate                              false
release compile                                     not claimed
physical fresh-process restart PASS                 not claimed
```

## 50. Exact next child

After descriptor/head binding is compiled and physically qualified, the next durability boundary is:

`ASH-BASETRAIN-RAM-ADAM-COMMITTED-A-INACTIVE-B-CANDIDATE-GENERATION-TRANSACTIONAL-SWAP-AND-FAILURE-ATOMICITY-CLOSURE-R1`

That child should stop mutating the committed RAM Adam M/V authority range-by-range while a target generation is still provisional. It should introduce a distinct inactive candidate generation, then atomically rotate authority only after the whole generation wins.

## 51. Center sentence

**이 revision부터 “G+1이 저장됐다”는 말은 Weight/M/V 파일이 존재한다는 뜻만이 아니다. source training-state, 네 개의 canonical restart payload, Muon momentum lineage, Eve R2 Adam 수식 profile, 02 device projection provenance, cursor와 scheduler, bundle과 P2 promotion을 하나의 immutable descriptor가 먼저 봉인한다. P3는 그 descriptor 자체를 다섯 번째 durable participant로 받고, 기존 `active_training_state.json` V4가 descriptor의 semantic digest와 physical file SHA를 함께 가리킨다. 머리는 여전히 하나다. 첫 descriptor는 실제 V3 source에서만 시작할 수 있고, 한번 V4 chain이 시작되면 V3로 내려가거나 parent descriptor를 잃어버릴 수 없다.**
