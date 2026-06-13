# QW-TOK-FORGE-01-S4-R1 Acceptance

## PASS

1. `--rebind-existing-candidate-evidence` 실행면이 존재한다.
2. S4-R1은 candidate를 write/rename/delete/overwrite하지 않는다.
3. S3 candidate receipt를 읽는다.
4. 실제 candidate file size와 S3 receipt size가 일치한다.
5. 실제 candidate SHA256과 S3 receipt SHA256이 일치한다.
6. candidate safetensors header parse가 성공한다.
7. embedding/lm_head shape가 `[48259, 2048]`이다.
8. forge00 대비 embedding hash가 변경되었다.
9. forge00 대비 lm_head hash가 변경되었다.
10. forbidden aggregate hash가 forge00/candidate 간 일치한다.
11. S4-R1 receipt 6종과 bake manifest를 생성한다.

## FAIL

1. candidate checkpoint 없음.
2. S3 candidate receipt 없음.
3. candidate SHA256 mismatch.
4. candidate size mismatch.
5. header parse 실패.
6. embedding/lm_head hash change 없음.
7. forbidden range hash mismatch.
8. forbidden range missing을 mismatch와 동시에 기록.
9. S4-R1에서 checkpoint write/rename/delete/overwrite 실행.
