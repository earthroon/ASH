# SFT-GPU-8F Compile Result

## Status

PENDING_COMPILE

## Reason

The bake environment does not provide `cargo` or `rustfmt`, and this extracted artifact root does not include a root `Cargo.toml` at the top level. Therefore, Rust compilation was not executed here.

## Executed validation

```txt
python tools/validate_sft_gpu_8f_static.py
```

Result: `PASS_STATIC`
