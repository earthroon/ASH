# 16AI-QW-38G-R6A-DECODE-03C Acceptance

## Patch

Dynamic Sampler Shadow Policy Seal

## Acceptance status

`STATIC_BAKE_DEFINED_NOT_RUN`

## Confirmed by static checks

- `decode03c_shadow_policy.rs` exists.
- `lib.rs` registers and reexports the DECODE-03C API.
- `sampler_parity::append_receipt()` calls the DECODE-03C receipt hook.
- Shadow policy calculation consumes DECODE-03B PCI receipt state.
- Shadow policy clamps `temperature`, `min_p`, and `top_p` to fixed safe ranges.
- `behavior_change=false` and `shadow_only=true` are written into the receipt.
- Summary keeps `ready_for_default_enable=false`.
- Static schema, empty JSONL receipt, summary, report, and probe prompts are included.

## Acceptance gates encoded

- PASS requires `behavior_change=false`.
- PASS requires `shadow_only=true`.
- PASS requires DECODE-03B PCI-derived input.
- FAIL if numeric risk does not force panic/safe-stop candidate behavior.
- FAIL if fallback risk does not mark rollback or safe-stop candidate behavior.
- FAIL if any shadow value leaves the configured clamp range.

## Not run in this environment

- cargo check
- cargo test
- WGSL compile
- runtime smoke
- fixed prompt replay

## Promotion rule

DECODE-03D may consume DECODE-03C only after runtime receipt produces at least one `decode03c_shadow_steps.jsonl` entry with `behavior_change=false`, `shadow_only=true`, and stable shadow policy summary evidence.

Default enable remains forbidden.
