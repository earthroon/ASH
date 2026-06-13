# ASH-FT-43 Delta Candidate Integrity Audit / No Apply Seal

## SSOT
ASH-FT-43 consumes ASH-FT-42 staged delta candidate artifacts as read-only inputs and creates an integrity audit manifest. It recomputes staged descriptor and staged artifact manifest hashes, audits the provenance chain, verifies selected group scope, validates descriptor-copy-only payload mode, and re-seals no-apply / no-stack-append / no-shadow-replay boundaries.

## Allowed
- integrity audit
- provenance audit
- selected group scope audit
- hash recompute
- staged candidate audit manifest creation

## Forbidden
- checkpoint apply
- official delta packet creation
- delta stack append
- checkpoint or safetensors mutation
- runtime apply
- shadow candidate creation or shadow replay
- promotion
- generation
- additional forward/backward
- optimizer step
- weight commit

## Expected verdict
`PASS_ASH_FT43_DELTA_CANDIDATE_INTEGRITY_AUDIT_NO_APPLY`

## Next
ASH-FT-44 Delta Candidate Payload Materialization / Explicit Tensor Payload No Stack Append Seal
