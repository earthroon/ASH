# 16AI-6E-R5 CJI Assembly Coverage Extraction Report

## 1. Model Identity SSOT

| field | value |
|---|---|
| model_identity | Ash 1.1B |
| spec_path_status | legacy_filename_not_model_size_ssot |
| source_gate | 16AI-6E-R4 PASS_DELTA_REPORT |
| input_json | `infer_debug/16AI-6E_dp_token_path_probe.json` |
| delta_json | `infer_debug/16AI-6E-R4_delta_summary.json` |

## 2. Scope

| field | value |
|---|---|
| coverage_mode | report_only |
| generation | false |
| token_ids_mutated | false |
| committed_prompt_ids | baseline |
| vocab_augmented | false |
| new_token_ids_created | false |

## 3. Coverage Summary

| field | value |
|---|---:|
| total_results | 21 |
| coverage_units | 60 |
| exact_covered_count | 0 |
| variant_covered_count | 54 |
| fallback_encoded_count | 0 |
| lookup_miss_count | 0 |
| unknown_used_count | 0 |
| protected_bypass_count | 6 |
| no_korean_span_count | 0 |
| coverage_score | 91.000 |
| merge_candidate_count | 13 |
| high_risk_candidate_count | 0 |
| critical_candidate_count | 0 |

## 4. Coverage Class Table

| class | count | ratio | meaning |
|---|---:|---:|---|
| ExactCovered | 0 | 0.000 | existing vocab direct hit |
| VariantCovered | 54 | 0.900 | boundary/normalized variant dependency |
| FallbackEncoded | 0 | 0.000 | native tokenizer fallback dependency |
| LookupMiss | 0 | 0.000 | no safe vocab path |
| UnknownUsed | 0 | 0.000 | unknown token risk |

## 5. Piece Coverage Table

| piece | class | variant | token_count | risk | case | wrapper |
|---|---|---|---:|---|---|---|
| `브라질` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | plain |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | plain |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | plain |
| `장점은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | plain |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | plain |
| `브라질` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | dialogue-ko |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | dialogue-ko |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | dialogue-ko |
| `장점은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | dialogue-ko |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | dialogue-ko |
| `브라질` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | instruction-ko |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | instruction-ko |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_beetle_question | instruction-ko |
| `장점은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | instruction-ko |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_beetle_question | instruction-ko |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | plain |
| `밥을` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | plain |
| `먹었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | plain |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | dialogue-ko |
| `밥을` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | dialogue-ko |
| `먹었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | dialogue-ko |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | instruction-ko |
| `밥을` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | instruction-ko |
| `먹었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_particle_short | instruction-ko |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_ending_question | plain |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_ending_question | dialogue-ko |
| `무엇인가요` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_ending_question | instruction-ko |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | plain |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | plain |
| `특징` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_compound_noun | plain |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | dialogue-ko |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | dialogue-ko |
| `특징` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_compound_noun | dialogue-ko |
| `장수풍뎅이` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | instruction-ko |
| `의` | VariantCovered | boundary_or_normalized_variant | 2 | Medium | ko_compound_noun | instruction-ko |
| `특징` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_compound_noun | instruction-ko |
| `검은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `창문` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `아래에` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `앉아` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `있었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | plain |
| `검은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `창문` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `아래에` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `앉아` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `있었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | dialogue-ko |
| `검은` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `고양이가` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `창문` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `아래에` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `앉아` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `있었다` | VariantCovered | boundary_or_normalized_variant | 1 | Medium | ko_descriptive_sentence | instruction-ko |
| `wrapper_user_label::plain` | ProtectedBypass | none | 0 | None | wrapper_user_label | plain |
| `wrapper_user_label::dialogue-ko` | ProtectedBypass | none | 0 | None | wrapper_user_label | dialogue-ko |
| `wrapper_user_label::instruction-ko` | ProtectedBypass | none | 0 | None | wrapper_user_label | instruction-ko |
| `wrapper_assistant_label::plain` | ProtectedBypass | none | 0 | None | wrapper_assistant_label | plain |
| `wrapper_assistant_label::dialogue-ko` | ProtectedBypass | none | 0 | None | wrapper_assistant_label | dialogue-ko |
| `wrapper_assistant_label::instruction-ko` | ProtectedBypass | none | 0 | None | wrapper_assistant_label | instruction-ko |

## 6. Merge Candidate Table

| candidate | pieces | frequency | current_vocab_hit | expected_token_reduction | risk |
|---|---|---:|---:|---:|---|
| `장수풍뎅이` | `장수\|풍뎅이` | 6 | true | 1 | Medium |
| `고양이가` | `고양\|이가` | 6 | true | 0 | Medium |
| `무엇인가요` | `무엇\|인가요` | 6 | true | 0 | Medium |
| `검은` | `검은` | 3 | true | 0 | Medium |
| `먹었다` | `먹\|었다` | 3 | true | 0 | Medium |
| `밥을` | `밥을` | 3 | true | 0 | Medium |
| `브라질` | `브\|라질` | 3 | true | 0 | Medium |
| `아래에` | `아\|래에` | 3 | true | 0 | Medium |
| `앉아` | `앉아` | 3 | true | 0 | Medium |
| `있었다` | `있\|었다` | 3 | true | 0 | Medium |
| `장점은` | `장\|점은` | 3 | true | 0 | Medium |
| `창문` | `창문` | 3 | true | 0 | Medium |
| `특징` | `특징` | 3 | true | 0 | Medium |

## 7. CJI Pattern Findings

| piece | syllables | batchim_pattern | cji_pattern | particle | ending | compound |
|---|---:|---|---|---:|---:|---:|
| `브라질` | 3 | `false,false,true` | `071200,050000,0C1408` | false | false | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `장점은` | 3 | `true,true,true` | `0C0015,0C0410,0B1204` | true | false | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `브라질` | 3 | `false,false,true` | `071200,050000,0C1408` | false | false | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `장점은` | 3 | `true,true,true` | `0C0015,0C0410,0B1204` | true | false | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `브라질` | 3 | `false,false,true` | `071200,050000,0C1408` | false | false | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `장점은` | 3 | `true,true,true` | `0C0015,0C0410,0B1204` | true | false | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `밥을` | 2 | `true,true` | `070011,0B1208` | true | false | false |
| `먹었다` | 3 | `true,true,false` | `060401,0B0414,030000` | false | true | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `밥을` | 2 | `true,true` | `070011,0B1208` | true | false | false |
| `먹었다` | 3 | `true,true,false` | `060401,0B0414,030000` | false | true | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `밥을` | 2 | `true,true` | `070011,0B1208` | true | false | false |
| `먹었다` | 3 | `true,true,false` | `060401,0B0414,030000` | false | true | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `무엇인가요` | 5 | `false,true,true,false,false` | `060D00,0B0413,0B1404,000000,0B0C00` | false | true | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `특징` | 2 | `true,true` | `101201,0C1415` | false | false | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `특징` | 2 | `true,true` | `101201,0C1415` | false | false | false |
| `장수풍뎅이` | 5 | `true,false,true,true,false` | `0C0015,090D00,110D15,030515,0B1400` | true | false | false |
| `의` | 1 | `false` | `0B1300` | true | false | false |
| `특징` | 2 | `true,true` | `101201,0C1415` | false | false | false |
| `검은` | 2 | `true,true` | `000410,0B1204` | true | false | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `창문` | 2 | `true,true` | `0E0015,060D04` | false | false | false |
| `아래에` | 3 | `false,false,false` | `0B0000,050100,0B0500` | true | false | false |
| `앉아` | 2 | `true,false` | `0B0005,0B0000` | false | false | false |
| `있었다` | 3 | `true,true,false` | `0B1414,0B0414,030000` | false | true | false |
| `검은` | 2 | `true,true` | `000410,0B1204` | true | false | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `창문` | 2 | `true,true` | `0E0015,060D04` | false | false | false |
| `아래에` | 3 | `false,false,false` | `0B0000,050100,0B0500` | true | false | false |
| `앉아` | 2 | `true,false` | `0B0005,0B0000` | false | false | false |
| `있었다` | 3 | `true,true,false` | `0B1414,0B0414,030000` | false | true | false |
| `검은` | 2 | `true,true` | `000410,0B1204` | true | false | false |
| `고양이가` | 4 | `false,true,false,false` | `000800,0B0215,0B1400,000000` | true | false | false |
| `창문` | 2 | `true,true` | `0E0015,060D04` | false | false | false |
| `아래에` | 3 | `false,false,false` | `0B0000,050100,0B0500` | true | false | false |
| `앉아` | 2 | `true,false` | `0B0005,0B0000` | false | false | false |
| `있었다` | 3 | `true,true,false` | `0B1414,0B0414,030000` | false | true | false |

## 8. 확정

- Existing vocab coverage classes were extracted from 16AI-6E best paths.
- ExactCovered / VariantCovered / FallbackEncoded / LookupMiss / UnknownUsed are separated.
- No new token ids were created.
- vocab_augmented=false and generation=false are preserved.

## 9. 추정

- VariantCovered and FallbackEncoded pieces are candidates for future tokenizer enhancement.
- Merge candidates are CJI-aware BPE research inputs, not applied vocab changes.

## 10. 판단불가

- Generation quality improvement.
- Assembled ids commit safety.
- Actual CJI-aware BPE training effect.
- Local Syllable Fusion effect.
