# EVE-MCU-R3H-CF3

## SUBMISSION LEASE PHYSICAL-ALLOCATION COALESCING

**Revision:** EVE-MCU-R3H-CF3  
**Parent:** EVE-MCU-R3H-CF2  
**Class:** submission-lifetime authority compression / physical-allocation lease coalescing

```text
+ COPY COMMAND / LEASE AUTHORITY SEPARATION
+ ONE LEASE PER PHYSICAL ALLOCATION / ACCESS CLASS
+ CF1 COPY-SPAN CARDINALITY PRESERVATION
+ LEASE RANGE UNION / COVERAGE AUTHORITY
+ NO COPY COMMAND MERGE
+ NO PACKED GEOMETRY CHANGE
+ NO EXTRA SUBMISSION
+ NO EXTRA WAIT
+ CF2 BORROWED READBACK PRESERVATION
```

## 1. Parent physical blocker

R3H-CF1 physically admitted packed decomposition, including high-cardinality routes such as:

```text
logical_count=2048
physical_span_count=128
copy_command_count=128
covered_elements=2048
gap_count=0
overlap_count=0
admitted=true
```

R3H-CF2 removed `mapped.to_vec()` full-window duplication statically, but the next physical campaign failed before mapped consumption with:

```text
memory allocation of 33669272 bytes failed
```

The parent readback submission path still allocated one `SubmissionLeaseSpec` per physical copy span through:

```text
Vec::with_capacity(copies.len() + 1)
for copy in copies:
    one copy_buffer_to_buffer
    one owned_existing_range SubmissionLeaseSpec
```

CF3 separates physical copy cardinality from allocation-lifetime cardinality.

## 2. Core law

```text
COPY GRANULARITY != LEASE GRANULARITY
```

Physical copy commands prove exact byte movement. Submission leases prove physical-allocation lifetime for the submission.

Many exact discontinuous copy spans may therefore share one allocation-bound lifetime lease without changing any source offset, destination offset, byte count, or packed-contiguity proof.

## 3. Production implementation

Primary source:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

CF3 adds:

```text
ProjectionLeaseDemandR3HCF3
ProjectionLeaseAggregateR3HCF3
ProjectionLeaseCoalescingStatsR3HCF3
coalesce_projection_lease_demands_r3h_cf3
projection_submission_specs_r3h_cf3
```

The production path folds lease demand directly into a deterministic `BTreeMap` keyed by:

```text
PhysicalAllocationId
SubmissionAccess class
BufferLeaseClass
```

No O(copy-count) lease-demand vector is created.

## 4. One allocation/access/class lease authority

For each source copy demand:

```text
allocation
semantic role
lease class
submission access
offset
size
```

are folded into an aggregate.

For one exact key:

```text
minimum_offset = min(all copy offsets)
maximum_end    = max(copy offset + copy size)
requested_range_count += 1
requested_byte_sum += copy size
```

The final lifetime lease conservatively covers:

```text
[minimum_offset, maximum_end)
```

This is a lifetime coverage range only. It is not a physical copy merge.

## 5. Semantic-role handling

Semantic role does not block safe physical coalescing.

If one physical allocation/access/class key receives multiple semantic-role labels, the coalesced lease role becomes:

```text
BufferSemanticRole::Unknown
```

rather than inventing a false single-role claim.

Physical allocation identity remains authority.

## 6. Queue/device authority

For every unique coalesced source allocation:

```text
queue_binding_for_physical_allocation(allocation)
```

must exactly equal the canonical queue binding selected for the readback submission.

Mismatch fails closed with:

```text
E_R3H_CF3_CROSS_AUTHORITY_COALESCING_ATTEMPT
```

No cross-queue or cross-device lease merge is admitted.

## 7. Access authority

Different `SubmissionAccess` classes are separate coalescing keys.

Therefore `READ + WRITE` is not weakened to READ.

CF3 preserves separate exact access authorities instead of silently escalating or weakening them.

The full-durable production source path currently emits:

```text
StorageReadOnly + SubmissionAccess::Read
```

for source copy allocations.

The readback staging lease remains an independent `MapReadback + Write` authority.

## 8. No O(copy) final lease vector

Parent:

```text
Vec::with_capacity(copies.len() + 1)
```

CF3:

```text
Vec::with_capacity(unique_allocation_access_class_keys + 1)
```

The `+1` is the mapped readback staging lease.

The final `SubmissionLeaseSpec` vector therefore scales with coalesced allocation authorities, not physical copy spans.

## 9. Per-copy String retirement

Parent `FullTrainableProjectionCopyR1` carried `site_id: String`, and every CF1 physical span materialized a formatted heap string solely to identify its one-per-copy lease spec.

CF3 removes this field and all six per-copy `format!(...)` initializers.

Physical copy cardinality is unchanged, but copy metadata no longer carries lease-only per-span heap strings.

## 10. Copy geometry preservation

CF3 preserves every existing `encoder.copy_buffer_to_buffer(...)` operation.

Required invariant:

```text
CF3 copy_command_count == CF2 copy_command_count
```

for an identical fixture.

CF3 does not merge, remove, reorder, or widen physical copy commands.

## 11. CF1 preservation

The following remain active:

```text
decompose_muon_logical_route_to_packed_spans_r3h_cf1
E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose]
```

Required physical evidence remains:

```text
physical_span_count > 1
copy_command_count == physical_span_count
gap_count=0
overlap_count=0
admitted=true
```

## 12. CF2 preservation

The scoped mapped consumer remains authoritative.

Production continues to require:

```text
mapped_full_window_clone_count=0
mapped_full_window_clone_bytes=0
consume before unmap
unmap before lease release
```

No `mapped.to_vec()` production path is reintroduced.

## 13. Submission/completion preservation

CF3 preserves:

```text
submit_with_leases
submission_completed_nonblocking
mark_map_requested
mark_mapped_read
mark_unmapped
release_submission_leases
```

No new submission is introduced. No `wait_for_submission_exact` callsite is introduced.

## 14. Runtime witness

CF3 emits:

```text
[ASH-EVE-MCU-R3H-CF3][lease-coalesce]
```

with:

```text
site
copy_command_count
lease_demand_count
unique_allocation_count
unique_access_key_count
coalesced_source_lease_count
submission_lease_spec_count
requested_byte_sum
conservative_covered_byte_sum
coverage_exact=true
access_coverage_exact=true
device_queue_exact=true
admitted=true
```

`submission_lease_spec_count` includes the one readback staging lease.

## 15. Required physical shape

For a high-cardinality CF1 window:

```text
copy_command_count >> coalesced_source_lease_count
```

must be observed.

Example shape only:

```text
copy_command_count=262144
coalesced_source_lease_count=24
submission_lease_spec_count=25
```

Exact counts are runtime-dependent and are not claimed by the bake.

## 16. Coverage authority

CF3 counts every source copy demand folded into an aggregate.

Before submission:

```text
covered_demand_count == lease_demand_count
```

is mandatory.

Failure:

```text
E_R3H_CF3_COPY_WITHOUT_COALESCED_LEASE
```

Range arithmetic is checked for overflow and empty ranges.

## 17. Determinism

`BTreeMap` ordering makes final source lease ordering deterministic by:

```text
PhysicalAllocationId
access-key ordinal
lease-class ordinal
```

No randomized hash iteration controls submission receipt ordering.

## 18. No geometry or numerical changes

CF3 does not modify:

```text
packed_index_for_logical
route_span
16x16 packed layout
Muon / HiMuon math
AdamW math
weight update values
candidate M/V values
BP-DK numerical witness
```

## 19. No memory-policy cheats

CF3 does not change:

```text
RAM36 hard limit
R6 stream chunk/window size
R3H resident-weight replacement policy
```

No smaller transfer window is used to hide the parent allocation failure.

## 20. Parent authority preservation

Required unchanged semantics:

```text
R3H host-weight retirement authority
R3G EXACT_TRACKED mutation completion
BP-DK-R3 RuntimeIdentity
R3C consuming generation commit
```

Expected BP-DK policy remains:

```text
identity_policy=RUNTIME_IDENTITY
full_payload_sha_count=0
runtime_identity_count=3
```

## 21. Unit fixtures added

Test prefix:

```text
r3h_cf3_
```

Fixtures:

```text
r3h_cf3_many_reads_one_allocation
r3h_cf3_two_allocations_two_leases
r3h_cf3_read_write_access_not_weakened
r3h_cf3_different_allocations_are_not_coalesced
r3h_cf3_discontinuous_copy_ranges_one_lifetime_lease
r3h_cf3_overlapping_ranges_preserve_copy_demand_count
```

## 22. Static bake seals

```text
ADD 0
MOD 1
DEL 0

modified source:
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs

parent scheduler SHA-256:
de98b59839e6acd2dc08a93ec25abb9d5bbeb8864f0cfb84507fad6c31f68699

CF3 scheduler SHA-256:
cd14a404060953818f490110490817af2e1f447f2f9f40ac1c51aa1da5cf9821

Vec::with_capacity(copies.len()+1) lease pattern = 0
mapped.to_vec() production file count = 0
new wait_for_submission_exact callsites = 0
CF1 witness preserved = yes
CF2 witness preserved = yes
CF3 witness count = 1
CF3 unit tests = 6
per-copy lease-only site_id String field = removed
```

`ResidentWeightPack::load_once` remains at the pre-existing canonical source-load site. CF3 adds no new callsite.

## 23. Baked artifacts

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF3_SUBMISSION_LEASE_PHYSICAL_ALLOCATION_COALESCING_CODE_ONLY.zip
SHA-256 96f4eef6e4ae5119087c034bbc42dbc81fa165296f4cb9ad00f5b845f57bdcd1
Files 8426
CRC PASS
```

Overlay:

```text
ASH_EVE_MCU_R3H_CF3_SUBMISSION_LEASE_PHYSICAL_ALLOCATION_COALESCING_OVERLAY_CODE_ONLY.zip
SHA-256 e33ce5e1d2133fb45f71ef80dd1ea251113d3b099747bfcdbb342969a8b37a85
Files 1
CRC PASS
```

Both code archives contain:

```text
Markdown files 0
specs/ files   0
artifacts/     0
```

## 24. Evidence state at bake time

```text
SOURCE / STATIC    PASS
ARCHIVE            PASS
COMPILE            UNVERIFIED
RUNTIME-TEST       UNVERIFIED
PHYSICAL           UNVERIFIED
PERFORMANCE        UNMEASURED
```

The bake environment contains no Rust toolchain, so compile/runtime/physical status must be promoted only from the canonical Windows authority.

## 25. Compile qualification

```text
cargo test -p base_train --lib --release --locked r3h_cf3_ -- --nocapture
cargo test -p base_train --lib --release --locked r3h_cf2_
cargo test -p base_train --lib --release --locked r3h_cf1_
cargo test -p base_train --lib --release --locked r3h_
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked bp_dk_r3_
cargo build -p base_train --bin base_train --release --locked -j 1
```

Static/compile promotion token:

```text
PASS_EVE_MCU_R3H_CF3_SUBMISSION_LEASE_PHYSICAL_ALLOCATION_COALESCING
```

## 26. Physical qualification

Re-seal the exact rebuilt `base_train.exe` using native CF1 release compile authority and rerun:

```text
--eve-mcu-close-r2-phys-canary-r1
```

Required positive witness:

```text
[ASH-EVE-MCU-R3H-CF3][lease-coalesce]
copy_command_count > coalesced_source_lease_count
coverage_exact=true
access_coverage_exact=true
device_queue_exact=true
admitted=true
```

The same run must retain CF1 and reach CF2 mapped consumption or a later canonical authority.

Physical promotion token:

```text
PASS_EVE_MCU_R3H_CF3_PHYSICAL_SUBMISSION_LEASE_COALESCING
```

Hold token:

```text
HOLD_EVE_MCU_R3H_CF3_LEASE_COALESCING_PHYSICAL_CLOSURE_UNPROVEN
```

## 27. Non-claims

CF3 does not claim to solve:

```text
copy-command encoder memory
hundreds-of-thousands command-list pressure
HiMuon target backing lifetime
R7A retained VRAM cache
full canary completion
step-time performance
```

If command encoder metadata becomes the next blocker after lease compression, it is a separate revision.

## 28. Completion law

CF3 is complete only when:

```text
1. copy-command cardinality and lease cardinality are separate authorities.
2. CF1 physical copy commands remain exact and unchanged.
3. no physical copy merge is used to reduce lease metadata.
4. lease demand is folded directly by physical allocation/access/class.
5. no O(copy-count) SubmissionLeaseSpec vector is first materialized and deduplicated later.
6. final source lease count scales with unique allocation/access/class keys.
7. every source copy demand is covered by a final coalesced lease.
8. discontinuous physical copies may share a conservative allocation lifetime range.
9. different queue/device authorities are not merged.
10. different access classes are not weakened.
11. semantic-role disagreement is represented conservatively rather than blocking safe physical coalescing.
12. per-copy lease-only site_id heap strings are removed.
13. staging readback remains a separate mapped lease.
14. no additional submission is introduced.
15. no additional exact wait is introduced.
16. CF1 packed span decomposition remains active.
17. CF2 borrowed mapped readback remains active.
18. mapped full-window clone count remains zero.
19. RAM36 hard limit is unchanged.
20. transfer window size is unchanged.
21. R3H, R3G, BP-DK-R3, and R3C authority semantics remain unchanged.
22. physical canary demonstrates copy_command_count >> coalesced_source_lease_count and progresses beyond the parent pre-map allocation blocker.
```

## 29. Final authority law

> EVE-MCU-R3H-CF3 preserves every physically required packed copy operation while replacing per-copy lifetime metadata with physical-allocation-bound lifetime authority.

> Copy commands describe movement. Submission leases describe lifetime. They are not the same unit and are no longer represented 1:1.

> Discontinuous source ranges may share one conservative physical-allocation lease without becoming one physical copy. Access class, allocation identity, and queue/device authority remain fail-closed boundaries.

> CF3 therefore compresses lease metadata toward O(unique physical allocation/access/class) while preserving CF1 geometry, CF2 zero-duplicate mapped consumption, R3H lifetime semantics, R3G completion authority, BP-DK-R3 RuntimeIdentity, and R3C atomic commit.
