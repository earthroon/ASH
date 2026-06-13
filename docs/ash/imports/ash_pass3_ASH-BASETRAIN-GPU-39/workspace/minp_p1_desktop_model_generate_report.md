# 16AI-QW-38G-R6A-MINP-P1 — Desktop model.generate Min-P Pipeline Wiring Bake Report

## 확정

P1 베이크는 P0의 SSOT인 `RuntimeSamplingConfig.min_p`를 바꾸지 않고, desktop `model.generate` 호출이 infer-compatible 경로로 들어가도록 연결했다.

### 변경 파일

- `apps/desktop/src/App.vue`
- `crates/orchestrator_local/src/lib.rs`
- `crates/orchestrator_local/src/infer_entry.rs`

### 반영 내용

1. desktop lab UI에 `minP` 상태와 range 입력을 추가했다.
2. `runGenerate()`와 translation helper의 `model.generate` payload에 canonical key `min_p`를 포함했다.
3. desktop boundary에서 `normalizeMinPForPayload()`로 `0.0..0.95` clamp를 수행한다.
4. orchestrator `model.generate`의 기존 prompt echo/stub 경로를 제거했다.
5. `model_generate_bridge_payload()`를 추가해 `prompt -> input`, `max_new_tokens -> maxNewTokens`, `min_p alias -> min_p`로 정규화한다.
6. `model.generate` handler는 `generate.started`를 낸 뒤 `handle_infer_run()`으로 위임한다.
7. infer 완료 시 `model_generate_session_id`가 있으면 desktop이 이미 듣고 있는 `generate.output`, `generate.done` 이벤트를 방출한다.

## SSOT

- 상태 귀속 위치: `RuntimeSamplingConfig.min_p`
- desktop payload key: `min_p`
- 외부 alias 허용: `minP`, `min_p`, `samplingMinP`, `sampling_min_p`
- 내부 canonical: `min_p`

## 정적 검증

- desktop `min_p` payload 포함: PASS
- desktop clamp helper 존재: PASS
- `model.generate` echo/stub 제거: PASS
- `model.generate -> handle_infer_run` bridge: PASS
- prompt/input bridge: PASS
- max_new_tokens/maxNewTokens bridge: PASS
- Min-P alias normalization: PASS
- infer 완료 이벤트 `generate.output` / `generate.done`: PASS

## 판단불가

현재 컨테이너에는 `cargo`와 `rustfmt`가 없어 Rust 컴파일/포맷 검증은 실행하지 못했다. `apps/desktop`에는 `node_modules`가 없어 Vite/TypeScript 빌드도 실행하지 못했다.

## 비범위

- GPU shader semantics 변경 없음
- CPU fallback sampler 변경 없음
- top-p active-set renormalization 변경 없음
- P5 수준 telemetry proof 변경 없음
