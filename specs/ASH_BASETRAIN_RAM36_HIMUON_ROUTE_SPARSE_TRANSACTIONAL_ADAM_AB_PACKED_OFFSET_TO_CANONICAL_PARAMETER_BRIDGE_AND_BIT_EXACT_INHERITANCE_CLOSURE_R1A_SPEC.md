# ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-PACKED-OFFSET-TO-CANONICAL-PARAMETER-BRIDGE-AND-BIT-EXACT-INHERITANCE-CLOSURE-R1A

## Revision

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-PACKED-OFFSET-TO-CANONICAL-PARAMETER-BRIDGE-AND-BIT-EXACT-INHERITANCE-CLOSURE-R1A`

Parent:

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANDIDATE-OVERLAY-AND-RESIDENT-WEIGHT-SUCCESSOR-HEADROOM-CLOSURE-R1`

## Physical trigger

The parent sparse candidate physically achieved:

- 154 Muon parameters
- 47 explicit AdamW parameters
- 0 mixed parameters
- sparse candidate overlay bytes: 1,582,088,192
- candidate bytes avoided: 7,751,073,792
- ResidentWeightPack successor reservation admitted under the unchanged 36 GiB RAM36 cap

The next failure was:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_MUON_INHERITED_ADAM_STATE_DRIFT_R1:model.layers.0.self_attn.q_proj.weight:98836480`

R1A treats this as an addressing-identity problem first. It does not weaken Muon inherited M/V bit equality and does not infer a HiMuon optimizer-semantic divergence until packed/canonical identity is exact.

## Core correction

The parent sparse path used the incoming packed-state global byte offset as if it were the same coordinate as the route plan's cumulative canonical element offset.

R1A separates four domains:

- `PackedGlobalElementOffsetR1A`
- `CanonicalParameterIndexR1A`
- `ParameterLocalElementOffsetR1A`
- `SparseOverlayElementOffsetR1A`

The production path is now:

`packed global offset -> source record -> existing source-record/canonical mapping -> canonical parameter -> parameter-local offset -> Muon/AdamW route -> committed M/V or sparse overlay`

No packed global offset directly indexes a cumulative canonical route entry.

## New authority

New module:

`crates/base_train/src/ram36_himuon_sparse_adam_packed_canonical_bridge_r1a.rs`

Primary type:

`RamAdamPackedCanonicalParameterBridgeR1A`

Per-source input:

`RamAdamPackedCanonicalSourceBindingInputR1A`

Per-parameter entry records:

- source record ordinal
- parameter ID
- canonical parameter index
- packed element start/count
- route kind
- sparse overlay element start/count
- entry digest

The bridge binds:

- optimizer routing digest
- candidate parameter-set digest
- stable source-record/canonical mapping digest
- parent sparse route-plan digest
- packed range geometry
- compact overlay geometry

## Existing bridge reuse

The existing `SourceRecordCanonicalParameterBridge` remains the source-record-to-canonical SSOT.

R1A adds `mapping_digest_r1a()` over its immutable binding set. The digest deliberately excludes per-step target generation fields so the same source/canonical mapping remains stable across the N8 horizon.

The packed/canonical R1A bridge stores and validates this mapping digest. Each optimizer step rebuilds the existing source/canonical bridge and requires the mapping digest to match the resident R1A bridge before candidate writes continue.

Failure identity:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PACKED_CANONICAL_BRIDGE_DRIFT_R1A`

## Packed range proof

Bridge construction requires source records in exact packed order with no overlap or gap.

Failures include:

- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PACKED_RANGE_OVERLAP_R1A`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PACKED_RANGE_GAP_R1A`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_CANONICAL_PARAMETER_DUPLICATE_BINDING_R1A`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_CANONICAL_PARAMETER_BINDING_MISSING_R1A`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_PARAMETER_ELEMENT_CARDINALITY_DRIFT_R1A`
- `FAIL_ASH_BASETRAIN_RAM36_HIMUON_SPARSE_ADAM_OVERLAY_COORDINATE_DISCONTINUITY_R1A`

Bridge metadata is O(parameter count), not O(model element count).

## Candidate write correction

`RamResidentAdamMv::write_candidate_slices()` keeps the existing packed byte offset ABI.

Sparse mode now immediately resolves that packed coordinate through `RamAdamPackedCanonicalParameterBridgeR1A`.

A candidate chunk crossing a packed parameter boundary is naturally split at the bridge entry boundary before route-specific handling.

### Muon-owned range

Committed M/V is indexed by the exact packed global element range.

Candidate M/V must remain bit exact using `f32::to_bits()` semantics.

No epsilon, NaN normalization or signed-zero normalization is introduced.

If a real divergence remains after exact coordinate resolution, R1A emits:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_MUON_INHERITED_ADAM_STATE_DRIFT_R1A`

The failure payload includes parameter ID, source record ordinal, canonical parameter index, packed global element offset, parameter-local offset and observed/expected M/V bits.

### AdamW-owned range

The resolved parameter-local offset is mapped to the compact sparse overlay through the exact bridge entry.

The parent sparse overlay cursor invariant remains unchanged.

## Commit correction

Parent R1 final sparse commit previously used route-plan cumulative canonical starts as committed M/V destinations.

R1A commit uses the packed/canonical bridge instead:

- source: compact AdamW overlay offset
- destination: exact packed element start
- length: exact packed parameter element count

All scatter geometry is validated before the no-fail mutation boundary.

Muon-owned M/V is never scattered during sparse commit.

Legacy non-sparse full A/B Vec-swap behavior remains unchanged.

## Runtime receipt

File:

`ram36_himuon_sparse_adam_packed_canonical_bridge_r1a.json`

Schema:

`ash.basetrain.ram36_himuon_sparse_adam_packed_canonical_bridge.v1a`

The receipt records route/candidate/source-bridge/packed-bridge digests, source/canonical counts, Muon/AdamW counts, packed logical cardinality, route cardinality and zero-valued structural error counters when admitted.

Physical measurement remains unclaimed statically.

## Runtime admission log

`[ASH-RAM36-HIMUON-SPARSE-ADAM-PACKED-CANONICAL-BRIDGE-R1A]`

It reports source/canonical counts, Muon/AdamW counts, packed/Muon/AdamW element counts, structural error counters, bridge digest and `verdict=ADMITTED`.

Physical hold token:

`HOLD_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_PACKED_CANONICAL_BRIDGE_AND_BIT_EXACT_INHERITANCE_PHYSICAL_PENDING_R1A`

## RAM and disk invariants

Unchanged:

- RAM36 hard limit = 38,654,705,664 bytes
- parent sparse overlay physical size authority
- no full candidate B reallocation
- no Adam candidate HDD spill
- no ResidentWeightPack spill
- no pagefile/swap authority
- HiMuon momentum remains separate
- ResidentWeightPack remains full and exact

R1A adds only bounded per-parameter metadata.

## Baked source truth

Actual diff against the exact parent contains five files.

New:

- `crates/base_train/src/ram36_himuon_sparse_adam_packed_canonical_bridge_r1a.rs`
- `tools/validate_ash_basetrain_ram36_himuon_route_sparse_transactional_adam_ab_packed_offset_to_canonical_parameter_bridge_and_bit_exact_inheritance_closure_r1a_static.py`

Modified:

- `crates/base_train/src/lib.rs`
- `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`
- `crates/base_train/src/ram_resident_adam_mv.rs`

## Static validation

New static PASS token:

`PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_PACKED_OFFSET_TO_CANONICAL_PARAMETER_BRIDGE_AND_BIT_EXACT_INHERITANCE_CLOSURE_R1A_STATIC`

Targeted regression at bake time:

- STATIC PASS: 18
- STATIC FAIL: 0

The chain includes R1A, parent sparse R1, parent RAM36 route-exact R1, legacy RAM Adam A/B, durability, Eve R1/R2, Weight Successor Journal, MCU scheduler/B06/full-model/bounded projection, SubmissionEpoch, MCU transactional commit/control plane, RAM36 underflow/successor ownership, and immutable N2 RAM36 authority.

The bake environment does not contain Cargo/Rustc. No Rust compile PASS and no physical R1A PASS are claimed.

## Physical qualification

The next local campaign must:

1. apply the R1A overlay to the current parent source;
2. compile into a new isolated `CARGO_TARGET_DIR` with incremental compilation disabled;
3. verify the R1A revision/runtime/failure tokens exist in the resulting executable;
4. build the cross-release helper in the same isolated target;
5. materialize Native CF1 with explicit `--target-dir` pointing at that isolated target;
6. regenerate cross-release parent compatibility authority;
7. run N8 with HiMuon and the existing route-sparse Adam A/B admission enabled and Weight Journal disabled.

Required runtime evidence includes:

- packed/canonical bridge admission
- 201 source/canonical mappings for the current authority
- 154 Muon / 47 AdamW / 0 mixed for the current route digest
- zero packed gap/overlap/binding/cardinality/overlay errors
- parent sparse overlay remains 1,582,088,192 bytes
- ResidentWeightPack successor remains admitted under RAM36
- Muon inherited M/V mismatch count = 0, or an exact R1A first-divergence failure
- sparse candidate seal/commit reached if inheritance passes

Only actual physical execution may justify:

`PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_PACKED_CANONICAL_BRIDGE_AND_BIT_EXACT_INHERITANCE_PHYSICAL_R1A`

## Final invariant

Packed layout is not canonical registry order by assumption.

Source-record identity is resolved explicitly.

Canonical parameter identity is resolved explicitly.

Parameter-local position is resolved explicitly.

Sparse overlay position is resolved explicitly.

Muon inherited Adam state remains bit exact.

AdamW candidate state remains sparse.

The 7.21875 GiB parent sparse-candidate RAM win is preserved.

The 36 GiB RAM36 cap is unchanged.

No full B fallback, no HDD spill and no physical PASS without a local physical rerun.
