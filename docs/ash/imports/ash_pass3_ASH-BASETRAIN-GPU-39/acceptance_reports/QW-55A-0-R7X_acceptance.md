# QW-55A-0-R7X Acceptance

## PASS

- R7X selector gate module exists.
- R7X model_core module is exported.
- Score rows are generated from R6 projected feature rows.
- Aggregate rows are generated and sorted deterministically.
- Selector result is created.
- Selected token candidate is created.
- Runtime commit is blocked.
- Runtime selection is not used.
- Runtime logits / sampler / generation_sampling / infer_only / runtime_profile binds remain disabled.
- Decode mutation is false.
- Greedy final authority runtime change is false.

## FAIL

- Runtime commit is allowed.
- `selected_token_committed=true`.
- `runtime_selection_used=true`.
- Runtime bind flags become true.
- Decode mutation occurs.
- Greedy final authority runtime changes.
- Receipt references are missing.
