# ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-REAL-LOSS-BACKWARD-ADMISSION-06C-R27-R1J-R2D

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-REAL-LOSS-BACKWARD-ADMISSION-06C-R27-R1J-R2D`
- Build revision: `bt-wgsl-atlas-runtime-real-loss-backward-admission-06c-r27-r1j-r2d`
- Physical parent: R27-R1J-R2C real-loss physical PASS
- Input authority: `RealLossReady` + `LossTapeReady`
- Output authority: `REAL_LOSS_BACKWARD_COMPLETE` + canonical real-gradient wave authority
- Gradient clipping: closed
- Optimizer: closed
- Weight mutation: closed
- Checkpoint export: closed
- Proof ledger: `HOLD`

## Objective

R2D consumes the same-process R2C real-loss context and proves that the actual production NLL adjoint propagates through bounded LM-head vocab VJP, final RMSNorm backward, reverse decoder layers 21 through 0, and embedding backward without opening optimizer or checkpoint authority.

The current V5 checkpoint contains a physically collapsed projection tail. Therefore R2D explicitly separates zero parameter gradients from backward-path failure. A zero logical gradient remains a present gradient authority, not a missing gradient. Hidden-adjoint continuity is tracked independently.

## Explicit admission

R2D adds:

```text
--admit-atlas-real-loss-backward
```

The physical chain is explicit:

```text
--admit-atlas-runtime-route
--admit-atlas-forward-wave-execution
--admit-atlas-final-output-real-loss
--admit-atlas-real-loss-backward
```

Standalone R2C retains its existing HOLD. Only explicit R2D admission continues into backward.

## Same-process parent authority

R2D must consume the live R2C context directly. It does not reload loss tape, hidden state, model output, or decoder state from disk.

Current physical parent evidence includes 164 active target rows, 164 targets found, no target misses, three bounded vocab waves, finite real mean loss, and both real-loss and loss-tape authority.

The physical parent `compact_loss_scalar_readback=2` is retained as observation SSOT and is not silently rewritten.

## Backward loss semantics

Backward begins from the already published mean NLL. Mean normalization is applied exactly once. R2D does not invent dynamic loss scaling, extra batch normalization, clipping or gradient rescaling.

R2C logZ, target IDs and active-row identities remain the target/loss authority.

## Bounded LM-head VJP

R2D keeps full logits and full dLogits surfaces closed. For each bounded vocab range it recomputes only the required logits from the resident Wave23 LM-head view, evaluates the cross-entropy adjoint, immediately performs:

- normalized-hidden VJP contribution;
- LM-head row-gradient wave;
- compact observability reduction;

then releases the bounded transient wave.

The existing R23/R24 backend math and vocab-range authority are reused. Current V5 yields three backward vocab waves, but the count is runtime-derived.

LM-head remains one logical gradient tensor although its physical gradient is streamed in vocab shards.

## Final RMSNorm backward

The accumulated LM-head input adjoint is applied to the retained R2C final-RMSNorm tape. R2D produces:

- `dHidden22`;
- logical gradient authority for `model.norm.weight`.

No final hidden replay or host payload bridge is admitted.

## Layer-boundary activation policy

R2D does not retain every attention/MLP intermediate for all 22 layers. When R2D is requested, R2B retains only canonical layer-boundary hidden states `hidden0..hidden22` on the same device.

Intermediate Q/K/V, attention, RMS, Gate/Up/SwiGLU/Down values are reconstructed deterministically per reverse layer from the corresponding boundary hidden plus the exact production weight wave.

This avoids full decoder-intermediate tape residency and avoids O(L^2) prefix replay.

## Reverse decoder Atlas execution

Decoder backward executes exactly:

```text
layer21
layer20
...
layer1
layer0
```

For each layer, the exact production Atlas weight group is re-admitted, the local forward intermediates are recomputed using the same production semantics, and existing backend/model-core VJP authorities are used for RMSNorm, linear, SwiGLU, RoPE and live attention backward.

Layer0 reuses the existing split Wave00/Wave01 production block authority and requires a complete nine-role decoder block before backward.

No second GPU device, second queue, generic attention-backward fallback or full-model preload is admitted.

## Tail zero-gradient forensic separation

Layer20/21 physical zero weights are not repaired or skipped.

R2D records separately:

- parameter-gradient nonzero role count;
- input hidden-adjoint nonzero count;
- adjoint finite status.

Possible classifications include zero parameter gradient with live residual adjoint. Layer20/21 parameter gradient nonzero is not a PASS requirement.

What is required is finite backward propagation to layer0 and at least one nonzero real-gradient element globally.

## Logical gradient authority

Current V5 trainable logical gradient coverage is:

```text
embedding.weight        1
decoder 22 x 9        198
model.norm.weight       1
lm_head.weight          1
-------------------------
total                  201
```

R2D requires exactly 201 logical gradient authorities with no missing or duplicate entries. A fully zero gradient tensor is still present and valid.

Embedding gradient may use a sparse physical representation over touched token rows while retaining one logical dense parameter-gradient identity. Duplicate token contributions must be reduced deterministically rather than through unordered floating atomic scatter.

## Gradient observability

Each logical parameter gradient receives compact evidence including parameter identity, role/layer, logical shape, finite/nonfinite counts, exact-zero/nonzero counts, max-absolute value, sum-of-squares and L2 norm.

Raw production gradient payload readback is prohibited. Compact reduction readbacks are admitted only as observability evidence.

Global raw-gradient observability publishes total nonzero element count, global L2 and max-absolute value. These values are not used to modify gradients in R2D.

## Authority ceiling

R2D must preserve:

```text
gradient_clip_applied = 0
gradient_rescale_applied = 0
optimizer_candidate_count = 0
optimizer_step_count = 0
optimizer_commit_count = 0
weight_mutation = 0
checkpoint_write = 0
r1j_real_export_event_observed = 0
```

R2D is an execution and observability frontier, not a training commit frontier.

## Receipt architecture

R2D uses 24 bounded receipt waves with <=8 fields per chunk, parallel chunk construction, deterministic sequential merge, duplicate-key fail closed, no giant final `json!` object and no recursion-limit workaround.

Per-parameter gradients and per-layer reverse receipts are streamed as bounded JSONL evidence rather than one monolithic object.

## Structural gate

Exactly 48 R2D contract gates are integrated:

```text
--require-bt-wgsl-r27r1j-r2d-contract-001
...
--require-bt-wgsl-r27r1j-r2d-contract-048
```

At least 72 semantic/negative canaries cover parent absence, stale loss authority, full logits/dLogits, vocab gaps/overlaps, missing VJP stages, reverse-order errors, missing layer checkpoints, device/queue drift, zero-gradient misclassification, nonfinite adjoints/gradients, missing logical gradients, forbidden clipping/optimizer/mutation/export, payload readback and receipt regressions.

Structural gate PASS proves wiring only; physical backward remains false in the structural context.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_REAL_LOSS_BACKWARD_ADMISSION_06C_R27_R1J_R2D
```

A physical PASS means the actual R2C real mean NLL and loss tape were consumed on the same device/queue, bounded LM-head VJP and final RMSNorm backward completed, all 22 decoder layers executed in reverse production order, embedding backward completed, all 201 logical gradient authorities were resolved with finite compact evidence, and at least one real-gradient element was nonzero while optimizer, mutation and checkpoint authority remained closed.

## Successful terminal HOLD

```text
HOLD_ASH_BASETRAIN_R1J_R2D_REAL_LOSS_BACKWARD_COMPLETE_REAL_GRADIENT_WAVE_AUTHORITY_READY_OPTIMIZER_NOT_YET_ADMITTED
```

A nonzero process exit caused solely by this typed HOLD remains the intended authority boundary.

## Next frontier

The next frontier is R2E gradient/optimizer commit admission. It may consume R2D gradient waves to admit clipping policy, optimizer state, update candidates and atomic training commit. Checkpoint export remains a later separate frontier.