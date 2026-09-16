# EVE-MCU-R3H-CF6

## CF1 VALIDATION RECEIPT COMPACTION

**Revision:** `EVE-MCU-R3H-CF6`  
**Parent:** `EVE-MCU-R3H-CF5-R1`  
**Class:** validation-observability compaction / success-receipt cardinality reduction

```text
+ NO PER-ROUTE SUCCESS LOG
+ PARAMETER / WINDOW AGGREGATE RECEIPT
+ FIRST-FAILURE DETAIL ONLY
+ EXACT COVERAGE COUNTER PRESERVATION
+ NO VALIDATION WEAKENING
+ OPTIONAL GPU REDUCTION HOOK
```

---

## 1. Purpose

CF6 removes the `O(route_count)` successful CF1 text-receipt stream without weakening CF1 packed-span validation.

Every Muon route still executes the existing CF1 checks for:

- logical route bounds and row identity,
- tile-row decomposition,
- packed start/end identity,
- physical contiguity within each span,
- logical gap/overlap exclusion,
- redundant physical split exclusion,
- exact covered-element closure.

Only the success-observability representation changes.

---

## 2. Parent problem

The parent emitted one line per successful Muon route:

```text
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose] ... admitted=true
```

Large physical campaigns therefore emitted hundreds of thousands of nearly identical lines while `logical_start` and parameter identity advanced.

The logging path also imposed formatting, stderr, PowerShell pipeline, `Tee-Object`, disk append and terminal-rendering overhead unrelated to validation correctness.

---

## 3. CF6 authority

Successful Muon routes now fold into a bounded window-local summary:

```text
[ASH-EVE-MCU-R3H-CF6][muon-packed-window-summary]
```

The summary retains exact totals for:

```text
route_count
logical_element_count
physical_span_count
copy_command_count
covered_element_count
gap_count
overlap_count
min_spans_per_route
max_spans_per_route
first_logical_start
final_logical_end
```

No per-route success receipt is emitted.

The same summary ABI is used by:

- `full-durable-r1`
- `r3h-successor`

---

## 4. First-failure attribution

CF1 decomposition errors remain fail-closed.

Each production callsite attaches route-specific context before propagating a validation failure:

```text
E_R3H_CF6_MUON_PACKED_FIRST_FAILURE
site=...
parameter_index=...
logical_start=...
logical_count=...
```

CF6 does not convert any CF1 failure into a warning or aggregate success.

---

## 5. Counter semantics

For every successful route `r`:

```text
summary.route_count              += 1
summary.logical_element_count    += r.logical_count
summary.physical_span_count      += r.physical_span_count
summary.copy_command_count       += r.physical_span_count
summary.covered_element_count    += r.covered_elements
summary.gap_count                += r.gap_count
summary.overlap_count            += r.overlap_count
```

All cumulative counters use checked arithmetic.

A nonzero route gap, route overlap, or route coverage drift remains fail-closed.

Aggregate admission requires:

```text
gap_count == 0
overlap_count == 0
covered_element_count == logical_element_count
copy_command_count == physical_span_count
```

plus all pre-existing CF1 validation predicates.

Muon routes separated by an AdamW route are not falsely classified as a logical gap. CF6 aggregates only route-local CF1 gap/overlap evidence.

---

## 6. Memory law

Validation bookkeeping is bounded:

```text
O(1) per active window summary
```

CF6 does not retain:

```text
Vec<RouteValidationReceipt>
Vec<SuccessLogRecord>
```

or any `O(route_count)` success-evidence collection.

---

## 7. No geometry / execution change

CF6 does not modify:

```text
logical_muon_tile_row_spans_r3h_cf1
packed_index_for_logical
Muon physical span geometry
copy_buffer_to_buffer cardinality
copy offsets or sizes
CF2 borrowed mapped readback
CF3 submission lease coalescing
CF4 observer checkpoint streaming
CF5 compact objective-probe projection
optimizer mathematics
RAM36 hard limit
runtime policy modes
```

The parent CF1 noncontiguous guards remain present for both full-durable and R3H-successor paths.

---

## 8. Optional GPU reduction hook

CF6 defines the CPU-side aggregate receipt shape expected from a future validation reducer.

CF6 does **not** claim a WGSL/GPU reducer implementation.

A future reducer may replace CPU counter accumulation only if it produces the same summary semantics and exact first-failure attribution contract.

---

## 9. Qualification tests

Added test prefix:

```text
r3h_cf6_
```

Tests:

```text
r3h_cf6_success_routes_aggregate_exactly
r3h_cf6_no_per_route_success_receipt
r3h_cf6_first_gap_failure_preserved
r3h_cf6_first_overlap_failure_preserved
r3h_cf6_counter_totals_match_parent
r3h_cf6_parameter_boundary_resets_summary
```

Required qualification command:

```powershell
cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  r3h_cf6_ `
  -- --nocapture
```

Parent regression remains required for CF5, CF4, CF3, CF2 and CF1 test families.

---

## 10. Physical witness

A successful physical campaign should emit compact receipts such as:

```text
[ASH-EVE-MCU-R3H-CF6][muon-packed-window-summary]
site=full-durable-r1
parameter_index=188
window_logical_start=...
window_logical_count=...
route_count=...
logical_element_count=...
physical_span_count=...
copy_command_count=...
covered_element_count=...
gap_count=0
overlap_count=0
min_spans_per_route=...
max_spans_per_route=...
admitted=true
```

The retired per-route success marker must not appear in production success logging.

Physical PASS requires both:

1. compact CF6 summary receipts with exact zero gap/overlap admission, and
2. continued campaign progress through the same CF1 geometry path.

---

## 11. Bake delta

```text
ADD 0
MOD 1
DEL 0
```

Modified file:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Parent SHA-256:

```text
cd14a404060953818f490110490817af2e1f447f2f9f40ac1c51aa1da5cf9821
```

CF6 SHA-256:

```text
57c5c0f2140196acbce35c315fd19c7bbdaf26909221d1bfba6069cdbbc7b308
```

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF6_CF1_VALIDATION_RECEIPT_COMPACTION_CODE_ONLY.zip
SHA-256 cb6adf667b790f53581c2f6f8204f8adbe00154eb74cd3de3bbf6e9b4e0bee74
FILES 8426
CRC PASS
```

Overlay code-only archive:

```text
ASH_EVE_MCU_R3H_CF6_CF1_VALIDATION_RECEIPT_COMPACTION_OVERLAY_CODE_ONLY.zip
SHA-256 20399fefce3ab9b95e34d38535ec3cf93dfbb86b372b12a73127731c8e8e5260
FILES 1
CRC PASS
```

Both archives contain zero Markdown files, zero `specs/` entries and zero `artifacts/` entries.

---

## 12. Evidence status at bake time

```text
SOURCE / STATIC      PASS
ARCHIVE              PASS
RUST COMPILE         UNVERIFIED
RUNTIME TEST         UNVERIFIED
PHYSICAL             UNVERIFIED
PERFORMANCE          UNMEASURED
GPU REDUCTION        NOT IMPLEMENTED / NOT CLAIMED
```

No compile, runtime or physical PASS is claimed by the bake environment.

---

## 13. Promotion tokens

Static / compile:

```text
PASS_EVE_MCU_R3H_CF6_CF1_VALIDATION_RECEIPT_COMPACTION
```

Exact counter parity:

```text
PASS_EVE_MCU_R3H_CF6_EXACT_VALIDATION_COUNTER_PARITY
```

Physical:

```text
PASS_EVE_MCU_R3H_CF6_PHYSICAL_COMPACT_VALIDATION_RECEIPT
```

Hold:

```text
HOLD_EVE_MCU_R3H_CF6_VALIDATION_RECEIPT_COMPACTION_UNPROVEN
```

---

## 14. Completion law

CF6 is complete only when:

1. every route still executes the full CF1 validation path;
2. successful routes no longer emit one textual CF1 receipt each;
3. exact route/span/copy/coverage/gap/overlap totals are preserved;
4. first failing route context remains available;
5. no validation predicate is removed or weakened;
6. validation bookkeeping stays bounded rather than `O(route_count)`;
7. packed geometry and copy commands remain unchanged;
8. CF2 through CF5 authorities remain unchanged;
9. physical canary demonstrates compact summary receipts without per-route success-log explosion.

> CF6 changes validation evidence representation, not validation strength. Successful route evidence is reduced into exact bounded receipts, while failures remain route-attributed and fail-closed.
