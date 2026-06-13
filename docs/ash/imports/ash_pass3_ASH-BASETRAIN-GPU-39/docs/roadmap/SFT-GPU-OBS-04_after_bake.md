# SFT-GPU-OBS-04 After Bake Roadmap

## Completed SSOT

SFT-GPU-OBS-04 adds operator review receipt intake on top of the OBS-03 attention queue.
It accepts an explicit operator receipt for a source review item, validates the queue/item/target/digest relationship, and appends a decision ledger event.

## Still closed

- action apply
- current pointer update
- rollback execution
- demotion apply
- quarantine apply
- registry mutation
- lifecycle mutation
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- CPU fallback success approval
- textureSample / sampler / normalized UV weight fetch approval

## Next recommended patch

SFT-GPU-OBS-05 — Operator Decision to Action Candidate Bridge / No-Apply Handoff Seal

Purpose:
Convert accepted OBS-04 decisions into action candidates that can later be consumed by an explicit RUN-13-style apply gate.
This remains no-apply by default: it prepares candidates and validates mapping, but does not execute rollback, demotion, quarantine, fallback activation, or pointer switch.

## Verification commands

```bash
cargo test -p ash_core sft_gpu_obs_04 -- --nocapture
cargo test -p lora_train gpu_health_review_receipt -- --nocapture
cargo test -p burn_webgpu_backend gpu_health_review_decision_signals -- --nocapture
cargo test -p ash_core sft_gpu_obs_03 -- --nocapture
cargo test -p ash_core sft_gpu_obs_02 -- --nocapture
cargo test -p ash_core sft_gpu_obs_01 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```

## Search pattern

```bash
rg "operator_review_receipt|review_decision|decision_ledger|attention_queue_decision|priority_downgrade" .
```
