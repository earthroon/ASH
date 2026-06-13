# ASH-BASETRAIN-GPU-37H-R1 Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-37H-R1`  
`JSON Receipt Atlas Tiling Buildfix / Parallel Section Layout For Shader Module Compile Candidate No Dispatch Seal`

## 확정

37H의 로컬 빌드 실패 원인은 GPU/WGSL validation 실패가 아니라 `serde_json::json!` 단일 거대 receipt macro expansion 한계였다.

Observed compiler error:

```txt
error: recursion limit reached while expanding `$crate::json_internal!`
```

R1은 `receipt_json()`의 단일 대형 `json!({ ... })`를 제거하고, receipt를 atlas tile section으로 분해한다.

## 수정

- Root receipt는 `receipt_atlas_root(vec![...])`로 조립한다.
- 각 top-level section은 `receipt_tile_*()` 함수로 분리한다.
- digest용 JSON도 `receipt_digest_tile_*()`로 분리한다.
- 37H runtime policy는 유지한다.
  - GPU adapter/device request 허용
  - shader module creation 허용
  - GPU buffer/upload/readback/pipeline/bind group/dispatch 금지

## 상태 귀속 위치

```txt
crates/base_train/src/ash_basetrain_gpu_37h_selected_group_row_block_shader_module_compile_candidate.rs
```

## SSOT 존재 여부

SSOT 있음. 37H runtime SSOT는 여전히 37G PASS receipt다. R1은 receipt construction layout만 변경한다.

## 재현 가능성

동일 37G PASS receipt와 동일 WGSL template 입력 시 동일 section tile layout 및 동일 digest contract가 재현되어야 한다. 단 GPU adapter/device 환경 정보는 환경 의존값이다.

## 정적 Guard

- source file open 없음
- row-block read 없음
- F32 decode 없음
- GPU buffer creation 없음
- queue upload 없음
- readback 없음
- compute pipeline 없음
- bind group 없음
- dispatch 없음
- forward/backward/optimizer/mutation 없음
- giant receipt json macro 제거
- atlas tiled section assembly 존재

## 판단불가

이 컨테이너에는 `cargo/rustc`가 없어 실제 빌드/실행은 확인하지 못했다. 로컬에서 아래 명령으로 확인한다.

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37h_selected_group_row_block_shader_module_compile_candidate
```

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37h_selected_group_row_block_shader_module_compile_candidate -- --gpu-upload-promotion-gate-receipt .\artifacts\ASH_BASETRAIN_GPU_37G_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PROMOTION_GATE.json
```
