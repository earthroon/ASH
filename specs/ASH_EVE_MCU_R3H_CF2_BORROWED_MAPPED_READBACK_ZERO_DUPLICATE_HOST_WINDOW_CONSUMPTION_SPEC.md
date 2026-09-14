# EVE-MCU-R3H-CF2

## BORROWED MAPPED READBACK + ZERO-DUPLICATE HOST WINDOW CONSUMPTION

**Revision:** EVE-MCU-R3H-CF2  
**Parent:** EVE-MCU-R3H-CF1  
**Class:** scoped mapped-readback lifetime authority / full-window host-clone retirement

```text
+ MAPPED RANGE DIRECT CONSUMPTION
+ RETIRE mapped.to_vec FULL-WINDOW CLONE
+ WEIGHT / ADAM M / ADAM V SLICE BORROW
+ CONSUME-BEFORE-UNMAP AUTHORITY
+ BOUNDED WINDOW LIFETIME
+ EXISTING SUBMISSION COMPLETION PRESERVATION
+ CF1 PHYSICAL-SPAN DECOMPOSITION PRESERVATION
+ NO WINDOW-SIZE CHEAT
+ NO RAM36 LIMIT CHANGE
```

## 1. Parent physical blocker

EVE-MCU-R3H-CF1 physically admitted multi-span Muon projection, including:

```text
physical_span_count=128
copy_command_count=128
covered_elements=2048
gap_count=0
overlap_count=0
admitted=true
```

The former `E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE` blocker was therefore passed by CF1.

The next observed physical blocker was:

```text
memory allocation of 32096400 bytes failed
```

with the canonical full-durable mapped readback still materializing the complete mapped staging range into a second owned `Vec<u8>`.

## 2. Parent source cause

The parent readback authority performed:

```rust
let mapped = staging.slice(..).get_mapped_range();
let bytes = mapped.to_vec();
drop(mapped);
staging.unmap();
...
Ok((bytes, epoch))
```

For the failing window, `staging_bytes` is the exact combined Weight + compact Adam M + compact Adam V readback payload. The additional `mapped.to_vec()` therefore creates a same-size second host allocation while the mapped view is still live.

CF2 removes this ownership duplication. It does not reduce the configured projection window.

## 3. Core authority law

A mapped readback window is itself the temporary host read authority.

Production consumers MUST execute while the mapping is live:

```text
GPU submission
  -> physical completion
  -> map completion
  -> mapped view
  -> borrowed Weight / M / V consumption
  -> consumer returns
  -> drop mapped view
  -> unmap staging buffer
  -> mark unmapped
  -> release submission leases
```

The complete mapped payload MUST NOT be converted to another full-size `Vec<u8>`.

## 4. Canonical scoped readback authority

CF2 replaces the production Vec-return helper with:

```text
with_mapped_full_trainable_projection_window_r3h_cf2
```

The helper owns:

- staging `wgpu::Buffer`
- command encoder and copy commands
- submission lease specs
- tracked submission
- map request and completion polling
- mapped `BufferView`
- scoped consumer invocation
- unmap and lease release

The consumer receives only borrowed slices whose lifetime is bounded by the mapped view.

## 5. Explicit mapped layouts

CF2 introduces:

```text
ProjectionMappedLayoutR3HCF2::WeightOnly
ProjectionMappedLayoutR3HCF2::WeightAdamMv
```

`WeightOnly` requires:

```text
staging_bytes == weight_bytes
```

`WeightAdamMv` requires:

```text
staging_bytes == weight_bytes + 2 * adamw_compact_bytes
```

Any mapped-length/layout drift is fail-closed before downstream consumption.

## 6. Borrowed view

The scoped consumer receives a `BorrowedProjectionWindowR3HCF2` containing only references:

```text
weight: &[u8]
adam_m_compact: &[u8]
adam_v_compact: &[u8]
staging_bytes: u64
```

No payload ownership transfer occurs.

Unit fixtures verify that Weight, M and V slices alias the original mapped backing at the expected offsets.

## 7. Full-durable Weight consumption

The previous full-durable path cloned:

```text
mapped[0..window_bytes] -> Vec<u8>
```

CF2 instead passes the mapped Weight slice directly to existing `&[u8]` consumers:

- `ResidentWeightPackBuilder::append_or_verify_initialized`
- durable Weight writer
- weight successor journal shadow
- R3E durable writer
- Weight SHA-256 hashers
- segment hasher
- numerical Weight delta witness

No full Weight-window clone is introduced under another name.

## 8. Compact Adam M/V consumption

The mapped compact Adam M and V regions are borrowed directly.

Existing logical target M/V buffers remain because mixed Muon/AdamW durable projection still requires logical target-state assembly. They are classified as derived logical target buffers, not copies of the complete mapped staging payload.

CF2 copies only the required compact Adam subranges into those existing logical M/V buffers.

## 9. R3H successor path

The R3H successor resident-Weight materialization path uses the same scoped readback authority with:

```text
ProjectionMappedLayoutR3HCF2::WeightOnly
```

The mapped Weight slice is appended directly into `ResidentWeightPackBuilder` before unmap.

No intermediate successor window `Vec<u8>` is produced.

## 10. Consume-before-unmap closure

After mapping:

```text
consumer result is captured
mapped view is dropped
staging is unmapped
mark_unmapped is executed
submission leases are released
consumer result is then propagated
```

A normal consumer `Err` therefore does not bypass mapped-view cleanup.

Cleanup failures receive separate CF2 attribution.

## 11. No lifetime escape

CF2 adds no unsafe lifetime extension.

Mapped data may not be:

- returned as a borrowed slice,
- stored in runtime state,
- stored through a raw pointer,
- transmuted to a longer lifetime.

The callback boundary structurally keeps mapped bytes inside the staging-buffer owner scope.

## 12. Submission authority preservation

The parent submission sequence remains:

```text
submit_with_leases
mark_map_requested
map_async
poll_nonblocking_and_refresh
submission_completed_nonblocking
mark_mapped_read
consumer
unmap
mark_unmapped
release_submission_leases
```

CF2 introduces:

```text
new wait_for_submission_exact callsites = 0
new submit_with_leases callsites = 0
```

No per-window extra submission or exact wait is added.

## 13. CF1 preservation

CF2 preserves the CF1 physical-span decomposition authority:

```text
decompose_muon_logical_route_to_packed_spans_r3h_cf1
```

and the physical-span guard:

```text
E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE
```

The logical route, packed ABI and physical copy decomposition are not changed by CF2.

## 14. Window geometry preservation

The canonical projection window remains:

```rust
const R6_STREAM_CHUNK_BYTES: usize = 16 * 1024 * 1024;
```

Parent and CF2 values are identical.

CF2 does not reduce the readback window to hide allocation pressure.

## 15. RAM36 preservation

`ram36_process_budget.rs` is byte-preserved from the parent.

The RAM36 hard-limit policy is not inflated, bypassed or conditionally disabled.

CF2 removes a duplicate allocation rather than changing the budget authority.

## 16. R3H / R3G / BP-DK / R3C preservation

CF2 does not modify:

- R3H source resident-Weight retirement authority
- R3H post-retirement process-private observation
- R3G mutation/completion semantics
- BP-DK-R3 RuntimeIdentity policy
- R3C consuming generation commit
- optimizer numerical equations

Expected BP-DK production evidence remains:

```text
identity_policy=RUNTIME_IDENTITY
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0
full_payload_sha_count=0
runtime_identity_count=3
```

## 17. Required runtime witness

Successful mapped consumption emits:

```text
[ASH-EVE-MCU-R3H-CF2][mapped-consume]
```

with:

```text
staging_bytes=...
weight_borrow_bytes=...
adam_m_borrow_bytes=...
adam_v_borrow_bytes=...
mapped_full_window_clone_count=0
mapped_full_window_clone_bytes=0
consumer_completed=true
unmap_after_consume=true
submission_epoch=...
admitted=true
```

The failing parent-size window should be able to report `staging_bytes=32096400` without allocating a same-size second full-window payload.

## 18. Unit fixtures

The bake adds five `r3h_cf2_` fixtures:

```text
r3h_cf2_weight_only_borrowed_window
r3h_cf2_weight_adam_mv_borrowed_layout
r3h_cf2_zero_adamw_window
r3h_cf2_layout_drift_rejected
r3h_cf2_borrowed_view_aliases_original_mapping
```

They qualify borrowed-layout geometry and zero-copy aliasing. Physical mapped cleanup still requires the real WGPU campaign.

## 19. Source scope

Exact code delta:

```text
ADD 0
MOD 1
DEL 0

MOD
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Parent scheduler SHA-256:

```text
0d6e2491d7fdb5de14795faedb0185de40f9f5173ae20beb60425c5e8a623b22
```

CF2 scheduler SHA-256:

```text
de98b59839e6acd2dc08a93ec25abb9d5bbeb8864f0cfb84507fad6c31f68699
```

## 20. Static bake seals

```text
mapped.to_vec() production-file count          0
old Vec-return readback helper count           0
CF2 scoped helper definition + callsites       3
CF2 production callsites                       2
CF2 tests                                      5
CF1 helper references                          preserved
NONCONTIGUOUS guard                            preserved
new wait_for_submission_exact delta            0
new ResidentWeightPack::load_once delta        0
new unsafe delta                               0
new submit_with_leases delta                   0
R6_STREAM_CHUNK_BYTES parent / CF2              identical
changed Rust delimiter balance                 PASS
```

Preserved authority file SHA-256 values:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
  d50e48a515dee72e84ea4939c595610702bc2b322aeabf9412b92f1c2b6f54af

crates/base_train/src/tensorcube_local_muon_optimizer.rs
  067f601397a8ff372b095f22b4f63330753702fbe998f0d0bccba71d4d8345b9

crates/base_train/src/ram36_process_budget.rs
  0394d326e5fddf14501db21412b98a9b4ac9d0377529daee9317baeac0fd4d3e

crates/base_train/src/resident_weight_replacement_authority_r3h.rs
  37079e72dc4c1a02ea53a410f51b35798a04d833ecb2aaac674241d7e3e4c497
```

## 21. Baked artifacts

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF2_BORROWED_MAPPED_READBACK_ZERO_DUPLICATE_HOST_WINDOW_CONSUMPTION_CODE_ONLY.zip
SHA-256 c8224a88420dc2667ccb5ab12a702084d142711d436fa9ff78ec11ad6d610128
Files 8426
CRC PASS
```

Overlay:

```text
ASH_EVE_MCU_R3H_CF2_BORROWED_MAPPED_READBACK_ZERO_DUPLICATE_HOST_WINDOW_CONSUMPTION_OVERLAY_CODE_ONLY.zip
SHA-256 cd0cb15c33454dfd9d8f607e91a5df8b9420bcb713d12aa050988e7d4c1389e3
Files 1
CRC PASS
```

Both code archives contain:

```text
Markdown files 0
specs/ files 0
artifacts/ files 0
```

## 22. Evidence state at bake time

```text
SOURCE / STATIC    PASS
ARCHIVE            PASS
COMPILE            UNVERIFIED
RUNTIME-TEST       UNVERIFIED
PHYSICAL           UNVERIFIED
PERFORMANCE        UNMEASURED
```

The bake environment does not contain a Rust toolchain. Compile/runtime/physical claims require replay on the canonical Windows build authority.

## 23. Qualification commands

Required CF2 tests:

```text
cargo test -p base_train --lib --locked r3h_cf2_ -- --nocapture
cargo test -p base_train --lib --release --locked r3h_cf2_ -- --nocapture
```

Parent regression:

```text
cargo test -p base_train --lib --release --locked r3h_cf1_
cargo test -p base_train --lib --release --locked r3h_
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked bp_dk_r3_
```

Canonical release:

```text
cargo build -p base_train --bin base_train --release --locked -j 1
```

Static/compile/runtime-test promotion token after successful Windows replay:

```text
PASS_EVE_MCU_R3H_CF2_BORROWED_MAPPED_READBACK_ZERO_DUPLICATE_HOST_WINDOW_CONSUMPTION
```

## 24. Physical qualification

Rebuild and reseal the exact current release binary, then rerun:

```text
--eve-mcu-close-r2-phys-canary-r1
```

Required positive evidence:

```text
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose]
  physical_span_count > 1
  gap_count=0
  overlap_count=0
  admitted=true

[ASH-EVE-MCU-R3H-CF2][mapped-consume]
  mapped_full_window_clone_count=0
  mapped_full_window_clone_bytes=0
  consumer_completed=true
  unmap_after_consume=true
  admitted=true
```

The run must progress beyond the former `memory allocation of 32096400 bytes failed` site and either complete the canary or reveal a new independent blocker.

Physical promotion token:

```text
PASS_EVE_MCU_R3H_CF2_PHYSICAL_BORROWED_MAPPED_READBACK
```

Hold token:

```text
HOLD_EVE_MCU_R3H_CF2_MAPPED_READBACK_PHYSICAL_CLOSURE_UNPROVEN
```

## 25. Completion law

CF2 is complete only when the production readback no longer materializes a full mapped payload `Vec<u8>`, Weight and compact Adam M/V are consumed through mapped borrows, mapped bytes cannot escape their staging-buffer lifetime, normal consumer errors still reach unmap/lease cleanup, no additional submission/exact wait/D2H is introduced, the 16 MiB projection window and RAM36 limit are unchanged, CF1 physical-span decomposition remains exact, and the physical campaign crosses the parent full-window allocation failure without recreating an equivalent duplicate allocation elsewhere.

## 26. Final authority law

EVE-MCU-R3H-CF2 removes ownership duplication, not evidence and not capacity policy.

The mapped WGPU readback range is the temporary host authority. Existing consumers operate directly on borrowed ranges while that authority is live. Only after consumption does the mapping close and the submission lease retire.

CF2 therefore preserves the complete GPU-copy, numerical, generation and transaction topology while eliminating the redundant full-window host allocation that blocked the parent physical canary.
