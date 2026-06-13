# 16AI-6W-7 Shadow Policy Expansion Probe

## Purpose

Verify that the byte-token suppression shadow policy registered in 16AI-6W-6 can enter a shadow-only expansion track without enabling the default runtime, mutating the sampler, or committing the policy as a live runtime path.

## Source gates

- 16AI-6W-6: PASS_SUPPRESSION_POLICY_SHADOW_COMMIT
- 16AI-6W-5: PASS_CONTROLLED_SUPPRESSION_REPLAY
- 16AI-6W-4: PASS_SUPPRESSION_POLICY_DRY_COMMIT_GATE
- 16AI-6W-3: PASS_SUPPRESSION_DRY_RUN_REPLAY
- 16AI-6W-2: PASS_BYTE_TOKEN_SUPPRESSION_CANDIDATE_GATE
- 16AI-6W-1: PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION
- 16AI-6V-5-R3: PASS_DECODER_OUTPUT_SANITY_GATE

## Contract

- expansion_mode=shadow-expansion-only
- default_runtime_enabled=false
- default_sampler_mutated=false
- output_mutated=false
- runtime_default_committed=false
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false
- embedding_resize_required=false

## Expected decision

- Low-risk policies are eligible for horizon-16 shadow expansion and later case expansion.
- Medium-risk policies are eligible only with risk tracking and case-limited expansion.
- No policy is enabled in the default runtime by this commit.
