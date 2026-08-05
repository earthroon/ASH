# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C1

## Raw Bridge Device/Queue Import Repair

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

`BackendDevice` and `BackendQueue` are owned by `burn_webgpu_backend::raw_bridge`. R6-R5 comparison consumers must import the aliases from that module directly rather than assuming crate-root re-exports.

## 1. Compile failure

```text
error[E0432]: unresolved imports crate::BackendDevice, crate::BackendQueue
```

Affected files:

```text
crates/burn_webgpu_backend/src/attention_context_layout_compare.rs
crates/burn_webgpu_backend/src/body_oproj_output_compare.rs
```

Canonical alias ownership:

```rust
pub type BackendDevice = RuntimeWgpuDevice;
pub type BackendQueue = RuntimeWgpuQueue;
```

is defined in:

```text
crates/burn_webgpu_backend/src/raw_bridge.rs
```

## 2. Repair

Both consumers now use:

```rust
use crate::raw_bridge::{BackendDevice, BackendQueue};
```

No crate-root re-export is introduced.

## 3. Reasoning

Adding a new crate-root re-export merely to hide a local import error would widen the public API and blur the existing raw-bridge ownership boundary. The consumers instead reference the SSOT owner directly.

## 4. Semantic boundary

This patch changes imports only. It does not change:

```text
context layout or strides
context parity arithmetic
OProj parity arithmetic
same-device adoption
payload-readback prohibition
Headwise writer authority
residual/MLP/next-layer HOLD boundaries
production or training promotion state
```

## 5. Static validation

```text
canonical raw_bridge aliases present = PASS
crate-root alias imports in repaired files = 0
other imported R6-R5 comparison symbols remain valid crate-root re-exports
Rust delimiter scan = PASS
ZIP integrity = PASS
```

Rust type-check and physical GPU execution remain user-side gates.

## 6. Commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r5.args"
```
