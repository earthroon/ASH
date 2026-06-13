# 16AI-4 Acceptance PENDING

## Acceptance Criteria

- AC-16AI-4-1: `<pad>` encodes as exactly `[0]`.
- AC-16AI-4-2: `<bos>` encodes as exactly `[1]`.
- AC-16AI-4-3: `<eos>` encodes as exactly `[2]`.
- AC-16AI-4-4: `<unk>` encodes as exactly `[3]`.
- AC-16AI-4-5: `single_token_exact=true` for all four core special tokens.
- AC-16AI-4-6: generation path remains disconnected by default.
- AC-16AI-4-7: CPU reference fallback remains preserved.
- AC-16AI-4-8: wrapper / chat role fragmentation remains diagnostic and is not silently patched.

## Expected remaining diagnostics

```txt
<br> may remain fragmented
<|user|> may remain fragmented
<|assistant|> may remain fragmented
사용자 / 사용자: may remain fragmented
어시스턴트 / 어시스턴트: may remain fragmented
wrapper suspicious_char_split may remain true
```

## Status

PENDING_LOCAL_RUN
