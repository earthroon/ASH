# ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANDIDATE-OVERLAY-AND-RESIDENT-WEIGHT-SUCCESSOR-HEADROOM-CLOSURE-R1

## Revision

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANDIDATE-OVERLAY-AND-RESIDENT-WEIGHT-SUCCESSOR-HEADROOM-CLOSURE-R1`

Parent source authority:

`ASH-BASETRAIN-RAM36-HIMUON-CORESIDENT-ROUTE-EXACT-OPTIMIZER-TRANSIENT-BOUND-AND-STALE-PARENT-PEAK-RETIREMENT-CLOSURE-R1`

## Physical trigger

Parent physical attribution identified `ResidentWeightPack` successor reservation as the actual N8 RAM36 blocker.

Observed route:

- Muon parameters: 154
- Explicit AdamW parameters: 47
- Mixed parameters: 0
- Muon elements: 968,884,224
- AdamW elements: 197,761,024
- Total trainable elements: 1,166,645,248

Observed successor failure:

- requested bytes: 4,666,580,992
- observed private bytes: 34,880,507,904
- projected bytes: 39,547,088,896
- RAM36 hard limit: 38,654,705,664
- exact excess bytes: 892,383,232
- owner: `ResidentWeightPack`
- projection-only over limit: true

The route-exact optimizer transient matched the historical parent bound within 118 bytes, so transient inflation is not the target of this revision.

## Objective

Keep one full canonical committed Adam M/V state while replacing the second full physical transactional candidate mirror with an AdamW-only route-sparse candidate overlay.

Logical A/B semantics remain complete:

- committed A is full canonical M/V;
- candidate B is still a complete logical canonical candidate;
- Muon-owned candidate M/V inherits committed A bit-exactly;
- AdamW-owned candidate M/V is stored in a compact overlay;
- full logical candidate hashes remain canonical full-pack hashes;
- commit remains permit-gated and failure-atomic.

Only the physical RAM representation changes. Optimizer math, route ownership, ResidentWeightPack format, durable Adam pack format, and the 36 GiB process cap remain unchanged.

## Admission

New explicit CLI:

`--admit-ram36-himuon-route-sparse-transactional-adam-ab`

Default: false.

Sparse mode requires N8 continuity, RAM-resident Adam, exact RAM inventory, RAM36 process authority, RAM36 enforcement, persistent ResidentWeightPack, TensorCube local-Muon production callsite, and an exact verified Muon registry.

Missing parent authority fails with:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_PARENT_ADMISSION_MISSING_R1`

## Route SSOT

New module:

`crates/base_train/src/ram36_himuon_route_sparse_transactional_adam_ab_r1.rs`

The plan is derived from the existing verified `FirstCandidateEligibilityRegistry` and binds the current `optimizer_routing_digest` and candidate parameter-set digest.

New types:

- `RamAdamRouteSparseOverlayPlanR1`
- `RamAdamRouteSparseOverlayEntryR1`
- `RamAdamRouteSparseEntryKindR1`

The plan records canonical per-parameter ranges, compact overlay offsets, Muon/AdamW counts, logical full bytes, physical overlay bytes, avoided bytes, and a plan digest.

R1 rejects any mixed Muon/AdamW parameter:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_MIXED_PARAMETER_UNSUPPORTED_R1`

No silent whole-parameter fallback is allowed.

## Current physical geometry

Current route arithmetic:

- full logical M bytes: 4,666,580,992
- full logical V bytes: 4,666,580,992
- legacy full candidate B: 9,333,161,984 bytes
- AdamW overlay M: 791,044,096 bytes
- AdamW overlay V: 791,044,096 bytes
- sparse candidate B: 1,582,088,192 bytes
- physical candidate bytes avoided: 7,751,073,792 bytes = 7.21875 GiB

These are route-derived planning values. Physical process-memory PASS remains pending local N8 execution.

## RAM ownership

Existing owners remain:

- `AdamMResident`
- `AdamVResident`
- `ResidentWeightPack`
- `TensorCubeLocalMuonMomentum`

New persistent sparse candidate owners:

- `AdamMRouteSparseCandidateOverlay`
- `AdamVRouteSparseCandidateOverlay`

Legacy full candidate owners remain for non-sparse execution:

- `AdamMCandidateResident`
- `AdamVCandidateResident`

The new owners participate in RAM36 persistent-footprint attribution.

## Exact inventory

`BaseTrainRamInventoryAuthority` adds:

`register_adam_route_sparse_candidate_overlay_r1(adamw_element_count)`

The sparse physical size is bound to `RuntimeOwnedCapacity`, not to the full packed-state manifest. Historical parent inventory evidence is not rewritten.

## Allocation lifecycle

Legacy mode retains existing full candidate allocation.

Sparse mode:

1. hydrates full committed M/V;
2. loads the verified production Muon runtime;
3. builds and validates the route-sparse plan;
4. reserves sparse M overlay under RAM36;
5. reserves sparse V overlay under RAM36;
6. allocates both overlay vectors once;
7. verifies materialized bytes;
8. registers sparse runtime-owned capacity;
9. reuses the same allocations across N8 generations.

No full candidate M/V vectors are allocated on the sparse path.

Admission log:

`[ASH-RAM36-HIMUON-ROUTE-SPARSE-ADAM-AB-R1]`

Physical HOLD token:

`HOLD_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_PHYSICAL_PENDING_R1`

## Candidate write semantics

`write_candidate_slices` remains the production write ABI and becomes representation-aware.

Full logical candidate M/V is still hashed in canonical write order.

For Muon-owned ranges, candidate M/V must be bit-exact to committed M/V and is not copied into the overlay.

Mismatch token:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_MUON_INHERITED_ADAM_STATE_DRIFT_R1`

For AdamW-owned ranges, candidate M/V is copied into the compact overlay at the sealed plan offset. Overlay writes are ordered, gap-free and duplicate-free.

Coverage token:

`FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_OVERLAY_COVERAGE_INCOMPLETE_R1`

## Candidate seal

The existing logical candidate seal remains authoritative.

Sparse mode additionally requires:

- logical candidate cursor equals full canonical M/V bytes;
- overlay cursor equals exact AdamW element count;
- expected canonical M SHA matches;
- expected canonical V SHA matches.

No full temporary candidate vector is assembled for hashing.

## Commit

Legacy mode retains full Vec-swap commit.

Sparse mode uses a prevalidated deterministic scatter commit:

- validate permit and generation identity;
- validate route plan and overlay cardinality;
- build and validate scatter geometry before mutation;
- enter no-fail mutation boundary;
- copy AdamW overlay M/V into canonical committed ranges;
- leave Muon-owned committed M/V unchanged;
- advance committed training/optimizer generations;
- return overlay to inactive reusable state.

No allocation, filesystem operation, route lookup, GPU synchronization, or fallible validation is introduced after sparse mutation begins.

Sparse commit log:

`[ASH-RAM-ADAM-ROUTE-SPARSE-TRANSACTIONAL-AB-R1]`

## Abort

Abort before commit preserves committed M/V and committed generation identities, clears logical/overlay candidate state, and retains overlay capacity for reuse. No copy-back is required because committed A is not modified before permit.

## Transaction receipt

Sparse mode does not emit the old two-full-physical-slot receipt as if it described the new topology.

New schema:

`ash.basetrain.ram_adam_route_sparse_transactional_ab.v1`

New file:

`ram_adam_route_sparse_transactional_ab_receipt_r1.json`

It records one full committed physical slot, one sparse candidate overlay slot, two logical A/B roles, route-plan digest, logical full M/V bytes, physical overlay bytes, avoided bytes, transaction counters, overlay reuse, full candidate allocation counts of zero, and physical RAM36 PASS claimed false.

## ResidentWeightPack headroom

The successor weight remains a full canonical `ResidentWeightPack`.

Sparse mode emits a fresh RAM36 projection immediately before successor reservation.

New file:

`ram36_himuon_route_sparse_adam_ab_headroom_r1.json`

Schema:

`ash.basetrain.ram36_himuon_route_sparse_transactional_adam_ab_headroom.v1`

It records route/plan digests, legacy full candidate bytes, sparse overlay bytes, avoided bytes, observed private bytes, outstanding reservation bytes, successor requested bytes, projected bytes, RAM36 hard limit, remaining headroom, successor admission projection, full candidate allocation counts of zero, overlay allocation count one, HDD spill bytes zero, and physical PASS claimed false.

Runtime log:

`[ASH-RAM36-HIMUON-ROUTE-SPARSE-HEADROOM-R1]`

The actual successor still passes through ordinary exact RAM36 `ResidentWeightPack` reservation with no discount.

## Prohibitions

R1 introduces no RAM36 inflation, hidden limit override, Adam candidate HDD spill, weight successor HDD spill, pagefile/swap authority, Weight Journal backing store, HiMuon momentum aliasing, silent full-candidate fallback, optimizer math change, or weight format change.

## Compatibility

Without the new sparse admission flag, existing full transactional A/B behavior remains unchanged, including full candidate allocation and Vec swap commit.

## Static validation

New validator:

`tools/validate_ash_basetrain_ram36_himuon_route_sparse_transactional_adam_ab_candidate_overlay_and_resident_weight_successor_headroom_closure_r1_static.py`

Bake regression result:

- static PASS: 17
- static FAIL: 0

The chain includes this R1, parent RAM36 HiMuon co-resident R1, Weight Successor Journal Shadow, legacy RAM Adam A/B, trainable-generation durability, Eve R1/R2, MCU AdamW active-device scheduler, MCU B06 backing ledger, full-model segmented successor, bounded durable projection, submission epoch dependency, MCU transactional commit/restart, MCU control plane, RAM36 underflow attribution, RAM36 successor ownership transition, and immutable N2 RAM36 authority.

The bake environment has no Cargo/Rustc, so no Rust compile PASS or physical N8 PASS is claimed.

## Baked source truth

Actual diff against the exact parent contains 10 files.

New:

- `crates/base_train/src/ram36_himuon_route_sparse_transactional_adam_ab_r1.rs`
- `tools/validate_ash_basetrain_ram36_himuon_route_sparse_transactional_adam_ab_candidate_overlay_and_resident_weight_successor_headroom_closure_r1_static.py`

Modified:

- `crates/base_train/src/bin/base_train.rs`
- `crates/base_train/src/config.rs`
- `crates/base_train/src/lib.rs`
- `crates/base_train/src/pipeline.rs`
- `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`
- `crates/base_train/src/ram36_process_budget.rs`
- `crates/base_train/src/ram_budget_exact_inventory.rs`
- `crates/base_train/src/ram_resident_adam_mv.rs`

## Physical qualification

The next campaign must compile from a fresh isolated target directory, materialize Native CF1 using the same explicit `--target-dir`, regenerate the N8 cross-release authority, then run N8 with the new sparse admission flag.

Required physical evidence includes sparse route admission, mixed=0, one sparse overlay allocation, zero full candidate M/V allocations, successor headroom receipt, admitted full ResidentWeightPack successor, exact candidate SHA, sparse commit per optimizer generation, no RAM36 rejection, no HDD spill, and eight N8 optimizer generations completed.

Only physical execution may justify:

`PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_PHYSICAL_R1`

## Final invariant

One full canonical committed M/V state.

One compact AdamW-only transactional candidate overlay.

Muon-owned Adam state inherits committed bits exactly.

AdamW-owned candidate state alone consumes candidate B RAM.

Logical A/B remains complete and canonical.

Full logical candidate SHA remains unchanged.

No full candidate B allocation on sparse mode.

No committed mutation before permit.

No HDD spill.

No RAM36 inflation.

No route approximation.

ResidentWeightPack remains full and exact.

Physical PASS remains pending the local N8 campaign.
