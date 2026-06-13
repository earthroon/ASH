# SFT-GPU-RUN-01 Acceptance

## Status

PASS_STATIC / PENDING_STRICT_GPU_RUNTIME_RUN

## Scope

Strict native GPU LoRA SFT train run with no CPU fallback.

## SSOT

- Train config digest
- Native GPU backend evidence
- No CPU fallback evidence
- GPU train step receipts
- Adapter update evidence
- Optimizer accounting evidence
- Artifact output evidence
- Save-reload parity evidence
- No runtime mutation guard
- Strict GPU train run seal

## Confirmed Static Gates

- Native GPU backend is required.
- GPU device fingerprint is required.
- CPU fallback is forbidden.
- CPU materialization is forbidden.
- Silent backend demotion is forbidden.
- Forward GPU receipt is required.
- Loss GPU receipt is required.
- Backward GPU receipt is required.
- Optimizer GPU receipt is required.
- Loss must be finite.
- Adapter delta must change.
- Adapter update must be applied.
- Optimizer accounting must be applied.
- Adapter artifact must be written.
- Save-reload parity must pass.
- Runtime current pointer update is forbidden.
- Promotion apply is forbidden.
- Lifecycle mutation is forbidden.
- Slot action apply is forbidden.
- ASH current binding is forbidden.

## Opened

- strict native GPU LoRA train run
- native GPU backend receipt
- no CPU fallback receipt
- GPU train step receipt
- adapter update receipt
- optimizer accounting receipt
- adapter artifact output receipt
- save-reload parity receipt

## Closed

- CPU fallback
- CPU materialized train path
- silent backend demotion
- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- ASH current binding

## Runtime Acceptance Pending

Requires actual strict GPU train run on target machine.
