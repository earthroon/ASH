# ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-FORWARD-WAVE-EXECUTION-ADMISSION-06C-R27-R1J-R2B

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-FORWARD-WAVE-EXECUTION-ADMISSION-06C-R27-R1J-R2B`
- Build revision: `bt-wgsl-atlas-runtime-forward-wave-execution-admission-06c-r27-r1j-r2b`
- Physical parent: R27-R1J-R2 physical `ResidencyHandoffReady`
- Plan authority parent: R27-R1J-R2A production Atlas plan materialization
- Forward scope: decoder layers 0..21 only
- Output authority: closed
- Loss/backward/optimizer/checkpoint export authority: closed
- Proof ledger: `HOLD`

## Objective

R2A has physically materialized and validated the production Atlas plan trio and R2 has physically admitted that exact plan/checkpoint tuple into the same-device AW01 residency coordinator. R2B advances exactly one authority boundary: decoder forward execution.

The successful R2B physical path consumes the production decoder waves and publishes the canonical final decoder hidden at `hidden_layer=22`. It does not execute the final RMSNorm, LM head, real loss, backward pass, optimizer or checkpoint export.

## Explicit admission

R2B adds:

```text
--admit-atlas-forward-wave-execution
--atlas-plan-materialization-receipt <PATH>
```

R2 route admission remains independently required:

```text
--admit-atlas-runtime-route
```

Forward admission without route admission fails closed. The R2A materialization receipt is also mandatory and may not be auto-discovered from the workspace.

R1J capture and R1J-R1 full-snapshot admission remain independent and are not required for R2B.

## Exact R2A binding

The explicit R2A receipt is reopened and matched against the live R2 context:

- checkpoint digest;
- tensor-group manifest digest;
- Atlas-group plan digest;
- sequential-load plan digest;
- R2A PASS token;
- R2A reproducibility PASS;
- recomputed production plan-set digest.

A modified checkpoint or any modified plan member fails closed. R2B does not mutate the plan set.

Current physical R2A authority:

```text
checkpoint digest = ad1edb55abef1466591a49d432a0cd24ba79a89f757fefd4d8fba492695ab092

tensor-group manifest = e08345879ff8eb1ac1dbbfcac9b09ad8e98357477d53d8b994eb9c9c99d9c6d9
atlas-group plan       = c596a12c55847aa612dbfdb0aa2e3df8149e2e2c52a0dcad94fecfbeb7607cca
sequential-load plan   = ed0ce3064e43a364c6cce74e92eec3399c2efdcb303535988d61173edcb0f3c2
plan set               = bb3786570bb3b1c2769f528752edd48d3ece3925aeb68065458988c134fa6b0c
```

## Production wave boundary

The current production plan contains 24 groups/waves:

```text
Wave 00  layer0 prefill bundle
Wave 01  layer0 decoder-tail bundle
Wave 02..22  layer1..layer21 decoder block bundles
Wave 23  output final bundle
```

R2B recognizes the whole schedule but may consume only decoder authority. The existing R2 seed residency supplies Wave00 for real embedding execution. Decoder layer execution then activates Wave01 through Wave22 sequentially. Wave23 `aw02.output.final_bundle` must exist but is explicitly deferred and must not be fetched or executed by R2B.

## Same-device runtime ownership

R2B reuses the exact R2 `ExistingDeviceBootstrap`, native WGPU device and queue. It does not create a second instance, adapter, device or queue.

The R2 admission function is split into a context-producing function and a receipt-publishing function so R2B may inherit the already verified AW00 transaction, AW01 coordinator, joined plan, native runtime handles, checkpoint identity and physical plan digests without rebuilding those authorities.

The legacy R2 behavior remains unchanged when the new forward flag is absent.

## AW01 forward-wave activation

`BaseTrainAtlasWave01ResidencyCoordinator` gains an explicit single-wave activation operation valid only from `ResidencyHandoffReady`.

For a requested production wave it:

1. resolves exactly one group from the joined production plan;
2. releases previous ring-slot ownership;
3. uploads and verifies the exact target-group slices using the existing bounded checkpoint reader and AW01 backend ring;
4. marks the target group `CurrentResident`;
5. preserves the coordinator state as `ResidencyHandoffReady` for the next sequential forward-wave transition.

No output-final wave is admitted in R2B.

## Real input authority

R2B uses one actual BaseTrain preflight batch from the existing dataset/tokenizer pipeline. It does not construct synthetic token IDs or a synthetic hidden state.

Token IDs, row-valid lengths and position IDs come from the same AW00 sequence authority already bound by R2.

Exactly one production forward batch is admitted in this frontier.

## Embedding and layer0

Wave00 residency is consumed through the existing production embedding executor:

```text
execute_base_train_atlas_wave_02_r6_r6_embedding_only
```

The resulting hidden is adopted onto the same Burn WGPU device without host hidden upload/readback.

Layer0 then activates Wave01 and materializes the full nine-role canonical decoder block from exact plan slices before layer0 forward is allowed. Partial layer0 publication is forbidden.

## Canonical decoder block authority

R2B reuses `DECODER_WEIGHT_REGISTRY_ORDER` as the single decoder-role owner. For each layer, all nine canonical tensors are resolved from the joined production plan and verified against their physical source-slice digests.

The physical tensor payload is read in bounded per-layer scope. R2B never materializes the whole checkpoint on the host or GPU and never performs a GPU weight payload readback.

Current AW01 schema owns one whole Atlas slice per tensor; R2B therefore rejects silent multi-slice tensor expansion rather than inventing a new runtime schema.

The actual decoder block is constructed with the established `build_r6_r6_actual_decoder_block` authority. No simplified or parallel decoder implementation is introduced.

## Actual production decoder forward

For every decoder layer 0 through 21, R2B executes the established split production body:

```text
input RMSNorm
Q/K/V projections
NeoX RoPE
Headwise Atlas preparation
shared Headwise W5/W6/W7 runtime attention
same-device context adoption
O projection
attention residual
post-attention RMSNorm
Gate / Up / SiLU-SwiGLU / Down
FFN residual
```

The live attention writer is bound through `BaseTrainLayerAttentionAuthoritySlot` and its shared-runtime lease before canonical context publication.

No reference replay or non-authoritative parity forward is inserted into the production R2B path.

## Sequential layer progression

Decoder layer count comes from the active model spec. For the current V5 model:

```text
decoder_layer_count = 22
```

R2B executes exactly layers 0..21 in order. The wave relation is deterministic:

```text
layer N -> production wave N+1
```

The output hidden from layer N becomes the sole input hidden for layer N+1. Re-embedding after layer0 is forbidden. No cross-layer forward overlap or all-layer weight preload is admitted in this frontier.

## Zero-weight physical truth

Layer20 and Layer21 are not skipped or repaired.

Current source truth remains:

```text
Layer20 projection zero/nonzero = 6 / 1
Layer21 projection zero/nonzero = 7 / 0
Layer20 RMS nonzero = 2
Layer21 RMS nonzero = 2
```

Numerically zero tensors are still physical tensors. R2B executes them as the checkpoint provides them. Neighbor-layer copying, random reinitialization, inferred replacement values and nonzero-output requirements are prohibited.

The causal origin of those zeros remains owned by the R1H/R1I/R1J forensic frontier, not R2B.

## Hidden publication and finite guard

Every layer output passes the existing same-device raw finite guard before the next hidden generation is accepted. NaN/Inf is a hard failure. Zero-valued results are observations, not automatic failure.

Full production hidden payload readback is prohibited. Only compact runtime evidence and receipts may leave the device.

Successful completion requires:

```text
decoder_execution_step_count = 22
hidden_layer_final = 22
final_decoder_hidden_ready = true
```

## Authority ceiling

R2B must retain:

```text
final RMSNorm forward = 0
LM-head forward = 0
canonical logits = 0
loss = 0
backward = 0
optimizer = 0
weight mutation = 0
checkpoint write = 0
checkpoint export = 0
output-final wave fetch = 0
```

R1J real export observation therefore remains zero in this frontier.

## Receipt architecture

Layer execution evidence is emitted as a streaming JSONL ledger instead of one giant layer array. The final R2B receipt uses the Pass88 bounded chunk-map pattern:

```text
19 semantic waves
-> <=8 fields per chunk
-> parallel chunk construction
-> sequential wave publication
-> deterministic merge
-> duplicate-key fail closed
```

No `#![recursion_limit]` workaround and no giant terminal `json!({...})` receipt are introduced.

Receipt waves:

```text
00 R2 physical parent
01 R2A plan-set binding
02 explicit forward admission
03 dataset/tokenizer batch authority
04 primary device/queue identity
05 layer0 seed residency
06 layer0 complete-block admission
07 layer0 execution
08 layers1-4 progression
09 layers5-8 progression
10 layers9-12 progression
11 layers13-16 progression
12 layers17-19 progression
13 layer20 physical-zero execution
14 layer21 physical-zero execution
15 final decoder hidden publication
16 runtime residency/generation health
17 mutation/fallback firewall
18 next output-frontier handoff
```

## Structural gate contract

Exactly 48 R2B contract gates are integrated into short, full, dedicated and resolved args:

```text
--require-bt-wgsl-r27r1j-r2b-contract-001
...
--require-bt-wgsl-r27r1j-r2b-contract-048
```

The structural gate requires at least 52 negative/semantic canaries and uses a non-physical gate context:

```text
physical_forward_pass = false
forward_admission_status = ATLAS_FORWARD_NOT_REQUESTED
final_decoder_hidden_ready = false
output_final_wave_admitted = false
```

Its PASS token proves contract integration, not production decoder execution.

## PASS semantics

`PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_FORWARD_WAVE_EXECUTION_ADMISSION_06C_R27_R1J_R2B` means the exact R2A production-plan/checkpoint authority has been bound to the physically admitted R2 same-device runtime and one real BaseTrain batch has progressed through all 22 canonical decoder layers with sequential Atlas wave activation to publish the finite canonical final decoder hidden at layer 22, without opening final-output, loss, backward, optimizer or checkpoint-export authority.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_FORWARD_WAVE_EXECUTION_ADMISSION_06C_R27_R1J_R2B
```

## Successful terminal HOLD

```text
HOLD_ASH_BASETRAIN_R1J_R2B_DECODER_FORWARD_COMPLETE_FINAL_OUTPUT_EXECUTION_NOT_YET_ADMITTED
```

This HOLD is an intentional authority boundary and may return a nonzero process exit until the next frontier explicitly opens final-output execution.

## Next frontier

The next authority is:

```text
ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-FINAL-OUTPUT-REAL-LOSS-ADMISSION-06C-R27-R1J-R2C
```

It may consume the R2B final decoder hidden and the deferred Wave23 output bundle to execute final RMSNorm, bounded LM-head vocab waves, real loss and loss-tape publication. Backward, optimizer and checkpoint export remain separate later frontiers.