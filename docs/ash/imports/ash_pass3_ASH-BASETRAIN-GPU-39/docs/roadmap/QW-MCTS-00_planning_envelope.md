# QW-MCTS-00 — MCTS Self-Play Planning Envelope / No Training Mutation Seal

## 확정
- MCTS node / edge / action / tree state envelope를 model_core에 추가한다.
- deterministic self-play episode fixture를 생성한다.
- expansion / simulation / backprop receipt를 생성한다.
- backprop receipt chain은 deterministic stable debug digest로 봉인한다.
- Value Network 호출, Value Network 학습, model weight mutation, checkpoint write, LoRA mutation, optimizer step, dataset/Arrow export, runtime decode bind는 금지한다.

## 상태 귀속 위치
- `crates/model_core/src/qw_mcts_planning_envelope.rs`
- `crates/model_core/tests/qw_mcts00_planning_envelope.rs`
- `crates/model_core/tests/qw_mcts00_no_training_mutation.rs`

## SSOT
QW-MCTS-00의 SSOT는 MCTS planning envelope와 deterministic self-play fixture이며, reward vector와 Value Network contract는 QW-MCTS-01로 이월한다.

## 재현 가능성
```powershell
cargo check -p model_core --lib
cargo test -p model_core qw_mcts00 --test qw_mcts00_planning_envelope
cargo test -p model_core qw_mcts00 --test qw_mcts00_no_training_mutation
```

## Next
`QW-MCTS-01 — Value Network Reward Vector Contract / Domain Score Gate Seal`
