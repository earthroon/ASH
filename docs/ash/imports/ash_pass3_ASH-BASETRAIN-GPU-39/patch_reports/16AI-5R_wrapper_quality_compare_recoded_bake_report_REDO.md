# 16AI-5R Wrapper Quality Compare Recoded Bake Report REDO

## 1. 확정

SSOT 기준은 업로드된 `ash_pass3_commit16AI-4_core_special_encode_bake.zip`입니다. 기존 16AI-5R 산출물은 재사용하지 않았고, 16AI-4 PASS 상태 위에 새 파일을 추가하는 방식으로 재베이크했습니다.

추가/수정 파일:

- `crates/model_core/src/bin/af16ai5_wrapper_quality_compare.rs`
- `scripts/run_16AI_5R_wrapper_quality_compare.sh`
- `scripts/run_16AI_5R_wrapper_quality_compare.ps1`
- `infer_debug/16AI-5R_static_scan_REDO.md`
- `acceptance_reports/16AI-5R_acceptance_PENDING.md`
- `patch_reports/16AI-5R_wrapper_quality_compare_recoded_bake_report_REDO.md`

구현된 16AI-5R 고정값:

- `generation_connected_default=false`
- `fallback_cpu_reference=true`
- `attention_native=false`
- `kv_cache_native=false`
- default wrappers: `plain,dialogue-ko,instruction-ko`
- `chatml-lite` default 제외 및 명시 입력 시 fail-fast 차단
- default sampling preset: `greedy`
- default `max_new_tokens=1`
- default `vocab_limit=48259`

## 2. 구현 내용

`af16ai5_wrapper_quality_compare.rs`는 기존 16AI/16AF-G5 내부 API 흐름을 재사용하되, 산출물 신뢰는 재사용하지 않고 16AI-5R 전용 bin으로 새로 작성했습니다.

각 wrapper case는 아래 필드를 출력/저장합니다.

- `wrapper`
- `prompt_len`
- `wrapped_text`
- `prompt_ids`
- `decoded_prompt`
- `suspicious_char_split`
- `roundtrip_exact`
- `cpu_reference.ids`
- `cpu_reference.new_ids`
- `cpu_reference.text`
- `cpu_reference.new_text`
- `native_candidate.ids`
- `native_candidate.new_ids`
- `native_candidate.text`
- `native_candidate.new_text`
- `token_ids_match`
- `new_token_ids_match`
- `text_match`
- `new_text_match`
- `first_mismatch`
- `quality_score`
- `byte_token_leak`
- `special_marker_leak`
- `spaced_korean`
- `high_repetition`
- `weak_word_boundary`
- `empty_output`
- `new_text_len`
- `unique_new_token_ratio`

## 3. Quality Score

초기 점수는 100점이며 아래 penalty를 적용합니다.

- `byte_token_leak`: -30
- `special_marker_leak`: -25
- `spaced_korean`: -25
- `high_repetition`: -20
- `empty_output`: -40
- `weak_word_boundary`: -10
- CPU/native token mismatch: -50

최종 점수는 `max(0, 100 - penalties)` 구조입니다.

`best_wrapper`는 가장 높은 `quality_score` 기준으로 산출하며, 동점이면 아래 순서로 tie-break 합니다.

1. `byte_token_leak=false`
2. `special_marker_leak=false`
3. `spaced_korean=false`
4. 더 긴 `new_text_len`

## 4. 검증 상태

정적 스캔은 완료했습니다.

- 필수 marker 존재 확인: PASS
- runner script 존재 확인: PASS
- 산출물 파일명 REDO 기준 생성: PASS

단, 이 실행 컨테이너에는 `cargo`가 설치되어 있지 않아 Rust compile/runtime 검증은 수행하지 못했습니다. 또한 업로드된 16AI-4 zip 안에는 `tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors` checkpoint가 없어서 generation runtime acceptance는 PENDING입니다.

## 5. 판단불가

아래 항목은 실제 Rust/Cargo 환경과 checkpoint가 있는 로컬/CI에서 실행 전까지 확정할 수 없습니다.

- `plain / dialogue-ko / instruction-ko` 중 실제 best wrapper
- greedy generation 품질 개선 여부
- CPU/native 실제 token parity
- checkpoint/tokenizer 품질 병목 여부
- sampling preset 확장 필요 여부

