# QW-TOK-FORGE-01-S0 Acceptance

## PASS criteria

- `tokenizer_v5_forge01_embed_lmhead_bootstrap.rs` exists.
- `qw_tok_forge01_embed_lmhead_bootstrap.rs` exists.
- Default checkpoint is `tokenizer_v5/artifacts/ash_v5_native_genesis.forge00.safetensors`.
- FORGE-01-S0 runtime guard rejects legacy TRAIN checkpoint/default fragments.
- S0 does not read checkpoint payloads.
- S0 does not write checkpoints.
- S0 does not train, backpropagate, create gradients, create optimizers, run GPU kernels, or decode.
- S0 writes the four S0 receipts.

## PARTIAL criteria

- Runtime files are created but local checkpoint/corpus probes are missing because the upload does not include large local artifacts.
- Cargo check is blocked by existing workspace unrelated issues.

## FAIL criteria

- Runtime default points to a legacy TRAIN/resized/rebound checkpoint.
- Patch identity remains `QW-TOK-TRAIN-*` in the new FORGE runtime.
- Checkpoint write executes during S0.
- Training, backward, optimizer, GPU kernel, or decode executes during S0.

## Current bake observation

This bake creates the FORGE namespace surface and static receipts. The uploaded zip does not include the 4.6GB FORGE-00 safetensors or the local training corpus, so existence checks for those files are intentionally deferred to the user's local workspace and to S1/S2.
