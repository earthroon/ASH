# ASH-BASETRAIN-BT-WGSL-PRODUCTION-MULTISTEP-LOOP-ACCUMULATION8-WARMUP-SCHEDULER-06C-R27-R1J-R6

## Revision
- Patch: `ASH-BASETRAIN-BT-WGSL-PRODUCTION-MULTISTEP-LOOP-ACCUMULATION8-WARMUP-SCHEDULER-06C-R27-R1J-R6`
- Build: `bt-wgsl-production-multistep-loop-accumulation8-warmup-scheduler-06c-r27-r1j-r6`
- Physical parent: R5 committed generation3 / optimizer step3 / cursor next3.
- Gradient accumulation: exact 8; production adoption=1.
- Scheduler schema: `ash.basetrain.scheduler_profile.v1`.
- Active state schema: `ash.basetrain.training_state.v3`.
- Loop budget: explicit bounded N optimizer steps, N>=2.
- CLOSED: generation checkpoint export, partial-accumulator resume, epoch/shuffle, distributed training, long-horizon unattended promotion.

## 1. Source authority
Initial R6 source is the R5 compare output `training_state/active_training_state.json` and its committed `candidate_step_000003`, never the shadow probe, generation2 checkpoint, genesis, gradients, or reconstructed deltas.
Required initial state: generation=3, optimizer_step=3, 201 weights, 201 m3, 201 v3, cursor revision=2, last ordinal=2, next ordinal=3, consumed count=3.
Fresh R6 continuation may instead use a prior committed R6 output through `--resume-training-state`.

## 2. Explicit admission
Required first-run CLI: `--r6-parent-r5-run-dir`, `--admit-production-multistep-loop`, `--production-loop-optimizer-steps N`, `--gradient-accumulation 8`, `--scheduler-profile`.
Exactly one of `--r6-parent-r5-run-dir` and `--resume-training-state` is allowed.
R6 rejects genesis init paths, resume checkpoint bundles, external Atlas plan paths, concurrent R2E/R3/R4/R5 top-level admissions, N<2, accumulation!=8, and absent scheduler profile.
There is no implicit infinite loop.

## 3. Eight microbatches are one optimizer transaction
Each optimizer transaction performs exactly eight real R2B/R2C/R2D microbatch passes, forms one accumulated gradient set, runs AdamW once, and performs one canonical commit.
Microbatches do not individually mutate canonical weights, m/v, cursor, or scheduler.
A 7/8 or 9/8 transaction is invalid.

## 4. Active-loss-slot weighted accumulation
R2D gradients represent each microbatch active-slot mean loss. R6 therefore computes:
`A = sum(g_i * active_loss_slots_i)`, `W = sum(active_loss_slots_i)`, `g = A/W`.
The independently computed active-slot count must equal the child R2D receipt for every microbatch.
This retires equal-weight averaging of unequal-length microbatches.

## 5. Device-local FP32 accumulator
`R6DeviceGradientAccumulator` owns one logical F32 accumulator per parameter, exactly 201 logical parameters.
Each microbatch gradient wave is immediately absorbed into the accumulator, so eight full gradient sets are never retained simultaneously.
There is no inter-microbatch reset. A new accumulator is created for each optimizer transaction.
Nonfinite observation uses compact u32 status readback; production gradient payload readback remains 0.
Dense and sparse embedding accumulation both run on WGPU.

## 6. Bounded GPU geometry
R6 uses workgroup size 64, target X groups 1024, legal X/Y axes <=65535, 16 MiB optimizer stream chunks, 2D dense/AdamW dispatch, and page-bounded finalize dispatch.
Sparse embedding accumulation remains row-aware and consumes the R2D unique-token sparse gradient contract.

## 7. Committed runtime state, not checkpoint-per-step
R6 does not write safetensors after each optimizer commit. Canonical source is the active training-state pointer plus physically digested committed candidate weight/m/v files.
Optimizer commit and checkpoint export remain separate authorities.

## 8. Derived runtime arena
Existing Atlas execution expects a single range-addressable byte source, while R5/R6 canonical weights are per-parameter files. R6 therefore derives step-local `runtime_weights.r6arena` only from verified committed weights.
Authority is exactly `DERIVED_CACHE_NON_CANONICAL`.
The arena contains 201 logical tensors, is used only for a derived Atlas execution plan, is never a checkpoint/resume/R1J authority, reports checkpoint export=0, and is deleted after successful step commit.

## 9. Child math route
Every microbatch reuses the existing real R2/R2B/R2C/R2D forward/loss/backward math. R6 adds a consumer-capable real R2D entrypoint so one real backward both produces the R2D receipt and feeds gradient waves directly into the accumulator. No observe-plus-replay double backward is required per microbatch.

## 10. Accumulated-gradient barrier
Before AdamW: microbatch_count=8, logical_parameter_count=201, dtype=F32, total contribution weight finite/positive, nonfinite=0, payload readback=0, nonzero gradient count>0, global L2 finite/positive, max abs finite.

## 11. AdamW continuation
For target global optimizer step N, R6 consumes committed weight_(N-1), m_(N-1), v_(N-1), and the finalized accumulated gradient.
Bias correction uses beta1^N and beta2^N. Decoupled weight decay remains active.
Candidate weight/m/v egress is bounded; raw gradient payload readback remains 0.

## 12. Candidate coverage and commit boundary
Each candidate contains exactly 201 weights + 201 m + 201 v, with continuous zero-to-full logical element coverage, no gaps/overlaps/duplicates, finite outputs, and synced physical SHA256 digests.
Candidate files may be `STAGING` then `VALIDATED` then `VALIDATED_READY_FOR_CANONICAL_POINTER`.
R6 intentionally does NOT write a pre-pointer `transaction.committed.json`; the atomic active-state pointer is canonical commit authority.

## 13. Dataset cursor transaction
A successful optimizer commit advances the cursor by exactly eight ordinals: last becomes the eighth consumed ordinal, next +=8, consumed +=8, revision +=1, generation/optimizer step advance together, previous cursor digest binds the prior cursor.
Cursor never advances during microbatch execution.
Dataset manifest ID + actual physical SHA256, tokenizer lineage, and deterministic builder identity remain bound.
Random sampling, shuffle, implicit epoch transition, and wraparound remain closed.

## 14. First physical N=2 promotion
Source: generation3 / optimizer step3 / cursor next3.
Step4 consumes ordinals 3..10 -> generation4 / step4 / cursor next11.
Step5 consumes ordinals 11..18 -> generation5 / step5 / cursor next19.
Total physical microbatches=16. N=2 is the minimum physical promotion harness; the runtime accepts any explicit N>=2 that remains within scheduler and dataset authority.

## 15. Partial accumulation failure
R6 never persists/adopts partial gradient accumulators. A crash after 5/8 leaves the previous canonical active state unchanged. Fresh execution resumes from the latest fully committed state and replays the whole eight-microbatch transaction. Orphan partial/candidate state is never guessed canonical.

## 16. Explicit scheduler/warmup authority
Scheduler profile schema is `ash.basetrain.scheduler_profile.v1` with profile ID, kind, base/minimum LR, warmup optimizer steps, total optimizer steps, warmup start LR, optimizer profile authority, revision, and digest.
Supported kinds: `CONSTANT`, `LINEAR_WARMUP_CONSTANT`, `LINEAR_WARMUP_LINEAR_DECAY`, `LINEAR_WARMUP_COSINE_DECAY`.
No hidden scheduler family or warmup length is inferred during R6 admission.
Scheduler clock is global optimizer commit, never microbatch count. A failed candidate does not advance it.
Committed scheduler state records profile ID/digest, global optimizer step, phase, and exact F32 LR bits used by the WGSL optimizer.

## 17. Scheduler profile digest
Profile digest uses SHA256 over a domain-separated, length-framed representation plus exact little-endian numeric bit encodings rather than JSON whitespace/float formatting.
Digest domain: `ash.basetrain.scheduler_profile.digest.v1`.

## 18. Physical admission profile
Baked source includes `specs/r6_physical_admission_probe_scheduler_profile.json`.
It is a physical admission probe only, NOT a production tuning recommendation.
It uses `LINEAR_WARMUP_CONSTANT`, base/minimum/warmup-start LR all 5e-5, warmup steps=4, total steps=5. This exercises the WARMUP-to-SCHEDULE commit-clock transition without silently changing the LR magnitude already used by the three-step lineage.
A real longer run requires a separately approved profile.

## 19. Unified training state V3
`ash.basetrain.training_state.v3` binds generation, optimizer step, candidate directory, candidate parameter-set digest, candidate manifest digest, optimizer-state digest/origin, dataset cursor, scheduler state, gradientAccumulation=8, accumulatedMicrobatchCount=8, parent training-state digest, and training-state digest.
Generation, optimizer, cursor, and scheduler are one transaction. Split-brain combinations are invalid.

## 20. Immutable committed-state history and resume proof
Every R6 commit creates `committed_training_state_step_XXXXXX.json` and a synchronized `active_training_state.json.partial` before atomic active-pointer replacement.
History and final active state must be byte-identical after promotion.
Fresh R6 resume validates trainingStateDigest, optimizerStateDigest, candidate set/manifest digests, cursor digest, scheduler state/step, accumulation fields, current history parity, and the previous R6 committed-state digest chain where available.
The highest-numbered candidate directory is never guessed canonical.

## 21. Windows atomic pointer
Windows uses `MoveFileExW(MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)` after the partial active file is fully written/flushed/synced. Non-Windows uses rename. Final active state is reopened and digest-validated after replacement.

## 22. Checkpoint authority remains closed
R6 exposes no periodic-checkpoint cadence CLI. Generation-N runtime commit does not imply checkpoint publication. Generation5 checkpoint persistence and retention policy move to R7. No uncommitted candidate may be checkpointed by R6.

## 23. Receipt and structural authority
Runtime receipt Atlas is exactly 56 waves and is never silently truncated. Waves are <=8 fields, independently built, deterministically ordered, sequentially written, and duplicate-key checked.
Structural contract is exactly 72 ordered gates `--require-bt-wgsl-r27r1j-r6-contract-001=true` through `072=true`.
Runtime contains exactly 190 unique meaningful negative canary names, with no numeric padding canaries.

## 24. Static verification
Validator: `tools/validate_r27r1j_r6_production_multistep_accumulation8_warmup_scheduler_static.py`.
It validates runtime/backend/WGSL/CLI/config/pipeline/structural wiring, exact canary/gate/wave contracts, resume digest/history chain, atomic Windows pointer semantics, and the baked physical scheduler-profile digest.
Parent R1J..R5 validators change only their stale terminal-child expectation to R6; parent patch semantics remain unchanged.

## 25. PASS/HOLD
PASS: `PASS_ASH_BASETRAIN_BT_WGSL_PRODUCTION_MULTI_STEP_LOOP_ACCUMULATION8_WARMUP_SCHEDULER_06C_R27_R1J_R6`

HOLD: `HOLD_ASH_BASETRAIN_R1J_R6_PRODUCTION_MULTI_STEP_ACCUMULATION8_COMMITTED_LONG_HORIZON_TRAINING_PROMOTION_NOT_YET_ADMITTED`

The HOLD is intentionally generation-neutral because R6 accepts explicit bounded N-step budgets. The earlier draft's hard-coded Generation5/Step5/Cursor19 HOLD is retired because it would be false for N>2. For the physical N=2 harness those exact values are validated in numeric receipt fields instead.

## 26. Minimum physical N=2 receipt
Expected: R5 parent=1; source gen3/step3/cursor3; accumulation=8/adoption=1; target+committed optimizer steps=2; microbatches=16; first ordinals 3..10; final ordinals 11..18; accumulator F32/201/nonfinite0; gradient payload readback0; scheduler valid/commits2/final step5; generation3->5; optimizer3->5; cursor last18/next19/consumed19; canonical weight/optimizer/cursor commits2; partial accumulation adoption0; checkpoint export from uncommitted state0; runtime arena `DERIVED_CACHE_NON_CANONICAL`; arena checkpoint export0; receipt waves56.

## 27. PASS meaning
R6 PASS means at least two consecutive production optimizer transactions completed from the exact R5 generation3 state. Each transaction consumed exactly eight deterministic microbatches, formed an active-loss-slot-weighted FP32 device accumulator, ran AdamW once using the correct global bias-correction index, and atomically advanced generation, optimizer state, persisted cursor, and explicit scheduler state together. Partial accumulation was never adopted and no checkpoint authority was silently created from the runtime arena.

## 28. Not proven
R6 does not prove cross-GPU determinism, distributed reduction, shuffled epoch traversal, partial-accumulator persistence, unrestricted long-horizon training, convergence/quality improvement, periodic retention, or generation5 checkpoint persistence.

## 29. Next frontier
`ASH-BASETRAIN-BT-WGSL-LONG-HORIZON-TRAINING-PROMOTION-PERIODIC-CHECKPOINT-CRASH-RESUME-EPOCH-SHUFFLE-06C-R27-R1J-R7`
R7 may open periodic checkpoint/retention, latest-state fresh resume, deterministic epoch/shuffle authority, dataset rollover, long-run health ledgers and drift observability.

## SSOT seal
R5 proved one resumed step is exactly reproducible. R6 turns it into a bounded production loop.
Eight microbatches make one optimizer transaction. Microbatches do not move weights, optimizer state, cursor, or scheduler. All eight finish before AdamW runs once. Accumulation is FP32/device-local and weighted by actual active loss slots. Scheduler progression is explicit and optimizer-step-clocked. Generation, optimizer, cursor, and scheduler commit together. Mid-wave failure leaves the old canonical state alive. The runtime arena is a cache, never a checkpoint.

`R5 GENERATION3 + CURSOR3 -> 8x MICROBACKWARD -> FP32 WEIGHTED ACCUMULATOR -> ADAMW -> ATOMIC GEN/OPT/CURSOR/SCHEDULER COMMIT -> REPEAT`
