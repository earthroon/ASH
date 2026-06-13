# QW-55A-RUNTIME-01 Acceptance

## PASS

- Failure stop module exists.
- Failure reason enum exists.
- Failure stop receipt builder exists.
- Silent recovery detector exists.
- Greedy/sampler/original-argmax/normal-stop recovery are false.
- Committed token is absent during failure stop.

## FAIL

- Selector failure uses greedy fallback.
- Selector failure returns to existing sampler.
- Selector failure is disguised as normal stop.
- Receipt or trace is missing.
