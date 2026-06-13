# QW-53B Roadmap Note

## Position in chain

```txt
QW-53A: real runtime top-k / repeat attractor trace
QW-53B: explicit subtitle-safe sampled decode profile
QW-53C: LoopRiskSignal bridge
QW-53D: candidate soft demotion
```

## What this patch changes

- Adds Rust decode profile registry/materializer for `subtitle_safe_sampled_v1`.
- Adds no-greedy-default-trap invariant.
- Adds runtime receipt writer.
- Adds model_core receipt validator.
- Adds tests for explicit enable, default preservation, no QWave apply, and no greedy trap.

## What this patch intentionally does not change

- Default unset decode remains unchanged.
- Greedy explicit profile remains possible.
- QWave still does not apply to token selection.
- No token hard ban is introduced.

## Next patch

`QW-53C — QWave LoopRiskSignal Bridge / Trace To Candidate Policy Seal`
