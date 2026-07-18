# ASH-TCU-DECODE-04-R4-R3-R1
# Stateful Fragment Staging / SentencePiece Context Ownership Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R3-R1_STATEFUL_FRAGMENT_STAGING_SENTENCEPIECE_CONTEXT_OWNERSHIP_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R3_LIVE_SELECTED_TOKEN_DECODE_SURFACE_SHADOW_SPLICE_LEGACY_OUTPUT_AUTHORITY_PRESERVATION_GATE`
- Runtime mode: `live_shadow_stateful_fragment_staging_compare_only`
- Private shadow-state mutation authority: `true`
- Production DecodeState/KV/output authority: `false`
- Legacy output authority: `exclusive`
- PASS authorizes: `ASH-TCU-DECODE-04-R4-R3-R2_BYTE_FRAGMENT_CARRY_UTF8_ASSEMBLY_NO_REPLACEMENT_FALLBACK_SEAL`
- R4-R4 and production apply: `false`

## 1. Purpose

R4-R3 proves one canonical selected-token shadow splice beside the authoritative legacy decoder. R4-R3-R1 adds one generation-scoped TensorCube fragment-staging owner that chooses the valid R4-R2 projection for the current SentencePiece boundary, accumulates private raw shadow text, and compares it with an independent tokenizer-core raw-sequence oracle.

The owner may mutate only its private state. It may not append production tokens, mutate KV, emit text or stream chunks, advance sampler/RNG, execute finish/stop, or replace legacy output.

## 2. Concrete SSOT

Implementation ownership is:

```text
model_core::R4R3R1FragmentStagingState
model_core::R4R3R1SentencePieceContext
model_core::classify_r4r3_r1_context
model_core::stage_r4r3_r1_fragment_transaction
tokenizer_core::decode_manifest_token_sequence_raw
model_core::append_legacy_fragment_with_r4r3_shadow
GenerationTelemetry::tensorcube_r4_r3_r1_fragment_stage
```

The live helper calls the legacy `append_token_piece_to_text` first. The exact legacy fragment remains the only production fragment. The R4-R3 and R4-R3-R1 observers receive immutable surface/fragment observations afterward.

## 3. State ownership

Exactly one `R4R3R1FragmentStagingState` is initialized per production generation epoch and passed through all selected-token materialization calls.

Forbidden:

- state per token
- state per route adapter
- state per stream flush
- global mutable singleton
- state shared across generation epochs
- reconstruction from legacy output on every step
- storage inside production `DecodeState` or `KvCache`

Owner identity binds:

```text
parent R4-R3 execution ID
+ generation epoch
+ tokenizer exact identity
+ state schema
+ initial prefix digest
```

Every receipt must preserve the same owner ID and generation epoch. Step indices and state revisions are monotonic and contiguous for committed steps.

## 4. SentencePiece context SSOT

A binary `at_text_start` flag is insufficient. The state owns five contexts:

```rust
pub enum R4R3R1SentencePieceContext {
    TextStart,
    AfterNonWhitespace,
    AfterAsciiSpace,
    AfterLineBreak,
    AfterOtherWhitespace,
}
```

Required behavior:

```text
""     + ▁hello -> "hello"
"A"    + ▁hello -> "A hello"
"A "   + ▁hello -> "A hello"
"A\n"  + ▁hello -> "A\nhello"
"A\t"  + ▁hello -> "A\t hello"
```

A line break is not document start. Existing ASCII space and line break suppress exactly one synthetic SentencePiece delimiter. Other whitespace follows legacy raw-decode behavior and receives the synthetic ASCII space.

Standalone `▁` behavior:

```text
TextStart / AfterAsciiSpace / AfterLineBreak -> empty fragment
AfterNonWhitespace / AfterOtherWhitespace   -> one ASCII space
```

Control tokens stage an empty fragment and do not flip context. Structural `<br>` stages one `\n` and transitions to `AfterLineBreak`.

No fragment trimming, whitespace collapse, Unicode normalization, cleanup decoding, or replacement-character repair is allowed.

## 5. State invariants

Required state fields include:

```text
parent_execution_id
tokenizer_identity
generation_epoch
owner_id
state_revision
next_step_index
initial_prefix_len_bytes
initial_prefix_digest
raw_visible_text
raw_visible_len_bytes
rolling_visible_digest
context
last_selected_token_id
last_piece_kind
staged_fragment_count
suppressed_token_count
structural_line_break_count
pending_bytes
pending_byte_token_ids
```

Required invariants:

```text
raw_visible_len_bytes == raw_visible_text.as_bytes().len()
context == classify_r4r3_r1_context(raw_visible_text)
state_revision == next_step_index
pending_bytes.is_empty()
pending_byte_token_ids.is_empty()
```

The pending-byte fields are reserved for R4-R3-R2 and must remain empty in every R4-R3-R1 PASS artifact.

## 6. Transaction contract

Every selected token executes:

```text
validate owner / epoch / step / token binding
capture pre-state and digest
resolve start, continuation, control, line-break, or HOLD decision
build candidate private state
validate candidate
commit atomically or rollback exactly
write immutable step receipt
```

Committed steps increment revision and next-step index exactly once. HOLD does not partially mutate the state.

The step receipt records token ID, surface digest, raw-piece digest, piece kind, context before/after, decision, staged fragment and digest, pre/post revisions and state digests, commit/rollback status, HOLD reason, legacy-fragment comparison class, and production mutation count.

## 7. Byte-fragment boundary

R4-R3-R1 does not own byte carry or UTF-8 assembly. A byte fragment or invalid/unmaterialized surface produces typed HOLD:

```text
committed=false
rollback_performed=true
pending_bytes=[]
pending_byte_token_ids=[]
replacement fallback count=0
R4-R3-R2 authorization for that fixture=false
```

### Live HOLD containment

A typed HOLD must not abort or rewrite legacy generation. After its receipt is recorded:

```text
private fragment state -> exact rollback
current generation R4-R3-R1 owner -> disabled
legacy decoder/output/stream/KV/sampler/RNG -> continue unchanged
```

The generation-scoped `Option<R4R3R1FragmentStagingState>` may become `None` after receipt recording. This is not a state commit and does not authorize byte carry. Continuing TensorCube staging after the gap is forbidden until R4-R3-R2 owns carry.

## 8. Raw sequence oracle

`tokenizer_core::decode_manifest_token_sequence_raw` is independent of the incremental context owner and must:

- resolve exact manifest token pieces
- preserve raw UTF-8 bytes
- apply the same raw SentencePiece boundary rule
- suppress control tokens
- materialize `<br>` as one newline
- return typed HOLD before a byte piece mutates output
- perform no cleanup, normalization, whitespace collapse, lossy conversion, or byte assembly

Required lengths:

```text
1, 2, 8, 32, 128, 512 selected tokens
```

For every admitted sequence:

```text
per-step staged fragments == oracle fragments
final raw shadow bytes == oracle raw bytes
control count parity=true
line-break count parity=true
final context parity=true
pending byte state empty=true
```

## 9. Hot-path route matrix

All eight materialization calls share the same generation owner and helper:

| Route | First token | Loop token |
|---|---:|---:|
| sampled cached | required | required |
| sampled streaming | required | required |
| greedy cached | required | required |
| greedy streaming | required | required |

Required static truth:

```text
route coverage=4/4
hot-path helper call sites=8
state-owner pass-through count=8
canonical context resolver count=1
canonical state transaction count=1
route-local state-machine count=0
bypass route count=0
hard-coded generation_epoch: 1 count=0
```

Streaming routes may forward only the fragment returned by the legacy append function.

## 10. Live activation seals

Live generation uses:

```text
ASH_TCU_DECODE04_R4_R3_SHADOW=1
ASH_TCU_DECODE04_R4_R3_R1_STAGING=1
ASH_TCU_DECODE04_R4_R3_R1_PARENT_EXECUTION_ID=<exact R4-R3 execution ID>
```

When staging is absent, legacy generation and the existing R4-R3 observer remain unchanged.

## 11. Parent admission

Input:

```text
--repo-root <PATH>
--r4-r3-parent-manifest <PATH>
```

The parent must be exact R4-R3 PASS, have `all_truth_checks_pass=true`, authorize R4-R3-R1, forbid R4-R4 and production apply, prove one canonical shadow splice, prove four-route coverage, prove legacy exclusive output authority, prove shadow on/off output and production-state parity, contain zero unexpected mismatches, reproduce its stable execution ID, and bind the exact tokenizer manifest SHA.

## 12. Capability boundary

Allowed mutable capability:

```text
one private R4R3R1FragmentStagingState owner
```

Forbidden capability counts must all be zero:

```text
production DecodeState mutable handle
production KV mutable handle
production output or stream sink handle
sampler or RNG handle
GPU queue or command encoder
finish/stop mutation handle
route-switch handle
production transaction handle
```

Production token, KV, text, stream, finish, sampler, RNG, and route mutation-attempt counters must all be zero.

## 13. Rust-owned artifacts

The Rust binary alone writes atomically:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_state_ownership_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_initial_state_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_fragment_stage_steps_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_final_state_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_context_transition_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_raw_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_non_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r1_byte_fragment_hold_fixture_receipt_latest.json
```

The local manifest is written last. Parent and tokenizer inputs may not overlap any output. Generated evidence is not baked into source archives.

## 14. Binary and CLI seals

Binary:

```text
ash_tcu_decode_04_r4_r3_r1_stateful_fragment_staging_sentencepiece_context_ownership_gate
```

Required seals:

```text
--activate-stateful-fragment-staging
--activate-sentencepiece-context-ownership
--activate-raw-sequence-oracle-parity
--activate-shadow-state-transaction-audit
--require-parent-r4-r3-pass
--require-parent-r4-r3-r1-authorization
--require-parent-legacy-exclusive-output-authority
--require-parent-single-canonical-shadow-splice
--require-parent-shadow-on-off-production-parity
--require-single-generation-scoped-state-owner
--require-generation-epoch-binding
--require-owner-id-stability
--require-monotonic-step-index
--require-atomic-shadow-state-transaction
--require-state-rollback-on-hold
--require-text-start-context
--require-after-non-whitespace-context
--require-after-ascii-space-context
--require-after-line-break-context
--require-after-other-whitespace-context
--require-start-continuation-projection-selection
--require-no-duplicate-sentencepiece-delimiter
--require-standalone-marker-context-parity
--require-control-no-context-flip
--require-structural-line-break-transition
--require-no-fragment-trim
--require-no-whitespace-collapse
--require-no-unicode-normalization
--require-raw-oracle-no-cleanup
--require-per-step-fragment-oracle-parity
--require-final-raw-text-byte-parity
--require-control-count-parity
--require-line-break-count-parity
--require-final-context-parity
--require-byte-fragment-typed-hold
--require-byte-carry-disabled
--require-no-replacement-character-fallback
--require-empty-pending-byte-state-on-pass
--require-sampled-cached-route
--require-sampled-streaming-route
--require-greedy-cached-route
--require-greedy-streaming-route
--require-single-canonical-context-resolver
--require-no-route-local-state-machine
--require-legacy-exclusive-output-authority
--require-no-production-decodestate-mutation
--require-no-production-kv-mutation
--require-no-production-token-append
--require-no-production-text-emit
--require-no-production-stream-emit
--require-no-production-finish-stop-mutation
--require-no-production-sampler-use
--require-no-production-rng-use
--require-no-production-route-change
--write-runtime-artifacts
--write-local-manifest
```

## 15. Execution identity

Execution ID is:

```text
decode04r4r3r1-<first 20 hex of lineage_bundle_digest>
```

The stable lineage binds parent execution/lineage, tokenizer exact identity, owner and snapshots, step receipts, context coverage, raw-oracle parity, route/static coverage, capability inventory, non-production mutation audit, byte-HOLD fixture, and route digest. Paths, timestamps, timings, pointer values, and process data are excluded.

## 16. PASS, HOLD, FAIL

PASS marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R3_R1_STATEFUL_FRAGMENT_STAGING_SENTENCEPIECE_CONTEXT_OWNERSHIP_GATE
```

PASS requires one owner, exact epoch and monotonic steps, five-context coverage, four-route/eight-call coverage, one resolver and transaction, raw incremental/oracle parity through 512 steps, exact typed-HOLD rollback, empty pending-byte state, zero forbidden capabilities, zero production mutation attempts, and `all_truth_checks_pass=true`.

HOLD covers unavailable/stale parent or tokenizer evidence, missing deterministic fixtures, byte carry not yet authorized, or classifiable evidence gaps with production unchanged. FAIL covers owner duplication, epoch or token divergence, partial transaction, route bypass, context/oracle divergence, replacement fallback, capability leakage, production-state change, or silent fallback.

PASS grants only:

```text
decode04_r4_r3_r2_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/text/stream/finish authority=false
```

## 17. Next gate

`ASH-TCU-DECODE-04-R4-R3-R2 Byte Fragment Carry / UTF-8 Assembly / No Replacement Fallback Seal` may activate pending-byte ownership while preserving this gate's generation owner, transaction rollback, raw-oracle contract, and exclusive legacy output authority.