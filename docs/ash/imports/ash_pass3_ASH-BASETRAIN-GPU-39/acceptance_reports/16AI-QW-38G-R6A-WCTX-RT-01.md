# 16AI-QW-38G-R6A-WCTX-RT-01 Acceptance Report

## Status

`BAKED_STATIC_NO_CARGO`

## Acceptance target

RT-01 must bind RT-00 forward output shape evidence to the MOCK-20 runtime receipt shape draft without executing new forward, decode, generation, sampling, token selection, candidate creation, review insertion, commit, runtime apply, training, backward, or weight commit.

## Required acceptance criteria

```text
total_cases >= 34
accepted_cases >= 4
blocked_cases >= 30
expectation_mismatched_cases == 0
bind_accepted_count >= 4
logits_shape_bound_count >= 4
logits_finite_verified_count >= 4
logits_digest_bound_count >= 4
runtime_identity_bound_count >= 4
no_new_forward == true
no_decode_executed == true
no_generation_executed == true
no_sampling_executed == true
no_token_selection_executed == true
no_selected_token == true
no_decoded_text == true
no_candidate_text == true
no_candidate_envelope_finalized == true
no_review_queue_inserted == true
no_auto_accept_executed == true
no_auto_commit_executed == true
no_target_mutation_executed == true
no_runtime_apply_executed == true
no_training_executed == true
no_backward_executed == true
no_weight_commit_executed == true
acceptance_pass == true
```

## Static evidence

- Module exists: yes
- CLI exists: yes
- `lib.rs` export exists: yes
- Positive cases: 4
- Negative cases: 30
- Total cases: 34
- Brace balance: 0
- Required block variants present: yes
- Output paths present: yes

## Local run command

```bash
cargo run -p ash_core --bin ash_word_context_rt_forward_output_shape_bind
```

Expected summary path:

```text
workspace/word_context_probe/wctx_rt_01_forward_output_shape_bind_summary.json
```
