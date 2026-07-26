# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F Pair-Order Query-Slot Deconfounding Addendum

## 0. Scope

This addendum corrects the pair-order schedule used by the R2E-R7 kernel-only continuity surface and the R2F guarded surface.

The previous v1 schedule used:

```text
order_bit = pair_index_in_visit XOR global_round XOR bucket_position
```

Under the exact mirrored schedules:

```text
A = 128,2048,256,1536,384,1024,512,768
B = reverse(A)
```

`global_round` parity and the reversed `bucket_position` parity cancel for the same KV bucket. Therefore each `pair_index_in_visit` parity was permanently associated with one AB/BA order. Query index, timestamp query offset, periodic spike position, and pair order were not independent.

This invalidates the v1 claim that no query-slot parity is permanently associated with one order.

## 1. Corrected authority

The canonical v2 order policy is:

```text
policy=mirrored-pair-query-slot-deconfounded-ab-ba-v2

order_bit =
    pair_index_in_visit
    XOR (global_round >> 1)
    XOR bucket_position

order_bit even=AB
order_bit odd=BA
```

The same function is used by:

```text
R2E-R7 warmup
R2E-R7 measured kernel-only surface
R2F guarded warmup
R2F guarded measured surface
```

No surface may implement a local order formula.

## 2. Required invariants

For every KV bucket and every `pair_index_in_visit` query slot:

```text
32 global rounds
AB ownership=16
BA ownership=16
```

For every adjacent mirrored round pair `(2n, 2n+1)` and the same KV/query slot:

```text
order(round 2n) != order(round 2n+1)
```

Each individual 32-pair bucket visit must still contain:

```text
AB=16
BA=16
```

## 3. Runtime gate

Rust must calculate and publish:

```text
pair_order_query_slot_deconfounded_pass
```

The field is true only when all buckets, all 32 query slots, and all 32 global rounds satisfy the invariants above.

The field must participate in:

```text
mirrored_schedule_pass
candidate_eligibility_pass
R2F production_route_shadow_eligibility_pass
final pass
```

A failure produces:

```text
pair_order_query_slot_deconfounding
```

and must HOLD before promotion.

## 4. CLI contract

Replace:

```text
--gqa4-pair-order-policy round-bucket-rotated-ab-ba-v1
```

with:

```text
--gqa4-pair-order-policy mirrored-pair-query-slot-deconfounded-ab-ba-v2
```

The old v1 enum is no longer accepted by the strict CLI registry.

## 5. Non-goals

This addendum does not:

```text
widen order-bias threshold
widen epoch-bias threshold
filter samples
remove spikes
selectively rerun rounds
change candidate or reference WGSL
change timestamp query count
change mirrored bucket order
```

## 6. Seal

The purpose of the v2 schedule is not to make order bias numerically smaller by relabeling samples. It ensures that AB/BA ownership is independent of the timestamp query-slot parity that produces those samples.

Only after this deconfounding gate passes may order-bias statistics be interpreted as path-order evidence.
