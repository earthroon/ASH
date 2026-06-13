# After SFT-GPU-RUN-10A1

1. Re-run `cargo test -p lora_train --test sft_gpu_hidden_source_manifest_binding -- --nocapture`.
2. Run native dump config to create the feature store manifest.
3. Run train config again and verify `hidden_source_guard` no longer fails on missing binding.
4. If digest mismatch appears, proceed to `SFT-GPU-RUN-10B — A-SFT Hidden Source Digest Hard Seal / Dataset-Manifest Parity Gate`.
