# ASH-TCU-K7N-D0R1 SPEC

## Generation-Scoped Route Snapshot / Shadow Observer Owner SSOT

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R1_GENERATION_SCOPED_ROUTE_SNAPSHOT_SHADOW_OBSERVER_OWNER_SSOT`
- Status target: `PASS_ASH_TCU_K7N_D0R1_GENERATION_SCOPED_ROUTE_SNAPSHOT_SHADOW_OBSERVER_OWNER_SSOT_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R1_GENERATION_SCOPED_ROUTE_SNAPSHOT_SHADOW_OBSERVER_OWNER_SSOT_SPEC.md`

## 2. Parent

Required parent:

- `ASH-TCU-K7N-D0_RUNTIME_CONSUMER_SHAPE_OWNER_AUDIT`
- implementation revision: `ASH-TCU-K7N-D0-R4`
- required status: `PASS_ASH_TCU_K7N_D0_RUNTIME_CONSUMER_SHAPE_OWNER_AUDIT_NO_EXECUTION_PATH_CHANGE`
- required verdict: `runtime_consumer_shape_and_resource_ownership_audited_but_no_safe_first_shadow_consumer_identified_without_execution_path_change`

D0R1 validates the current-tree D0 final seal, D0 local manifest, Registry v4, R1F final seal and protected artifacts. A parent ZIP is not required.

## 3. Purpose

D0 identified the vocab-atlas projection boundary as the leading first-shadow-consumer candidate, but the following owners remained unresolved:

1. generation-scoped route snapshot owner;
2. route read owner;
3. shadow parity observer owner;
4. shadow observation synchronization owner.

D0R1 establishes these owners as typed SSOT without authorizing TensorCube execution.

D0R1 does not resolve vocab-atlas M/N/K, physical layout, tail policy, route identity registration or WGPU type-generation compatibility. Those remain D0R2 scope.

## 4. Target Boundary

Target source:

`crates/model_core/src/native_wgpu.rs`

Target symbol:

`NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`

D0 callsite identity:

`call-66cc14a91d31bf8452215b67`

Operation family:

`vocab_atlas_tile_projection`

Existing Burn output remains authoritative.

## 5. Authoritative Registry State

D0R1 validates and snapshots:

- schema: `ash_tensorcube_route_registry_v4`
- instance: `137787e9861968ec03c9fb11d440fe764d3dc5121491271b30e76fe80bc98b6d`
- digest: `5e7657b88f6878405099abc078ea82841588361420989d1c3eeade67ec62edb3`
- epoch: `1`
- Candidate: `ash_tcu_k6p_row_major_emit_candidate_v1`
- Default: `ash_tcu_k6p_row_major_emit_candidate_v1`
- UserVisible: `burn_baseline`
- Production: `burn_baseline`

The Registry is read-only in D0R1.

K6P must not be silently aliased to the vocab-atlas operation. The normal D0R1 operation binding state is:

`unbound_requires_new_route_identity`

## 6. Scope

D0R1 may:

- deserialize and validate Registry v4;
- create one immutable snapshot per generation;
- pin that snapshot for the generation lifetime;
- store the cached-generation session in `DecodeState`;
- store the one-shot session in function scope;
- observe the vocab-atlas projection boundary;
- record logical shape metadata only;
- assign parity and synchronization owners;
- create local receipts, report, final seal and manifest from Rust.

D0R1 must not:

- call `Queue::submit`;
- create a compute pipeline or command encoder;
- dispatch TensorCube;
- lease a raw Burn/WGPU buffer;
- create or publish TensorCube output;
- compare Burn output with nonexistent shadow output;
- emit a parity success claim;
- modify Registry v4 or its epoch;
- change Candidate, Default, UserVisible or Production bindings;
- change Burn logits, token selection or returned tensor shape;
- claim performance, production readiness or Tensor Core execution.

## 7. State Ownership SSOT

### 7.1 Model lifetime

`NativeWgpuModel` owns exactly one:

`TensorCubeGenerationShadowObserverOwner`

The owner contains:

- immutable Registry v4 read authority;
- no-execution observer policy;
- generation session factory.

It does not own a current generation snapshot, TensorCube pipeline or output buffer.

### 7.2 Generation lifetime

A generation owns exactly one:

`TensorCubeGenerationShadowSession`

The session owns:

- `GenerationScopedTensorCubeRouteSnapshot`;
- `TensorCubeShadowParityObserver`;
- `TensorCubeShadowObservationSequencer`;
- counters;
- generation-local step ordinal;
- lifecycle state.

### 7.3 Cached generation

`DecodeState` owns:

`Option<ModelTensorCubeGenerationShadowSession>`

The session is created before prefill, used for prefill projection observation, moved into `DecodeState`, and reused for decode projections.

### 7.4 One-shot generation

`forward_logits_for_generation` owns a local session for the duration of the one-shot call.

### 7.5 Concurrency

Global mutable current-snapshot state is forbidden. Concurrent generations own separate session values and separate pinned snapshots. The shared Registry source is immutable.

## 8. Snapshot Contract

Schema:

`ash_tensorcube_generation_route_snapshot_v1`

Required fields:

- Registry schema, instance, digest and epoch;
- Candidate, Default, UserVisible and Production route IDs;
- operation binding state;
- canonical snapshot digest.

Snapshot creation rules:

1. validate typed Registry v4;
2. validate all four route bindings;
3. copy Registry identity and route slots;
4. set operation binding to `UnboundRequiresNewRouteIdentity`;
5. compute canonical domain-separated digest;
6. keep snapshot immutable for the generation lifetime.

Mid-generation Registry drift must not mutate the pinned snapshot.

## 9. Route Read Owner

`TensorCubeShadowRouteReadView` is the only route-read surface inside the generation session.

It may expose:

- route epoch;
- Registry digest;
- operation binding state.

It must not expose:

- execution backend selection;
- pipeline selection;
- route commit, rollback or epoch mutation;
- output authority selection.

A route read must not influence the Burn/TensorCube execution path in D0R1.

## 10. Shadow Observer Contract

The observer subject is fixed to:

- callsite: `call-66cc14a91d31bf8452215b67`
- symbol: `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`
- family: `vocab_atlas_tile_projection`

Allowed metadata:

- generation step ordinal;
- input row count;
- hidden size;
- atlas tile count;
- vocab size;
- Registry digest and epoch;
- Burn-authority-preserved flag.

Forbidden observation payload:

- logits contents;
- model weight contents;
- raw buffer contents;
- prompt or generated text;
- sampled token contents;
- timing or GPU timestamp values.

Observer ordering:

`before observation -> existing Burn projection -> after observation`

The observer cannot return or replace a tensor.

## 11. Parity Owner

D0R1 assigns the parity owner but performs no parity comparison.

Required receipt values:

- `shadow_output_available=false`
- `comparison_attempted=false`
- `comparison_passed=false`
- `comparison_failed=false`
- `parity_claim_emitted=false`

Allowed state:

- `blocked_unbound_operation_identity`; or
- `observation_ready_no_execution`.

## 12. Synchronization Owner

The synchronization mode is:

`cpu_observation_order_only_no_gpu_dispatch`

Required zero counters:

- queue submit;
- device poll;
- buffer map;
- GPU fence;
- TensorCube dispatch.

The sequencer proves only CPU-side before/after observation ordering. It does not claim GPU completion or cross-queue ordering.

## 13. Projection Integration

The existing Burn computation must remain semantically intact:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

The existing output construction must remain intact:

```rust
Tensor::<NativeInferenceBackend, 2>::from_data(
    TensorData::new(merged_logits, [1, atlas.vocab_size]),
    &self.device,
)
```

D0R1 may add only no-output observation calls before and after this computation.

The following must not change:

- atlas tile iteration order;
- `token_start` and `token_len` handling;
- merged-logits append order;
- top-k merge and best-token calculations;
- output device, dtype and dimensions;
- sampling input authority.

## 14. Required Counters

Per generation:

- snapshot create count: exactly `1`;
- route read count: at least `1` after observation;
- projection boundary observation count: at least `1` when vocab-atlas is reached;
- Burn projection completion count: equal to completed before observations.

Always zero:

- raw-buffer lease count;
- TensorCube dispatch count;
- TensorCube output count;
- parity comparison count;
- downstream output commit count;
- route mutation count;
- queue submit count;
- device poll count;
- buffer map count;
- GPU fence count.

## 15. Failure Policy

Registry schema, instance, digest, epoch or binding mismatch blocks session creation.

Normal inference must preserve the Burn path and emit an explicit blocked diagnostic. It must not silently switch to another TensorCube route.

The dedicated D0R1 audit binary treats any session, source-contract, protected-state or artifact failure as audit failure.

Runtime observer code must not synchronously write receipts. The dedicated audit binary owns filesystem artifact generation.

## 16. Required Implementation

Backend:

- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_generation_route_snapshot.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observation.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_no_dispatch_synchronization_owner.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_contract_audit.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_verdict.rs`

Model integration:

- `crates/model_core/src/tensorcube_generation_shadow_session.rs`
- `crates/model_core/src/native_wgpu.rs`
- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/lib.rs`

Orchestrator:

- `crates/orchestrator_local/src/ash_tcu_k7n_d0r1_generation_scoped_route_snapshot_shadow_observer_owner_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d0r1_generation_scoped_route_snapshot_shadow_observer_owner_audit.rs`

Focused tests:

- `crates/burn_webgpu_backend/tests/ash_tcu_k7n_d0r1_generation_route_snapshot.rs`
- `crates/burn_webgpu_backend/tests/ash_tcu_k7n_d0r1_shadow_observer_owner.rs`
- `crates/burn_webgpu_backend/tests/ash_tcu_k7n_d0r1_no_dispatch_synchronization.rs`
- `crates/model_core/tests/ash_tcu_k7n_d0r1_generation_shadow_session_integration.rs`

## 17. Required Tests

At minimum:

1. valid Registry v4 snapshot creation;
2. schema, instance, digest and epoch mismatch fail-closed;
3. deterministic snapshot digest;
4. operation binding remains unbound;
5. K6P is not aliased to vocab-atlas;
6. one session per cached generation;
7. one local session per one-shot generation call;
8. separate session snapshots are isolated;
9. route-read owner resolved;
10. parity owner resolved without comparison;
11. synchronization owner resolved without GPU work;
12. Burn matmul expression preserved;
13. merged logits ordering and return shape preserved;
14. all execution, mutation and output counters remain zero.

## 18. Protected State Guard

Hash before and after:

- Registry v4;
- R1F final seal;
- D0 local manifest;
- D0 final seal;
- D0 candidate decision;
- D0 ownership map;
- D0 shape/layout census;
- canonical K6P WGSL;
- K6P config and row-major path.

PASS requires zero protected-artifact rewrites.

The modified `native_wgpu.rs` is checked by semantic fingerprint rather than whole-file equality. The existing matmul, tile order, merged-logits append and return-shape expressions must remain present.

## 19. Local Artifacts

The source bake must not include pre-generated D0R1 runtime artifacts, manifests, receipts or SHA sidecars.

The Rust audit binary generates:

- immutable bundle: `artifacts/tensorcube/k7n_d0r1/<execution_id>/`
- latest mirrors: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r1_*_latest.json`
- local manifest: `ash_tensorcube_k7n_d0r1_local_manifest_latest.json`

Required artifact families:

- prior D0 receipt;
- generation route snapshot;
- owner assignment;
- route-read audit;
- shadow observer;
- parity owner;
- synchronization owner;
- generation lifecycle;
- concurrency isolation;
- protected-state guard;
- static checks;
- report;
- final seal;
- verdict;
- local manifest.

Canonical artifact digests exclude absolute paths, drive letters, user/host names, timestamps, process IDs, hardware identity and filesystem discovery order.

## 20. Required Execution

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r1_generation_scoped_route_snapshot_shadow_observer_owner_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0-pass `
  --require-d0-explicit-no-safe-candidate `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --target-vocab-atlas-projection-boundary `
  --create-generation-scoped-route-snapshot `
  --pin-snapshot-for-generation `
  --assign-route-read-owner `
  --assign-shadow-parity-observer-owner `
  --assign-no-dispatch-synchronization-owner `
  --integrate-generation-shadow-session `
  --verify-cached-generation-session-ownership `
  --verify-one-shot-generation-session-ownership `
  --verify-concurrent-session-isolation `
  --require-unbound-vocab-atlas-route-identity `
  --require-burn-output-authority `
  --require-no-raw-buffer-lease `
  --require-no-tensorcube-dispatch `
  --require-no-parity-comparison `
  --require-no-downstream-output-commit `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-audit-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 21. PASS Conditions

- D0 PASS and explicit no-safe-candidate verdict validated;
- Registry v4 typed validation succeeds;
- route epoch is exactly `1`;
- model-lifetime owner exists exactly once per model;
- generation-lifetime session owns snapshot, route reader, parity observer and sequencer;
- cached generation stores session in `DecodeState`;
- one-shot generation owns a local session;
- snapshot creation count is one per generation;
- operation route identity remains unbound;
- Burn output remains authoritative;
- protected Registry and K6P state remains unchanged;
- raw lease, dispatch, shadow output, comparison, output commit and route mutation counts are zero;
- no parity, performance, production or Tensor Core execution claim is emitted.

## 22. Final Verdict

`generation_scoped_route_snapshot_route_read_shadow_parity_observer_and_no_dispatch_synchronization_owners_established_for_vocab_atlas_projection_without_tensorcube_execution_or_runtime_output_change`

## 23. Explicit Non-Authorization

D0R1 PASS does not authorize:

- TensorCube dispatch;
- raw-buffer lease;
- vocab-atlas route registration;
- shape/layout/tail closure;
- Burn/TensorCube parity execution;
- D1 consumer binding;
- any route slot or epoch change.

## 24. Next State

Only the following patch is authorized after D0R1 PASS:

`ASH-TCU-K7N-D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT`

D0R2 must close vocab-atlas route identity, M/N/K evidence, physical layouts, swapped RHS layout, full-tile versus ragged-tail policy, stride/transpose requirements, raw-buffer lease preconditions and WGPU generation compatibility before D1 may begin.
