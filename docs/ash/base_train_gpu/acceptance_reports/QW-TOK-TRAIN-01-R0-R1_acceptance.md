# QW-TOK-TRAIN-01-R0-R1 Acceptance

## Status

PARTIAL_STATIC_PATCH_READY

## Confirmed in bake

- Source-level serialization repair applied.
- Report-facing focus token strings converted to ASCII-safe `escape_debug()` output.
- No training execution path opened.
- No checkpoint write path opened.

## Pending local proof

Run the TRAIN-01 dry-run locally and verify:

```powershell
$report = Get-Content ".\artifacts\qw_tok_train01_embedding_lmhead_atlas_adaptation_report.json" -Raw | ConvertFrom-Json
$report.status
$report.failures
```

Expected:

```txt
PASS_QW_TOK_TRAIN01_DRY_RUN_PLAN_ONLY
failures = []
```
