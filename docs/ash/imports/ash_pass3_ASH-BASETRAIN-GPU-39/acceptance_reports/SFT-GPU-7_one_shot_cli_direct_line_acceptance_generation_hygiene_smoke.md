# SFT-GPU-7 Acceptance

## Status

PENDING STATIC / RUNTIME REQUIRED

## Scope

one-shot CLI direct-line acceptance / generation hygiene smoke

## Required Contract

One command must verify:

- config strict contract
- lm_head module_lora target
- response-only shifted label mask
- GPU lm_head LoRA training smoke
- adapter manifest / safetensors artifact
- runtime load / logits delta
- deterministic generation hygiene
- final direct-line acceptance report

## Gates

- [ ] config contract pass
- [ ] SFT mask pass
- [ ] GPU training smoke pass
- [ ] artifact export/reload pass
- [ ] runtime delta pass
- [ ] generation hygiene pass
- [ ] `direct_line_acceptance.json` written
- [ ] `direct_line_acceptance.md` written

## Generation Hygiene Gates

- [ ] no replacement character
- [ ] no suspicious byte marker leakage
- [ ] no Hangul char-split pattern
- [ ] output is non-empty
- [ ] no severe repetition loop
- [ ] greedy/runtime generation smoke is deterministic by fixed seed
- [ ] runtime adapter sidecar is used

## Non-goals

- This commit does not judge literary quality.
- This commit does not score character voice.
- This commit does not require LoRA output to be better than base output.
