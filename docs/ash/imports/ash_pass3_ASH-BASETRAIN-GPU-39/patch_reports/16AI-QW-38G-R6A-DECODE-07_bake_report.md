# 16AI-QW-38G-R6A-DECODE-07 Bake Report

## Result

status: PASS_STATIC_KOREAN_MORPH_SALAD_OVERLAY_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine

## Added files

- `crates/ash_core/src/korean_morph_salad_policy.rs`
- `crates/ash_core/src/korean_morph_window.rs`
- `crates/ash_core/src/korean_morph_salad_overlay.rs`
- `crates/ash_core/src/korean_morph_salad_receipt.rs`

## Modified files

- `crates/ash_core/src/enko_decode_quality_receipt.rs`
- `crates/ash_core/src/lib.rs`

## Workspace artifacts

- `workspace/qw38g_r6a_decode07_korean_morph_salad_policy.json`
- `workspace/qw38g_r6a_decode07_korean_morph_*_fixture.json`
- `workspace/qw38g_r6a_decode07_korean_morph_windows.json`
- `workspace/qw38g_r6a_decode07_korean_morph_overlays.json`
- `workspace/qw38g_r6a_decode07_korean_morph_receipt.json`
- `workspace/qw38g_r6a_decode07_korean_morph_key_material.json`
- `workspace/qw38g_r6a_decode07_korean_morph_report.json`

## Counts

- morph_receipt_created_count: 6
- deterministic_key_created_count: 6
- strong_penalty_decision_count: 2
- recommend_rollback_decision_count: 2
- rollback_executed_count: 0
- production_default_apply: false

## Compile note

`cargo` / `rustc` are not available in the bake environment, so this is a static contract bake, not a Rust compile pass.
