# ASH-TCU-K7N-D0 SPEC

## Title
Runtime Consumer / Shape / Layout / Resource Ownership Audit / Same-Device Feasibility / First Shadow Consumer Decision / No Execution Path Change Seal

## Patch ID
`ASH-TCU-K7N-D0_RUNTIME_CONSUMER_SHAPE_OWNER_AUDIT`

## Status Target
`PASS_ASH_TCU_K7N_D0_RUNTIME_CONSUMER_SHAPE_OWNER_AUDIT_NO_EXECUTION_PATH_CHANGE`

## Parent
- Patch: `ASH-TCU-K7N-C-R1F-R2`
- Package: `ash_pass3_ASH-TCU-K7N-C-R1F-R2_filesystem_order_canonicalization_fix_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip`
- SHA-256: `b71578834f80e8f1c45324294d4224df3beec6a05ce1eb50e0caa159b8d03588`
- Required prior status: `PASS_ASH_TCU_K7N_C_R1F_UNIT_TEST_MATRIX_TRUTH_REPAIR_FINAL_SEAL_NO_RUNTIME_CONSUMER_BINDING`

## Purpose
D0 inventories the actual ASH matmul/projection callsites and resolves shape, physical layout, route-read ownership, Device/Queue ownership, input/weight/output buffer ownership, fallback ownership, return-value ownership, same-device raw-buffer feasibility and WGPU type-generation compatibility. It recommends exactly one first shadow consumer or emits an explicit no-safe-candidate verdict.

D0 is audit-only. It must not bind a runtime consumer or change model output.

## Authoritative State
D0 must validate:

- Registry schema: `ash_tensorcube_route_registry_v4`
- Registry instance: `137787e9861968ec03c9fb11d440fe764d3dc5121491271b30e76fe80bc98b6d`
- Registry digest: `5e7657b88f6878405099abc078ea82841588361420989d1c3eeade67ec62edb3`
- Route epoch: `1`
- Candidate and Default: `ash_tcu_k6p_row_major_emit_candidate_v1`
- UserVisible and Production: `burn_baseline`
- Actual TensorCube runtime consumer count: `0`

Any mismatch is fail-closed. D0 must not silently repair or migrate parent truth.

## Scope
D0 may:

- scan Rust source and module graphs;
- register mandatory audit domains from one typed SSOT registry;
- inventory matmul, linear, attention, FFN, LM-head and vocab-atlas callsites;
- record static, symbolic or unknown M/N/K without guessing;
- record rank, dtype, layout, stride, transpose, batch, ragged and tail requirements;
- resolve Device, Queue, tensor, buffer, synchronization, fallback, error and return-value owners;
- classify same-device borrow feasibility and WGPU generation compatibility;
- rank candidate shadow consumers;
- generate deterministic local receipts, manifest and immutable artifact bundle from Rust.

D0 must not:

- dispatch TensorCube from a normal ASH model path;
- change any runtime return value;
- change Candidate, Default, UserVisible or Production bindings;
- mutate Registry v4 or create Registry v5;
- create an executable route resolver, pipeline cache or buffer pool;
- promote TensorCube output authority;
- remove Burn fallback;
- claim performance, quality, production readiness or Tensor Core execution;
- package pre-generated D0 manifests or runtime artifacts.

## Mandatory Audit Domains
The audit registry must cover at least:

- model construction and model forward;
- decoder block;
- attention projections and score/value matmul;
- FFN up, gate and down projections;
- generic linear/matmul wrappers;
- LM-head and vocab-atlas projection;
- training forward and backward-facing projection paths when present;
- inference, generation, sampler input and output publication;
- Burn-to-raw WGPU bridge;
- native WGPU runtime handles;
- Registry and runtime-context readers;
- detached K6P benchmark/parity execution.

A domain may contain zero consumers but may not be omitted.

## Reference Classification
Every discovered reference must be exactly one of:

- `control_plane_declaration`
- `audit_only_read`
- `test_only_read`
- `detached_migration`
- `detached_benchmark_or_parity`
- `runtime_support_utility`
- `actual_runtime_consumer`
- `candidate_runtime_consumer`
- `unclassified`

An `actual_runtime_consumer` must read/resolve a TensorCube route, dispatch TensorCube with real model inputs or weights, and allow the result to affect downstream output. All three conditions are required.

PASS requires `unclassified = 0` and `actual_runtime_consumer = 0`.

## Callsite, Shape And Layout Contract
Each callsite row must bind:

- repository-relative source path;
- module, symbol and parent symbol;
- operation kind and runtime domain;
- inference/training/generation reachability;
- current backend and output authority;
- shape record, ownership record and route-read record;
- stable source fingerprint.

Each shape record must bind M/N/K, batch, ranks, dtypes, accumulation dtype, physical layouts, transpose flags, contiguity, dynamic dimensions, ragged/tail requirement and evidence source.

Allowed dimension evidence is `compile_time_constant`, `model_config_constant`, `runtime_symbolic`, `runtime_observed_fixture`, `derived_from_tensor_shape` or `unknown`. Unknown values must remain unknown.

Every candidate must be compared against canonical K6P: `M=256`, `N=256`, `K=32`, `f32`, row-major output. A different semantic shape requires a new route identity.

## Ownership Contract
Every candidate must resolve:

- operation request owner;
- route snapshot and route-read owner;
- backend selection owner;
- Device and Queue owner;
- input and weight tensor/buffer owner or lease provider;
- output allocation owner;
- synchronization owner;
- fallback, parity and error owner;
- downstream return-value owner;
- teardown/device-loss owner.

Critical unknown ownership rejects the candidate.

## Same-Device And WGPU Compatibility
D0 must classify:

- NativeWgpuRuntimeHandles availability;
- Device/Queue identity;
- BurnToRawWgpuBridge reachability;
- strict same-device borrow support;
- buffer offsets, sizes, storage usage and alignment;
- tensor lifetime and output wrapping/copy contract;
- host upload/readback requirements;
- WGPU crate generation and feature compatibility.

Allowed same-device verdicts:
`same_device_zero_copy_feasible`, `same_device_copy_required`, `host_round_trip_required`, `type_generation_blocked`, `lifetime_blocked`, `usage_flag_blocked`, `insufficient_evidence`.

Allowed WGPU verdicts:
`compatible`, `adapter_required`, `feature_split`, `version_split`, `unknown`.

`transmute`, pointer reinterpretation and undocumented ABI assumptions are forbidden.

## Candidate Decision
D0 must evaluate all discovered viable candidates, including generic linear, FFN, attention, LM-head and vocab-atlas paths when present. Ranking dimensions include shape/layout determinism, same-device feasibility, comparator proximity, fallback simplicity, output containment, tail/batch complexity and blast radius.

Exactly one of the following must be produced:

1. one recommended first shadow consumer; or
2. `no_safe_first_shadow_consumer_identified`.

The current expected leading candidate is vocab-atlas tile projection, but it is not pre-authorized. D0 must prove its symbol, reachability, shape, layout and ownership from source.

A recommended candidate must preserve Burn output authority and prevent TensorCube output from reaching downstream.

## Local Artifact Boundary
The bake package contains source code only. It must not contain a pre-generated D0 manifest, latest receipt, immutable artifact bundle, runtime artifact or SHA sidecar.

The Rust audit binary must generate locally:

- immutable bundle: `artifacts/tensorcube/k7n_d0/<execution_id>/`
- latest mirrors: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d0_*_latest.json`
- local manifest binding immutable and latest paths with SHA-256 digests.

Required local artifacts include audit target registry, reference inventory, callsite inventory, shape/layout census, ownership map, route-read audit, same-device feasibility, WGPU compatibility, candidate ranking, candidate decision, protected-artifact guard, report, final seal, verdict and local manifest.

Canonical digests must exclude absolute paths, drive letters, host/user names, timestamps, target paths, hardware model and filesystem discovery order.

## Protected Artifact Guard
D0 must hash before and after:

- Registry v4;
- R1F final seal, test registry, summary and invariant coverage;
- R1E closure root;
- K7N-B prepared transaction;
- K7N-C commit and RuntimeRouteMutation evidence;
- R1A-R1E protected receipts;
- canonical K6P WGSL, config and row-major path.

PASS requires zero rewrites, Registry byte equality and K6P source byte equality.

## Required Implementation

- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0_runtime_consumer_shape_owner_audit.rs`
- `crates/burn_webgpu_backend/tests/ash_tcu_k7n_d0_runtime_consumer_shape_owner_audit.rs`
- `crates/orchestrator_local/src/ash_tcu_k7n_d0_runtime_consumer_shape_owner_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d0_runtime_consumer_shape_owner_audit.rs`

Required crate exports and Cargo bin registration may be added. Normal model callsites should remain untouched.

## Required Execution

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0_runtime_consumer_shape_owner_audit -- `
  --repo-root D:\1111113232\DUST\1\ash_pass3 `
  --parent-package D:\1111113232\DUST\1\ash_pass3_ASH-TCU-K7N-C-R1F-R2_filesystem_order_canonicalization_fix_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip `
  --require-parent-r1f-r2-sha `
  --require-r1f-pass `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --build-audit-target-registry `
  --scan-runtime-domains `
  --inventory-matmul-and-projection-callsites `
  --inventory-route-readers `
  --census-shapes-and-layouts `
  --resolve-resource-ownership `
  --audit-same-device-buffer-feasibility `
  --audit-wgpu-type-compatibility `
  --rank-first-shadow-consumer-candidates `
  --select-exactly-one-recommendation-or-explicit-none `
  --require-no-unclassified-references `
  --require-no-runtime-consumer `
  --verify-registry-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-protected-artifacts-unchanged `
  --write-audit-receipts `
  --write-final-seal `
  --no-execution-path-change `
  --no-runtime-dispatch `
  --no-route-mutation `
  --no-runtime-output-claim `
  --no-weight-mutation `
  --no-performance-claim
```

## PASS Conditions

- parent SHA and prior R1F PASS validated;
- Registry schema, instance, digest, epoch and bindings validated;
- all mandatory domains covered;
- duplicate target/callsite/shape/ownership counts are zero;
- all references classified and actual runtime consumer count remains zero;
- callsite, route-read, shape/layout, Device/Queue, buffer/output, fallback and return-value audits complete;
- same-device and WGPU compatibility classified;
- exactly one recommendation or explicit NONE verdict;
- runtime TensorCube dispatch count zero;
- TensorCube downstream output count zero;
- execution path, runtime output, route state, Registry and weights unchanged;
- protected artifact rewrite count zero;
- no performance claim.

## Final Verdicts
Recommended candidate:
`runtime_consumer_shape_and_resource_ownership_audited_and_one_shadow_consumer_recommended_without_execution_path_change`

No safe candidate:
`runtime_consumer_shape_and_resource_ownership_audited_but_no_safe_first_shadow_consumer_identified_without_execution_path_change`

Both are valid D0 audit outcomes when evidence is complete. Neither authorizes direct binding.

## Next-State Contract
D0 may authorize only:

- `ASH-TCU-K7N-D1_SINGLE_SHADOW_CONSUMER_CONTRACT_SSOT`; or
- `ASH-TCU-K7N-D0R_<BLOCKER>_PREREQUISITE_REPAIR` when no safe candidate exists.

D1 must bind one operation and one shape family with Burn authoritative and TensorCube shadow-only.