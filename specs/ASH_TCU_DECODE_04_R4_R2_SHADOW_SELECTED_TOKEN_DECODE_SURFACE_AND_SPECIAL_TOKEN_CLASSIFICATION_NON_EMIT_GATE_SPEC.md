# ASH-TCU-DECODE-04-R4-R2

## SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE

```text
patch_id=ASH-TCU-DECODE-04-R4-R2_SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE
parent_status=PASS_ASH_TCU_DECODE_04_R4_R1_TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
production_authority=false
runtime_mode=artifact_only_tokenizer_shadow_decode
```

## Runtime boundary

R4-R2 consumes only immutable R4-R1 artifacts and the frozen tokenizer-v5 manifest.

```text
checkpoint_open_count=0
checkpoint_range_read_count=0
gpu_dispatch_count=0
production_sampler_use_count=0
production_rng_read_count=0
```

Required parent artifacts:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_selection_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_non_commit_audit_latest.json
```

Required tokenizer artifact:

```text
tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json
vocab_size=48259
```

Missing or inconsistent inputs produce HOLD. Silent parent rerun, legacy-tokenizer fallback, token clamping and `<unk>` substitution are forbidden.

## Selection SSOT

The only token decoded by this stage is obtained from the verified R4-R1 selection receipt.

```text
selection_field=selected_token_id_draft
rank_field=selected_parent_rank
probability_field=selected_probability
commit_authorized=false
```

The implementation must not hard-code the token ID observed in a previous run.

## Tokenizer identity

The exact tokenizer manifest file bytes are hashed independently from the embedded manifest hash.

```text
manifest_parse_success=true
manifest_id_non_empty=true
tokenizer_spec_id_non_empty=true
file_sha256_recorded=true
embedded_hash_recorded_separately=true
manifest_rewrite_count=0
```

## Logical token ownership

Exact ID lookup scans both physical domains:

```text
manifest.vocab
manifest.reserved_tokens
```

The tokenizer-v5 manifest intentionally mirrors reserved tokens across the two domains:

```text
vocab:            id=X token=T is_reserved=true
reserved_tokens:  id=X token=T group=G
```

An exact one-to-one mirror pair is one logical mapping, not a collision.

```text
logical_mapping_count=1
physical_occurrence_count=2
owner_domain=canonical_reserved_mirror_pair
canonical_mirror_pair=true
```

A normal non-reserved vocabulary entry has one physical occurrence.

The mirror collapses only when ID and token string agree, the vocabulary entry carries `is_reserved=true`, and each domain contributes exactly one record. Any other repeated ID produces HOLD.

```text
selected_token_mapping_count=1
selected_token_collision_count=0
arbitrary_owner_selected=false
```

## Decode surface

```text
selected token ID
-> exact raw piece
-> piece kind
-> special-token class
-> start-context fragment
-> continuation-context fragment
```

The bounded receipt-local surface contains one selected token only.

```text
selected_token_count=1
max_raw_piece_bytes=4096
max_start_fragment_bytes=4096
max_continuation_fragment_bytes=4096
full_vocab_decode_surface_count=0
```

Canonical piece kinds:

```text
plain_text
sentence_piece_text
byte_fragment
structural_line_break
control
unknown
invalid_utf8
```

Canonical special classes:

```text
not_special
core_pad
core_bos
core_eos
core_unk
reserved_task
reserved_language
reserved_glossary
reserved_translation_memory
reserved_cue_boundary
reserved_structural_line_break
reserved_control
reserved_other
byte_fragment
unknown_token_id
invalid_manifest_entry
```

## Context projection

SentencePiece spacing remains context-sensitive.

```text
raw_piece=U+2581foo
start_context_fragment=foo
continuation_context_fragment=" foo"
```

For standalone U+2581:

```text
start_context_fragment=null
continuation_context_fragment=" "
```

`<br>` is structural line break data:

```text
piece_kind=structural_line_break
special_class=reserved_structural_line_break
start_context_fragment="\n"
continuation_context_fragment="\n"
text_emit_attempt_count=0
```

An isolated `<byte:HH>` or `<0xHH>` piece remains pending and is not materialized as replacement-character text.

```text
piece_kind=byte_fragment
byte_fragment_pending=true
text_materialization_ready=false
suppressed_in_output=true
```

## Independent oracle

The primary adapter may use tokenizer-core decode SSOT after exact ownership validation. The oracle independently implements ID scanning, mirror normalization, classification, byte parsing and context projection.

Shared transform, classification, byte-parser and projection helpers are forbidden.

```text
raw_piece_mismatch_count=0
piece_kind_mismatch_count=0
special_class_mismatch_count=0
reserved_group_mismatch_count=0
start_context_fragment_mismatch_count=0
continuation_context_fragment_mismatch_count=0
byte_fragment_pending_mismatch_count=0
adapter_oracle_mismatch_count=0
```

## Fixture matrix

```text
F0 selected parent token
F1 core EOS
F2 structural line break
F3 manifest-backed SentencePiece token
F4 manifest-backed plain-text token
F5 manifest-backed byte token or NOT_APPLICABLE
F6 missing ID EXPECTED_HOLD
F7 duplicate logical owner EXPECTED_HOLD
```

F6 must prove no zero-token or `<unk>` fallback. F7 uses an in-memory manifest clone and must not alter the frozen tokenizer artifact.

## Non-emit firewall

The adapter receives no mutable DecodeState, token sequence, GenerationCursor, KV handle, stream sender, output buffer, production RNG, checkpoint handle or GPU handle.

```text
token_append_attempt_count=0
token_append_commit_count=0
kv_append_attempt_count=0
kv_append_commit_count=0
eos_transition_attempt_count=0
finish_reason_change_count=0
stop_state_change_count=0
text_emit_attempt_count=0
stream_emit_attempt_count=0
assistant_buffer_write_count=0
user_visible_output_write_count=0
runtime_route_change_count=0
runtime_output_changed=false
all_state_digest_match=true
all_state_unchanged=true
```

The only authorized writes are R4-R2 shadow artifacts.

## Memory and performance

```text
full_vocab_duplicate_map_count=0
full_vocab_decoded_string_vector_count=0
soft_peak_heap_bytes<=33554432
hard_peak_heap_bytes<=67108864
soft_total_runtime_target_ms=500
hard_total_runtime_ceiling_ms=1500
```

A single run remains provisional performance evidence.

## Artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_parent_selection_binding_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_tokenizer_identity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_selected_token_lookup_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_decode_surface_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_special_token_classification_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_fixture_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_non_emit_audit_latest.json
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R4_R2_SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R4_R2_SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R4_R2_SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE
PASS_VERDICT=decode04_r4_r2_shadow_selected_token_decode_surface_special_classification_non_emit_pass
```

PASS authorizes only `ASH-TCU-DECODE-04-R4-R3` shadow special-token policy decision and text-fragment staging non-commit work. It does not authorize token append, KV mutation, EOS/STOP execution, text emission, production tokenizer adoption, production route switching or DECODE-05 promotion.