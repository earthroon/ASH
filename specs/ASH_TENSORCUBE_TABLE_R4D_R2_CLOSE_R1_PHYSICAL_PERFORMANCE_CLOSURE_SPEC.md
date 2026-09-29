# TENSORCUBE-TABLE-R4D-R2-CLOSE-R1

## PHYSICAL / PERFORMANCE CLOSURE

```text
TENSORCUBE-TABLE-R4D-R2-CLOSE-R1

PHYSICAL / PERFORMANCE CLOSURE

+ R4D-R2 DURABLE PROJECTION HOST COPY COLLAPSE CLOSURE
+ R4D-R2-CF2 MONOTONIC SEGMENT CURSOR CLOSURE
+ R4D-R2-CF3 PREINITIALIZED SOURCE READ CLOSURE
+ A01 SUBMISSION-LEASE R1 PRESERVATION

+ PER-RUN QUALIFICATION RECEIPT
+ OBSERVE / ACTIVE RUN ROLE
+ R2 / CF2 / CF3 RECEIPT AGGREGATION
+ A01 TELEMETRY AGGREGATION
+ N8 PHASE WALL-TIME SAMPLE

+ POSITIVE PATH WITNESS BEFORE ZERO ADMISSION
+ UNOBSERVED != MEASURED ZERO
+ R2 SOURCE-ALIAS ZERO NOT PROMOTED WITHOUT OBSERVER
+ CF2 MULTI-CHUNK / CROSS-CHUNK WITNESS
+ CF3 ELISION + PHYSICAL-FALLBACK WITNESS
+ CF3 SPOOLED NO-CLONE WITNESS
+ A01 ACTIVE ZERO WITNESS PRESERVATION

+ PERFORMANCE SAMPLE != PERFORMANCE CLOSURE
+ REPEATED SAME-BINARY CROSS-RUN CAMPAIGN REQUIRED

+ NO NEW OPTIMIZER MATH
+ NO NEW GPU TRANSFER / WAIT
+ NO DURABILITY SEMANTIC CHANGE
```

---

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4D-R2-CLOSE-R1

Short name:
R4D-R2-CLOSE-R1

Class:
PHYSICAL QUALIFICATION SCAFFOLD
PERFORMANCE ATTRIBUTION SCAFFOLD
PROMOTION TRUTH GATE
```

Direct bake parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4D_R2_CF3_
PREINITIALIZED_SOURCE_READ_VERIFY_SCRATCH_COLLAPSE_CODE_ONLY.zip

SHA-256
8ef8d9b7c015d40440dd0613effe93a42371c1028ee1240adf138ff6e0d6d1bb
```

---

## 1. Current Evidence Boundary

The parent is:

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

CLOSE-R1 does not infer any higher evidence grade from the existing source/static state.

---

## 2. Scope

CLOSE-R1 adds no new production optimization law.

It aggregates already existing R2 / CF2 / CF3 / A01 evidence into one per-run receipt and records one existing N8 phase-wall performance sample.

It does not change:

```text
optimizer math
shader / WGSL
R2 streaming geometry
CF2 cursor semantics
CF3 same-source proof semantics
A01 lease lifecycle
CF11 candidate bytes / SHA
durability ordering
```

---

## 3. Runtime Mode

Environment:

```text
ASH_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_MODE
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

CLOSE-R1 code is inert in normal production when OFF.

---

## 4. OBSERVE Mode Binding

CLOSE-R1 OBSERVE requires:

```text
R4D-R2      = ACTIVE
R4D-R2-CF2  = ACTIVE
R4D-R2-CF3  = OBSERVE
```

CF3 remains the shadow parity authority for this run.

CLOSE-R1 does not call OBSERVE a performance candidate.

---

## 5. ACTIVE Mode Binding

CLOSE-R1 ACTIVE requires:

```text
R4D-R2      = ACTIVE
R4D-R2-CF2  = ACTIVE
R4D-R2-CF3  = ACTIVE
```

A01 is independently read from:

```text
ASH_A01_SUBMISSION_LEASE_R1_MODE
```

When A01 is ACTIVE, its frontier/reevaluation and hot-path zero telemetry participate in CLOSE-R1 physical qualification.

---

## 6. Zero Evidence Representation

CLOSE-R1 materializes:

```text
UNOBSERVED
MEASURED_ZERO
MEASURED_NON_ZERO
```

plus an optional numeric value.

A zero may pass only when it is represented as:

```text
MEASURED_ZERO + Some(0)
```

Literal/default zero is not sufficient.

---

## 7. R2 Source-Alias Truth Repair Boundary

Current R4D-R2 exposes:

```text
source_alias_leak_count
```

but the parent source has no source-backed mutation/observation authority for that field.

Therefore CLOSE-R1 deliberately records:

```text
r2_source_alias_observation = UNOBSERVED
```

and does not promote the parent's literal/default zero into physical evidence.

Consequently the current bake cannot issue physical PASS until a real alias observation authority exists and is exercised.

This is intentional fail-closed evidence handling, not a runtime fallback.

---

## 8. R2 Physical Gates

CLOSE-R1 reads the existing R2 receipt and requires positive path exercise plus zero forbidden-work counters.

Positive witness:

```text
weight_span_count > 0
```

Forbidden physical work:

```text
resident sequential owned-copy bytes
resident full f32 materialization bytes
mapped projection full-clone bytes
resident Adam M/V full-window clone bytes
R3B candidate full-window clone bytes
full-window serialization Vec bytes
statistics rescan bytes
```

All must be zero in the physically exercised ACTIVE path.

R2 projection D2H remains separately visible and is not required to be zero.

R2 scratch must remain within the existing 64 KiB authority.

---

## 9. CF2 Physical Gates

Positive witnesses:

```text
weight_cursor_open_count > 0
weight_chunk_visit_count > 1
cursor_cross_window_retention_count > 0
mv_cursor_open_count > 0
route_cursor_open_count > 0
route_cursor_visit_count > 0
```

Only after those witnesses may CLOSE-R1 admit measured zero for:

```text
per_chunk_full_parameter_scan_count
per_route_full_parameter_scan_count
parameter_segment_vec_materialization_count
parameter_segment_secondary_sort_count
legacy_segments_for_parameter_call_count
```

This is stricter than a source-only zero claim.

---

## 10. CF3 Physical Gates

Positive witnesses:

```text
initialized_base_read_count > 0
direct_host_same_source_overlay_elision_count > 0
append_same_source_verify_elided_bytes > 0
append_physical_verify_bytes > 0
provenance_invalidated_bytes > 0
paged_spool_no_clone_witness_count > 0
```

Required zero/bound:

```text
paged_spool_file_clone_count = MEASURED_ZERO
verify_scratch_peak_bytes <= 64 KiB
```

Thus CLOSE-R1 proves both:

```text
same-source verification elision executed
AND
unproven physical verification remained live
```

before CF3 may be physically closed.

---

## 11. A01 Preservation Gates

When A01 ACTIVE is requested, CLOSE-R1 requires:

```text
r1_completion_frontier_advance_count > 0
r1_release_local_reevaluation_count > 0
```

and measured zero for:

```text
r1_hotpath_full_census_count
r1_hotpath_full_registry_key_materialization_count
```

When A01 is not ACTIVE these fields are UNOBSERVED for CLOSE-R1 qualification and are not converted to zero evidence.

---

## 12. Performance Sample Boundary

CLOSE-R1 records the existing N8 phase receipt fields:

```text
total wall
training-loop wall
training-compute wall
optimizer wall
AdamW wall
Muon wall
final durability wall
storage publication wall
storage copy wall
storage digest-verify wall
finalization wall
final weight/M/V bytes
```

This is one run sample.

The receipt explicitly reports:

```text
UNMEASURED_REQUIRES_REPEATED_SAME_BINARY_CROSS_RUN_CAMPAIGN
```

for performance classification.

One runtime sample can never issue a final performance PASS.

---

## 13. Performance Closure Requirement

Final performance closure remains a later runtime campaign requirement:

```text
same source
same release binary
same model
authorized same dataset / batch / route
the same durability and logging policy
repeated baseline / active arms
```

CLOSE-R1 does not invent an arbitrary minimum speedup threshold.

Valid future classifications include:

```text
IMPROVED
NEUTRAL_WITHIN_OBSERVED_VARIANCE
REGRESSED
INSUFFICIENT_SIGNAL
```

---

## 14. Runtime Receipt

File:

```text
tensorcube_table_r4d_r2_close_r1_physical_performance_closure_receipt.json
```

Compact log:

```text
[ASH-TENSORCUBE-TABLE-R4D-R2-CLOSE-R1][physical-performance-closure]
```

Physical token is either:

```text
PASS_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_PHYSICAL
```

or:

```text
HOLD_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_PHYSICAL
```

Current source-alias evidence boundary makes the first token unreachable until that observer is genuinely implemented and exercised.

Performance token remains:

```text
HOLD_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_PERFORMANCE_REQUIRES_CROSS_RUN_CAMPAIGN
```

in this bake.

Final token remains:

```text
HOLD_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_REQUIRES_PHYSICAL_AND_PERFORMANCE_PROMOTION
```

until later runtime evidence exists.

---

## 15. Scheduler Integration

At the existing N8 final evidence boundary, after sealing:

```text
R4D-R2 receipt
R4D-R2-CF2 receipt
R4D-R2-CF3 receipt
```

CLOSE-R1, when enabled, snapshots:

```text
A01 submission lease telemetry
N8 phase wall-time receipt
```

and materializes one aggregate run receipt.

No extra GPU submission, map, poll, or durability operation is introduced.

---

## 16. Actual Bake Delta

```text
MOD 2
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r2_close_r1_physical_performance_closure.rs
tools/validate_ash_tensorcube_table_r4d_r2_close_r1_physical_performance_closure_static.py
```

No parent optimizer/CF11/A01 implementation source is modified by CLOSE-R1.

---

## 17. Source Seals

```text
crates/base_train/src/lib.rs
e8f55d24695945406c9271f835930fd89273351c6b2132fcedeb5e6036fdf5ee

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
a0f394fd42980750595d2337cd86354e9a08f7c43bc6a8dfcb19acea299f652a

crates/base_train/src/tensorcube_table_r4d_r2_close_r1_physical_performance_closure.rs
03da9cd48c8ba78054e26453570022f0a687ee15669070111fd4bfd5de6d9798

tools/validate_ash_tensorcube_table_r4d_r2_close_r1_physical_performance_closure_static.py
0a7ffc72f2353ec3ea4f370eacbd6c32d2cc1a4468fd46bf98bddb3dc2292ae6
```

---

## 18. Protected Graph

```text
Cargo.toml unchanged
Cargo.lock unchanged

WGSL parent = 321
WGSL work   = 321
WGSL changed / added / deleted = 0 / 0 / 0
```

CLOSE-R1 adds no shader/package graph mutation.

---

## 19. Static Acceptance

CLOSE-R1:

```text
PASS_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_PHYSICAL_PERFORMANCE_CLOSURE_STATIC checks=84
```

Selected parent regressions:

```text
CF3         120/120 PASS
CF2         105/105 PASS
R4D-R2      140/140 PASS
A01          53/53 PASS
R4D-R1      145/145 PASS
CF8         136/136 PASS
CF7         151/151 PASS
R0B         178/178 PASS
R0A         104/104 PASS
CF6         135/135 PASS
CF5         127/127 PASS
CF4          67/67 PASS
CF3-slot     77/77 PASS
R4B-CF3     127/127 PASS
R1                  PASS
B06          63/63 PASS
CF11         64/64 PASS
```

No parent validator source was modified.

---

## 20. Artifact Packaging Law

Code ZIPs intentionally exclude:

```text
specs/
artifacts/
*SPEC.md
generated manifest JSON
__pycache__ / *.pyc
```

Source-code modules whose Rust/Python filenames contain the word `manifest` remain code.

Overlay code-only ZIP:

```text
ASH_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_
PHYSICAL_PERFORMANCE_CLOSURE_OVERLAY_CODE_ONLY.zip

SHA-256
62e0af3087f7596bb3aa24d51537d8db55890b4f59a856902b8e5c003fd8bd64

files=4
CRC=PASS
```

Full code-only ZIP:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4D_R2_CLOSE_R1_
PHYSICAL_PERFORMANCE_CLOSURE_CODE_ONLY.zip

SHA-256
49c7aa826ba7175146af92de12dda8876ba82f36af71020026e5e985c530c84a

files=8536
CRC=PASS
```

---

## 21. Evidence State After Bake

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

Rust toolchain is unavailable in the bake environment.

No compile/runtime/physical/performance claim is promoted.

---

## 22. Compile Acceptance

Authoritative local environment must run:

```powershell
cargo check `
  -p burn_webgpu_backend `
  --lib `
  --release `
  --locked `
  -j 1

cargo check `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked `
  -j 1
```

All must PASS before COMPILE promotion.

---

## 23. Runtime Qualification Order

```text
1. COMPILE
2. CLOSE-R1 OBSERVE run
3. CLOSE-R1 ACTIVE run
4. resolve R2 source-alias observer evidence gap
5. ACTIVE physical promotion
6. repeated same-binary baseline/active performance campaign
7. performance classification
8. final CLOSE-R1 promotion
```

The source-alias observer gap is not silently skipped.

---

## 24. R4D-R3 Handoff

After physical/performance closure, measured durability evidence becomes input to:

```text
TENSORCUBE-TABLE-R4D-R3
GENERATION DURABILITY I/O COMPACTION
```

Relevant existing timings include:

```text
final durability wall
storage publication wall
storage copy wall
storage digest-verify wall
finalization wall
```

CLOSE-R1 does not claim `sync_all` dominance before the runtime measurements demonstrate it.

---

## 25. Completion Law

This bake may claim only:

```text
SOURCE BAKED
STATIC PASS
qualification receipt path implemented
false-zero promotion blocked for R2 source alias
single-run performance sample path implemented
```

It may not claim:

```text
COMPILE PASS
RUNTIME PASS
PHYSICAL PASS
PERFORMANCE IMPROVEMENT
R2 FINAL CLOSED
```

until those higher evidence layers are actually produced.

---

## 26. Final Law

> **CLOSE-R1 is an evidence closure layer, not another optimizer revision.**

> **A physical zero requires an exercised runtime authority. The uninstrumented R2 source-alias counter is therefore represented as UNOBSERVED rather than being promoted from literal/default zero.**

> **CF2 requires actual multi-chunk and cross-chunk cursor execution before its zero scan/materialization counters can participate in physical promotion.**

> **CF3 requires both successful same-source elision and successful physical fallback verification, plus an exercised spooled no-clone witness, before its optimized verification path can close.**

> **One N8 timing receipt is a performance sample, not a performance conclusion. Repeated same-binary cross-run comparison remains mandatory.**

> **No durability barrier is changed in CLOSE-R1. Measured durability timings are handed to R4D-R3 as evidence, not assumed to be the next bottleneck.**
