# ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-FINAL-OUTPUT-REAL-LOSS-ADMISSION-06C-R27-R1J-R2C

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATLAS-RUNTIME-FINAL-OUTPUT-REAL-LOSS-ADMISSION-06C-R27-R1J-R2C`
- Build revision: `bt-wgsl-atlas-runtime-final-output-real-loss-admission-06c-r27-r1j-r2c`
- Physical parent: R27-R1J-R2B production decoder forward physical PASS
- Plan authority parent: R27-R1J-R2A production Atlas plan materialization
- Input authority: `FinalDecoderHiddenReady`, current V5 `hidden_layer=22`
- Output authority: `RealLossReady` and `LossTapeReady`
- Backward / optimizer / weight mutation / checkpoint export: closed
- Proof ledger: `HOLD`

## Objective

R2C advances exactly one authority boundary after the physically proven R2B decoder forward. The same process and same WGPU device/queue retain the canonical layer-22 final decoder hidden. R2C then admits only production Wave23, `aw02.output.final_bundle`, executes final RMSNorm, performs bounded LM-head vocab projection with the existing R23 stable streaming loss authority, publishes real next-token mean NLL and a backward-ready loss tape, then stops before backward.

R2C does not replay decoder forward, persist/reload hidden through the host, create a second model, run optimizer logic, mutate weights, or export a checkpoint.

## Explicit authority

R2C adds:

```text
--admit-atlas-final-output-real-loss
```

Physical execution requires the full explicit chain:

```text
--admit-atlas-runtime-route
--admit-atlas-forward-wave-execution
--admit-atlas-final-output-real-loss
```

The existing R2A materialization receipt remains mandatory through the R2B parent contract. R1J capture and full-snapshot admission remain independent.

## R2B same-process context handoff

R2B is refactored without changing standalone semantics so its physical executor can return a child context containing:

- R2 route context and AW01 coordinator;
- exact checkpoint and production-plan authority;
- canonical BaseTrain sequence authority;
- final decoder hidden on the same Burn WGPU device;
- hidden layer/generation and final-hidden authority digest;
- R2B physical receipt.

Standalone R2B still emits its existing PASS followed by `HOLD_ASH_BASETRAIN_R1J_R2B_DECODER_FORWARD_COMPLETE_FINAL_OUTPUT_EXECUTION_NOT_YET_ADMITTED`. When R2C is explicitly requested, the same context is consumed directly instead of persisting hidden to CPU or disk.

## Exact Wave23 authority

The production plan contains 24 sequential waves. R2C admits exactly:

```text
wave_order = 23
group_id   = aw02.output.final_bundle
```

The group is resolved from the joined production plan, not guessed from file order, size, names, or workspace discovery.

The transition is completion-bound:

```text
Layer21 forward complete
-> final decoder hidden committed
-> layer21 weight lease released
-> decoder residency vacant
-> Wave23 staging
-> Wave23 atomic residency adoption
```

Decoder/output weight-residency overlap is not admitted in this revision.

## Output tensor authority

Current V5 output-final authority requires `model.norm.weight` and the untied `lm_head.weight`. Binding mode is explicit; R2C does not infer tied/untied semantics from tensor shape and does not synthesize missing bias or output tensors.

Wave23 resident views are validated for group identity, dtype, shape, source digest, runtime holder and residency generation.

Current V5 is explicitly untied. A tied configuration is fail-closed until the production output-plan/runtime contract explicitly admits it.

## Final RMSNorm

R2C consumes the exact R2B final decoder hidden and uses the existing model-core final RMSNorm materialization/forward authority. No decoder replay or final-hidden host reload is allowed.

`forward_with_tape` retains the final RMSNorm inverse-RMS and gamma lineage for the later backward frontier. The normalized hidden is bridged as a same-device raw lease, guarded for non-finite values, and published as the canonical LM-head input.

Successful R2C requires exactly one final RMSNorm forward.

## LM-head Atlas residency and bounded vocab views

Wave23 owns the full LM-head payload as Atlas transport residency. R2C does not create a second full LM-head GPU buffer.

The existing AW01 resident Atlas buffer is borrowed directly through offset/size raw views for bounded vocab row ranges. R2C does not reread/upload the complete LM-head from checkpoint for each vocab wave.

The vocab partition is derived from model vocab size, hidden width and bounded R23-compatible view budget. Current V5 geometry yields a 16,384-row compatibility wave size and three vocab waves, but wave count is runtime-derived rather than hardcoded.

Each view is an exact row-major subrange of the resident `lm_head.weight`. Vocab coverage must have zero gaps and zero overlaps.

## Existing R23 real-loss authority reuse

R2C directly reuses the existing `burn_webgpu_backend` R23 authorities:

- `R23LossAccumulator`;
- `validate_r23_vocab_wave_ranges`;
- same-pass target-logit capture;
- active-row-only projection;
- deterministic stable streaming logsumexp;
- mean NLL exactly once;
- compact status/loss scalar readback;
- R23 synthetic semantic oracles.

No second softmax/loss implementation is introduced.

## Sequence and target authority

The same BaseTrain batch and canonical R2B sequence authority are retained. For each valid token position q, the canonical target is q+1 only when q+1 remains inside the valid prefix.

Padding never owns loss. The terminal valid token receives no fabricated EOS target. Target IDs are consumed directly from the canonical token sequence with no decode/re-encode path.

Model and tokenizer vocab sizes must match exactly. Current V5 authority is 48,259.

## Memory and payload rules

R2C keeps:

```text
full_vocab_logits_surface = 0
target_logit_second_forward = 0
global_float_atomic = 0
production_logit_payload_readback = 0
production_hidden_payload_readback = 0
production_weight_payload_readback = 0
second_full_lm_head_buffer_materialization = 0
```

Only bounded transient logits for the active rows of the current vocab view, compact status words and compact final loss scalars are admitted.

## Real-loss and loss-tape publication

Successful execution requires:

- every target found exactly once;
- no vocab gap or overlap;
- no non-finite logits or loss values;
- nonzero active loss-row count;
- stable logsumexp completion;
- loss mean applied exactly once.

R2C publishes `real_loss_authority=1`, `final_loss_authority=1` and `loss_tape_authority=1`.

The loss tape retains the sequence authority digest, pre-final hidden raw lease, final RMSNorm inverse-RMS/gamma/normalized-hidden leases, active-row identities, target IDs, logZ/NLL/loss-value leases, loss-sum/loss-mean bits and a real-loss authority digest. Full logits are never stored in the tape.

## Authority ceiling

R2C must preserve:

```text
backward_count = 0
gradient_publication = 0
optimizer_count = 0
weight_mutation = 0
checkpoint_write = 0
r1j_real_export_event_observed = 0
```

R2C does not perform LM-head backward, final RMSNorm backward, decoder backward, gradient-atlas publication, clipping, Adam, production weight commit or checkpoint export.

## Receipt architecture

R2C uses the established bounded receipt pattern:

```text
20 semantic waves
-> <=8 fields per chunk
-> parallel chunk construction
-> deterministic sequential merge
-> duplicate-key fail closed
```

No giant terminal `json!({...})` object and no recursion-limit workaround are admitted. Vocab execution evidence is streamed separately as bounded JSONL records.

## Structural gate

Exactly 48 R2C contract gates are integrated:

```text
--require-bt-wgsl-r27r1j-r2c-contract-001
...
--require-bt-wgsl-r27r1j-r2c-contract-048
```

The structural gate carries at least 64 semantic/negative canaries and deliberately reports `physical_real_loss_pass=false`, `ATLAS_FINAL_OUTPUT_NOT_REQUESTED`, `real_loss_authority=false`, and `loss_tape_authority=false`. Structural PASS proves wiring only, not physical loss execution.

## PASS

```text
PASS_ASH_BASETRAIN_BT_WGSL_ATLAS_RUNTIME_FINAL_OUTPUT_REAL_LOSS_ADMISSION_06C_R27_R1J_R2C
```

This PASS means the exact physical R2B final decoder hidden and exact R2A Wave23 production output authority were consumed on the same device/queue; final RMSNorm and bounded resident-Atlas LM-head vocab projection completed; the existing R23 streaming logsumexp/target-capture authority produced a finite real next-token mean loss; and the loss tape was published without opening backward, optimizer, mutation or checkpoint-export authority.

## Successful terminal HOLD

```text
HOLD_ASH_BASETRAIN_R1J_R2C_REAL_LOSS_AND_LOSS_TAPE_READY_BACKWARD_NOT_YET_ADMITTED
```

A nonzero process exit caused only by this typed HOLD remains an intentional authority boundary.

## Next frontier

The next frontier is R2D real-loss backward admission. It may consume the R2C loss tape, Wave23 output authority and retained R2B decoder-forward tapes to perform logit VJP, final RMSNorm backward and reverse decoder-wave backward toward the canonical real-gradient atlas. Optimizer and checkpoint export remain separate later frontiers.