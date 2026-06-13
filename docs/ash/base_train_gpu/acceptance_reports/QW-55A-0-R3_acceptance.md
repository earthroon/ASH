# QW-55A-0-R3 Acceptance

## Static Acceptance Status

- QW55A0_R3 constants: PASS
- Feature/score fixture config: PASS
- Feature/score fixture struct: PASS
- Dry-run report/trace/receipt structs: PASS
- 16 feature channel order helper: PASS
- 16 score channel order helper: PASS
- Deterministic feature rows: PASS
- Deterministic score rows: PASS
- `[16, 16]` matrix shape seal: PASS
- R2 receipt hash reference as string: PASS
- No backend dependency from model_core: PASS
- No selector result: PASS
- No selected token/root rank: PASS
- No decode mutation: PASS
- No greedy authority mutation: PASS

## Cargo Status

Not executed in this container because `cargo` is unavailable. Run locally:

```powershell
cargo check -p model_core --lib
cargo test -p model_core qw55a0_r3 --test qw55a0_r3_feature_score_matrix_fixture
```
