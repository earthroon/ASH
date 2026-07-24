# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2

## Forced-Route Parity Dispatcher Ownership Separation /
## Production Capacity-4 Runtime Rebind /
## Measurement Audit Runtime Non-Escape /
## Cross-Domain Legacy Call Elimination Seal

## Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r2.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2
measurement_capacity_trace_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R1
forced_route_parity_ownership_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R2
promotion_scope=incremental_decode_only
```

## Proven failure

R2-R1 proved that CLI, gate, backend constant and measurement wrapper all carried `MeasurementAudit/64`. The first divergence was a second legacy production call entering the same MeasurementAudit dispatcher with capacity 4. The nonce and call site bind the divergence to `forced_route_parity_pass`. Therefore the defect is dispatcher ownership leakage, not measurement-capacity forwarding.

## Dispatcher SSOT

```text
production_dispatcher:
  domain=Production
  capacity=4
  owns=forced parity, canary, rollback, production cases, promoted decode

measurement_dispatcher:
  domain=MeasurementAudit
  capacity=64
  owns=query-atlas timing spans and measurement telemetry only
```

Both dispatchers share one native adapter, device and queue. Mutable guard runtime, ring buffers, slot state and telemetry state remain distinct.

## Probe API

`run_crossover_probe_epoch` must receive two explicitly named dispatcher references:

```rust
fn run_crossover_probe_epoch(
    measurement_dispatcher: &HeadwiseAtlasDispatcher,
    parity_dispatcher: &HeadwiseAtlasDispatcher,
    ...
)
```

Measurement span calls use `measurement_dispatcher`. Single and GQA2 forced-route parity calls use `parity_dispatcher`.

Required preconditions:

```text
measurement domain=MeasurementAudit
parity domain=Production
runtime identities differ
same device and queue=true
```

## Forced parity preservation

Moving parity to the production dispatcher must preserve the same Q/K/V fixture, position snapshot, route identity, nonce derivation, reference output and tolerance.

```text
forced parity domain=Production
forced parity ring capacity=4
forced parity measurement-slot use=0
forced parity inside timestamp span=0
forced parity samples in performance population=0
```

## Measurement runtime non-escape

The measurement-rooted call graph may reach measurement-span encoding and measurement telemetry only. It may not reach forced-route guarded output, generic production helpers, canary, rollback or production cases.

```text
measurement_runtime_escape_edge_count=0
cross_domain_legacy_call_count=0
authoritative_legacy_trace_id_count=0
```

## Query-atlas preservation

```text
pairs_per_round=32
timestamps_per_pair=4
queries_per_round=128
queue_submit_count_per_round=1
query_resolve_count_per_round=1
per_pair_submit_count=0
per_sample_timestamp_readback_count=0
```

Forced parity executes only after query-atlas evidence and measurement telemetry are sealed. Its submissions and samples are excluded from query-atlas and production performance populations.

## Static truth

Executable checks must prove:

```text
run_crossover_probe_epoch has measurement_dispatcher and parity_dispatcher
measurement spans use measurement_dispatcher
forced parity uses parity_dispatcher
main passes &measurement_dispatcher then &production_dispatcher
forced_route_parity_pass asserts Production domain
production capacity remains 4
measurement capacity remains 64
```

Comments and specification strings cannot satisfy these checks.

## Negative controls

R2-R2 inherits 920 controls and adds 40 ownership controls:

```text
dispatcher parameters=10
measurement escape=10
production parity=10
isolation and identity=10

total=960
executed=960
skipped=0
fail=0
```

## PASS boundary

PASS requires exact R2-R1 source binding, distinct production and measurement dispatcher/runtime identities, same device and queue, production capacity 4, measurement capacity 64, two-parameter probe API, forced parity production binding, zero measurement escape edges, zero cross-domain legacy calls, unchanged parity semantics, preserved query-atlas truth, performance and tail gates, 960 controls, static truth and artifact digest truth.

PASS does not prove universal cross-adapter crossover, zero benchmark waits outside measured spans, native indirect o-proj, transactional KV rollback, canonical full-model decode or model-quality improvement.

Expected PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R2_FORCED_ROUTE_PARITY_DISPATCHER_OWNERSHIP_SEPARATION_PRODUCTION_CAPACITY4_RUNTIME_REBIND_MEASUREMENT_AUDIT_RUNTIME_NON_ESCAPE_CROSS_DOMAIN_LEGACY_CALL_ELIMINATION_QUERY_ATLAS_AND_PARITY_TRUTH_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

Expected HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R2_FORCED_ROUTE_PARITY_DISPATCHER_OWNERSHIP_OR_MEASUREMENT_RUNTIME_NON_ESCAPE_INCOMPLETE
```
