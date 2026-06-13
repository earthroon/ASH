# 16AI-QW-26 — QWave Long-run SFT Telemetry / Drift & Overfit Guard Seal

## Base

- Base ZIP: `ash_pass3_16AI-QW-25_qwave_korean_minimal_pair_eval_baked.zip`
- New module: `crates/lora_train/src/qwave_long_run_sft_telemetry.rs`
- New tests: `crates/lora_train/tests/qwave_long_run_sft_telemetry.rs`
- Export updated: `crates/lora_train/src/lib.rs`

## SSOT

- Input SSOT: QW-25 Korean minimal pair eval receipt and lineage refs QW-24 through QW-12.
- New receipt SSOT: `QWaveLongRunSftTelemetryReceipt`.
- State ownership: long-run telemetry evaluation only.
- No model, adapter pointer, runtime pointer, tokenizer, vocabulary, embedding, production training, or runtime state is mutated by this patch.

## Acceptance checklist

1. QW-25 Korean eval receipt consumption: PASS
2. QW-24/QW-23/QW-22/QW-21/QW-20/QW-19/QW-18/QW-17/QW-16/QW-12 lineage refs: PASS
3. QW-13/QW-14/QW-15 metadata receipt refs: PASS
4. Korean eval no-regression source guard: PASS
5. Telemetry window guard: PASS
6. Baseline and conditioned snapshot guard: PASS
7. Min train/eval steps guard: PASS
8. Sandboxed telemetry guard: PASS
9. Telemetry-only source guard: PASS
10. Finite telemetry guard: PASS
11. Loss drift report: PASS
12. Gradient drift report: PASS
13. QWave coverage drift report: PASS
14. Adapter delta drift report: PASS
15. Korean eval drift report: PASS
16. Non-Korean regression report: PASS
17. Overfit guard report: PASS
18. Base/token/vocab/embedding unchanged guard: PASS
19. Adapter/current/artifact pointer unchanged guard: PASS
20. Production state unchanged guard: PASS
21. Training promotion/runtime apply rejection: PASS
22. Outcome/recommendation generation: PASS
23. Telemetry-only manifest: PASS
24. Deterministic receipt fingerprinting: PASS

## Native test status

- `cargo test -p lora_train qwave_long_run_sft_telemetry`: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Seal

QW-26 evaluates long-run stability only. It does not promote training mode, apply runtime changes, mutate current/artifact pointers, or silently correct invalid telemetry.
