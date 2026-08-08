# ASH-BASETRAIN-INFERENCE-CANARY-01-D1

## Cargo Bin Registry / Exact Tokenizer Path Binding Closure

> Parent implementation SSOT: `ASH-BASETRAIN-INFERENCE-CANARY-01`
> Physical forward parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10`
> Forward numerical authority: `LogitSurfaceAuthoritySlot`
> Runtime input authority: `BaseTrainRuntimeInputSequenceAuthority`
> Tokenizer decode authority: `TokenizerManifest` + `tokenizer_core::decode_ssot`
> Current tokenizer manifest path SSOT: `D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json`
> Proof ledger: HOLD

---

# 1. D1 reason

The CANARY-01 gate source existed at:

```text
crates/orchestrator_local/src/bin/ash_basetrain_inference_canary_01_gate.rs
```

but `crates/orchestrator_local/Cargo.toml` uses an explicit `[[bin]]` registry. A source file without an explicit registry entry is therefore not a Cargo target. The observed runtime/launch failure was:

```text
error: no bin target named `ash_basetrain_inference_canary_01_gate`
```

D1 repairs the authority mismatch instead of renaming or reusing the training coordinator gate.

---

# 2. Cargo bin registry SSOT

The same revision that contains the canary gate source must contain:

```toml
[[bin]]
name = "ash_basetrain_inference_canary_01_gate"
path = "src/bin/ash_basetrain_inference_canary_01_gate.rs"
required-features = ["orchestrator_tcu_audit_bins"]
```

The source path and target name are exact. No alias target, training-gate reuse, or auto-discovery assumption is admitted.

---

# 3. Tokenizer manifest path SSOT

For the current workspace, the inference canary response file must bind exactly:

```text
--inference-canary-tokenizer-manifest
D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json
```

The previous `${ASH_TOKENIZER_MANIFEST}` placeholder is retired for this revision.

No environment fallback, alternate manifest search, silent path correction, historical tokenizer fallback, or manifest substitution is admitted. If the workspace path changes, the path must change through an explicit spec/args revision.

The tokenizer artifact remains external runtime input and is not copied into the baked ZIP.

---

# 4. Branch contract

CANARY-01 remains an inference validation branch directly from R6-R10:

```text
                                      +-> R6-R11 loss -> R6-R12 backward
R6-R10 canonical logits -------------+
                                      +-> INFERENCE-CANARY-01
```

Required:

```text
R6-R10 invocation = exactly 1
R6-R11 invocation = 0
R6-R12 invocation = 0
```

Training coordinator behavior is unchanged by D1.

---

# 5. Last-valid-query contract

Use the exact retained runtime input authority:

```text
valid_length = row_valid_lengths[0]
last_valid_query = valid_length - 1
```

For the current fixture:

```text
B=1
Q=32
V=48259
valid_length=32
last_valid_query=31
selected row offset=1496029
```

R6-R11 target rows are not inference-position authority.

---

# 6. GPU top-1 contract

CANARY-01 performs deterministic full-vocabulary GPU argmax only:

```text
Stage 1: workgroup 256, one partial winner per group
Stage 2: partial winners -> one winner
```

Current V=48259 yields 189 stage-1 partials. This count remains runtime-derived.

Comparator:

```text
nonfinite -> fail
higher logit -> win
exact equal logit -> lower token id wins
```

The shared `burn_webgpu_backend::wgsl_numeric_contract` owns finite classification. Local `isFinite` assumptions are forbidden.

---

# 7. Readback boundary

Forbidden:

```text
full BQV logit readback
selected full-V row readback
CPU argmax
CPU finite scan
```

Allowed compact semantic observation:

```text
u32 token_id
f32 logit
```

The implementation may use aligned status/staging bytes and must report physical readback bytes truthfully.

---

# 8. Tokenizer identity contract

Before decode require exact manifest admission:

```text
manifest.trainer.vocab_size == V
manifest.vocab.len() == V
embedded manifest hash recomputes exactly
vocab hash recomputes exactly
reserved-token hash recomputes exactly
canonical vocab IDs are unique
canonical IDs cover exactly 0..V-1
selected token id resolves exactly once
```

Use existing `tokenizer_core::decode_ssot` functions. No token remap or second-best substitution is allowed.

---

# 9. Generation/training boundaries

Required zeros:

```text
loss execution=0
backward=0
optimizer=0
weight mutation=0
sampling=0
autoregressive loop=0
sequence append=0
second forward=0
KV cache=0
production inference claim=0
```

CANARY-01 observes one next-token winner only.

---

# 10. D1 implementation surface

D1 changes only:

```text
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_inference_canary_01.rs
specs/cli/ash_basetrain_inference_canary_01.args
```

The canary numerical implementation, shaders, gate source, R6-R10 parent, R6-R11, and R6-R12 are unchanged.

Build revision:

```text
inference-canary-01-d1-explicit-bin-registration-and-tokenizer-path-binding-v1
```

---

# 11. Cargo run

The exact tokenizer path is already in the canary response file. No environment variable setup is required.

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_inference_canary_01_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args" `
     "@specs/cli/ash_basetrain_inference_canary_01.args"
```

Do not run `cargo clean` without independent stale-build evidence.

---

# 12. Expected physical evidence

Current fixture should report at least:

```text
logit_shape_bqv=1x32x48259
logit_scalar_count=1544288
row_valid_length=32
last_valid_query=31
vocab_size=48259
top1_workgroup_size=256
top1_stage1_partials=189
top1_reduction_passes=2
top1_visited=48259
top1_finite=48259
top1_nonfinite=0
top1_final_candidate_count=1
selected_token_id=<physical observation>
selected_logit=<physical observation>
tokenizer_identity_bound=1
exact_vocab_piece_resolved=1
logit_pointer_unchanged=1
input_authority_unchanged=1
raw_logit_payload_readback=0
loss_execution=0
backward=0
optimizer=0
sampling=0
autoregressive_loop=0
second_forward=0
kv_cache=0
production_inference_claim=0
proof_ledger=HOLD
```

Selected token identity, logit, piece, and decoded fragment remain physical observations and are not predeclared.

---

# 13. Admission seal

D1 is admitted only when Cargo recognizes the explicit bin target and the dedicated canary physically executes through R6-R10, full-vocab GPU top-1, exact tokenizer-manifest identity, and one-token decode observation without entering loss, backward, sampling, autoregressive generation, KV-cache, optimizer, or production-inference paths.
