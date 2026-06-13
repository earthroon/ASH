# 16AI-QW-38G-R6A-SALAD-01C-A — Generic Early EOS Collapse Guard / Receipt Always Write Seal

## 확정

- `crates/orchestrator_local/src/infer_entry.rs`에 01C-A를 적용했습니다.
- `[29871, 2]` 특정 패턴만 보던 흐름을 보강하여 `generated_tail_len <= 2`, `last_token == EOS`, `output_text_chars <= 8` 조건을 generic early EOS collapse로 감지합니다.
- SALAD receipt는 payload path와 canonical path(`workspace/salad01c_generation_receipt.json`) 양쪽을 지원하며, output JSON에도 `salad01c_receipt`를 삽입합니다.
- mojibake risk audit 필드를 추가했습니다.

## 추정

- `[29899, 2]`처럼 EOS 직전 토큰이 바뀐 collapse 변종도 retry 후보가 됩니다.
- receipt 파일 쓰기가 실패해도 output JSON 내부 receipt로 최소 증거를 남기도록 구성했습니다.

## 판단불가

- 이 베이크 환경에는 cargo가 없어 로컬 빌드/런타임 재생은 수행하지 못했습니다.
- 실제 retry가 collapse를 복구하는지는 선배 로컬에서 `cargo build` 후 재실행해야 판정 가능합니다.

## Mutation Flags

- checkpoint_modified = false
- tokenizer_modified = false
- safetensors_modified = false
- lm_head_modified = false
- final_norm_modified = false
- ban_mask_modified = false
