# QW-53D Roadmap

## Position in QWave loop-control chain

1. QW-53A captures real runtime TopK/repeat-attractor traces.
2. QW-53B provides explicit safe sampled decode, without changing defaults.
3. QW-53C converts QWave/repeat evidence into `LoopRiskSignal` records.
4. QW-53D converts High/Critical `LoopRiskSignal` records into finite soft-demotion decisions.

## What this patch intentionally does not do

- It does not hard-ban tokens.
- It does not remove candidates.
- It does not mask logits.
- It does not alter model or LoRA weights.
- It does not enable runtime apply by default.

## Recommended local validation order

```bash
cargo test -p runtime qw53d
cargo test -p model_core qw53d

cargo run -p runtime --bin qw53d_soft_demotion_probe -- . \
  --input workspace/policy/qw53c_loop_risk_signal_candidates.jsonl \
  --output workspace/policy/qw53d_soft_demotion_decisions.jsonl \
  --mode shadow

cargo run -p model_core --bin qw53d_soft_demotion_audit_validate -- . \
  --input workspace/policy/qw53d_soft_demotion_decisions.jsonl \
  --output workspace/trace/qw53d_soft_demotion_audit_validation.json
```

## Next patch

`QW-53E — Shadow Demotion Replay / Repeat Escape Evidence Comparison Seal`
