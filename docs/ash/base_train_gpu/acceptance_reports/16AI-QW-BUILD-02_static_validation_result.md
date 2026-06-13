# 16AI-QW-BUILD-02 Static Validation Result

## Result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE_IN_CONTAINER

## Checks

- tokenizer graph serialization shadowed helper fixed: PASS
- duplicate lib.rs re-export resolved via alias: PASS
- lm_head vocab atlas markdown format arguments aligned: PASS
- QWave conditioning train score type annotation: PASS
- QWave runtime apply score type annotation: PASS
- QWave canary candidate score type annotation: PASS
- real batch final step borrow/move scalar copy: PASS
- acceptance report exists: PASS
- bake report exists: PASS

## Suggested native commands

```bash
cargo test -p tokenizer_core hangul_qwave
cargo test -p tokenizer_core hangul_qwave_dp_bridge
cargo test -p lora_train qwave
```
