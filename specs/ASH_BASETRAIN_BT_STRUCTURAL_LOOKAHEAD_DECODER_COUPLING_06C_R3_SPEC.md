# ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R3

## Full LM-Head Contiguous Materialization Retirement / Exact 395337728-Byte Failure Binding / Post-Layer Structural Decoder Gradient / Atlas-Wave LM Backward Deferred Seal

> Parent: `BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R2`
>
> Failure evidence: CubeCL allocation panic at `395337728` bytes
>
> Repair class: frozen LM objective residency/gradient boundary
>
> Proof ledger: `HOLD`

## 1. Root cause

The failed allocation is exactly:

```text
48259 vocab rows * 2048 hidden * 4 f32 bytes = 395337728 bytes
```

R2 constructed the complete frozen `lm_head.weight` as one `TrainingBackend` tensor. That violates the already established ASH LM-head vocabulary-row Atlas-Wave residency rule and can fail even when aggregate VRAM is sufficient because CubeCL requires one contiguous allocation.

## 2. R3 prohibition

R3 retires all 06C call edges that can create:

```text
Tensor<TrainingBackend,2>[48259,2048]
Param<lm_head.weight> full GPU materialization
full frozen LM-head Autodiff tensor
```

Required runtime receipt:

```text
full_lm_head_gpu_materialization_count=0
full_lm_head_gpu_materialization_bytes=0
observed_forbidden_contiguous_lm_head_bytes=395337728
```

## 3. Decoder gradient preservation

R3 does not refreeze the selected decoder.

Each selected layer has two uses of the shared structural head bank:

```text
pre-layer prediction
  -> TensorCube / deltaQ / structural gate / shared-KV coupled layer execution

post-layer prediction
  -> R06A structural auxiliary loss
  -> selected decoder backward
```

The post-layer structural prediction is not injected back into the same layer. It is supervision only, so there is no cyclic forward dependency.

Required:

```text
post_layer_structural_decoder_gradient=1
selected_decoder_gradient_nonzero_count > 0
structural_head_gradient_nonzero_count > 0
structural_gate_gradient_nonzero_count > 0
```

## 4. LM objective status

R3 does not silently replace canonical full-vocabulary LM loss with sampled logits, partial vocabulary, CPU softmax, or a fake scalar.

The canonical LM objective gradient is explicitly:

```text
HOLD_LM_VOCAB_ROW_ATLAS_WAVE_BACKWARD_NOT_YET_ADMITTED
```

Current physical profile therefore requires:

```text
lambda_lm = 0
lm_objective_gradient_count = 0
```

The frozen LM-head parameter authority remains unchanged and cannot enter the optimizer/update map.

A later patch must implement exact vocab-row Atlas-Wave LM backward before `lambda_lm > 0` can be re-admitted.

## 5. Structural objective

The first 06C coupled step remains physically meaningful because the selected decoder is supervised by post-layer H1/H2/H3/H4 structural targets.

```text
L_total = lambda_struct * L_struct_post_layer
```

R06A ground truth remains loss-only.

The predictions used for TensorCube injection remain pre-layer predictions, so no target or post-layer future result is fed into the current layer.

## 6. Preserved architecture

Unchanged from R2:

```text
16x16x4 TensorCube
H1/H2/H3/H4 horizon slabs
one canonical K/V per selected layer
zero branch KV caches/clones/authority
branch-local deltaQ and deltaC
zero-ground-truth forward injection
Atlas-Wave parallel parameter update map
DeltaK petrification state machine
shared-KV petrification immunity
zero direct logit prior
zero sampler/speculative decode authority
```

## 7. Response policy

Required true:

```text
--require-bt-struct-lookahead-zero-full-lm-head-materialization
--require-bt-struct-lookahead-postlayer-structural-decoder-gradient
--require-bt-struct-lookahead-lm-wave-backward-deferred
```

R2 `--require-bt-struct-lookahead-canonical-lm-loss` is retired from the R3 physical profile.

Required value:

```text
--bt-struct-lookahead-lambda-lm
0.0
```

## 8. Scope

R3 changes exactly:

```text
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

## 9. Next LM stage

Natural follow-up after physical R3 admission:

```text
BT-STRUCTURAL-LOOKAHEAD-LM-ATLAS-WAVE-BACKWARD-06C-LM1

Vocab-Row LM-Head Wave Plan /
No Full LM-Head GPU Materialization /
Exact Full-Vocab Normalizer /
Wave-Local Frozen Weight Residency /
Canonical dLogits /
Wave-Reduced dHidden /
Selected Decoder Gradient Injection /
No LM-Head Weight Gradient /
Zero Logit Payload Readback /
Atomic Gradient Merge Seal
```

Only after LM1 physical admission may `lambda_lm > 0` return to the coupled training objective.
