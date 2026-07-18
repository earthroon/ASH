# ASH-TCU-DECODE-04-R4-R3-R2
# Byte Fragment Carry / UTF-8 Assembly / No Replacement Fallback Seal

- Patch ID: `ASH-TCU-DECODE-04-R4-R3-R2_BYTE_FRAGMENT_CARRY_UTF8_ASSEMBLY_NO_REPLACEMENT_FALLBACK_SEAL`
- Parent: `ASH-TCU-DECODE-04-R4-R3-R1_STATEFUL_FRAGMENT_STAGING_SENTENCEPIECE_CONTEXT_OWNERSHIP_GATE`
- Runtime mode: `live_shadow_stateful_byte_carry_compare_only`
- Private shadow-state mutation authority: `true`
- Production DecodeState/KV/output authority: `false`
- Legacy output authority: `exclusive`
- Replacement-character fallback: `forbidden`
- PASS authorizes: `ASH-TCU-DECODE-04-R4-R3-R3_STATEFUL_SHADOW_FRAGMENT_SEQUENCE_PARITY_AND_FLUSH_BOUNDARY_GATE`
- R4-R4 and production apply: `false`

## 1. Purpose

R4-R3-R2 activates the `pending_bytes` and `pending_byte_token_ids` fields reserved by R4-R3-R1. Byte pieces are accumulated only in the generation-scoped private shadow owner. A fragment becomes visible to the private shadow text only when the collected bytes are a complete, strictly valid UTF-8 scalar sequence.

Required outcomes:

```text
valid incomplete prefix -> private carry commit only
complete valid UTF-8 -> exact private fragment materialization
invalid UTF-8 -> exact rollback and typed HOLD/FAIL
terminal incomplete UTF-8 -> typed HOLD, no force flush
replacement fallback -> never
legacy production output -> unchanged
```

## 2. Concrete SSOT

```text
model_core::R4R3R1FragmentStagingState
model_core::R4R3R2ByteCarryReceipt
model_core::R4R3R2Utf8AssemblyDecision
model_core::R4R3R2Utf8AssemblyStatus
model_core::parse_r4r3_r2_manifest_byte_piece
model_core::validate_r4r3_r2_utf8_prefix
model_core::stage_r4r3_r2_byte_fragment_transaction
tokenizer_core::parse_manifest_byte_piece
tokenizer_core::decode_manifest_token_sequence_raw_with_byte_carry
model_core::append_legacy_fragment_with_r4r3_shadow
GenerationTelemetry::tensorcube_r4_r3_r2_byte_carry
```

There is one byte parser, one strict UTF-8 validator, and one byte transaction. Route adapters may not own byte buffers, UTF-8 decoders, classifiers, or repair policies.

## 3. Parent admission

Input:

```text
--repo-root <PATH>
--r4-r3-r1-parent-manifest <PATH>
```

The parent must be exact PASS and prove:

```text
all_truth_checks_pass=true
decode04_r4_r3_r2_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
single_generation_scoped_state_owner=true
per_step_fragment_oracle_parity=true
final_raw_text_byte_parity=true
legacy_exclusive_output_authority_proven=true
all_production_mutation_counts_zero=true
```

Parent execution identity must reproduce as:

```text
execution_id = "decode04r4r3r1-" + lineage_bundle_digest[0..20]
```

The exact parent manifest SHA, state owner ID, tokenizer path, tokenizer manifest SHA, and lineage digest are bound into R4-R3-R2.

## 4. State ownership

R4-R3-R2 extends the existing `R4R3R1FragmentStagingState`; it does not create a second owner.

Activated fields:

```text
pending_bytes: Vec<u8>
pending_byte_token_ids: Vec<u32>
```

Required invariants:

```text
owner count per generation epoch = 1
byte owner count per generation epoch = 1
R4-R3-R2 owner ID == R4-R3-R1 owner ID
pending_bytes.len == pending_byte_token_ids.len
pending_bytes.len <= 3 while incomplete
pending bytes form a valid incomplete UTF-8 prefix
cross-generation carry = forbidden
route-local carry = forbidden
global mutable carry singleton = forbidden
```

## 5. Byte-piece recognition

Only tokenizer-core canonical parsing may recognize byte pieces. Accepted canonical forms are the tokenizer manifest's exact byte syntax, including `<0xXX>` and the already-supported `<byte:XX>` representation.

Forbidden:

```text
arbitrary string first-byte extraction
permissive malformed hexadecimal parsing
unknown-token to UNK substitution
route-local parser
byte-piece spelling normalization
```

## 6. Strict UTF-8 status

The validator returns one typed status:

```text
empty
incomplete { expected_total_len, current_len }
complete { scalar_count, utf8_len }
invalid { error_offset, invalid_reason }
```

Invalid reasons include unexpected continuation, invalid leader, invalid continuation, overlong encoding, surrogate code point, non-shortest form, out-of-range code point, and prefix length overflow.

Required scalar rules:

```text
00..7F
C2..DF 80..BF
E0 A0..BF 80..BF
E1..EC 80..BF 80..BF
ED 80..9F 80..BF
EE..EF 80..BF 80..BF
F0 90..BF 80..BF 80..BF
F1..F3 80..BF 80..BF 80..BF
F4 80..8F 80..BF 80..BF
```

`C0/C1`, surrogate encodings, overlong forms, and code points above `U+10FFFF` are rejected.

Materialization policy is singular:

```text
utf8_materialization_policy=earliest_complete_scalar_sequence
```

## 7. Atomic byte transaction

Each selected token executes exactly one private-state transaction:

```text
validate parent/owner/epoch/step/token binding
capture pre-state and digest
resolve byte or non-byte path
append byte to candidate carry
strictly classify candidate prefix
construct candidate state
validate candidate invariants
compare with independent oracle
commit exactly once or rollback exactly
write immutable receipt
```

Decisions:

```text
non_byte_delegated_to_r4_r3_r1
byte_carry_started
byte_carry_extended
byte_sequence_materialized
byte_sequence_hold_incomplete_at_fixture_boundary
invalid_byte_sequence_hold
invalid_byte_sequence_fail
```

## 8. Incomplete carry

For a valid incomplete prefix:

```text
pending bytes and token IDs append exactly once
raw_visible_text unchanged
rolling visible digest unchanged
SentencePiece context unchanged
state revision += 1
next step index += 1
visible fragment = none
```

A following non-byte token may not skip, repair, prepend, or force-flush the carry. It produces typed HOLD, exact rollback, and generation-local shadow deactivation while legacy generation continues.

## 9. Complete materialization

For a complete valid scalar sequence:

```text
strict non-lossy UTF-8 decode
exact fragment bytes appended to private raw text
raw byte length and rolling digest updated
context derived from materialized text
pending bytes and IDs cleared
staged fragment count += 1
state revision and step index += 1
```

No normalization, trimming, whitespace collapse, case folding, newline rewrite, alternate charset conversion, or replacement insertion is allowed.

## 10. Replacement fallback prohibition

The byte path and oracle may not use:

```text
String::from_utf8_lossy
replacement-character insertion
invalid-byte dropping
invalid sequence truncation
unknown-token repair
silent byte substitution
```

Static and runtime audits must report:

```text
lossy_utf8_api_count=0
replacement_character_literal_count=0
invalid_byte_skip_path_count=0
silent_repair_path_count=0
runtime_replacement_fallback_count=0
```

## 11. Independent byte-aware oracle

`tokenizer_core::decode_manifest_token_sequence_raw_with_byte_carry` is independent of the model-core transaction. It resolves exact manifest pieces, performs strict carry and UTF-8 materialization, applies raw SentencePiece rules for non-byte tokens, and returns typed terminal incomplete or invalid evidence without cleanup or lossy conversion.

Required parity:

```text
incremental token ID == oracle token ID
incremental fragment bytes == oracle fragment bytes
incremental pending bytes == oracle pending bytes
incremental pending token IDs == oracle pending token IDs
incremental raw visible bytes == oracle raw bytes
final context parity=true
replacement fallback count=0
```

The first divergent step must be reported without summarizing it away.

## 12. Fixture coverage

Valid coverage includes ASCII, 2-byte, 3-byte, 4-byte, adjacent byte-built scalars, byte-built space, line break, tab, Hangul, and emoji. Sequence lengths include 1, 2, 3, 4, 8, 32, 128, and 512 selected tokens.

Invalid coverage includes:

```text
unexpected continuation byte
C0/C1 overlong leader
E0 overlong sequence
surrogate sequence
out-of-range F4 sequence
invalid F5 leader
invalid continuation
non-byte token during incomplete carry
terminal incomplete 2/3/4-byte sequence
```

Invalid deterministic fixtures must prove exact rollback and zero production mutation. Invalid canonical tokenizer streams are FAIL, not recoverable output.

## 13. Flush boundary

Generation end with empty carry is clean. Generation end with non-empty carry is:

```text
verdict=typed_hold_incomplete_utf8
force_flush_performed=false
replacement_fallback_count=0
production_output_delta=0
```

R4-R3-R2 does not define a production-facing incomplete-byte flush policy.

## 14. Live containment

On live typed HOLD:

```text
private candidate state -> exact rollback
R4-R3-R2/R4-R3-R1 owner for current generation -> disabled
legacy decoder/output/stream/KV/sampler/RNG -> continue unchanged
owner restart in same generation -> forbidden
```

This is shadow deactivation, not silent production fallback.

## 15. Hot-path routes

All eight selected-token materialization sites share the same owner and transaction:

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
canonical byte parser count=1
canonical UTF-8 validator count=1
canonical byte transaction count=1
route-local byte buffer count=0
route-local UTF-8 decoder count=0
bypass route count=0
```

Streaming may forward only the legacy fragment.

## 16. Live activation

```text
ASH_TCU_DECODE04_R4_R3_SHADOW=1
ASH_TCU_DECODE04_R4_R3_R1_STAGING=1
ASH_TCU_DECODE04_R4_R3_R1_PARENT_EXECUTION_ID=<exact R4-R3 execution ID>
ASH_TCU_DECODE04_R4_R3_R2_BYTE_CARRY=1
ASH_TCU_DECODE04_R4_R3_R2_PARENT_EXECUTION_ID=<exact R4-R3-R1 execution ID>
```

Absent R4-R3-R2 activation leaves R4-R3-R1 behavior unchanged; byte pieces remain typed HOLD.

## 17. Capability and production parity

Allowed mutable capability: one private generation-scoped fragment state owner including its pending-byte fields.

Forbidden capability counts are zero for production DecodeState, KV, output/stream sinks, sampler, RNG, GPU queue/encoder, finish/stop, route switch, and production transaction handles.

Shadow on/off must preserve selected tokens, legacy fragments, output bytes, stream chunks, DecodeState, KV owner, sampler, RNG, finish/stop, and runtime route.

TensorCube production mutation-attempt counters are all zero.

## 18. Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_state_extension_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_utf8_validator_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_byte_carry_steps_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_final_state_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_raw_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_invalid_utf8_fixture_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_terminal_incomplete_hold_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_shadow_on_off_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_non_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r2_no_replacement_fallback_audit_latest.json
```

Writes are atomic and the local manifest is written last. Parent, tokenizer, and production artifacts are read-only and disjoint from outputs. Generated evidence is excluded from source archives.

## 19. Binary and CLI seals

Binary:

```text
ash_tcu_decode_04_r4_r3_r2_byte_fragment_carry_utf8_assembly_no_replacement_fallback_seal
```

Required seals:

```text
--activate-byte-fragment-carry
--activate-strict-utf8-assembly
--activate-byte-aware-raw-oracle-parity
--activate-no-replacement-fallback-audit
--require-parent-r4-r3-r1-pass
--require-parent-r4-r3-r2-authorization
--require-parent-single-generation-state-owner
--require-parent-fragment-oracle-parity
--require-parent-legacy-exclusive-output-authority
--require-parent-zero-production-mutations
--require-shared-r4-r3-r1-state-owner
--require-owner-id-stability
--require-generation-epoch-binding
--require-monotonic-step-index
--require-atomic-byte-state-transaction
--require-exact-rollback-on-hold
--require-single-canonical-byte-parser
--require-single-canonical-utf8-validator
--require-single-canonical-byte-transaction
--require-no-route-local-byte-buffer
--require-no-route-local-utf8-decoder
--require-valid-incomplete-prefix-carry
--require-strict-complete-utf8-materialization
--require-earliest-complete-scalar-materialization
--require-pending-byte-token-id-parity
--require-pending-byte-length-bound
--require-no-nonbyte-crossing-incomplete-carry
--require-terminal-incomplete-byte-typed-hold
--require-no-overlong-utf8
--require-no-surrogate-codepoint
--require-no-out-of-range-codepoint
--require-no-invalid-continuation
--require-no-unexpected-continuation
--require-no-lossy-utf8-conversion
--require-no-replacement-character-fallback
--require-no-invalid-byte-skip
--require-no-silent-byte-repair
--require-per-step-byte-oracle-parity
--require-final-raw-text-byte-parity
--require-final-context-parity
--require-valid-fixture-coverage
--require-invalid-fixture-coverage
--require-byte-built-whitespace-context-coverage
--require-byte-built-linebreak-context-coverage
--require-byte-built-hangul-coverage
--require-byte-built-emoji-coverage
--require-sampled-cached-route
--require-sampled-streaming-route
--require-greedy-cached-route
--require-greedy-streaming-route
--require-eight-hot-path-call-sites
--require-legacy-exclusive-output-authority
--require-shadow-on-off-output-byte-parity
--require-shadow-on-off-stream-chunk-parity
--require-shadow-on-off-decodestate-parity
--require-shadow-on-off-kv-owner-parity
--require-shadow-on-off-sampler-parity
--require-shadow-on-off-rng-parity
--require-shadow-on-off-finish-stop-parity
--require-shadow-on-off-runtime-route-parity
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

## 20. Execution identity

```text
decode04r4r3r2-<first 20 hex of lineage_bundle_digest>
```

The stable lineage binds parent execution/lineage, parent owner, tokenizer exact identity, materialization policy, validator, valid and invalid fixtures, byte-step receipts, oracle parity, terminal HOLD, route coverage, capability inventory, production parity, non-mutation audit, no-replacement audit, and route digest. Paths, timestamps, durations, process data, and pointer values are excluded.

## 21. PASS/HOLD/FAIL

PASS marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R3_R2_BYTE_FRAGMENT_CARRY_UTF8_ASSEMBLY_NO_REPLACEMENT_FALLBACK_SEAL
```

PASS requires one shared owner, strict valid/incomplete/invalid classification, byte/token-ID parity, all valid and invalid fixture coverage, per-step oracle parity, final raw byte parity, terminal typed HOLD, zero lossy/replacement/skip/repair paths, four routes, eight hot-path calls, legacy-exclusive output authority, shadow on/off production parity, zero production mutations, and `all_truth_checks_pass=true`.

PASS grants only:

```text
decode04_r4_r3_r3_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/text/stream/finish authority=false
```

HOLD covers unavailable/stale evidence, incomplete terminal carry, non-byte crossing incomplete carry, or classifiable evidence gaps with production unchanged. FAIL covers invalid canonical streams, acceptance of malformed UTF-8, lossy/replacement behavior, carry divergence, partial transactions, owner duplication, route bypass, oracle divergence, legacy output mutation, production-state mutation, or silent repair.

## 22. Next gate

PASS authorizes only:

```text
ASH-TCU-DECODE-04-R4-R3-R3
Stateful Shadow Fragment Sequence Parity / Flush Boundary Gate
```

R4-R3-R3 may prove mixed normal/control/line-break/byte-built sequence parity and clean generation-end flush behavior. It still may not replace legacy output authority or enter R4-R4 without separate promotion and rollback gates.
