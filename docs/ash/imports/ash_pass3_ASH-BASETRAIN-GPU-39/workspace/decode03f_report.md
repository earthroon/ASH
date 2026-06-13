# 16AI-QW-38G-R6A-DECODE-03F
## Guard Overlay Auto-tuning / Threshold Calibration Seal

### 확정
- `crates/model_core/src/decode03f_guard_calibration.rs` 추가.
- `crates/model_core/src/lib.rs` export 추가.
- `sampler_parity::append_receipt()`에 DECODE-03F hook 추가.
- `workspace/decode03f_candidates.jsonl` candidate-only receipt 추가.
- `workspace/decode03f_summary.json` summary 추가.

### 계약
- `candidate_only = true`
- `runtime_apply = false`
- `can_promote_to_default = false`
- 03F는 threshold를 실제 runtime에 적용하지 않는다.

### 판단불가
- cargo/rustc가 없어 빌드·런타임 검증은 수행하지 못했다.
