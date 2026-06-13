들어간 것
- `crates/runtime/src/infer.rs`
- `crates/runtime/src/lib.rs`
- `docs/DECODE_OVERRIDE_CANDIDATE_POOL_PRIORITY5_PATCH.md`

핵심
- task별 candidate diversity policy를 runtime-level SSOT로 올림
- empty candidate plan일 때 단일 후보 대신 task-specific auto plan을 생성
- analysis / subtitle_polish / translation_assist / json_polish / default 프로필 분리

실제 효과
- analysis: 더 많은 후보, 더 높은 min_new_tokens, 더 넓은 temperature 분산
- subtitle_polish: 짧고 안정적인 후보군
- translation_assist: 중간 길이, 자연스러운 다양성
- json_polish: 보수적 decode

아직 아닌 것
- reranker trace에 diversity profile 노출은 아직 없음
- profile별 가중치 자동 튜닝은 아직 없음
