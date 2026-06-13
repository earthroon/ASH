# ASH-FT-24 Sequential Atlas Group Training Schedule / Deterministic Group Order Seal

SSOT: ASH-FT-24 reads ASH-FT-23 group memory budget registry and creates a deterministic schedule for ASH-FT-25 without enabling active training. It must not load tensor payloads, create GPU resources, allocate gradients/optimizer state, run forward/backward, update weights, create delta packets, mutate the base checkpoint, or promote a candidate.

Allowed outputs:
- artifacts/ash_ft/ash_ft24_schedule_plan.json
- artifacts/ash_ft/ash_ft24_group_schedule_candidates.json
- artifacts/ash_ft/ash_ft24_deferred_group_queue.json
- artifacts/ash_ft/ash_ft24_deterministic_training_schedule.json
- artifacts/ash_ft/ash_ft24_schedule_hash_receipt.json
- artifacts/ash_ft/ash_ft24_no_active_training_guard.json
- artifacts/ash_ft/ash_ft24_no_runtime_allocation_guard.json
- artifacts/ash_ft/ash_ft24_next_patch_route.json
- artifacts/ash_ft/ASH-FT-24_receipt.json

Default policy schedules LOW and MEDIUM groups only. HIGH, BLOCKED, and UNKNOWN_REVIEW groups are deferred unless an explicit later review policy changes the route. If no executable groups exist, the patch can PASS with route status BLOCKED_NO_SCHEDULE_CANDIDATES and next_stage_allowed=false.
