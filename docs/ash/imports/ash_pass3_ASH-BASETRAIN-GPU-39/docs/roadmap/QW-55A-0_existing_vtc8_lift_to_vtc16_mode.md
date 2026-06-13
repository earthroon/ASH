# QW-55A-0 — Existing VTC8 Atlas Lift To VTC16 Mode / Single TensorCore SSOT Seal

## 목적

기존 `TensorCube 8x8 MicroTile Atlas`를 단일 TensorCore SSOT로 유지한 채, 8x8 물리 타일 4개를 묶은 `Tile16LogicalFromTile8` 논리 모드를 추가한다.

이번 패치는 QW-55A selector authority를 켜지 않는다. 즉, greedy final authority를 아직 변경하지 않고, decode 결과도 변경하지 않는다.

## 상태 귀속 위치

```txt
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile.rs
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_parity.rs
crates/model_core/src/qw55a_vtc16_contract.rs
```

## SSOT 존재 여부

```txt
TensorCube 8x8 MicroTile SSOT: 존재, 유지
Grouped 16x16 schedule primitive: 존재, 재사용
Tile16LogicalFromTile8 named mode: 이번 패치에서 추가
QW-55A 16채널 feature/score contract: 이번 패치에서 추가
QW-55A final selector authority: 이번 패치에서 미적용
```

## 구현된 계약

- `TensorCubeVtcTileMode::Tile8Physical`
- `TensorCubeVtcTileMode::Tile16LogicalFromTile8`
- `TensorCubeVtcTileModeLayout`
- `tensorcube_vtc_tile_mode_layout()`
- `build_qw55a0_vtc8_to_vtc16_mode_report()`
- `tensorcube_cpu_vtc16_logical_reference_from_tile8()`
- `Qw55aVtc16PathFeatureRow`
- `Qw55aVtc16PathScoreRow`
- 16 feature channels / 16 score channels manifest

## 금지 계약

```txt
신규 vtc16_matrix_atlas.rs 생성 금지
신규 vtc16_matrix_atlas.wgsl 생성 금지
contiguous 16x16 physical tile 생성 금지
기존 8x8 tile layout 변경 금지
QW-55A-0에서 decode 결과 변경 금지
CPU reference를 runtime selector fallback으로 사용 금지
hard ban / token mask / vocab removal 금지
model weight / checkpoint / adapter mutation 금지
```

## Acceptance

```txt
PASS: 기존 8x8 layout 유지
PASS: Tile16LogicalFromTile8 mode 추가
PASS: logical 16x16은 8x8 물리 타일 4개 그룹으로 표현
PASS: grouped 16x16 schedule 8 step 재사용
PASS: CPU reference는 parity wrapper로만 추가
PASS: QW-55A 16채널 feature/score contract 추가
PASS: trace/receipt/report 생성
PASS: decode mutation 없음
```

## 다음 패치

```txt
QW-55A-0-R1
Logical VTC16 Native Smoke / Existing 8x8 Kernel Reuse Seal
```
