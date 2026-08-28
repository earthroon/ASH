# ASH-BASETRAIN-RAM36-SUCCESSOR-WEIGHT-RESERVATION-PHYSICAL-ALLOCATION-OWNERSHIP-TRANSITION-CLOSURE-R1

## Status

Implementation-bound repair for the current exact N8 RAM36 first failure.

The preceding attribution run established:

```text
phase=CandidateOutputs
observed_private_bytes=34265280512
reserved_not_yet_materialized_bytes=4666580992
projected_used_bytes=38931861504
hard_limit_bytes=38654705664
exact_excess_bytes=277155840
private_usage_actually_over_limit=false
projection_only_over_limit=true
reservation_double_accounting_suspected=true
```

The exact successor reservation and builder capacity were both:

```text
4,666,580,992 bytes
```

while the reservation remained `Admitted` and continued contributing the same bytes to RAM36 projection after `ResidentWeightPackBuilder::new()` had already obtained that physical capacity.

This revision repairs only that ownership transition.

## Core authority distinction

```text
Reservation Bytes
!=
Physical Allocated Capacity Bytes
!=
Logical Materialized Bytes
```

`Reservation Bytes` represent future allocation commitment that has not yet entered process-private ownership.

`Physical Allocated Capacity Bytes` represent capacity already owned by the successor builder and therefore already represented by process-private observation.

`Logical Materialized Bytes` represent actual successor weight payload bytes written into that capacity.

Physical allocation does not imply logical materialization.

## State machine

The existing `HostRamReservation` remains the single reservation SSOT.

```text
Admitted
  -> PhysicalAllocated
  -> Materializing
  -> Materialized
  -> Promoted
  -> Released
```

Only `Admitted` contributes to RAM36 reservation projection.

```text
Admitted            contributes_to_projection = true
PhysicalAllocated   contributes_to_projection = false
Materializing       contributes_to_projection = false
Materialized        contributes_to_projection = false
Promoted            contributes_to_projection = false
Released            contributes_to_projection = false
```

## Exact physical allocation transition

The exact production order is:

```text
Reserve successor ResidentWeightPack bytes
    -> ResidentWeightPackBuilder::new(...)
    -> observe builder.allocated_capacity_bytes()
    -> validate allocated capacity == reservation requested bytes
    -> transition exact reservation ID to PhysicalAllocated
    -> subtract only that reservation requested byte count from projection total
```

The builder must already exist successfully before the transition occurs.

Required exactness:

```text
reservation.owner == ResidentWeightPack
reservation.state == Admitted
reservation.requested_bytes > 0
reservation.requested_bytes == builder.allocated_capacity_bytes()
target generation identity exact
target optimizer-step identity exact
physical_allocated_bytes before == 0
```

Mismatch fails closed.

## Projection conservation

Before physical allocation transition:

```text
reserved_projection_total_before
```

includes the successor reservation.

After exact physical allocation transition:

```text
reserved_projection_total_after
=
reserved_projection_total_before
-
this_reservation.requested_bytes
```

The reservation object is not deleted. Its state changes to `PhysicalAllocated` and its identity remains active for materialization, promotion, and release evidence.

No blanket projection reset is permitted.

## Physical allocation witness

The runtime emits:

```text
[ASH-RAM36-SUCCESSOR-WEIGHT-PHYSICAL-ALLOCATION-TRANSITION-R1]
```

with at least:

```text
reservation_id
owner
source_generation
target_generation
source_optimizer_step
target_optimizer_step
requested_bytes
physical_allocated_bytes_before
physical_allocated_bytes_after
logical_materialized_bytes
state_before
state_after
projection_contribution_before
projection_contribution_after
reserved_total_before
reserved_total_after
physical_capacity_exact
reservation_identity_preserved
```

and then:

```text
PASS_ASH_BASETRAIN_RAM36_SUCCESSOR_WEIGHT_RESERVATION_PHYSICAL_ALLOCATION_OWNERSHIP_TRANSITION_R1
```

This token claims the exact physical-allocation ownership transition only. It does not claim N8 completion.

## Logical materialization

After physical allocation, each successor builder append advances logical materialization monotonically.

```text
0 <= logical_materialized_bytes <= physical_allocated_bytes == requested_bytes
```

A nonzero partial payload is represented as `Materializing`.

The reservation becomes `Materialized` only after the successor builder finalizes exact coverage and digest identity.

Forbidden repair:

```text
physical allocation -> materialized_bytes = requested_bytes
```

Physical capacity ownership must not fabricate payload completion.

## Promotion

Promotion requires:

```text
state == Materialized
physical_allocated_bytes == requested_bytes
materialized_bytes == requested_bytes
exact target generation
exact target optimizer step
```

The same reservation ID then transitions to `Promoted`.

Runtime witness:

```text
[ASH-RAM36-SUCCESSOR-WEIGHT-PROMOTION-R1]
```

Only after exact promotion is the old current resident reservation released.

Current resident weight remains valid until promotion.

## Failure semantics

Required fail-closed tokens include:

```text
Ram36SuccessorPhysicalAllocationOwnerDrift
Ram36SuccessorPhysicalAllocationGenerationDrift
Ram36SuccessorPhysicalAllocationOptimizerStepDrift
Ram36SuccessorPhysicalAllocationStateDrift
Ram36SuccessorPhysicalAllocationRequestedBytesDrift
Ram36SuccessorPhysicalAllocationCapacityMismatch
Ram36SuccessorPhysicalAllocationDuplicateTransition
Ram36ReservationProjectionTotalDrift
Ram36SuccessorMaterializationProgressStateDrift
Ram36SuccessorMaterializationProgressRegression
Ram36SuccessorLogicalMaterializationExceedsPhysicalAllocation
Ram36SuccessorMaterializationCoverageDrift
Ram36SuccessorPromotionStateDrift
Ram36SuccessorPromotionPhysicalAllocationDrift
Ram36SuccessorPromotionMaterializationDrift
```

## Preserved RAM36 semantics

The exact hard limit remains:

```text
38,654,705,664 bytes
36 GiB exact
```

OS process-private usage remains authoritative and is never discounted by successor capacity.

The previous RAM36 underflow attribution witness remains active. If a later physical execution still underflows, that new witness determines whether the new first failure is actual private-memory exhaustion or a different projection owner.

## Forbidden repairs

```text
No Hard-Limit Increase /
No Private-Usage Discount /
No Reservation Suppression /
No Reservation Deletion At Allocation /
No Blanket Projection Reset /
No Fake Full Materialization /
No Saturating Subtraction /
No Underflow Masking /
No Warning-Only Continuation /
No Early Current-Resident Retirement /
No Failed-Candidate Promotion /
No Physical N2 Mutation /
No RAM36 Parent Replacement /
No BP-DK Reopen /
No Muon Registry Rewrite /
No Muon Profile Rewrite /
No Canonical Bridge Rewrite /
```

## Baked implementation surfaces

```text
crates/base_train/src/ram36_process_budget.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
tools/validate_ash_basetrain_ram36_reservation_projection_remaining_underflow_attribution_closure_r1_static.py
tools/validate_ash_basetrain_ram36_successor_weight_reservation_physical_allocation_ownership_transition_closure_r1_static.py
```

`ram_weight_pack_persistent_residency.rs` remains the existing capacity/materialized-byte observation authority and is not semantically rewritten by this revision.

## Static validation

Required token:

```text
PASS_ASH_BASETRAIN_RAM36_SUCCESSOR_WEIGHT_RESERVATION_PHYSICAL_ALLOCATION_OWNERSHIP_TRANSITION_CLOSURE_R1_STATIC
```

The previous attribution static token must also remain PASS:

```text
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1_STATIC
```

## Focused fixtures

```text
Admitted contributes to projection; all later states do not.
Requested 100 / allocated 100 -> exact transition accepted.
Requested 100 / allocated 99 -> fail closed.
Requested 100 / allocated 101 -> fail closed.
Physical allocated 100 / logical materialized 0 -> valid PhysicalAllocated state.
Physical allocated 100 / logical materialized 40 -> valid Materializing state with zero reservation projection.
```

## Expected next physical result

At the prior failing phase, if no other allocation changes, the successor reservation should no longer be added to process-private usage after exact physical allocation.

The next exact N8 must emit the physical-allocation transition PASS token before optimizer transient phases.

If `Ram36RemainingUnderflow` reappears, the retained attribution witness becomes the new first-failure authority. Closed N2/RAM36-parent/BP-DK/Muon axes are not reopened without contradictory evidence.

## Non-claims

This revision does not claim:

```text
N8 completion /
GEN13 reached /
Muon durable checkpoint completion /
Resume authority promotion /
Global RAM36 optimality /
```

It claims only exact successor ResidentWeightPack reservation-to-physical-allocation ownership transition closure.