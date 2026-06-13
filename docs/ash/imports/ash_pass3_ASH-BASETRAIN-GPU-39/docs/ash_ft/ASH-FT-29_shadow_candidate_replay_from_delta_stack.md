# ASH-FT-29
## Shadow Candidate Replay From Delta Stack / No Promotion Seal

SSOT: ASH-FT-29 reads the ASH-FT-28 ordered append-only delta stack ledger and replays only replay-ready delta packets into a shadow-only candidate workspace. It must not mutate the base checkpoint, canonical safetensors shards, runtime default binding, checkpoint alias, or promotion registry.

Allowed outputs:
- artifacts/ash_ft/shadow_candidates/ash_ft29_shadow_replay_plan.json
- artifacts/ash_ft/shadow_candidates/ash_ft29_replay_packet_filter_receipt.json
- artifacts/ash_ft/shadow_candidates/ash_ft29_replay_order_receipt.json
- artifacts/ash_ft/shadow_candidates/ash_ft29_shadow_candidate_manifest.json
- artifacts/ash_ft/shadow_candidates/ash_ft29_shadow_tensor_map.json
- artifacts/ash_ft/shadow_candidates/ash_ft29_shadow_replay_receipt.json
- artifacts/ash_ft/ash_ft29_no_base_checkpoint_mutation_guard.json
- artifacts/ash_ft/ash_ft29_no_runtime_default_apply_guard.json
- artifacts/ash_ft/ash_ft29_no_promotion_guard.json
- artifacts/ash_ft/ash_ft29_next_patch_route.json
- artifacts/ash_ft/ASH-FT-29_receipt.json

Forbidden:
- base checkpoint mutation
- canonical safetensors mutation
- runtime default apply
- checkpoint alias rebind
- promotion
- generation
- training

Expected PASS: PASS_ASH_FT29_SHADOW_CANDIDATE_REPLAY_FROM_DELTA_STACK_NO_PROMOTION
Expected BLOCKED examples:
- BLOCKED_ASH_FT29_FT28_NOT_EXECUTED
- BLOCKED_ASH_FT29_EMPTY_LEDGER
- BLOCKED_ASH_FT29_METADATA_ONLY_PACKET_NOT_REPLAY_READY
- BLOCKED_ASH_FT29_NO_REPLAY_READY_PACKET
