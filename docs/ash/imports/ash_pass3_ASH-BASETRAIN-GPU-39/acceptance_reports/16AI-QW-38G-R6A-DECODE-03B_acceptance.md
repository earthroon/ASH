# 16AI-QW-38G-R6A-DECODE-03B Acceptance

## Patch

Path Confidence Index / PCI Receipt Seal

## Acceptance status

STATIC_BAKE_DEFINED_NOT_RUN

## Confirmed by static checks

- `decode03b_pci.rs` exists.
- `lib.rs` registers and reexports the DECODE-03B API.
- `sampler_parity::append_receipt()` calls the DECODE-03B receipt hook.
- PCI computation clamps final PCI to `0.0..=1.0`.
- Hard caps exist for numeric risk, empty active set, and global finite fallback.
- `behavior_change=false` is written into the receipt.
- Static schema, empty JSONL receipt, summary, report, and probe prompts are included.

## Not run in this environment

- cargo check
- cargo test
- WGSL compile
- runtime smoke
- fixed prompt replay

## Promotion rule

DECODE-03C may consume DECODE-03B only after runtime receipt produces at least one `decode03b_pci_steps.jsonl` entry with `behavior_change=false` and no numeric risk.
