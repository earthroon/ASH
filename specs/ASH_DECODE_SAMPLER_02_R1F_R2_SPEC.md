# ASH-DECODE-SAMPLER-02-R1F-R2

## Canonical Live Inference Smoke /
## Single Native Model Instance Runtime Receipt /
## Bound Prompt-to-Token Forward Evidence /
## KV Write-Read Session Identity /
## Live Candidate and Final Result Binding Closure

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1F-R2
parent_patch_id=ASH-DECODE-SAMPLER-02-R1F
patch_class=canonical_live_native_inference_binding_smoke
runtime_schema=ash.decode.sampler.02.r1f.r2.canonical_live_inference_smoke.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_local_manifest.json
r1f_spec_commit=a1b6ef97840a0cc5c7ad7f376e42431ee111d60d
parent_r1f_archive_sha256=cf1386f6d19be269dddf9d9a0f2d790adc3c2728ea7b1b0a4ea67e9fc5ce77fa
```

Required parent evidence is the complete R1A through R1F artifact and manifest chain. Every parent manifest must hash-bind the exact referenced primary artifact. Copied PASS markers are not evidence.

---

# 1. Parent truth and remaining gap

R1F proves the production binding APIs, the real R1E bundle reconstruction, deterministic model/tokenizer/session/KV/cache identity helpers, and a 64-case rejection matrix. Its PASS was executed with `--run-live-smoke false`.

R1F does not prove that a real native model forward ran under the new binding contract. Before R1F-R2, the runtime could infer forward activity from generated token count, infer GPU completion from non-empty output, construct a native model inside a repeatable generation closure, and return candidate/result bindings without a dedicated live forward and KV operation receipt.

R1F-R2 closes only this live execution gap.

---

# 2. Canonical live smoke contract

The gate must invoke the existing canonical runtime surface:

```text
runtime::run_standard_infer_with_decode
```

A parallel smoke-only inference engine is forbidden.

The request carries an explicit native-only contract:

```text
patch_id=ASH-DECODE-SAMPLER-02-R1F-R2
require_native_wgpu=true
allow_cpu_fallback=false
allow_reference_generation=false
allow_output_guard_regeneration=false
allow_second_infer_execution=false
smoke_min_new_tokens>=2
smoke_max_new_tokens>=smoke_min_new_tokens
```

Any fallback, retry, second inference, output-guard regeneration, or reference generation causes fail-closed rejection.

---

# 3. Single native model instance ownership

The canonical request must prove:

```text
native_model_construct_count=1
native_model_bind_count=1
checkpoint_bundle_load_count=1
authoritative_native_model_instance_count=1
model_instance_switch_count=0
reference_model_construct_count=0
cpu_fallback_entry_count=0
output_guard_regeneration_count=0
standard_infer_execution_count=1
```

The verified R1E runtime binding is converted into one `VerifiedModelInstanceBinding` before the first authoritative forward. `NativeWgpuModel::bind_verified_model_instance` is single-bind and immutable. A second bind or a model-instance switch fails closed.

---

# 4. Bound prompt encode evidence

The runtime creates one `BoundTokenizerRuntimeIdentity`, one `BoundDecodeSessionContract`, and one `BoundPromptEncodeReceipt` before generation.

The prompt receipt binds:

```text
input_text_sha256
prompt_text_sha256
prompt_template_id
prompt_token_count
ordered_prompt_token_digest
prompt token head and tail
tokenizer_instance_id
tokenizer_vocab_digest
special_token_contract_digest
model_instance_id
decode_session_id
effective_runtime_binding_digest
receipt_digest
```

The session binds the verified model instance, tokenizer instance, prompt token digest, sampling policy digest, EOS authority contract digest, max-new-token limit, and session epoch.

---

# 5. Actual native forward receipts

Token count is not forward evidence. The model-core live route emits actual receipts around the production forward calls.

Required types:

```text
NativeForwardDispatchReceipt
NativeForwardCompletionReceipt
NativeForwardRunSummary
```

Every dispatch receipt includes:

```text
forward_dispatch_id
forward_ordinal
phase=prefill|decode_step
model_instance_id
decode_session_id
effective_runtime_binding_digest
input_token_count
input_token_digest
prompt_token_count
generated_count_before_forward
kv_past_len_before
vocab_limit
command_submission_observed
submitted_work_digest
dispatch_receipt_digest
```

Every completion receipt includes:

```text
same forward dispatch identity
GPU completion evidence source
completion_observed
last-logits storage kind
last-logits shape and vocab size
selected token id
kv_past_len_after
completion receipt digest
```

Accepted GPU completion evidence sources are actual runtime evidence:

```text
queue_submit_and_mapped_readback
queue_submit_and_device_poll
native_raw_logits_bridge_completion
```

Generated token existence, vector length, and simple function return are not accepted as GPU completion evidence.

Required run truth:

```text
native_forward_dispatch_count>=2
native_forward_completion_count=native_forward_dispatch_count
native_forward_incomplete_count=0
completion_dispatch_id_mismatch_count=0
prefill_dispatch_count=1
decode_dispatch_count>=1
gpu_completion_observed=true
model_instance_switch_count=0
decode_session_switch_count=0
```

---

# 6. KV write-read session identity

The production decode state records:

```text
PrefillWrite
DecodeRead
DecodeAppendWrite
FinalStateRead
```

Every operation carries:

```text
operation_id
operation_ordinal
forward_dispatch_id
operation kind
model_instance_id
decode_session_id
effective_runtime_binding_digest
layer count and layer-observation status
prompt length
generated count before operation
past length before and after
read length
write position
expected read length
expected write position
key/value shape digests
identity_verified
monotonic
operation receipt digest
```

Required run truth:

```text
prefill_write_count=1
decode_read_count>=1
decode_append_write_count>=1
final_state_read_count=1
identity_mismatch_count=0
non_monotonic_count=0
cross_session_accept_count=0
cross_model_accept_count=0
read_after_write_observed=true
```

The smoke requires at least two generated tokens so a decode-step KV read-after-write is exercised after prefill.

---

# 7. Live telemetry and result propagation

`GenerationTelemetry` owns the live prompt receipt, native dispatches, native completions, forward summary, KV operations, and KV summary.

The only permitted propagation chain is:

```text
GenerationTelemetry
-> StandardInferResult
-> project_standard_infer_result_to_candidate_output
-> StandardInferCandidateOutput
-> R1F-R2 gate artifact
```

The result and candidate must match the live receipt on:

```text
effective_runtime_binding_digest
model_instance_id
tokenizer_instance_id
decode_session_id
canonical live receipt digest
```

Required origin and reconstruction truth:

```text
binding_origin=live_generation_carry_through
candidate_binding_reconstruction_count=0
result_binding_reconstruction_count=0
route_receipt_binding_reconstruction_count=0
```

Request-side or orchestrator-side reconstruction of missing live binding evidence is forbidden.

---

# 8. Runtime request surface

Add `CanonicalLiveSmokeRuntimeConfig` to `StandardInferRequest` and carry it through `ResolvedStandardInferRequest`.

The runtime validates the contract before model construction. It creates the verified model instance, bound tokenizer identity, decode session, prompt receipt, and EOS authority contract, then inserts them into `GenerationSamplingConfig` before prefill.

The native model is bound before its first forward. CPU/reference branches and output-guard regeneration reject the smoke request rather than silently changing authority.

---

# 9. Gate binary

Add:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_gate.rs
```

The binary:

```text
validates R1A-R1F parent evidence
resolves the real runtime profile
runs one canonical standard inference request
requires native-only execution
projects the final result into one candidate without a second inference
verifies forward/KV/model/session/result identity
writes receipts, primary artifact, and local manifest
```

Required arguments:

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
--runtime-profile
--smoke-input
--smoke-max-new-tokens
--smoke-min-new-tokens
--require-native-wgpu
--allow-cpu-fallback
--allow-reference-generation
--allow-output-guard-regeneration
--full-checkpoint-hash
--out-dir
```

---

# 10. Required local artifacts

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_runtime_artifact.json
  ash_decode_sampler_02_r1f_r2_local_manifest.json
  ash_decode_sampler_02_r1f_r2_parent_binding_receipt.json
  ash_decode_sampler_02_r1f_r2_bound_prompt_encode_receipt.json
  ash_decode_sampler_02_r1f_r2_native_forward_runtime_receipt.json
  ash_decode_sampler_02_r1f_r2_kv_write_read_runtime_receipt.json
  ash_decode_sampler_02_r1f_r2_candidate_final_binding_receipt.json
  ash_decode_sampler_02_r1f_r2_static_checks.json
  ash_decode_sampler_02_r1f_r2_verdict.json
```

Generated artifacts, manifests, receipts, and runtime directories are excluded from the source bake archive.

---

# 11. Canonical failures

```text
R1FParentEvidenceIncomplete
CanonicalLiveSmokePatchIdMismatch
CanonicalLiveSmokeMinimumTooSmall
CanonicalLiveSmokeNativeRequired
CanonicalLiveSmokeCpuFallbackForbidden
CanonicalLiveSmokeReferenceForbidden
CanonicalLiveSmokeRegenerationForbidden
CanonicalLiveSmokeSecondInferForbidden
CanonicalLiveSmokeMaxBelowMinimum
CanonicalLiveSmokeNativeRouteNotSelected
CanonicalLiveSmokeNativeLoadFailed
CanonicalLiveSmokeSecondInferExecutionObserved
CanonicalLiveSmokeOutputGuardRegenerationObserved
CanonicalLiveSmokeGenerationTelemetryMissing
CanonicalLiveSmokePromptReceiptMissing
CanonicalLiveSmokeDecodeSessionMissing
CanonicalLiveSmokeTelemetrySessionMismatch
CanonicalLiveSmokeModelConstructCountInvalid
CanonicalLiveSmokeModelBindCountInvalid
CanonicalLiveSmokeCheckpointLoadCountInvalid
CanonicalLiveSmokeReferenceModelObserved
CanonicalLiveSmokeCpuFallbackObserved
CanonicalLiveSmokeRegenerationObserved
CanonicalLiveSmokeExecutionCountInvalid
NativeForwardDispatchReceiptMissing
NativeForwardCompletionReceiptMissing
NativeForwardCompletionEvidenceMissing
NativeForwardDispatchCompletionMismatch
NativeForwardModelInstanceMismatch
NativeForwardDecodeSessionMismatch
KvPrefillWriteMissing
KvDecodeReadMissing
KvDecodeAppendWriteMissing
KvFinalStateReadMissing
KvIdentityMismatch
KvNonMonotonic
CandidateLiveInferenceReceiptMissing
CandidateFinalBindingMismatch
CompileTruthMissing
```

---

# 12. PASS formula

```text
PASS =
  r1a_through_r1f_parent_binding_pass
  && compile_truth_pass
  && full_checkpoint_hash=true
  && native_model_construct_count==1
  && native_model_bind_count==1
  && checkpoint_bundle_load_count==1
  && authoritative_native_model_instance_count==1
  && model_instance_switch_count==0
  && reference_model_construct_count==0
  && cpu_fallback_entry_count==0
  && output_guard_regeneration_count==0
  && standard_infer_execution_count==1
  && native_forward_dispatch_count>=2
  && native_forward_completion_count==native_forward_dispatch_count
  && native_forward_incomplete_count==0
  && completion_dispatch_id_mismatch_count==0
  && prefill_dispatch_count==1
  && decode_dispatch_count>=1
  && gpu_completion_observed
  && forward_model_instance_switch_count==0
  && forward_decode_session_switch_count==0
  && prefill_write_count==1
  && decode_read_count>=1
  && decode_append_write_count>=1
  && final_state_read_count==1
  && kv_identity_mismatch_count==0
  && kv_non_monotonic_count==0
  && cross_session_kv_accept_count==0
  && cross_model_kv_accept_count==0
  && kv_read_after_write_observed
  && generated_tail_count>=smoke_min_new_tokens
  && candidate_final_binding_match
  && binding_origin==live_generation_carry_through
  && candidate_binding_reconstruction_count==0
  && result_binding_reconstruction_count==0
  && model_quality_claim_count==0
```

PASS proves one canonical native inference request ran with actual prompt, forward, KV, candidate, and result binding receipts. It does not prove model quality, translation quality, throughput, long-session stability, or production promotion.

---

# 13. Build and run

```powershell
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_gate
```

```powershell
cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_gate `
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
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --smoke-input "The train has already left." `
  --smoke-max-new-tokens 4 `
  --smoke-min-new-tokens 2 `
  --require-native-wgpu true `
  --allow-cpu-fallback false `
  --allow-reference-generation false `
  --allow-output-guard-regeneration false `
  --full-checkpoint-hash true `
  --out-dir workspace/runtime/decode
```

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1F_R2_CANONICAL_LIVE_INFERENCE_SMOKE_SINGLE_NATIVE_MODEL_INSTANCE_BOUND_PROMPT_TO_TOKEN_FORWARD_KV_WRITE_READ_SESSION_IDENTITY_LIVE_CANDIDATE_FINAL_RESULT_BINDING_NO_FALLBACK_NO_RETRY_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_canonical_live_inference_smoke_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1f_r2_local_manifest.json
```
