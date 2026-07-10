# ASH-TCU-K7N-A SPEC

## Title

Central Route Registry SSOT / Runtime-Owned Route Catalog Binding Epoch And Genesis Snapshot / Explicit Bootstrap Baseline / No Route Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7N-A
```

## Status Target

```txt
PASS_ASH_TCU_K7N_A_CENTRAL_ROUTE_REGISTRY_SSOT_EXPLICIT_BOOTSTRAP_NO_ROUTE_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent

```txt
ASH-TCU-K7M-C
```

Required prior status:

```txt
PASS_ASH_TCU_K7M_C_EXECUTION_EVIDENCE_BINDING_ACTUAL_GPU_MEASUREMENT_NO_HISTORICAL_BACKFILL_NO_ROUTE_MUTATION_SEAL
```

Required prior verdict:

```txt
current_tensorcube_gpu_execution_measurement_and_parity_evidence_bound_no_historical_event_backfill
```

## Purpose

K7N-A installs one runtime-owned TensorCube route registry. Before K7N-A, route-related state is distributed across receipts, activation records, rollback records, and annotations. K7N-A creates a single live state owner for route catalog, candidate/default/user-visible/production bindings, registry epoch, registry identity, genesis snapshot, canonical digest, rollback stack, and mutation ledger.

The live registry must be owned by `TensorCubeRuntimeContext` through `Arc<RwLock<TensorCubeRouteRegistry>>`. Orchestrator JSON and receipts are evidence mirrors only and must not become alternative writable state owners.

K7N-A creates genesis state from explicit bootstrap input. It does not infer live state from legacy receipts, adopt a route, mutate default/user-visible/production routes, execute rollback, change runtime output, replace production, mutate weights, or promote a performance claim.

## State Ownership

```txt
TensorCubeRuntimeContext
└── Arc<RwLock<TensorCubeRouteRegistry>>
```

Forbidden ownership patterns:

```txt
process-global mutable static
hidden OnceLock route state
orchestrator-owned live route map
receipt-only route selection
silent environment-variable fallback
legacy receipt inference as runtime truth
```

## SSOT

Runtime owner:

```txt
crates/burn_webgpu_backend/src/tensorcube_runtime_context.rs
```

Registry schema owner:

```txt
crates/burn_webgpu_backend/src/tensorcube_route_registry.rs
```

Runtime mirror:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7n_a_central_route_registry_latest.json
```

Genesis snapshot:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7n_a_registry_genesis_snapshot_latest.json
```

Schema version:

```txt
ash_tensorcube_route_registry_v1
```

## Route Types

K7N-A must define:

```rust
pub struct TensorCubeRouteId(String);

pub enum TensorCubeRouteKind {
    BurnBaseline,
    TensorCubeCandidate,
    TensorCubeShadow,
    Disabled,
}

pub enum TensorCubeRouteLifecycle {
    Registered,
    CapabilityProven,
    EligibleForReview,
    Adopted,
    Retired,
    Quarantined,
}

pub enum TensorCubeRouteSlot {
    Candidate,
    Default,
    UserVisible,
    Production,
}

pub enum TensorCubeRouteBindingSource {
    ExplicitBootstrap,
    RuntimeMutation,
    RollbackRestore,
}
```

Route IDs must be non-empty ASCII, at most 128 bytes, contain only lowercase letters, digits, underscore, dash, or dot, contain no whitespace or path separators, and must not equal `unknown` or `implicit`. Invalid IDs must fail without silent normalization.

## Route Catalog

Required initial routes:

```txt
burn_baseline
ash_tcu_k6p_row_major_emit_candidate_v1
```

Burn baseline:

```txt
kind = BurnBaseline
lifecycle = Registered
```

TensorCube candidate:

```txt
kind = TensorCubeCandidate
lifecycle = CapabilityProven
candidate_identity = ash_tcu_k6p_row_major_emit_candidate_v1
```

Candidate capability fields must be read from K7M-C:

```txt
execution ID
dispatch digest
readback digest
CPU parity proven
Burn parity proven
```

They must not be hardcoded.

## Explicit Bootstrap

All four slot bindings must be supplied explicitly by CLI or caller configuration:

```txt
candidate
default
user-visible
production
```

Recommended explicit baseline:

```txt
candidate = ash_tcu_k6p_row_major_emit_candidate_v1
default = burn_baseline
user-visible = burn_baseline
production = burn_baseline
```

This is not an implicit fallback. The audit must fail if any binding is omitted or references a route absent from the catalog.

Genesis binding fields:

```txt
binding_source = ExplicitBootstrap
bound_at_epoch = 0
bound_by_patch = ASH-TCU-K7N-A
explicit_operator_input = true
runtime_mutation_evidence_id = none
```

## Registry

```rust
pub struct TensorCubeRouteRegistry {
    pub registry_schema_version: String,
    pub registry_instance_id: String,
    pub epoch: u64,
    pub catalog: BTreeMap<TensorCubeRouteId, TensorCubeRouteCatalogEntry>,
    pub bindings: BTreeMap<TensorCubeRouteSlot, TensorCubeRouteBinding>,
    pub rollback_stack: Vec<TensorCubeRouteSnapshot>,
    pub mutation_ledger: Vec<TensorCubeRouteMutationRecord>,
    pub mutation_enabled: bool,
    pub genesis_digest: String,
    pub current_registry_digest: String,
}
```

Canonical ordering is mandatory. `BTreeMap` and stable serialization must ensure deterministic digests. HashMap iteration order must not affect digests.

Genesis requirements:

```txt
epoch = 0
mutation_enabled = false
rollback_stack.len() = 0
mutation_ledger.len() = 0
```

The genesis snapshot must not be pushed into the rollback stack.

## Digest Policy

K7N-A must produce distinct non-empty:

```txt
catalog_digest
bindings_digest
genesis_digest
current_registry_digest
```

The current registry digest must cover schema version, registry instance ID, epoch, catalog, bindings, rollback stack, mutation ledger, mutation-enabled state, and genesis digest while excluding its own digest field.

Genesis digest must cover schema version, explicit bootstrap digest, initial catalog, initial bindings, epoch zero, empty rollback stack, empty mutation ledger, mutation disabled state, and K7M-C capability evidence identifiers.

## Runtime Context

```rust
#[derive(Clone)]
pub struct TensorCubeRuntimeContext {
    route_registry: Arc<RwLock<TensorCubeRouteRegistry>>,
}
```

Required read-only API:

```rust
route_registry_handle
route_snapshot
current_route
registry_epoch
registry_digest
```

K7N-A must not expose an unrestricted mutable reference. Lock poisoning must return `RegistryLockPoisoned`; it must not recreate defaults, reset epoch, or fall back to receipts.

## Mutation Disabled Probe

K7N-A may define the future mutation-record schema, but all mutation attempts must return `MutationDisabled` and leave state unchanged.

The audit must:

```txt
construct runtime context
read all four slots
read epoch and digest
serialize and deserialize snapshot
verify canonical digest stability
attempt forbidden mutation
confirm MutationDisabled
read registry again
```

Required invariants:

```txt
epoch before = 0
epoch after = 0
registry digest unchanged
bindings unchanged
mutation ledger remains empty
rollback stack remains empty
```

## Snapshot Integrity

K7N-A must prove:

```txt
schema version valid
registry instance ID present
catalog route count >= 2
all four slots present
all bound routes exist in catalog
all binding sources are explicit bootstrap
epoch = 0
mutation disabled
mutation ledger empty
rollback stack empty
catalog/bindings/genesis/current digests valid
serialize-deserialize roundtrip valid
canonical digest stable after roundtrip
```

The JSON snapshot is an evidence mirror only. Automatic restore from JSON is out of scope.

## No-Mutation Guards

K7N-A must prove:

```txt
default route adoption = false
user-visible route adoption = false
production route adoption = false
route mutation transaction started = false
route mutation transaction committed = false
route epoch incremented = false
runtime route mutation evidence created = false
production replacement executed = false
runtime decode output changed = false
assistant message output changed = false
rollback executed = false
model weights mutated = false
optimizer state mutated = false
safetensors checkpoint mutated = false
performance claim allowed = false
```

Genesis bootstrap is not runtime mutation evidence.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_route_id.rs
crates/burn_webgpu_backend/src/tensorcube_route_kind.rs
crates/burn_webgpu_backend/src/tensorcube_route_lifecycle.rs
crates/burn_webgpu_backend/src/tensorcube_route_slot.rs
crates/burn_webgpu_backend/src/tensorcube_route_binding_source.rs
crates/burn_webgpu_backend/src/tensorcube_route_catalog_entry.rs
crates/burn_webgpu_backend/src/tensorcube_route_binding.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry_bootstrap.rs
crates/burn_webgpu_backend/src/tensorcube_route_snapshot_kind.rs
crates/burn_webgpu_backend/src/tensorcube_route_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_route_mutation_record.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry_error.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry.rs
crates/burn_webgpu_backend/src/tensorcube_runtime_context.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_prior_k7m_c_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_route_registry_schema.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_route_catalog.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_explicit_bootstrap_intent.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_runtime_owner_binding.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_registry_epoch_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_registry_genesis_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_registry_snapshot_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_registry_read_only_probe.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_no_route_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_no_runtime_output_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_a_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7n_a_central_route_registry_ssot_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_a_central_route_registry_ssot_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_a_central_route_registry_ssot_audit -- --repo-root <repo> --require-k7m-c-pass --bootstrap-candidate-route ash_tcu_k6p_row_major_emit_candidate_v1 --bootstrap-default-route burn_baseline --bootstrap-user-visible-route burn_baseline --bootstrap-production-route burn_baseline --create-central-route-registry --bind-runtime-owner --create-genesis-snapshot --verify-canonical-registry-digest --run-read-only-registry-probe --require-mutation-disabled --no-route-adoption --no-production-replacement --no-runtime-output-claim --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_A_PRIOR_K7M_C_RECEIPT
PASS_ASH_TCU_K7N_A_ROUTE_REGISTRY_SCHEMA
PASS_ASH_TCU_K7N_A_ROUTE_CATALOG
PASS_ASH_TCU_K7N_A_EXPLICIT_BOOTSTRAP_INTENT
PASS_ASH_TCU_K7N_A_RUNTIME_OWNER_BINDING
PASS_ASH_TCU_K7N_A_REGISTRY_EPOCH_POLICY
PASS_ASH_TCU_K7N_A_REGISTRY_GENESIS_SNAPSHOT
PASS_ASH_TCU_K7N_A_REGISTRY_SNAPSHOT_INTEGRITY
PASS_ASH_TCU_K7N_A_REGISTRY_READ_ONLY_PROBE
PASS_ASH_TCU_K7N_A_MUTATION_DISABLED
PASS_ASH_TCU_K7N_A_NO_ROUTE_ADOPTION
PASS_ASH_TCU_K7N_A_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7N_A_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_A_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_A_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_A_CENTRAL_ROUTE_REGISTRY_SSOT_EXPLICIT_BOOTSTRAP_NO_ROUTE_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

Measured IDs and digests must come from the actual K7M-C receipt and actual registry instance. They must not be hardcoded.

## Recommended Next Patch

```txt
ASH-TCU-K7N-B
Route Epoch And Hash Transaction Receipt / Runtime-Owned Mutation Proposal Validation / Before And After Snapshot Digest / No Default User-Visible Or Production Adoption Seal
```

## Final Seal

K7N-A creates a single runtime-owned route registry at genesis epoch zero from explicit bootstrap input. Mutation is disabled. Legacy receipts remain evidence only. K7N-A does not adopt routes, replace production, alter runtime output, execute rollback, mutate weights, or promote performance claims.
