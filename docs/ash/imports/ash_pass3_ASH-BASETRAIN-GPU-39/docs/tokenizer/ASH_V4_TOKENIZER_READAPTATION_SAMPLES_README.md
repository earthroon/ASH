# ASH V4 Tokenizer Re-adaptation Samples

이 파일 묶음은 V4 tokenizer re-adaptation 1단계용 JSONL 샘플 20개입니다.

구성:
- persona_lock 5개
- guarded_freeform 5개
- subtitle_polish 5개
- structure_analysis 5개

목적:
- 새 reserved/control token을 실제 샘플 prefix로 반복 노출
- embed_tokens / lm_head 재적응
- identity / bridge / guard / style / signal 그룹의 행동 연결 강화

권장 사용:
- migrated V4 checkpoint seed
- embed/lm_head 높은 LR, body 낮은 LR
- V4 prefix가 포함된 샘플 비중을 높게 유지

파일:
- ash_v4_tokenizer_readaptation_samples_20.jsonl
