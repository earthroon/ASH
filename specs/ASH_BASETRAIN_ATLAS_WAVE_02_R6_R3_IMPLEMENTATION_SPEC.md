# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3

## Stage11 Atlas Parallel Streaming Wave Online-Softmax Merge

> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3`  
> Build revision: `stage11-atlas-parallel-streaming-wave-v2`  
> Amendment: C1  
> Direct parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R2-R1`  
> Parent state required: C4 physical PASS  
> Selected-layer writer: R6 Headwise preserved  
> Stage12/context/output authority: blocked  
> Production admission: blocked  
> Proof ledger: HOLD

## 0. SSOT

R6-R3 obtains the live R6-R2-R1 Stage10 retained candidate/oracle statistics in the same process, packs one canonical KV chunk at a time into a bounded reusable GPU atlas pair, performs q-tile-parallel candidate and independent oracle global online-softmax folds, verifies the frozen global state through compact GPU receipts, preserves Q/K/V and the R6 Headwise writer, and authorizes no Stage12 or context output.

This C1 amendment supersedes the previous direct-bind-per-source-entry Stage11 schedule.

## 1. Root-cause closure

The previous gate built the complete local manifest through one oversized `serde_json::json!` expression and reached Rust's macro recursion limit.

C1 does not raise `#![recursion_limit]`. It assembles the manifest from multiple small JSON objects into a `serde_json::Map<String, Value>` and rejects duplicate keys before sealing.

## 2. Authorized execution route

```text
R6 live Q/K/V and Headwise authority
  -> same-process R6-R2-R1 execution exactly once
  -> retained Stage10 candidate/oracle statistics buffers
  -> canonical Stage11 source plan
  -> bounded candidate/oracle statistics atlas allocation
  -> per-source GPU atlas pack
  -> one canonical streaming wave per KV chunk
  -> q-tile-parallel candidate global fold
  -> independent q-tile-parallel raw-oracle global fold
  -> atlas pair reuse for the next chunk
  -> compact parity and invariant verification
  -> frozen Stage11 global-state live handoff
```

A previous process cannot transfer live `wgpu::Buffer`, `wgpu::Device`, or `wgpu::Queue` handles. The prior R6-R2-R1 manifest is lineage evidence only. R6-R3 executes the parent chain exactly once in its own process and consumes that live handoff.

## 3. Statistics-atlas authority

The atlas is bounded to the largest single chunk wave, not the complete multi-chunk source set.

```text
candidate atlas capacity = max records required by one chunk wave
oracle atlas capacity    = max records required by one chunk wave
atlas lifetime           = one R6-R3 invocation
atlas reuse              = each chunk after the first
atlas payload readback   = 0
full-source materialize  = 0
```

Stage10 retained buffers do not need `COPY_SRC`. A compute pack shader reads each retained buffer as storage and writes its assigned atlas interval.

## 4. Canonical streaming-wave schedule

```text
for chunk_ordinal in ascending canonical order:
    select exactly q_tile_count source entries
    validate source/chunk/q_tile ordinals and live-buffer digests
    build the chunk wave descriptor table
    pack every candidate q_tile source into the candidate atlas
    pack every oracle q_tile source into the oracle atlas
    dispatch one candidate merge wave
    dispatch one oracle merge wave
    reuse the atlas pair for the next chunk
```

Chunk waves remain serial because they update the same global records. Query tiles within a chunk wave execute in parallel.

```text
pack workgroup_size = 64 x 1 x 1
pack dispatch/source = ceil(statistics_record_count / 64)
merge workgroup_size = 32 x 1 x 1
expected subgroup size = 32
merge dispatch/chunk = dispatch_workgroups(q_tile_count, 16, 1)
```

## 5. ABI and counters

```text
Stage11 ABI = ash.basetrain.atlas-wave.02.r6-r3.stage11-atlas-parallel-streaming-wave.v2
Statistics atlas ABI = ash.basetrain.atlas-wave.02.r6-r3.stage11-statistics-atlas.parallel-streaming-wave.v1
Kernel profile = tensorcube-stage11-sg32-atlas-parallel-streaming-wave-v1
Stage10 record bytes = 16
Stage11 global-state record bytes = 16
compact verifier readback bytes = 128

atlas_wave_count = canonical_chunk_count
atlas_pack_dispatch_count = source_entry_count * 2
atlas_merge_dispatch_count = canonical_chunk_count * 2
candidate_stage11_dispatch_count = canonical_chunk_count
oracle_stage11_dispatch_count = canonical_chunk_count
atlas_buffer_reuse_count = canonical_chunk_count - 1
atlas_payload_readback_count = 0
atlas_full_source_materialization_count = 0
statistics_payload_readback_count = 0
Q/K/V read count = 0
Stage12 dispatch count = 0
TensorCube context/output commit count = 0
```

## 6. Required implementation files

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r3_stage11_merge.rs
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_statistics_atlas_pack.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_candidate_merge.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_oracle_merge.wgsl
crates/base_train/src/base_train_atlas_wave_02_r6_r3_stage11_authority.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r3_stage11_online_softmax_merge_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r3.args
```

## 7. Forbidden substitutions

- CPU merge or payload readback of Stage10 statistics
- JSON reconstruction of statistics buffers
- `COPY_SRC` retrofit as a prerequisite
- full multi-chunk statistics atlas materialization
- Q/K score recomputation or V/texture reads during Stage11
- full score or probability matrices
- Stage10 rerun after live handoff publication
- Stage12 weighted-V execution
- TensorCube context or output commit
- Headwise writer replacement
- silent sequence, chunk, ULP, or subgroup fallback

## 8. Cargo commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r3_stage11_online_softmax_merge_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r3_stage11_online_softmax_merge_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r3.args"
```

Expected output directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r3/stage11-atlas-parallel-streaming-wave-v2
```

## 9. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R3_TENSORCUBE_STAGE11_ATLAS_PARALLEL_STREAMING_WAVE_ONLINE_SOFTMAX_MULTI_CHUNK_STATISTICS_MERGE_R6_R2_R1_RETAINED_STATISTICS_SAME_PROCESS_GPU_ATLAS_PACK_CANONICAL_CHUNK_WAVE_QTILE_PARALLEL_FOLD_BOUNDED_ATLAS_REUSE_DETERMINISTIC_GLOBAL_MAX_EXP_SUM_ADMITTED_COUNT_CANDIDATE_RAW_ORACLE_GLOBAL_STATE_PARITY_INDEPENDENT_CAUSAL_RANGE_INVARIANTS_FROZEN_GLOBAL_SOFTMAX_STATE_HANDOFF_ACTUAL_Q_K_V_AND_KV_TEXTURE_PRESERVATION_HEADWISE_WRITER_PRESERVATION_NO_STAGE10_RERUN_JSON_RECONSTRUCTION_PAYLOAD_READBACK_STAGE12_CONTEXT_OUTPUT_COMMIT_OPROJ_MLP_FULL_MODEL_PRODUCTION_PROMOTION_PROOF_LEDGER_HOLD_SEALED
```
