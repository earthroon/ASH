# Commit 16O-16V Static Verify

## Checked

- `StandardInferRequest` struct and active Rust constructors include:
  - `disable_native_structure_routing`
  - `disable_native_text_density`
  - `disable_native_gpu_penalty`
- `StandardInferResult` active constructors include:
  - `tail_decode_probe`
  - `tokenizer_checkpoint_probe`
  - `native_aux_probe`
- Python probe scripts compile with `python3 -m py_compile`.
- `scripts/commit_16q_decode_ids.py --ids 29035,13032` resolves:
  - `▁걱정이네`
  - `▁나오거든요`
  - `걱정이네 나오거든요`
- `infer_debug/commit_16r_16t_16u_matrix.jsonl` generated 17 sealed matrix rows.
- `infer_debug/commit_16s_spec_vocab_scan.json` confirms bundled tokenizer manifest vocab is `48259` while all bundled `specs/model_spec*.toml` vocab sizes are larger.

## Not checked

- Rust compile was not run because this container has no `cargo` or `rustfmt` binary.
- Native inference was not executed because no runnable Rust toolchain/runtime command is available in this environment.
- Checkpoint tensor shape alignment could not be fully verified because no `.safetensors` checkpoint was found inside this snapshot.
