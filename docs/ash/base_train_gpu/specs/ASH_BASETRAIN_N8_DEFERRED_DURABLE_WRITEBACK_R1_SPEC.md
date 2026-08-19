# ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1

## 1. Patch identity

```text
ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1

Eight-Step Resident Transaction /
Intermediate Packed Payload Write Zero /
Resident Weight Successor Authority /
RAM Adam M·V Continuity /
Final-Step Triple-Pack Materialization /
Single Durable Checkpoint Publication /
Single Archive Publication Seal
```

Parent build revision:

```text
n8-deferred-durable-writeback-r1
```

Resident-checkpoint closure identity:

```text
ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1-
RESIDENT-CHECKPOINT-SOURCE-AUTHORITY-CLOSURE

Resident Logical Checkpoint Authority /
Physical File Existence Decoupling /
Resident Range-Read Session Identity /
Path·Digest·Byte-Length·Generation Parity Seal /
Disk Legacy Preservation /
Silent Disk Fallback Prohibition /
Step2→Step8 Resident Continuation Seal
```

Closure revision:

```text
n8-deferred-resident-checkpoint-source-authority-r1
```

## 2. Purpose

N8 long-horizon training executes eight optimizer steps. The RAM-resident Adam route
already supported final-only Adam M/V materialization, but the packed weight path was
still able to force large filesystem payload materialization into the optimizer loop.
R1 moves the durability boundary from each optimizer step to the end of the admitted
8-step resident transaction.

Optimizer steps 1–7 advance through resident weight and RAM Adam state without writing
large packed training payloads. Step 8 materializes the final `weights.r6pack`,
`adam_m.r6pack`, and `adam_v.r6pack`, then performs the existing durable
checkpoint/archive publication.

The Resident Checkpoint Source Authority Closure completes that design. After step 1,
the logical next checkpoint path intentionally exists only as metadata while its weight
payload is resident in memory. Runtime checkpoint consumers must therefore recognize a
verified resident range-read session as the physical backing authority for that logical
checkpoint identity. They must not require or recreate an intermediate `weights.r6pack`.

This patch changes persistence timing, checkpoint backing authority, and resident
continuation only. It does not change training or optimizer mathematics.

## 3. Explicit admission

The route is explicit:

```text
--admit-n8-deferred-durable-writeback
```

It requires the existing parent admissions, including:

```text
--admit-production-multistep-loop
--admit-n8-long-horizon-continuity
--production-loop-optimizer-steps 8
--admit-ram-resident-adam-mv
--admit-ram-weight-pack-persistent-residency
--storage-publication-policy checkpoint
```

The persistent weight route retains its RAM36/exact-inventory parent requirements.
No existing parent gate is weakened.

Admission failures remain fail-closed:

```text
N8DeferredWritebackN8AdmissionMissing
N8DeferredWritebackStepWindowMismatch
N8DeferredWritebackRamAdamMvAuthorityMissing
N8DeferredWritebackResidentWeightAuthorityMissing
N8DeferredWritebackCheckpointPublicationRequired
```

When deferred admission is absent, the legacy durable route is preserved.

## 4. Eight-step resident transaction

For source generation `G`:

```text
G
 -> resident successor G+1
 -> resident successor G+2
 -> ...
 -> resident successor G+7
 -> resident successor G+8
 -> final triple-pack materialization
 -> durable checkpoint publication
 -> archive publication
```

For the current generation-5 N8 reproducer:

```text
5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13
```

Intermediate steps are resident commits, not durable checkpoints. A crash before the
final materialization restarts from the last durable generation rather than claiming the
latest resident generation as recoverable state.

## 5. Intermediate packed payload write zero

In deferred mode, steps 1–7 must not create or write large packed training payloads:

```text
weights.r6pack = 0 bytes written
adam_m.r6pack  = 0 bytes written
adam_v.r6pack  = 0 bytes written
runtime payload file count = 0
```

The weight writer is gated by the final boundary:

```text
write_weight_payload = !deferred_durable_writeback || final_writeback
```

Adam M/V writers retain final-writeback-only behavior.

The candidate weight stream still computes its SHA-256 and byte length even when no
disk writer exists, so resident and manifest identities remain complete.

Intermediate large-payload write detection is fail-closed:

```text
N8DeferredWritebackIntermediatePackedPayloadWriteDetected
```

Small control/diagnostic files are not classified as packed training payload. Per-step
cursor, scheduler, receipt, and transaction metadata may still be written. The active
training-state control record reports zero runtime payload files for deferred
intermediate generations.

## 6. Resident weight successor authority

Updated weight bytes flow to the resident successor on every step and to the physical
weight writer only at the final boundary:

```text
GPU/optimizer candidate bytes
        -> ResidentWeightPackBuilder     steps 1–8
        -> weights.r6pack writer         step 8 only
```

The resident successor preserves:

```text
generation
optimizer step
logical source path
byte length
SHA-256
```

No intermediate disk weight file may become a hidden continuation authority.

## 7. Resident Atlas plan source

The legacy packed-runtime Atlas materializer remains physical-file-backed.
Deferred continuation uses:

```text
materialize_production_atlas_plan_for_resident_packed_runtime
```

Before resident plan materialization the scheduler verifies:

```text
resident generation == SourceState generation
resident optimizer step == SourceState optimizer step
resident source path == logical packed-weight source path
resident byte length == manifest weight byte length
resident SHA-256 == manifest weight SHA-256
```

Failure token:

```text
N8DeferredWritebackResidentPlanSourceIdentityDrift
```

Only the source backing changes. Tensor geometry, parameter order, offsets, digests,
registry digest, Atlas grouping, and plan digest contracts remain unchanged.

## 8. Source-generation SSOT compatibility

R1 composes with:

```text
ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1
```

`SourceState.generation` remains the semantic generation authority. Resident weight and
RAM/VRAM objects are carriers and parity witnesses. No synthetic generation-zero
fallback is reintroduced.

## 9. RAM Adam M/V continuity

Deferred admission requires the existing RAM-resident Adam M/V route.

Steps 1–7:

```text
Adam M physical pack write = 0
Adam V physical pack write = 0
```

Step 8:

```text
Adam M final pack write = 1
Adam V final pack write = 1
```

Existing RAM Adam process-budget, exact-inventory, generation, final-writeback, and
resume contracts remain authoritative.

## 10. Final-step triple-pack materialization

Only step 8 is the packed-payload durability boundary. It must materialize:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

Required final state:

```text
weight payload bytes > 0
Adam M payload bytes > 0
Adam V payload bytes > 0
runtime payload file count = 3
```

Failure tokens include:

```text
N8DeferredWritebackFinalTriplePackIncomplete
N8DeferredWritebackFinalWeightDigestDrift
```

Checkpoint serialization format is unchanged.

## 11. Durable checkpoint and archive publication

The existing N8 storage publication remains after the 8-step loop. Required counts:

```text
durable checkpoint publication count = 1
archive/durable receipt publication count = 1
```

Failure tokens:

```text
N8DeferredWritebackMultipleDurablePublication
N8DeferredWritebackMultipleArchivePublication
```

Ordering remains:

```text
final resident successor
 -> final triple-pack materialization
 -> final training-state commit
 -> N8 finalization
 -> durable checkpoint publication
 -> archive publication
```

## 12. Resident Checkpoint Source Authority Closure

### 12.1 Parent physical failure

The physical reproducer proved the parent writeback behavior:

```text
[N8-DEFERRED][STEP]
step=1/8
source_generation=5
target_generation=6
weight_source=resident
adam_source=ram_resident
weight_payload_write_bytes=0
adam_m_payload_write_bytes=0
adam_v_payload_write_bytes=0
final_materialization=0
```

Immediately afterward step-2 admission failed with:

```text
BTR27R1JR6APackedSourceMissing:
.../training_state/slot_b/weights.r6pack
```

This proved that step 1 had successfully created resident generation 6 while a legacy
checkpoint preflight still treated the logical `weights.r6pack` path as an unconditional
filesystem authority.

### 12.2 Logical identity versus physical backing

Within deferred intermediate generations:

```text
checkpoint logical identity
    = path + generation + byte length + SHA-256

checkpoint physical backing
    = verified ResidentWeightPack / active resident range-read session
```

The logical checkpoint path remains stable even when no physical file exists.

```text
logical path present in metadata
physical weights.r6pack absent
resident source present and verified
```

is a valid deferred intermediate state.

### 12.3 Active resident range-read authority

`begin_checkpoint_resident_range_read_session` now binds the resident generation in
addition to resident bytes and SHA-256.

The active session exposes a verified resident source authority containing:

```text
logical path
generation
byte length
SHA-256
```

Checkpoint preflight validates the resident authority before considering any legacy disk
path.

### 12.4 Path, digest, size, and generation parity

Required parity:

```text
requested logical path == resident logical path
expected SHA-256        == resident SHA-256
expected byte length    == resident byte length
SourceState generation  == resident session generation
```

Hard failures:

```text
N8DeferredResidentCheckpointPathDrift
N8DeferredResidentCheckpointDigestDrift
N8DeferredResidentCheckpointSizeDrift
N8DeferredResidentCheckpointGenerationDrift
```

No mismatch is repaired silently.

### 12.5 Physical file existence decoupling

For a valid active resident authority the former unconditional checks are not source
truth:

```text
resolved_checkpoint.is_file()
fs::metadata(checkpoint_path).len()
```

`training.rs` accepts the verified resident authority before the legacy
`BTR27R1JR6APackedSourceMissing` physical gate.

`atlas_runtime_route_admission.rs` obtains checkpoint byte length from the resident
authority when resident-backed. The legacy filesystem metadata path remains available
only when deferred mode is not active.

### 12.6 Silent disk fallback prohibition

Deferred mode is fail-closed if the resident authority is absent after resident
continuation has been admitted.

```text
N8DeferredResidentCheckpointAuthorityMissing
N8DeferredResidentCheckpointUnexpectedDiskFallback
```

The runtime must not respond by:

```text
creating a placeholder weights.r6pack
creating a zero-byte file
copying/spilling the resident payload to satisfy preflight
using a stale physical file
silently switching from resident to disk authority
```

Legacy disk behavior remains unchanged when deferred mode is not admitted.

### 12.7 Range-read continuation

The existing checkpoint range reader already projects bounded reads from resident bytes
when an active resident session is present and validates request-path identity. The
closure preserves that mechanism and extends the session identity with generation and
source digest authority.

Existing resident slice bound failures remain authoritative for out-of-range projection;
this closure does not weaken those range checks.

### 12.8 Step 2 through step 8 continuation

Primary physical acceptance is:

```text
step 1 target generation 6
    -> ResidentWeightPack(6)
    -> no slot_b/weights.r6pack
    -> step 2 source generation 6 admitted from resident authority
```

The same invariant must hold through step 8:

```text
6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13
```

Steps 1–7 continue to report zero packed payload bytes. Step 8 retains final triple-pack
materialization.

## 13. Runtime evidence

Per-step parent diagnostic:

```text
[N8-DEFERRED][STEP]
```

Resident checkpoint source diagnostic:

```text
[N8-DEFERRED][CHECKPOINT-SOURCE]
```

For a valid intermediate resident source it reports the resident authority, generation,
logical path, identity parity, physical-file observation, and:

```text
disk_fallback=0
```

Successful finalization writes:

```text
n8_deferred_durable_writeback_receipt.json
```

The parent receipt continues to seal zero intermediate packed payload writes, one final
triple-pack materialization, one durable publication, one archive publication, and zero
synthetic disk fallback.

## 14. Static validator and CF1 integration

Canonical validator:

```text
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
```

It remains registered in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The closure extends the same validator rather than introducing a competing authority.
It seals:

```text
resident closure identity/revision
resident session digest/generation ownership
resident source authority resolver
path/digest/size/generation hard gates
resident authority before physical-file requirement
legacy disk gate preservation
no deferred disk fallback
no placeholder pack creation
resident-valid/file-absent fixture
resident-absent/file-absent fixture
path/digest/size/generation negative fixtures
```

## 15. Implementation surface

Parent R1 implementation surface remains:

```text
crates/base_train/src/bin/base_train.rs
crates/base_train/src/config.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/production_atlas_plan_materialization.rs
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
tools/validate_ram_resident_adam_mv_final_writeback_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Resident Checkpoint Source Authority Closure adds/modifies:

```text
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/training.rs
crates/base_train/src/atlas_runtime_route_admission.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
```

Baked overlays exclude generated artifacts, manifests, `.sha256` sidecars, and Python
cache output.

## 16. Bake-time structural evidence

Observed in the reconstructed cumulative source tree after applying the closure:

```text
N8 deferred durable writeback + resident checkpoint closure: 87/87 PASS
N8 source-weight generation SSOT:                            28/28 PASS
Persistent TensorCube resource validator:                    68/68 PASS
N8 long-horizon continuity:                                  70/70 PASS
RAM resident Adam M/V final writeback:                       70/70 PASS
RAM weight-pack persistent residency / Atlas readahead:      67/67 PASS
VRAM hot-weight-page residency:                              70/70 PASS
GPU successor weight commit continuity:                      52/52 PASS
Storage-root authority:                                      39/39 PASS
RAM36 process-budget authority:                              63/63 PASS
```

The RAM exact-inventory static validator also exits successfully in the reconstructed
full source tree.

The bake environment has no Cargo/Rust toolchain, so Rust compilation and physical N8
execution are not claimed here. Release CF1 on the authoritative local checkout is the
next required gate.

## 17. Promotion tokens

Parent static tokens:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_EIGHT_STEP_RESIDENT_TRANSACTION_R1
PASS_ASH_BASETRAIN_N8_INTERMEDIATE_PACKED_PAYLOAD_WRITE_ZERO_R1
PASS_ASH_BASETRAIN_N8_FINAL_TRIPLE_PACK_MATERIALIZATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_DURABLE_CHECKPOINT_PUBLICATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_ARCHIVE_PUBLICATION_R1
```

Closure static tokens:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_SOURCE_AUTHORITY_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_IDENTITY_PARITY_R1
PASS_ASH_BASETRAIN_N8_DEFERRED_STEP2_RESIDENT_CONTINUATION_R1
```

Physical closure token:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_SOURCE_PHYSICAL_R1
```

Parent physical/final tokens remain:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_PHYSICAL_R1
PROMOTE_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_R1
```

Static evidence alone does not satisfy the physical/final tokens.

## 18. Physical acceptance

The current reproducer must progress beyond the former step-2 physical-file failure.
Required evidence:

```text
step 1/8: packed payload bytes = 0
resident generation 6 created
physical slot_b/weights.r6pack may be absent

step 2/8: source generation 6
checkpoint authority = resident
disk_fallback = 0
packed payload bytes = 0
```

The same resident continuation must hold through steps 3–7. Step 8 alone may create the
final triple-pack and durable/archive publications.

The following former error must not recur for a valid resident intermediate source:

```text
BTR27R1JR6APackedSourceMissing:<intermediate weights.r6pack>
```

## 19. Non-goals / semantic no-change boundary

R1 and this closure do not change:

- forward or backward equations,
- loss or gradient values,
- gradient accumulation count,
- AdamW or Muon equations,
- scheduler profile or learning-rate policy,
- dataset/token ordering,
- generation increment policy,
- TensorCube topology,
- exact subgroup32 execution,
- R14 owner-pin semantics,
- Stage11 merge semantics,
- Atlas geometry or parameter ordering,
- packed checkpoint serialization format,
- archive format.

They change only physical persistence timing, intermediate resident continuation, and
checkpoint source backing authority.

## 20. Final SSOT statement

```text
During an admitted N8 eight-step resident transaction, SourceState generations advance
through verified resident weights and RAM Adam M/V state.

Optimizer steps 1–7 write zero packed training payload bytes and expose zero packed
runtime payload files.

An intermediate checkpoint path is a logical identity, not an unconditional filesystem
authority. A verified ResidentWeightPack and active resident range-read session may back
that identity when path, generation, byte length, and SHA-256 match exactly.

If resident authority is valid, a physical intermediate weights.r6pack is unnecessary.
If resident authority is absent or mismatched, execution fails closed and never silently
creates, spills, substitutes, or falls back to disk.

Only step 8 materializes weights.r6pack, adam_m.r6pack, and adam_v.r6pack, after which the
final durable checkpoint is published once and the archive is published once.
```
