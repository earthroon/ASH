# ASH text qwave patch v2

## 이번 단계에서 실제로 바뀐 축

1. `tokenizer_core`
   - 한글 음절에서 받침 class / coda weight / curvature bias를 계산
   - 토큰 내부에서 조사 / 높임 / 호칭 / 선어말 / 종결어미를 분리
2. `text_kernel`
   - density gate가 ambiguity + cairo + bridge 뿐 아니라
     coda / curvature / honorific ratio까지 반영
   - `preferred_resolution` 외에 `preferred_packed_path`, `shader_density_lane`, `shader_weight_scale` 산출
3. `runtime`
   - backend label이 text density 결과를 포함해 annotate 됨
   - output artifact에 packed path / density lane 기록
4. `orchestrator_local`
   - infer 요청 시 text kernel 관측을 자동 수행
5. `audio_kernel`
   - audio -> runtime bridge에서도 text hints를 함께 주입
6. `burn_webgpu_backend`
   - text density gate uniform / WGSL helper scaffold 추가

## packed path 규칙

- compact -> `packed_compact`
- adaptive + 높은 받침 밀도 -> `packed_adaptive_coda`
- dense -> `packed_dense`
- dense + 높은 cairo risk -> `packed_dense_cairo`

## 남는 작업

- 실제 backend dispatch에서 `TextDensityGateUniform`을 bind group에 연결
- `NativeWgpuModel` 로드 경로에서 packed path 선택 분기 연결
- hot token artifact의 packed bytes 레이아웃과 `packed_path_id`를 진짜로 접속
