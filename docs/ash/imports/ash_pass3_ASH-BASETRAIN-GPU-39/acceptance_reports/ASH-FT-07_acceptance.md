# ASH-FT-07 Acceptance

Status before local run: `PENDING_RUNTIME`

Expected PASS string:

```txt
PASS_ASH_FT07_SINGLE_GROUP_OPTIMIZER_DRYRUN_NO_CANDIDATE_WRITE
```

Runtime command writes only:

```txt
artifacts/ash_ft/ash_ft07_optimizer_dryrun_plan.json
artifacts/ash_ft/ash_ft07_optimizer_state_preview.json
artifacts/ash_ft/ash_ft07_delta_preview_receipt.json
artifacts/ash_ft/ash_ft07_weight_after_preview_receipt.json
artifacts/ash_ft/ASH-FT-07_receipt.json
```

Packaging rule:

```txt
Do not package artifacts/ash_ft/*.json runtime outputs.
Only package code, docs, specs, acceptance reports, and artifacts_templates/*.template.json.
```
