# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1E

## RAM36 HIMUON ROUTE-SPARSE TRANSACTIONAL ADAM A/B ACTIVATION + RESIDENT WEIGHT SUCCESSOR HEADROOM CLOSURE

### Scope

R1E activates the already-implemented HiMuon route-sparse transactional Adam A/B path in the R1B-CF1 FreshGenesis production configuration. It does not introduce a new optimizer implementation.

The physical blocker entering R1E is the RAM36 successor reservation rejection where current private bytes remain under 36 GiB but a full successor `ResidentWeightPack` would project the process above the hard cap.

### Production law

- RAM36 hard limit remains `38,654,705,664` bytes (36 GiB).
- No HDD/mmap/pagefile spill is admitted.
- No full candidate M/V fallback is admitted when route-sparse production is requested.
- R1C output authority ordering remains unchanged.
- R1D micro-batch=1 / R6A-R1 one-lane ABI remains unchanged.
- Dataset and R1A source identity remain unchanged.

### R1B-CF1 activation

`crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs`

- patch identity becomes `ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1E`
- sets `admit_ram36_himuon_route_sparse_transactional_adam_ab = true`
- reconstructs `RamAdamRouteSparseOverlayPlanR1` from the generated canonical Muon registry and the admitted R1A candidate-parameter-set digest
- fails closed unless route counts are exactly `154 Muon / 47 explicit AdamW / 0 mixed`
- fails closed unless Muon+AdamW element coverage equals the canonical trainable element cardinality
- fails closed unless the sparse candidate is physically smaller than the full candidate
- publishes route digest, plan digest, parameter/element counts, full/compact moment bytes, saved bytes, hard limit, and explicit no-fallback/no-spill policy in preflight and R1B receipts
- marks packed-canonical bridge and order-independent overlay coverage as required and explicitly deferred to the existing physical production path

### Existing production implementation reused unchanged

The following existing modules are not modified by R1E:

- `production_multistep_loop_accumulation8_scheduler.rs`
- `ram_resident_adam_mv.rs`
- `ram36_himuon_route_sparse_transactional_adam_ab_r1.rs`
- `ram36_himuon_sparse_adam_packed_canonical_bridge_r1a.rs`
- `ram36_himuon_sparse_adam_order_independent_overlay_coverage_r1b.rs`

The scheduler already:

1. skips full candidate M/V reservations/allocation when route-sparse admission is enabled,
2. builds the exact route plan after the production Muon runtime is materialized,
3. builds and binds the packed-canonical bridge,
4. builds the order-independent overlay coverage ledger,
5. materializes compact AdamW-only M/V overlays,
6. writes the route-sparse transactional receipt,
7. computes and publishes the successor-weight headroom receipt before reserving the successor `ResidentWeightPack`.

### Route authority

Expected physical route geometry from the admitted model/registry:

- Muon parameters: `154`
- explicit AdamW parameters: `47`
- mixed parameters: `0`
- Muon elements: runtime exact authority
- AdamW elements: runtime exact authority
- `Muon elements + AdamW elements == canonical trainable elements`

No route membership may be missing, duplicated, or mixed.

### Candidate memory geometry

The route plan itself remains authority for exact byte counts.

For the currently observed model geometry:

- full candidate M/V logical domain: 1,166,645,248 elements × 2 × 4 bytes
- compact candidate M/V physical domain: AdamW-owned elements only × 2 × 4 bytes
- `physical_bytes_avoided > 0` is required

Static arithmetic is not promoted to a physical RAM36 PASS. Actual successor admission remains dependent on runtime private-byte observation.

### Physical headroom gate

The existing runtime headroom receipt remains the physical authority:

`ram36_himuon_route_sparse_adam_ab_headroom_r1.json`

A successful physical closure requires:

- sparse overlay active,
- full candidate allocation counts remain zero,
- HDD spill bytes remain zero,
- successor `ResidentWeightPack` reservation admitted,
- projected bytes are `<= 38,654,705,664`,
- no hidden full-candidate reservation.

### Forbidden fixes

- RAM36 cap increase
- disk or mmap spill
- full candidate M/V fallback
- hidden full-size candidate reservation
- mixed-route compatibility fallback
- R6A executor modification
- micro-batch or accumulation geometry changes
- dataset/R1A regeneration as a workaround
- R1C ordering rollback
- R1D one-lane rollback

### Re-materialization

- Dataset regeneration: **NOT REQUIRED**
- R1A regeneration: **NOT REQUIRED**
- `base_train` rebuild: **REQUIRED**
- Native CF1 reseal: **REQUIRED**
- new R1B campaign root: **REQUIRED**
- A/B/C reentry: **REQUIRED**

### Static bake evidence

Changed source:

`crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs`

SHA-256:

`c7eb82195a04c6a8ca62f4043ed60d065a6dc0e9647b31a6fada8ad5e34e6156`

Key evidence locations in the baked file:

- R1E patch identity: line 31
- expected route counts: lines 42-44
- route-sparse production admission enabled: line 350
- exact route plan build/checks: lines 399-423
- preflight route-sparse evidence: lines 466-485
- final R1B receipt route-sparse evidence: lines 577 onward

Preserved critical source SHA-256:

- R1C scheduler: `38cb9f897aada6b6b70de65530ed1abfad19550178b3ef782525e72772b922fe`
- RAM resident Adam implementation: `b0a641ef28c26ecfd6d65d1f0552b32c2e45eeada899272c06ea1d6bd817135d`
- route-sparse plan/headroom implementation: `dda9b35b25a9b857249a3104fbd1ceccd5a359e67254e79c08d1d16f2f10b46b`
- packed-canonical bridge: `faef41f67e601073fec77022e9d2c19d50a05b9f95da90b51b477910115602f7`
- order-independent overlay coverage: `15a6e8c1913d3146c79bd2f39d2af517719e3d78d7c461229989509bc45e838c`

Archive identity:

- Overlay ZIP SHA-256: `dadc3e65a301c154d8e0bea7ed6fcb5b0f7d45addf82de8da8046a1e86935574`
- Full code-only ZIP SHA-256: `3d7ca6efb1668cc10e6c2104657253a35f368a403b8f4ffdb8f5d8a35360027d`
- Overlay file count: `1`
- Full code-only file count: `8423`
- ZIP CRC: PASS for both archives

### Verification status

- physical RAM36 blocker attribution: **CONFIRMED by supplied runtime log**
- existing route-sparse implementation availability: **CONFIRMED STATIC**
- R1E activation/configuration delta: **CONFIRMED STATIC**
- archive integrity: **CONFIRMED**
- release compile: **NOT VERIFIED IN BAKE ENVIRONMENT** (`cargo` unavailable)
- Native CF1: **NOT YET VERIFIED**
- successor reservation under RAM36: **NOT YET VERIFIED**
- full A/B/C promotion: **NOT YET VERIFIED**

No compile or physical PASS is claimed by this specification.
