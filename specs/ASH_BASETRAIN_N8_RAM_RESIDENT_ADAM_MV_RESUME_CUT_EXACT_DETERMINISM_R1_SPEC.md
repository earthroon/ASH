# ASH-BASETRAIN-N8-RAM-RESIDENT-ADAM-MV-RESUME-CUT-EXACT-DETERMINISM-R1

## Status

Implementation-aligned Resume-Cut authority on top of the Pass147 BaseTrain source tree.

This R1 replaces the slow per-step disk Adam M/V hot path with RAM-resident Adam M/V for the determinism proof. The already completed disk-Adam GEN13 run is retained only as an optional frozen payload-compatibility reference and is never re-executed by this patch.

## Core contract

```text
GEN5 Common Parent Authority /

RAM-Resident Adam-M Authority /
RAM-Resident Adam-V Authority /
One-Time Durable M/V Hydration /
Whole-Leg RAM Optimizer-State Residency /

No Per-Step M/V Disk Read /
No Per-Step M/V Disk Write /
No HDD Optimizer Hot Path /

RAM Continuous-8 Reference /
RAM 4 + Durable GEN9 Cut + Fresh Reload + 4 /

Exact GEN9 Cut Boundary /
Exact OPT9 Cut Boundary /
Exact CURSOR51 Cut Boundary /

Planned Resume-Cut M/V Durable Flush /
No Unplanned Intermediate M/V Flush /

Fresh-Process GEN9 M/V Rehydration /
No Cross-Process RAM Carry /
No GPU Residency Carry /

Exact Weight Reload /
Exact Adam-M Reload /
Exact Adam-V Reload /
Exact Scheduler Continuation /
Exact Cursor Continuation /

Continuous GEN13 vs Resume-Cut GEN13 Exact Parity /

Existing Disk-Adam GEN13 Frozen Compatibility Reference /
No Slow Disk Baseline Re-Execution /

No Zero-Moment Fallback /
No M/V Reconstruction /
No Cursor Synthesis /
No Scheduler Replay /
No Batch Replay /

No Optimizer Math Change /
No QK-Norm Admission /
No Local-Muon Admission /
No PCIe-Overlap Admission /

Durable Snapshot Is Resume Artifact /
RAM Is Hot Optimizer-State SSOT /
No Dual Mutable M/V Authority /
No Canonical Promotion Before Resume-Cut PASS
```

## 1. Primary determinism authority

The primary proof is strictly same-source-tree:

```text
RAM_CONTINUOUS_GEN13
==
RAM_RESUME_CUT_GEN13
```

Both runs must bind the same:

```text
sourceTreeDigest
authoritativeBinarySha256
GEN5 active-state identity
model/tokenizer/dataset authorities
scheduler profile
parameter inventory
AdamW semantics
```

The old disk-Adam GEN13 is not the determinism authority because it may have been produced by an older source-tree digest.

## 2. Frozen disk reference

The already completed disk-Adam N8 GEN13 may be supplied to the comparison binary as:

```text
--frozen-disk-reference-dir <RUN>
```

Only final packed weight/M/V payload digests are observed for compatibility.

The patch records:

```text
slowDiskBaselineRerunCount = 0
```

A disk-reference mismatch never redefines the same-source RAM Resume-Cut proof.

## 3. Common parent

Both RAM paths originate from the physically promoted GEN5 parent:

```text
GEN5
OPT5
cursor next = 19
```

The original promotion receipt and pointer remain the parent authority.

For `cut-leg2`, the runtime source is GEN9, but the common-parent identity is still rebound through the original GEN5 physical-promotion receipt. No GEN9 receipt is allowed to synthesize a new ancestry root.

## 4. Runtime roles

R1 introduces three BaseTrain roles:

```text
continuous
cut-leg1
cut-leg2
```

and one independent comparison binary.

### continuous

```text
source: GEN5 / OPT5 / CURSOR19
budget: 8 optimizer commits
final:  GEN13 / OPT13 / last82 / next83 / consumed83
writeback reason: RUN_FINAL
```

### cut-leg1

```text
source: GEN5 / OPT5 / CURSOR19
budget: 4 optimizer commits
final:  GEN9 / OPT9 / last50 / next51 / consumed51
writeback reason: RESUME_CUT_BOUNDARY
```

### cut-leg2

```text
source: durable GEN9 / OPT9 / CURSOR51
budget: 4 optimizer commits
final:  GEN13 / OPT13 / last82 / next83 / consumed83
writeback reason: RUN_FINAL
```

No adaptive cut location is admitted.

## 5. RAM M/V authority

Each process performs exactly one M/V hydration from a physically persisted packed state.

After hydration and digest verification:

```text
AdamMHotAuthority = RAM
AdamVHotAuthority = RAM
```

Disk state is a durable source/snapshot, not a second mutable optimizer authority.

The existing physical-RAM capacity gate remains authoritative and requires an explicit nonzero reserve.

No capacity failure may silently fall back to disk Adam.

## 6. Physical M/V disk-accounting repair

This patch repairs an accounting defect inherited from the first RAM-resident implementation.

Intermediate RAM-resident generations physically write only the weight pack, but the old `R6ADiskStepReceipt` assigned the logical M/V pack byte size to `packed_m_payload_write_bytes` and `packed_v_payload_write_bytes` even when no M/V file was written.

R1 now records:

```text
intermediate packed_m_payload_write_bytes = 0
intermediate packed_v_payload_write_bytes = 0
```

while retaining the logical M/V pack sizes inside the packed-state manifest.

At the final step of a leg, the physical M/V write bytes remain the real pack byte counts.

This distinction is required for a truthful:

```text
perStepMvDiskWriteBytes = 0
```

proof.

## 7. Planned writeback reasons

The existing RAM-resident final-writeback contract is extended with an explicit writeback reason.

Exactly two reasons are admitted:

```text
RUN_FINAL
RESUME_CUT_BOUNDARY
```

No `AUTO`, memory-pressure, background, per-step, or best-effort flush reason exists in R1.

`cut-leg1` is the only path allowed to persist M/V before the end of an eight-step logical experiment, and that persistence occurs only after the fully committed GEN9 transaction.

## 8. GEN9 cut transaction

The GEN9 cut is published only after:

```text
gradient accumulation complete
optimizer candidate complete
weight commit
RAM M commit
RAM V commit
scheduler commit
cursor commit
GEN9 active state commit
```

Partial accumulation and uncommitted-state checkpointing remain forbidden.

## 9. Durable GEN9 publication

R1 adds an exact-state storage publisher for the cut path.

The durable checkpoint includes:

```text
active_training_state.json
committed_training_state_step_000009.json
committed_training_state_step_000008.json when required for parent-chain verification
packed_state_manifest.json
weight pack
Adam-M pack
Adam-V pack
checkpoint_binding.json
```

The previous committed-state copy is required because normal BaseTrain resume verifies the `parentTrainingStateDigest` chain.

Publication preserves the existing Storage Root behavior:

```text
D: hot runtime
→ E:\ASH .partial
→ stream digest verification
→ sync
→ physical digest verification
→ same-volume durable rename
```

Canonical-parent pointer updates remain zero.

## 10. Cut binding

The durable GEN9 `checkpoint_binding.json` binds:

```text
trainingGeneration = 9
optimizerStep = 9
cursorNextBatchOrdinal = 51
resumeCutPatchId
resumeCutRole = cut-leg1
writebackReason = RESUME_CUT_BOUNDARY
sourceTreeDigest
authoritativeBinarySha256
commonParentActiveStateSha256
freshProcessRequiredAfterCut = true
canonicalParentPromotion = false
```

`cut-leg2` verifies these fields before optimizer execution.

## 11. Fresh-process boundary

`cut-leg1` terminates through an expected HOLD after the durable GEN9 publication.

`cut-leg2` is a separate `base_train` process. Therefore process RAM, WGPU handles, GPU buffers, Atlas leases, micro-atlas slots, and accumulators cannot be carried through the cut as runtime authority.

The cut checkpoint itself declares `freshProcessRequiredAfterCut=true`; `cut-leg2` rejects a cut artifact without that contract.

## 12. GEN9 rehydration

`cut-leg2` physically verifies the durable GEN9 weight/M/V payload digests, validates optimizer durability and `RAM_RESIDENT_MV` state semantics, and then hydrates M/V once into fresh process RAM.

Forbidden:

```text
zero M/V fallback
M/V reconstruction from weights
receipt → optimizer-state synthesis
stale D: runtime fallback
```

## 13. Scheduler continuity

The N8 scheduler extension remains the only scheduler profile authority.

`continuous` extends GEN5/OPT5 to target step13.

`cut-leg1` is allowed to bind the same extended profile while terminating at target step9.

`cut-leg2` must already receive the target profile from GEN9 and therefore rejects a second scheduler-profile rebind.

Scheduler replay is not used.

## 14. Cursor geometry

Continuous batches:

```text
19..26
27..34
35..42
43..50
51..58
59..66
67..74
75..82
```

Cut path:

```text
leg1: 19..26, 27..34, 35..42, 43..50
leg2: 51..58, 59..66, 67..74, 75..82
```

The checkpoint cursor is the restart SSOT. No directory name, receipt filename, or inferred ordinal may replace it.

## 15. Gradient/R14 geometry

All roles retain:

```text
gradient accumulation = 8
```

Expected physical accumulated-gradient passes:

```text
continuous = 8
cut-leg1   = 4
cut-leg2   = 4
```

R14 lane cardinality is therefore:

```text
continuous = 64
cut-leg1   = 32
cut-leg2   = 32
```

Every observed lane must preserve the existing 4/4 owner-pin, raw-owner identity, zero writable-alias, and zero-fault contracts.

## 16. Feature isolation

For the first exactness proof R1 requires:

```text
RAM-resident Adam M/V = ON
PCIe optimizer overlap = OFF
QK-RMSNorm = OFF
```

TensorCube Local-Muon is not admitted into the BaseTrain optimizer execution path by this R1.

The purpose is to isolate storage/resume determinism from later optimizer/attention changes.

## 17. Continuous finalization

The continuous role reuses normal N8 long-horizon finalization and Storage Root checkpoint publication, then publishes the RAM-resident receipt and the Resume-Cut role receipt.

Expected successful terminal sequence includes:

```text
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_CONTINUOUS_GEN5_TO_GEN13_R1
PASS_ASH_BASETRAIN_N8_LONG_HORIZON_CONTINUITY_GEN5_TO_GEN13_OPT5_TO_OPT13_CURSOR19_TO_CURSOR83_R1
HOLD_ASH_BASETRAIN_N8_RAM_ADAM_MV_CONTINUOUS_GEN13_READY_CUT_LEG1_REQUIRED
```

The final HOLD may cause `base_train` to exit with code 1 and is an expected frontier when the preceding PASS evidence exists.

## 18. Cut-leg1 finalization

After exact GEN9 durable publication:

```text
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_RESUME_CUT_GEN5_TO_GEN9_R1
HOLD_ASH_BASETRAIN_N8_RAM_ADAM_MV_GEN9_CUT_DURABLE_READY_FRESH_PROCESS_RELOAD_REQUIRED
```

The HOLD intentionally forces the operator to start a new process for `cut-leg2`.

## 19. Cut-leg2 finalization

After fresh GEN9 rehydration and four commits:

```text
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_GEN9_FRESH_REHYDRATION_R1
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_RESUME_GEN9_TO_GEN13_R1
HOLD_ASH_BASETRAIN_N8_RAM_ADAM_MV_RESUMED_GEN13_READY_COMPARE_REQUIRED
```

## 20. Exact comparison binary

R1 adds:

```text
n8_ram_resident_adam_mv_resume_cut_compare
```

Required inputs:

```text
--continuous-run-dir
--resumed-run-dir
--output-path
```

Optional:

```text
--frozen-disk-reference-dir
```

The comparator first requires exact same-source RAM run identity:

```text
sourceTreeDigest
authoritativeBinarySha256
commonParentActiveStateSha256
```

It then physically rehashes the final durable weight/M/V payloads and compares:

```text
weight digest
Adam-M digest
Adam-V digest
parameter-offset registry digest
scheduler step/profile digest
cursor last/next/consumed
generation
optimizer step
```

Receipt-byte equality is intentionally not required because run paths, timestamps, and process-specific metadata are not semantic training state.

## 21. Core PASS

The primary terminal token is:

```text
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_RESUME_CUT_CONTINUOUS8_EQ_CUT4_RELOAD4_GEN13_R1
```

It means only that, under the same new CF1/source-tree/binary authority:

```text
GEN5 → RAM continuous 8 → GEN13
```

and:

```text
GEN5 → RAM 4 → durable GEN9 → fresh process → RAM 4 → GEN13
```

produce exact semantic training-state parity.

## 22. Optional disk compatibility PASS

If the frozen old disk GEN13 has the same final packed weight/M/V payload digests as the new RAM-continuous GEN13, the comparator additionally prints:

```text
PASS_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_FROZEN_DISK_GEN13_COMPATIBILITY_PARITY_R1
```

This is a compatibility observation, not a same-source determinism claim.

## 23. Final HOLD

After the exact comparator PASS:

```text
HOLD_ASH_BASETRAIN_N8_RAM_RESIDENT_ADAM_MV_GEN13_RESUME_DETERMINISTIC_READY_CANONICAL_PROMOTION_NOT_YET_ADMITTED
```

No canonical parent pointer is updated by this R1.

## 24. Mismatch attribution

The comparator fails closed with distinct classes including:

```text
RAM_RESUME_MODEL_WEIGHT_MISMATCH
RAM_RESUME_ADAM_M_MISMATCH
RAM_RESUME_ADAM_V_MISMATCH
RAM_RESUME_CURSOR_MISMATCH
RAM_RESUME_SCHEDULER_MISMATCH
RAM_RESUME_GENERATION_MISMATCH
RAM_RESUME_OPTIMIZER_STEP_MISMATCH
RAM_RESUME_PARAMETER_INVENTORY_MISMATCH
```

No generic mismatch repair or silent state normalization is admitted.

## 25. CF1 integration

R1 adds:

```text
tools/validate_n8_ram_resident_adam_mv_resume_cut_static.py
```

and registers it in the CF1 compile chain.

The CF1 chain also performs an explicit cargo check of:

```text
n8_ram_resident_adam_mv_resume_cut_compare
```

before producing the new source-tree-bound compile receipt.

Any Pass148 source-tree change invalidates the prior CF1 receipt.

## 26. PCIe validator repair

The normal PCIe-overlap path remains unchanged, but adding a separate RAM-continuous branch introduced an earlier textual occurrence of the N8 PASS token.

The PCIe static validator is therefore repaired to validate the final normal-N8 branch ordering rather than using the first global textual occurrence. The underlying PCIe runtime semantics are unchanged.

## 27. Bake-time static evidence

The Pass148 bake environment produced:

```text
Resume-Cut RAM Adam          118/118 PASS
RAM Resident Adam M/V         69/69 PASS
RAM Adam PCIe overlap         76/76 PASS
N8 Long Horizon               70/70 PASS
Storage Root                  39/39 PASS
Scheduler Extension           23/23 PASS
QK RMSNorm                    96/96 PASS
TensorCube Local Muon        101/101 PASS
Local-Muon Registry           92/92 PASS
Subgroup32 AdamW              36/36 PASS
R14                           52/52 PASS
Training Lineage              86/86 PASS
R2A micro-segment             32/32 PASS
```

Six older CF1 validators could not run in the intentionally slim bake archive because their `specs/cli/*.args` contract fixtures are not carried in the slim artifact. They are not claimed as PASS here.

The bake environment has no Cargo/rustc/WGPU physical toolchain. Therefore Rust compilation, shader/device execution, RAM capacity admission, GEN9 physical durable publication, fresh-process reload, and final exact parity remain operator-machine authority.

## 28. Changed source surface

Pass148 changes exactly 12 code/tool files:

```text
crates/base_train/src/bin/base_train.rs
crates/base_train/src/bin/n8_ram_resident_adam_mv_resume_cut_compare.rs
crates/base_train/src/config.rs
crates/base_train/src/lib.rs
crates/base_train/src/n8_ram_resident_adam_mv_resume_cut.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/storage_root_authority.rs
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_n8_ram_resident_adam_mv_resume_cut_static.py
tools/validate_ram_adam_mv_pcie_transfer_overlap_static.py
```

## SSOT seal

```text
COMMON PARENT
= GEN5 / OPT5 / CURSOR19

HOT ADAM M/V
= RAM only

PROCESS HYDRATION
= exactly once per role invocation

PER-STEP M/V DISK READ
= 0

PER-STEP M/V DISK WRITE
= 0

CONTINUOUS
= GEN5 + 8 → GEN13

CUT
= GEN5 + 4 → GEN9/OPT9/CURSOR51
  → RESUME_CUT_BOUNDARY durable flush
  → expected process stop
  → fresh process
  → durable GEN9 rehydration
  → +4 → GEN13

PRIMARY EXACTNESS
= RAM continuous GEN13 == RAM cut/reload GEN13

OLD DISK GEN13
= frozen payload-compatibility reference only
= rerun count 0

ZERO-MOMENT FALLBACK
= forbidden

M/V RECONSTRUCTION
= forbidden

SCHEDULER REPLAY
= forbidden

CURSOR SYNTHESIS
= forbidden

PCIe OVERLAP
= OFF for R1 proof

QK RMSNORM
= OFF for R1 proof

CANONICAL PROMOTION
= not admitted
```
