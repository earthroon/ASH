# ASH-FT-49D Real Delta Candidate Payload Integrity Audit

This patch rechecks the payload created in ASH-FT-49C from the real optimizer candidate update path. The audit is intentionally read-only: payload write is disabled and all packet/stack/apply/runtime routes remain sealed.

## State authority
- Input SSOT: `ash_ft49c_real_delta_candidate_payload_manifest.json`
- Hash authority: `ash_ft49c_payload_hash_manifest.json`
- Source lineage: ASH-FT-49A -> ASH-FT-49B -> ASH-FT-49C
- Output SSOT: `ash_ft49d_real_delta_payload_audit_manifest.json`

## Next
ASH-FT-49E — Real Official Delta Packet Envelope Draft / No Stack Append No Apply Seal
