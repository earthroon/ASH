# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C1

## RMSNorm Epsilon f64 Bit-Restore Compile Closure

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6`  
> Failure: Rust `E0308` at R6-R6 decoder-block authority construction  
> Scope: configuration bit restoration only  
> BaseTrain live admission: `HOLD` until physical rerun

## 0. Observed failure

```text
error[E0308]: mismatched types
expected u32, found u64

norm_eps: f32::from_bits(authority.config.rms_norm_eps_bits) as f64
```

## 1. SSOT type contract

The production config authority reads `rms_norm_eps` as `f64` and seals it with:

```rust
rms_norm_eps_bits: rms_norm_eps.to_bits()
```

Therefore:

```text
source semantic type = f64
sealed bits type = u64
canonical restoration = f64::from_bits(u64)
```

This matches the existing `rope_theta_bits: u64` restoration convention.

## 2. Repair

Before:

```rust
norm_eps: f32::from_bits(authority.config.rms_norm_eps_bits) as f64,
```

After:

```rust
norm_eps: f64::from_bits(authority.config.rms_norm_eps_bits),
```

## 3. Rejected alternatives

The compiler suggestion to convert `u64` to `u32` is not adopted.

```text
try_into::<u32>() = rejects valid f64 bit patterns
as u32              = truncates the high 32 bits
f32::from_bits       = changes the sealed numeric ABI
```

No lossy cast, default epsilon, clamp or fallback is introduced.

## 4. Changed source

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
```

## 5. Preserved semantics

```text
checkpoint config parsing unchanged
checkpoint authority digest unchanged
RMSNorm epsilon numeric value preserved exactly
actual decoder-block construction unchanged
QKV/OProj/MLP wiring unchanged
BaseTrain writer authority unchanged
layer-1 tensor commit unchanged
rollback contract unchanged
```

## 6. Static validation

```text
rms_norm_eps source parser = required_f64
rms_norm_eps seal = f64::to_bits -> u64
R6-R6 restore = f64::from_bits(u64)
remaining f32::from_bits(rms_norm_eps_bits) count = 0
Rust delimiter balance = PASS
ZIP integrity = PASS
```

Rust type-check and physical GPU execution remain user-side gates.

## 7. Commands

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
