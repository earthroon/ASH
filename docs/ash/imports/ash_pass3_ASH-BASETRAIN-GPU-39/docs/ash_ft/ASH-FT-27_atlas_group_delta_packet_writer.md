# ASH-FT-27
## Atlas Group Delta Packet Writer / No Base Checkpoint Mutation Seal

## SSOT

ASH-FT-27 writes a selected atlas group delta packet artifact from ASH-FT-26 optimizer dry-run evidence. It must not mutate the base checkpoint, canonical safetensors shards, selected/frozen group source weights, optimizer state, runtime aliases, promotion state, or the ordered delta stack ledger.

## State ownership

- Input SSOT: ASH-FT-26 receipt, update candidate dry-run receipt, optimizer profile receipt, no-state/no-weight/no-delta guards, and ASH-FT-25 selected group receipt.
- Output SSOT: `artifacts/ash_ft/delta_packets/ash_ft27_selected_group_delta_packet.manifest.json`.
- Ledger authority remains untouched until ASH-FT-28.

## Allowed

- Create delta packet envelope JSON.
- Create selected group delta metadata JSON.
- Create packet manifest JSON.
- Copy a materialized update candidate payload only when it already exists and is separate from base checkpoint.
- Create integrity and no-mutation guards.

## Forbidden

- Base checkpoint mutation.
- Canonical safetensors rewrite.
- Selected/frozen group source weight mutation.
- Optimizer state mutation.
- Real optimizer step.
- Delta stack append or ledger mutation.
- Shadow replay, runtime default apply, checkpoint alias rebind, or promotion.

## PASS

Expected verdict: `PASS_ASH_FT27_ATLAS_GROUP_DELTA_PACKET_WRITER_NO_BASE_CHECKPOINT_MUTATION`.

## BLOCKED

- `BLOCKED_ASH_FT27_FT26_NOT_EXECUTED`
- `BLOCKED_ASH_FT27_UPDATE_CANDIDATE_MISSING`
- `BLOCKED_ASH_FT27_METADATA_ONLY_PACKET_FORBIDDEN`

## Next

ASH-FT-28 — Sequential Delta Stack Ledger Append / Ordered Group Accumulation Seal.
