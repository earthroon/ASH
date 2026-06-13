# SFT-GPU-8 Compile Result

## Status

NOT RUN in this sandbox.

## Reason

`cargo` and `rustc` were not available in the execution environment used to bake this patch.

## User-side command

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected SFT-GPU-8 logs

```txt
[lora_train][quality_eval] summary samples=... fail=... warnings=... text_changed=... report=...
```

## Expected files

```txt
workspace/lora_runs/<run_name>/eval/quality_fixture_pack_ko.json
workspace/lora_runs/<run_name>/eval/base_vs_lora_samples.json
workspace/lora_runs/<run_name>/eval/base_vs_lora_samples.md
workspace/lora_runs/<run_name>/eval/quality_eval_summary.json
workspace/lora_runs/<run_name>/eval/quality_eval_summary.md
```
