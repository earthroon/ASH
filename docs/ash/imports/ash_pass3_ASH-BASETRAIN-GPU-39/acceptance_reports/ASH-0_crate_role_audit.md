# ASH-0 crate role audit / ash_core SSOT boundary seal

## Status
PASS_STATIC / PASS_ASH_CORE_ROLE_AUDIT

## Boundary
`crates/ash_core` is sealed as the Ash domain decision crate. It owns identity, capability, synapse registry contracts, runtime attachment plans, curriculum route metadata, failure replay metadata, promotion decisions, and decision traces.

## Current dependency surface
- anyhow
- policy
- serde
- sha2

## Forbidden dependencies
- runtime
- model_core
- lora_train
- artifact_store
- orchestrator_local
- burn
- wgpu
- safetensors

## Current ash_core inventory
- State: AshCore, AshStateBus, ConversationState, StateVectorV1, IdentityRhythm, ExistentialState
- Decision: AshDecisionEngine, AshDecisionInput, AshDecision, AshPromptAnalysis, AshDecisionTrace, AshGateDecision, AshGenerationPolicy
- Memory: ContractMemoryStore, LexStableStore, LexGraphStore, EligibilityKernel, ReactorKernel
- LoRA: LoraSummary
- Policy: AshRuntimePolicy, AshCorePolicyContext

## Runtime readiness finding
`runtime` can load `RuntimeLoraAttachment` JSON paths, but it does not directly consume promoted `runtime_adapter_registry.json` yet.

## Artifact store readiness finding
`artifact_store` can write JSON and list root files, but it does not yet manage promoted adapter lifecycle, adapter copy, rollback, or current/promoted pointers.

## Orchestrator overlap finding
`orchestrator_local` currently handles `lora_json_paths` and output fields such as selected/attached/missing LoRA ids. Future synapse routing decisions must remain in `ash_core`; `orchestrator_local` should execute plans, not decide synapse semantics.

## Guards
- `ash_core` must not run GPU training kernels.
- `ash_core` must not run runtime forward passes.
- `ash_core` must not parse safetensors adapter weights.
- `ash_core` must not copy promoted adapter files.
- `ash_core` must not silently remap `target_key`.
- `ash_core` must not silently approve missing adapters.

## Rust-native validation
- `crates/ash_core/tests/ash_0_boundary.rs`
- `crates/ash_core/src/bin/ash_core_audit.rs`

No Python validator is added for ASH-0.

## Next
- ASH-1 AshIdentity + Capability schema seal
- ASH-2 Adapter Synapse Registry seal
- ASH-3 Runtime Attachment Plan contract
