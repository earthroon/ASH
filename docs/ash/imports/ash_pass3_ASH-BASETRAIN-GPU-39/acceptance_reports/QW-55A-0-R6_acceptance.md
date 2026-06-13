# QW-55A-0-R6 Acceptance

## PASS

- R6 report exists.
- R5 candidate snapshot fixture is referenced.
- R5 candidate snapshot receipt hash is present.
- R4 backend bridge receipt hash is present.
- Candidate count is 16.
- Projected feature row count is 16.
- Feature channel count is 16.
- Feature matrix shape is [16, 16].
- Feature matrix row-major length is 256.
- Feature channel order is valid.
- Feature channel source mapping is valid.
- Candidate rank order is preserved.
- Candidate token ids are preserved.
- No runtime logits/sampler/generation_sampling bind exists.
- No score rows are generated.
- No aggregate scores are generated.
- No aggregate winner is created.
- No selector result is created.
- No selected token or selected root rank exists.
- No decode mutation or greedy authority mutation occurs.

## FAIL

- Any projection count, feature shape, or channel mapping drift.
- Runtime logits/sampler/generation_sampling binding.
- Score row, aggregate score, aggregate winner, selector result, selected token, or selected rank creation.
- Missing R5/R4 receipt references.
- Decode mutation or greedy final authority mutation.
