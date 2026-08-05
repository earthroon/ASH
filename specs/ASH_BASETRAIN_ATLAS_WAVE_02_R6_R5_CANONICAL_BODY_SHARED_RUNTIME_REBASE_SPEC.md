# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5

## Canonical Body Shared-Runtime Rebase / Actual Checkpoint QKV Consumer Splice / Stage11 Flag ABI Isolation / Layout-Tagged Pre-OProj Context / Existing Body OProj Adoption / Headwise Writer Preservation Seal

> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5`  
> Build revision: `canonical-body-shared-runtime-rebase-actual-oproj-shadow-v1`  
> Direct physical parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4-C2`  
> Body authority parent: `ASH-BASETRAIN-G202D-SHARED-ATTENTION-RUNTIME-01`  
> Full source specification: 1,902 lines  
> Full source specification SHA-256: `46f4dd0a30ce83a7e7c6e895a7ef07f587e61b7e80de595f4abb78a1d7c232e4`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

R6-R5 does not promote the physically passing R6 Stage10/11/12 chain into an independent production attention engine.

The canonical candidate remains the existing G202D W5/W6/W7 shared TensorCube runtime. R6-R2/R3/R4 remains an actual-checkpoint shadow oracle. Headwise remains the authoritative selected-layer and production attention-output writer.

The actual layer-0 checkpoint QKV projection is executed once. The resulting `PreparedAtlasInputs` is consumed by:

```text
1. canonical W5/W6/W7 shared-runtime candidate
2. R6 Stage10/11/12 shadow oracle
3. Headwise authoritative reference
```

The three pre-OProj contexts are sealed with explicit semantic shape, physical layout, physical strides, source generation, completion and buffer range. They are adopted into same-device Burn tensors, passed through one actual checkpoint-backed `AshLinear` OProj module instance, and compared pairwise on GPU.

R6-R5 does not commit residual state, post-attention norm, MLP state, next-layer hidden state, gradients, optimizer state or checkpoint mutation.

## 1. Authority

```text
canonical TensorCube candidate = W5/W6/W7 shared runtime
actual-checkpoint shadow oracle = R6-R2/R3/R4
selected-layer writer           = Headwise
production authority            = unchanged
training default writer         = unchanged
```

Forbidden authority changes:

```text
shared TensorCube writer adoption = 0
R6 writer adoption = 0
production authority compare-and-swap = 0
training route promotion = 0
```

## 2. Parent requirements

The gate requires both:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r4/stage12-weighted-v-context-v1/ash_basetrain_atlas_wave_02_r6_r4_local_manifest.json
workspace/runtime/basetrain/g202d/ash_basetrain_g202d_local_manifest.json
```

The R6-R4 parent must report:

```text
patch = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4
pass = true
production_admission = BLOCKED
proof_ledger = HOLD
```

The G202D manifest must match the G202D patch ID, build revision and PASS token owned by `model_core`.

Serialized manifests are lineage evidence only. They do not reconstruct live QKV, Stage11 state, context or OProj payloads.

## 3. Stage11 flag-domain isolation

Three flag domains are separate Rust newtypes.

### W6 Stage11

```text
0x00000001 = VALID
0x00000002 = ALL_MASKED
```

### R6 Stage11

```text
0x00000001 = VALID
0x00000002 = ALL_CHUNKS_CONSUMED
0x00000004 = CANONICAL_ORDER
0x00000008 = FINAL_WRITE
```

### Stage12 row classification

```text
0x00000001 = VALID
0x00000002 = ALL_MASKED
0x00000008 = FINAL_WRITE
0x00000010 = CAUSAL
```

Required:

```text
raw cross-domain cast count = 0
automatic From<u32> cross-domain conversion count = 0
shared semantic enum count = 0
```

A W6 Stage11 handle is consumed only by W7. An R6 Stage11 handle is consumed only by R6-R4 Stage12.

## 4. Layout-tagged context ABI

Semantic shape for all routes:

```text
[B,Q,H,D]
```

Physical layouts:

```text
Headwise = BHQD
W7       = BQHD
R6       = BHQD
```

Every context handle records:

```text
semantic shape
physical layout enum
physical shape
contiguous physical strides
buffer offset
buffer byte length
element type and element count
source engine
source generation
completion token
source identity digest
```

Forbidden:

```text
BHQD buffer relabeled as BQHD
BQHD buffer relabeled as BHQD
hidden transpose without receipt
q_seq=1 layout coincidence used as prefill proof
```

## 5. Actual checkpoint QKV consumer splice

The fixture is restricted to actual checkpoint layer 0.

```text
layer index = 0
batch size = 1
sequence length = 32
query heads = 32
KV heads = 4
head dimension = 64
hidden size = 2048
```

The body input is normalized once and actual checkpoint `q_proj`, `k_proj` and `v_proj` are executed once. One live QKV source surface is shared by all three attention routes.

Required counters:

```text
actual QKV projection count = 1
QKV consumer count = 3
duplicate QKV projection count = 0
checkpoint QKV reconstruction count = 0
host QKV upload count = 0
```

Arbitrary layer greater than 0 is blocked until a previous-layer hidden lease owns the actual input generation.

## 6. Shared-runtime candidate and R6 shadow

The canonical candidate route reuses:

```text
W5 Stage10 shared statistics runtime
W6 Stage11 shared global-softmax runtime
W7 Stage12 shared weighted-value runtime
W8 layout-aware context parity runtime
```

R6 remains:

```text
R6-R2 Stage10 actual-checkpoint statistics witness
R6-R3 Stage11 atlas-parallel streaming merge witness
R6-R4 Stage12 BHQD weighted-V shadow oracle
```

R6-specific attention kernels are not renamed into the canonical shared runtime. Existing W5/W6/W7 and R6 kernels remain separate until a later shared-runtime implementation rebase is physically admitted.

## 7. Context parity

Context scalar count for the seq32 fixture:

```text
1 * 32 * 32 * 64 = 65536
```

Three GPU comparisons are required:

```text
Headwise BHQD vs R6 BHQD
Headwise BHQD vs W7 BQHD
R6 BHQD vs W7 BQHD
```

The existing Headwise parity pipeline and W8 layout-aware parity pipeline are reused. No duplicate attention-compute WGSL is introduced.

Required:

```text
compared scalar count per pair = 65536
three-pair compared scalar count = 196608
Headwise-R6 mismatch = 0
Headwise-W7 mismatch = 0
R6-W7 mismatch = 0
context payload readback count = 0
compact status readback only
```

## 8. Same-device Burn tensor adoption

Each context route is adopted into a Burn tensor by one explicit same-device copy.

```text
context source COPY_SRC capability = true
Burn destination COPY_DST capability = true
same device = true
same queue lineage = true
copy count = 3
cross-device copy count = 0
context CPU payload readback count = 0
zero-copy claim count = 0
```

R6-R4 candidate context adds `COPY_SRC` only as a consumer permission. Stage12 arithmetic, parity and writer authority remain unchanged.

## 9. Existing body OProj adoption

R6-R5 uses the actual checkpoint tensor:

```text
checkpoint tensor key = model.layers.0.self_attn.o_proj.weight
runtime target key = layers.0.attn.o_proj
```

The gate builds exactly one checkpoint-backed `AshLinear` OProj module and shares that same module instance across Headwise, W7 and R6 context routes.

```text
checkpoint payload read count = 1
checkpoint weight upload count = 1
AshLinear OProj module instance count = 1
route dispatch count = 3
prepared runtime LoRA set count = 1
fixture runtime LoRA attachment count = 0
trainable LoRA slot count = 0
synthetic W9A projection dispatch count = 0
```

This is the same `AshLinear` implementation, target key, checkpoint tensor and prepared LoRA boundary used by `AshDecoderBlock.o_proj`. R6-R5 does not construct or execute the rest of the decoder block.

## 10. OProj parity

The three actual OProj outputs are compared pairwise on GPU.

```text
Headwise OProj vs R6 OProj
Headwise OProj vs W7 OProj
R6 OProj vs W7 OProj
```

Required:

```text
OProj scalar count per route = 65536
compared scalar count per pair = 65536
three-pair compared scalar count = 196608
all pair mismatch counts = 0
non-finite output count = 0
OProj payload readback count = 0
```

## 11. Writer-preservation boundary

R6-R5 stops after OProj parity.

```text
Headwise writer preserved = true
production authority unchanged = true
legacy training writer unchanged = true
residual commit count = 0
post-attention norm dispatch count = 0
MLP dispatch count = 0
next-layer publish count = 0
backward dispatch count = 0
optimizer write count = 0
base-weight mutation count = 0
LoRA-weight mutation count = 0
checkpoint write count = 0
```

## 12. Implemented source surfaces

New model-core files:

```text
crates/model_core/src/attention_stage11_flag_domain.rs
crates/model_core/src/attention_context_layout_tag.rs
crates/model_core/src/base_train_atlas_wave_02_r6_r5_body_splice.rs
crates/model_core/src/base_train_atlas_wave_02_r6_r5_oproj_shadow.rs
```

New backend files:

```text
crates/burn_webgpu_backend/src/attention_context_layout_compare.rs
crates/burn_webgpu_backend/src/body_oproj_output_compare.rs
```

New base-train files:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r5_authority.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r5_receipts.rs
```

New gate and CLI:

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r5.args
```

Modified surfaces:

```text
crates/model_core/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
crates/base_train/src/lib.rs
crates/orchestrator_local/Cargo.toml
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r4_stage12_weighted_v.rs
```

The user-supplied canonical runtime crate is restored at:

```text
crates/runtime
```

The source bundle does not fabricate a missing root workspace `Cargo.toml` or `crates/artifact_store`.

## 13. CLI policy gates

The response file must set all of the following to true:

```text
--require-actual-body-qkv
--require-shared-runtime-candidate
--require-r6-shadow-oracle
--require-headwise-authority
--require-layout-tagged-context
--require-actual-oproj
--require-same-device-copy
--require-context-payload-readback-zero
--require-oproj-payload-readback-zero
--require-residual-commit-zero
--require-mlp-dispatch-zero
--require-next-layer-zero
--require-writer-preserved
```

Output directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r5/canonical-body-shared-runtime-rebase-v1
```

## 14. Required receipts

```text
00_parent_r6_r4_physical_chain
01_stage11_flag_domain_isolation
02_shared_stage10_source_sidecar
03_w7_shared_runtime_receipt
04_headwise_layout_tag
05_w7_layout_tag
06_r6_layout_tag
07_context_three_way_parity
08_oproj_tensor_authority
09_actual_body_oproj_module
10_headwise_oproj_route
11_w7_oproj_route
12_r6_oproj_route
13_oproj_three_way_parity
14_writer_preservation
15_body_splice_receipt
```

The final manifest records the direct R6-R4 parent digest, G202D manifest digest, QKV source identity, three layout-tagged context identities, OProj module identity, checkpoint weight identity, comparison coverage and writer-preservation receipt.

## 15. Static admission performed by the bake

```text
Rust delimiter scan = PASS for 10 primary Rust files
orchestrator Cargo TOML parse = PASS
CLI response pair parse = PASS for 70 unique keys
Cargo bin registration = PASS
R6 context COPY_SRC contract = PASS
single OProj module construction surface = PASS
module export scan = PASS
isFinite references in primary changed files = 0
subgroupAdd references in primary changed files = 0
unsafe blocks in primary changed files = 0
transmute references in primary changed files = 0
```

These checks do not replace Rust type-check, WGSL module creation or physical GPU parity.

## 16. Validation boundary

The bake environment did not contain `cargo`, `rustc` or `rustfmt`, and network DNS prevented toolchain acquisition.

Therefore:

```text
Rust type-check = judgment deferred
WGSL module creation = judgment deferred
physical GPU parity = judgment deferred
PASS token = not claimed before user-side execution
```

## 17. Cargo commands

Type-check:

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate
```

Physical gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r5_canonical_body_splice_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r5.args"
```

## 18. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R5_CANONICAL_BODY_SHARED_RUNTIME_REBASE_ACTUAL_CHECKPOINT_QKV_SINGLE_SOURCE_CONSUMER_SPLICE_G202D_W5_W6_W7_CANDIDATE_R6_R2_R3_R4_SHADOW_ORACLE_HEADWISE_AUTHORITATIVE_REFERENCE_STAGE11_FLAG_DOMAIN_ISOLATION_W6_ALL_MASKED_R6_ALL_CHUNKS_CONSUMED_STAGE12_ROW_CLASSIFICATION_LAYOUT_TAGGED_PRE_OPROJ_CONTEXT_HEADWISE_BHQD_SHARED_TENSORCUBE_BQHD_R6_BHQD_SEMANTIC_BQHD_SHAPE_STRIDE_GENERATION_COMPLETION_SEALED_SAME_DEVICE_BURN_TENSOR_ADOPTION_ACTUAL_ASH_DECODER_BLOCK_OPROJ_CHECKPOINT_WEIGHT_RUNTIME_LORA_BINDING_FULL_SURFACE_CONTEXT_AND_OPROJ_THREE_WAY_PARITY_NO_SYNTHETIC_W9A_PROJECTION_CONTEXT_PAYLOAD_READBACK_OPROJ_PAYLOAD_READBACK_LAYOUT_RELABEL_HIDDEN_TRANSPOSE_DUPLICATE_QKV_PROJECTION_CROSS_DOMAIN_FLAG_CAST_RESIDUAL_COMMIT_MLP_NEXT_LAYER_BACKWARD_OPTIMIZER_WEIGHT_CHECKPOINT_MUTATION_PRODUCTION_OR_TRAINING_ROUTE_PROMOTION_HEADWISE_WRITER_AND_PRODUCTION_AUTHORITY_PRESERVED_PROOF_LEDGER_HOLD_SEALED
```

## 19. Final seal

```text
R6-R5 is not another attention-engine fork.
It is the canonical body splice that lets one actual checkpoint QKV surface feed the existing W5/W6/W7 candidate, the R6 shadow oracle and the Headwise authority, isolates incompatible Stage11 flag domains, seals BHQD/BQHD physical layouts, adopts all three contexts on the same device, executes one shared actual checkpoint-backed OProj module, proves full-surface context and OProj parity, and preserves Headwise writer authority with all downstream commits held.
```
