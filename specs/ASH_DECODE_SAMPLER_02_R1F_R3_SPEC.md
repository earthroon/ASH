# ASH-DECODE-SAMPLER-02-R1F-R3

## Native GPU Stochastic Selection /
## Greedy Authority Revocation /
## CPU Materialization Zero /
## Top-p Min-p Multinomial Receipt Seal

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1F-R3
parent_patch_id=ASH-DECODE-SAMPLER-02-R1F-R2
patch_class=native_gpu_stochastic_selection_authority_hardening
runtime_schema=ash.decode.sampler.02.r1f.r3.native_gpu_stochastic_selection.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1f_r3_native_gpu_stochastic_selection_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1f_r3_local_manifest.json
r1f_r2_spec_commit=677207e0dc1104c9a3cfbefdb15f333dd7335c32
parent_r1f_r2_r3_archive_sha256=b9dcb9a455d672158b50fcb822d2d3e9227b2e4ca08482c8159a38d0c49a1be7
```

Required parent evidence is the complete R1A through R1F-R2 artifact and manifest chain. Every manifest must hash-bind the exact referenced primary artifact. Copied PASS tokens are not evidence.

---

# 1. Parent truth

R1F-R2 proves one canonical native WGPU inference request completed with:

```text
verified checkpoint/model/tokenizer binding
single native model instance
bound prompt and decode session
actual prefill and decode forward receipts
KV write-read session identity
GPU vocab atlas
row-gather embedding
candidate/final binding closure
```

The live log still showed:

```text
scope=greedy_fallback
allowed=true
materialized=true
reason=lazy_gpu_last_row_to_cpu_row
```

The legacy atlas projection also materialized each tile through CPU, assembled a CPU `merged_logits`, and uploaded the merged row again. R1F-R3 removes those authority and materialization gaps.

---

# 2. Purpose

Make native GPU stochastic sampling the only selected-token owner on the canonical R1F-R3 route:

```text
row-gather embedding
-> native transformer forward
-> tiled lm_head projection
-> GPU-resident global logits row
-> same-device raw lease
-> GPU special-token/EOS/penalty filtering
-> temperature
-> top-k
-> min-p
-> top-p
-> GPU multinomial choice
-> selected-token scalar receipt
-> token commit
```

Required truth:

```text
selection_authority=strict_multistage_gpu_sampler_raw_lease
greedy_authority_step_count=0
cpu_materialized_step_count=0
atlas_tile_cpu_materialized_step_count=0
host_upload_step_count=0
cpu_oracle_step_count=0
legacy_sampler_step_count=0
fallback_step_count=0
```

Argmax may remain diagnostic-only. It may not commit a token.

---

# 3. Canonical policy

Add a typed production policy:

```text
DecodeSamplerPolicyId::NativeTopPMinPProduction
```

Canonical scalars:

```text
temperature=0.72
top_k=40
top_p=0.92
min_p=0.04
```

Typed ownership locks temperature, top-k, top-p, min-p, and seed. Structure routing may not mutate those fields after finalization.

Canonical policy object:

```text
NativeGpuStochasticSelectionPolicy
policy_id=native_gpu_top_p_min_p_multinomial_v1
```

It requires:

```text
native WGPU
GPU vocab atlas
row-gather embedding
GPU-resident atlas output
same-device raw logits lease
strict multistage sampler
sampled=true
step-derived RNG
positive temperature
active top-p
active min-p
```

It forbids:

```text
greedy authority
CPU logits materialization
host upload fallback
CPU oracle
legacy GPU sampler
sampler fallback
top-k overflow fallback
structure rerank selection authority
result-side receipt reconstruction
```

---

# 4. GPU-resident vocab projection

The full lm_head weight remains tiled. The canonical strict route must not allocate the full 395,337,728-byte lm_head buffer.

Each atlas tile performs GPU matmul and contributes directly to one GPU-resident contiguous logits row. The row is approximately:

```text
48259 tokens * 4 bytes = 193036 bytes
```

Required receipt:

```text
GpuResidentVocabAtlasProjectionReceipt
```

Per projection it records:

```text
projection ordinal
vocab size
hidden size
tile count
tile capacity
global logits row bytes
projection dispatch count
projection completion count
segment gap count
segment overlap count
ragged-tail coverage
CPU tile readback count
CPU merged-logits allocation count
host reupload count
GPU-resident status
receipt digest
```

Required:

```text
CPU tile readback count=0
CPU merged-logits allocation count=0
host reupload count=0
segment gap count=0
segment overlap count=0
ragged tail covered=true
```

The legacy non-strict projection may remain for other routes, but the canonical R1F-R3 production branch may not call `.into_data()`, construct `merged_logits`, or use `Tensor::from_data` for projected logits.

---

# 5. Same-device last-logits authority

The GPU-resident logits row is borrowed through the existing strict raw-lease bridge. Device identity must match the active native model and GPU sampler runtime.

Allowed readback:

```text
selected token id scalar
selected score/logprob scalar
compact candidate/filter telemetry
```

Forbidden readback:

```text
full logits row
atlas tile logits
CPU merged logits
CPU softmax/top-p/min-p
CPU greedy argmax
```

---

# 6. Filter and selection order

Canonical order:

```text
special-token and EOS legality mask
repetition/frequency/active penalties
temperature scaling
top-k
min-p
top-p renormalization
multinomial draw
selected-token legality verification
```

The selected token must be present in the final candidate set and unmasked by the special-token/EOS contract.

---

# 7. Step-derived RNG

Add:

```text
NativeGpuStepRngSubstream
derive_native_gpu_step_rng
```

The substream digest binds:

```text
root seed
effective runtime binding digest
model instance id
decode session id
generation index
decode step ordinal
sampler policy digest
```

Required:

```text
same inputs and step -> reproducible substream
different step -> different substream
different session -> different substream
different root seed -> different substream
RNG substream duplicate count=0
```

Selected tokens are not required to differ between seeds because stochastic draws may coincide.

---

# 8. Step receipt

Add:

```text
NativeGpuStochasticStepReceipt
```

Every generated token records:

```text
model/tokenizer/session/binding identities
sampler policy id and digest
same-device raw=true
vocab size
temperature/top-k/top-p/min-p bits
root and step seed
RNG counter and digest
pre-filter candidate count
post-top-k count
post-min-p count
post-top-p count
min-p threshold
active max and sum-exp
selected token id
selected score
selected logprob
selected rank
selected in final set
selected masked status
sampled=true
multinomial executed=true
path=multistage
selected_token_source=strict_multistage_gpu_sampler_raw_lease
CPU/host/oracle/greedy/legacy/fallback flags
receipt digest
```

Any missing, mismatched, non-finite, masked, fallback, or non-multistage evidence fails closed.

---

# 9. Run summary

Add:

```text
NativeGpuStochasticRunSummary
```

It aggregates:

```text
generated token count
stochastic step count
multinomial step count
sampled-true step count
same-device raw step count
CPU materialized step count
atlas tile CPU materialized step count
host upload step count
CPU oracle step count
greedy authority step count
legacy sampler step count
fallback step count
top-k overflow fallback step count
invalid final-set step count
RNG duplicate count
model/session switch count
selected-token digest
step-receipt chain digest
```

PASS requires every generated step to be native GPU stochastic and every forbidden count to be zero.

---

# 10. Runtime integration

Add `NativeGpuStochasticRuntimeConfig` under `CanonicalLiveSmokeRuntimeConfig`.

The runtime must:

```text
validate the R1F-R3 strict contract before model load
construct the canonical policy
apply canonical sampled scalars and root seed
set rollout policy to MultistageOnly
set fallback_on_mismatch=false
set fallback_on_topk_overflow=false
bind StrictGpuDecodePolicy before first forward
select sampled generation entrypoint
collect projection and stochastic step receipts
build run summary
propagate receipts to StandardInferResult and candidate output
```

The result-level sampled backend count is derived from the stochastic run summary, not from greedy purity telemetry.

---

# 11. Candidate and result propagation

The only accepted propagation chain is:

```text
GenerationTelemetry
-> StandardInferResult
-> StandardInferCandidateOutput
-> R1F-R3 gate artifact
```

Result and candidate must match the run summary on:

```text
effective runtime binding digest
model instance id
decode session id
sampler policy digest
```

Required:

```text
binding_origin=live_generation_carry_through
result binding reconstruction count=0
candidate binding reconstruction count=0
route receipt reconstruction count=0
```

---

# 12. Canonical live gate

Add:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1f_r3_native_gpu_stochastic_selection_gate.rs
```

The gate invokes exactly one canonical:

```text
runtime::run_standard_infer_with_decode
```

Required CLI:

```text
--repo-root
--r1a-parent-artifact
--r1a-parent-manifest
--r1b-parent-artifact
--r1b-parent-manifest
--r1c-parent-artifact
--r1c-parent-manifest
--r1d-parent-artifact
--r1d-parent-manifest
--r1e-parent-artifact
--r1e-parent-manifest
--r1f-parent-artifact
--r1f-parent-manifest
--r1f-r2-parent-artifact
--r1f-r2-parent-manifest
--runtime-profile
--smoke-input
--smoke-max-new-tokens
--smoke-min-new-tokens
--temperature
--top-k
--top-p
--min-p
--seed
--require-native-wgpu
--forbid-greedy
--forbid-cpu-materialize
--forbid-host-upload
--forbid-cpu-oracle
--forbid-legacy-sampler
--forbid-fallback
--full-checkpoint-hash
--out-dir
```

Canonical values:

```text
smoke input=The train has already left.
max new tokens=8
min new tokens=4
temperature=0.72
top-k=40
top-p=0.92
min-p=0.04
seed=48259
```

---

# 13. Negative-control matrix

Minimum 96 cases:

```text
16 policy validation
16 RNG substream
16 filter pipeline
16 greedy authority rejection
16 CPU materialization rejection
16 result propagation
```

Required rejected controls include:

```text
temperature zero
top-k one
top-p inactive
min-p inactive
missing policy digest
legacy greedy execution mode
native GPU argmax authority
CPU oracle authority
legacy GPU sampler authority
same-device raw missing
host upload observed
CPU last-logits row observed
atlas tile materialization observed
CPU merged logits observed
sampled=false
multinomial=false
non-multistage path
fallback reason present
top-k overflow fallback
selected token absent from final set
selected token masked
RNG substream reused across steps
candidate/result receipt reconstructed
```

Every expected rejection must report:

```text
rejected=true
fallback_used=false
```

---

# 14. Static gates

```text
strict GPU sampled choice call count >=1
strict sampled choice is production authority
strict raw-lease dispatch count >=1
multistage-only rollout required
fallback-on-mismatch false
fallback-on-top-k-overflow false
canonical greedy call count=0
canonical CPU oracle count=0
canonical CPU materialize allowed count=0
canonical host upload allowed count=0
canonical legacy sampler allowed count=0
strict atlas projection `.into_data()` count=0
strict atlas CPU merged-logits count=0
strict atlas host reupload count=0
GPU-resident global logits row owner count=1
step-seed derivation function count=1
stochastic step receipt builder count=1
result binding reconstruction count=0
```

---

# 15. Required local artifacts

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1f_r3_native_gpu_stochastic_selection_runtime_artifact.json
  ash_decode_sampler_02_r1f_r3_local_manifest.json
  ash_decode_sampler_02_r1f_r3_parent_binding_receipt.json
  ash_decode_sampler_02_r1f_r3_policy_receipt.json
  ash_decode_sampler_02_r1f_r3_gpu_resident_vocab_projection_receipt.json
  ash_decode_sampler_02_r1f_r3_same_device_last_logits_receipt.json
  ash_decode_sampler_02_r1f_r3_rng_substream_receipt.json
  ash_decode_sampler_02_r1f_r3_filter_pipeline_receipt.json
  ash_decode_sampler_02_r1f_r3_stochastic_step_receipts.json
  ash_decode_sampler_02_r1f_r3_stochastic_run_summary.json
  ash_decode_sampler_02_r1f_r3_greedy_authority_revocation_receipt.json
  ash_decode_sampler_02_r1f_r3_cpu_materialization_zero_receipt.json
  ash_decode_sampler_02_r1f_r3_candidate_final_binding_receipt.json
  ash_decode_sampler_02_r1f_r3_negative_control_matrix.json
  ash_decode_sampler_02_r1f_r3_static_checks.json
  ash_decode_sampler_02_r1f_r3_no_mutation_guard.json
  ash_decode_sampler_02_r1f_r3_model_quality_claim_guard.json
  ash_decode_sampler_02_r1f_r3_verdict.json
```

Per-case files live under `workspace/runtime/decode/r1f_r3/cases/<case_id>/`.

Generated runtime artifacts, manifests, receipts, and case directories are excluded from the source bake archive.

---

# 16. Primary artifact ABI

Required flat top-level fields:

```text
schema
patch_id
parent_patch_id
pass
status
verdict
primary_artifact
manifest
runtime_binding_digest
model_instance_id
decode_session_id
sampler_policy_id
sampler_policy_digest
selection_authority
generated_token_count
stochastic_step_count
multinomial_step_count
sampled_true_step_count
cpu_materialized_step_count
atlas_tile_cpu_materialized_step_count
greedy_authority_step_count
fallback_step_count
negative_control_case_count
negative_control_fail_count
model_quality_claim_count
```

Duplicate keys or nested replacement of this public ABI fail closed.

---

# 17. Canonical failures

```text
R1FR2ParentEvidenceIncomplete
NativeGpuStochasticPolicyMissing
NativeGpuStochasticPolicyDigestMissing
NativeGpuStochasticPolicyMismatch
NativeGpuStochasticTypedOwnershipMissing
NativeGpuStochasticTemperatureInvalid
NativeGpuStochasticTopKInvalid
NativeGpuStochasticTopPInactive
NativeGpuStochasticMinPInactive
NativeGpuStochasticRootSeedMissing
NativeGpuStochasticStepSeedReuse
NativeGpuStochasticSameDeviceRawMissing
NativeGpuStochasticRawLeaseDeviceMismatch
NativeGpuStochasticSamplerRuntimeUnavailable
NativeGpuStochasticNonMultistagePath
NativeGpuStochasticSampledFalse
NativeGpuStochasticMultinomialNotExecuted
NativeGpuStochasticSelectedTokenMissing
NativeGpuStochasticSelectedTokenNotInFinalSet
NativeGpuStochasticSelectedTokenMasked
NativeGpuStochasticSelectedScoreNonFinite
NativeGpuStochasticSelectedLogprobMissing
NativeGpuStochasticFallbackObserved
NativeGpuStochasticTopKOverflowFallbackObserved
NativeGpuStochasticLegacySamplerObserved
NativeGpuStochasticCpuOracleObserved
NativeGpuStochasticGreedyAuthorityObserved
NativeGpuStochasticTileArgmaxAuthorityObserved
NativeGpuStochasticHostUploadObserved
NativeGpuStochasticLastLogitsCpuMaterialized
NativeGpuStochasticAtlasTileCpuMaterialized
NativeGpuStochasticMergedLogitsCpuBuildObserved
NativeGpuStochasticGpuResidentAtlasOutputMissing
NativeGpuStochasticGlobalLogitsCoverageGap
NativeGpuStochasticGlobalLogitsCoverageOverlap
NativeGpuStochasticVocabTailCoverageMismatch
NativeGpuStochasticCandidateBindingMismatch
NativeGpuStochasticResultBindingMismatch
NativeGpuStochasticReceiptReconstructed
CompileTruthMissing
```

---

# 18. PASS formula

```text
PASS =
  R1A through R1F-R2 parent binding pass
  && compile truth pass
  && real runtime bundle verified
  && native model construct count==1
  && native model bind count==1
  && standard infer execution count==1
  && vocab projection==gpu_atlas
  && embedding mode==row_gather
  && full lm_head upload skipped
  && full embedding upload skipped
  && GPU-resident global logits row present
  && projection dispatch count==tile count*generated token count
  && projection completion count==dispatch count
  && segment gap count==0
  && segment overlap count==0
  && tail coverage pass
  && generated token count>=minimum
  && stochastic step count==generated token count
  && multinomial step count==generated token count
  && sampled-true step count==generated token count
  && same-device raw step count==generated token count
  && all selected-token sources are strict multistage GPU raw lease
  && top-p and min-p active on every step
  && all selected tokens are legal and in the final set
  && RNG duplicate count==0
  && all CPU/host/oracle/greedy/legacy/fallback counts==0
  && model/session switch count==0
  && candidate/final binding match
  && result/candidate reconstruction count==0
  && negative-control case count>=96
  && negative-control fail count==0
  && default policy mutation count==0
  && model quality claim count==0
```

PASS proves native stochastic selected-token authority and zero CPU logits materialization on the tested route. It does not prove language quality, translation accuracy, absence of repetition, optimal sampling parameters, teacher-forced target rank, throughput, or production readiness.

---

# 19. Build and run

```powershell
cargo fmt --all -- --check
cargo check --manifest-path crates/burn_webgpu_backend/Cargo.toml
cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_r3_native_gpu_stochastic_selection_gate
```

```powershell
cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_r3_native_gpu_stochastic_selection_gate `
  -- `
  --repo-root . `
  --r1a-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json `
  --r1a-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json `
  --r1b-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json `
  --r1b-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json `
  --r1c-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json `
  --r1c-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json `
  --r1d-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json `
  --r1d-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1d_local_manifest.json `
  --r1e-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_runtime_artifact.json `
  --r1e-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1e_local_manifest.json `
  --r1f-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1f_live_inference_binding_runtime_artifact.json `
  --r1f-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1f_local_manifest.json `
  --r1f-r2-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_runtime_artifact.json `
  --r1f-r2-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --smoke-input "The train has already left." `
  --smoke-max-new-tokens 8 `
  --smoke-min-new-tokens 4 `
  --temperature 0.72 `
  --top-k 40 `
  --top-p 0.92 `
  --min-p 0.04 `
  --seed 48259 `
  --require-native-wgpu true `
  --forbid-greedy true `
  --forbid-cpu-materialize true `
  --forbid-host-upload true `
  --forbid-cpu-oracle true `
  --forbid-legacy-sampler true `
  --forbid-fallback true `
  --full-checkpoint-hash true `
  --out-dir workspace/runtime/decode
```

Expected PASS:

```text
PASS_ASH_DECODE_SAMPLER_02_R1F_R3_NATIVE_GPU_STOCHASTIC_SELECTION_GREEDY_AUTHORITY_REVOKED_CPU_MATERIALIZATION_ZERO_TOP_P_MIN_P_MULTINOMIAL_RECEIPT_NO_FALLBACK_NO_MODEL_QUALITY_OVERCLAIM
```
