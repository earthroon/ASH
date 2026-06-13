# 16AI-4 Core Special Token Encode Path Bake Report

## SSOT

- Base: 16AI-3 spec alignment PASS state.
- Scope: tokenizer core special token encode path only.
- Generation connected: false.
- CPU reference fallback: preserved.
- Attention native: false.
- KV cache native: false.

## Patch

Modified:

```txt
crates/tokenizer_core/src/lib.rs
```

Added `NativeTokenizer::exact_core_special_id(...)` and an early exact-special guard in `TokenizerEngine::encode(...)`.

Core special tokens covered:

```txt
<pad> -> manifest.special_tokens.pad.id
<bos> -> manifest.special_tokens.bos.id
<eos> -> manifest.special_tokens.eos.id
<unk> -> manifest.special_tokens.unk.id
```

## Intentional Non-goals

The following fragmentation remains diagnostic and is not fixed in 16AI-4:

```txt
<br>
<|user|>
<|assistant|>
사용자
사용자:
어시스턴트
어시스턴트:
wrapper roundtrip spacing
```

## Expected audit changes

After rerunning `af16ai2_alignment_audit`, expected core special results:

```txt
<pad> encode_len=1 single_token_exact=true ids=0
<bos> encode_len=1 single_token_exact=true ids=1
<eos> encode_len=1 single_token_exact=true ids=2
<unk> encode_len=1 single_token_exact=true ids=3
```

`roundtrip_exact` may remain false for `<pad>`, `<bos>`, and `<eos>` because decode intentionally suppresses pad/bos and stops on eos. This is not part of 16AI-4 failure criteria.

## Runtime status

Not executed in this container because `cargo` / `rustc` are unavailable.
