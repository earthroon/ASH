# EVE-MCU-R3H-CF11

## PAGED COPY-ON-WRITE CANDIDATE WEIGHT SUCCESSOR
## + DURABLE PACKED PAGE SPOOL
## + FULL-CANDIDATE HOST ALLOCATION RETIREMENT

**Revision:** `EVE-MCU-R3H-CF11`  
**Parent:** `EVE-MCU-R7A-CF9-CF4 + EVE-MCU-R3H-CF10 + CF3A lineage`  
**Parent full code-only SHA-256:** `4254f5a46f360e9e1d898050a6353c1cab3059bf41baa92a0934b66eeb561347`  
**Class:** host weight residency cutover / paged COW candidate / packed durable spool / post-source-retirement promotion

---

## 1. Physical motivation

Observed host allocation authority before CF11:

```text
committed resident weight      4,666,580,992 bytes
candidate weight builder       4,666,580,992 bytes
candidate Adam M                 791,044,096 bytes
candidate Adam V                 791,044,096 bytes
---------------------------------------------------
known large host authorities  10,915,250,176 bytes
```

The removable single largest allocation is the second full candidate weight pack.

CF11 removes the step-time `ResidentWeightPackBuilder::Full(Vec<u8>)` candidate allocation from the direct ActiveVerified/R3C1 path.

---

## 2. Production activation scope

CF11 production cutover is intentionally narrow:

```text
defer_resident_weight_successor_r3h
AND
CF3A direct-host Adam path
AND
resident_weight_source.is_some()
```

This corresponds to the current ActiveVerified + CF3A + R3C1 physical campaign path.

Legacy / qualification paths that do not satisfy this gate preserve the existing full `ResidentWeightPackBuilder` behavior.

CF11 therefore does **not** claim that every historical ASH weight-successor path is paged.

---

## 3. New candidate authority

`ResidentWeightPackBuilder` now has two storage backends:

```text
Full(Vec<u8>)                 legacy/reference
PagedCowCf11(...)             CF11 production direct path
```

CF11 candidate state is:

```text
immutable committed source Arc<Vec<u8>>
+
bounded dirty-page cache
+
packed durable dirty-page spool
+
initialized-range / coverage metadata
```

A logically complete candidate generation no longer implies a second complete candidate heap object.

---

## 4. Frozen CF11 page geometry

```text
CF11_PAGE_BYTES              = 67,108,864 bytes  (64 MiB)
CF11_MAX_DIRTY_RAM_PAGES     = 4
CF11_MAX_DIRTY_RAM_BYTES     = 268,435,456 bytes (256 MiB)
```

The dirty cache is a hard software bound. New dirty-page admission evicts an eligible page when the cache is full.

The streaming final merge additionally uses bounded scratch:

```text
page merge buffer            <= 64 MiB
BufWriter buffer             = 16 MiB
```

No scratch allocation is generation-sized.

---

## 5. Copy-on-write semantics

For a candidate range:

```text
Dirty RAM page    -> candidate page bytes
Dirty spooled page-> packed spool bytes
Inherited page    -> committed source bytes
```

Partial first write:

```text
source page
-> one candidate page clone
-> overwrite target subrange
```

Full-page overwrite:

```text
allocate dirty page
-> write incoming page
-> no source-page clone
```

Random-order writes remain supported for CF3A Adam W and CF4 Muon W.

---

## 6. Packed dirty-page spool

The temporary spool is:

```text
<weights.r6pack>.cf11.pages
```

It is **packed**, not indexed by `page_ordinal * page_size`.

Authority:

```text
page ordinal -> packed spool file offset
```

This prevents a high logical page ordinal from implicitly expanding the temporary spool to model-pack size on Windows/NTFS.

Tracked separately:

```text
spool_payload_bytes  = unique packed dirty payload physically represented
spool_write_bytes    = total writes including rewrites
```

The temporary spool is synced before final merge and removed after successful candidate seal.

---

## 7. Candidate file seal

At candidate terminal, CF11 streams canonical page order into the target `weights.r6pack`:

```text
for page ordinal 0..N:
    dirty -> packed candidate spool page
    clean -> committed source page
    write to target weights.r6pack
    update canonical SHA-256
```

This creates the canonical candidate file without assembling a full candidate `Vec`.

Admission requires:

```text
canonical bytes == expected weight_pack_bytes
canonical SHA-256 == expected manifest SHA-256
full_candidate_heap_allocation_count == 0
```

---

## 8. Important implementation boundary: post-retirement full resident source

CF11 does **not** permanently eliminate the next-step full resident source pack.

The current ASH next-step ABI still expects one full `ResidentWeightPack` source.

Therefore the production lifetime becomes:

```text
STEP EXECUTION
committed source W      ~4.66 GB
CF11 dirty cache        <=256 MiB
candidate file/spool    disk-backed

R3H REPLACEMENT
old source last-use closes
-> old resident source Arc drops
-> old RAM36 reservation releases
-> headroom is rechecked
-> only then target weights.r6pack is loaded as new full ResidentWeightPack
```

This is the central CF11 guarantee:

> source full W and candidate full W are not simultaneously resident as two full heap packs.

The post-retirement load emits:

```text
[ASH-R3H-HOST-ALLOC-TRACE][cf11-promote-after-source-retire]
```

A 4.66 GB target resident allocation after source retirement is therefore **expected** and is not counted as a full candidate heap allocation.

---

## 9. No duplicate promotion SHA pass

The canonical candidate SHA-256 is computed during the just-completed streaming candidate-file seal.

Post-source-retirement promotion:

- verifies file byte length;
- binds the sealed candidate digest;
- loads the canonical bytes into the new `ResidentWeightPack`;
- does not recompute another full CPU SHA pass.

This avoids paying a second full-file hash immediately after the candidate file was sealed and synced.

---

## 10. R3H authority integration

New replacement authority:

```text
CF11_PAGED_COW_DURABLE_MERGE_AFTER_SOURCE_RETIREMENT
```

CF11 replacement receipt declares:

```text
resident_weight_successor_d2h_bytes = 0
resident_weight_successor_d2h_submission_count = 0
full_temporary_copy_count = 0
digest_exact = true
```

The candidate came from canonical host/durable COW merge, not target-device D2H.

---

## 11. CF3A / CF4 preservation

CF3A Adam candidate W direct writes continue through the existing random-write builder API.

CF4 Muon candidate W direct writes use the same builder authority.

For CF11, both land in the same paged-COW logical candidate generation.

No optimizer-specific second full W generation is introduced.

---

## 12. Disk-write boundary

CF11 trades host-RAM high-water for bounded RAM plus disk traffic.

If most model pages become dirty, the packed dirty spool can approach one full weight generation and the final canonical merge writes another full `weights.r6pack`.

Therefore:

```text
HOST MEMORY REDUCTION  = SOURCE/STATIC supported
120 s/step SPEEDUP     = UNKNOWN until physical measurement
```

Metrics retained in the seal:

```text
dirty_page_count
inherited_page_count
peak_dirty_ram_pages
peak_dirty_ram_bytes
spooled_page_count
spool_payload_bytes
spool_write_bytes
page_reload_count
dirty_page_reopen_count
dirty_page_rewrite_count
```

Page reload/rewrite growth is a page-thrash signal and blocks performance promotion.

---

## 13. Terminal receipt

CF11 emits:

```text
[ASH-EVE-MCU-R3H-CF11][paged-candidate-weight-successor]
```

Critical fields:

```text
page_size_bytes=67108864
peak_dirty_ram_pages<=4
peak_dirty_ram_bytes<=268435456
full_candidate_heap_allocation_count=0
admitted=true
```

---

## 14. Physical ordering gate

The following runtime order is mandatory:

```text
[ASH-EVE-MCU-R3H][source-host-retired]

BEFORE

[ASH-R3H-HOST-ALLOC-TRACE][cf11-promote-after-source-retire]
```

Any reversed ordering means the original double-residency problem remains.

---

## 15. Old allocation marker gate

On the CF11 direct physical path, the following old step-time candidate allocation must be absent:

```text
[ASH-R3H-HOST-ALLOC-TRACE][resident-weight-builder]
generation=1
expected_bytes=4666580992
allocation_kind=Vec::with_capacity
```

Legacy/reference paths may still contain the code and marker.

---

## 16. Rust unit-test authority

Real test prefix added:

```text
r3h_cf11_
```

Current tests:

```text
r3h_cf11_inherited_page_reads_source_exact
r3h_cf11_partial_write_materializes_one_page
r3h_cf11_peak_dirty_pages_bounded_and_spooled
r3h_cf11_random_order_writes_preserve_exact_candidate
```

The tests use a small internal page geometry but the production constructor freezes 64 MiB × 4.

---

## 17. Static validation

New validator:

```text
tools/validate_ash_eve_mcu_r3h_cf11_paged_cow_candidate_weight_successor_static.py
```

Current bake result:

```text
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=54
```

Preserved static results:

```text
PASS_EVE_MCU_R7A_CF9_CF4_MUON_WAVE_BOUNDED_DEVICE_SUCCESSOR_STATIC checks=47
PASS_EVE_MCU_R3H_CF10_GPU_RESIDENT_EVIDENCE_REDUCTION_STATIC
PASS_ASH_EVE_HIMUON_FULL_TRAINABLE_GENERATION_COMMIT_PERMIT_JOIN_AND_ATOMIC_ADAM_MUON_WEIGHT_PROMOTION_CLOSURE_R3C_STATIC
PASS_ASH_BASETRAIN_RAM36_SUCCESSOR_WEIGHT_RESERVATION_PHYSICAL_ALLOCATION_OWNERSHIP_TRANSITION_CLOSURE_R1_STATIC
PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_CANDIDATE_OVERLAY_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_CLOSURE_R1_STATIC
```

Inherited parent drift:

```text
R3C1 static = 25/30 PASS
```

The same five R3C1 checks fail on the untouched CF4 parent, so this is not classified as a CF11 regression.

---

## 18. Modified files

```text
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
MOD crates/base_train/src/ram_weight_pack_persistent_residency.rs
MOD crates/base_train/src/resident_weight_replacement_authority_r3h.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
ADD tools/validate_ash_eve_mcu_r3h_cf11_paged_cow_candidate_weight_successor_static.py
```

Source SHA-256:

```text
94e739c83b4fc25f599f8be5d7ae4255feb282215e22b316a159bfc7f69a1f6c  ram_weight_pack_persistent_residency.rs
def162b05fa130a7b76c52630b3220e112ac1f634da68b81814b2573040846a0  production_multistep_loop_accumulation8_scheduler.rs
a58359472ef8f6d962b3471414a5c648fa8a3f290ebfed8f03854be31b2dacec  resident_weight_replacement_authority_r3h.rs
225a281c550f3a0e1505755626f0aff8201b47d7d0a7220296c6c54cbdd496b8  tensorcube_local_muon_production_callsite_adoption.rs
246c7b3c0e98a4b85b6eae2bbdbe9de2d49d9a4de7017b689050582ff41e5f62  validate_ash_eve_mcu_r3h_cf11_paged_cow_candidate_weight_successor_static.py
```

---

## 19. Code-only artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_OVERLAY_CODE_ONLY.zip
SHA-256 3497cd6374624e467a8e43751a9263983485fda8d9d215a47daa27e51f386b46
FILES 5
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_CODE_ONLY.zip
SHA-256 020e8e30d0ee9158eab26ceb2567f7563a7017fecc57bd36ab8a51c63564eb68
FILES 8433
CRC PASS
```

Both archives exclude:

```text
specs/
artifacts/
manifests/
.git/
Markdown
__pycache__/
*.pyc
```

The full archive retains `Cargo.toml` and `Cargo.lock`.

---

## 20. Evidence status at bake

```text
SOURCE               APPLIED
STATIC               PASS
ARCHIVE CRC           PASS
RUST COMPILE          NOT RUN IN BAKE ENVIRONMENT
WGSL                  NO NEW WGSL
RUNTIME               NOT RUN
PHYSICAL              NOT RUN
PERFORMANCE           UNMEASURED
```

No Rust toolchain is installed in the bake environment, therefore no compile/runtime claim is made.

### Compilefix-1: successor builder reborrow

First user compile exposed:

```text
error[E0382]: borrow of moved value: successor_weight_builder
```

The streaming call consumed `Option<&mut ResidentWeightPackBuilder>` by value and the later CF4 direct demotion attempted to borrow the same option again.

Compilefix-1 changes only the streaming callsite:

```text
successor_weight_builder
-> successor_weight_builder.as_deref_mut()
```

This is a short mutable reborrow; ownership of the outer `Option<&mut ...>` remains available for the later direct demotion.

Static validation now rejects both:

```text
missing reborrow
legacy bare move into streaming call
```

Compilefix-1 status:

```text
SOURCE    APPLIED
STATIC    PASS 54/54
COMPILE   USER RE-RUN REQUIRED
```

---

## 21. Promotion law

CF11 is physically admitted only if the real campaign proves all of:

```text
full candidate generation-1 resident-weight-builder allocation count = 0

CF11 terminal seal present
full_candidate_heap_allocation_count=0
page_size_bytes=67108864
peak_dirty_ram_pages<=4
peak_dirty_ram_bytes<=268435456
admitted=true

source-host-retired line occurs before cf11-promote-after-source-retire

post-retirement target ResidentWeightPack materializes successfully

no memory allocation failure
no OutOfMemory
no DeviceLost
no WGPU Validation Error
```

Performance promotion additionally requires measured step wall time and spool/reload metrics.

---

## 22. Final law

> CF11 removes the second complete step-time candidate weight heap, not the canonical next-step resident source.

> During the step, candidate W is source inheritance plus at most four 64 MiB dirty RAM pages and a packed durable dirty-page spool.

> Canonical candidate `weights.r6pack` is produced by bounded page-order streaming merge.

> The old full source pack is physically dropped and its RAM36 reservation released before the new full resident source pack is allocated.

> No late operation may reconstruct a second full candidate pack while the old source is still resident.

> Memory admission is established before any performance claim; the additional disk I/O must be measured against the `base_train <= ~120 s/step` project target.
