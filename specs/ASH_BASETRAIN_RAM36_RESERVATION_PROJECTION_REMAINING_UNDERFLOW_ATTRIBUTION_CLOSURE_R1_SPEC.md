# ASH-BASETRAIN-RAM36-RESERVATION-PROJECTION-REMAINING-UNDERFLOW-ATTRIBUTION-CLOSURE-R1

## Status

Implementation-bound attribution closure for the current exact N8 first failure:

```text
Ram36RemainingUnderflow
```

The failure is observed only after the following boundaries pass:

```text
Cross-Release Physical N2 admission                       PASS
Immutable N2 / RAM36 exact retry parent authority         PASS
TensorCube Local Muon canonical source-record bridge      PASS
BP-DK post-candidate TARGET optimizer-generation binding  PASS
GEN5 -> GEN6 durable transition                           OBSERVED
```

This revision does not repair or suppress the RAM36 failure. It records the exact failure phase, exact process-private usage, exact outstanding reservation ledger, exact projected usage, and exact excess before preserving the original fail-closed `Ram36RemainingUnderflow` result.

## Core projection

```text
projected_used_bytes =
    observed_private_bytes
  + reserved_not_yet_materialized_bytes
```

```text
remaining_bytes =
    hard_limit_bytes
  - projected_used_bytes
```

The exact RAM36 hard limit remains:

```text
38,654,705,664 bytes
36 GiB exact
```

No hard-limit increase is part of this revision.

## Attribution verdicts

The runtime distinguishes:

```text
ActualPrivateUsageOverLimit
```

when:

```text
observed_private_bytes > hard_limit_bytes
```

from:

```text
ProjectionOnlyOverLimit
```

when:

```text
observed_private_bytes <= hard_limit_bytes
AND
projected_used_bytes > hard_limit_bytes
```

The exact excess is:

```text
exact_excess_bytes = projected_used_bytes - hard_limit_bytes
```

The exact-limit boundary is valid and is not an underflow. One byte over the limit is an exact one-byte excess.

## Exact failure phase

The RAM36 authority carries explicit phase attribution:

```text
BeforeOptimizerStep /
SuccessorReservation /
TripleBatchInputs /
CandidateOutputs /
Serialization /
SuccessorMaterialize /
CandidateComplete /
GenerationPromotion /
OldResidentRelease /
```

Existing exact runtime labels are mapped to these phase identities. Unrelated RAM36 observations remain `RuntimeOtherExact` and preserve their literal label.

## Generation context

The optimizer scheduler binds:

```text
Source Generation /
Current Generation /
Target Generation /
Source Optimizer Step /
Current Optimizer Step /
Target Optimizer Step /
```

together with the current resident weight generation and exact current resident weight bytes.

No generation is inferred from arithmetic.

## Reservation ledger authority

The existing `HostProcessRamBudget` reservation ledger remains the sole reservation SSOT.

Every `update_remaining` first verifies:

```text
sum(requested_bytes for ADMITTED reservations)
==
reserved_not_yet_materialized_bytes
```

Mismatch fails independently as:

```text
Ram36ReservationLedgerTotalDrift
```

The attribution witness enumerates every active reservation with:

```text
Reservation ID /
Owner /
Requested Bytes /
Materialized Bytes /
State /
Contributes To Projection /
```

No replacement ledger is introduced.

## Resident owner witnesses

At failure the RAM36 authority reports exact materialized bytes owned by the existing reservation ledger for:

```text
Resident Weight Pack /
Adam-M Resident /
Adam-V Resident /
TensorCube Local Muon Momentum /
```

It also reports the existing parent evidence bounds for:

```text
Optimizer Segment Transient /
Optimizer Serialization Transient /
PCIe Staging /
```

Optimizer transient observed-capacity bytes are recorded from the concrete Rust vectors in the hot path.

PCIe staging observed bytes remain `None` when the current runtime does not expose a direct owned-byte observation. The configured bound remains authoritative. No zero-valued observation is synthesized.

## Successor resident-weight overlap witness

`ResidentWeightPackBuilder` exposes read-only observations:

```text
allocated_capacity_bytes
materialized_bytes
```

The builder currently uses:

```rust
Vec::with_capacity(expected_bytes)
```

Therefore a successor builder may own an allocated full weight-pack capacity while the successor reservation remains `ADMITTED` and contributes its full requested bytes to `reserved_not_yet_materialized_bytes`.

R1 does not repair this condition. It records:

```text
Resident Weight Successor Generation /
Resident Weight Successor Reserved Bytes /
Resident Weight Successor Allocated Capacity Bytes /
Resident Weight Successor Materialized Bytes /
Resident Weight Successor Materialized /
Successor Reservation Contributes To Projection /
Reservation Double-Accounting Suspected /
```

`reservation_double_accounting_suspected=true` requires both:

```text
an admitted ResidentWeightPack reservation contributes to projection
AND
successor builder allocated capacity bytes > 0
```

This is an attribution verdict only. It is not a repair and is not silently promoted to a proven ownership correction.

## Step-start deltas

`BeforeOptimizerStep` captures the step-start private and reservation values.

The underflow witness reports:

```text
Private Bytes Delta Since Step Start /
Reservation Bytes Delta Since Step Start /
Projected Bytes Delta Since Step Start /
```

so the exact phase that raised the projection can be compared with the step baseline.

## Runtime witness

Immediately before preserving `Ram36RemainingUnderflow`, the runtime emits:

```text
[ASH-RAM36-RESERVATION-PROJECTION-UNDERFLOW-R1]
```

including at least:

```text
Exact Failure Phase /
Observed Private Bytes /
Reserved Not-Yet-Materialized Bytes /
Projected Used Bytes /
Hard Limit Bytes /
Exact Excess Bytes /
Active Reservation Count /
Reservation Ledger Sum /
Generation Context /
Current Resident Weight /
Successor Reservation and Builder Capacity /
Adam-M Resident Bytes /
Adam-V Resident Bytes /
Muon Momentum Resident Bytes /
Optimizer Transient Bound and Observation /
Serialization Bound and Observation /
PCIe Staging Bound /
Actual-Private-vs-Projection-Only Verdict /
Reservation Double-Accounting Suspected /
```

Each active reservation is then emitted as:

```text
[ASH-RAM36-RESERVATION]
```

The attribution PASS token is emitted before the original failure:

```text
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1
```

The expected attribution-only terminal sequence may therefore be:

```text
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1
Error: Ram36RemainingUnderflow
```

This is a successful R1 attribution run.

## Focused fixtures

Required fixtures:

```text
Private 37 GiB / Reserved 0 / Limit 36 GiB
-> ActualPrivateUsageOverLimit / Exact Excess 1 GiB

Private 34 GiB / Reserved 3 GiB / Limit 36 GiB
-> ProjectionOnlyOverLimit / Exact Excess 1 GiB

Private 34 GiB / Reserved 2 GiB / Limit 36 GiB
-> Exact Boundary / No Underflow

Projected = Limit + 1 byte
-> Exact Excess 1 byte
```

## Preserved fail-closed semantics

The remaining calculation continues to use checked arithmetic. No saturating hard-limit subtraction is introduced.

Forbidden repairs:

```text
No Hard-Limit Increase /
No Reservation Suppression /
No Saturating Subtraction /
No Underflow Masking /
No Warning-Only Continuation /
No Parent RAM36 Replacement /
No New RAM36 Parent Receipt /
No Physical N2 Mutation /
No BP-DK Reopen /
No Muon Registry Rewrite /
No Muon Profile Rewrite /
No Canonical Bridge Rewrite /
```

## Baked implementation surfaces

```text
crates/base_train/src/ram36_process_budget.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_weight_pack_persistent_residency.rs
tools/validate_ash_basetrain_ram36_reservation_projection_remaining_underflow_attribution_closure_r1_static.py
```

## Static PASS token

```text
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1_STATIC
```

## Repair decision boundary

After one physical attribution run:

```text
ActualPrivateUsageOverLimit
    -> physical memory-plan contraction path

ProjectionOnlyOverLimit
    -> reservation ownership/capacity analysis

ProjectionOnlyOverLimit
AND reservation_double_accounting_suspected=true
    -> successor reservation/materialization ownership closure candidate
```

No repair branch is selected before the physical witness is observed.

## Non-claims

R1 does not claim:

```text
RAM36 failure repaired /
N8 complete /
Durable Muon checkpoint complete /
Resume authority promoted /
Long-horizon production ready /
```

It claims only exact attribution of the RAM36 remaining-projection underflow before repair.