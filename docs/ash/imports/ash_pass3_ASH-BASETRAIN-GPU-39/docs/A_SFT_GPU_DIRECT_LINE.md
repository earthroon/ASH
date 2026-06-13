# A-SFT GPU Direct Line Contract v1

## SSOT

A-SFT direct line is defined by the following contract:

- `family`: `sft_lora`
- `mode`: `train`
- `dataset.loss_on`: `response_only`
- `training.plan_kind`: `module_lora` or `module_local_lora`
- `hyper.target_modules`: [`lm_head`]
- `lora.targets`: [`lm_head`]
- `lora.artifact_family`: `module_lora`
- `lora.merge_mode`: `runtime_attach`
- `guards.expect_target_key`: `lm_head`

## Forbidden Drift

The following drift is forbidden:

- SFT config silently falling back to `shared_hidden_classifier`
- `lora.artifact_family=sft_lora` while runtime attachment expects `module_lora`
- prompt tokens contributing to SFT loss
- `hyper.target_modules` and `lora.targets` disagreeing
- unknown config fields being ignored in the sealed config structs
- A-SFT native train-from-features running without `dataset.feature_store_manifest`

## SFT-GPU-1 Scope

This commit seals the config and direct-line plan contract only.

It implements:

- strict config parsing for the A-SFT-facing config structs
- top-level A-SFT contract fields: `family`, `mode`, `lora`, `guards`, `a_sft_native_contract`
- `dataset.loss_on=response_only` as an explicit parsed field
- `training.plan_kind=module_lora` as a required direct-line field
- `lora.artifact_family=module_lora` as the runtime-attach artifact family
- a validator that rejects A-SFT configs drifting back to shared-hidden classifier training
- CLI contract logging before plan construction

It does not implement:

- GPU LoRA A/B update
- response-only loss mask execution
- lm_head module target resolver expansion
- adapter save/reload parity verification
- runtime logits delta verification

## Expected Good Failure Before SFT-GPU-2

After SFT-GPU-1, an A-SFT config should no longer become a shared-hidden plan. If the next failure is:

```txt
no module targets resolved for module_lora training plan
```

that is a good failure for this stage. It means the config entered the module LoRA direct line, and SFT-GPU-2 must seal `lm_head` as a trainable module LoRA target.

## SFT-GPU-2 Target Resolver Seal

`lm_head` is a global `module_lora` target.

It must resolve as:

- target: `lm_head`
- target_key: `lm_head`
- scope: `global`
- attachment count: `1`

It must not resolve as:

- `layers.0.lm_head`
- `layers.N.lm_head`
- `classifier.shared_hidden_token_head`
- `shared_hidden_token_adapter`

Layer-local targets such as `attn.q_proj` remain per-layer targets.

`MODULE_LOCAL_TRACE_TARGETS` intentionally does not include `lm_head`.
`lm_head` is not a layer-local activation trace target; it is the global hidden-to-vocab projection target.

SFT-GPU-2 keeps the SFT-GPU-1 non-goals intact. It does not implement response-only loss execution, GPU LoRA A/B update, adapter save/reload parity, or runtime logits delta verification.

## SFT-GPU-3 Response-only Label Mask Seal

A-SFT direct line uses shifted causal labels. Prompt tokens are condition-only; response tokens are supervised-only.

Given:

```txt
full_ids = [prompt..., response...]
```

The batch builder must produce:

```txt
input_ids = full_ids[..n-1]
labels = full_ids[1..]
```

Then labels are masked by the predicted-token span:

- if the predicted token belongs to prompt span, label = `IGNORE_INDEX` (`-100`)
- if the predicted token belongs to response span, label = token id

Required invariants:

- `input_ids.len() == labels.len() == loss_mask.len()`
- `prompt_loss_tokens == 0`
- `response_loss_tokens > 0`
- response first token is included in loss
- prompt tokens are never supervised
- v1 rejects non-empty template suffix after `{response}`
- truncation must never remove all response tokens

SFT-GPU-3 intentionally stops before CE/lm_head LoRA update when `loss_on=response_only` reaches the direct JSONL trainer. GPU CE/lm_head LoRA update is SFT-GPU-4 scope.

## SFT-GPU-4 GPU lm_head LoRA Training Smoke

SFT-GPU-4 verifies that the A-SFT direct line can perform a minimal WGPU/Burn autodiff update for `lm_head` LoRA.

The sealed smoke path is:

```txt
response-only SFT batch
→ teacher/frozen hidden feature upload
→ base lm_head logits
→ lm_head LoRA delta logits
→ response-token-only CE
→ Burn autodiff gradients
→ optimizer update of lm_head.lora_A / lm_head.lora_B
```

Only these tensors are trainable in the smoke:

- `lm_head.lora_A`
- `lm_head.lora_B`

Frozen / non-trainable:

- tokenizer
- base model / teacher hidden source
- base `lm_head.weight`

Required invariants:

- `target_key == "lm_head"`
- `artifact_family == "module_lora"`
- `prompt_loss_tokens == 0`
- `response_loss_tokens > 0`
- `selected_response_tokens > 0`
- WGPU/autodiff backend is required
- `cpu_training_steps == 0`
- `gpu_training_steps > 0`
- loss is finite
- LoRA B norm changes after update

SFT-GPU-4 intentionally does **not** seal adapter artifact persistence or runtime reload. Those remain SFT-GPU-5/SFT-GPU-6 boundaries.

## SFT-GPU-5 Adapter Manifest / Safetensors Artifact Seal

SFT-GPU-5 persists the trained `lm_head` LoRA tensors as a runtime-readable `module_lora` artifact.

Required artifact layout:

```txt
artifacts/lm_head_lora/
├─ adapter_manifest.json
├─ adapter_model.safetensors
└─ artifact_report.json
```

Required tensor keys:

```txt
lm_head.lora_A
lm_head.lora_B
```

Required shapes:

```txt
lm_head.lora_A = [rank, hidden_size]
lm_head.lora_B = [vocab_size, rank]
```

Required manifest invariants:

- `schema_version == 1`
- `artifact_family == "module_lora"`
- `target_key == "lm_head"`
- `target_modules == ["lm_head"]`
- `feature_strategy == "module_local_io"`
- `format == "safetensors"`
- `adapter_path == "adapter_model.safetensors"`
- `training_contract.loss_on == "response_only"`
- `training_contract.prompt_loss_tokens == 0`
- `training_contract.response_loss_tokens > 0`
- `training_contract.cpu_training_steps == 0`
- `training_contract.gpu_training_steps > 0`
- `validation.reload_ok == true`
- `validation.lora_b_norm > 0`

Forbidden tensor keys:

```txt
layers.0.lm_head.*
classifier.shared_hidden_token_head.*
shared_hidden_token_adapter.*
```

This commit does not verify runtime logits delta. Runtime attachment and LoRA on/off logits comparison are sealed in SFT-GPU-6.

## SFT-GPU-6 Runtime Load / Logits Delta Verification

SFT-GPU-6 closes the A-SFT direct line by converting the sealed `lm_head` artifact into a runtime attachment sidecar, loading it through the existing runtime loader, and verifying that the loaded attachment changes `lm_head` logits.

Required artifact/runtime layout:

```txt
artifacts/lm_head_lora/
├─ adapter_manifest.json
├─ adapter_model.safetensors
├─ adapter_runtime.json
├─ artifact_report.json
├─ runtime_delta_report.json
└─ runtime_delta_report.md
```

Verification flow:

```txt
adapter_manifest.json
+ adapter_model.safetensors
→ adapter_runtime.json RuntimeLoraAttachment sidecar
→ model_core::load_runtime_lora_attachments
→ validate_runtime_lora_attachment_for_module
→ LoRA OFF/ON lm_head logits equivalence check
→ delta stats report
```

SFT-GPU-6 checks the exact lm_head delta equation used by the runtime attachment:

```txt
base_logits = hidden @ lm_head.weight^T
z = hidden @ lora_A^T
delta_logits = z @ lora_B^T * (alpha / rank)
logits_on = base_logits + delta_logits
```

Required invariants:

- `artifact_family == "module_lora"`
- `target_key == "lm_head"`
- runtime sidecar loads through `model_core::load_runtime_lora_attachments`
- runtime module validation passes
- `logits_off_shape == logits_on_shape`
- `delta_max_abs > 0`
- `delta_mean_abs > 0`
- `delta_nonzero_count > 0`
- reload from the runtime sidecar is reproducible within tolerance

This commit does not evaluate generated text quality. Generation hygiene is a later boundary.

## SFT-GPU-7 One-shot CLI Direct-line Acceptance / Generation Hygiene Smoke

SFT-GPU-7 runs the full A-SFT GPU direct line from the existing training CLI and writes a final acceptance report.

Pipeline:

```txt
config strict contract
→ lm_head module_lora target resolver
→ response-only shifted label mask
→ GPU lm_head LoRA training smoke
→ adapter manifest / safetensors artifact
→ runtime load / logits delta verification
→ deterministic generation hygiene smoke
→ direct_line_acceptance.json / md
```

Required acceptance gates:

- `family == sft_lora`
- `dataset.loss_on == response_only`
- `target_key == lm_head`
- `prompt_loss_tokens == 0`
- `response_loss_tokens > 0`
- `gpu_training_steps > 0`
- `cpu_training_steps == 0`
- `artifact_family == module_lora`
- `runtime_delta.delta_max_abs > 0`
- `runtime_delta.delta_mean_abs > 0`
- `generation_hygiene.fail_count == 0`

Generation hygiene is not a style or literary quality score. It only rejects obvious decoding corruption:

- replacement character leakage
- suspicious byte-marker leakage
- Hangul character split patterns such as `장 수 풍 뎅 이`
- empty output
- severe repetition loops

Final reports:

```txt
workspace/lora_runs/<run_name>/acceptance/direct_line_acceptance.json
workspace/lora_runs/<run_name>/acceptance/direct_line_acceptance.md
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/generation_hygiene_report.json
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/generation_hygiene_report.md
```

## SFT-GPU-8 Base-vs-LoRA Sample Report / Quality Eval Fixture Pack

SFT-GPU-8 adds a deterministic comparison window after one-shot direct-line acceptance.

Pipeline:

```txt
quality fixture pack
→ base greedy generation
→ LoRA greedy generation
→ hygiene proxy metrics
→ base-vs-lora comparison metrics
→ human-reviewable Markdown report
→ machine-readable JSON report
```

This is not a literary quality judge. It does not claim that LoRA is stylistically better.
It only makes the comparison reproducible and flags obvious decoding regressions.

Required invariants:

- same prompt fixture
- same tokenizer
- same checkpoint
- same deterministic decode settings
- KV cache reset per prompt
- base output recorded
- LoRA output recorded
- hygiene metrics computed for both outputs
- JSON and Markdown reports written

Hard failure conditions for the LoRA output:

- replacement character leakage
- suspicious byte marker leakage
- Hangul character splitting such as `장 수 풍 뎅 이`
- empty output
- severe repetition loop

Report outputs:

```txt
workspace/lora_runs/<run_name>/eval/quality_fixture_pack_ko.json
workspace/lora_runs/<run_name>/eval/base_vs_lora_samples.json
workspace/lora_runs/<run_name>/eval/base_vs_lora_samples.md
workspace/lora_runs/<run_name>/eval/quality_eval_summary.json
workspace/lora_runs/<run_name>/eval/quality_eval_summary.md
```


## SFT-GPU-8C Hidden Source Guard

A-SFT direct training must not silently load the full checkpoint-backed teacher in train phase.

Allowed hidden sources:

1. `feature_store_manifest`
2. explicitly wired `atlas_grouped_native_hidden`
3. `full_checkpoint_teacher` only when `phase=native_dump`

Forbidden:

```txt
phase=direct_train
→ full checkpoint-backed teacher
```

If neither feature store nor Atlas grouped hidden is available, the run must fail before loading the full checkpoint. This is intentional: OOM prevention is preferred over silent fallback.

## SFT-GPU-8D Native Dump / Feature Store Bridge

SFT-GPU-8D separates full-checkpoint hidden extraction from LoRA training.

Allowed:

```txt
phase=native_dump
-> full checkpoint teacher
-> feature_store_manifest
-> lm_head_weight.safetensors snapshot
```

Allowed:

```txt
phase=train_from_features
-> feature_store_manifest
-> feature batches
-> lm_head LoRA train
```

Forbidden:

```txt
phase=train_from_features
-> full checkpoint teacher
```

The bridge exists to avoid OOM-prone full-checkpoint teacher loading during train phase. The train phase reads the dumped feature batches and the small `lm_head_weight.safetensors` snapshot instead of constructing a full teacher.

## SFT-GPU-8E Native Dump Atlas Grouped Hidden Batching

SFT-GPU-8E seals native dump progress visibility and token-budget grouping.

The native dump phase now uses `a_sft_native_contract.dump_batching` with `strategy=atlas_token_grouped` to prepare response-only examples into groups before hidden extraction.

Required invariants:

```txt
teacher_load_count == 1
strategy == atlas_token_grouped
group_count > 0
feature_batch_count > 0
prompt_loss_tokens == 0
response_loss_tokens > 0
hidden tokens == labels len == loss mask len
```

The dump writes:

```txt
feature_store_work/native_dump_progress_report.json
feature_store_work/native_dump_progress_report.md
```

Each group logs example count, token count, hidden shape, response loss tokens, and timing fields so slow native dump runs can be diagnosed as forward-bound, readback-bound, or write-bound instead of silently crawling.
