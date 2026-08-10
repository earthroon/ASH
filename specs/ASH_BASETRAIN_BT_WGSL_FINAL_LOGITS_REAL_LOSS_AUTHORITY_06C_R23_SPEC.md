# ASH-BASETRAIN-BT-WGSL-FINAL-LOGITS-REAL-LOSS-AUTHORITY-06C-R23

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-FINAL-LOGITS-REAL-LOSS-AUTHORITY-06C-R23`
- Build revision: `bt-wgsl-final-logits-real-loss-authority-06c-r23`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-G205D-ATOMIC-WEIGHT-OPTIMIZER-STATE-COMMIT-06C-R22`
- Parent code baseline: R22-R2 status-protocol repair
- Next consumer: R24 real-loss LM Head + Final RMSNorm backward
- Proof ledger: `HOLD`

## SSOT

R23 consumes the exact Final RMSNorm hidden already produced by the production forward path in 06B. R23 does not re-run the decoder or Final RMSNorm and does not use the R22 deterministic-fixture training-state root as a forward source. The retained Final RMSNorm raw GPU lease is read-only and remains pinned for R24.

Canonical next-token labels are derived directly from the runtime input-sequence authority by shift-by-one inside each valid prefix. Padding suffix positions and the terminal valid token have no loss contribution. No synthetic EOS, ignore-index default, text decode, or re-tokenization participates in label authority.

The manifest/checkpoint determines whether the LM Head is a tied embedding alias or a distinct `lm_head.weight`. Binding mode, source tensor identity, source dtype, optional `lm_head.bias`, vocabulary size, hidden width, and explicit identity logit-scale policy are sealed before execution. Tied/untied status is never inferred from shape, pointer equality, filenames, or value equality.

R23 streams LM Head rows by bounded vocabulary waves. Each wave decodes only its contiguous checkpoint row range, uploads only that decoded F32 wave to GPU, projects only loss-active hidden rows, and creates a transient `active_rows × wave_vocab_rows` logit scratch. No full `B×Q×V` or full active-row vocabulary logit surface is retained. The transient wave scratch is immediately reduced into per-row chunk max, exp-sum, and same-pass target logit, then discarded.

Per-row streaming LogSumExp state is merged in ascending vocabulary-range order using running-max rescaling. The first wave initializes the running state explicitly, without an infinite sentinel. After exact full-vocabulary coverage, the backend computes per-row `logZ`, next-token NLL, deterministic fixed-order loss sum, and one mean over active next-token rows. The canonical loss first exists as a device-local scalar; only compact loss/status scalars are read back for receipts. Production hidden, weight, and logit payload readback remain zero.

R23 publishes `real_loss_authority=1` and `final_loss_authority=1`, plus an R24 loss tape containing the exact final-hidden lineage, active-row map, target IDs, device-resident per-row LogZ, LM Head source authority, vocab-wave plan, and loss-policy identity. R23 does not execute dLogits, LM Head backward, Final RMSNorm backward, decoder backward, gradient publication, optimizer work, weight mutation, production training-state commit, or checkpoint persistence.

## Current physical target geometry

The current audit fixture is sealed as:

```text
batch_size=1
seq_len=32
valid_token_count=8
loss_active_slot_count=7
terminal_without_target_count=1
pad_loss_mask_count=24
synthetic_eos_target_count=0
```

Active source positions are 0..6 and targets are the canonical token IDs at positions 1..7. R06A H1 count is used only as a parity cross-check and never as label authority.

## LM Head source authority

For the current Llama checkpoint authority:

```text
vocab_size=48259
hidden_width=2048
```

Binding mode is runtime-derived from `tie_word_embeddings`:

```text
TIED_EMBEDDING  -> model.embed_tokens.weight + exact logical alias
UNTIED_LM_HEAD  -> lm_head.weight
```

If `lm_head.bias` exists, its presence and tensor identity are explicit and the full bias vector may remain resident because it is vocabulary-sized only; the large LM Head weight itself remains single-wave resident. The model config has no separate logit-scale field in this authority, therefore R23 seals an explicit identity logit-scale policy rather than a hidden temperature.

## Vocabulary-wave plan

Rows per wave are runtime-derived from:

- checkpoint source-row bytes,
- decoded F32 row bytes,
- C10 host transient budget,
- WGPU max storage-buffer binding size,
- active-row transient-logit storage cost,
- dispatch-dimension limits,
- and a no-full-weight cap.

The wave plan must contain more than one weight wave and its ranges must cover `[0, vocab_size)` exactly once with zero gap and zero overlap. Peak resident LM Head weight waves is one. There is no prefetch or cross-wave overlap in R23.

## WGSL loss pipeline

R23 adds four compute stages:

1. `base_train_r23_active_lm_head_projection.wgsl`
   - one invocation per active-row / vocab-row pair,
   - F32 dot product across hidden width,
   - optional bias,
   - explicit logit scale,
   - finite guard,
   - same-projection-pass target-logit capture,
   - transient wave logits only.

2. `base_train_r23_chunk_reduce.wgsl`
   - fixed 256-lane workgroup per active row,
   - deterministic chunk max,
   - deterministic `sum(exp(logit-max))`.

3. `base_train_r23_stream_merge.wgsl`
   - exact first-wave initialization,
   - running-max rescale merge,
   - one target capture across the complete vocabulary,
   - no global floating-point atomic reduction.

4. `base_train_r23_loss_finalize.wgsl`
   - validates target-found exactly once,
   - computes per-row LogZ and NLL,
   - sums NLL in fixed row order on device,
   - divides exactly once by active-row count,
   - writes loss sum and mean device scalars.

All R23 shaders use the canonical exponent-mask `finite_f32` predicate. `isFinite`, `isNan`, `isInf`, NaN clamp, Inf clamp, logit clipping, and loss clipping are prohibited.

## Status ABI

`R23StatusV1` is fixed as:

```text
0 = INCOMPLETE
1 = COMPLETE
2 = NONFINITE
3 = TARGET_MISSING
4 = TARGET_OUT_OF_RANGE
5 = WAVE_COVERAGE_FAILURE
```

Production success requires row status `1` for every active row and loss status `1`. Host-side target-range and wave-coverage validation is fail-closed before production authority.

## Synthetic semantic authority

Synthetic data proves math only and never becomes loss authority.

The small-vocab oracle uses multiple active rows, hidden width 4, vocab size 10, explicit bias, targets that land in the first/middle/last waves, and two distinct exact vocabulary partitions. GPU LogZ/NLL/mean are compared with an independent CPU-F64 full-vocabulary reference using oracle-only absolute `1e-6` or relative `1e-5` tolerance.

Five negative canaries are required:

1. target ID out of range,
2. vocabulary-wave gap,
3. vocabulary-wave overlap,
4. nonfinite projected logit with status 2,
5. target missing with status 3.

## Reproducibility

The live production loss pipeline runs twice from the same hidden, sequence, LM Head authority, bias authority, logit-scale policy, and vocabulary-wave plan. Loss-sum and loss-mean bits must match. Device-resident LogZ, NLL, and two-scalar loss buffers are compared through the existing exact GPU parity pipeline with zero tensor payload readback.

## R24 loss tape

R23 retains:

```text
sequence_authority_digest
final_hidden_raw_lease
final_hidden_authority_digest
lm_head_source_authority
vocab_wave_plan
active_rows
target_ids
logz_device_buffer
loss_values_device_buffer
loss_sum_bits
loss_mean_bits
loss_policy_digest
real_loss_authority_digest
```

Full logits are not retained. R24 must re-stream vocabulary waves to construct `softmax - one_hot(target)` from the retained LogZ and target map.

## Production boundaries

Required after R23:

```text
real_loss_authority=1
final_loss_authority=1
real_loss_backward_authority=0
production_training_state_authority=0

dlogits_dispatch=0
lm_head_backward=0
final_rmsnorm_backward=0
gradient_publication=0
optimizer=0
weight_mutation=0
checkpoint_write=0

production_hidden_payload_readback=0
production_weight_payload_readback=0
production_logit_payload_readback=0
full_vocab_logits_surface=0
```

## Expected physical summary

```text
r22_physical_parent=1
r22_fixture_root_consumed_as_forward_source=0
production_forward_hidden_lineage=1
final_rmsnorm_forward_authority=1
final_hidden_raw_borrow=1
final_hidden_batch=1
final_hidden_seq=32
final_hidden_width=2048
final_hidden_host_upload=0
final_hidden_payload_readback=0
final_hidden_mutation=0
sequence_authority_bound=1
valid_token_count=8
next_token_target_policy=1
loss_active_slot_count=7
terminal_without_target_count=1
pad_loss_mask_count=24
synthetic_eos_target_count=0
target_reencode_count=0
target_decode_search_count=0
model_vocab_size=48259
tokenizer_vocab_size=48259
model_tokenizer_vocab_exact_match=1
lm_head_binding_mode=<runtime>
lm_head_manifest_authority=1
lm_head_vocab_rows=48259
lm_head_hidden_width=2048
lm_head_bias_presence=<runtime>
logit_scale_policy=IDENTITY_LLAMA_CONFIG_AUTHORITY
label_smoothing=0
class_weighting=0
vocab_wave_loader=1
vocab_wave_size=<runtime>
vocab_wave_count=<runtime>
vocab_wave_gap=0
vocab_wave_overlap=0
peak_resident_lm_head_weight_waves=1
full_lm_head_host_materialization=0
full_lm_head_gpu_residency=0
lm_head_payload_readback=0
lm_head_weight_mutation=0
active_row_only_projection=1
full_vocab_logits_surface=0
production_logit_payload_readback=0
target_logit_same_pass_capture=1
target_logit_second_forward=0
stable_streaming_logsumexp=1
running_max_rescale_merge=1
global_float_atomic=0
target_found_count=7
target_missing_count=0
nonfinite_logit_count=0
per_token_nll_count=7
loss_sum=<runtime>
loss_mean=<runtime>
loss_mean_exactly_once=1
device_local_loss_scalar=1
compact_loss_scalar_readback=1
real_loss_authority=1
final_loss_authority=1
loss_tape_authority=1
loss_tape_active_rows=7
loss_tape_target_ids=7
loss_tape_logz_count=7
loss_tape_full_logits=0
status_abi=R23StatusV1
status_success_value=1
synthetic_small_vocab_cpu_f64_oracle=1
synthetic_streaming_logsumexp_oracle=1
synthetic_target_capture_oracle=1
synthetic_wave_partition_oracle=1
negative_canaries=5
production_hidden_payload_readback=0
production_weight_payload_readback=0
dlogits_dispatch=0
lm_head_backward=0
final_rmsnorm_backward=0
gradient_publication=0
optimizer=0
weight_mutation=0
checkpoint_write=0
production_training_state_authority=0
reproducibility_runs=2
reproducibility_match=1
r24_handoff_ready=1
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## Receipt Atlas

Nine deterministic waves:

```text
Wave 0  R22 parent / fixture isolation / exact Final RMSNorm hidden
Wave 1  canonical sequence / shift-by-one targets / pad+terminal mask
Wave 2  LM Head source / tied-or-untied / bias / logit-scale policy
Wave 3  vocab-wave plan / bounded single-wave residency
Wave 4  active-row projection / target capture / chunk statistics
Wave 5  streaming LogSumExp / NLL / loss scalar
Wave 6  real-loss authority / R24 loss tape / production readback boundary
Wave 7  synthetic F64 / partition / negative canaries / reproducibility
Wave 8  zero backward+optimizer / R24 handoff / PASS / proof ledger
```

The final atlas fails closed on duplicate global keys and reports `monolithic_final_json=0`.

## CLI gates

Exactly 112 R23 `--require-bt-wgsl-r23-*` gates are installed exact-once in runtime validation, short args, full args, and resolved-args repair input. The implementation list in `base_train_r23_final_logits_real_loss_authority.rs` is the canonical gate set for this revision.

## PASS seal

`PASS_ASH_BASETRAIN_BT_WGSL_FINAL_LOGITS_REAL_LOSS_AUTHORITY_06C_R23`

R23 ends with a physically computed, device-originated next-token cross-entropy loss and an R24-ready loss tape, but no real-loss gradient has yet been produced. Production training-state authority remains zero until the subsequent real-loss backward chain is physically admitted.
