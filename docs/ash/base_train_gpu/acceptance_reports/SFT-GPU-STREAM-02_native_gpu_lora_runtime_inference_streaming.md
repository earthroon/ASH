# SFT-GPU-STREAM-02 Acceptance

## Status

PASS_STATIC / PENDING_RUNTIME_GPU_INFERENCE_STREAM

## Scope

Native GPU LoRA runtime inference streaming smoke receipt and token event seal.

## SSOT

- Artifact capture seal: `AshSftRunArtifactCaptureReport`
- GPU training step seal: `AshSftGpuStreamStepTelemetryReport`
- Runtime token ledger: `AshSftGpuRuntimeTokenLedgerEvidence`
- Runtime inference seal: `AshSftGpuRuntimeInferenceStreamSeal`

## Confirmed Static Gates

- SFT-RUN-04 artifact capture evidence is required.
- SFT-GPU-STREAM-01 GPU step telemetry evidence is required.
- Native GPU runtime backend is required.
- Runtime LoRA smoke attachment is required.
- Base-only fallback is fail-closed.
- Silent fallback is fail-closed.
- Token event ledger digest is required.
- Token index must be monotonic and contiguous.
- LoRA delta must be observed.
- Non-finite logit metrics fail closed.
- Device mismatch fails closed.
- Runtime attach is allowed only for smoke.
- Runtime attach as current remains closed.
- Production runtime attach remains closed.
- Slot ready remains closed.
- Synapse binding remains closed.
- Registry mutation remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- runtime smoke receipt intake
- runtime attach for smoke
- token ledger digest recording
- native GPU runtime confirmation
- LoRA delta observation

## Closed

- runtime attach as current
- production runtime attach
- slot ready finalization
- ASH synapse binding
- registry mutation
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires an actual native GPU runtime to emit canonical token event stream evidence.

## Static validation note

The bake environment did not include `cargo`, `rustc`, or `rustfmt`; compile-time validation remains pending in the local Rust environment.
