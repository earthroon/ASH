# 16AI-6-0 Fragmentation Baseline Bake Report

## 1. 확정

SSOT 기준은 현재 16AI-5R REDO 베이크 트리입니다. 16AI-6-0은 기존 generation compare를 수정하지 않고, tokenizer fragmentation baseline 전용 bin을 새로 추가했습니다.

추가 파일:

- `crates/model_core/src/bin/af16ai6_0_fragmentation_baseline.rs`
- `scripts/run_16AI_6_0_fragmentation_baseline.sh`
- `scripts/run_16AI_6_0_fragmentation_baseline.ps1`
- `infer_debug/16AI-6-0_static_scan.md`
- `acceptance_reports/16AI-6-0_acceptance_PENDING.md`
- `patch_reports/16AI-6-0_fragmentation_baseline_bake_report.md`

고정값:

- `generation=false`
- `assembly_mode=off`
- `cheonjiin_dp=false`
- `checkpoint_required=false`
- `chatml_lite_excluded=true`
- default wrappers: `plain,dialogue-ko,instruction-ko`
- default `vocab_limit=48259`

## 2. 구현 내용

`af16ai6_0_fragmentation_baseline.rs`는 `TokenizerManifest`와 `NativeTokenizer`만 사용해 현재 tokenizer의 encode/decode 상태를 기록합니다. 체크포인트와 모델 추론을 요구하지 않습니다.

각 case + wrapper마다 아래 필드를 저장합니다.

- `case_id`
- `wrapper`
- `raw_text`
- `wrapped_text`
- `prompt_len_chars`
- `prompt_len_bytes`
- `prompt_ids`
- `prompt_ids_len`
- `decoded_prompt`
- `roundtrip_exact`
- `normalized_roundtrip_exact`
- `suspicious_char_split`
- `spaced_korean`
- `wrapper_label_fragmented`
- `byte_token_leak`
- `special_marker_leak`
- `weak_word_boundary`
- `unknown_token_count`
- `fallback_like_token_count`
- `out_of_vocab_id_count`
- `fragmentation_score`
- `quality_score`
- `token_path`
- `char_analysis`

## 3. Fragmentation Score

초기 score는 penalty 합산형입니다.

- `spaced_korean`: +25
- `suspicious_char_split`: +25
- `wrapper_label_fragmented`: +35
- `roundtrip_exact=false`: +10
- `normalized_roundtrip_exact=false`: +5
- `unknown_token_count > 0`: +30
- `byte_token_leak`: +30
- `special_marker_leak`: +25
- `weak_word_boundary`: +10

최종:

- `fragmentation_score = min(100, penalties)`
- `quality_score = 100 - fragmentation_score`

## 4. 검증 상태

정적 스캔은 완료했습니다.

- 필수 marker 존재 확인: PASS
- runner script 존재 확인: PASS
- checkpoint 비요구 구조 확인: PASS
- generation 비실행 구조 확인: PASS

단, 이 실행 컨테이너에는 `cargo`가 설치되어 있지 않아 Rust compile/runtime 검증은 수행하지 못했습니다.

## 5. 판단불가

아래 항목은 실제 Rust/Cargo 환경에서 실행 전까지 확정할 수 없습니다.

- 실제 baseline fragmentation score
- worst_case / worst_wrapper 실제 값
- token_path offset 외 추가 정합성
- 16AI-6A Protected Span Scanner의 개선 폭
