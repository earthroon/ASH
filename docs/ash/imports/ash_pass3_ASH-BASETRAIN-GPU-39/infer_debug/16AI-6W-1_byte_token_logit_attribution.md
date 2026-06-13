# 16AI-6W-1 Byte Token Logit Attribution Probe

## Status

PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION

## Scope

| field | value |
|---|---|
| target_text | `<0x63>` |
| top_k | 20 |
| generation | false |
| checkpoint_required | true |
| gpu_execution | false |
| global_default_commit | false |
| gpu_default | false |

## Summary

| field | value |
|---|---:|
| case_count | 2 |
| run_count | 4 |
| byte_top1_count | 4 |
| byte_near_tie_count | 0 |
| model_common_byte_bias_count | 2 |
| prompt_path_influenced_count | 0 |
| decoder_mapping_suspicious_count | 0 |

## Pair Table

| case | baseline_piece | v6_piece | same_selected | pair_decision |
|---|---|---|---:|---|
| ko_descriptive_sentence | `<0x63>` | `<0x63>` | true | ModelCommonByteBias |
| ko_particle_short | `<0x63>` | `<0x63>` | true | ModelCommonByteBias |

## Top-K Table

| case | mode | rank | token_id | piece | logit | byte_like |
|---|---|---:|---:|---|---:|---:|
| ko_descriptive_sentence | v5-baseline | 1 | 171 | `<0x63>` | 8.141459 | true |
| ko_descriptive_sentence | v5-baseline | 2 | 31123 | `▁양념치킨` | 6.875867 | false |
| ko_descriptive_sentence | v5-baseline | 3 | 31582 | `▁가려다가` | 6.253701 | false |
| ko_descriptive_sentence | v5-baseline | 4 | 1301 | `라도` | 6.138677 | false |
| ko_descriptive_sentence | v5-baseline | 5 | 22777 | `▁남도` | 6.087823 | false |
| ko_descriptive_sentence | v5-baseline | 6 | 19468 | `▁먹으` | 5.967691 | false |
| ko_descriptive_sentence | v5-baseline | 7 | 8228 | `▁피로` | 5.880944 | false |
| ko_descriptive_sentence | v5-baseline | 8 | 3915 | `었기` | 5.850627 | false |
| ko_descriptive_sentence | v5-baseline | 9 | 5105 | `▁재미로` | 5.722165 | false |
| ko_descriptive_sentence | v5-baseline | 10 | 28030 | `▁플래시` | 5.717849 | false |
| ko_descriptive_sentence | v5-baseline | 11 | 29529 | `▁황당했` | 5.707657 | false |
| ko_descriptive_sentence | v5-baseline | 12 | 4181 | `▁무서워` | 5.544105 | false |
| ko_descriptive_sentence | v5-baseline | 13 | 29876 | `▁들어봤어요` | 5.508636 | false |
| ko_descriptive_sentence | v5-baseline | 14 | 10881 | `었다면` | 5.327458 | false |
| ko_descriptive_sentence | v5-baseline | 15 | 20809 | `▁쓸고` | 5.248794 | false |
| ko_descriptive_sentence | v5-baseline | 16 | 28930 | `▁그때까지만` | 5.184422 | false |
| ko_descriptive_sentence | v5-baseline | 17 | 7172 | `▁이야기도` | 5.181967 | false |
| ko_descriptive_sentence | v5-baseline | 18 | 21829 | `▁장기로` | 5.131001 | false |
| ko_descriptive_sentence | v5-baseline | 19 | 655 | `이라는` | 5.118605 | false |
| ko_descriptive_sentence | v5-baseline | 20 | 25608 | `▁알바생이` | 5.086873 | false |
| ko_descriptive_sentence | v6-branch-local | 1 | 171 | `<0x63>` | 8.141459 | true |
| ko_descriptive_sentence | v6-branch-local | 2 | 31123 | `▁양념치킨` | 6.875867 | false |
| ko_descriptive_sentence | v6-branch-local | 3 | 31582 | `▁가려다가` | 6.253701 | false |
| ko_descriptive_sentence | v6-branch-local | 4 | 1301 | `라도` | 6.138677 | false |
| ko_descriptive_sentence | v6-branch-local | 5 | 22777 | `▁남도` | 6.087823 | false |
| ko_descriptive_sentence | v6-branch-local | 6 | 19468 | `▁먹으` | 5.967691 | false |
| ko_descriptive_sentence | v6-branch-local | 7 | 8228 | `▁피로` | 5.880944 | false |
| ko_descriptive_sentence | v6-branch-local | 8 | 3915 | `었기` | 5.850627 | false |
| ko_descriptive_sentence | v6-branch-local | 9 | 5105 | `▁재미로` | 5.722165 | false |
| ko_descriptive_sentence | v6-branch-local | 10 | 28030 | `▁플래시` | 5.717849 | false |
| ko_descriptive_sentence | v6-branch-local | 11 | 29529 | `▁황당했` | 5.707657 | false |
| ko_descriptive_sentence | v6-branch-local | 12 | 4181 | `▁무서워` | 5.544105 | false |
| ko_descriptive_sentence | v6-branch-local | 13 | 29876 | `▁들어봤어요` | 5.508636 | false |
| ko_descriptive_sentence | v6-branch-local | 14 | 10881 | `었다면` | 5.327458 | false |
| ko_descriptive_sentence | v6-branch-local | 15 | 20809 | `▁쓸고` | 5.248794 | false |
| ko_descriptive_sentence | v6-branch-local | 16 | 28930 | `▁그때까지만` | 5.184422 | false |
| ko_descriptive_sentence | v6-branch-local | 17 | 7172 | `▁이야기도` | 5.181967 | false |
| ko_descriptive_sentence | v6-branch-local | 18 | 21829 | `▁장기로` | 5.131001 | false |
| ko_descriptive_sentence | v6-branch-local | 19 | 655 | `이라는` | 5.118605 | false |
| ko_descriptive_sentence | v6-branch-local | 20 | 25608 | `▁알바생이` | 5.086873 | false |
| ko_particle_short | v5-baseline | 1 | 171 | `<0x63>` | 7.522536 | true |
| ko_particle_short | v5-baseline | 2 | 1301 | `라도` | 6.675454 | false |
| ko_particle_short | v5-baseline | 3 | 31582 | `▁가려다가` | 6.298357 | false |
| ko_particle_short | v5-baseline | 4 | 655 | `이라는` | 6.144827 | false |
| ko_particle_short | v5-baseline | 5 | 31123 | `▁양념치킨` | 5.999853 | false |
| ko_particle_short | v5-baseline | 6 | 29876 | `▁들어봤어요` | 5.984222 | false |
| ko_particle_short | v5-baseline | 7 | 138 | `<0x42>` | 5.701425 | true |
| ko_particle_short | v5-baseline | 8 | 4181 | `▁무서워` | 5.547632 | false |
| ko_particle_short | v5-baseline | 9 | 25608 | `▁알바생이` | 5.455833 | false |
| ko_particle_short | v5-baseline | 10 | 672 | `▁자기가` | 5.179546 | false |
| ko_particle_short | v5-baseline | 11 | 264 | `<0xC0>` | 5.084425 | true |
| ko_particle_short | v5-baseline | 12 | 19468 | `▁먹으` | 5.055264 | false |
| ko_particle_short | v5-baseline | 13 | 29989 | `▁종편` | 5.040774 | false |
| ko_particle_short | v5-baseline | 14 | 20809 | `▁쓸고` | 5.019851 | false |
| ko_particle_short | v5-baseline | 15 | 29529 | `▁황당했` | 4.993932 | false |
| ko_particle_short | v5-baseline | 16 | 29898 | `구의` | 4.990582 | false |
| ko_particle_short | v5-baseline | 17 | 3915 | `었기` | 4.962616 | false |
| ko_particle_short | v5-baseline | 18 | 8228 | `▁피로` | 4.928447 | false |
| ko_particle_short | v5-baseline | 19 | 5105 | `▁재미로` | 4.904747 | false |
| ko_particle_short | v5-baseline | 20 | 28930 | `▁그때까지만` | 4.805480 | false |
| ko_particle_short | v6-branch-local | 1 | 171 | `<0x63>` | 7.522536 | true |
| ko_particle_short | v6-branch-local | 2 | 1301 | `라도` | 6.675454 | false |
| ko_particle_short | v6-branch-local | 3 | 31582 | `▁가려다가` | 6.298357 | false |
| ko_particle_short | v6-branch-local | 4 | 655 | `이라는` | 6.144827 | false |
| ko_particle_short | v6-branch-local | 5 | 31123 | `▁양념치킨` | 5.999853 | false |
| ko_particle_short | v6-branch-local | 6 | 29876 | `▁들어봤어요` | 5.984222 | false |
| ko_particle_short | v6-branch-local | 7 | 138 | `<0x42>` | 5.701425 | true |
| ko_particle_short | v6-branch-local | 8 | 4181 | `▁무서워` | 5.547632 | false |
| ko_particle_short | v6-branch-local | 9 | 25608 | `▁알바생이` | 5.455833 | false |
| ko_particle_short | v6-branch-local | 10 | 672 | `▁자기가` | 5.179546 | false |
| ko_particle_short | v6-branch-local | 11 | 264 | `<0xC0>` | 5.084425 | true |
| ko_particle_short | v6-branch-local | 12 | 19468 | `▁먹으` | 5.055264 | false |
| ko_particle_short | v6-branch-local | 13 | 29989 | `▁종편` | 5.040774 | false |
| ko_particle_short | v6-branch-local | 14 | 20809 | `▁쓸고` | 5.019851 | false |
| ko_particle_short | v6-branch-local | 15 | 29529 | `▁황당했` | 4.993932 | false |
| ko_particle_short | v6-branch-local | 16 | 29898 | `구의` | 4.990582 | false |
| ko_particle_short | v6-branch-local | 17 | 3915 | `었기` | 4.962616 | false |
| ko_particle_short | v6-branch-local | 18 | 8228 | `▁피로` | 4.928447 | false |
| ko_particle_short | v6-branch-local | 19 | 5105 | `▁재미로` | 4.904747 | false |
| ko_particle_short | v6-branch-local | 20 | 28930 | `▁그때까지만` | 4.805480 | false |

## 확정

- source gates passed.
- selected token id / piece / top-k logits recorded.
- baseline and v6 branch-local paths compared.
- no tokenizer/vocab/checkpoint mutation performed.

## 판단불가

- RoPE/reference fidelity root cause.
- training/checkpoint root cause.
- GPU path behavior.
