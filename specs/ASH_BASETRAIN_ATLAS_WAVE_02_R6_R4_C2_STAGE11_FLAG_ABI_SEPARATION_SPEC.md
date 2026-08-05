# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4-C2

## Stage11 Input Flag ABI and Stage12 Row Flag Separation

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4-C1`  
> Required parent state: R6-R3-C4 physical PASS  
> Build revision: `stage12-atlas-parallel-streaming-weighted-v-bhqd-stage11-flag-abi-v3`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

R6-R4 Stage12 consumes R6-R3 Stage11 records using the exact Stage11 flag ABI. Bit `0x00000002` in a Stage11 global-state record means `ALL_CHUNKS_CONSUMED`; it does not mean `ALL_MASKED`. Stage12 row-classification records are a separate ABI where bit `0x00000002` may mean `ALL_MASKED`.

## 1. Physical failure evidence

The C1 physical receipt reported:

```text
candidate input-contract failures = 2048
oracle input-contract failures = 2048
candidate-oracle mismatch = 0
candidate-Headwise mismatch = 65458
denominator violations = 65536
missing writes = 65536
row mismatches = 1024
valid rows = 0
masked rows = 0
```

With 1024 global records and 2 chunks, `2048` contract failures on both routes proves that every chunk-row pair rejected the frozen Stage11 state before weighted-V accumulation. Both routes then produced the same zero context, explaining candidate-oracle parity alongside Headwise failure.

## 2. Stage11 input flags

```text
STAGE11_FLAG_VALID               = 0x00000001
STAGE11_FLAG_ALL_CHUNKS_CONSUMED = 0x00000002
STAGE11_FLAG_CANONICAL_ORDER     = 0x00000004
STAGE11_FLAG_FINAL_WRITE         = 0x00000008
STAGE11_FLAG_ERROR_MASK          = 0xf0000000
```

A valid Stage11 record requires:

```text
VALID set
ALL_CHUNKS_CONSUMED set
CANONICAL_ORDER set
FINAL_WRITE set
error mask clear
finite global max
finite positive denominator
admitted count > 0
```

A fully masked Stage11 record requires:

```text
VALID clear
ALL_CHUNKS_CONSUMED set
CANONICAL_ORDER set
FINAL_WRITE set
error mask clear
max = -infinity
denominator = 0
admitted count = 0
```

## 3. Stage12 row-classification flags

The normalize pass creates a new Stage12-owned row record. Only this output ABI uses:

```text
ROW_FLAG_VALID       = 0x00000001
ROW_FLAG_ALL_MASKED  = 0x00000002
ROW_FLAG_FINAL_WRITE = 0x00000008
ROW_FLAG_CAUSAL      = 0x00000010
```

Stage11 input flags and Stage12 row flags must never be interpreted through one shared semantic enum merely because some bit values overlap.

## 4. Patched surfaces

```text
base_train_atlas_wave_02_r6_r4_stage12_texture_weighted_v.wgsl
base_train_atlas_wave_02_r6_r4_stage12_raw_qkv_oracle.wgsl
base_train_atlas_wave_02_r6_r4_stage12_context_normalize.wgsl
base_train_atlas_wave_02_r6_r4_stage12_weighted_v.rs
base_train_atlas_wave_02_r6_r4_stage12_authority.rs
```

## 5. Static admission

The Rust loader requires the candidate, oracle and normalize shaders to contain the Stage11 `ALL_CHUNKS_CONSUMED`, `CANONICAL_ORDER` and error-mask contract. Candidate and oracle shaders are rejected if they define `FLAG_ALL_MASKED` for Stage11 input.

## 6. Preserved contracts

```text
candidate/oracle deterministic score replay preserved
candidate K/V texture route preserved
oracle raw K/V route preserved
BHQD output preserved
256-byte compact readback preserved
context payload readback = 0
Headwise writer mutation = 0
TensorCube context commit = 0
OProj/MLP/next-layer dispatch = 0
production promotion = 0
```

## 7. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r4_stage12_weighted_v_context_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r4.args"
```
