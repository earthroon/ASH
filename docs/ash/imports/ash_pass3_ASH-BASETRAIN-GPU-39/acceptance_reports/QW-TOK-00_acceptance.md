# QW-TOK-00 Acceptance

## PASS evidence
- Tokenizer V5 probe module added.
- Local artifact path recorded.
- Tokenizer files are not packaged in bake.
- Runtime vocab parity is PENDING until runtime dimensions are supplied.
- Auto repair paths are blocked.

## Required local validation

```powershell
cargo check -p model_core --lib
cargo test -p model_core qw_tok00 --test qw_tok00_tokenizer_v5_runtime_binding_probe
cargo test -p model_core qw_tok00 --test qw_tok00_vocab_cap_parity
cargo test -p model_core qw_tok00 --test qw_tok00_no_tokenizer_auto_repair
```
