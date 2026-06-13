# ASH-FT-28
## Sequential Delta Stack Ledger Append / Ordered Group Accumulation Seal

SSOT: ASH-FT-28 appends exactly one validated ASH-FT-27 delta packet to an ordered append-only delta stack ledger and computes parent/after stack hashes. It must not mutate base checkpoint, canonical safetensors, model weights, runtime aliases, or promotion state. It must not replay the delta stack or create a shadow candidate.

## Inputs
- artifacts/ash_ft/ASH-FT-27_receipt.json
- artifacts/ash_ft/delta_packets/ash_ft27_selected_group_delta_packet.json
- artifacts/ash_ft/delta_packets/ash_ft27_selected_group_delta_metadata.json
- artifacts/ash_ft/delta_packets/ash_ft27_selected_group_delta_packet.manifest.json
- artifacts/ash_ft/ash_ft27_delta_packet_integrity_receipt.json
- FT-27 no mutation guards
- optional artifacts/ash_ft/delta_stack/ledger.json

## Outputs
- artifacts/ash_ft/delta_stack/ledger.json
- artifacts/ash_ft/delta_stack/ash_ft28_ledger_append_plan.json
- artifacts/ash_ft/delta_stack/ash_ft28_ledger_entry.json
- artifacts/ash_ft/delta_stack/ash_ft28_stack_hash_receipt.json
- artifacts/ash_ft/ash_ft28_delta_packet_append_validation.json
- no base mutation / no replay / no shadow candidate guards
- artifacts/ash_ft/ASH-FT-28_receipt.json

## PASS
PASS_ASH_FT28_SEQUENTIAL_DELTA_STACK_LEDGER_APPEND_ORDERED_GROUP_ACCUMULATION

## BLOCKED
- BLOCKED_ASH_FT28_FT27_NOT_EXECUTED
- BLOCKED_ASH_FT28_METADATA_ONLY_APPEND_FORBIDDEN
- BLOCKED_ASH_FT28_DUPLICATE_PACKET_HASH
- BLOCKED_ASH_FT28_DUPLICATE_GROUP_SAME_PASS

## Next
ASH-FT-29 Shadow Candidate Replay From Delta Stack / No Promotion Seal.
