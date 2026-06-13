# 16AI-QW-38G-R6A-DECODE-10 Bake Report

## Result

status: PASS_STATIC_SUBTITLE_SURFACE_RERANK_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
base: 16AI-QW-38G-R6A-DECODE-09 baked zip

## Added modules

- crates/ash_core/src/subtitle_surface_rerank_policy.rs
- crates/ash_core/src/subtitle_surface_metrics.rs
- crates/ash_core/src/subtitle_surface_penalty.rs
- crates/ash_core/src/subtitle_surface_selection.rs
- crates/ash_core/src/subtitle_surface_rerank_receipt.rs

## Runtime flags

- runtime_decode_executed_count: 0
- model_forward_executed_count: 0
- sampling_executed_count: 0
- qe_model_executed_count: 0

## Boundary

DECODE-10 selects by subtitle surface only. It does not run QE, COMET/xCOMET, source adequacy, glossary/TM, model forward, or real sampling.

## Canonical receipt keys

```txt
valid_surface: q4sha256:eefe2f57d0ab209b254f0761bd2716fb4965117c280565bc234e5d7387f9f452
orphan_particle: q4sha256:6880470c27f16c07bea6c1b6dd8b4013e9b58385b60f789c2826f4322a5835d9
cps_overflow: q4sha256:f1318d2be8465f64e5ea70fd69d187dc2f3078a0ff1dfba7ebbcb68efbaea9ae
pool_not_ready: q4sha256:f97eab1fcea156a2b2ac3fc5de8187e18708c7972b92115de9276408e8d167f7
all_rejected: q4sha256:e4fa32279e81fcd30ce888d825bf0b2aa16b56fcdc152f9b689fa4339036e052
```

## Compile note

Rust compile was not executed in this bake environment. The seal is static contract materialization.
