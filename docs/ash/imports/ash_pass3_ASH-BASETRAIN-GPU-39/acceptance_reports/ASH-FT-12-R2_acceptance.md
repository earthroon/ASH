# ASH-FT-12-R2 Acceptance

Expected command remains the same as FT-12/R1.

Expected PASS:

```txt
PASS_ASH_FT12_SHADOW_CANDIDATE_RUNTIME_BIND_DRYRUN_NO_DECODE_NO_GENERATION
```

Acceptance checks:

- `--worker-stack-mb` is parsed into `AshFt12Config`.
- Binary spawns `ash-ft12-runtime-bind-dryrun` worker thread.
- Worker stack size is derived from `worker_stack_mb` with a 16MB minimum.
- Existing no-decode/no-generation/no-runtime-default guards remain unchanged.
