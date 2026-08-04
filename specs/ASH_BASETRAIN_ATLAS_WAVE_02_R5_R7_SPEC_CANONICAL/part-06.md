base_train_atlas_wave_02_r5_r7_selected_layer_forward.rs
shaders/base_train_atlas_wave_02_r5_r7_rope_neox_half_split.wgsl
```

Required public APIs:

```rust
pub fn load_base_train_atlas_wave_02_r5_r7_resident_tensor_leases(...)
    -> Result<BaseTrainAtlasWave02R5R7ResidentTensorLeaseSet>;

pub fn run_base_train_atlas_wave_02_r5_r7_selected_layer_forward(...)
    -> Result<BaseTrainAtlasWave02R5R7GpuExecution>;
```

The selected forward may internally reuse the existing embedding, RMSNorm, QKV and attention-oracle shaders after their ABI and lineage checks pass.

It must not use the legacy adjacent R5 RoPE shader.

## orchestrator_local crate

```text
src/bin/ash_basetrain_atlas_wave_02_r5_r7_selected_layer_real_forward_gate.rs
```

Cargo feature:

```text
orchestrator_tcu_audit_bins
```

---

# 28. Gate execution algorithm

The physical gate executes in this exact authority order.

```text
1. Expand response-file arguments.
2. Import and hash R5-R6 local manifest.
3. Import R5-R6 checkpoint tensor-set authority receipt.
4. Verify R5-R6 pass token and checkpointSetDigest continuity.
5. Import and hash R5-R5 local manifest.
6. Verify NeoXHalfSplit and rope theta continuity.
7. Parse selected-layer and fixture authorities.
8. Resolve exactly five selected tensor authorities from R5-R6 inventory.
9. Reverify shard CAS and exact tensor ranges.
10. Plan bounded source pages for all five selected tensors.
11. Decode each wave with parallel exact-range workers.
12. Upload pages into one aligned same-device f32 atlas allocation.
13. Read back and digest every completed wave.
14. Publish five non-overlapping resident leases.
15. Freeze checkpoint reads and weight writes for forward phase.
16. Build CPU-f64 reference from the same raw ranges.
17. Run actual embedding stage.
18. Run actual RMSNorm stage.
19. Run actual Q/K/V stage.
20. Run full-shape NeoX RoPE stage.
21. Run compact GQA attention oracle stage.
22. Read back complete bounded activation surface.
23. Compare every selected-surface element.
24. Verify exact padding zeros and all zero authority counters.
25. Execute negative counterfactual ledger.
26. Write receipts and selected-layer authority.
27. Write local manifest.
28. Print PASS token only after all writes and digest checks succeed.
```

---

# 29. Static admission checks

The source tree must satisfy at least:

```text
R5-R7 patch ID exported
R5-R7 pass token exported
new authority module exported from base_train
new atlas parallel streaming-wave residency module exported from base_train
new selected-forward module exported from burn_webgpu_backend
new NeoX full-shape WGSL included
legacy adjacent WGSL not referenced by R5-R7
no Headwise import in R5-R7 gate
no TensorCube import in R5-R7 gate
no OProj or MLP dispatch symbol in R5-R7 gate
no checkpoint directory scan
no suffix tensor resolution
no hidden layer fallback
no hardcoded 32000 vocabulary
no hardcoded 2048 hidden size in authority builder
no hardcoded 10000 rope theta in WGSL
no production admission true literal
```

---

# 30. Runtime counters

Required successful values:

```text
selected_tensor_count                       5
executed_layer_count                        1
resident_lease_count                        5
mixed_generation_count                      0
stale_lease_count                           0
checkpoint_reopen_during_forward_count      0
weight_write_during_forward_count           0
host_full_tensor_materialization_count      0
headwise_dispatch_count                     0
tensorcube_dispatch_count                   0
o_projection_dispatch_count                 0
mlp_dispatch_count                          0
next_layer_dispatch_count                   0
full_model_dispatch_count                   0
loss_dispatch_count                         0
backward_dispatch_count                     0
optimizer_step_count                        0
```

Expected positive values:

```text
source_payload_read_bytes                   > 0
decoded_runtime_bytes                       > source_payload_read_bytes for BF16/F16
weight_buffer_create_count                  1 sealed non-overlapping atlas allocation
atlas_page_count                            > 0
atlas_wave_count                            > 0
parallel_decode_wave_count                  = atlas_wave_count
bounded_wave_readback_count                 = atlas_wave_count
lm_head_upload_count                        0
weight_queue_write_count                    > 0 during residency phase
forward_dispatch_count                      5
queue_submit_count                          >= 1
activation_readback_bytes                   > 0
```

---

# 31. PASS criteria

R5-R7 passes only when all of the following are true.

```text
R5-R6 checkpoint-set authority imported exactly
R5-R5 NeoX RoPE authority imported exactly
selected layer valid and explicit
exact five physical tensors selected
all selected tensor identity digests match
all shard and byte-range checks pass
source dtype is BF16 or F16
all decodes finite and complete
host full tensor materialization count zero
same-device resident lease set sealed
no mixed runtime or generation lineage
actual embedding consumed
actual RMSNorm consumed
actual Q/K/V consumed
full-shape NeoX RoPE consumed
compact 32Q:4KV GQA consumed
full bounded selected-surface parity passes
masked lanes are exact zero
negative counterfactual ledger passes
Headwise dispatch count zero
TensorCube dispatch count zero
full-model dispatch count zero
production admission blocked
proof ledger hold
R6 admission blocked
full-model admission blocked
```

---

# 32. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R7_SELECTED_LAYER_REAL_CHECKPOINT_FORWARD_ACTUAL_EMBEDDING_RMSNORM_QKV_TENSOR_ADOPTION_BF16_F16_DECODE_AUTHORITY_PRODUCTION_CANDIDATE_GQA_CONSUMPTION_EXTERNAL_ROPE_CONVENTION_LIVE_CONSUMPTION_GPU_CPU_F64_SELECTED_SURFACE_PARITY_RESIDENT_TENSOR_LEASE_PROVENANCE_NO_HEADWISE_OUTPUT_AUTHORITY_NO_FULL_MODEL_ADMISSION_PRODUCTION_BLOCKED_PROOF_LEDGER_HOLD_R6_BLOCKED_SEALED
```

The token must not be printed when any stage is skipped, mocked, inferred from static source, or replaced by a synthetic tensor.

---

# 33. Post-pass state

After physical PASS, the project state becomes:

```text
R5-R3  Model Geometry Authority                 PHYSICAL PASS
R5-R4  GQA Physical Geometry                    PHYSICAL PASS
R5-R5  External RoPE Convention                 PHYSICAL PASS
R5-R6  Production Checkpoint Tensor Set         PHYSICAL PASS
R5-R7  Selected-Layer Real Checkpoint Forward   PHYSICAL PASS
```

The newly proven boundary is:

```text
real production-candidate checkpoint bytes
  -> selected real layer tensors
  -> decoded resident weights
  -> actual embedding/RMSNorm/QKV
  -> external NeoX RoPE
  -> compact GQA attention context
  -> CPU-f64 selected-surface parity
```

The following remain unproven:

```text
Headwise live output authority
TensorCube live output authority
O projection
residual path
MLP
complete transformer block
all 22 layers
final logits
loss
backward
optimizer
production training
```

---

# 34. Downstream dependency

The next patch may be:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6

Headwise Training Adapter Live Adoption /
Production-Candidate Selected-Layer Input /
Same-Device Resident Lease Consumption /
Oracle-vs-Headwise Context Parity /
Headwise Selected-Layer Output Authority /
TensorCube Handoff Authority Preservation /
No Loss·Backward·Optimizer Seal
```

R6 must consume the R5-R7 lease and selected-forward authorities directly.

R6 must not reopen the checkpoint, rebuild the selected tensors, replace the R5-R7 decode authority, or derive a parallel geometry SSOT.

---

# 35. Final seal

R5-R7 seals one narrow but critical fact:

```text
The selected-layer attention context was produced from the exact real 48,259-vocabulary production-candidate checkpoint tensors, under the externally correct NeoX RoPE convention and the physically correct 32Q:4KV GQA mapping, on one same-device resident lineage, and matched a CPU-f64 reference across the complete bounded selected surface.
```

It does not seal anything beyond that sentence.
