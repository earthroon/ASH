# 16AI-QW-38G-R6A-SALAD-02 Acceptance

## Static Acceptance
- module exists: PASS
- lib registration: PASS
- sampler parity hook: PASS
- observe-only contract: PASS
- action execution forbidden: PASS

## Runtime Acceptance
Not run in this container. Execute in a Rust-enabled environment:

```bash
ASH_SAMPLER_PARITY=probe \
ASH_SAMPLER05_PARITY=receipt \
ASH_DECODE03A_ENTROPY=receipt \
ASH_DECODE03B_PCI=receipt \
ASH_DECODE03C_SHADOW=receipt \
ASH_DECODE03D_CONTROLLED_ENABLE=true \
ASH_DECODE03D_MODE=controlled \
ASH_DECODE03D_BEHAVIOR_CHANGE_ALLOWED=true \
ASH_SALAD02_DETECTOR=receipt \
ASH_SALAD02_DETECTOR_ONLY=true \
ASH_SALAD02_RECEIPT=workspace/salad02_steps.jsonl \
ASH_SALAD02_SUMMARY=workspace/salad02_summary.json
```

## Required Runtime Conditions
- `behavior_change` remains false in every SALAD-02 step.
- `detector_only` remains true.
- `action_executed` remains false.
- `salad_score` is clamped to `[0.0, 1.0]`.
- HIGH/CRITICAL findings create candidates only; no rollback/safe-stop is executed in SALAD-02.
