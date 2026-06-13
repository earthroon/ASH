# 16AI-QW-38G-R6A-DECODE-03B Report

## Patch

Path Confidence Index / PCI Receipt Seal

## SSOT

- Input SSOT: `16AI-QW-38G-R6A-DECODE-03A` entropy/confidence metric receipt
- Runtime hook: `sampler_parity::append_receipt()` -> `decode03b_pci::append_decode03b_receipt_from_sampler03()`
- Behavior contract: `behavior_change=false`

## Implemented files

- `crates/model_core/src/decode03b_pci.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/decode03b_pci_receipt_schema.json`
- `workspace/decode03b_pci_steps.jsonl`
- `workspace/decode03b_summary.json`
- `workspace/decode03b_static_checks.json`
- `workspace/decode03b_probe_prompts.jsonl`
- `acceptance_reports/16AI-QW-38G-R6A-DECODE-03B_acceptance.md`

## PCI components

- entropy component
- top1/top2 margin component
- selected-rank component
- selected-logprob component
- active-set health component
- fallback penalty
- DECODE-03A risk penalty

## Hard caps

- `nan_seen || inf_seen` -> PCI = 0.0
- `empty_active_set_seen` -> PCI <= 0.20
- `global_finite_fallback_seen` -> PCI <= 0.35
- `guard_entropy_inversion && selected_rank > 5` -> PCI <= 0.45
- `min_p_overcompression && active_count_final <= 2` -> PCI <= 0.50

## Runtime flags

```bash
ASH_SAMPLER_PARITY=probe \
ASH_SAMPLER05_PARITY=receipt \
ASH_DECODE03A_ENTROPY=receipt \
ASH_DECODE03B_PCI=receipt \
ASH_DECODE03B_REQUIRE_DECODE03A=true \
ASH_DECODE03B_ENABLE_HYSTERESIS=true \
ASH_DECODE03B_RECEIPT=workspace/decode03b_pci_steps.jsonl \
ASH_DECODE03B_SUMMARY=workspace/decode03b_summary.json
```

## Static result

`workspace/decode03b_static_checks.json` reports `PASS_STATIC`.

## Execution status

- `cargo_check`: NOT_RUN
- `runtime_smoke`: NOT_RUN
- `decode replay`: NOT_RUN

This bake is static-defined only in the current environment.
