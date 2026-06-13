# ASH-FT-01 Operator Notes

ASH-FT-01 turns the ASH-FT-00 full coverage map into a training budget table.

It does not read candidate tensor values. It only reads:

```txt
artifacts/ash_ft/ash_ft00_full_coverage_manifest.json
artifacts/ash_ft/ash_ft00_atlas_group_plan.json
```

The output tells the operator which atlas groups are GREEN, YELLOW, RED, or BLACK against the configured VRAM budget.

- GREEN: likely feasible under the configured budget.
- YELLOW: feasible but needs caution.
- RED: tile split strongly recommended.
- BLACK: not feasible as a full group; tile split and/or optimizer offload required.

The next natural patch after PASS is:

```txt
ASH-FT-02
Full Coverage Slice Read Probe / All Tensor Families / No GPU Upload Seal
```
