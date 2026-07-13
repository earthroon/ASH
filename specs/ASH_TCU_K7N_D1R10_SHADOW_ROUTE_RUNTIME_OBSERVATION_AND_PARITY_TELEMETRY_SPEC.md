# ASH-TCU-K7N-D1R10 SPEC

## Shadow Route Runtime Observation and Parity Telemetry

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R10_SHADOW_ROUTE_RUNTIME_OBSERVATION_AND_PARITY_TELEMETRY`
- Parent execution: `d1r9-51a514ce0aa90762af3d`
- Parent registry schema: `ash_tensorcube_shadow_route_registry_v1`
- Parent route epoch: `1`
- Required active route count: `17`
- Required holdlist count: `4`

Observation PASS:

```text
PASS_ASH_TCU_K7N_D1R10_SHADOW_ROUTE_RUNTIME_OBSERVATION_AND_PARITY_TELEMETRY_EVIDENCE_COMPLETE_BURN_AUTHORITY_PRESERVED_HEALTH_OUTCOME_SEALED
```

Hard failure:

```text
FAIL_ASH_TCU_K7N_D1R10_SHADOW_ROUTE_RUNTIME_OBSERVATION_AND_PARITY_TELEMETRY_OUTPUT_AUTHORITY_OR_RUNTIME_SAFETY_VIOLATION
```

D1R10 observes the D1R9 exact-signature shadow registry. It does not expand the whitelist and does not grant TensorCube output authority.

## 2. Parent SSOT

Required D1R9 state:

```text
execution_id=d1r9-51a514ce0aa90762af3d
registry_schema=ash_tensorcube_shadow_route_registry_v1
route_epoch=1
active_route_count=17
holdlist_count=4
holdlist_active_route_count=0
shadow_feature_enabled=true
output_authority=burn
rollback_armed=true
```

Required parent artifacts include the D1R9 local manifest, final seal, apply receipt, active shadow registry, route-epoch receipt, rollback authority and output-authority guard. Manifest immutable hashes and current registry bytes must reconcile before observation.

## 3. Ownership

D1R9 owns active route membership, signatures, holdlist, route epoch and rollback authority.

D1R10 owns runtime telemetry, sampled parity, overhead pairs, failure windows, route health, quarantine transactions and global rollback evidence.

Burn remains authoritative for model output, logits, sampler input, KV-state updates and downstream tensors. TensorCube owns non-authoritative shadow output and telemetry only.

## 4. Canonical Replay

```text
active routes=17
warmup invocations per route=16
measured exact-match attempts per route=128
total measured exact-match attempts=2176
```

Route ordering rotates each round, reverses on odd rounds and alternates Burn-first and TensorCube-first order. Every dispatch uses the same authoritative Burn adapter, device and queue.

## 5. Skip Coverage

```text
4 holdlist signatures x 16 attempts=64 holdlist skips
unknown signature skips>=32
stride mismatch skips>=16
shader digest mismatch skips>=16
ABI digest mismatch skips>=16
pipeline-layout mismatch skips>=16
runtime-authority mismatch skips>=16
```

Every skip executes Burn, skips TensorCube and records the reason. Range, wildcard, nearest-shape, category and dispatch-only matching are forbidden.

## 6. Sampled Parity

```text
sample every 16 successful shadow invocations
samples per route=8
total parity samples=136
```

Control `S00_CONTROL_M1_N16_K4` requires exact bit match. Non-control shapes require absolute and relative tolerance `0.00001`, zero failing elements, zero NaN or infinity mismatches and zero guard mutations. Parity readback is comparison-only.

## 7. Dispatch Health

Per route:

```text
attempt count=128
success rate>=0.99
maximum consecutive failures<3
rolling failure rate<=0.05 over 100 attempts
```

A shadow failure must preserve the successful Burn request and may not suppress Burn output.

## 8. Fault Injection

Required non-destructive injections:

```text
one synthetic shadow dispatch failure
one synthetic shadow timeout
one synthetic signature mismatch
```

Injected failures are excluded from natural rates but must prove Burn success and unchanged output authority.

## 9. Overhead Observation

```text
overhead pairs per route=32
total overhead pairs=544
```

Critical-path ratio is shadow-request Burn GPU time divided by Burn-only GPU time. Total occupancy ratio is Burn plus TensorCube GPU time divided by Burn-only GPU time.

Critical-path classes:

```text
green: median<=1.15 and p95<=1.25
amber: median<=1.35 and p95<=1.50 after missing green
red: median>1.35 or p95>1.50
```

Total occupancy is bounded at median `<=2.25` and p95 `<=2.75`. Resolution floor is `1000 ns` with timestamp multiplier `32`.

## 10. Route Health

Each signature receives one health receipt: `healthy`, `degraded`, `quarantine_required` or `rolled_back`.

Quarantine is required on three consecutive natural failures, rolling failure rate over five percent, sampled parity failure, NaN or infinity mismatch, guard mutation, red critical-path overhead, excessive occupancy or signature contradiction. Aggregate metrics cannot override an individual route failure.

## 11. Quarantine and Rollback

All quarantines found in one execution commit atomically:

```text
health: active -> quarantined
enabled: true -> false
membership retained
quarantine epoch increment count<=1
```

Global rollback is required for output-authority contamination, sampler or KV substitution, control parity or guard failure, registry or epoch corruption, shader/ABI/pipeline drift, runtime-authority drift, shadow-attributable device loss or out-of-memory, or model-weight mutation.

Global rollback disables all D1R9 shadow routes, restores Burn-only execution, advances the epoch monotonically and writes a rollback receipt. It does not emit the normal PASS marker.

## 12. Health Outcomes

Exactly one outcome is sealed:

```text
OUTCOME_ASH_TCU_K7N_D1R10_CONTINUE_17_SIGNATURE_SHADOW
OUTCOME_ASH_TCU_K7N_D1R10_CONTINUE_REDUCED_SIGNATURE_SHADOW
OUTCOME_ASH_TCU_K7N_D1R10_HOLD_SHADOW_SCOPE_NO_EXPANSION
OUTCOME_ASH_TCU_K7N_D1R10_GLOBAL_ROLLBACK_EXECUTED
```

Observation PASS and health outcome are separate.

## 13. Output Authority Boundary

```text
output_authority=burn
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
sampler_substitution_count=0
kv_state_mutation_count=0
runtime_output_changed=false
```

No outcome authorizes TensorCube production output, S15 admission, holdlist promotion, whitelist expansion or generalized model-speed claims.

## 14. Required Source Files

Backend modules:

```text
tensorcube_k7n_d1r10_parent_reconciliation.rs
tensorcube_k7n_d1r10_observation_schedule.rs
tensorcube_k7n_d1r10_route_invocation.rs
tensorcube_k7n_d1r10_runtime_observer.rs
tensorcube_k7n_d1r10_skip_telemetry.rs
tensorcube_k7n_d1r10_parity_sampler.rs
tensorcube_k7n_d1r10_parity_comparator.rs
tensorcube_k7n_d1r10_guard_telemetry.rs
tensorcube_k7n_d1r10_failure_window.rs
tensorcube_k7n_d1r10_overhead_pair.rs
tensorcube_k7n_d1r10_overhead_statistics.rs
tensorcube_k7n_d1r10_device_event.rs
tensorcube_k7n_d1r10_fault_injection.rs
tensorcube_k7n_d1r10_route_health.rs
tensorcube_k7n_d1r10_quarantine.rs
tensorcube_k7n_d1r10_global_rollback.rs
tensorcube_k7n_d1r10_output_authority_guard.rs
tensorcube_k7n_d1r10_observation_receipt.rs
tensorcube_k7n_d1r10_contract_audit.rs
tensorcube_k7n_d1r10_verdict.rs
```

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_runtime_observation_contract.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r10_runtime_observation_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r10_shadow_route_runtime_observation_and_parity_telemetry.rs
```

## 15. PASS Boundary

```text
parent evidence valid=true
observed route count=17
exact match request count=2176
parity sample count=136
route health receipt count=17
TensorCube authoritative output count=0
shadow output commit count=0
production output commit count=0
sampler substitution count=0
KV-state mutation count=0
Burn output authority preserved=true
global rollback executed=false
one health outcome selected=true
```

## 16. Next State

```text
continue 17 signatures -> ASH-TCU-K7N-D1R11_SHADOW_ROUTE_SUSTAINED_SOAK_AND_FAILURE_RECOVERY
continue reduced shadow -> ASH-TCU-K7N-D1R10-R1_QUARANTINED_SIGNATURE_REVIEW
hold without expansion -> ASH-TCU-K7N-D1R10-R2_OVERHEAD_OR_RESOLUTION_FOCUSED_REVIEW
global rollback -> ASH-TCU-K7N-D1R10-RB1_GLOBAL_ROLLBACK_POSTMORTEM_AND_CANDIDATE_REENTRY_POLICY
```

The canonical audit command is distributed with `d1r10_cargo_command.txt` and `run_ash_tcu_k7n_d1r10.ps1`; it binds all parent, schedule, parity, overhead, authority, quarantine and rollback gates defined above.