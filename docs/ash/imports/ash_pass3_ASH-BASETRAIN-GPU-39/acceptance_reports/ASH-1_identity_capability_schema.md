# ASH-1 AshIdentity + Capability schema seal

## Status
PASS_STATIC / PASS_ASH_IDENTITY_CAPABILITY_SCHEMA

## Sealed
- AshIdentityProfile
- LanguageProfile
- BehaviorProfile
- AshCapability
- AshCapabilityRegistry
- CapabilityTargetModule
- CapabilityEvalGate
- CapabilityRuntimeCondition

## Required capabilities
- korean_response_stability
- context_binding
- logic_repair
- runtime_attach_integrity

## Boundary
ash_core owns identity/capability schema.
ash_core does not load adapter weights.
ash_core does not run runtime forward.
ash_core does not run GPU training kernels.
ash_core does not copy promoted adapter files.

## Validation
- cargo test -p ash_core ash_1_identity_capability
- cargo run -p ash_core --bin ash_identity_capability_audit

## Python
No Python validator is allowed for ASH-1.
