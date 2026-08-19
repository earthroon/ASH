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

Build revision:

```text
n8-deferred-durable-writeback-r1
```

## 2. Purpose

N8 long-horizon training executes eight optimizer steps. Before this patch the
RAM-resident Adam path already deferred Adam M/V pack materialization until final
writeback, but `weights.r6pack` was still materialized on every optimizer step.
The next step therefore remained coupled to large packed-state filesystem writes.

R1 introduces an explicit N8 deferred-durability route in which optimizer steps 1–7
advance through resident weight and RAM Adam state without writing any large packed
training payload. Step 8 materializes the complete final triple pack exactly once and
then performs the existing durable checkpoint/archive publication.

This patch changes persistence timing and resident continuation authority. It does not
change forward, backward, gradient, AdamW, Muon, scheduler, TensorCube, subgroup, Atlas,
or checkpoint serialization mathematics.

## 3. Explicit admission

New CLI admission:

```text
--admit-n8-deferred-durable-writeback
```

The route is fail-closed and requires all of the following:

```text
--admit-production-multistep-loop
--admit-n8-long-horizon-continuity
--production-loop-optimizer-steps 8
--admit-ram-resident-adam-mv
--admit-ram-weight-pack-persistent-residency
--storage-publication-policy checkpoint
```

The existing persistent weight route additionally retains its RAM36/exact-inventory
parent requirements. R1 does not weaken those pre-existing admission gates.

Required failure tokens include:

```text
N8DeferredWritebackN8AdmissionMissing
N8DeferredWritebackStepWindowMismatch
N8DeferredWritebackRamAdamMvAuthorityMissing
N8DeferredWritebackResidentWeightAuthorityMissing
N8DeferredWritebackCheckpointPublicationRequired
```

When the deferred flag is absent, legacy per-step weight materialization behavior remains
unchanged.

## 4. Eight-step resident transaction

For a source generation `G`, the admitted transaction is:

```text
G
 -> step 1 resident successor G+1
 -> step 2 resident successor G+2
 -> ...
 -> step 7 resident successor G+7
 -> step 8 resident successor G+8
 -> final triple-pack materialization
 -> durable checkpoint publication
 -> archive publication
```

For the current N8 generation-5 reproducer this is:

```text
5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13
```

Intermediate steps are resident commits. They are explicitly non-durable and must not be
presented as restartable checkpoints.

## 5. Intermediate packed payload write zero

In deferred mode, optimizer steps 1–7 must not create/write any large packed training
payload:

```text
weights.r6pack = 0 bytes written
adam_m.r6pack  = 0 bytes written
adam_v.r6pack  = 0 bytes written
runtime payload file count = 0
```

The weight writer is gated by:

```text
write_weight_payload = !deferred_durable_writeback || final_writeback
```

Adam M/V writers retain their existing final-writeback-only gating.

The implementation maintains a streaming SHA-256 over candidate weight bytes even when
there is no disk weight writer, so the run-local manifest and resident successor keep a
truthful weight digest/byte-length identity.

The following hard failure is preserved for any intermediate packed payload write:

```text
N8DeferredWritebackIntermediatePackedPayloadWriteDetected
```

### Control-write boundary

R1 does **not** claim zero filesystem writes of every kind. Small run-local control and
diagnostic files such as transaction markers, cursor/scheduler state, receipts, and
training-state JSON may still be written per step. The performance seal is specifically:

```text
intermediate packed training payload bytes = 0
```

The active training-state control record also reports:

```text
runtimePayloadFilesPerGeneration = 0
```

for deferred intermediate generations, so control metadata cannot claim a payload file
that does not physically exist.

## 6. Resident weight successor authority

Without a physical intermediate `weights.r6pack`, the next optimizer step must consume
the in-memory successor weight pack.

Candidate weight bytes therefore flow simultaneously into the resident successor builder
and, only on the final step, the disk writer:

```text
GPU/optimizer candidate bytes
        -> ResidentWeightPackBuilder     (steps 1–8)
        -> weights.r6pack writer         (step 8 only)
```

The resulting resident successor preserves generation, optimizer-step, source-path,
byte-length, and SHA-256 identity.

No intermediate disk weight file is allowed to become a hidden next-step authority.

## 7. Resident Atlas plan source

The existing packed-runtime Atlas plan materializer requires a physical packed weight
file. That requirement is correct for the legacy route but would make deferred step 2
fail before execution because step 1 intentionally has no `weights.r6pack`.

R1 therefore introduces:

```text
materialize_production_atlas_plan_for_resident_packed_runtime
```

The legacy public materializer still requires a physical file.

The resident materializer is selected only under deferred admission and is supplied only
a previously verified `ResidentWeightPack`. Before use the scheduler verifies:

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

The resident materializer removes only the physical-file-existence requirement. Tensor
geometry, offsets, parameter digests, registry digest, Atlas grouping, and plan digest
contracts remain unchanged.

## 8. Source-generation SSOT compatibility

R1 composes with:

```text
ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1
```

`SourceState.generation` remains the semantic generation authority. Resident weight and
RAM/VRAM residency are witnesses/carriers, not generation creators.

The deferred route does not reintroduce any synthetic generation-zero fallback.

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

The existing RAM Adam optimizer state, exact inventory, process-budget, generation, and
final writeback checks remain authoritative.

## 10. Final-step triple-pack materialization

Only the final optimizer step is a packed-payload durability boundary.

It must materialize all three payloads:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

Required physical conditions:

```text
weight payload bytes > 0
Adam M payload bytes > 0
Adam V payload bytes > 0
runtime payload file count = 3
```

Failure token:

```text
N8DeferredWritebackFinalTriplePackIncomplete
```

The final weight writer digest is cross-checked against the independently streamed weight
digest:

```text
N8DeferredWritebackFinalWeightDigestDrift
```

No checkpoint serialization format is changed.

## 11. Durable checkpoint and archive publication

The existing N8 storage publication runs after the eight-step training loop.
R1 verifies the resulting storage receipt rather than moving archive publication into the
optimizer loop.

Required counts:

```text
durable checkpoint publication count = 1
archive/durable receipt publication count = 1
```

Failure tokens:

```text
N8DeferredWritebackMultipleDurablePublication
N8DeferredWritebackMultipleArchivePublication
```

Publication ordering remains:

```text
final resident successor
 -> final triple-pack materialization
 -> final training-state commit
 -> N8 finalization
 -> durable checkpoint publication
 -> archive publication
```

## 12. Restart/crash semantics

Intermediate generations are intentionally non-durable. A process failure before final
writeback must not claim recovery from the latest resident generation.

Restart authority remains the last durable source checkpoint.

The existing run-local publication state remains explicitly non-resumable. R1 does not
silently synthesize missing weight or Adam payloads and does not introduce an automatic
intermediate disk fallback.

## 13. Runtime evidence

Per-step diagnostic:

```text
[N8-DEFERRED][STEP]
```

reports source/target generation, packed payload bytes, and final-materialization status.

On successful finalization R1 writes:

```text
n8_deferred_durable_writeback_receipt.json
```

both to the runtime output and durable receipt root.

The receipt seals:

```text
optimizer_steps = 8
resident_weight_authority = true
ram_adam_mv_authority = true

intermediate_weight_payload_write_count = 0
intermediate_adam_m_payload_write_count = 0
intermediate_adam_v_payload_write_count = 0
intermediate_*_payload_write_bytes = 0

final_weight_write_count = 1
final_adam_m_write_count = 1
final_adam_v_write_count = 1

durable_checkpoint_publication_count = 1
archive_publication_count = 1
synthetic_disk_fallback_count = 0
training_math_change_count = 0
optimizer_math_change_count = 0
gradient_math_change_count = 0
```

## 14. Static validator and CF1 integration

New validator:

```text
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
```

It is registered in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The existing RAM final-writeback validator is updated to distinguish:

```text
legacy RAM run-local mode:   weight payload files = 1
N8 deferred run-local mode:  packed payload files = 0
final writeback:              packed payload files = 3
```

This is a validator-authority correction required by the new explicit route. The legacy
runtime route itself is preserved.

## 15. Baked implementation surface

The R1 overlay contains exactly these implementation/validator files:

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

The overlay excludes generated artifacts, manifests, `.sha256` sidecars, and Python cache
output.

## 16. Bake-time structural evidence

Observed in the cumulative bake worktree:

```text
N8 deferred durable writeback R1:                         56/56 PASS
RAM resident Adam M/V final writeback:                    70/70 PASS
N8 source-weight generation SSOT:                         28/28 PASS
N8 long-horizon continuity:                               70/70 PASS
RAM weight-pack persistent residency / Atlas readahead:   67/67 PASS
Storage-root authority:                                   39/39 PASS
RAM36 process-budget authority:                           63/63 PASS
VRAM hot-weight-page residency:                           70/70 PASS
GPU successor weight commit continuity:                   52/52 PASS
N8 RAM-resident resume-cut determinism:                  118/118 PASS
RAM Adam M/V PCIe overlap:                                76/76 PASS
```

The exact-inventory validator also passes its complete current gate set.

Some full CF1 validators cannot be executed in the lightweight bake worktree because
their `specs/cli/...` fixture files are intentionally absent from that reduced tree.
Cargo/Rust physical compilation is also not claimed from the bake container because the
Rust toolchain is unavailable there. The authoritative local checkout's Release CF1 is
therefore a required promotion gate.

## 17. Promotion tokens

Static/structural tokens:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_EIGHT_STEP_RESIDENT_TRANSACTION_R1
PASS_ASH_BASETRAIN_N8_INTERMEDIATE_PACKED_PAYLOAD_WRITE_ZERO_R1
PASS_ASH_BASETRAIN_N8_FINAL_TRIPLE_PACK_MATERIALIZATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_DURABLE_CHECKPOINT_PUBLICATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_ARCHIVE_PUBLICATION_R1
```

Physical token:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_PHYSICAL_R1
```

Final promotion token:

```text
PROMOTE_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_R1
```

Physical and promotion tokens are not satisfied by static bake evidence alone.

## 18. Non-goals / semantic no-change boundary

R1 does not change:

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
- packed checkpoint serialization format,
- archive format.

R1 changes only the physical persistence timing and next-step resident-source authority
inside the explicitly admitted N8 transaction.

## 19. Final SSOT statement

```text
During an admitted N8 eight-step resident transaction, SourceState generations advance
through verified resident weights and RAM Adam M/V state.

Optimizer steps 1–7 may write small control/diagnostic state, but they write zero packed
training payload bytes and expose zero runtime payload files.

Only step 8 materializes weights.r6pack, adam_m.r6pack, and adam_v.r6pack, after which the
final durable checkpoint is published once and the archive is published once.

No intermediate disk payload may become a hidden continuation authority or fallback.
```
