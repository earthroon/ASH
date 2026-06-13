# QW-50-R0W-C
## Decode Duplication Trace Semantics Split / Generated Repeat Attribution Seal

## 1. SSOT
- base_patch: QW-50-R0W-B
- related_chain: QW-52C-R13-S6
- mutation_scope: trace semantics + wrapper path preparation only
- sampler_mutation: false
- logit_mutation: false
- token_selection_mutation: false

## 2. Prior Evidence
- last_token_push.pushed: false
- prefix_len_delta: 0
- legacy duplication_detected: true
- legacy recommended_next_patch: QW-50-R0W-B
- repeated token: 417 / ▁보니까

## 3. Repair Decisions
- prefix push duplication is counted only when the last-token push actually occurs and prefix_len_delta > 0.
- generated token self-repeat is attributed as generated_history_repeat when pushed=false and prefix_len_delta=0.
- R0W-B is not recommended again when only generated-history repeat remains.
- wrapper now patches both checkpoint_path and tokenizer_manifest_path before Vulkan inference.

## 4. Wrapper Paths
- checkpoint_path: D:/1111113232/DUST/1/ash_pass3/tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors
- tokenizer_manifest_path: D:/1111113232/DUST/1/ash_pass3/tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json

## 5. Static Validation
- status: PASS_STATIC
- cargo_verified: false
- cargo_note: cargo/rustc unavailable in bake environment

## 6. No Mutation Proof
- sampler_mutation: false
- logit_mutation: false
- token_ban_added: false
- rerank_execution: false
- retry_execution: false
- generated_sequence_mutation: false

## 7. Next Patch Recommendation
- QW-50-R0X-A — Greedy Repeat Attractor Observation / No Token Mutation Seal
