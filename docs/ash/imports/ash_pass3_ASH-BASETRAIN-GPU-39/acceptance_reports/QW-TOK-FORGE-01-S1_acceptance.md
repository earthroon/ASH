# QW-TOK-FORGE-01-S1 Acceptance

## 확정

S1 베이크는 다음 파일을 포함한다.

- `crates/model_core/src/tokenizer_v5_forge01_embed_lmhead_bootstrap.rs`
- `crates/model_core/src/bin/qw_tok_forge01_embed_lmhead_bootstrap.rs`
- `specs/QW-TOK-FORGE-01-S1_genesis_checkpoint_preflight_forge00_hash_gate_seal.md`
- `README_QW_TOK_FORGE_01_S1_BAKED.md`
- S1 receipt scaffold 6종

## Acceptance checklist

- [x] `--preflight-forge00` CLI flag added
- [x] FORGE-00 path guard retained
- [x] legacy TRAIN path guard retained
- [x] streaming full sha256 function added
- [x] safetensors header length reader added
- [x] header sha256 calculation added
- [x] payload sha256 streaming calculation added
- [x] safetensors header JSON parser added
- [x] embedding/lm_head key/shape checker added
- [x] model_spec/tokenizer vocab checker added
- [x] no mutation receipt added
- [x] checkpoint write remains disabled
- [x] training/forward/backward/optimizer/GPU/decode remains disabled

## 판단불가

`ash_v5_native_genesis.forge00.safetensors`는 이 zip에 포함되어 있지 않으므로, 현재 베이크 환경에서는 실제 4.6GB checkpoint hash PASS를 실행하지 않았다. 로컬 프로젝트 루트에서 CLI를 실행하면 S1 runtime receipt가 생성된다.
