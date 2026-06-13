# ASH-8 Public API / CLI bridge

## Status
PASS_STATIC / PASS_ASH_PUBLIC_API_CLI_BRIDGE

## Sealed
- AshApiRequest
- AshApiResponse
- AshApiError
- AshApiContext
- AshCliCommand
- AshCliInput
- AshCliOutput
- ash_api CLI binary
- ash_public_api_audit binary

## Public API
- handle_ash_api_request
- ash_public_runtime_route
- ash_public_curriculum_route
- ash_public_replay_route
- ash_public_promotion_decision
- ash_public_default_attachment_plan

## CLI Commands
- identity
- capabilities
- synapses
- runtime-route
- curriculum-route
- replay-route
- promotion-decision
- audit-all

## Dependency boundary
- serde_json is allowed for Rust-native CLI/API JSON I/O.
- Python validators remain forbidden.
- ash_core must not depend on runtime, model_core, lora_train, artifact_store, orchestrator_local, burn, wgpu, or safetensors.

## Guards
- no runtime execution
- no LoRA training execution
- no safetensors loading
- no artifact copying
- no silent fallback
- no Python validator

## Re-bake note
- ASH-8 re-bake also removes a duplicate `intent` field in `runtime_router.rs` that could break compilation before the public API surface is added.

## Boundary
ash_core exposes decision APIs only. orchestrator/runtime/lora_train/artifact_store execute the decisions later.
