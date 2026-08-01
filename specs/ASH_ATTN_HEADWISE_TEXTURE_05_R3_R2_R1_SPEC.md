# ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2-R1

## Allocation Serial Origin Closure /
## Post-Bootstrap Relative Counter Authority /
## Bootstrap Allocation Count Separation /
## Canonical Serial Vector Correction /
## Generation Ledger Expected·Observed Parity /
## No Occupancy Failure Misclassification Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R2-R1`  
> Build revision: `HEADWISE-TEXTURE-05-R3-R2-R1-allocation-serial-origin-closure-v1`  
> Parent implementation: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3`

## 1. Root cause

The physical allocator reports a post-bootstrap append-relative serial:

```text
observed relative serial  [0,44,88,154,242,330]
```

The previous R3-R2 gate compared it with a lifetime-absolute vector that included the bootstrap twenty-two allocations:

```text
incorrect comparison vector [22,66,110,176,264,352]
```

All generation occupancy, refcount, free-set, retirement, zero-growth, transient-owner and session-retirement invariants passed. The only failure was the serial origin mismatch.

## 2. Authority split

```text
bootstrap allocation count authority       22
post-bootstrap relative serial authority    [0,44,88,154,242,330]
derived lifetime serial                     [22,66,110,176,264,352]
append allocation delta authority           [44,44,66,88,88]
```

The physical allocator remains authoritative for the relative serial. The bootstrap receipt remains authoritative for the separate bootstrap count. Lifetime serial is derived only as:

```text
lifetime serial = bootstrap allocation count + relative serial
```

## 3. Generation ledger schema

Each generation entry records:

```text
allocator_allocation_serial_origin = post_bootstrap_relative
bootstrap_allocation_count
allocator_allocation_serial
derived_lifetime_allocation_serial
occupancy_pass
allocation_serial_pass
pass = occupancy_pass && allocation_serial_pass && lifetime_derivation_pass
```

Occupancy and serial validation are independent predicates.

## 4. Canonical vectors

```text
generation                  T0   T1   T2   T3   T4   T5
relative serial              0   44   88  154  242  330
bootstrap count             22   22   22   22   22   22
lifetime serial             22   66  110  176  264  352
append delta                     44   44   66   88   88
```

## 5. Failure classification

A serial-only mismatch must be classified as one of:

```text
allocation_serial_origin_mismatch
allocation_serial_relative_vector_mismatch
allocation_serial_lifetime_derivation_mismatch
allocation_serial_delta_mismatch
```

It must not be classified as:

```text
expected_generation_occupancy
persistent residency leak
current_previous_refcount_leak
retired_page_free_set_divergence
```

## 6. Completion gate

```text
bootstrap allocation count                     22
relative serial vector                         exact
lifetime serial vector                         exact
append delta vector                            exact
six occupancy predicates                       PASS
six allocation serial predicates               PASS
generation page ledger                         PASS
parent R3-R2 invariants                         PASS
R3-R3 peak closure                              PASS
residency plateau within budget                 PASS
production authority mutations                    0
candidate output commits                           0
```

After PASS, the Texture-05 eligibility HOLD may contain only the remaining latency predicates.

## 7. Execution

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r3_r2_gate -- "@specs/cli/ash_attn_headwise_texture_05_r3_r2.args"
```

Then rerun the physical gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```
