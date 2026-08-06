# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C3

## Micro-Atlas Tile Map / Sequential Wave Streaming / Mega-Atlas Retirement / Token-Row Sparse Embedding Residency Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C2`  
> Observed failure: `AW02R5R7AtlasExceedsDeviceMaxBufferSize:416317440:268435456`  
> Route: BaseTrain FullPrefill layer 0  
> Production inference admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Failure

The R6-R6 gate still called the R5-R7 legacy uploader, which decoded and concatenated these tensors into one GPU buffer:

```text
embedding + input RMS + Q + K + V
```

Current-profile decoded sizes:

```text
embedding [48259,2048] = 395,337,728 bytes
input RMS              =       8,192 bytes
Q [2048,2048]          =  16,777,216 bytes
K [256,2048]           =   2,097,152 bytes
V [256,2048]           =   2,097,152 bytes
aligned total          = 416,317,440 bytes
device max_buffer_size = 268,435,456 bytes
```

The active failure was therefore a real mega-atlas allocation, not a false device-limit report.

## 1. SSOT correction

R6-R6 does not need the five legacy tensors in one atlas.

The actual checkpoint-backed `AshDecoderBlock` already owns RMSNorm, Q, K, V, OProj and MLP weights. Re-uploading RMS/Q/K/V through the legacy atlas is duplicate residency.

The only pre-block atlas responsibility is token embedding lookup.

```text
full embedding tensor residency = forbidden
five-tensor mega atlas = forbidden
requested embedding rows only = admitted
one reusable micro-atlas slot = admitted
token-position tile map = admitted
concurrent waves = forbidden
```

The legacy R5-R7 uploader remains available to older routes, but the R6-R6 live gate no longer calls it.

## 2. Micro-atlas tile model

One tile is one requested embedding row:

```text
global token ID
  -> exact checkpoint row [hidden_size]
  -> decode F16/BF16/F32 to F32
  -> wave-local micro-atlas row
```

For hidden size 2048:

```text
decoded row bytes = 2048 * 4 = 8,192 bytes
```

Repeated token IDs create one tile and multiple position-map entries. Padding positions are excluded and remain zero because the output hidden buffer is GPU-cleared before wave dispatch.

## 3. Default wave profile

```text
rows per wave = 4
parallel decode workers = 4
fixture unique token rows = 32
wave count = 8
micro-atlas capacity = 4 * 8,192 = 32,768 bytes
```

Each wave executes:

```text
1. read up to four exact checkpoint rows in parallel
2. decode rows independently to F32
3. sort rows by global token ID
4. write rows into the reusable micro-atlas slot
5. build token-position -> wave-local-row tile maps
6. queue-write atlas, two maps and 16-byte params
7. dispatch embedding scatter WGSL
8. wait for GPU completion
9. perform bounded gate verification
10. reuse the same slot for the next wave
```

Required sequentiality:

```text
concurrent_wave_count = 1
wave_overlap_count = 0
fence_wait_count = wave_count
micro_atlas_buffer_reuse_count = wave_count - 1
```

## 4. GPU scatter contract

Shader:

```text
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r6_micro_embedding.wgsl
```

Bindings:

```text
0 micro_embedding_rows : storage read array<f32>
1 token_positions      : storage read array<u32>
2 local_rows           : storage read array<u32>
3 params               : uniform, four u32, 16 bytes
4 embedding_hidden     : storage read_write array<f32>
```

Indexing:

```text
entry_index = invocation / hidden_size
hidden_lane = invocation % hidden_size
position = token_positions[entry_index]
local_row = local_rows[entry_index]

output[position, hidden_lane]
  = micro_atlas[local_row, hidden_lane]
```

The shader has no full-vocabulary binding.

## 5. Allocation receipts

The live gate must report:

```text
legacy_mega_atlas_request_bytes = 416,317,440 for current profile
mega_atlas_buffer_create_count = 0
full_embedding_upload_count = 0
micro_atlas_buffer_create_count = 1
micro_atlas_capacity_bytes = 32,768 for default fixture
micro_atlas_peak_resident_bytes <= micro_atlas_capacity_bytes
tile_map_buffer_create_count = 2
concurrent_wave_count = 1
wave_overlap_count = 0
```

The final hidden output, tile maps and uniform buffers remain individually far below the device limit.

## 6. Preserved live-body semantics

C3 does not change:

```text
actual AshDecoderBlock authority
single actual QKV projection
NeoX RoPE
W4 Texture06
W5 Stage10
W6 Stage11
W7 Stage12
same-device context adoption
actual OProj
attention residual
post-attention RMSNorm
SwiGLU MLP
FFN residual
layer-1 hidden CAS
Headwise rollback-only policy
no silent fallback
no backward or optimizer
```

Only pre-block embedding residency changes.

## 7. Changed source

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r6_micro_atlas_streaming.rs
crates/base_train/src/lib.rs
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r6_live_body.rs
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r6_micro_embedding.wgsl
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args
```

## 8. Static validation

```text
static checks = 39 PASS / 0 FAIL
changed files against C2 parent = 10 exact
active R6-R6 legacy mega-atlas call count = 0
active R6-R6 resident weight bundle call count = 0
micro-atlas allocation site count = 1
Rust/WGSL uniform field order = exact
Rust/WGSL uniform bytes = 16
Rust/WGSL bindings = 0..4 exact
fixture micro-atlas capacity = 32,768 bytes
fixture wave count = 8
symbolic unique-token coverage = PASS
symbolic repeated-token coverage = PASS
symbolic padding coverage = PASS
recursion-limit workaround count = 0
.sha256 sidecar count = 0
```

Cargo type-check, WGSL module creation and physical GPU execution remain user-side gates.

## 9. Commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p burn_webgpu_backend `
  -p base_train `
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
