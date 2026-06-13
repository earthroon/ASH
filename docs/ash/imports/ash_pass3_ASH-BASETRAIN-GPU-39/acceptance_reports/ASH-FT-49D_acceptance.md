# ASH-FT-49D Acceptance Report

## Patch
ASH-FT-49D — Real Delta Candidate Payload Integrity Audit / No Stack Append No Apply Seal

## Expected result
PASS_ASH_FT49D_REAL_DELTA_CANDIDATE_PAYLOAD_INTEGRITY_AUDIT_NO_STACK_APPEND_NO_APPLY

## Confirmed by runner design
- FT-49C receipt must be PASS.
- FT-49C payload file must exist and be readable.
- Payload SHA256 must recompute and match FT-49C hash manifest when that manifest provides a hash.
- Shape/dtype manifest must expose non-empty tensor metadata.
- Payload scope must remain `selected_group_only`.
- Source lineage must resolve to ASH-FT-49B / real_optimizer_candidate_update.
- Synthetic source and stale FT-44 fallback source are rejected.
- Official packet, delta stack append, checkpoint apply, safetensors mutation, shadow replay, generation, runtime apply, and promotion remain forbidden.

## Compile status
Not claimed in this bake environment.
