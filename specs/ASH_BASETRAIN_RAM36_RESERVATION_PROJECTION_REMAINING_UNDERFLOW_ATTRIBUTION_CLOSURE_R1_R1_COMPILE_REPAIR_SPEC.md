# ASH-BASETRAIN-RAM36-RESERVATION-PROJECTION-REMAINING-UNDERFLOW-ATTRIBUTION-CLOSURE-R1-R1

## Status

Compile-only ownership repair to R1. No attribution semantic change.

## Trigger

Rust compile failure E0382 in `production_multistep_loop_accumulation8_scheduler.rs`:

```text
use of moved value: successor_reservation
```

The promotion path moved the `HostRamReservation` into the resident reservation authority:

```rust
resident_weight_reservation.replace(successor_reservation)
```

and then attempted to read `successor_reservation.requested_bytes` and `successor_reservation.materialized_bytes` for the RAM36 attribution witness.

`HostRamReservation` is not `Copy`, so that use-after-move is invalid.

## Repair

Before the reservation ownership transfer, copy only the scalar witness values:

```rust
let successor_reserved_bytes = successor_reservation.requested_bytes;
let successor_materialized_bytes = successor_reservation.materialized_bytes;
```

Then move the original reservation exactly once:

```rust
resident_weight_reservation.replace(successor_reservation)
```

After the move, the RAM36 attribution witness consumes only the copied `u64` scalar values.

## Why no clone

The compiler suggested cloning the reservation. This revision intentionally does not use that repair.

The reservation object itself is an ownership-bearing ledger entry. Cloning it solely to satisfy a witness read would create a second in-memory copy of an authority object with no semantic need.

The exact witness fields are `u64` and are `Copy`, so scalar capture preserves single reservation ownership while retaining the exact requested/materialized byte evidence.

## Preserved invariants

```text
Single Reservation Ownership Transfer /
No HostRamReservation Clone /
No Duplicate Reservation Authority /
Exact Requested Bytes Witness /
Exact Materialized Bytes Witness /
Original R1 Failure Phase Attribution /
Original R1 Projection Calculation /
Original 36 GiB Hard Limit /
Original Ram36RemainingUnderflow Fail-Closed Guard /
```

## Static regression

The existing R1 static validator now additionally requires:

```text
Successor requested/materialized scalar capture occurs before move /
No successor_reservation field access after move /
No successor_reservation.clone() repair /
```

The R1 static PASS token remains:

```text
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1_STATIC
```

## Baked implementation surfaces

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
tools/validate_ash_basetrain_ram36_reservation_projection_remaining_underflow_attribution_closure_r1_static.py
```

## Non-claims

R1-R1 does not change:

```text
RAM36 accounting semantics /
Reservation lifecycle semantics /
Successor materialization semantics /
Underflow attribution verdicts /
Hard limit /
BP-DK behavior /
Muon behavior /
Physical N2 authority /
```

It only repairs Rust move ownership so the R1 attribution code can compile and run.