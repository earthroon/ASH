# SFT-GPU-8E Compile Result

Compile was not executed in this sandbox because cargo/rustc is unavailable.

Recommended command:

```powershell
cargo check -p lora_train
```

Native dump smoke:

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1b_native_dump.json 1
```

Expected logs include:

```txt
[lora_train][a_sft_dump] strategy=atlas_token_grouped ...
[lora_train][a_sft_dump] teacher_loaded_once=true ...
[lora_train][a_sft_dump][group 0] examples=... tokens=... max_seq=...
[lora_train][a_sft_dump][group 0] timing ...
[lora_train][a_sft_dump] complete groups=... batches=... teacher_load_count=1 ...
```
