# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3

## Stage11 Online-Softmax Multi-Chunk Statistics Merge

> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3`  
> Direct parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R2-R1`  
> Parent state required: C4 physical PASS  
> Selected-layer writer: R6 Headwise preserved  
> Stage12/context/output authority: blocked  
> Production admission: blocked  
> Proof ledger: HOLD

## 0. SSOT

R6-R3 consumes only the live R6-R2-R1 retained Stage10 statistics, folds them once in canonical chunk-major and q-tile-minor order into frozen 16-byte global max/exp-sum/admitted-count records, proves candidate/oracle and causal invariants on GPU, preserves Q/K/V plus the R6 Headwise writer, and authorizes no Stage12 or context output.

## 1. Authorized execution route

```text
R6 live Q/K/V and Headwise authority
  -> same-process R6-R2-R1 execution exactly once
  -> retained Stage10 candidate/oracle statistics buffers
  -> canonical Stage11 source plan
  -> candidate global online-softmax fold
  -> independent raw-oracle global fold
  -> compact parity verification
  -> independent source/merge/causal invariant verification
  -> frozen Stage11 global-state live handoff
```

A prior process cannot transfer live `wgpu::Buffer`, `wgpu::Device`, or `wgpu::Queue` handles. Therefore the R6-R3 gate imports the prior R6-R2-R1 manifest as lineage evidence, then executes R6-R2-R1 exactly once inside the same process to obtain the live retained statistics handoff.

After the handoff is published, Stage10 candidate/oracle dispatch counts must remain zero.

## 2. Forbidden substitutions

The following are prohibited:

- reading Stage10 statistics payloads to CPU
- serializing Stage10 statistics into JSON
- reconstructing Stage10 GPU buffers from JSON or sidecars
- rerunning Stage10 after live handoff publication
- recomputing QK scores during Stage11
- creating a full attention score matrix
- creating a full softmax probability matrix
- reading Q, K, or V during Stage11
- executing Stage12 weighted-V accumulation
- creating TensorCube context output
- replacing the R6 Headwise selected-layer writer
- OProj, residual, RMSNorm, MLP, next-layer, full-model, backward, optimizer, checkpoint write, or production promotion

## 3. State ownership

```text
R6-R2-R1 Stage10 retained statistics buffers
  owner: R6-R2-R1 live handoff until Stage11 queue completion

R6-R3 source plan and dispatch order
  owner: base_train R6-R3 source-plan authority

R6-R3 candidate/oracle pipelines and global-state buffers
  owner: burn_webgpu_backend R6-R3 runtime

R6-R3 frozen global-state lifetime
  owner: non-serializable R6-R3 live handoff

Receipts and manifests
  owner: identity, counters, digests, and policy only
```

No JSON object owns a GPU handle. No logical digest may be treated as a live handle.

## 4. Parent record ABI

Each Stage10 partial statistics record is exactly 16 bytes:

| word | meaning | encoding |
|---:|---|---|
| 0 | partial max | `f32` bits in `u32` |
| 1 | partial exp sum | `f32` bits in `u32` |
| 2 | admitted key count | `u32` |
| 3 | Stage10 flags | `u32` |

Valid parent records require `VALID` and `FINAL_WRITE`, finite max and exp sum, positive admitted count, and `1 <= exp_sum <= admitted_count`.

A fully masked record must encode negative infinity max, zero exp sum, zero admitted count, and final-write only.

## 5. Canonical source plan

The retained source vector must already be ordered:

```text
for chunk_ordinal in 0 .. canonical_chunk_count:
    for q_tile_index in 0 .. q_tile_count:
        one source entry
```

Canonical source ordinal:

```text
source_ordinal = chunk_ordinal * q_tile_count + q_tile_index
```

The planner validates order and descriptors. It must not silently sort, repair, or infer missing entries.

Expected source entry count:

```text
canonical_chunk_count * q_tile_count
```

Expected global record count for the current batch-one profile:

```text
seq_q * 32
```

## 6. Stage11 global-state ABI

ABI:

```text
ash.basetrain.atlas-wave.02.r6-r3.stage11-global-softmax-state.v1
```

Each output record is exactly 16 bytes:

| word | meaning | encoding |
|---:|---|---|
| 0 | global max | `f32` bits in `u32` |
| 1 | global exp sum normalized to global max | `f32` bits in `u32` |
| 2 | global admitted key count | `u32` |
| 3 | Stage11 flags | `u32` |

Record layout:

```text
record_id = query_token * 32 + query_head
```

Required final flags:

```text
VALID | ALL_CHUNKS_CONSUMED | CANONICAL_ORDER | FINAL_WRITE
```

No error flag may be set in a PASS record.

## 7. Candidate merge law

For current state `A = (m_a, s_a, n_a)` and valid partial `B = (m_b, s_b, n_b)`:

```text
m = max(m_a, m_b)
s = s_a * exp(m_a - m) + s_b * exp(m_b - m)
n = n_a + n_b
```

The first valid partial initializes the global state. Fully masked partials contribute no value and no admitted count.

Candidate dispatch is source-entry ordered and writes one state update per global record for every canonical chunk.

## 8. Independent oracle

The oracle does not reuse candidate merge results.

For each source entry it:

1. scans valid Stage10 block records for a chunk-local max
2. rescales each block exp sum to the chunk-local max
3. forms a chunk-local exp sum and admitted count
4. merges the chunk state into the oracle global state

Candidate and oracle state buffers, pipelines, write-count buffers, and bind groups remain distinct.

## 9. GPU verification

Compact global parity checks:

- exact global max bits
- exp-sum ULP distance not exceeding configured threshold
- exact admitted count
- exact final flags
- candidate write count equals canonical chunk count
- oracle write count equals canonical chunk count
- all expected global records compared

Independent invariant checks:

- source order mismatch count is zero
- descriptor mismatch count is zero
- source coverage mismatch count is zero
- parent record encoding errors are zero
- global max does not decrease
- exp sum is finite and bounded
- admitted count matches causal availability
- post-handoff Stage10 rerun count is zero
- statistics payload readback count is zero
- Q/K/V read counts are zero
- Stage12/context/output/writer/route mutation counts are zero

Only 128 bytes of compact status may be read back. Production statistics and global-state payload readback are prohibited.

## 10. Implemented code surface

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r3_stage11_authority.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r3_source_plan.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r3_frozen_global_state_handoff.rs
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r3_stage11_merge.rs
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_candidate_merge.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_oracle_merge.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_global_verify.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_invariant_verify.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r3_stage11_known_vector_fixture.wgsl
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r3_stage11_online_softmax_merge_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r3.args
```

The R6-R3 gate is registered under the existing `orchestrator_tcu_audit_bins` feature. The native bootstrap large-buffer authority includes the R6-R3 gate source name.

## 11. PASS conditions

All conditions must hold:

- imported R6-R2-R1 manifest valid
- same-process parent identity equals imported lineage
- parent Stage10 execution count equals one
- post-handoff Stage10 rerun count equals zero
- exact canonical source plan
- candidate and oracle dispatch counts equal source entry count
- exact partial record coverage
- candidate/oracle max, exp sum, count, and flags parity
- merge, range, and causal invariants pass
- source lifetime violation count equals zero
- statistics and global-state payload readback counts equal zero
- compact readback bytes equal 128
- Q/K/V read counts equal zero
- Headwise writer and route mutation counts equal zero
- Stage12 dispatch count equals zero
- TensorCube context creation and output commit counts equal zero
- known-vector fixture passes
- all fault injections are denied

## 12. Canonical PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R3_TENSORCUBE_STAGE11_LIVE_ONLINE_SOFTMAX_MULTI_CHUNK_STATISTICS_MERGE_R6_R2_R1_RETAINED_STATISTICS_SAME_PROCESS_CONSUMPTION_CANONICAL_CHUNK_QTILE_ORDER_DETERMINISTIC_GLOBAL_MAX_EXP_SUM_ADMITTED_COUNT_FOLD_CANDIDATE_RAW_ORACLE_GLOBAL_STATE_PARITY_INDEPENDENT_MERGE_CAUSAL_RANGE_INVARIANTS_FROZEN_GLOBAL_SOFTMAX_STATE_HANDOFF_ACTUAL_Q_K_V_AND_KV_TEXTURE_PRESERVATION_HEADWISE_WRITER_PRESERVATION_NO_STAGE10_RERUN_JSON_RECONSTRUCTION_PAYLOAD_READBACK_STAGE12_CONTEXT_OUTPUT_COMMIT_OPROJ_MLP_FULL_MODEL_PRODUCTION_PROMOTION_PROOF_LEDGER_HOLD_SEALED
```

The token may be printed only after physical GPU execution and fault-injection evidence pass.

## 13. Validation status

Static validation is complete for file presence, TOML parsing, delimiter balance, module exports, bin registration, args pair structure, required source tokens, large-buffer registration, and Stage11 shader prohibition checks.

Rust compile closure, project-version Naga validation, and target-GPU physical PASS remain judgment deferred until the supplied Cargo commands run in the ASH Windows workspace.

## 14. Commands

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

## 15. Next dependent patch

Only after R6-R3 physical PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4
Stage12 Live Weighted-V Accumulation
```

R6-R4 may consume the frozen global state, Q, K/V texture lineage, and actual V lease. It may not reconstruct R6-R3 state from JSON or rerun Stage11 after the frozen handoff is published.
