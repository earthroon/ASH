# QW-55A-0-R5 Acceptance

## PASS

- Root candidate snapshot fixture module exists.
- model_core lib exports the module.
- Root candidate fixture test exists.
- Candidate count is sealed as 16.
- Rank order is sealed as stable 0..15.
- Token IDs are deterministic and unique.
- Runtime logits, sampler state, generation_sampling, infer_only CLI, and runtime_profile binds are sealed off.
- Selector result, root winner, selected token, decode mutation, and greedy authority mutation are all false/None.

## Local commands

```powershell
cargo check -p model_core --lib
cargo test -p model_core qw55a0_r5 --test qw55a0_r5_root_candidate_snapshot_fixture
```
