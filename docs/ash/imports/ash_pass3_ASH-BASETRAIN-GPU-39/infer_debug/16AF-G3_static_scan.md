# 16AF-G3 Static Scan

## 확인

G3 runner는 generation compare/logging 전용이며 generation default를 true로 바꾸지 않습니다.

## Forbidden path policy

다음 경로를 새 runner에서 직접 도입하지 않습니다.

- Tensor.matmul
- fused_matmul_autotune
- LocalTuner
- RawWgpuBufferLease
- into_contiguous_aligned
- burn_cubecl_fusion

## Runtime gate

- candidate default remains false
- CPU fallback compare remains explicit
- attention_native=false
- kv_cache_native=false
