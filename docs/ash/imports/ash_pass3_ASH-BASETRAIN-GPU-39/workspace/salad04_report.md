# 16AI-QW-38G-R6A-SALAD-04 — Korean Morph Loop Guard Seal

## Baked scope

- Added `crates/model_core/src/salad04_korean_morph_guard.rs`
- Registered `mod salad04_korean_morph_guard` in `model_core/src/lib.rs`
- Exported SALAD-04 public types and helpers from `model_core`
- Added `sampler_parity::append_receipt()` hook for SALAD-04 receipt generation
- Added workspace schema, empty JSONL receipt, summary, probe prompts, static checks, source hash manifest, and acceptance report

## Contract

```txt
behavior_change = false
guard_overlay_only = true
rollback_execution = false
stop_execution = false
no_morph_autocorrect = true
```

## Implemented guard overlay

SALAD-04 classifies lightweight Korean morph-risk pieces into:

```txt
HangulSyllable / HangulJamo / JosaLike / EomiLike / Punctuation / Whitespace / Symbol / BytePiece / Mixed / Unknown
```

It detects dominant loop kinds:

```txt
JosaRepeat / JosaChain / EomiRepeat / EomiPunctuationLoop / JamoLeak / ByteJamoMixedLeak / SyllableFragmentLoop / EojeolBoundaryCollapse / PunctuationGlueLoop / MixedMorphLoop
```

## Runtime flags

```bash
ASH_SALAD04_MODE=risk_overlay \
ASH_SALAD04_GUARD_OVERLAY_ONLY=true \
ASH_SALAD04_REQUIRE_SALAD02=true \
ASH_SALAD04_RECEIPT=workspace/salad04_steps.jsonl \
ASH_SALAD04_SUMMARY=workspace/salad04_summary.json
```

## Validation status

```txt
cargo_check: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
runtime_smoke: NOT_RUN
static_text_checks: PASS
```

## Next recommended patch

```txt
16AI-QW-38G-R6A-EVAL-00
Fixed Prompt Suite / Decode Regression Bench Seal
```
