# SFT-GPU-7 Compile / Runtime Result

Status: **NOT RUN IN SANDBOX**

The current sandbox does not provide `cargo`, `rustc`, or a WGPU runtime device, so Rust compile and runtime execution could not be performed here.

Run in the project environment:

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

Expected SFT-GPU-7 logs:

```txt
[lora_train][acceptance] running one-shot direct-line acceptance
[lora_train][generation_hygiene] prompts=... pass_count=... fail_count=... warnings=... pass=...
[lora_train][acceptance] status=PASS gates=config:true,sft_mask:true,gpu_training:true,artifact:true,runtime_delta:true,generation_hygiene:true
```

Expected SFT-GPU-7 outputs:

```txt
workspace/lora_runs/<run_name>/acceptance/direct_line_acceptance.json
workspace/lora_runs/<run_name>/acceptance/direct_line_acceptance.md
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/generation_hygiene_report.json
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/generation_hygiene_report.md
```
