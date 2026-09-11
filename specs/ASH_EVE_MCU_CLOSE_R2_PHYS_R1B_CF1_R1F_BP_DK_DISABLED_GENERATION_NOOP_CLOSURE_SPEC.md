# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1F

## BP-DK R2A DISABLED-MODE PHYSICAL GENERATION OPEN NO-OP CLOSURE

### 1. Scope

R1F closes a control-flow contradiction in the BP-DK R2A production caller when the canonical BP-DK runtime mode is `Disabled`.

The physical blocker entering this correction is:

```text
E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN
```

R1E had already physically admitted route-sparse Adam A/B, the RAM36 successor headroom gate, and successor `ResidentWeightPack` physical allocation before execution reached this BP-DK blocker.

### 2. Confirmed contradiction

The production helper `ensure_bp_delta_k_generation_phys_r2()` already branches on `mode.observes()`.

Before R1F its `false` branch:

1. retired R1/R2/R2A pending state,
2. forced scheduler cutover false,
3. then called `perf_r2a_phys.begin_generation(optimizer_step)`.

The low-level physical runtime correctly rejects generation open while its mode does not observe, producing `E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN`.

R1F fixes the caller. It does **not** weaken the low-level guard.

### 3. Disabled-mode authority

Canonical Disabled behavior is:

```text
Disabled
→ retire pending DK state
→ scheduler cutover false
→ mark outer disabled bypass witness
→ return mode
```

It does not open a BP-DK physical generation.

For `!mode.observes()`:

- `perf_r1a_pre_epoch = None`
- `perf_r1a_post_epoch = None`
- `perf_r2_gradient_catalog = None`
- prepared R2A observation/plan/batches = None
- physical prepared parameter state cleared
- physical post pending set = None
- `perf_r2a_phys_scheduler_cutover_active = false`
- `perf_r2a_phys.mark_disabled_outer_bypass_cutover()`
- return immediately

### 4. Low-level guard preservation

`BpDeltaKR2APhysicalClosureRuntime::begin_generation()` remains unchanged and retains:

```rust
ensure!(self.mode.observes(), "E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN");
```

This is intentional. Any future caller that attempts a physical generation in Disabled mode must continue to fail closed.

### 5. No fake physical qualification

The existing `disabled_outer_bypass_cutover` witness is used to prove that the outer caller took the Disabled bypass path.

R1F does not convert this witness into a fake physical generation PASS.

The existing physical-closure receipt requires other real physical cutovers in addition to the disabled-bypass witness before `physical_pass_claimed` can become true. Disabled mode therefore does not fabricate a DK physical generation qualification.

### 6. Observe / Active preservation

The observing path remains unchanged.

When `mode.observes() == true`, the existing caller still executes:

```rust
self.bpdk.perf_r1a1_sync.begin_generation(optimizer_step)?;
self.bpdk.perf_r2a_phys.begin_generation(optimizer_step)?;
```

No Disabled→ObserveOnly or Disabled→Active auto-promotion is introduced.

### 7. Training-pipeline preservation

The early `return Ok(mode)` occurs only inside the DK helper. The caller `prepare_delta_k_generation_phys_r2()` already interprets non-observing mode as a DK no-op and returns from the DK preparation helper without aborting the surrounding optimizer/training transaction.

Therefore:

```text
skip DK != skip optimizer step
```

### 8. Preserved prior closures

R1F does not modify:

- R1E route-sparse Adam activation or RAM36 headroom implementation/configuration
- R1D micro-batch=1 / one-lane execution contract
- R1C output-authority ordering
- dataset/R1A source identity
- WGPU bootstrap
- R6A executor
- numerical capture topology
- DK math, proposal, Hebbian, router reinjection, or policy selection

### 9. Re-materialization contract

- Dataset regeneration: **NOT REQUIRED**
- R1A regeneration: **NOT REQUIRED**
- R1A cursor regeneration: **NOT REQUIRED**
- `base_train` release rebuild: **REQUIRED**
- Native CF1 reseal: **REQUIRED**
- new R1B campaign root: **REQUIRED**
- A/B/C reentry: **REQUIRED**

### 10. Static bake evidence

Changed file:

`crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`

Baked SHA-256:

`90a6ffb49f15e763b85437051f059c44b7422b193237bc60f3f6717ed7e82bcd`

Key locations in the baked source:

- `ensure_bp_delta_k_generation_phys_r2`: line 5234
- Disabled scheduler cutover forced false: line 5254
- Disabled outer-bypass witness mark: line 5255
- Disabled immediate return: line 5256
- observing-path physical `begin_generation`: line 5304

The Disabled branch contains no `begin_generation()` call after R1F.

### 11. Preserved-source evidence

Low-level physical runtime remained byte-identical to the R1E input:

`crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs`

SHA-256:

`2b56af36c95a2654dc50d7eb4c0ade743bd78714f31d5946097d7f589e2d2c3a`

The error token `E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN` remains present.

R1E R1B-CF1 route-sparse configuration remained byte-identical:

`c7eb82195a04c6a8ca62f4043ed60d065a6dc0e9647b31a6fada8ad5e34e6156`

R1C production scheduler remained byte-identical:

`38cb9f897aada6b6b70de65530ed1abfad19550178b3ef782525e72772b922fe`

Full-archive comparison against R1E changed exactly one file.

### 12. Archive identity

Overlay ZIP SHA-256:

`3ceb76061764096212b0b486f8e882a1798f5f6708873af25d9a6161e629fe37`

Full code-only ZIP SHA-256:

`5a4316acaf6772e8f61fcc83127a3f2c53540de5b281198876d66dacad447c53`

Archive inventory:

- overlay file entries: 1
- full code-only file entries: 8423
- full archive entries including directories: 8543
- overlay ZIP CRC: PASS
- full ZIP CRC: PASS

### 13. Forbidden fixes

R1F does not:

- auto-promote Disabled to ObserveOnly or Active
- remove or relax the low-level Disabled generation-open guard
- synthesize a generation identity
- synthesize DK observation/proposal state
- set scheduler cutover true in Disabled mode
- create a fake DK physical PASS receipt
- alter DK policy selection
- disable R1E sparse Adam
- increase RAM36
- add disk spill
- roll back R1D one-lane or R1C output authority

### 14. Verification status

- R1E physical RAM36/headroom closure before this blocker: **CONFIRMED BY USER PHYSICAL LOG**
- Disabled caller contradiction: **CONFIRMED SOURCE-ATTRIBUTED**
- R1F static correction: **CONFIRMED**
- low-level guard preservation: **CONFIRMED**
- full archive one-file delta: **CONFIRMED**
- ZIP integrity: **CONFIRMED**
- release compile: **NOT VERIFIED IN BAKE ENVIRONMENT** (`cargo` unavailable)
- Native CF1: **NOT YET VERIFIED**
- Disabled-mode physical bypass continuation: **NOT YET VERIFIED**
- full A/B/C promotion: **NOT YET VERIFIED**

No compile or physical PASS is claimed by this specification.

### 15. Physical acceptance gate

The first R1F physical success condition is that `E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN` no longer occurs while BP-DK remains Disabled.

Expected semantics in that run:

```text
BP-DK mode = Disabled
observes = false
physical DK generation open = 0
scheduler cutover = false
disabled outer bypass witness = true
```

The optimizer production pipeline must then continue to the next real authority. Any subsequent first failure is a new attribution boundary.

### 16. Closure statement

R1F establishes one control-flow law:

```text
Disabled means no BP-DK generation exists to open.
```

The caller performs a clear-only bypass and preserves the low-level fail-closed guard for any future invalid generation-open attempt.
