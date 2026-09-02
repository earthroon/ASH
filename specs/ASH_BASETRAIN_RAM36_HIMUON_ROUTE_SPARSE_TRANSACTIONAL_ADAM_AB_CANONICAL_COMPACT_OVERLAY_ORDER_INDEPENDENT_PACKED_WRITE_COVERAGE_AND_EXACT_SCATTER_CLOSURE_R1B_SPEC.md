# ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANONICAL-COMPACT-OVERLAY-ORDER-INDEPENDENT-PACKED-WRITE-COVERAGE-AND-EXACT-SCATTER-CLOSURE-R1B

## Revision

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANONICAL-COMPACT-OVERLAY-ORDER-INDEPENDENT-PACKED-WRITE-COVERAGE-AND-EXACT-SCATTER-CLOSURE-R1B`

Parent:

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-PACKED-OFFSET-TO-CANONICAL-PARAMETER-BRIDGE-AND-BIT-EXACT-INHERITANCE-CLOSURE-R1A`

## Physical trigger

The R1 sparse candidate path already physically established the RAM objective:

- sparse Adam candidate overlay: 1,582,088,192 bytes
- candidate bytes avoided: 7,751,073,792 bytes
- ResidentWeightPack successor reservation admitted under the unchanged 36 GiB RAM36 hard cap

R1A then reached the packed/canonical bridge under a valid Native CF1 and cross-release chain but rejected the bridge with:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_OVERLAY_COORDINATE_DISCONTINUITY_R1A`

The failure is caused by requiring AdamW compact overlay offsets encountered in packed traversal to be globally monotonic. That reintroduces the invalid assumption that packed AdamW parameter order equals canonical compact overlay order.

## R1B decision

R1B keeps three order domains independent:

1. packed candidate arrival order;
2. canonical parameter order;
3. canonical compact sparse-overlay layout order.

The existing R1A packed-to-canonical bridge remains the parameter-identity SSOT.

The parent R1 compact overlay remains laid out in canonical route order.

Candidate writes may arrive in packed order. Correctness is proven by per-AdamW-parameter coverage, not by a global overlay destination cursor.

## Canonical overlay layout

R1B modifies the R1A bridge validation so packed-range validation and overlay-layout validation are separate traversals.

Packed traversal proves:

- packed range continuity;
- no packed overlap;
- source-record/canonical identity;
- parameter cardinality.

Overlay traversal sorts AdamW bridge entries by `sparse_overlay_element_start` and proves:

- first compact overlay start is zero;
- no compact overlay gap;
- no compact overlay overlap;
- final compact overlay end equals exact AdamW element count.

New failures:

- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_CANONICAL_OVERLAY_LAYOUT_GAP_R1B`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_CANONICAL_OVERLAY_LAYOUT_OVERLAP_R1B`

Packed traversal is no longer allowed to require `expected_overlay == overlay_cursor`.

## Coverage SSOT

New module:

`crates/base_train/src/ram36_himuon_sparse_adam_order_independent_overlay_coverage_r1b.rs`

New authority:

`RamAdamSparseOverlayCoverageLedgerR1B`

New entry:

`RamAdamSparseOverlayCoverageEntryR1B`

Each AdamW parameter tracks:

- canonical parameter index;
- parameter ID;
- canonical compact overlay start;
- expected element count;
- written element count;
- next expected parameter-local element;
- write operation count;
- completion state;
- entry digest.

The ledger is O(AdamW parameter count), not O(model element count).

No per-element bitmap or full-model coverage table is introduced.

## Candidate write semantics

The production write ABI remains the existing packed-byte-offset interface.

R1A resolves:

`packed offset -> source record -> canonical parameter -> parameter-local offset -> route kind`

For Muon-owned ranges, R1A bit-exact inherited M/V validation is unchanged.

For AdamW ranges, physical destination is:

`compactOverlayElementStart + parameterLocalElementOffset`

Inter-parameter arrival order is not constrained.

Within each AdamW parameter, local writes remain sequential and exact.

Gap failure:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PARAMETER_LOCAL_WRITE_GAP_R1B`

Replay/overlap failure:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PARAMETER_LOCAL_WRITE_REPLAY_OR_OVERLAP_R1B`

Overrun failure:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PARAMETER_LOCAL_WRITE_OVERRUN_R1B`

Overlay range failure:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_OVERLAY_RANGE_OUT_OF_BOUNDS_R1B`

The legacy field `candidate_overlay_cursor_elements` remains only as an aggregate written-element count for compatibility. It is no longer a sparse physical destination ordering authority.

## Seal

Sparse candidate seal requires the R1B ledger to be complete.

Required:

- every AdamW ledger entry complete;
- total written AdamW elements equals exact plan AdamW element count;
- parameter-local gap count = 0;
- replay/overlap count = 0;
- overrun count = 0;
- parent logical full candidate M/V coverage exact;
- parent logical M/V SHA exact;
- R1A Muon inheritance checks exact.

Incomplete coverage fails with:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_ORDER_INDEPENDENT_COVERAGE_INCOMPLETE_R1B`

## Abort and reuse

Candidate begin resets only O(parameter count) coverage metadata.

The physical sparse M/V overlay allocation is retained and reused.

Abort resets the R1B coverage ledger and leaves committed M/V unchanged.

No full candidate reallocation or copy-back is introduced.

## Exact scatter commit

Sparse commit remains a deterministic scatter from canonical compact overlay to exact packed committed M/V destinations.

For every AdamW parameter:

- source = canonical compact overlay start;
- destination = exact packed element start from R1A bridge;
- length = exact parameter element count.

Before mutation, R1B validates:

- all source ranges are inside M/V overlay allocations;
- all destination ranges are inside committed M/V;
- total scatter elements equal exact AdamW element count;
- compact source ranges are gap-free and non-overlapping;
- packed destination ranges are non-overlapping.

Scatter entries are sorted by packed destination before mutation for deterministic increasing committed destinations.

Failure:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_EXACT_SCATTER_GEOMETRY_INVALID_R1B`

After the no-fail mutation boundary starts, no allocation, filesystem operation, route reconstruction, hash finalization or fallible geometry validation is allowed.

Muon-owned committed M/V is not written by the sparse scatter.

## Runtime receipt

File:

`ram36_himuon_sparse_adam_order_independent_overlay_coverage_r1b.json`

Schema:

`ash.basetrain.ram36_himuon_sparse_adam_order_independent_overlay_coverage.v1b`

The receipt records:

- packed/canonical bridge digest;
- coverage ledger digest;
- ledger entry count;
- complete/incomplete counts;
- expected/written AdamW elements;
- local gap/replay/overrun counters;
- order-independent write count;
- `packedWriteOrderMonotonicRequired=false`;
- `canonicalOverlayOrderPreserved=true`;
- full candidate M/V allocation counts = 0;
- physical PASS claimed false.

## Runtime logs

Admission:

`[ASH-RAM36-HIMUON-SPARSE-ADAM-ORDER-INDEPENDENT-OVERLAY-R1B]`

Seal coverage:

`[ASH-RAM36-HIMUON-SPARSE-ADAM-OVERLAY-COVERAGE-R1B]`

Commit scatter:

`[ASH-RAM36-HIMUON-SPARSE-ADAM-EXACT-SCATTER-R1B]`

Physical HOLD token:

`HOLD_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_ORDER_INDEPENDENT_OVERLAY_COVERAGE_AND_EXACT_SCATTER_PHYSICAL_PENDING_R1B`

Physical PASS token is reserved for actual N8 qualification:

`PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_ORDER_INDEPENDENT_OVERLAY_COVERAGE_AND_EXACT_SCATTER_PHYSICAL_R1B`

## Preserved invariants

R1B does not change:

- RAM36 hard cap of 38,654,705,664 bytes;
- sparse candidate physical allocation size;
- ResidentWeightPack successor representation;
- R1A packed/canonical bridge identity;
- Muon inherited M/V bit-exact rule;
- optimizer math;
- HiMuon routing;
- durable full Adam M/V pack format;
- TensorCube/HiMuon momentum ownership;
- Weight Journal policy;
- legacy full A/B path when sparse admission is disabled.

Forbidden:

- full candidate B reintroduction;
- candidate overlay HDD spill;
- pagefile/swap authority;
- silent packed/canonical order approximation;
- silent last-write-wins coverage repair;
- RAM36 limit increase.

## Baked source truth

Actual diff against the exact R1A full-source parent contains six files.

New:

- `crates/base_train/src/ram36_himuon_sparse_adam_order_independent_overlay_coverage_r1b.rs`
- `tools/validate_ash_basetrain_ram36_himuon_route_sparse_transactional_adam_ab_canonical_compact_overlay_order_independent_packed_write_coverage_and_exact_scatter_closure_r1b_static.py`

Modified:

- `crates/base_train/src/lib.rs`
- `crates/base_train/src/ram36_himuon_sparse_adam_packed_canonical_bridge_r1a.rs`
- `crates/base_train/src/ram_resident_adam_mv.rs`
- `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`

## Static validation

Bake regression result:

- STATIC PASS: 19
- STATIC FAIL: 0

The chain includes R1B, R1A, parent sparse R1, RAM36 HiMuon route-exact R1, legacy transactional Adam A/B, trainable-generation durability, Eve R1/R2, Weight Successor Journal Shadow, MCU AdamW scheduler, MCU B06 ledger, full-model segmented successor, bounded durable projection, SubmissionEpoch dependency, MCU active transactional commit/restart, MCU control plane, RAM36 underflow attribution, successor-weight physical ownership transition, and immutable N2 RAM36 authority.

The bake environment does not contain Cargo or Rustc. No Rust compile PASS and no physical N8 PASS are claimed.

## Physical qualification

The next local campaign must use:

1. a fresh isolated `CARGO_TARGET_DIR`;
2. incremental compilation disabled;
3. the exact R1B `base_train.exe`;
4. cross-release helper built before Native CF1 sealing;
5. Native CF1 materialized last with explicit `--target-dir`;
6. a fresh cross-release authority bound to that exact consumer binary and CF1;
7. HiMuon production route ON;
8. route-sparse Adam A/B ON;
9. Weight Journal OFF for baseline physical qualification.

Required runtime milestones:

- R1A packed/canonical bridge reaches `verdict=ADMITTED`;
- R1B order-independent overlay reaches `verdict=ADMITTED`;
- parent sparse physical overlay remains 1,582,088,192 bytes for the current route authority;
- ResidentWeightPack successor remains admitted under RAM36;
- Muon inheritance reaches exact R1A verification;
- R1B coverage reaches `verdict=EXACT`;
- exact scatter reaches `verdict=COMMITTED`;
- no full candidate allocation;
- no RAM36 rejection;
- no HDD spill.

If R1A exact Muon inheritance still fails after R1B bridge and coverage admission, that exact first divergence becomes the next SSOT for real HiMuon M/V semantic investigation.

## Final invariant

Canonical overlay layout is canonical.

Packed arrival order is packed.

They are not required to match.

Parameter identity bridges them.

Parameter-local ordering proves each AdamW parameter write.

Per-parameter ledger proves candidate completeness.

Exact scatter maps compact canonical AdamW state into exact packed committed destinations.

Muon M/V remains inherited bit-exactly.

The sparse RAM win remains intact.

The 36 GiB cap remains intact.

No full B fallback, no HDD spill, no silent order repair, and no physical PASS without physical execution.
