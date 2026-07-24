# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1

## Measurement Ring Capacity Argument Trace /
## Call-Site-to-Backend Exact Value Receipt /
## Domain-Capacity Pair Assertion /
## Opaque Ensure Diagnostic Closure Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r1.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1
measurement_capacity_trace_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1
input_identity_digest_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
promotion_scope=diagnostic_only
```

This revision does not change attention math, WGSL, query-atlas topology, route policy, performance thresholds, production capacity, or measurement capacity. It turns the previously opaque measurement-capacity failure into an exact value trace.

## 1. Failure binding

The R2 binary entered the first 512-token probe epoch and failed with:

```text
HeadwiseGuardDecisionMeasurementRingCapacityInvalid
```

The CLI, gate constant, and source-level backend constant all declared measurement capacity 64, but the error did not reveal the value received by the validator. No corrective capacity change is authorized until the first divergent layer is proven.

## 2. Domain-capacity contract

Domain and capacity are carried by one typed value:

```rust
pub struct HeadwiseGuardDecisionRingContract {
    pub domain: HeadwiseGuardDecisionRingDomain,
    pub capacity: u32,
}
```

Canonical contracts:

```text
Production: domain=production capacity=4 allowed range=3..16
MeasurementAudit: domain=measurement-audit capacity=64 exact
```

Production and measurement mutable runtimes remain isolated and share only the same native device and queue handles.

## 3. Capacity trace

The authoritative trace binds:

```text
trace_id
call_site
dispatcher_domain
requested_domain
requested_capacity
expected_capacity
telemetry_capacity
slot_index
build_revision
```

The gate emits a preflight line before the first probe. The backend emits one first-call line for Single slot 0 and one for GQA2 slot 32. Per-pair log flooding is forbidden.

## 4. Exact diagnostic errors

Measurement validation failures must include:

```text
trace_id
call_site
actual_domain
expected_domain
actual_capacity
expected_capacity
telemetry_capacity
slot_index
build_revision
```

The opaque value-free capacity ensure is retired from the authoritative path.

## 5. Semantic capacity separation

These capacities are separate SSOT fields and may not be substituted for one another:

```text
measurement decision ring=64
telemetry ring=4096
timestamp queries per round=128
timestamp readback ring=4
measurement snapshot ring=4
```

The named contract path prevents positional argument drift.

## 6. Static and runtime controls

R2-R1 inherits 880 controls and adds 40 trace controls:

```text
trace continuity=10
value propagation=10
diagnostic completeness=10
source/binary and API binding=10
total=920
```

Required aggregate:

```text
negative_control_count=920
negative_control_executed_count=920
negative_control_skipped_count=0
negative_control_fail_count=0
```

## 7. PASS boundary

PASS requires:

```text
CLI measurement capacity=64
measurement dispatcher domain=MeasurementAudit
measurement dispatcher capacity contract=64
backend validator expected capacity=64
trace ID and value continuity across the authoritative path
actual/expected values present in all capacity failures
production capacity remains 4 with range 3..16
no positional capacity drift
no runtime policy change
920 controls pass
static and digest truth pass
zero promotion and model-quality claims
```

PASS proves diagnostic closure only. It does not prove that the subsequent 64-slot runtime, timestamp queries, probe admission, production tails, or attention promotion pass.

## 8. Canonical diagnostic run

Use the R2-R1 gate with the same full R2 measurement contract and:

```text
--decision-token-ring-capacity 4
--measurement-decision-token-ring-capacity 64
--measurement-guard-snapshot-ring-capacity 4
--expected-negative-controls 920
```

Expected PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R1_MEASUREMENT_RING_CAPACITY_ARGUMENT_TRACE_CALL_SITE_TO_BACKEND_EXACT_VALUE_RECEIPT_DOMAIN_CAPACITY_PAIR_ASSERTION_OPAQUE_ENSURE_DIAGNOSTIC_CLOSURE_NO_RUNTIME_PROMOTION_CLAIM
```

Expected HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R1_MEASUREMENT_CAPACITY_TRACE_DOMAIN_PAIR_ASSERTION_OR_DIAGNOSTIC_CLOSURE_INCOMPLETE
```
