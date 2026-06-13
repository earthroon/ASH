# SFT-FFN-TEX-ATLAS-05 Acceptance

## Status

PASS_STATIC / PENDING_GPU_TIMING_RUNTIME

## Scope

Texture FFN timing probe and storage buffer compare seal.

## SSOT

- Source atlas bake seal
- Source projection parity seal
- Source batched dispatch seal
- Source budget guard seal
- Source atomic compaction seal
- Storage baseline timing evidence
- Texture padded timing evidence
- Texture compacted timing evidence
- Timing compare evidence
- Timing probe seal

## Confirmed Static Gates

- Atlas bake seal is required.
- Projection parity seal is required.
- Batched dispatch seal is required.
- Budget guard seal is required.
- Atomic compaction seal is required.
- Timing source is required.
- Storage baseline timing is required.
- Texture padded timing is required.
- Texture compacted timing is required.
- Output digest must match.
- Speedup metrics are recorded.
- Padding skip benefit is recorded.
- Timing probe execution is allowed.
- Texture path promotion candidate remains closed.
- Texture path default switch remains closed.
- Training dispatch remains closed.
- Production dispatch remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- texture FFN timing probe
- storage baseline timing receipt
- texture padded timing receipt
- texture compacted timing receipt
- storage vs texture compare
- padding skip benefit metric
- speedup ratio recording

## Closed

- texture path promotion candidate
- texture path default switch
- training dispatch
- production dispatch
- SFT training in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU timing collection from target backend.
