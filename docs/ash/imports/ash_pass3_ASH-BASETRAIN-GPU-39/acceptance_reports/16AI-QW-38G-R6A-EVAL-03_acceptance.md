# Acceptance Report — 16AI-QW-38G-R6A-EVAL-03

## Status
PASS_STATIC / RUNTIME_NOT_RUN

## Confirmed static contracts
- `candidate_replay_only = true`
- `base_config_mutation_allowed = false`
- `runtime_promotion_allowed = false`
- `can_promote_to_default = false`
- hard fail criteria include global fallback, active set empty, critical salad, backend semantic regression, threshold kind mismatch, and output-too-short.

## Not run
- cargo check
- runtime replay
- backend parity replay
- long horizon candidate soak

## Next step
Run EVAL-03 replay candidate. If pass, proceed to `16AI-QW-38G-R6A-DECODE-03G` controlled apply.
