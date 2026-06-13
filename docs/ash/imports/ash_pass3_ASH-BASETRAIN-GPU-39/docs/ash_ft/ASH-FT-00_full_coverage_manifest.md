# ASH-FT-00 Full Coverage Manifest Notes

ASH-FT-00 is the first ASH-FT patch for full-coverage atlas fine-tuning.

The intent is not partial LoRA-only tuning and not one-shot full checkpoint loading. The intent is complete tensor coverage with bounded atlas grouping:

```txt
full checkpoint load: no
full tensor coverage: yes
training execution in FT-00: no
weight mutation in FT-00: no
future grouped fine-tune basis: yes
```

## Why this exists

A customized safetensors checkpoint needs a full trainable coverage map. If only embedding or lm_head is registered, later training can only tighten the shell. ASH-FT-00 registers every tensor family so future stages can tighten the full model body by region.

## Output contract

ASH-FT-00 writes three runtime files when executed locally:

```txt
artifacts/ash_ft/ash_ft00_full_coverage_manifest.json
artifacts/ash_ft/ash_ft00_atlas_group_plan.json
artifacts/ash_ft/ASH-FT-00_receipt.json
```

These are generated outputs and should not be included in baked patch zip files.

## Next patch

```txt
ASH-FT-01
Atlas Group Memory Budget Planner / Optimizer State Shard Estimate / No Tensor Load Seal
```
