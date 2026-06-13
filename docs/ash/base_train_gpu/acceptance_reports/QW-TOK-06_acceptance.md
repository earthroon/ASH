# QW-TOK-06 Acceptance

Status: `PENDING_QW_TOK06_SUBTITLE_FIXTURE_OR_RUNNER_UNAVAILABLE`

## PASS checks installed
- QW-TOK-06 module exists.
- `lib.rs` wires and re-exports the module.
- Subtitle prompt fixture case structure exists.
- Subtitle control token contract structure exists.
- Cue/br structure probe exists.
- Subtitle smoke output structure exists.
- No quality score seal exists.
- No reward/training mutation seal exists.
- Expected vocab size is sealed to `48259`.
- Expected max token id is sealed to `48258`.
- Quality scoring is blocked by default.
- Translation/subtitle quality evaluation is blocked by default.
- Reward/value scoring is blocked by default.
- QW/MCTS execution is blocked by default.
- Training mutation and dataset export are blocked by default.
- Checkpoint/model/runtime/tokenizer writes are blocked by default.

## Local validation
Run on operator machine:

```powershell
cargo check -p model_core --lib
cargo test -p model_core qw_tok06 --test qw_tok06_subtitle_prompt_fixture_smoke
cargo test -p model_core qw_tok06 --test qw_tok06_subtitle_control_token_contract
cargo test -p model_core qw_tok06 --test qw_tok06_no_quality_score
cargo test -p model_core qw_tok06 --test qw_tok06_no_training_no_reward
```
