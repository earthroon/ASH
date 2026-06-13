# QW-50-R0X-A
## Greedy Repeat Attractor Observation / No Token Mutation Seal

## 1. SSOT
- base_patch: QW-50-R0W-C
- mutation_scope: observation_only
- token_mutation: false
- logit_mutation: false
- sampler_mutation: false

## 2. Implemented
- Added `greedyRepeatAttractorObservation` to `nativeDecodeR0wTrace`.
- Added step-level top1/top2/top3 margin matrix.
- Added top1 lock ratio after repeat onset.
- Surfaced the observation in `infer_only --json`.
- Added PowerShell/CMD/Python Vulkan wrappers.

## 3. No Mutation Proof
- token_ban_added: false
- hard_ban_added: false
- blacklist_mutation: false
- logit_mutation: false
- logit_penalty_added: false
- sampler_mutation: false
- rerank_execution: false
- retry_execution: false
- generated_sequence_mutation: false

## 4. Runtime Paths
- checkpoint_path: `D:/1111113232/DUST/1/ash_pass3/tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors`
- tokenizer_manifest_path: `D:/1111113232/DUST/1/ash_pass3/tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json`

## 5. Verification
- cargo_check_status: NOT_RUN_CARGO_NOT_AVAILABLE_IN_BAKE_ENV
- local command: `cargo check --workspace --all-targets`
- wrapper command: `./scripts/run_qw50_r0x_a_vulkan_infer_wrapper.ps1 -Text "I didn't mean to hurt you. I just wanted to protect you."`

## 6. Next Patch Routing
- low/medium margin: QW-50-R0X-B / Greedy Margin Escape Candidate / Dry-run Only Seal
- high margin or persistent mismatch: QW-50-R0X-C / Runtime Spec Tokenizer Checkpoint Alignment Audit / No Weight Mutation Seal
