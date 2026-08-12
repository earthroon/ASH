# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-RELOAD-PARITY-AND-STEP2-CONTINUATION-06C-R27-R1J-R4

## 0. Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-RELOAD-PARITY-AND-STEP2-CONTINUATION-06C-R27-R1J-R4`
- Build revision: `bt-wgsl-checkpoint-reload-parity-and-step2-continuation-06c-r27-r1j-r4`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-COMMITTED-GENERATION-CHECKPOINT-EXPORT-06C-R27-R1J-R3`
- Source authority: R3 committed checkpoint bundle, training generation `1`, optimizer step `1`
- Reload output authority: fresh-process generation-1 model/optimizer parity
- Step2 output authority: training generation `2`, optimizer step `2`
- Generation-2 checkpoint export: CLOSED
- R1J writer event in R4: CLOSED

## 1. Parent physical SSOT

R4 is designed against the physically passed R3 bundle whose observed state is:

- model logical tensor count: `201`
- optimizer-state logical tensor count: `402`
- model missing/duplicate: `0`
- optimizer missing/duplicate: `0`
- R3 generation-1 combined-state digest parity: `1`
- R1J E0 through E5: all observed
- R1J real export event: `1`
- bundle manifest valid/published: `1`
- source training generation: `1`
- source optimizer step: `1`
- configured gradient accumulation observed by R2E/R3: `8`
- physical microbatch accumulation: `1`
- production accumulation adoption: `0`

The R3 physical checkpoint identities used by the current parent run are:

- model SHA256: `5a369a1e6b747bfaf7a10e0adef6355eb4f54db201d8de051d0a3d7752d607ce`
- optimizer SHA256: `46b0ed637a52d6d50ed9b3a50153270eb963be67c5d88f44c9ddff3350f2b8de`

R4 never hardcodes those hashes as substitute source data. It reads the bundle manifest and recomputes the actual file digests.

## 2. Fresh-process boundary

R4 is a resume test, not an extension of the R3 process.

A valid R4 invocation MUST NOT carry:

- `--init-checkpoint-path`
- R2E optimizer-commit admission
- R3 checkpoint-export admission
- inherited tensor-group manifest path
- inherited Atlas group-plan path
- inherited sequential-load plan path
- inherited R2A materialization receipt path
- an existing R4 runtime `training_state` under the output directory

The runtime repeats these checks even if the CLI already checked them. This prevents a direct library caller from bypassing the fresh-process contract.

R4 source authority is only:

`--resume-checkpoint-bundle <R3 checkpoint_step_000001 directory>`

## 3. CLI admission

R4 adds:

- `--resume-checkpoint-bundle <path>`
- `--admit-checkpoint-reload-parity`
- `--admit-step2-continuation`

Reload-only admission requires the resume bundle and forbids genesis initialization.

Step2 additionally requires:

- `--admit-atlas-runtime-route`
- `--admit-atlas-forward-wave-execution`
- `--admit-atlas-final-output-real-loss`
- `--admit-atlas-real-loss-backward`

R2E and R3 flags are explicitly forbidden in the same R4 invocation.

## 4. Bundle-first authority resolution

R4 reads `checkpoint_bundle_manifest.json` first and requires:

- schema `ash.basetrain.checkpoint_bundle.r3.v1`
- `publicationState=COMMITTED`
- `trainingGeneration=1`
- `optimizerStep=1`
- exact model-spec identity
- exact tokenizer lineage identity
- exact dataset manifest identity

Only after that index is valid may the model, optimizer, and R1J files be opened.

## 5. Physical SHA256 parity

R4 computes the actual bytes of:

- `model.safetensors`
- `optimizer.safetensors`

and requires equality with the R3 bundle manifest.

No path-derived, filename-derived, or metadata-only digest can satisfy this gate.

## 6. R1J reader continuity

R4 reads the R3 R1J sidecar and requires all of the following to be physically present:

- `captureComplete=true`
- `realExportEventObserved=true`
- `authoritative=true`
- `outputFileSha256Authority == actual R3 model SHA256`

A missing `authoritative` field is not interpreted as true.

R4 is a reader/continuation stage and therefore does not emit a new R1J writer event.

## 7. Safetensors reopen validation

The model checkpoint MUST expose exactly `201` logical F32 tensors.

The optimizer checkpoint MUST expose exactly `402` logical F32 tensors:

- 201 `optimizer.m.<parameter>` tensors
- 201 `optimizer.v.<parameter>` tensors

For every safetensors entry R4 verifies:

- dtype `F32`
- logical shape product
- `shape_elements * 4 == data span`
- non-empty span
- exact payload continuity with no gap or overlap
- last payload end equals physical file size

Thus reload-only PASS cannot be obtained from a self-inconsistent header even when tensor counts superficially match.

## 8. Logical digest reconstruction

For each model parameter R4 computes the actual tensor-payload SHA256.

It reconstructs:

1. model logical digest
2. optimizer logical digest from m/v
3. generation-1 combined state digest from `parameter_id:weight_digest:m_digest:v_digest`

Required parity:

- reconstructed model logical digest == R3 bundle model logical digest
- reconstructed optimizer logical digest == R3 bundle optimizer logical digest
- reconstructed combined generation-1 digest == R2E candidate digest carried by R3

This is the reload parity barrier.

## 9. Optimizer configuration parity

Step2 continuation may not silently change optimizer semantics.

R4 requires exact parity with the R3 manifest for:

- optimizer kind: AdamW
- profile authority: `ASH-FT-38:ash_ft38_adamw_group_local_v1`
- learning rate
- beta1 `0.9`
- beta2 `0.999`
- epsilon `1e-8`
- weight decay
- configured gradient accumulation

Current observed accumulation SSOT is `8`.

Production 8-microbatch accumulation is still not adopted by R4. R4 executes one physical continuation microbatch only.

Scheduler/warmup progression remains closed.

## 10. Dataset continuation truth

R3 does not currently persist a canonical dataset cursor. R4 MUST NOT fabricate one.

The current physical step1 path deterministically used the first train preflight microbatch, ordinal `0`.

For R4 step2, the fresh process deterministically asks the same train split builder for at most two microbatches and selects ordinal `1`.

Required:

- step1 batch ordinal authority: `0`
- step2 batch ordinal authority: `1`
- random batch fallback: `0`
- if ordinal 1 is unavailable: fail closed

This is an explicit R4 limitation. Persistent dataset-cursor/checkpoint authority is deferred to a later patch and is not silently claimed here.

## 11. Generation-aware Atlas plan

R4 does not reuse genesis byte ranges.

After generation-1 checkpoint parity closes, R4 materializes a new production Atlas plan from the actual R3 `model.safetensors`.

The existing genesis R2A path retains its V5 tail-zero canary. The new committed-generation R2A wrapper disables only that genesis-specific zero-pattern assertion while preserving checkpoint/header/shape/role/plan validation.

No weight is repaired or rewritten.

## 12. Step2 execution source

The real step2 forward/loss/backward path receives:

- generation-1 `model.safetensors`
- generation-aware R2A plan
- deterministic train batch ordinal 1
- same model/tokenizer/dataset lineage

The ordinary R2/R2B/R2C/R2D production math path is reused.

R4 does not invent a separate forward or backward implementation.

## 13. Real step2 loss and backward

R4 requires the first step2 backward pass to produce:

- R2D physical PASS token
- 201 logical gradients
- zero missing gradients
- zero gradient-nonfinite tensors
- zero adjoint-nonfinite count

Step2 loss is read from the actual R2C runtime receipt produced by this continuation pass.

Step2 loss is an observation. R4 does not require it to be lower than step1 loss.

Gradient direction versus step1 is not a correctness gate.

## 14. Optimizer state origin

Step2 optimizer state origin is exactly:

`RELOADED_R3_STEP1_STATE`

The optimizer candidate path reads:

- generation-1 weight from R3 model checkpoint
- m1 from R3 optimizer checkpoint
- v1 from R3 optimizer checkpoint
- live step2 gradient from the replayed R2D GPU gradient wave

Genesis-zero moments are forbidden.

## 15. Deterministic backward replay

As in R2E, the first R2D pass provides full compact gradient observability but does not retain every raw gradient payload.

R4 therefore performs exactly one deterministic backward replay with a live gradient consumer.

Replay parity requires equality of:

- logical gradient tensor count
- global nonzero gradient element count
- raw global gradient L2 bit pattern
- raw global gradient max-abs bit pattern
- tail gradient classification

A mismatch aborts step2 candidate generation.

## 16. AdamW step index 2

The R4 WGSL candidate kernel consumes restored m1/v1 and uses true step-2 bias correction:

- `m2 = beta1*m1 + (1-beta1)*g2`
- `v2 = beta2*v1 + (1-beta2)*g2^2`
- denominator `1-beta1^2`
- denominator `1-beta2^2`
- decoupled `weight_decay * weight1`

Step1 bias correction is forbidden.

## 17. Micro-Atlas continuation

The R2E micro-Atlas geometry is retained:

- macro stream chunk budget: `16 MiB`
- micro-Atlas tile span target: `65,536` elements
- workgroup size: `64`
- target X workgroups: `1024`
- X/Y dispatch axes must each remain `<= 65,535`

Large dense gradient leases are sliced into bounded GPU sub-leases.

Sparse embedding continuation is split on full logical row boundaries so untouched rows still receive AdamW decoupled weight decay while their gradient is logically zero.

Gradient payload readback remains zero.

## 18. Candidate generation-2 staging

R4 creates a new local runtime state root under the new R4 output directory.

It seeds an active authority for the verified R3 source:

- generation `1`
- optimizer step `1`
- source R3 model/optimizer SHA256

Then it creates:

`training_state/candidate_step_000002/`

For every one of the 201 logical parameters it stages:

- candidate generation-2 weight
- candidate m2
- candidate v2
- logical coverage ranges
- update nonzero count
- update sum-of-squares/L2 contribution
- update max abs
- weight/m/v digest

## 19. Candidate validation barrier

Before generation promotion R4 requires:

- candidate parameter count `201`
- every logical parameter range continuous from zero to exact element count
- no overlap
- no gap
- candidate weight finite
- candidate m2 finite
- candidate v2 finite
- gradient payload readback `0`
- at least one real parameter update

Transaction order:

`STAGING -> VALIDATED -> COMMITTED`

## 20. Atomic generation and optimizer-step promotion

Only after the complete candidate set validates does R4 write a temporary active-generation pointer and atomically rename it into place.

Required transition:

- training generation `1 -> 2`
- optimizer step `1 -> 2`

The two authorities are published in the same active training-state object.

If candidate generation fails before promotion, generation1/step1 remain the source authority.

## 21. R3 checkpoint immutability

R4 recomputes the R3 model and optimizer physical SHA256 after step2 candidate commit.

They MUST match the pre-step2 values exactly.

R4 never mutates:

- R3 `model.safetensors`
- R3 `optimizer.safetensors`
- R3 bundle manifest
- R3 R1J provenance

## 22. Closed authorities

R4 keeps the following closed:

- generation-2 checkpoint write/export
- R1J writer event
- scheduler commit
- production accumulation adoption
- full-model weight readback
- full optimizer-state readback
- production gradient payload readback
- random batch selection
- genesis fallback
- zero-moment fallback

## 23. Reload-only mode

When `--admit-checkpoint-reload-parity` is supplied without `--admit-step2-continuation`, R4 performs the bundle/physical/logical parity gate only.

Reload-only PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_RELOAD_PARITY_06C_R27_R1J_R4`

Reload-only HOLD:

`HOLD_ASH_BASETRAIN_R1J_R4_GENERATION1_RELOAD_PARITY_COMPLETE_STEP2_CONTINUATION_NOT_YET_ADMITTED`

No generation2 candidate exists in reload-only mode.

## 24. Full step2 PASS

Full R4 PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_RELOAD_PARITY_AND_STEP2_CONTINUATION_06C_R27_R1J_R4`

Successful boundary HOLD:

`HOLD_ASH_BASETRAIN_R1J_R4_GENERATION2_AND_OPTIMIZER_STEP2_COMMITTED_GENERATION2_CHECKPOINT_EXPORT_NOT_YET_ADMITTED`

An exit code 1 caused only by that exact HOLD after PASS is the intended terminal boundary.

## 25. Physical receipt minimum

Full R4 must report at least:

- fresh process `1`
- source training generation `1`
- source optimizer step `1`
- model physical SHA parity `1`
- optimizer physical SHA parity `1`
- R1J provenance parity `1`
- model logical tensor count `201`
- optimizer logical state tensor count `402`
- model logical digest parity `1`
- optimizer logical digest parity `1`
- combined generation1 parity `1`
- genesis fallback `0`
- zero-moment fallback `0`
- optimizer state origin `RELOADED_R3_STEP1_STATE`
- configured gradient accumulation matching R3, current physical SSOT `8`
- step1 batch ordinal `0`
- step2 batch ordinal `1`
- step2 real batch/forward/loss/backward count `1`
- step2 logical gradient tensor count `201`
- gradient missing/nonfinite `0`
- replay count `1`
- replay parity `1`
- candidate parameter count `201`
- candidate gap/duplicate/nonfinite `0`
- nonzero global update count
- optimizer step `1 -> 2`
- training generation `1 -> 2`
- optimizer commit count `1`
- training-step commit count `1`
- R3 checkpoint mutation `0`
- checkpoint write/export `0`
- R1J writer event `0`
- receipt Atlas waves `40`

## 26. Receipt Atlas

R4 runtime receipt uses exactly `40` deterministic waves.

Each wave is limited to at most 8 fields and is built independently, sorted by ordinal, then sequentially written and merged with duplicate-key rejection.

No recursion-limit workaround is introduced.

## 27. Structural contract

R4 structural admission uses exactly 56 contract flags:

`--require-bt-wgsl-r27r1j-r4-contract-001=true`
through
`--require-bt-wgsl-r27r1j-r4-contract-056=true`

Structural mode proves only the availability and invariants of the R4 bridge. It does not perform physical reload or step2 mutation.

Required structural state includes:

- fresh process required
- generation1 required
- optimizer step1 required
- model 201 / optimizer 402
- no genesis/zero-moment fallback
- step2 bias correction step 2
- candidate generation2 semantics
- generation2 checkpoint export closed
- physical reload PASS false in structural mode
- physical step2 PASS false in structural mode

## 28. Semantic canaries

The current implementation contains `119` R4 negative semantic canaries, exceeding the minimum 110.

They cover, among others:

- same-process R3 reuse
- inherited R2E runtime state
- absent/invalid bundle
- physical SHA drift
- absent/non-authoritative R1J
- 201/402 count drift
- safetensors shape-span inconsistency
- logical/combined digest drift
- optimizer config drift
- accumulation drift
- genesis fallback
- zero-moment fallback
- genesis byte-range reuse
- step2 before reload barrier
- step1 batch reuse
- random batch fallback
- missing ordinal-1 batch
- full-model/full-optimizer materialization
- gradient payload readback
- step1 bias correction reuse
- source m/v ignored or zero-rebootstrapped
- candidate range gaps/overlaps
- premature generation2 promotion
- R3 checkpoint mutation
- premature generation2 checkpoint export
- dispatch-axis overflow
- macro-gradient unsplit path
- candidate-store reuse
- active-generation multiwrite
- receipt duplicate keys
- recursion-limit workaround

## 29. Static validation

R4 static validator:

`tools/validate_r27r1j_r4_checkpoint_reload_parity_step2_continuation_static.py`

It verifies runtime, backend, WGSL, CLI/config/pipeline wiring, committed-generation plan wrapper, structural chain, 40-wave receipt, 56 gates, 119 canaries, fresh-process firewalls, digest/parity gates, step2 m/v continuation, and generation2 atomic promotion.

Parent validators R1J through R3 are updated only to recognize R4 as the new terminal structural child; their original patch contracts remain unchanged.

## 30. PASS meaning

R4 full PASS means a completely new process consumed only the R3 committed checkpoint bundle, independently verified the model/optimizer physical files and R1J provenance, reconstructed exact 201-model/402-optimizer logical state and generation1 combined digest, then used the reloaded generation1 weights and real m1/v1 state to execute a new real step2 batch through the existing Atlas forward/loss/backward path. A second deterministic backward replay supplied live GPU gradients to an AdamW step-2 candidate kernel, and only after all 201 generation2 weight/m2/v2 candidates validated was training generation2 / optimizer step2 atomically published.

It does not prove convergence, loss improvement, production accumulation, scheduler/warmup behavior, or generation2 checkpoint persistence.

## 31. Next frontier

Recommended next patch:

`ASH-BASETRAIN-BT-WGSL-GENERATION2-CHECKPOINT-EXPORT-AND-MULTISTEP-RESUME-DETERMINISM-06C-R27-R1J-R5`

R5 should export generation2, reload it in another fresh process, prove step2 optimizer-state parity, and introduce an explicit persisted dataset-continuation cursor before opening a general continuous multi-step training loop.

## 32. SSOT seal

R3 wrote generation1.
R4 does not trust process memory from R3.

R4 trusts only a committed R3 bundle after actual byte and logical parity checks.

Generation1 weights come from R3 model bytes.
m1/v1 come from R3 optimizer bytes.
Step2 uses AdamW step index 2.

There is no genesis fallback.
There is no zero-moment fallback.
There is no random batch fallback.

R3 does not persist a dataset cursor, so R4 does not pretend that it does. Current deterministic continuation is explicitly ordinal 0 -> ordinal 1.

Generation1 remains canonical until all generation2 candidates validate.
R3 checkpoint bytes remain immutable.
Generation2 checkpoint export remains closed.

The R4 boundary is:

`FRESH R3 RELOAD -> EXACT GENERATION1 + M1/V1 -> REAL STEP2 -> VALIDATED GENERATION2 + M2/V2 -> ATOMIC GENERATION2 COMMIT`
