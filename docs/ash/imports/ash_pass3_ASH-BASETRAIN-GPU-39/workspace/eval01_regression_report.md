# 16AI-QW-38G-R6A-EVAL-01
## Backend Replay Matrix / CPU-WebGPU Parity Regression Seal

### 확정
- `crates/model_core/src/eval01_backend_replay.rs` 추가.
- CPU canonical trace와 candidate backend trace 구조를 분리.
- step diff / run pair diff / backend summary 구조를 추가.
- `sampler_parity::append_receipt()` 후속 hook에 EVAL-01 연결.
- backend capability manifest, backend matrix, metric schema, empty JSONL receipts, summary 생성.

### SSOT
CPU oracle replay trace가 backend 의미론 SSOT이며 WebGPU/runtime/fallback trace는 projection으로 비교한다.

### 안전계약
- backend failure run 조용한 제외 금지.
- unsupported feature는 applied=true로 기록 금지.
- output text만 보고 PASS 금지.
- min_p threshold kind mismatch는 FAIL 후보.

### 판단불가
- cargo/rustc가 없어 빌드 및 실제 backend replay는 실행하지 못했다.
- 현재 상태는 STATIC_BAKE_DEFINED_NOT_RUN.
