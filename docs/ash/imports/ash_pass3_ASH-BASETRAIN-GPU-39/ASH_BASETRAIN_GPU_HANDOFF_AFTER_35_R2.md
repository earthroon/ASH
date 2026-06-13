# ASH-BASETRAIN-GPU-35-R2 Handoff

## Status
- Patch: ASH-BASETRAIN-GPU-35-R2
- Default baked status: BLOCKED_MISSING_OPERATOR_MANIFEST_ENV
- Runtime GPU required: false
- Actual GPU buffer allocation in 35-R2: false
- Selected group weight load: false
- Backward: false
- Optimizer: false

## SSOT
- Source: ASH-BASETRAIN-GPU-35-R1A PASS
- Source triage digest: `6ae58278133af89a3ab6100d9f1eaf4ff056eddf809f3e820f2eb0b5a522f1d6`
- R2 materialization digest, default blocked route: `5089e283dc38d5826860f92c8b8e6176c827ef315e464fa43e8a991e5cb65fe3`

## Operator path
```powershell
$env:ASH_BASETRAIN_GPU_OPERATOR_SELECTED_GROUP_MANIFEST_PATH="D:\1111113232\DUST\1\ash_pass3\target\selected_atlas_group_slot_0_manifest.operator.json"
$env:ASH_BASETRAIN_GPU_SELECTED_GROUP_MANIFEST_PATH="D:\1111113232\DUST\1\ash_pass3\target\selected_atlas_group_slot_0_manifest.json"
```

## Next
- Materialized PASS: ASH-BASETRAIN-GPU-35-R1-RECHECK
- Blocked PASS: ASH-BASETRAIN-GPU-35-R2A
