# ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-GRADIENT-OPTIMIZER-COMMIT-ADMISSION-06C-R27-R1J-R2E

## 0. Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-GRADIENT-OPTIMIZER-COMMIT-ADMISSION-06C-R27-R1J-R2E`
- Build revision: `bt-wgsl-atlas-runtime-gradient-optimizer-commit-admission-06c-r27-r1j-r2e`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-REAL-LOSS-BACKWARD-ADMISSION-06C-R27-R1J-R2D`
- Input authority: `REAL_LOSS_BACKWARD_COMPLETE / REAL_GRADIENT_WAVE_AUTHORITY_READY`
- Output authority: `ATLAS_TRAINING_GENERATION_COMMITTED`, optimizer step `0 -> 1`, training generation `0 -> 1`
- Checkpoint export: CLOSED
- R1J live export event: CLOSED
- Proof ledger: HOLD

## 1. Physical parent SSOT

R2E may execute only after the same invocation physically completes R2D. The current admitted V5 physical baseline is:

- logical gradient tensors: `201`
- missing: `0`
- duplicate: `0`
- gradient nonfinite tensors: `0`
- adjoint nonfinite count: `0`
- global nonzero gradient elements: `979910656`
- raw global gradient L2: `30.488143996254884`
- raw global gradient max abs: `0.68896836`
- decoder backward steps: `22`
- decoder adjoint: layer `22 -> 0`
- Layer21 parameter-gradient nonzero roles: `0`, hidden adjoint nonzero count: `335872`
- Layer20 parameter-gradient nonzero roles: `0`, hidden adjoint nonzero count: `335872`
- first nonzero decoder parameter-gradient layer from tail: `19`
- tail classification: `TAIL_PARAMETER_GRAD_ZERO_WITH_RESIDUAL_ADJOINT_LIVE`

These values are evidence, not hardcoded optimizer inputs. Runtime R2E binds the current same-invocation R2D receipt and rejects replay drift.

## 2. Explicit admission chain

R2E is opened only by:

`--admit-atlas-gradient-optimizer-commit`

The complete chain is required:

1. `--admit-atlas-runtime-route`
2. `--admit-atlas-forward-wave-execution`
3. `--admit-atlas-final-output-real-loss`
4. `--admit-atlas-real-loss-backward`
5. `--admit-atlas-gradient-optimizer-commit`

No parent admission is inferred from a child flag. R2D standalone PASS/HOLD semantics remain unchanged when the R2E flag is absent.

## 3. Optimizer authority

R2E does not invent an optimizer configuration.

Current BaseTrain configuration authority for the V5 large-model route is:

- optimizer kind: `adamw`
- learning rate: `5e-5`
- weight decay: `0.01`
- warmup steps configured: `500`
- gradient accumulation configured: `32`

R2E binds optimizer kind, learning rate, and weight decay from `BaseOptimizerConfig` at runtime.

Adam-family primitive semantics are additionally bound to the existing FT38 profile identity:

- profile: `ASH-FT-38:ash_ft38_adamw_group_local_v1`
- beta1: `0.9`
- beta2: `0.999`
- epsilon: `1e-8`
- optimizer-state dtype: `fp32`

FT38's historical/default learning-rate field does not override the BaseTrain runtime learning-rate authority. BaseTrain remains authoritative for learning rate and weight decay.

## 4. Clip policy authority

Current `BaseOptimizerConfig` has no canonical max-gradient-norm field. R2E therefore MUST NOT fabricate a threshold.

Current physical R2E policy:

- `clip_policy=NONE_NO_CANONICAL_MAX_NORM_AUTHORITY`
- `clip_scale=1.0`
- no gradient clipping
- no gradient rescale

The R2D raw norm remains the pre-clip observation baseline. Adding max-norm clipping later requires an explicit SSOT/admission revision and cannot silently alter this patch.

## 5. Accumulation and scheduler boundary

BaseTrain currently configures gradient accumulation `32` and warmup `500`, but this R2E patch is a one-microbatch physical optimizer-commit admission, not production multi-microbatch training-loop admission.

Receipt requirements:

- `configured_gradient_accumulation=32` for the current large-model config
- `physical_microbatch_accumulation_count=1`
- `production_accumulation_adoption=0`
- `scheduler_commit_count=0`

R2E MUST NOT pretend that one diagnostic physical batch satisfies 32-microbatch production accumulation. Warmup/scheduler progression remains closed.

## 6. Why deterministic backward replay exists

The R2D parent publishes compact real-gradient authority but does not retain all raw gradient payloads. R2E cannot manufacture optimizer input from receipts.

R2E therefore executes exactly one deterministic backward replay in the same process/device and installs a raw-gradient consumer at the point each physical gradient wave exists.

Required replay parity against the first R2D pass:

- logical gradient tensor count
- global gradient nonzero element count
- raw global gradient L2 bit pattern
- raw global gradient max-abs bit pattern
- tail gradient classification

Mismatch is fail-closed: `R2EBackwardReplayGradientParityMismatch`.

The replay does not publish a second canonical R2D artifact set.

## 7. Gradient payload ownership

R2E consumes `RawWgpuBufferLease` gradient waves directly.

Required:

- production gradient payload readback: `0`
- full-model gradient residency: `0`
- one bounded gradient wave at a time
- raw gradient authority immutable

Dense parameter gradients are consumed by exact logical element ranges. Sparse embedding gradients retain the unique token-row map.

## 8. AdamW sparse-embedding correctness

Sparse embedding gradient representation does not imply sparse logical parameter update under decoupled AdamW weight decay.

For each bounded embedding row range:

- touched rows consume their real sparse gradient
- untouched rows consume logical gradient `0`
- decoupled weight decay still applies to untouched nonzero weights

Thus `gradient=0` is not aliased to `parameter update=0`.

## 9. Checkpoint source authority

The generation-0 source checkpoint remains immutable.

R2E parses only the safetensors header and exact tensor data ranges. It MUST NOT deserialize/materialize the full checkpoint model.

Current R2E checkpoint candidate kernel is F32-only and fail-closed:

- checkpoint tensor dtype `F32`: admitted
- any other dtype: `R2ECheckpointDtypeUnsupported`
- no silent BF16/F16 conversion

The parent checkpoint precommit identity is the streaming SHA256 of the actual checkpoint bytes, not a path-derived surrogate digest.

## 10. Candidate state, not checkpoint export

R2E creates a runtime training candidate store under the run output directory:

`training_state/candidate_step_000001/`

For every logical parameter it stages:

- candidate weight
- first moment `m`
- second moment `v`

These files are runtime training state. They are NOT a safetensors checkpoint and do not constitute R3 checkpoint export.

Candidate files use create-new semantics. Existing candidate-step or active-generation state is fail-closed; there is no silent resume or overwrite.

## 11. Logical parameter coverage

Current V5 exact logical parameter count is `201`.

R2E requires:

- optimizer parameter count: `201`
- gradient count: `201`
- candidate parameter count: `201`
- missing: `0`
- duplicate: `0`
- per-parameter candidate range gaps: `0`
- per-parameter candidate range overlaps: `0`

Zero gradients remain present gradient authorities and count toward 201.

## 12. Candidate kernel

The R2E backend candidate kernel performs AdamW step-1 candidate generation with genesis-zero moments:

- `m1 = (1-beta1) * g`
- `v1 = (1-beta2) * g^2`
- step-1 bias correction
- `adam_term = m_hat / (sqrt(v_hat) + epsilon)`
- `update = adam_term + weight_decay * weight`
- `candidate_weight = weight - learning_rate * update`

The kernel validates finite gradient, source weight, moments, and candidate weight.

The gradient stays device-local. Candidate weight/m/v are bounded staging outputs and may be read back for the runtime candidate store.

## 13. Candidate observability

For each logical parameter, R2E records compact update observations:

- logical identity and shape
- covered logical ranges
- update nonzero element count
- update sum-of-squares / L2 contribution
- update max abs
- candidate weight digest
- candidate first-moment digest
- candidate second-moment digest

No raw parameter, gradient, or optimizer-state payload is logged into receipts.

Global R2E physical PASS requires at least one nonzero parameter update.

## 14. Tail-zero semantics

R2D proved Layer21 and Layer20 parameter gradients may be zero while residual adjoints remain live. R2E MUST preserve that distinction.

R2E records separately:

- Layer21 gradient nonzero role count
- Layer21 update nonzero role count
- Layer20 gradient nonzero role count
- Layer20 update nonzero role count
- Layer19 update nonzero role count
- first nonzero parameter-update layer from tail

The first changed layer is observed, not hardcoded. Under AdamW, a zero gradient can still coexist with a nonzero decay update.

## 15. Transaction states

Candidate transaction states:

1. `STAGING`
2. `VALIDATED`
3. `COMMITTED`

`STAGING -> COMMITTED` without validation is forbidden.

During STAGING and VALIDATED, generation 0 remains canonical. Candidate calculation itself is not canonical weight mutation.

## 16. Atomic training-generation promotion

After all 201 candidates and optimizer states pass coverage/digest/finite validation, R2E prepares generation 1 and atomically promotes the active training-generation pointer by same-directory temporary-file rename.

Authority transition:

- training generation `0 -> 1`
- optimizer step `0 -> 1`

Partial per-tensor canonical promotion is forbidden.

If staging or replay validation fails before promotion:

- candidate transaction becomes ABORTED when possible
- generation 0 remains canonical
- incomplete candidate data cannot auto-resume

## 17. Digest lineage

R2E binds:

- physical checkpoint SHA256 as precommit parameter-set parent identity
- ordered candidate weight/m/v digests into candidate parameter-set digest
- candidate manifest digest
- training-step state digest

After successful promotion:

- postcommit parameter-set digest equals candidate parameter-set digest
- candidate set must not alias the parent checkpoint identity when real update count is nonzero

## 18. Mutation boundary

Only successful generation promotion authorizes:

- canonical weight mutation = `1`
- optimizer-state mutation = `1`
- optimizer step count = `1`
- optimizer commit count = `1`
- training step commit count = `1`

Before promotion these remain zero canonical mutations.

## 19. Closed authorities

R2E MUST keep:

- full model weight readback: `0`
- full optimizer state readback: `0`
- gradient payload readback: `0`
- checkpoint write: `0`
- checkpoint export: `0`
- R1J real export event observed: `0`
- scheduler commit: `0`
- production accumulation adoption: `0`

## 20. Receipt Atlas

R2E uses 28 receipt waves:

00 R2D physical parent
01 explicit optimizer admission
02 raw-gradient authority binding
03 optimizer-config authority
04 clipping-policy authority
05 optimizer replay plan
06 LM-head optimizer wave
07 final-RMS optimizer wave
08 Layer21 optimizer candidate
09 Layer20 optimizer candidate
10 layers19-16 candidate
11 layers15-12 candidate
12 layers11-8 candidate
13 layers7-4 candidate
14 layers3-1 candidate
15 Layer0 split candidate
16 embedding candidate
17 optimizer-state coverage
18 candidate parameter coverage
19 candidate finite validation
20 update observability
21 tail update forensic
22 candidate-generation digest
23 transaction validation barrier
24 atomic generation promotion
25 postcommit parity
26 mutation/checkpoint firewall
27 R3 handoff

Receipt rules remain:

- max 8 fields per chunk
- parallel chunk build
- sequential streaming write
- deterministic wave merge
- duplicate key fail-closed
- no recursion-limit workaround

## 21. Structural gate

Structural contract keys:

`--require-bt-wgsl-r27r1j-r2e-contract-001` through `048`.

Structural gate does not execute optimizer mutation. It must report:

- `gradient_optimizer_commit_bridge_ready=1`
- `physical_optimizer_commit_pass=0`
- `optimizer_commit_admission_status=ATLAS_GRADIENT_OPTIMIZER_COMMIT_NOT_REQUESTED`
- `optimizer_step_count=0`
- `training_generation=0`
- checkpoint export closed

Structural gate requires at least 80 semantic canaries. Current code carries 82.

## 22. Physical runtime receipt minimum

Successful physical R2E must report at least:

- R2D physical parent bound
- explicit optimizer commit requested
- raw-gradient authority bound
- logical gradient tensor count `201`
- preclip global gradient L2 / max abs
- clip policy / scale
- optimizer kind and profile authority
- learning rate, beta1, beta2, epsilon, weight decay
- optimizer state origin `GENESIS_ZERO_MOMENTS` for this first fresh step
- configured accumulation and physical one-microbatch boundary
- replay count `1` and parity `1`
- optimizer parameter count `201`
- candidate parameter count `201`
- zero candidate gaps / duplicates / nonfinite values
- nonzero global parameter-update count
- update L2 / max abs
- tail update forensic
- training generation `0 -> 1`
- optimizer step `0 -> 1`
- optimizer commit count `1`
- training-step commit count `1`
- canonical weight mutation `1`
- optimizer-state mutation `1`
- checkpoint write/export `0`
- receipt Atlas waves `28`

## 23. Negative canaries

At minimum R2E rejects:

- absent R2D parent
- absent raw-gradient authority
- missing/duplicate/mismatched gradient identity or shape
- nonfinite gradient
- missing or silently defaulted optimizer authority
- invalid LR/beta/epsilon/weight decay
- stale/double/per-wave-inconsistent clip authority
- replay mismatch
- second device/queue
- full gradient residency or host readback
- mutation during staging
- missing/duplicate/nonfinite candidate or optimizer state
- partial Layer0 candidate
- duplicate decay/bias correction
- step-index mismatch
- parent/candidate generation alias
- missing/mismatched candidate digest
- commit before 201 candidates
- commit before validation
- partial generation promotion
- all updates zero despite real nonzero gradient
- scheduler silent advance
- checkpoint write/export
- R1J export event
- candidate-store reuse / silent resume
- non-F32 checkpoint silent conversion
- sparse embedding row-map corruption
- skipped AdamW decay on untouched embedding rows
- Layer20/21 zero-gradient-as-missing alias
- configured accumulation silent adoption
- warmup/scheduler silent adoption
- giant final receipt / duplicate receipt key / recursion-limit workaround

Current semantic canary count is `82`.

## 24. PASS / HOLD

Physical PASS token:

`PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_GRADIENT_OPTIMIZER_COMMIT_ADMISSION_06C_R27_R1J_R2E`

Successful authority-boundary HOLD:

`HOLD_ASH_BASETRAIN_R1J_R2E_OPTIMIZER_STEP1_AND_TRAINING_GENERATION1_COMMITTED_CHECKPOINT_EXPORT_NOT_YET_ADMITTED`

An exit code 1 caused only by this exact HOLD after the PASS token is an intended terminal boundary, not R2E failure.

## 25. PASS meaning

R2E PASS means the same-invocation real R2D gradient authority was deterministically reproduced and consumed by the canonical admitted AdamW step-1 candidate path; all 201 logical parameter candidates and required optimizer-state candidates were generated and validated without gradient payload readback or partial canonical mutation; then and only then training generation 1 / optimizer step 1 was promoted as the canonical runtime training state.

It does not mean multi-step training, 32-microbatch production accumulation, warmup/scheduler advancement, checkpoint export, or R1J live writer provenance has occurred.

## 26. Next frontier

Next patch:

`ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-COMMITTED-GENERATION-CHECKPOINT-EXPORT-06C-R27-R1J-R3`

R3 consumes R2E generation 1 plus optimizer state 1 and opens canonical checkpoint serialization/export. R1J E0-E5 live provenance capture becomes physically observable only there.

## 27. SSOT seal

R2D proves the gradient. R2E does not optimize from receipts; it replays the real backward once and consumes live GPU gradient waves.

R2E does not invent clipping, accumulation, scheduler, or optimizer defaults. Candidate data is not canonical until all 201 parameters and optimizer states validate. Failure before promotion leaves generation 0 canonical. The sole canonical mutation boundary is generation-pointer promotion from 0 to 1. Checkpoint export remains closed.
