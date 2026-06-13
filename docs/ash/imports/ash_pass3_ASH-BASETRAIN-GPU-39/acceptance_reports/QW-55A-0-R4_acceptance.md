# QW-55A-0-R4 Acceptance

## PASS

- R3 feature matrix [16,16]을 row-major 256 payload로 변환했다.
- R3 score matrix [16,16]을 row-major 256 payload로 변환했다.
- feature/score matrix를 각각 4개의 8x8 block으로 분해했다.
- backend generic Tile16LogicalFromTile8 validator를 추가했다.
- R2 final step receipt hash와 R3 dry-run receipt hash를 참조했다.
- selector result, root winner, selected token을 생성하지 않았다.
- decode mutation, greedy final authority mutation이 없다.
- 신규 VTC16 stack/WGSL 및 contiguous 16x16 tile이 없다.

## Local validation commands

```powershell
cargo check -p model_core --lib
cargo check -p burn_webgpu_backend --lib
cargo test -p model_core qw55a0_r4 --test qw55a0_r4_feature_score_backend_bridge
cargo test -p burn_webgpu_backend qw55a0_r4 --test qw55a0_r4_tile16logical_backend_bridge
```
