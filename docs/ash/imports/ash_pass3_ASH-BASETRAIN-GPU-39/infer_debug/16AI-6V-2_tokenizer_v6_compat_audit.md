# 16AI-6V-2 V6 Compat Audit Probe

## 1. Inputs

| field | value |
|---|---|
| v5_manifest | artifacts/tokenizer_manifest_v5_final.json |
| v6_manifest | artifacts/tokenizer_manifest_v6_compat.json |
| ssot_json | infer_debug/16AI-6V-0_tokenizer_v6_compat_ssot.json |
| manifest_run_json | infer_debug/16AI-6V-1_tokenizer_v6_compat_manifest.json |

## 2. Summary

| field | value |
|---|---:|
| total_checks | 61 |
| pass_count | 61 |
| warn_count | 0 |
| fail_count | 0 |
| blocking_fail_count | 0 |
| manifest_compatible | true |
| checkpoint_compatible | true |
| default_safe | true |
| gpu_safe_shadow_only | true |
| dpo_training_disabled | true |
| acceptance_status | PASS_TOKENIZER_V6_COMPAT_AUDIT |

## 3. Blocking Contract Checks

| check | field | expected | actual | status |
|---|---|---|---|---|
| FILE-01 | v5_manifest_exists | true | true | Pass |
| FILE-02 | v6_manifest_exists | true | true | Pass |
| ID-01 | manifest_kind | tokenizer_runtime_profile | tokenizer_runtime_profile | Pass |
| ID-02 | tokenizer_version | v6-compat | v6-compat | Pass |
| ID-04 | model_identity.model_identity | Ash 1.1B | Ash 1.1B | Pass |
| BASE-01 | base_tokenizer.base_tokenizer_version | v5 | v5 | Pass |
| BASE-02 | base_tokenizer.base_manifest | artifacts/tokenizer_manifest_v5_final.json | artifacts/tokenizer_manifest_v5_final.json | Pass |
| BASE-03 | base_tokenizer.base_vocab_size | 48259 | 48259 | Pass |
| BASE-04 | base_tokenizer.fallback_to_base | true | true | Pass |
| V5-01 | v5.trainer.vocab_size | 48259 | 48259 | Pass |
| COMPAT-01 | compatibility_contract.checkpoint_compatible | true | true | Pass |
| COMPAT-02 | compatibility_contract.vocab_size | 48259 | 48259 | Pass |
| COMPAT-03 | compatibility_contract.token_id_table_mutated | false | false | Pass |
| COMPAT-04 | compatibility_contract.new_token_ids_created | false | false | Pass |
| COMPAT-05 | compatibility_contract.vocab_augmented | false | false | Pass |
| COMPAT-06 | compatibility_contract.embedding_resize_required | false | false | Pass |
| COMPAT-07 | compatibility_contract.checkpoint_rewrite_required | false | false | Pass |
| DEFAULT-01 | runtime_defaults.default_mode | v5-baseline | v5-baseline | Pass |
| DEFAULT-02 | runtime_defaults.global_default_commit | false | false | Pass |
| DEFAULT-03 | runtime_defaults.fallback_to_v5 | true | true | Pass |
| DEFAULT-04 | runtime_defaults.cpu_fallback | true | true | Pass |
| DEFAULT-05 | runtime_defaults.gpu_default | false | false | Pass |
| MODE-01 | available_modes | contains v5-baseline | true | Pass |
| LAYER-03 | runtime_layers | contains existing_vocab_lookup_lattice | true | Pass |
| LAYER-04 | runtime_layers | contains dp_best_token_path_assembler | true | Pass |
| LAYER-05 | runtime_layers | contains quality_policy_gate | true | Pass |
| POLICY-04 | policy_scope.global_commit_supported | false | false | Pass |
| GPU-04 | gpu_contract.gpu_default | false | false | Pass |
| GPU-05 | gpu_contract.cpu_fallback | true | true | Pass |
| STATUS-01 | runtime_status_policy.pending_manifest_is_not_runtime_pass | true | true | Pass |
| STATUS-02 | runtime_status_policy.runtime_pass_required_for_execution_gates | true | true | Pass |
| STATUS-03 | runtime_status_policy.status_reader_must_distinguish_pending_and_pass | true | true | Pass |
| DPO-02 | dpo.training_enabled | false | false | Pass |
| DPO-03 | dpo.weights_mutated | false | false | Pass |
| DPO-04 | dpo.checkpoint_created | false | false | Pass |

## 4. Runtime Mode Checks

| check | expected | actual | status |
|---|---|---|---|
| MODE-01 | contains v5-baseline | true | Pass |
| MODE-02 | contains v6-shadow | true | Pass |
| MODE-03 | contains v6-branch-local | true | Pass |
| MODE-04 | contains v6-policy-gated | true | Pass |
| MODE-05 | contains v6-gpu-shadow | true | Pass |

## 5. Runtime Layer Checks

| check | expected | actual | status |
|---|---|---|---|
| LAYER-01 | contains protected_span_scanner | true | Pass |
| LAYER-02 | contains cheonjiin_structural_analyzer | true | Pass |
| LAYER-03 | contains existing_vocab_lookup_lattice | true | Pass |
| LAYER-04 | contains dp_best_token_path_assembler | true | Pass |
| LAYER-05 | contains quality_policy_gate | true | Pass |
| LAYER-06 | contains branch_local_commit_selector | true | Pass |
| LAYER-07 | contains gpu_shadow_backend_gate | true | Pass |

## 6. GPU Contract Checks

| check | field | expected | actual | status |
|---|---|---|---|---|
| GPU-01 | gpu_contract.gpu_shadow_supported | true | true | Pass |
| GPU-02 | gpu_contract.gpu_shadow_parity_1_verified | true | true | Pass |
| GPU-03 | gpu_contract.gpu_shadow_replay8_verified | true | true | Pass |
| GPU-04 | gpu_contract.gpu_default | false | false | Pass |
| GPU-05 | gpu_contract.cpu_fallback | true | true | Pass |
| GPU-06 | gpu_contract.max_verified_new_tokens | 8 | 8 | Pass |
| GPU-07 | gpu_contract.exact_parity_cases | 2 | 2 | Pass |

## 7. Runtime Status Policy Checks

| check | field | expected | actual | status |
|---|---|---|---|---|
| STATUS-01 | runtime_status_policy.pending_manifest_is_not_runtime_pass | true | true | Pass |
| STATUS-02 | runtime_status_policy.runtime_pass_required_for_execution_gates | true | true | Pass |
| STATUS-03 | runtime_status_policy.status_reader_must_distinguish_pending_and_pass | true | true | Pass |

## 8. 확정

- v6 manifest 호환성 audit 결과를 생성한다.
- vocab/checkpoint 불변 계약을 검사한다.
- default-off / gpu shadow-only / DPO training disabled 계약을 검사한다.

## 9. 추정

- blocking fail이 0이면 V3 encoder facade로 넘어갈 수 있다.

## 10. 판단불가

- v6 runtime encode 실제 동작은 아직 검증하지 않는다.
- generation 품질과 GPU 장기 안정성은 판단하지 않는다.
