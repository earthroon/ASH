# 16AI-QW-38G-R6A-MINP-P1 Acceptance

## 완료 기준

- [x] desktop `model.generate` payload에 `min_p` 포함
- [x] `min_p` payload key를 내부 canonical과 동일하게 사용
- [x] desktop boundary clamp 추가
- [x] Rust boundary clamp는 P0의 `normalize_min_p`를 재사용
- [x] `model.generate` prompt echo/stub 경로 제거
- [x] `model.generate`를 infer-compatible bridge로 연결
- [x] `prompt`를 infer `input`으로 정규화
- [x] `max_new_tokens`를 infer `maxNewTokens`로 정규화
- [x] `model.generate` 요청의 `min_p`가 infer payload로 도달
- [x] infer 완료 시 desktop 이벤트 `generate.output` / `generate.done` 방출
- [x] P1 summary JSON 생성
- [x] P1 patch 생성

## 검증 상태

- 정적 패턴 검증: PASS
- `cargo check`: NOT RUN — container에 cargo 없음
- `cargo test`: NOT RUN — container에 cargo 없음
- `rustfmt`: NOT RUN — container에 rustfmt 없음
- `npm/vite build`: NOT RUN — `node_modules` 없음

## 판정

`DESKTOP_MODEL_GENERATE_MINP_PIPELINE_WIRED_STATIC_BAKE`
