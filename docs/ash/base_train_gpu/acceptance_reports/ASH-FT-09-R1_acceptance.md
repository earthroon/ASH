# ASH-FT-09-R1 Acceptance

## PASS criteria

- `ash_ft09_single_group_shadow_candidate_write_dryrun.rs` imports `AshFt08IntegrityReceipt`.
- No reference remains to `AshFt08DeltaPacketIntegrityReceipt`.
- FT-09 expected PASS string remains unchanged.
- Runtime artifact JSON files are not packaged.
- `target/` build output is not packaged.

## Expected PASS

```text
PASS_ASH_FT09_SINGLE_GROUP_SHADOW_CANDIDATE_WRITE_DRYRUN_NO_RUNTIME_DEFAULT_APPLY
```
