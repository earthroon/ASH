# A01-SUBMISSION-LEASE-R1

## INCREMENTAL COMPLETION FRONTIER + LIVE-SET COMPACTION

```text
A01-SUBMISSION-LEASE-R1

INCREMENTAL COMPLETION FRONTIER
+ LIVE-SET COMPACTION

+ EXISTING SUBMISSION COMPLETION SEMANTICS PRESERVATION
+ EXISTING LEASE IDENTITY PRESERVATION
+ EXISTING RETIREMENT DISPOSITION PRESERVATION
+ MONOTONIC COMPLETION FRONTIER
+ SUBMISSION-ORDERED PENDING LEASE INDEX
+ DELTA-ONLY COMPLETION REEVALUATION
+ RELEASE-LOCAL RETIREMENT REEVALUATION
+ LIVE / TERMINAL LEASE DOMAIN SPLIT
+ COMPACT TERMINAL RECORD
+ TERMINAL SNAPSHOT RECONSTRUCTION
+ RELEASE-BEFORE-COMPLETION CLOSURE
+ COMPLETION-BEFORE-RELEASE CLOSURE
+ OBSERVE FULL-CENSUS PARITY
+ ACTIVE NO HOT-PATH FULL LEASE CENSUS
+ ACTIVE NO HOT-PATH LEASE-KEY Vec MATERIALIZATION
+ EXPLICIT AUDIT-ONLY FULL CENSUS
+ RESOURCE-REUSE AUTHORITY PRESERVATION
+ STALE / TERMINAL LEASE IDENTITY PRESERVATION
+ NO NEW GPU SUBMISSION
+ NO NEW GPU WAIT
+ NO NEW MAP
+ NO NUMERICAL CHANGE
```

## 0. Revision

```text
Patch ID:
A01-SUBMISSION-LEASE-R1

Short name:
A01-LEASE-FRONTIER-R1

Class:
CPU HOT-PATH BOOKKEEPING COMPACTION
SUBMISSION COMPLETION INDEXING
LEASE LIFECYCLE REPRESENTATION COMPACTION
```

Direct production source:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
```

Static validator:

```text
tools/validate_ash_a01_submission_lease_r1_incremental_completion_frontier_static.py
```

## 1. Purpose

The parent A01 runtime couples completion refresh with registry-wide lifetime census.
R1 separates:

```text
completion progress
```

from:

```text
global lease-state audit
```

The canonical retirement decision remains the existing A01 retirement-disposition authority.
R1 changes which lease IDs are reevaluated, not the lifecycle law itself.

## 2. Runtime Mode

Environment:

```text
ASH_A01_SUBMISSION_LEASE_R1_MODE
```

Accepted:

```text
OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default:

```text
OFF
```

### OFF

Parent completion refresh and parent full lifetime census remain authoritative.

### OBSERVE

Incremental frontier/index state is maintained, while the full census remains a parity authority.
No terminal live-record compaction is published in OBSERVE.

### ACTIVE

Incremental frontier/index state becomes authoritative for completion/release reevaluation.
Terminal `RetiredComplete` leases leave the hot live map and are retained as compact terminal records.
Normal completion/release hot paths do not invoke the full registry census.

## 3. Canonical Runtime Domains

R1 materializes three conceptual domains:

```text
LIVE LEASE MAP
PENDING COMPLETION INDEX
TERMINAL LEASE HISTORY
```

The pending-completion index is keyed by:

```text
QueueAuthorityId
    -> SubmissionEpoch.ordinal
        -> LogicalLeaseId[]
```

No synthetic cross-queue ordinal ordering is introduced.

## 4. Completion Frontier

Each queue domain retains the existing:

```text
completed_through
```

authority.

R1 advances it monotonically:

```text
new_completed_through = max(old_completed_through, observed_completed_through)
```

A stale observation never moves the frontier backwards.

When the frontier advances from A to B, only pending submission buckets now covered by B are removed from the pending index and reevaluated.

## 5. Event-Local Reevaluation

R1 reevaluates a lease only when a lifecycle input affecting that lease changes.

Primary events:

```text
completion frontier advance
lease release
map-state mutation
explicit audit
```

Release operations reevaluate only the lease IDs explicitly released.

## 6. Existing Retirement Law Preservation

The canonical decision remains equivalent to the parent order:

```text
completion coverage
pending queue write
map state
queue completion
logical state
```

No second independent retirement-rule implementation is introduced.

The following dispositions remain unchanged:

```text
Live
PendingQueueWrite
InFlight
HostMapped
ReleasedAwaitingCompletion
RetiredComplete
ConservativeHold
```

## 7. Release-Before-Completion Closure

Required sequence:

```text
submitted
-> released
-> submission incomplete
-> ReleasedAwaitingCompletion
-> frontier reaches submission
-> RetiredComplete
```

The pending index must retain the released lease until the completion frontier covers its submission.

## 8. Completion-Before-Release Closure

Required sequence:

```text
submitted
-> completion frontier reaches submission
-> lease remains logically Live
-> disposition Live
-> release event
-> RetiredComplete
```

No second completion event is required after release.

## 9. Terminal Live-Set Compaction

In ACTIVE, when a lease reaches exact `RetiredComplete`:

```text
full AshBufferLease
    -> removed from hot live map
    -> converted to TerminalLeaseRecordR1
```

Terminal history retains source-proven post-terminal fields needed to reconstruct the existing public lease snapshot.

Fields whose terminal values are structurally fixed are not stored redundantly:

```text
logical_state = Released
map_state = Unmapped
pending_queue_write_count = 0
completion_coverage = ExactTracked
allocation = Owned(...)
```

Terminal snapshot reconstruction preserves the public `AshBufferLease` shape.

## 10. Terminal Mutation Compatibility

If an existing mutation API addresses a terminal lease in ACTIVE, R1 rehydrates the compact terminal record into a live `AshBufferLease`, applies the existing mutation, and reevaluates it.

This avoids turning a previously addressable lease ID into a false unknown/stale identity solely because of compaction.

## 11. Physical Allocation Snapshot Preservation

The existing APIs:

```text
physical_allocation_write_lease_snapshots_r3g2
physical_allocation_lease_snapshots_r7a1
submission_lease_snapshot
```

must continue to expose terminal prior-incarnation leases where parent semantics require them.

Terminal records are reconstructed into the existing public snapshot representation for these explicit snapshot paths.

## 12. Resource Reuse Preservation

`assert_reuse_eligible()` remains equivalent to parent:

```text
RetiredComplete -> eligible
all other dispositions -> reject
```

No allocation becomes reusable earlier because of frontier advancement or terminal compaction.

## 13. Hot-Path Census Closure

ACTIVE normal hot paths must not directly perform the parent pattern equivalent to:

```rust
state.leases
    .keys()
    .copied()
    .collect::<Vec<_>>()
```

followed by registry-wide retirement recomputation.

The protected functions include:

```text
poll_nonblocking_and_refresh
refresh_async_completion_mailboxes
submission_completed_nonblocking
wait_for_submission_exact
release_submission_lease_site
release_submission_leases
```

## 14. Explicit Audit Boundary

Full census remains available through explicit audit/parity helpers.

R1 distinguishes:

```text
hot-path full census
explicit audit full census
```

with separate telemetry.

ACTIVE must not silently fall back to full census when incremental state is inconsistent.

## 15. OBSERVE Parity

OBSERVE compares incremental cached dispositions and incremental lifetime counters against a full parent-equivalent census.

Required exact parity:

```text
live_inflight_lease_count
released_inflight_lease_count
retired_complete_lease_count
per-live-lease retirement disposition
```

Any drift fails closed.

## 16. Telemetry

R1 adds measured counters for:

```text
r1_completion_refresh_count
r1_completion_frontier_advance_count
r1_completion_frontier_unchanged_count
r1_completion_delta_submission_count
r1_completion_delta_lease_count
r1_retirement_reevaluation_count
r1_release_local_reevaluation_count
r1_hotpath_full_census_count
r1_audit_full_census_count
r1_hotpath_full_registry_key_materialization_count
r1_live_lease_count
r1_peak_live_lease_count
r1_terminal_compaction_count
r1_retained_terminal_record_count
r1_full_live_record_retired_count
r1_stale_id_lookup_live_count
r1_stale_id_lookup_terminal_count
```

These are mutation-backed counters. A zero is not inferred from source structure alone.

## 17. GPU Boundary

R1 adds no new:

```text
queue.submit
map_async
get_mapped_range
queue.write_buffer
copy_buffer_to_buffer
PollType::Wait
PollType::Poll
```

The existing one queue submission site, exact-wait site, and nonblocking poll site are preserved.

## 18. Numerical / Storage Boundary

R1 changes no:

```text
shader
WGSL
optimizer math
tensor value
buffer byte layout
candidate math
durable file format
```

## 19. Static Acceptance

Required structural gates:

```text
runtime mode authority exists
terminal lease record exists
pending completion index exists
cached disposition authority exists
completion frontier helper exists
release-local reevaluation exists
terminal compaction exists
terminal rehydration exists
OBSERVE parity exists
explicit audit exists
legacy refresh_lifetime_counters_locked retired
ACTIVE finalize does not call full census
hot completion/release functions contain no direct full-key Vec census
GPU transfer/wait primitive counts unchanged
release-before-completion fixture exists
completion-before-release fixture exists
```

Pass token:

```text
PASS_A01_SUBMISSION_LEASE_R1_INCREMENTAL_COMPLETION_FRONTIER_STATIC
```

## 20. Compile Acceptance

Required on the authoritative Rust environment:

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

All must PASS before COMPILE promotion.

## 21. Runtime Qualification

First run OBSERVE with a workload exercising:

```text
lease creation
submission
completion refresh
release-before-completion
completion-before-release
map requested / mapped / unmapped
physical retirement / reuse queries
prior-incarnation allocation snapshots
```

Required:

```text
retirement parity exact
lifetime counter parity exact
snapshot semantics exact
no early reuse
```

## 22. ACTIVE Physical Qualification

Then run ACTIVE.

Required:

```text
frontier advance physically observed
completion delta lease processing observed
release-local reevaluation observed
terminal compaction observed
terminal snapshot reconstruction observed
hotpath full census count = measured 0
hotpath full registry key materialization count = measured 0
no early physical retirement
no early resource reuse
no lost pending lease
```

## 23. Performance Qualification

Compare same-source:

```text
A01-R1 OFF
vs
A01-R1 ACTIVE
```

Measure:

```text
CPU process time
optimizer-step wall time
generation wall time
completion bookkeeping wall time
lease mutex hold wall time
retirement reevaluation count
hot-path allocation count/bytes
peak live lease count
retained terminal history bytes
```

No speedup claim is promoted from SOURCE/STATIC alone.

## 24. Bake Delta

```text
MOD 1
ADD 1
DEL 0
```

Modified:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
```

Added:

```text
tools/validate_ash_a01_submission_lease_r1_incremental_completion_frontier_static.py
```

Cargo graph and WGSL are unchanged by this bake.

## 25. Static Bake Evidence

```text
PASS_A01_SUBMISSION_LEASE_R1_INCREMENTAL_COMPLETION_FRONTIER_STATIC checks=53
```

A directly related existing R4A-CF2-CF1 static validator also remains PASS:

```text
PASS_TENSORCUBE_TABLE_R4A_CF2_CF1_DIRECT_PRODUCER_OUTPUT_CF1_SHARED_ARENA_STATIC checks=90
```

Some historical validators in the code-only parent require `specs/` files that are intentionally absent from code-only archives and therefore are not promotable evidence from this bake environment.

Historical R7A/R7A1 validators that already fail on the parent retain the same failure set; those failures are not attributed to A01-R1.

## 26. Evidence State

```text
SOURCE       BAKED
STATIC       PASS (A01-R1 53/53)
COMPILE      UNVERIFIED (Rust toolchain unavailable in bake environment)
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

No higher evidence grade is inferred from static validation.

## 27. Artifact Packaging Law

Distributed code ZIPs contain code only.

Explicitly excluded from generated ZIP artifacts:

```text
specs/
artifacts/
generated manifest JSON
this specification
bake report
```

Source-code modules whose Rust/Python filenames contain the word `manifest` remain code and are not treated as generated manifest artifacts.

## 28. Artifact Seals

```text
Modified source SHA-256
3507b5c7de9a1c0e85e80ad3f5aee5a52bf05f7c038ec887b462d654bda9804e

Static validator SHA-256
a84558fca7bb3d43226cc2cd3ee125b230d25ab0faff7a714177e0686283f04a

Overlay code-only ZIP SHA-256
5456fc58f0240402c9f44b732f0fda8b34118e6560cff2e40943cad2ec72da27
files=2

Full code-only ZIP SHA-256
fb2d8507041ffddf0059c077d57fbd99a4d64518199c0f7446b01d59b324bcbb
files=8530
```

## 29. Successor

After A01-R1 physical closure:

```text
TENSORCUBE-TABLE-R4D-R2-CF2
MONOTONIC SEGMENT CURSOR
+ CHUNK LOOKUP COLLAPSE
```

A01-R1 does not absorb R4D-R2 segment traversal or durability I/O work.

## 30. Final Law

> A01-R1 does not change when a submission is complete, when a lease is logically released, or when a resource is reusable. It changes the CPU path used to reach those answers.

> Completion becomes a queue-local monotonic frontier. Only leases whose lifecycle inputs changed are reevaluated.

> Retired terminal leases leave the hot live set while source-proven historical identity remains reconstructable for existing snapshot and reuse authorities.

> Full registry census remains an explicit OFF/OBSERVE/audit mechanism, not the normal ACTIVE completion price.

> SOURCE and STATIC evidence do not claim runtime or performance closure.
