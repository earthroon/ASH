# QW-TOK-00-R7 — Runtime Model Spec Reconciliation Replay / Evidence Packet Seal

## 확정
R6 evidence packet을 기존 R5 reconciliation builder에 다시 주입하여 runtime/model/checkpoint/tokenizer vocab cap 48259 대조를 replay한다.

## 상태 귀속 위치
- SSOT: `artifacts/qw_tok00_r6_evidence_packet.json`, R5 reconciliation builder
- 신규 구현: `crates/model_core/src/tokenizer_v5_reconciliation_replay.rs`
- 테스트: `qw_tok00_r7_reconciliation_replay`, `qw_tok00_r7_evidence_packet_schema`, `qw_tok00_r7_no_apply_no_mutation`, `qw_tok00_r7_replay_status_contract`

## SSOT 존재 여부
- R5 reconciliation engine: 존재
- R6 evidence packet: 존재하지만 로컬 evidence가 incomplete일 수 있음
- R7 replay seal: 이번 패치에서 추가

## 재현 가능성
```powershell
cargo check -p model_core --lib
cargo test -p model_core qw_tok00_r7 --test qw_tok00_r7_reconciliation_replay
cargo test -p model_core qw_tok00_r7 --test qw_tok00_r7_evidence_packet_schema
cargo test -p model_core qw_tok00_r7 --test qw_tok00_r7_no_apply_no_mutation
cargo test -p model_core qw_tok00_r7 --test qw_tok00_r7_replay_status_contract
```

## 금지
- R5 reconciliation logic 복제 금지
- runtime spec write / checkpoint manifest write / model config write 금지
- embedding/lm_head resize 금지
- tokenizer rewrite / vocab padding/truncation / token remap 금지
- runtime decode bind / sampler / QW selector / MCTS mutation 금지

## 판정
- R5 replay PASS -> R7 PASS
- R5 replay PENDING -> R7 PENDING
- R5 replay FAILED -> R7 FAILED
- invalid evidence packet -> R7 FAILED
- apply/mutation -> BLOCKED
