# 16AI-QW-38G-R6A-R12A-R8A — Projection Removal Design Branch

## Status
STATIC_VALIDATION_PASS

## Purpose
R8에서 position55 단독 source mask가 weak/inconclusive로 닫힌 뒤, R7-R2의 intervention-axis top인 HEAD2_TARGET_DIRECTION_PROJECTION_REMOVAL을 별도 design branch로 재진입한다.

## Implemented
- native R8A env gate 추가
- head2 projected value를 lm_head[13]-lm_head[373] basis로 parallel/orthogonal 분해
- full removal / partial attenuation / norm-preserving attenuation / orthogonal-only profiles 작성
- R8A runner 추가
- projection profile scoreboard / output stability matrix / safe projection candidate writer 추가

## Guard
- checkpoint_modified=false
- tokenizer_modified=false
- safetensors_modified=false
- lm_head_modified=false
- final_norm_modified=false
- ban_mask_modified=false
- mutation_performed=false
