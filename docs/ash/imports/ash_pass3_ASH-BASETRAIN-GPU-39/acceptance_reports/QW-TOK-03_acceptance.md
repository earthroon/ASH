# QW-TOK-03 Acceptance

## PASS

- runtime input packet replay module exists.
- packet schema validation exists.
- runner schema descriptor exists.
- infer smoke candidate descriptor exists.
- id range `0..48258` is enforced.
- model inference is not executed.
- token generation is not executed.
- sampler/QW/MCTS are not executed.
- GPU queue submit and WGPU dispatch are not used.
- report, trace, and receipt are generated.

## FAIL

- id `48259` is accepted as valid.
- input packet schema mismatch is treated as PASS.
- runner schema mismatch is treated as PASS.
- infer smoke candidate is executed.
- model inference/token generation/sampler/QW/MCTS/GPU dispatch occurs.
