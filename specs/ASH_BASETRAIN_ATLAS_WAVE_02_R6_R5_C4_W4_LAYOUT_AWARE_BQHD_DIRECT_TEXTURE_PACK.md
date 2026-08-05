# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C4

## W4 Layout-Aware BQHD Direct Texture Pack / Strided K-V Source Binding / No QKV Reprojection or Transpose Buffer Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C3`  
> Failure surface: `W4KShapeMismatch`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Root cause

The actual checkpoint R5-R7 live QKV handoff is BQHD:

```text
Q = [B,Q,Hq,D]  = [1,32,32,64]
K = [B,Q,Hkv,D] = [1,32,4,64]
V = [B,Q,Hkv,D] = [1,32,4,64]
PreparedAtlasInputs.input_layout = Bqhd
```

The W4 live sidecar admission and frozen replay admission were hard-coded to BHQD:

```text
Q expected = [B,Hq,Q,D]
K expected = [B,Hkv,Q,D]
V expected = [B,Hkv,Q,D]
```

The failure therefore occurred before W5/W6/W7 dispatch. It was not a K value mismatch and not a checkpoint geometry failure.

## 1. Why shape relabel is forbidden

The original W4 chunk slicer derives one contiguous range per KV head. That is valid for BHQD because each head owns a contiguous `[Q,D]` plane.

For BQHD, one head across tokens is strided by `Hkv * D`. Relabeling `[B,Q,Hkv,D]` as `[B,Hkv,Q,D]` would cause the texture upload to read the wrong K/V scalars.

C4 therefore does not relabel, transpose on host, duplicate QKV projection or create a replacement QKV buffer.

## 2. Layout-aware admission

W4 first-pass and frozen-replay shape checks now branch on `PreparedAtlasInputs.input_layout`:

```text
Bhqd:
  Q [1,Hq,Q,D]
  K/V [1,Hkv,Q,D]

Bqhd:
  Q [1,Q,Hq,D]
  K/V [1,Q,Hkv,D]
```

Both passes use the same shape helper and the same upload-mode dispatcher.

## 3. BQHD direct texture pack

The existing Texture06 upload shader gains a source mode:

```text
mode 0 = contiguous per-head slice, existing BHQD route
mode 1 = full BQHD source binding, direct strided indexing
```

For BQHD, the source scalar index is:

```text
source_token = token_start + local_token
scalar_index = ((source_token * kv_head_count + kv_head) * head_dim) + dim
```

The destination remains:

```text
rgba32float texture coordinate = (dim / 4, local_token, kv_head)
```

No intermediate transpose buffer is allocated.

## 4. Strided logical leases

Each BQHD KV head receives a logical strided lease receipt while binding the original full K or V buffer window.

```text
backing buffer = original actual-checkpoint QKV buffer
access = read only
head views may overlap the same backing window
read/read overlap = admitted
K/V backing buffers = distinct
source buffer duplication = 0
source staging copy = 0
```

The receipt records token range, head index, logical shape and full binding window. It does not claim that a BQHD head slice is physically contiguous.

## 5. Preserved authority boundaries

```text
actual QKV projection count = 1
QKV replacement buffer count = 0
QKV transpose buffer count = 0
QKV host read/upload = 0
W5/W6/W7 remain candidate
R6 remains shadow oracle
Headwise remains authoritative writer
residual commit = 0
MLP dispatch = 0
next-layer publish = 0
production/training promotion = 0
```

## 6. Changed files

```text
crates/burn_webgpu_backend/src/headwise_texture_06_chunk_upload.rs
crates/burn_webgpu_backend/src/shaders/headwise_texture_06_chunk_upload.wgsl
crates/model_core/src/headwise_texture_06_chunk_runtime.rs
crates/model_core/src/headwise_texture_06_live_binding.rs
```

## 7. Static validation

```text
Rust delimiter balance = PASS
WGSL delimiter balance = PASS
BQHD full-index parity for seq32, Hkv4, D64, two chunks = PASS
first-pass layout branch present = PASS
frozen-replay layout branch present = PASS
BHQD contiguous upload mode retained = PASS
BQHD direct full-buffer upload mode present = PASS
host transpose/copy path added = 0
.sha256 sidecar files = 0
```

Rust type-check, WGSL module creation and physical GPU parity remain user-side gates.

## 8. Cargo commands

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
