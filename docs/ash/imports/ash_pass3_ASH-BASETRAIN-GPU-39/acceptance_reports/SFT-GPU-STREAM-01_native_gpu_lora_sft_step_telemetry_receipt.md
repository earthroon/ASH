# SFT-GPU-STREAM-01 Acceptance

## Status

PASS_STATIC / PENDING_RUNTIME_GPU_STREAM

## Scope

Native GPU LoRA SFT step telemetry receipt and streaming event seal.

## SSOT

- Source execution receipt: `AshSftRunExecutionReceiptIntakeReport`
- Step event ledger: `AshSftGpuLoraStepTelemetryLedgerEvidence`
- Step stream seal: `AshSftGpuStreamStepTelemetrySeal`

## Confirmed Static Gates

- Native GPU backend is required.
- CPU fallback is fail-closed.
- Step event ledger digest is required.
- Step index must be strictly monotonic and contiguous.
- NaN/Inf loss or norm metrics fail closed.
- Device fingerprint mismatch fails closed.
- Event digest chain mismatch fails closed.
- ASH core does not execute training.
- ASH core does not write gradients.
- ASH core does not run optimizer steps.
- ASH core does not capture trained artifacts in this commit.
- Slot ready remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- step telemetry receipt intake
- step ledger digest recording
- native GPU backend confirmation

## Closed

- SFT training execution in core
- native dump execution in core
- gradient write in core
- optimizer step in core
- trained artifact capture
- LoRA artifact write
- artifact persistent write
- slot ready
- ASH synapse binding
- runtime attach
- registry mutation
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual native GPU LoRA runner to emit canonical step event JSONL.
