# SFT-GPU-STREAM-03 Acceptance

## Status

PASS_STATIC / PENDING_REAL_RUNNER_TRANSPORT

## Scope

Runner stream transport intake, JSONL parsing evidence, and canonical step ledger bridge for Native GPU LoRA SFT step telemetry.

## SSOT

- Source execution receipt: `AshSftRunExecutionReceiptIntakeReport`
- Raw transport digest: `raw_transport_sha256`
- Canonical step ledger: `canonical_step_ledger_sha256`
- Transport intake seal: `AshSftGpuStreamTransportIntakeSeal`
- STREAM-01 bridge: `AshSftGpuStreamTransportCanonicalBridge`

## Confirmed Static Gates

- Execution receipt is required.
- Transport source kind must be explicit.
- Raw transport digest is required.
- Malformed JSONL evidence fails closed.
- Schema mismatch evidence fails closed.
- Parsed event count must be greater than zero.
- Runner execution id must match.
- Slot / lease / command / adapter id must match.
- Target key / artifact family must match.
- Native GPU backend is required.
- CPU fallback fails closed.
- NaN/Inf metric fails closed.
- Event and step sequence must be monotonic.
- Canonical step ledger digest is required.
- Canonical bridge can be handed to SFT-GPU-STREAM-01.
- ASH core does not spawn runner process.
- ASH core does not execute training.
- ASH core does not write gradients.
- ASH core does not run optimizer steps.
- ASH core does not write artifacts.
- Slot ready remains closed.
- ASH synapse binding remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- runner stream transport intake
- JSONL raw-line evidence receipt
- parsed step event canonicalization bridge
- canonical step ledger digest recording
- partial stream resume marker
- ready_for_stream_01_receipt

## Closed

- runner process spawn in core
- SFT training execution in core
- gradient write in core
- optimizer step in core
- artifact write in core
- slot ready
- ASH synapse binding
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual native GPU LoRA SFT runner to emit canonical JSONL stream. This bake does not spawn or execute the runner.
