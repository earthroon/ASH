# QW-54F Roadmap

QW-54F moves structural repeat-risk control from synthetic replay/evidence into the real native inference path.

## Implemented lane

1. CLI flag enables QW-54F.
2. `infer_only` sets explicit runtime env flags.
3. `decode_state` passes recent token context into model-core selection.
4. `generation_sampling` materializes the current candidate row and applies finite structural soft demotion.
5. Candidate telemetry records `rerank_delta`.
6. Trace/receipt/report are written for operator inspection.

## Not implemented in this patch

- Full WGSL structural risk compute inside the final selection kernel.
- Semantic piece-level Cheonjiin decomposition at selection time.
- Hard bans or token masks.

Those are intentionally excluded to preserve the no-hard-ban contract.
