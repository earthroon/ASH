# SFT-GPU-8D Compile Result

`cargo` / `rustc` were not available in the sandbox used for this bake, so compile/runtime execution could not be performed here.

Run in the project environment:

```powershell
cargo check -p lora_train
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1b_native_dump.json 1
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json 1
```
