# ASH-2 Adapter Synapse Registry seal

## Status
PASS_STATIC / PASS_ASH_ADAPTER_SYNAPSE_REGISTRY

## Sealed
- AdapterPromotionStatus
- AdapterArtifactFamily
- AdapterTargetKey
- AshAdapterSynapse
- AshAdapterSynapseRegistry
- AshAdapterSynapseAuditReport

## Default registered adapter
- ash_lm_head_lora_promoted
- artifact_family = ModuleLora
- target_key = lm_head
- linked capabilities:
  - korean_response_stability
  - runtime_attach_integrity

## Guards
- adapter_id must be unique
- linked capability ids must exist in AshCapabilityRegistry
- promoted adapter must have manifest_path and model_path
- runtime_scale must be positive
- runtime_scale must not exceed 4.0
- custom target_key requires custom_target_key risk tag
- Python validator forbidden

## Boundary
ash_core stores adapter synapse metadata only.
ash_core does not load safetensors.
ash_core does not copy adapter files.
ash_core does not run runtime forward.
ash_core does not run GPU training kernels.

## Rust-native validation
- cargo test -p ash_core ash_2_adapter_synapse
- cargo run -p ash_core --bin ash_adapter_synapse_audit

## Next
ASH-3 Runtime Attachment Plan contract
