# ASH-FT-44 Delta Candidate Payload Materialization / Explicit Tensor Payload No Stack Append Seal

## SSOT
ASH-FT-44 consumes the ASH-FT-43 integrity audit manifest and an explicit candidate tensor source manifest, then materializes a selected-group tensor delta payload as a candidate artifact only.

## Allowed
- explicit selected-group tensor payload materialization
- payload shape/dtype manifest creation
- payload hash manifest creation
- payload provenance receipt creation

## Forbidden
- official delta packet creation
- delta stack append
- checkpoint apply
- base checkpoint mutation
- canonical safetensors rewrite
- shadow candidate creation/replay
- generation
- runtime default apply
- promotion

## Required gates
- `explicit_payload_gate == true`
- `allow_tensor_payload_write == true`
- candidate tensor source manifest exists
- tensor source scope is `selected_group_only`
- tensor source is not synthetic/fabricated
- tensor names, shapes, dtypes, and finite status are known

## Expected PASS
`PASS_ASH_FT44_DELTA_CANDIDATE_PAYLOAD_MATERIALIZATION_EXPLICIT_TENSOR_PAYLOAD_NO_STACK_APPEND`

## Next
ASH-FT-45 Materialized Delta Payload Integrity Audit / No Stack Append No Apply Seal
