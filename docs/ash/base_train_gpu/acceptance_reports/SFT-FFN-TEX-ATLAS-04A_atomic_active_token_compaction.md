# SFT-FFN-TEX-ATLAS-04A Acceptance

## Status

PASS_STATIC / PENDING_GPU_ATOMIC_COMPACTION_RUNTIME

## Scope

Atomic active token compaction and padding skip counter seal.

## SSOT

- Source budget guard seal
- Source batched dispatch seal
- Padding mask digest
- Atomic counter reset digest
- Atomic counter final digest
- Active indices digest
- Padding skip evidence
- Atomic compaction seal

## Confirmed Static Gates

- Budget guard seal is required.
- Batched dispatch seal is required.
- Padding mask is required.
- Padding mask digest is required.
- Atomic counter reset is required.
- Counter initial value must be zero.
- Counter final value must match expected active token count.
- Active indices digest is required.
- Active indices overflow fails closed.
- Cross-adapter contamination fails closed.
- Cross-slot contamination fails closed.
- Atomic compaction prepass is allowed.
- Global atomic per active token is allowed for the first sealed prepass.
- Atomic use in FFN dot product remains closed.
- Atomic output accumulation remains closed.
- dispatchIndirect args write remains closed.
- FFN batched dispatch execution remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- atomic active token compaction prepass
- global atomic active token counter
- padding mask digest recording
- active indices digest recording
- active token count recording
- padding skip ratio recording
- counter reset receipt

## Closed

- FFN batched dispatch execution
- dispatchIndirect execution
- dispatchIndirect args write
- atomic in FFN dot product
- atomic output accumulation
- SFT training in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU atomic compaction prepass run.
