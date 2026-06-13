# QW-MCTS-01 — Value Network Reward Vector Contract / Domain Score Gate Seal

## 확정
- 16-channel MCTS reward vector contract added.
- Domain score gate added as fixture-only, not runtime authority.
- Reward source attribution is fixture-only and measured probes are deferred.
- Value Network call/training, optimizer step, checkpoint write, LoRA mutation, dataset/Arrow export, runtime authority are all blocked.

## 상태 귀속 위치
- `crates/model_core/src/qw_mcts_reward_vector.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/tests/qw_mcts01_reward_vector_contract.rs`
- `crates/model_core/tests/qw_mcts01_no_value_training_mutation.rs`

## Acceptance
- reward channel count = 16
- reward vector count = QW-MCTS-00 node count
- domain score gate valid
- source attribution valid
- aggregate reward score available
- debug checksum is not included in aggregate reward
- no Value Network call/training/mutation/export/runtime authority

## Next
`QW-MCTS-02 — DeltaK/QWave HDC State Encoder / No Value Authority Seal`
