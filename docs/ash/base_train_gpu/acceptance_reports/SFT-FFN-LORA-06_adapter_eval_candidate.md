# SFT-FFN-LORA-06 Acceptance

## Status

PASS_STATIC / PENDING_GPU_EVAL_RUNTIME

## Scope

Adapter eval candidate and loss direction smoke seal.

## SSOT

- Source adapter artifact candidate seal
- Artifact manifest digest
- Artifact payload digest
- Safetensors candidate digest
- Eval fixture evidence
- Loss evidence
- Output sanity evidence
- Non-regression policy
- Artifact mutation guard
- No promotion guard
- Adapter eval candidate seal

## Confirmed Static Gates

- Artifact candidate seal is required.
- Artifact candidate must be accepted.
- Adapter scope is required.
- Slot scope is required.
- Target module id is required.
- Manifest digest is required.
- Payload digest is required.
- Safetensors candidate digest is required.
- Eval fixture is required.
- Eval fixture digest is required.
- Baseline loss is required.
- Candidate loss is required.
- Loss must be finite.
- Loss regression beyond tolerance fails closed.
- Output digest is required.
- Empty output fails closed.
- Non-finite output fails closed.
- Collapsed output fails closed.
- Artifact mutation during eval fails closed.
- Artifact write during eval fails closed.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Promotion review enqueue remains closed.
- Operator approval remains closed.
- Eval candidate smoke is allowed.
- Artifact read for eval is allowed.

## Opened

- adapter eval candidate smoke
- artifact read for eval
- eval fixture evidence
- loss direction evidence
- output sanity evidence
- non-regression policy
- artifact mutation guard
- no promotion guard

## Closed

- artifact write during eval
- runtime attach
- promotion apply
- current pointer update
- promotion review enqueue
- operator approval
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual adapter eval run from target backend.
