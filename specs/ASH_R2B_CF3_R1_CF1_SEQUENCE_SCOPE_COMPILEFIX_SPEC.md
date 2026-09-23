# R2B-CF3-R1-CF1
# TRACE EXECUTE-SEQUENCE SCOPE COMPILEFIX

## Purpose

Close E0425 caused by a forward reference to `parity_event_count` in the parent CF3 trace event.

## Exact repair

Within the `r2b_cf3_trace_enabled_now == true` branch, replace:

```rust
"execute_sequence": match r2b_cf3_execute_sequence {
    0 => parity_event_count,
    value => value,
},
```

with:

```rust
"execute_sequence": r2b_cf3_execute_sequence,
```

## Reason

The branch itself proves CF3 tracing is enabled. `r2b_cf3_execute_sequence` is populated by
`R2B_CF3_EXECUTE_SEQUENCE.fetch_add(1, Ordering::Relaxed) + 1`, so zero fallback is unreachable.
`parity_event_count` is intentionally created later after compact parity readback and must not be
referenced before that point.

## Preservation

No change to:

```text
GPU source->shadow copy
exact-u32 parity kernel
16-byte compact readback
FFN fused dispatch
parity_event_count increment semantics
promotion count semantics
CF3 backing topology
R1J downstream boundary
```

## Acceptance

```text
CF3-R1 static 76/76
CF3 static 60/60
CF2-R1 static 67/67
CF2 static 48/48
```

Compile/runtime/physical require operator re-run.
