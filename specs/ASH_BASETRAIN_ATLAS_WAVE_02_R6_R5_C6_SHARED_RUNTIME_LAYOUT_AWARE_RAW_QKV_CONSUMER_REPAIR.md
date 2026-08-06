# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C6

## Shared-Runtime Layout-Aware Raw QKV Consumer Repair / W5 BQHD Query·Raw-K Oracle Indexing / W7 BQHD Query·Raw-KV Oracle Indexing / W5→W6→W7 Layout Identity Propagation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C5`  
> Observed runtime failure: `W5CandidateOracleParityMismatch`  
> Observed mismatch: `504 / 1024 records`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. Failure position

The physical run passed the R6 actual-checkpoint Stage10/11/12 path, W4 BQHD shape admission and W4 BQHD direct K/V texture pack. It then failed inside W5 candidate/oracle statistics parity.

## 1. Root cause

The R6-R5 actual-checkpoint handoff is BQHD:

```text
Q = [B,Q,Hq,D]
K = [B,Q,Hkv,D]
V = [B,Q,Hkv,D]
```

C4 correctly packed BQHD K/V into Texture06 using:

```text
((token * kv_heads + kv_head) * head_dim) + dimension
```

However, the canonical W5 shared-runtime shaders still interpreted raw Q and raw K as BHQD.

```text
W5 candidate K texture = correct BQHD source
W5 oracle raw K        = incorrectly interpreted as BHQD
W5 candidate raw Q     = incorrectly interpreted as BHQD
W5 oracle raw Q        = incorrectly interpreted as BHQD
```

The candidate and oracle shared the same incorrect Q interpretation, but disagreed on K because only the texture side had already become BQHD-aware.

## 2. W5 repair

`TensorCubeStage10TextureKParams` now carries `input_layout_code` with padding to an 80-byte uniform contract.

```text
0 = BHQD
1 = BQHD
```

Q indexing:

```text
BHQD: ((query_head * q_seq + query_token) * head_dim) + dimension
BQHD: ((query_token * query_heads + query_head) * head_dim) + dimension
```

Oracle raw-K indexing:

```text
BHQD: ((kv_head * source_seq_len + global_token) * head_dim) + dimension
BQHD: ((global_token * kv_heads + kv_head) * head_dim) + dimension
```

The candidate continues reading K directly from Texture06.

## 3. W7 preventive closure

The same defect existed in W7:

```text
candidate raw Q assumed BHQD
oracle raw Q assumed BHQD
oracle raw K/V assumed BHQD
```

`TensorCubeStage12ChunkParams` now carries the same layout code with a 96-byte uniform contract.

W7 Q indexing:

```text
BHQD: ((query_head * q_seq + query_token) * head_dim) + dimension
BQHD: ((query_token * query_heads + query_head) * head_dim) + dimension
```

W7 oracle raw K/V indexing:

```text
BHQD: ((kv_head * source_seq_len + token) * head_dim) + dimension
BQHD: ((token * kv_heads + kv_head) * head_dim) + dimension
```

Candidate K/V texture reads remain unchanged.

## 4. Layout identity propagation

```text
W5 invocation identity.input_layout
  → W6 invocation identity.input_layout
  → W7 invocation identity.input_layout
```

W5 and W7 reject a layout change within one invocation. One invocation digest can no longer silently represent both BHQD and BQHD payload interpretations.

## 5. ABI revisions

```text
ash.attn.interconnect.w5.tensorcube-stage10-texture-k-live-shadow.v2-layout-aware-qk
ash.attn.interconnect.w7.tensorcube-stage12-weighted-value.v2-layout-aware-qkv
```

Build revisions:

```text
W5-live-q-buffer-k-texture-stage10-shadow-r2-layout-aware-qk
W6-R1C-wgsl-reserved-identifier-admission-layout-identity-propagation
W7-w6-global-state-frozen-kv-replay-stage12-shadow-r2-layout-aware-qkv
```

## 6. Preserved boundaries

```text
actual checkpoint QKV projection count = 1
QKV replacement buffer count = 0
QKV transpose buffer count = 0
QKV CPU payload readback count = 0
QKV host restaging count = 0
Texture06 direct K/V use preserved
W5/W6/W7 candidate authority preserved
R6 shadow oracle authority preserved
Headwise writer authority preserved
residual commit count = 0
MLP dispatch count = 0
next-layer publish count = 0
production/training promotion count = 0
```

## 7. Changed source files

```text
crates/burn_webgpu_backend/src/tensorcube_stage10_texture_k_live_shadow.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_texture_k_candidate.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_texture_k_oracle.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_texture_k_verify.wgsl
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_stage12_texture_kv_candidate.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_stage12_raw_kv_oracle.wgsl
crates/model_core/src/attention_interconnect_w5.rs
crates/model_core/src/attention_interconnect_w6.rs
crates/model_core/src/attention_interconnect_w7.rs
```

## 8. Static validation

```text
primary checks = 51
Rust/WGSL delimiter balance = PASS
Stage10 Rust/WGSL uniform agreement = PASS
Stage12 Rust/WGSL uniform agreement = PASS
BQHD Q full-coordinate parity, seq32/Hq32/D64 = PASS, 65536 scalars
BQHD K/V full-coordinate parity, seq32/Hkv4/D64 = PASS, 8192 scalars per tensor
BHQD Q regression coordinate parity = PASS
BHQD K/V regression coordinate parity = PASS
W5 identity layout seal = PASS
W6 identity layout propagation = PASS
W7 identity layout propagation = PASS
new QKV transpose buffer = 0
new host QKV readback = 0
```

Rust type-check, WGSL module creation and physical GPU parity remain user-side gates.

## 9. Cargo commands

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

## 10. Admission expectation

C6 is expected to remove the observed W5 `504/1024` divergence caused by raw-K layout interpretation. PASS is not claimed until the user-side run reaches the terminal R6-R5 seal with zero W5/W6/W7, context and OProj mismatches while preserving Headwise writer authority.
