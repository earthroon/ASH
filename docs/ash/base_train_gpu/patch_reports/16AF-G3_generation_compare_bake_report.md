# 16AF-G3 Generation Compare Bake Report

## 확정

16AF-G3는 16AF-G2 native FFN candidate max_new_tokens=8 stability PASS 이후, native candidate 출력과 CPU reference fallback 출력을 같은 prompt/max_new_tokens/vocab_limit 조건으로 비교하기 위한 runner를 추가한 패치입니다.

## 반영 파일

- `crates/model_core/src/bin/af16g3_generation_compare.rs`
- `scripts/run_16AF_G3_generation_compare.ps1`
- `scripts/run_16AF_G3_generation_compare.sh`

## 주요 기능

- CPU reference model과 native FFN candidate model을 분리 실행합니다.
- native candidate는 `try_enable_native_atlas_ffn_generation_candidate(true)`로 preupload/cache를 활성화합니다.
- 두 경로 모두 동일 prompt ids, max_new_tokens, vocab_limit로 greedy generation을 수행합니다.
- 다음 값을 로그와 JSON/MD 리포트에 남깁니다.
  - CPU output ids / new ids / decoded text / decoded new text
  - native output ids / new ids / decoded text / decoded new text
  - token_ids_match
  - new_token_ids_match
  - text_match
  - first_mismatch_index
- `generation_connected_default=false`, `fallback_cpu_reference=true`, `attention_native=false`, `kv_cache_native=false` 유지가 명세입니다.

## 판단불가

이 환경에는 cargo/rustc/wgpu runtime이 없어 로컬 빌드와 runtime compare는 실행하지 못했습니다. 로컬에서 `af16g3_generation_compare`를 실행해 PASS/FAIL을 닫아야 합니다.
