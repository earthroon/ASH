# ASH-TCU-K7N-D1R11 SPEC

## Shadow Route Sustained Soak and Failure Recovery

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R11_SHADOW_ROUTE_SUSTAINED_SOAK_AND_FAILURE_RECOVERY`
- Parent execution: `d1r10-ecb4a2d179c818e726a2`
- Parent outcome: `continue_17_signature_shadow`
- Parent route epoch: `1`
- Active exact-signature routes: `17`

PASS:

```text
PASS_ASH_TCU_K7N_D1R11_SHADOW_ROUTE_SUSTAINED_SOAK_AND_FAILURE_RECOVERY_LONG_HORIZON_STABLE_RECOVERY_DRILLS_VALID_BURN_AUTHORITY_PRESERVED
```

Hard failure:

```text
FAIL_ASH_TCU_K7N_D1R11_SHADOW_ROUTE_SUSTAINED_SOAK_AND_FAILURE_RECOVERY_RUNTIME_SAFETY_OR_RECOVERY_CONTRACT_VIOLATION
```

D1R11 performs sustained non-authoritative shadow observation and failure-recovery drills. It does not grant TensorCube production output authority.

## 2. Parent SSOT

Required D1R10 state:

```text
execution_id=d1r10-ecb4a2d179c818e726a2
health_outcome=continue_17_signature_shadow
route_epoch_after=1
observed_route_count=17
healthy_route_count=17
degraded_route_count=0
quarantined_route_count=0
parity_failing_sample_count=0
guard_mutation_count=0
output_authority=burn
```

The D1R10 manifest, final seal, observation receipt, route-health receipts and current D1R9 shadow registry must reconcile before GPU work.

## 3. Ownership and Isolation

D1R9 owns route membership, epoch semantics and rollback authority. D1R10 owns the short-horizon runtime baseline. D1R11 owns sustained telemetry, restart restoration, resource lifetime, natural quarantine decisions and isolated failure-recovery drills.

Burn remains authoritative for output, logits, sampler input, KV updates and downstream state. TensorCube remains non-authoritative shadow-only.

## 4. Sustained Soak Schedule

```text
soak epochs=8
segments=4
process restarts=3
warmup per route=64
measured attempts per route per epoch=512
measured attempts per route=4096
total measured exact matches=69632
```

Each segment runs in a fresh child process. The parent reloads and reconciles the disk registry between segments. Route epoch and membership must remain stable unless a natural quarantine is required after the complete soak.

## 5. Parity and Guard

```text
sample interval=64 successful measured shadow invocations
samples per route per epoch=8
samples per route=64
total samples=1088
absolute tolerance=0.00001
relative tolerance=0.00001
guard pattern=0x7FC12345
guard words>=16
```

The control shape requires exact-bit parity. Every route requires zero failing elements, zero NaN or infinity mismatches and zero guard mutations.

## 6. Resource Lifetime

At every epoch boundary:

```text
live temporary shadow buffers=0
live timestamp staging buffers=0
live parity readback buffers=0
mapped buffers=0
pending map callbacks=0
pending queue submissions=0
shadow buffer pool entries<=17
post-warmup pool growth=0
```

## 7. Overhead and Drift

```text
overhead pairs per route per epoch=8
overhead pairs per route=64
total overhead pairs=1088
```

Critical-path and total-occupancy ratios are separate. First-to-last epoch drift is sealed per signature. Aggregate statistics cannot hide a red route.

## 8. Natural Quarantine

Natural signature quarantine is required on three consecutive failures, rolling failure rate over five percent, parity failure, NaN or infinity mismatch, guard mutation, red critical-path overhead, excessive occupancy or route-specific resource leakage.

All naturally required quarantines commit atomically with at most one route-epoch increment. Route entries remain present and become `enabled=false`, `health=quarantined`.

D1R11 hardens the dormant D1R9 route-state validator so the already-defined active, quarantined and rolled-back states are valid only in their matching enabled/disabled combinations. Output authority rules remain unchanged.

## 9. Isolated Failure-Recovery Drills

Failure drills use `ash_tensorcube_shadow_route_drill_registry_v1` and never publish over the active registry.

Required drills:

```text
three-consecutive-failure quarantine
explicit quarantine recovery
six-percent rolling-failure quarantine
comparator-layer parity-failure quarantine
control-parity global rollback
post-rollback process restart
clean monotonic drill reset
```

The global rollback drill must restore Burn-only state and survive process restart.

## 10. Output Authority Boundary

```text
output_authority=burn
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
sampler_substitution_count=0
kv_state_mutation_count=0
```

No outcome authorizes whitelist expansion, holdlist promotion, S15 admission, TensorCube output commit or production readiness.

## 11. Outcomes

Exactly one outcome is sealed:

```text
OUTCOME_ASH_TCU_K7N_D1R11_CONTINUE_17_SIGNATURE_SHADOW
OUTCOME_ASH_TCU_K7N_D1R11_CONTINUE_REDUCED_SIGNATURE_SHADOW
OUTCOME_ASH_TCU_K7N_D1R11_HOLD_SHADOW_SCOPE_NO_EXPANSION
OUTCOME_ASH_TCU_K7N_D1R11_GLOBAL_ROLLBACK_EXECUTED
```

Observation PASS and the soak outcome are separate.

## 12. Required Source Files

Backend modules:

```text
tensorcube_k7n_d1r11_parent_reconciliation.rs
tensorcube_k7n_d1r11_soak_schedule.rs
tensorcube_k7n_d1r11_soak_invocation.rs
tensorcube_k7n_d1r11_soak_runtime.rs
tensorcube_k7n_d1r11_restart_restoration.rs
tensorcube_k7n_d1r11_parity_sampler.rs
tensorcube_k7n_d1r11_parity_drift.rs
tensorcube_k7n_d1r11_guard_telemetry.rs
tensorcube_k7n_d1r11_failure_window.rs
tensorcube_k7n_d1r11_overhead_pair.rs
tensorcube_k7n_d1r11_overhead_drift.rs
tensorcube_k7n_d1r11_resource_lifetime.rs
tensorcube_k7n_d1r11_memory_stability.rs
tensorcube_k7n_d1r11_device_event.rs
tensorcube_k7n_d1r11_natural_quarantine.rs
tensorcube_k7n_d1r11_drill_registry.rs
tensorcube_k7n_d1r11_signature_quarantine_drill.rs
tensorcube_k7n_d1r11_rolling_failure_drill.rs
tensorcube_k7n_d1r11_parity_failure_drill.rs
tensorcube_k7n_d1r11_global_rollback_drill.rs
tensorcube_k7n_d1r11_recovery_restoration.rs
tensorcube_k7n_d1r11_sustained_route_health.rs
tensorcube_k7n_d1r11_burn_authority_guard.rs
tensorcube_k7n_d1r11_soak_receipt.rs
tensorcube_k7n_d1r11_contract_audit.rs
tensorcube_k7n_d1r11_verdict.rs
```

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_sustained_soak_contract.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r11_sustained_soak_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r11_shadow_route_sustained_soak_and_failure_recovery.rs
```

## 13. PASS Boundary

```text
parent evidence valid=true
soak epoch count=8
restart count=3
measured exact-match count=69632
parity sample count=1088
parity failure count=0
guard mutation count=0
restart restoration success count=3
resource lifetime receipts=8
failure-recovery drills valid=true
tensorcube authoritative output count=0
shadow output commit count=0
production output commit count=0
actual global rollback executed=false
one soak outcome selected=true
```

## 14. Next State

```text
continue 17 signatures -> ASH-TCU-K7N-D1R12_SHADOW_ROUTE_PRODUCTION_LIKE_WORKLOAD_CANARY
continue reduced shadow -> ASH-TCU-K7N-D1R11-R1_NATURALLY_QUARANTINED_SIGNATURE_REVIEW
hold without expansion -> ASH-TCU-K7N-D1R11-R2_SOAK_DEGRADATION_AND_RESOURCE_LIFETIME_REVIEW
global rollback -> ASH-TCU-K7N-D1R11-RB1_ACTIVE_REGISTRY_ROLLBACK_POSTMORTEM_AND_REENTRY_POLICY
```

## 15. Audit Command

The canonical audit command is distributed with `d1r11_cargo_command.txt` and `run_ash_tcu_k7n_d1r11.ps1`. It binds all parent, soak, restart, parity, guard, resource-lifetime, overhead, natural-quarantine, drill-registry and Burn-authority gates defined above.
