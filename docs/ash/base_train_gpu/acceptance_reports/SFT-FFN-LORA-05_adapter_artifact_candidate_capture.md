# SFT-FFN-LORA-05 Acceptance

## Status

PASS_STATIC / PENDING_ARTIFACT_CANDIDATE_RUNTIME

## Scope

Adapter artifact candidate capture with no runtime attach.

## SSOT

- Source updated adapter delta smoke seal
- Source optimizer step candidate seal
- Source gradient receipt seal
- Source LoRA target seal
- Artifact format policy
- Lineage evidence
- Adapter manifest candidate
- Artifact payload evidence
- Artifact write evidence
- No runtime attach guard
- Adapter artifact candidate seal

## Confirmed Static Gates

- Delta smoke seal is required.
- Delta smoke must be accepted.
- Optimizer step seal is required.
- Gradient seal is required.
- LoRA target seal is required.
- Adapter scope is required.
- Slot scope is required.
- Target module id is required.
- Target module fingerprint is required.
- Artifact format policy is required.
- Lineage evidence is required.
- Lineage digest is required.
- Manifest candidate is required.
- Manifest digest is required.
- Payload evidence is required.
- Payload digest is required.
- Safetensors candidate digest is required.
- LoRA A/B digest is required.
- Artifact candidate write is required.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Slot ready mark fails closed.
- ASH binding fails closed.
- Adapter artifact candidate capture is allowed.
- Artifact candidate write is allowed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- adapter artifact candidate capture
- artifact candidate write
- adapter manifest candidate
- artifact payload digest
- safetensors candidate digest
- training lineage digest
- no runtime attach guard

## Closed

- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual adapter artifact candidate write from target artifact store.
