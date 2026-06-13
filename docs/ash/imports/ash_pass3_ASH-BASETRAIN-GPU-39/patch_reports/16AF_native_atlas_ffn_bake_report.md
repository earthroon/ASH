# 16AF Native Atlas FFN SiLU/SwiGLU Bake Report

## 확정

- 본체 SSOT: `ash_pass3_commit16P3R_row_gather_telemetry_fallback_seal.zip`
- 명세 SSOT: `16_af_native_atlas_ffn_patch_roadmap (1).md`
- 적용 범위: standalone FFN parity probe. Generation path에는 연결하지 않음.
- 기존 safe inference 체인: 16Y / 16AA / 16AB / 16AC / 16P-3R 유지.

## 구현 파일

```txt
crates/burn_webgpu_backend/src/native_atlas_ffn.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_atlas_ffn_probe.rs
crates/model_core/src/lib.rs
```

## 구현 내용

1. `NativeAtlasFfn16AfDispatcher` 추가.
   - native-owned WGPU device/queue 사용.
   - checkpoint CPU weights를 직접 storage buffer로 업로드.
   - Burn Tensor 내부 버퍼 차용 없음.

2. WGSL compute path 추가.
   - `gate_up_swiglu` entry point: `gate_proj`, `up_proj`, `SiLU(gate) * up`.
   - `down_project` entry point: `down_proj(mid)`.
   - row-major `[out_dim, in_dim]` weight layout 기준.

3. `model_core` parity harness 추가.
   - `native_atlas_ffn_16af_weight_layout()`
   - `synthetic_hidden_vector_16af()`
   - `run_native_atlas_ffn_16af_parity_probe()`

4. 리포트/재현 파일 추가.
   - `infer_debug/16AF_ffn_silu_refs.txt`
   - `infer_debug/16AF_native_atlas_shader_refs.txt`
   - `infer_debug/16AF_forbidden_path_scan.txt`
   - `patches/16AF_native_atlas_ffn_source_only.patch`

## Acceptance 상태

| 항목 | 상태 | 비고 |
|---|---:|---|
| AC-16AF-1 | 부분 충족 | 새 16AF 파일에서는 Burn/CubeCL matmul 호출 없음 |
| AC-16AF-2 | 부분 충족 | 새 16AF 파일 forbidden path scan 0 line |
| AC-16AF-3 | 판단불가 | cargo/GPU 실행 환경 없음 |
| AC-16AF-4 | 구현됨 | CPU reference shape와 native output shape 비교 코드 추가 |
| AC-16AF-5 | 구현됨 | max_abs_delta / mean_abs_delta threshold 비교 코드 추가 |
| AC-16AF-6 | 판단불가 | cargo/GPU 실행 환경 없음 |
| AC-16AF-7 | 충족 | 기존 safe generation path 직접 수정 없음 |
| AC-16AF-8 | 충족 | generation path에 native FFN 연결하지 않음 |

## 검증 한계

이 컨테이너에는 `cargo`, `rustc`, `rustfmt`가 없어 실제 Rust 빌드/실행 검증은 수행하지 못함.
기록 파일: `infer_debug/16AF_baseline_burn_webgpu_backend_check.txt`

## 판단

16AF는 현재 “완전 GPU 추론 복귀”가 아니라 “FFN 단독 native parity probe 스캐폴드 + dispatcher 구현” 상태로 베이크됨.
parity 실행은 로컬 Rust/WGPU 환경에서 `run_native_atlas_ffn_16af_parity_probe()`를 호출해 확인해야 함.
