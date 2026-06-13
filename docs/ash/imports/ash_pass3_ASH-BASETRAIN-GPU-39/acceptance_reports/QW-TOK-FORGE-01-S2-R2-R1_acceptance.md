# QW-TOK-FORGE-01-S2-R2-R1 Acceptance

## Status
PENDING_LOCAL_CARGO_BUILD

## Static checks performed in bake environment
- `as usize <` ambiguous pattern replaced in the two reported S2-R2 locations.
- Top-level runtime `artifacts/*.json` were not included in the baked zip.
- Patch is source-only and does not mutate checkpoint/corpus/candidate artifacts.

## Local command
```powershell
cargo build -p model_core --bin qw_tok_forge01_embed_lmhead_bootstrap
```
