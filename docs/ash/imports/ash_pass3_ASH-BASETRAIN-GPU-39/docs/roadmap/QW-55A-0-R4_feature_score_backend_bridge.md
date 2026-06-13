# QW-55A-0-R4 — Feature Score Matrix Backend Bridge / No Selector Commit Seal

## 확정

R4는 R3의 QW-55A 16x16 feature/score fixture를 backend가 이해할 수 있는 Tile16LogicalFromTile8 bridge payload로 변환하는 dry-run 패치다. selector, root winner, selected_token_id, decode commit, greedy authority 변경은 모두 금지한다.

## 상태 귀속 위치

- model_core semantic bridge: `crates/model_core/src/qw55a_vtc16_backend_bridge.rs`
- backend generic validator: `crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_logical16_bridge.rs`
- R4 report: `artifacts/qw55a0_r4_feature_score_backend_bridge_report.json`
- R4 trace: `workspace/runtime_traces/qw55a0_r4_feature_score_backend_bridge_trace.jsonl`
- R4 receipt: `workspace/trace/qw55a0_r4_feature_score_backend_bridge_receipt.json`

## SSOT

model_core는 QW-55A 의미/fixture/request를 소유하고, burn_webgpu_backend는 QW-55A 의미를 모르는 generic logical16 payload validator만 소유한다.

## 불변조건

- feature/score matrix shape는 각각 [16, 16]
- row-major payload length는 각각 256
- feature/score tile8 block count는 각각 4
- tile offset은 (0,0), (0,8), (8,0), (8,8)
- tile_mode_requested는 Tile16LogicalFromTile8
- contiguous 16x16 tile 생성 금지
- 신규 VTC16 Rust/WGSL stack 생성 금지
- selector result/root winner/selected token 생성 금지
- decode mutation 및 greedy final authority mutation 금지

## 다음 패치

QW-55A-0-R5 — Root Candidate Snapshot Fixture / No Logits Runtime Bind Seal
