# ASH-BASETRAIN-BT-WGSL-PACKED-RUNTIME-NATIVE-BOOTSTRAP-AND-ACCUMULATION-WAVE-RESIDENCY-06C-R27-R1J-R6A-R1

## Revision and authority

- Patch: `ASH-BASETRAIN-BT-WGSL-PACKED-RUNTIME-NATIVE-BOOTSTRAP-AND-ACCUMULATION-WAVE-RESIDENCY-06C-R27-R1J-R6A-R1`
- Build: `bt-wgsl-packed-runtime-native-bootstrap-and-accumulation-wave-residency-06c-r27-r1j-r6a-r1`
- Code parent: Pass104 / R6A Packed Runtime State Disk Pressure Retirement.
- Physical parent: physically passed R5 generation3 / optimizer-step3 / cursor-next3.
- R6 and R6A physical promotion before R6A-R1: not established.
- Observed pre-patch physical failure: `ATLAS_RUNTIME_NATIVE_RUNTIME_UNAVAILABLE`.
- Role: close production-native bootstrap and retire accumulation8 packed-weight work-read amplification without changing R6 training math.

## 1. Internal native bootstrap

R6A-R1 does not require the historical external `--admit-atlas-runtime-route` flag. Production top-level admission selects native bootstrap internally when both `admit_production_multistep_loop` and `admit_r6a_r1_native_bootstrap_wave_residency` are true.

`prepare_training_config_and_atlas_runtime_bootstrap` accepts either historical explicit R2 admission or this production-internal route. The production bootstrap source is `base_train_r27r1j_r6a_r1_production_internal_native_bootstrap`.

The user-facing external R2 flag remains forbidden for the R6/R6A/R6A-R1 command. Child execution config may enable the internal R2 route only after the top-level production bootstrap exists.

## 2. Same device and queue authority

One ExistingDeviceBootstrap owns the Burn WGPU device and registers NativeWgpuRuntimeHandles. Atlas execution, FP32 accumulation, and AdamW must resolve from the same device/queue lineage.

Required authority:

- production native runtime required = 1
- external R2 admission requested = 0
- production internal native bootstrap = 1
- native bootstrap count = 1 per process
- per-microbatch bootstrap count = 0
- native runtime handles bound = 1
- same device identity = 1
- same queue identity = 1
- secondary adapter/device = 0
- CPU/generic fallback = 0

## 3. Bootstrap before storage mutation

The production loop resolves native runtime handles before creating its output directory, before R5-to-packed migration, and before candidate pack writes. Missing native runtime therefore fails before large storage mutation.

Required receipt: `storageMutationBeforeNativeBootstrap=0`.

## 4. No composite-batch shortcut

R6A-R1 preserves the existing G204D production `batch_size == 1` contract. The eight logical microbatches are not concatenated into `batch_size=8`, cross-lane sequence metadata is not rebuilt, and no cross-lane padding semantics are introduced.

Each lane remains an independent `BaseBatchCpu` with `batch_size=1`, its own valid lengths, positions, targets, loss authority, hidden checkpoints, and adjoint. `BTR2DG204DCurrentProductionBatchOneRequired` remains present.

## 5. Weight-wave-first accumulation

The old R6 schedule performed a complete Atlas forward/loss/backward traversal for each of eight microbatches. R6A-R1 makes the weight wave the outer loop and lanes 0..7 the inner loop.

For each decoder layer: activate the Atlas wave once, load/materialize the decoder block once, execute lanes 0..7 with that same block, retain each lane's next boundary hidden, then release the block.

The source generation, packed-weight SHA256, parameter registry, and block weights remain stable across all eight lanes.

## 6. Boundary hidden bank

Each lane keeps only the boundary hidden states required by the existing activation-checkpoint/recompute contract. A full eight-microbatch QKV/MLP decoder tape is not retained.

Workspace demand is calculated from the actual eight sequence lengths, hidden size, and layer count before training storage mutation. If the configured workspace cannot admit the lane bank, execution fails with `ACCUMULATION_WAVE_RESIDENCY_WORKSPACE_EXCEEDED`. There is no silent fallback to the old microbatch-first traversal and no activation disk spill.

## 7. Output-wave fanout

The final output Atlas group is admitted once per optimizer transaction. Final RMSNorm and untied LM-head residency are shared while all eight independent batch-one lanes compute their own target authority, streaming loss, loss tape, loss mean/sum, and active-loss-slot count.

Output forward fanout = 8. The output group remains resident for lane0..7 LM-head/final-RMS backward. Output backward fanout = 8.

## 8. Reverse decoder fanout

Backward is also weight-wave-first. Layer21 weights are loaded once and lanes0..7 run layer21 backward, then the block is released; the same pattern continues to layer0.

Each lane locally recomputes the required forward state from its own boundary hidden using the already-loaded block. The existing batch-one G204D attention-backward path remains intact.

## 9. Shared FP32 accumulator

One `R6DeviceGradientAccumulator` serves the optimizer transaction. Eight lane authorities have independent compact finite-status buffers/readbacks and independent active-loss contribution weights; there are not eight full parameter accumulators.

Dense and sparse embedding gradients are consumed immediately into the shared FP32 accumulator using lane-indexed accumulation. Contribution order for each resident parameter wave is deterministic lane order 0 through 7.

## 10. Active-loss-slot weighting

R6 semantics are preserved exactly:

`G = sum(g_i * active_i) / sum(active_i)`.

The production loop independently computes expected active slots and requires parity with the wave-resident executor. Logical accumulation remains 8. `physicalGradientPassesPerStep=1` means one shared Atlas reverse traversal per optimizer transaction, not one GPU kernel.

## 11. Packed-weight read session

All packed-weight range reads for one optimizer transaction are enclosed in one checkpoint-range read session bound to the exact `weights.r6pack` source. The source file is opened once and the session records physical read calls, seeks, and bytes.

Each optimizer step persists `r6a_r1_weight_read_receipt.json` with source/target generation, optimizer step, logical microbatch count, batch ordinal range, source-open/read/seek counts, physical weight work-read bytes, forward/backward layer-wave counts, output fanout, runtime-arena zero, and activation-spill zero.

## 12. Read amplification receipt

`actualWaveResidentWeightReadBytes` is the physically observed packed-weight work read for the shared traversal. The structural microbatch-first equivalent is that same admitted traversal repeated eight times:

- single traversal reference sum = actual wave-resident read bytes
- microbatch-first equivalent = actual * 8
- retired weight refetch bytes = actual * 7
- accumulation8 Atlas weight-read amplification = 1.0

This is a structural equivalent baseline from the admitted schedule, not an independently benchmarked historical R6 run. Optimizer state reads, migration reads, fresh-resume scans, and digest reads remain separate accounting classes.

## 13. R6A storage retirement remains sealed

R6A-R1 preserves three packed runtime payloads per generation, no per-parameter runtime payload files, no `runtime_weights.r6arena`, no arena I/O, write-time SHA256 authority, post-write digest reread bytes zero, three packed payload syncs per optimizer commit, immutable source packs, and ping-pong slot commit.

## 14. R6 training semantics remain authoritative

Unchanged:

- gradient accumulation = 8
- eight logical batch-one lanes per optimizer transaction
- AdamW once after the full accumulation
- cursor +8 per optimizer commit
- scheduler +1 per optimizer commit
- generation +1 and optimizer step +1 per commit
- explicit scheduler profile and global-step bias correction
- atomic generation/optimizer/cursor/scheduler/packed-slot promotion
- no partial accumulator adoption
- no epoch/shuffle adoption
- no generation checkpoint export

## 15. N=2 physical promotion harness

The first physical R6A-R1 run starts from R5 generation3 / optimizer3 / cursor-next3, performs the one-time generation3 packed adoption, then:

- step4 consumes ordinals 3..10 -> generation4 / optimizer4 / cursor-next11
- step5 consumes ordinals 11..18 -> generation5 / optimizer5 / cursor-next19

Expected logical microbatches = 16. Expected wave-resident physical gradient traversals = 2, one per optimizer transaction.

## 16. Required PASS chain

The physical run must emit:

1. `PASS_ASH_BASETRAIN_BT_WGSL_PRODUCTION_MULTI_STEP_LOOP_ACCUMULATION8_WARMUP_SCHEDULER_06C_R27_R1J_R6`
2. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_STATE_DISK_PRESSURE_RETIREMENT_06C_R27_R1J_R6A`
3. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_NATIVE_BOOTSTRAP_AND_ACCUMULATION_WAVE_RESIDENCY_06C_R27_R1J_R6A_R1`

Intended terminal HOLD:

`HOLD_ASH_BASETRAIN_R1J_R6A_R1_PACKED_WAVE_RESIDENT_PRODUCTION_MULTISTEP_COMMITTED_LONG_HORIZON_TRAINING_PROMOTION_NOT_YET_ADMITTED`

Exit code 1 caused only after the complete PASS chain by this HOLD is intended.

## 17. Minimum R6A-R1 receipt

Expected fixed contract fields include: R5 physical parent=1, R6A code parent=1, internal native bootstrap=1, external R2 admission=0, native bootstrap count=1, same device/queue=1, storage mutation before bootstrap=0, production optimizer steps=2, logical microbatches per step=8, physical gradient traversals per step=1, logical microbatches=16, physical gradient traversals=2, fanout lanes=8, forward/backward/output fanout=8, decoder forward/backward traversals=2, Atlas plan materializations=2, per-microbatch plan materialization=0, packed-weight read session opens=2, runtime arena create/rewrite=0, post-write digest reread=0, activation disk spill=0, generation after=5, optimizer after=5, cursor-next after=19, receipt Atlas waves=72, proof ledger HOLD.

Read-call/seek/byte totals, final max sequence length, and active-loss-slot totals are physical observations and are not hardcoded.

## 18. Structural and static authority

- Runtime R6A-R1 receipt Atlas: exactly 72 waves.
- Structural receipt Atlas: exactly 72 semantic waves.
- Structural gates: exactly 88 ordered gates.
- Semantic negative canaries: 115 unique meaningful names, no numeric filler.
- Composite-batch fallback is absent from production runtime.
- Existing R2D batch-one production gate remains present.
- Parent R1J through R6A semantic contracts remain intact; only terminal-child expectations and R6 physical accumulation orchestration assertions are updated for R6A-R1.

Static validator: `tools/validate_r27r1j_r6a_r1_packed_runtime_native_bootstrap_accumulation_wave_residency_static.py`.

## 19. PASS meaning

R6A-R1 PASS proves that production BaseTrain creates native Atlas runtime handles internally on the same Burn WGPU device/queue before mutating packed storage, and executes accumulation8 without repeating a complete packed-weight Atlas traversal for each logical microbatch. Eight independent batch-one lanes share each resident decoder/output weight wave, preserve independent sequence/loss/adjoint authority, and feed one active-slot-weighted FP32 accumulator in deterministic lane order. The runtime arena, per-parameter runtime-state files, post-write rehash, and per-microbatch packed-weight traversal remain retired.

## 20. Not proven

R6A-R1 does not prove disk active time can never reach 100%, zero disk I/O, permanent full-model GPU/RAM residency, permanent optimizer-state GPU residency, distributed accumulation, cross-device determinism, epoch/shuffle authority, long-horizon training promotion, or checkpoint retention policy. Large sequential packed-state writes and actual model/optimizer work reads may still saturate a slow disk. The patch retires structural amplification, not the disk itself.

## SSOT seal

`BOOTSTRAP FIRST -> STORAGE SECOND -> EIGHT INDEPENDENT BATCH_SIZE=1 LANES -> WEIGHT WAVE OUTSIDE / LANES INSIDE -> ONE FP32 SHARED ACCUMULATOR -> ONE ATLAS WEIGHT TRAVERSAL PER PHASE AND OPTIMIZER TRANSACTION -> NO EIGHTFOLD PACKED WEIGHT REFETCH -> NO RUNTIME ARENA -> NO ACTIVATION DISK SPILL -> NO SILENT MICROBATCH-FIRST FALLBACK.`