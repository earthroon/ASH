# 16AI-6V-1 Tokenizer V6 Compat Manifest

## 1. Identity

| field | value |
|---|---|
| tokenizer_version | v6-compat |
| tokenizer_name | AshTokenizerV6Compat |
| model_identity | Ash 1.1B |
| base_tokenizer_version | v5 |
| base_manifest | artifacts/tokenizer_manifest_v5_final.json |
| vocab_size | 48259 |

## 2. Manifest Role

16AI-6V-1 creates the static runtime tokenizer profile manifest:

```txt
artifacts/tokenizer_manifest_v6_compat.json
```

This is not a new vocabulary declaration. It is a checkpoint-compatible runtime profile layered over tokenizer v5.

## 3. Compatibility Contract

| field | value |
|---|---:|
| checkpoint_compatible | true |
| token_id_table_mutated | false |
| new_token_ids_created | false |
| vocab_augmented | false |
| embedding_resize_required | false |
| checkpoint_rewrite_required | false |

## 4. Runtime Defaults

| field | value |
|---|---|
| default_mode | v5-baseline |
| fallback_to_v5 | true |
| global_default_commit | false |
| gpu_default | false |
| cpu_fallback | true |

## 5. Available Modes

- v5-baseline
- v6-shadow
- v6-branch-local
- v6-policy-gated
- v6-gpu-shadow

## 6. Runtime Layers

- protected_span_scanner
- cheonjiin_structural_analyzer
- existing_vocab_lookup_lattice
- dp_best_token_path_assembler
- quality_policy_gate
- branch_local_commit_selector
- gpu_shadow_backend_gate

## 7. Verified Gates

| gate | status |
|---|---|
| 16AI-6V-0 | PASS_TOKENIZER_V6_COMPAT_SSOT |
| 16AI-6E-R4 | PASS_DELTA_REPORT |
| 16AI-6E-R5 | PASS_COVERAGE_REPORT |
| 16AI-6F | PASS_COMMIT_GATE_COMPARE_ONLY |
| 16AI-6G | PASS_QUALITY_RECOMPARE |
| 16AI-6H-R2 | PASS_POLICY_QUALITY_INTEGRATED |
| 16AI-6I | PASS_GATED_COMMIT_PROBE |
| 16AI-6J | PASS_GPU_SHADOW_PARITY |
| 16AI-6J-R2 | PASS_GPU_SHADOW_REPLAY8 |

## 8. GPU Contract

| field | value |
|---|---:|
| gpu_shadow_supported | true |
| gpu_shadow_parity_1_verified | true |
| gpu_shadow_replay8_verified | true |
| gpu_default | false |
| cpu_fallback | true |
| max_verified_new_tokens | 8 |
| exact_parity_cases | 2 |

## 9. Runtime Status Policy

```txt
pending_manifest_is_not_runtime_pass=true
runtime_pass_required_for_execution_gates=true
status_reader_must_distinguish_pending_and_pass=true
```

## 10. 확정

- v6 compat manifest was created.
- v6 remains checkpoint-compatible with tokenizer v5 and Ash 1.1B.
- No vocab mutation, token id creation, embedding resize, checkpoint rewrite, or default runtime switch is introduced.
- GPU support is declared only as shadow-supported; gpu_default remains false.

## 11. 추정

- The manifest can be audited by 16AI-6V-2.
- The declared modes can be consumed later by a v6 encoder facade.
- DPO candidate export can be supported later without training in this commit.

## 12. 판단불가

- Whether the manifest loads correctly through future runtime facade code.
- Whether v6 should become the default tokenizer.
- Whether gpu_default can be enabled.
- Whether DPO training improves Ash 1.1B.
