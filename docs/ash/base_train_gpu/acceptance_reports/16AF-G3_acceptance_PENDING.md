# 16AF-G3 Acceptance PENDING

## PASS 조건

- build gate PASS
- `generation_connected_default=false`
- `fallback_cpu_reference=true`
- `candidate_runtime_enabled=true`
- `attention_native=false`
- `kv_cache_native=false`
- CPU reference generation executed=true
- native candidate generation executed=true
- native output token ids logged
- CPU fallback output token ids logged
- decoded text logged when tokenizer manifest is available
- `token_ids_match=true`
- `new_token_ids_match=true`
- summary pass=true
- seal: `PASS native FFN candidate generation output matches CPU reference fallback`

## FAIL 조건

- native candidate enable 실패
- CPU reference fallback이 사라짐
- default gate가 true로 바뀜
- token ids mismatch
- first_mismatch_index가 존재함
- tokenizer decode 실패가 PASS를 가로막지는 않지만 text_match는 n/a로 기록해야 함
