# ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R1
# Strict Last-Logits Access Policy Inheritance / Native GPU Argmax Worker Admission / Zero CPU Materialize Promotion Seal

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R1_STRICT_LAST_LOGITS_ACCESS_POLICY_INHERITANCE_NATIVE_GPU_ARGMAX_WORKER_ADMISSION_ZERO_CPU_MATERIALIZE_PROMOTION_SEAL`
- Parent context: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1`
- Canonical policy ID: `strict_same_device_gpu_last_logits_v1`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2`
- R8-R2-R3 authorization: `false`
- R8-R3 authorization: `false`
- R4-R5-R2 authorization: `false`
- Legacy removal/retirement: `false`
- General production apply: `false`

## Problem

A route-isolated native GPU worker emitted:

```text
[tensorcube][cpu_materialize]
mode=warn
scope=greedy_fallback
allowed=true
materialized=true
reason=lazy_gpu_last_row_to_cpu_row
```

The child-process boundary lost the previous strict last-logits policy and resolved the process-local default `warn` policy. Native GPU argmax was also controlled by an ambient environment switch and could silently return to disabled.

## SSOT repair

Ambient environment is not policy authority.

The canonical chain is:

```text
explicit sealed policy
→ coordinator-resolved policy digest
→ single-use worker policy envelope
→ explicit child CLI policy
→ child admission receipt
→ generation policy digest
→ final promotion reducer
```

Environment variables may mirror the sealed policy for compatibility with existing model code, but any conflict rejects worker admission before GPU creation.

## Required policy

```text
policy_id=strict_same_device_gpu_last_logits_v1
health_mode=strict
allow_cpu_materialize=false
allow_host_upload_fallback=false
require_same_device_raw=true
fail_closed_on_cpu_materialize=true
require_native_gpu_argmax_for_greedy=true
allow_policy_downgrade=false
```

Missing fields are not filled with `warn` or permissive defaults. The worker is rejected.

## Worker admission

Admission occurs before:

```text
model load
WGPU adapter request
WGPU device creation
CubeCL stream creation
first model dispatch
first logits access
```

Required digest equality:

```text
coordinator policy digest
== worker launch token policy digest
== child CLI policy digest
== worker-resolved policy digest
```

A mismatched environment mirror, stale token, missing field, policy downgrade, warn mode, or permissive mode rejects admission.

## Greedy route authority

Routes:

```text
greedy_cached
greedy_streaming
```

Required:

```text
native GPU argmax enabled
native GPU argmax dispatched for every selected token
native GPU argmax authoritative
CPU greedy fallback never entered
host-upload fallback never entered
```

If native GPU argmax is unavailable, the generation returns HOLD with zero contribution. It may not fall back to CPU.

## Sampled route authority

Routes:

```text
sampled_cached
sampled_streaming
```

Required:

```text
GPU sampler selected-token path active
full last-logits CPU materialization=0
host-upload fallback=0
same-device sampler input=true
```

`full_logits_compat_top_k_merge` must be classified as GPU-resident or CPU-materializing. CPU-materializing compatibility is non-promotable.

## Zero materialization seal

PASS requires:

```text
cpu_materialize_requested_count=0
cpu_materialize_executed_count=0
host_upload_fallback_requested_count=0
host_upload_fallback_executed_count=0
warn_worker_admission_count=0
permissive_worker_admission_count=0
```

Telemetry-only enforcement is forbidden. A forbidden access attempt aborts the generation before authoritative commit.

## Route and cohort matrix

Required worker matrix:

```text
4 live route workers
12 performance cohort-route workers
16 strict admissions total
```

Smoke minimum per route:

```text
100 generations
2500 selected tokens
```

All workers must use a fresh process and bind the exact same policy digest.

## Runtime changes

The implementation must:

```text
pass strict policy through child CLI
mirror strict mode and GPU argmax to the child environment
validate policy before GPU touch
fail closed in the shared isolated GPU probe
emit native GPU argmax authority telemetry
count and reject all CPU materialization and host-upload paths
preserve R8-R2-R2/R8-R2-R3/R4-R5-R2 authority as false
```

Canonical GPU argmax marker:

```text
[tensorcube][native_gpu_argmax] authoritative=true
```

## PASS authority

```text
r4_r5_r1_r8_r2_r2_r1_r1_strict_last_logits_policy_pass=true
r4_r5_r1_r8_r2_r2_r1_r2_authorized=true
```

Still false:

```text
r4_r5_r1_r8_r2_r3_authorized=false
r4_r5_r1_r8_r3_authorized=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r8_r2_r2_r1_r1_strict_last_logits_policy_inheritance_gate
```

## Next gate

```text
ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2
Strict Policy-Bound Readback Repair Rerun /
Zero CPU Materialize Route Matrix /
Sampled Shadow Serialization Revalidation Gate
```
