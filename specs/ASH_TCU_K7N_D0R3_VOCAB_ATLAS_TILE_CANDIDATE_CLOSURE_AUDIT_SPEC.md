# ASH-TCU-K7N-D0R3 SPEC

## Vocab Atlas Tile Candidate Closure Audit

## 1. Identity

- Patch: `ASH-TCU-K7N-D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT`
- Status: `PASS_ASH_TCU_K7N_D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT_NO_RAW_LEASE_NO_PIPELINE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- Path: `specs/ASH_TCU_K7N_D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT_SPEC.md`
- Class: candidate contract closure audit
- Next: `ASH-TCU-K7N-D1_SINGLE_SHADOW_CONSUMER_CONTRACT`

D0R3 seals the final candidate contract bundle. It does not export a Buffer, create a lease, allocate output, create a shader module or pipeline, dispatch TensorCube, read back output, compare parity, or replace Burn output.

## 2. Parent

Required D0R2R4 state:

- execution: `d0r2r4-2751587442ccccc1a848`
- eligibility: `eligible_for_d0r3_candidate_closure`
- prerequisite blockers: none
- strategy: `stride_aware_view`
- full tile: true
- ragged tail: false
- runtime execution authorized: false

Manifest: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2r4_local_manifest_latest.json`

## 3. Candidate SSOT

The closure contract contains:

1. final identity;
2. input and future output bindings;
3. bind-group and pipeline-layout schemas;
4. kernel identity;
5. logical tile, workgroup, and dispatch geometry;
6. CPU reference fixture;
7. future parity schema;
8. rollback, admission, and revocation;
9. zero-execution and protected-state evidence.

Required identity:

- callsite: `call-66cc14a91d31bf8452215b67`
- operation: `vocab_atlas_tile_projection`
- route: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- WGPU authority: `ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`
- output authority: `burn`
- runtime execution authorized: false

## 4. Binding Resolution

K6P canonical slot order is retained. The candidate WGSL replaces the historical control-array ABI with the sealed D0R2R2A 16-word ABI without changing slot ownership.

| Binding | Role | Type | Access |
|---:|---|---|---|
| 0 | LHS `[M,K]` stride `[K,1]` | storage | read-only |
| 1 | stored RHS `[N,K]`, logical `[K,N]` stride `[1,K]` | storage | read-only |
| 2 | future output `[M,N]` row-major | storage | read-write |
| 3 | 16-word params, 64 bytes | uniform | read-only |

Candidate source:

`crates/burn_webgpu_backend/src/shaders/tensorcube_k7n_d0r3_vocab_atlas_tile_candidate_16x16_kpanel4.wgsl`

Actual binding resources and layouts remain uncreated.

## 5. Output Contract

- shape: `[M,N]`
- dtype: `f32`
- stride: `[N,1]`
- span: `checked_mul(checked_mul(M,N),4)`
- future usage: `STORAGE | COPY_SRC`
- allocation authorized: false
- commit authorized: false
- authority: Burn

## 6. Kernel and Geometry

Geometry authority:

1. `tensorcube_k6p_row_major_emit_config.rs`
2. `tensorcube_k6p_row_major_emit_16x16_logical16_kpanel4.wgsl`
3. D0R3 candidate WGSL
4. D0R3 Rust mirrors

Required values:

- logical tile: `16x16`
- K panel: `4`
- workgroup: `16x16x1`
- invocation count: `256`
- dispatch X: `ceil_div(N,16)`
- dispatch Y: `ceil_div(M,16)`
- dispatch Z: `1`
- bounds guard: required
- ragged-tail dispatch: false
- Device-limit recheck at admission: true
- dispatch authorized: false

Logical tile and physical workgroup remain separately owned even when current X/Y values match.

## 7. ABI

The parameter ABI is the exact D0R2R2A contract:

- 16 scalar `u32`
- 64 bytes
- Rust/WGSL field-order parity
- binding-relative offsets
- RHS index: `rhs_offset + k * rhs_k_stride + n * rhs_n_stride`

ABI drift blocks D1 admission.

## 8. CPU Fixture

Fixture: `signed_asymmetric_m1_n3_k4_v1`

- M=1, N=3, K=4
- LHS: `[1.0,-2.0,0.0,3.0]`
- stored RHS rows:
  - `[2.0,1.0,-1.0,0.5]`
  - `[-3.0,0.0,4.0,2.0]`
  - `[1.0,-1.0,2.0,-2.0]`
- expected: `[1.5,3.0,-3.0]`

The fixture uses an independent scalar K-ascending loop and exposes transpose and stride errors. Burn matmul and GPU output cannot serve as the reference implementation.

## 9. Future Parity Schema

Required fields include candidate, kernel, binding, geometry, and fixture digests; Burn and TensorCube output digests; element and mismatch counts; NaN/Inf counts; error maxima; tolerance policy; state; and commit authorization.

D0R3 values:

- tolerance policy: `ash_tcu_k6p_f32_abs_rel_1e_5_v1`
- absolute/relative tolerance: `0.00001`
- state: `not_executed`
- output commit authorized: false

## 10. Rollback, Admission, Revocation

Rollback target: `burn_only_vocab_atlas_projection`.

Rollback cancels candidate admission and preserves evidence. It does not mutate Registry, advance route epoch, or delete artifacts.

Admission scope: `d1_single_shadow_consumer_contract_only`.

Current admission: false.

Revoke on digest drift, route-epoch change, Device loss, atlas replacement, weight change, parity failure, or Device-limit failure. Stale candidate reuse is forbidden.

## 11. Zero Execution

All counters remain zero:

- raw Buffer export, lease, or lease clone;
- binding resource, bind-group, or layout creation;
- shader module, pipeline layout, or compute pipeline;
- command encoder, Queue submission, or dispatch;
- output allocation, readback, parity, or commit;
- tensor copy or transpose materialization;
- Registry write, route mutation, or epoch change;
- runtime output or model-weight mutation;
- new Device or Queue.

## 12. Protected State

Hash before and after:

- D0R2R4 manifest, final seal, identity, and lineage;
- D0R2R3 LHS/RHS binding windows;
- D0R2R2A ABI source;
- Registry v4;
- raw bridge;
- K6P config and WGSL;
- candidate WGSL;
- Burn vocab-atlas projection.

Preserve:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

## 13. Implementation

Backend modules cover identity, input/output bindings, layouts, kernel identity, geometry, CPU fixture, parity, rollback, admission, revocation, closure, audit, and verdict.

Additional files:

- `shaders/tensorcube_k7n_d0r3_vocab_atlas_tile_candidate_16x16_kpanel4.wgsl`
- `model_core/src/vocab_atlas_tile_candidate_closure_contract.rs`
- `orchestrator_local/src/ash_tcu_k7n_d0r3_vocab_atlas_tile_candidate_closure_report.rs`
- `orchestrator_local/src/bin/ash_tcu_k7n_d0r3_vocab_atlas_tile_candidate_closure_audit.rs`

Focused tests cover identity, bindings, output span, layouts, kernel, geometry, dispatch, CPU fixture, parity, rollback/revocation, zero execution, and model integration.

## 14. Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r3_vocab_atlas_tile_candidate_closure_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2r4-pass `
  --require-d0r2r4-execution d0r2r4-2751587442ccccc1a848 `
  --require-d0r3-closure-eligibility `
  --require-no-current-prerequisite-blockers `
  --require-selected-strategy stride_aware_view `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --bind-final-candidate-identity `
  --verify-candidate-evidence-lineage `
  --bind-input-binding-schema `
  --bind-future-output-binding-schema `
  --bind-bind-group-layout-schema `
  --bind-pipeline-layout-schema `
  --bind-kernel-source-identity `
  --bind-kernel-entry-point-identity `
  --verify-k6p-config-shader-parity `
  --bind-logical-tile-geometry `
  --bind-physical-workgroup-geometry `
  --bind-dispatch-geometry `
  --reject-logical-workgroup-conflation `
  --require-runtime-device-limit-recheck `
  --verify-full-tile-dispatch-coverage `
  --build-cpu-reference-fixture `
  --verify-cpu-reference-fixture `
  --bind-future-parity-receipt-schema `
  --require-parity-state-not-executed `
  --bind-rollback-contract `
  --bind-admission-contract `
  --bind-revocation-contract `
  --classify-candidate-closure-eligibility `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-binding-resource `
  --require-no-bind-group-layout `
  --require-no-bind-group `
  --require-no-shader-module `
  --require-no-pipeline-layout `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-tensorcube-dispatch `
  --require-no-output-buffer `
  --require-no-readback `
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

## 15. PASS

Marker:

`PASS_ASH_TCU_K7N_D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT_NO_RAW_LEASE_NO_PIPELINE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`

Verdict:

`vocab_atlas_full_tile_candidate_contract_closed_with_final_identity_input_and_future_output_bindings_pipeline_layout_kernel_geometry_cpu_reference_parity_schema_rollback_admission_and_revocation_sealed_and_candidate_eligible_for_d1_single_shadow_consumer_contract_without_raw_lease_pipeline_dispatch_or_output_change`

Expected state:

```text
candidate_closure_eligibility=eligible_for_d1_single_shadow_consumer_contract
selected_strategy=stride_aware_view
full_tile_candidate=true
ragged_tail_candidate=false
output_authority=burn
runtime_execution_authorized=false
raw_buffer_lease_authorized=false
pipeline_creation_authorized=false
dispatch_authorized=false
parity_state=not_executed
```

## 16. Non-Authorization

D0R3 PASS does not authorize lease admission, output allocation, binding or pipeline creation, dispatch, readback, parity execution, output commit, ragged-tail execution, Registry registration, route-epoch change, promotion, performance claims, or production-readiness claims.

Only `ASH-TCU-K7N-D1_SINGLE_SHADOW_CONSUMER_CONTRACT` is authorized next.
