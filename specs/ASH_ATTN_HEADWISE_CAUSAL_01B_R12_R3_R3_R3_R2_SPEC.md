# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2

## Measurement Guard Ring Domain Separation /
## 64-Slot Pair-Matrix Decision Runtime /
## Production Default Ring Preservation /
## Capacity-Mutation Isolation Seal

## Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2
parent_source_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
parent_runtime_evidence_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2
input_identity_digest_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
timestamp_measurement_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
```

## Failure binding

The R3-R1 binary compiled and entered the first 512-token probe epoch, then failed with `HeadwiseGuardDecisionRingCapacityInvalid`. The query-atlas probe requires 64 guarded spans per round, while the existing production ring contract admits only capacities 3 through 16 and defaults to 4.

## State ownership

Two dispatcher-owned runtimes are mandatory:

```text
Production dispatcher
  domain=production
  ring_capacity=4
  production authority=true

Measurement dispatcher
  domain=measurement-audit
  ring_capacity=64
  production authority=false
```

Both dispatchers derive from the same native runtime handles. Adapter, device and queue are shared. Guard ring buffers, slot state, telemetry state, capacity freeze state and runtime identity are not shared.

## Capacity policy

```text
production capacity range=3..16
production canonical capacity=4
measurement canonical capacity=64
```

The domain and capacity are immutable after runtime construction. Raising the global production maximum to 64, shrinking the pair matrix, reusing one dispatcher at capacities 64 and 4, or changing the production CLI capacity are forbidden repairs.

## Slot map

For probe pair index `p` in `0..31`:

```text
Single slot=p
GQA2 slot=32+p
```

Production Reference/Atlas measurement uses Atlas slots `0..31`; Reference consumes no guard-decision slot. Physical AB/BA or RA/AR order does not change logical slot identity.

## Query-atlas preservation

```text
pairs_per_round=32
timestamps_per_pair=4
queries_per_round=128
queue_submits_per_round=1
query_resolves_per_round=1
per_pair_submit_count=0
per_sample_timestamp_readback_count=0
```

The pair matrix may not be fragmented merely to fit the production ring.

## Evidence preservation

The measurement runtime writes compact decision tokens into its GPU telemetry surface before logical slots are released for subsequent round encoding. Telemetry drains occur outside timestamp spans. Output tensor values remain unread.

Required:

```text
wait_inside_timed_span_count=0
wait_between_pair_members_count=0
output_value_readback_count=0
measurement_slot_reuse_before_token_copy_count=0
```

## Negative controls

R2 inherits 820 controls and adds 60 domain, capacity, slot and isolation controls.

```text
negative_control_count=880
negative_control_executed_count=880
negative_control_skipped_count=0
negative_control_fail_count=0
```

## PASS boundary

PASS requires exact parent binding, production/measurement domain separation, production capacity 4, measurement capacity 64, same device and queue, distinct mutable guard runtimes, zero capacity mutation or cross-domain rebinding, exact 64-slot probe map, preserved one-submit query-atlas rounds, complete raw-sample truth, corrected probe admission, all production buckets, 880 controls, static truth, digest truth and zero model-quality claims.

PASS does not prove universal cross-adapter crossover, zero benchmark drain waits, native indirect o_proj, transactional KV rollback, canonical full-model decode, prefill/chunked production or model-quality improvement.

## Canonical run

Use the R2 gate with:

```text
--production-guard-ring-domain production
--measurement-guard-ring-domain measurement-audit
--decision-token-ring-capacity 4
--measurement-decision-token-ring-capacity 64
--measurement-guard-snapshot-ring-capacity 4
--expected-negative-controls 880
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_MEASUREMENT_GUARD_RING_DOMAIN_SEPARATION_64_SLOT_PAIR_MATRIX_DECISION_RUNTIME_PRODUCTION_DEFAULT_RING_PRESERVATION_CAPACITY_MUTATION_ISOLATION_SAME_DEVICE_DISPATCHER_SEPARATION_QUERY_ATLAS_COMBINED_RAW_TAIL_TRUTH_INCREMENTAL_ONLY_NO_OUTPUT_VALUE_READBACK_NO_MODEL_QUALITY_OVERCLAIM
```
