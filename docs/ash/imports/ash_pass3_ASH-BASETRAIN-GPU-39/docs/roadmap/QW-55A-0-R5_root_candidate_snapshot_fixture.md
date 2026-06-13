# QW-55A-0-R5 — Root Candidate Snapshot Fixture / No Logits Runtime Bind Seal

## 확정

R5는 QW-55A가 이후 평가할 root candidate snapshot fixture를 model_core 안에 생성한다.
실제 runtime logits, sampler state, generation_sampling.rs, infer_only CLI, runtime_profile.toml에는 bind하지 않는다.

## 상태 귀속 위치

- `crates/model_core/src/qw55a_root_candidate_fixture.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/tests/qw55a0_r5_root_candidate_snapshot_fixture.rs`

## SSOT

- QW-55A deterministic root candidate snapshot fixture
- No logits runtime bind seal

## 금지

- runtime logits 접근 금지
- sampler state 접근 금지
- generation_sampling.rs bind 금지
- infer_only CLI enable 금지
- runtime_profile.toml enable 금지
- actual tokenizer / vocab / lm_head 접근 금지
- selector result / root winner / selected token 생성 금지
- decode final commit 변경 금지
- greedy final authority 변경 금지

## Acceptance

- candidate_count = 16
- root_rank = 0..15
- root_token_id unique
- generated_from_runtime_logits = false
- generated_from_sampler_state = false
- generated_from_generation_sampling = false
- no_logits_runtime_bind = true
- no_sampler_runtime_bind = true
- no_generation_sampling_bind = true
- selector_result_created = false
- root_winner_created = false
- selected_token_id = None
- decode_mutation = false
- greedy_final_authority_changed = false

## 다음

QW-55A-0-R6 — Root Candidate Feature Projection / No Aggregate Winner Seal
