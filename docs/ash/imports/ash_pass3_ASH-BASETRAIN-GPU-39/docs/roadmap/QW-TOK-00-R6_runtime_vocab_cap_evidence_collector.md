# QW-TOK-00-R6 Runtime Vocab Cap Evidence Collector / Operator Path Probe Seal

## Purpose
Collect operator-path evidence for tokenizer/checkpoint/runtime vocab cap reconciliation against final vocab size `48259` and max token id `48258`.

## Scope
- Probe operator project root, tokenizer artifacts dir, artifacts dir, workspace dir.
- Read JSON/TOML metadata when provided.
- Parse safetensors index/header evidence without loading tensor bodies.
- Build `qw_tok00_r6_evidence_packet.json` as replay input for QW-TOK-00-R5.

## Hard bans
- No apply.
- No runtime spec write.
- No checkpoint manifest write.
- No model config write.
- No full weight tensor load.
- No embedding/lm_head resize.
- No tokenizer rewrite, vocab padding/truncation, token remap.
- No runtime decode, sampler, QW selector, or MCTS mutation.
