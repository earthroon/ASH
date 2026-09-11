# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1G

## BP-DK R2A DISABLED-MODE COMMIT / ABORT FINALIZE NO-OP SYMMETRY CLOSURE

### Scope

R1G completes the Disabled-mode BP-DK R2A lifecycle symmetry established by R1F. R1F physically removed the invalid Disabled `begin_generation()` call, after which production advanced to `E_DK_R2A_PHYS_GENERATION_DRIFT` during finalize. The remaining defect is that commit/abort finalize still assumed a DK physical generation always existed.

### Authority law

For BP-DK mode `Disabled`:

```text
generation open = 0
prepared-plan freeze = 0
physical commit resolve = 0
physical abort resolve = 0
scheduler cutover = false
outer disabled bypass witness = true
```

`skip DK finalize != skip optimizer finalize`.

ObserveOnly / Active modes retain their existing physical generation lifecycle.

### Implementation

Changed file:

`crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`

R1G adds mode gates around the R2A physical finalize seams only.

Commit path, inside `record_generation_commit_internal_r3c1`:

- `perf_r2a_prepared_plan` freeze runs only when `self.bpdk.perf_r1_mode.observes()`.
- `perf_r2a_phys.record_prepared_plan_frozen(...)` runs only when observing.
- `perf_r2a_phys.resolve_generation(..., true)` runs only when observing.

Abort path, inside `record_generation_abort`:

- `perf_r2a_phys.resolve_generation(..., false)` runs only when observing.

The existing `perf_r1a1_sync.resolve_generation(...)` path remains unchanged because it already handles non-observing mode as a no-op.

### R1F preservation

The Disabled entry path remains:

```text
pending DK state retire
→ scheduler cutover false
→ mark_disabled_outer_bypass_cutover()
→ return
```

No Disabled `begin_generation()` call is reintroduced.

### Low-level guard preservation

`crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs` remains unchanged.

The following fail-closed guards remain present:

- `E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN`
- `E_DK_R2A_PHYS_GENERATION_DRIFT`

R1G fixes caller control flow. It does not weaken the physical runtime.

### No fake receipts or synthetic lifecycle

R1G does not:

- auto-promote Disabled to ObserveOnly or Active,
- synthesize a DK generation during finalize,
- synthesize a prepared plan,
- create a fake DK commit receipt,
- create a fake DK abort receipt,
- catch and ignore `GENERATION_DRIFT`,
- make low-level `resolve_generation()` silently succeed without a generation.

### Prior physical closures preserved

R1G does not modify the already-admitted R1E/R1D/R1C production paths:

- R1E HiMuon route-sparse Adam A/B remains active.
- 154 Muon / 47 AdamW / 0 mixed route semantics remain unchanged.
- RAM36 hard limit remains 36 GiB.
- no disk spill / no full candidate fallback remains unchanged.
- R1D micro-batch=1 and R6A-R1 one-lane geometry remain unchanged.
- R1C output-authority publication ordering remains unchanged.
- dataset and R1A source/cursor identities remain unchanged.

### Static evidence

Baked changed source SHA-256:

`1e7e2a08f48f9942ef76773d49db5e29a68fe78623c9a6bd3707c8ba772c835c`

Key lines in the baked source:

- R1F Disabled outer bypass witness: line 5255
- commit finalize observes gate: line 13715
- commit prepared-plan physical freeze binding: line 13730
- commit physical resolve: line 13739
- abort finalize observes gate: line 13885
- abort physical resolve: line 13886

Low-level guard file SHA-256, preserved:

`2b56af36c95a2654dc50d7eb4c0ade743bd78714f31d5946097d7f589e2d2c3a`

R1E R1B-CF1 source SHA-256, preserved:

`c7eb82195a04c6a8ca62f4043ed60d065a6dc0e9647b31a6fada8ad5e34e6156`

R1C scheduler SHA-256, preserved:

`38cb9f897aada6b6b70de65530ed1abfad19550178b3ef782525e72772b922fe`

### Archive identity

Overlay ZIP SHA-256:

`1fcb9adfd13aa937f3d66a0da8957b7416cb1602b318654de89e99b7c45c40f2`

Full code-only ZIP SHA-256:

`bc8b407560129fc2233949f3ec6e6f51c925f91a59209f9325e7f61a4f8294a0`

Archive inventory:

- overlay files: 1
- full code-only files: 8423
- overlay ZIP CRC: PASS
- full ZIP CRC: PASS

### Compile / physical status

Bake environment had no `cargo` or `rustfmt` executable available.

Therefore:

- static correction: **CONFIRMED**
- archive integrity: **CONFIRMED**
- release compile: **NOT VERIFIED IN BAKE ENVIRONMENT**
- Native CF1: **NOT YET VERIFIED**
- Disabled finalize physical closure: **NOT YET VERIFIED**
- full A/B/C promotion: **NOT YET VERIFIED**

No compile or physical PASS is claimed by this spec.

### Re-materialization contract

- dataset regeneration: **NOT REQUIRED**
- R1A regeneration: **NOT REQUIRED**
- R1A cursor regeneration: **NOT REQUIRED**
- `base_train` rebuild: **REQUIRED**
- Native CF1 reseal: **REQUIRED**
- fresh R1B campaign root: **REQUIRED**
- A/B/C reentry: **REQUIRED**

### Physical acceptance gate

R1G first succeeds physically when Disabled mode no longer produces:

```text
E_DK_R2A_PHYS_GENERATION_DRIFT
```

and the surrounding optimizer production transaction continues to the next real authority.

Disabled expected semantics:

```text
BP-DK observes = false
DK begin_generation count = 0
DK prepared-plan freeze attempt = 0
DK commit resolve attempt = 0
DK abort resolve attempt = 0
scheduler cutover = false
outer disabled bypass witness = true
```

Any subsequent first failure is a new attribution boundary.

### Closure statement

R1G completes the lifecycle symmetry:

```text
No open
→ no freeze
→ no commit resolve
→ no abort resolve
```

The low-level generation guards remain authoritative and fail closed for every invalid observing-mode lifecycle call.
