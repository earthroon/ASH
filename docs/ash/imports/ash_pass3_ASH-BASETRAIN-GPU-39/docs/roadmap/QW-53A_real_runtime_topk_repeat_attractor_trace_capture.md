# QW-53A — Real Runtime TopK Repeat Attractor Trace Capture / QWave Apply Eligibility Evidence Seal

## SSOT

- Core/runtime/model/tokenizer/backend logic: Rust + WGPU/WGSL only.
- TypeScript/JavaScript scope: frontend display / command bridge only.
- This patch does not mutate token selection, token rank, logits, sampler state, LoRA weights, or model weights.

## State owner

- Runtime capture owner: `crates/runtime/src/qw53a_runtime_topk_trace.rs`
- Validation/report owner: `crates/model_core/src/qw53a_real_runtime_topk_repeat_attractor_trace.rs`
- Existing ingest target: `workspace/runtime_traces/qw52c_r13_s6_runtime_topk_trace_batch.jsonl`

## Runtime output

When `ASH_QW53A_TRACE=1`, runtime writes:

- `workspace/runtime_traces/qw53a_real_runtime_topk_repeat_attractor_trace.jsonl`
- `workspace/runtime_traces/qw52c_r13_s6_runtime_topk_trace_batch.jsonl`
- `workspace/trace/qw53a_runtime_trace_capture_receipt.json`

## Runtime env

```bash
ASH_QW53A_TRACE=1
ASH_QW53A_TOPK=8
ASH_QW53A_REPEAT_WINDOW=32
ASH_QW53A_OUTPUT_DIR=.
```

## Validation commands

```bash
cargo run -p model_core --bin qw53a_real_runtime_topk_repeat_attractor_trace -- .
cargo run -p model_core --bin qw53a_real_runtime_topk_repeat_attractor_trace_validate -- .
cargo run -p model_core --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay -- .
```

## No-apply invariant

The following fields must remain false in every trace record:

- `shadow_result_applied`
- `runtime_apply_allowed`
- `token_selection_mutated`
- `token_rank_mutated`
- `logit_mutated`
- `sampler_mutated`

## Next patch

`QW-53B — Subtitle Safe Sampled Decode Profile / No Greedy Default Trap Seal`
