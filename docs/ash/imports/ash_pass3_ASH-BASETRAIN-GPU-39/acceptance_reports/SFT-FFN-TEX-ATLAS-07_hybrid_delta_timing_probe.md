# SFT-FFN-TEX-ATLAS-07 Acceptance

## Status

PASS_STATIC / PENDING_GPU_HYBRID_TIMING_RUNTIME

## Scope

Hybrid delta timing probe for base texture + LoRA buffer path.

## SSOT

- Source hybrid LoRA seal
- Source base timing probe seal
- Source atomic compaction seal
- Source batched dispatch seal
- Source projection parity seal
- Source atlas bake seal
- Texture base timing evidence
- LoRA delta timing evidence
- Texture hybrid timing evidence
- Storage hybrid baseline timing evidence
- Hybrid timing compare evidence
- Hybrid timing seal

## Confirmed Static Gates

- Hybrid LoRA seal is required.
- Base timing probe seal is required.
- Atomic compaction seal is required.
- Batched dispatch seal is required.
- Projection parity seal is required.
- Atlas bake seal is required.
- Timing source is required.
- Texture base only timing is required.
- LoRA delta only timing is required.
- Texture hybrid timing is required.
- Storage hybrid baseline timing is required.
- Hybrid output digest must match.
- LoRA delta digest must match.
- Speedup metrics are recorded.
- LoRA delta overhead is recorded.
- Hybrid timing probe execution is allowed.
- Hybrid path promotion candidate remains closed.
- Hybrid path default switch remains closed.
- Hybrid training path remains closed.
- Hybrid production path remains closed.
- LoRA buffer write remains closed.
- LoRA optimizer step remains closed.
- LoRA texture update remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- hybrid timing probe execution
- texture base only timing receipt
- LoRA delta only timing receipt
- texture hybrid timing receipt
- storage hybrid baseline timing receipt
- hybrid vs storage compare
- LoRA delta overhead metric
- hybrid speedup ratio recording

## Closed

- hybrid path promotion candidate
- hybrid path default switch
- hybrid training path
- hybrid production path
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU timing collection from target backend.
