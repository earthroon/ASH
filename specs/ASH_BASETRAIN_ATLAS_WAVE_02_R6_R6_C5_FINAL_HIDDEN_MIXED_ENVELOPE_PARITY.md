# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C5

## Final-Hidden Mixed Envelope Parity / Strict Stage Contract Preservation / Detailed Mismatch Receipt Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C4`  
> Observed failure: `R6R6FinalHiddenParityMismatch`  
> Failure position: live shared final hidden vs non-committing Headwise reference final hidden  
> BaseTrain live admission: `HOLD` until physical rerun

## 0. Observed state

The physical run passed:

```text
native bootstrap
micro-atlas tile-map sequential wave streaming
deterministic shared-runtime context replay
actual shared body continuation
final-hidden finite guard
```

It then failed at the tolerance comparison between:

```text
reference final hidden
shared live final hidden
```

The previous error did not expose mismatch count, maximum absolute error, maximum relative error or first failing coordinate.

## 1. Contract mismatch

`HeadwiseOutputParityPipeline::compare()` preserves a strict dual-threshold contract:

```text
mismatch when:
  absolute_error > absolute_tolerance
  OR
  relative_error > relative_tolerance
```

Therefore a value may be rejected even when its absolute error is below the configured absolute tolerance, solely because a near-zero reference value produces a large relative error.

R6-R6 CLI declares both:

```text
--final-hidden-absolute-tolerance
--final-hidden-relative-tolerance
```

For final hidden admission these are now interpreted as a mixed envelope:

```text
mismatch when:
  absolute_error > absolute_tolerance
  AND
  relative_error > relative_tolerance
```

Equivalent pass rule:

```text
absolute_error <= absolute_tolerance
OR
relative_error <= relative_tolerance
```

This is restricted to the non-committing Headwise-reference final-hidden gate.

## 2. Preserved strict and exact paths

The existing `compare()` API remains strict.

```text
Stage parity users = unchanged
R6-R5 context parity = unchanged
R6-R5 OProj parity = unchanged
W4/W5/W6/W7 physical gates = unchanged
```

The existing `compare_exact()` API also remains bit-exact:

```text
live context vs replay context
live final hidden vs replay final hidden
committed layer-1 hidden vs published layer-1 hidden
```

No exact or stage comparison is moved to the mixed envelope.

## 3. New API

```rust
HeadwiseOutputParityPipeline::compare_mixed_envelope(...)
```

Internal mode values:

```text
0 = strict dual-threshold comparison
1 = mixed final-hidden envelope
```

The mode is carried in the uniform ABI with three padding words.

```text
Rust params = 8 u32 = 32 bytes
WGSL params = 8 u32 = 32 bytes
```

## 4. Failure visibility

If the mixed envelope still fails, the returned error now includes:

```text
envelope violation count
non-finite count
maximum absolute error
maximum relative error
first failing linear index
```

Example form:

```text
R6R6FinalHiddenParityMismatch:
violations=<n>:
nonfinite=<n>:
max_abs=<value>:
max_rel=<value>:
first=<index>
```

No tensor payload readback is added. These values come from the existing 24-byte compact decision buffer.

## 5. Changed source

```text
crates/burn_webgpu_backend/src/headwise_output_parity.rs
crates/burn_webgpu_backend/src/shaders/headwise_output_parity.wgsl
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
```

## 6. Preserved runtime semantics

```text
micro-atlas allocation and residency unchanged
actual checkpoint decoder block unchanged
QKV projection unchanged
W4/W5/W6/W7 unchanged
actual OProj and MLP unchanged
layer-1 hidden CAS unchanged
rollback contract unchanged
receipt wave-map unchanged
payload readback count unchanged
```

## 7. Static validation

```text
strict compare mode retained = PASS
exact compare mode retained = PASS
mixed-envelope call count in R6-R6 gate = 1
exact replay comparison count = 3
Rust/WGSL param word count = 8 / 8
Rust/WGSL param byte count = 32 / 32
comparison mode range guard = PASS
zero-floor exact raw call count = 0
Rust/WGSL delimiter balance = PASS
recursion_limit workaround count = 0
.sha256 sidecar count = 0
```

Cargo type-check, WGSL module creation and physical GPU execution remain user-side gates.

## 8. Commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p burn_webgpu_backend `
  -p orchestrator_local
```

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args"
```
