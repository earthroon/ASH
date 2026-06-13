# 16AI-QW-30 — QWave Runtime Apply Gate / Explicit Operator-Controlled Activation Seal

## Patch
- Base ZIP: `ash_pass3_16AI-QW-29_qwave_runtime_shadow_eval_baked.zip`
- New module: `crates/lora_train/src/qwave_runtime_apply_gate.rs`
- New receipt SSOT: `QWaveRuntimeApplyGateReceipt`

## Input SSOT
- QW-29 Runtime Shadow Eval Receipt: consumed
- QW-28 Training Rollback Ledger Receipt: referenced
- QW-27 Training Mode Promotion Gate Receipt: referenced
- QW-26 Long-run SFT Telemetry Receipt: referenced
- QW-25 Korean Minimal Pair Eval Receipt: referenced
- QW-24 Conditioned SFT Smoke Receipt: referenced
- QW-23 Train Candidate Receipt: referenced
- QW-22 Projection Dry-run Receipt: referenced
- QW-21 LoRA Conditioning Candidate Receipt: referenced
- QW-20 Runtime Routing Hint Candidate Receipt: referenced
- QW-19/QW-18/QW-17/QW-16/QW-12 receipt lineage: referenced
- QW-13/QW-14/QW-15 metadata receipt lineage: referenced

## Guards
- Shadow eval no-regression source guard: implemented
- Shadow unsafe/regressed source block: implemented
- Operator request guard: implemented
- Operator acknowledgement guard: implemented
- Feature flag activation plan guard: implemented
- Silent enable / auto enable guard: implemented
- Rollback pointer ready guard: implemented
- Runtime telemetry activation plan guard: implemented
- Activation scope guard: implemented with safe enum only
- Runtime gate approval guard: implemented
- No mutation guard: implemented

## Generated artifacts
- `QWaveRuntimeApplyEligibilityReport`
- `QWaveRuntimeApplyQueueEntry`
- `QWaveRuntimeApplyGateManifest`
- `QWaveRuntimeApplyGateReceipt`

## Mutation boundary
Blocked:
- silent enable
- auto runtime apply
- production sampler mutation
- temperature / top_p / top_k / repetition penalty mutation
- logit bias / direct logit mutation
- backend switch
- current / artifact / adapter pointer mutation
- base model mutation
- adapter / LoRA A/B mutation
- token / vocab / embedding mutation
- rollback execution
- training apply / training mode apply
- sample weight / curriculum / batch reorder / loss rewrite
- global gradient scaling
- optimizer / scheduler mutation outside sandbox

## Validation
- Static validation: PASS
- Native Rust test: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Completion
QW-30 is apply-gate-only. It creates an explicit operator-controlled runtime activation gate but does not enable runtime, mutate sampler/logits, switch backend, or change current/artifact/adapter pointers.
