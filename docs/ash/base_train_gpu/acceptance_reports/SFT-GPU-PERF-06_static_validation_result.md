# SFT-GPU-PERF-06 Static Validation Result

## Files checked

- crates/lora_train/src/batch_parallel_vocab_tile_pass2_grad.rs
- crates/lora_train/tests/batch_parallel_vocab_tile_pass2_grad.rs
- crates/lora_train/src/lib.rs

## Static checks

- file existence: PASS
- lib.rs module export: PASS
- public API export: PASS
- acceptance report: PASS
- bake report: PASS
- brace/bracket balance: PASS

## Cargo test attempt

Command:

```bash
cargo test -p lora_train --test batch_parallel_vocab_tile_pass2_grad -- --nocapture
```

Result:

```txt
bash: line 2: cargo: command not found
```

Native Rust tests were not executed because cargo/rustc are unavailable in this container.
