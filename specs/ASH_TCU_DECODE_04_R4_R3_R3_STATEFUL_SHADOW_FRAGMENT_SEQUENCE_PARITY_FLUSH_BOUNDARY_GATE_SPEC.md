# ASH-TCU-DECODE-04-R4-R3-R3
# Stateful Shadow Fragment Sequence Parity / Flush Boundary Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R3-R3_STATEFUL_SHADOW_FRAGMENT_SEQUENCE_PARITY_FLUSH_BOUNDARY_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R3-R2_BYTE_FRAGMENT_CARRY_UTF8_ASSEMBLY_NO_REPLACEMENT_FALLBACK_SEAL`
- Runtime mode: `live_shadow_sequence_parity_and_flush_boundary_compare_only`
- Legacy output authority: exclusive
- Production authority: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R3-R4_SHADOW_SEQUENCE_CHECKPOINT_RESTORE_AND_GENERATION_EPOCH_REENTRY_GATE`

## Purpose

R4-R3-R3 proves that the generation-scoped R4-R3-R1/R2 shadow owner preserves the exact order and byte identity of mixed normal, control, structural line-break, empty, byte-carry, and byte-materialized fragments through generation finalization.

Required truth:

```text
no missing sequence entry
no duplicate fragment
no dropped fragment
no reordered fragment
no stale replay
no cross-generation carry
no forced terminal byte flush
no replacement or cleanup fallback
exact full-sequence raw-byte parity
exactly-once private finalization
legacy production output unchanged
```

## Concrete SSOT

```text
model_core::R4R3R1FragmentStagingState
model_core::R4R3R3SequenceLedger
model_core::R4R3R3SequenceEntry
model_core::R4R3R3FlushBoundaryDecision
model_core::stage_r4r3_r3_sequence_entry_transaction
model_core::finalize_r4r3_r3_generation_boundary
model_core::append_legacy_fragment_with_r4r3_shadow
tokenizer_core::decode_manifest_token_sequence_raw_with_byte_carry
GenerationTelemetry::tensorcube_r4_r3_r3_sequence_ledger
GenerationTelemetry::tensorcube_r4_r3_r3_flush_boundary
```

One R4-R3-R1 state owner owns one append-only R4-R3-R3 ledger. Route-local, stream-local, global, and cross-generation ledgers are forbidden.

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r3-r2-parent-manifest <PATH>
```

Parent requirements:

```text
exact R4-R3-R2 PASS
all_truth_checks_pass=true
decode04_r4_r3_r3_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
UTF-8 validator and byte oracle parity=true
terminal incomplete typed HOLD=true
replacement_fallback_count=0
legacy exclusive output authority=true
all production mutation counts=0
execution_id="decode04r4r3r2-" + lineage_bundle_digest[0..20]
```

The exact parent file SHA, lineage digest, owner ID, tokenizer path, tokenizer SHA, and materialization policy are bound.

## State and ledger ownership

`R4R3R1FragmentStagingState` gains an optional serde-defaulted `sequence_ledger`. This preserves deserialization of earlier R4-R3-R1/R2 artifacts while allowing live R4-R3-R3 activation.

Ledger invariants:

```text
owner ID == fragment-state owner ID
generation epoch == fragment-state generation epoch
next sequence index == ledger entry count
sequence index starts at 0 and is contiguous
step index is contiguous before typed-HOLD disablement
previous-entry digest binds the prior entry
ledger is append-only
finalized ledger rejects further append
```

Every admitted selected token produces exactly one entry, including empty fragment, control suppression, and byte-carry-only steps.

Fragment classes:

```text
normal_sentence_piece
empty_sentence_piece
suppressed_control
structural_line_break
byte_carry_only
byte_materialized_utf8
typed_hold
```

Visible ledger fragments in sequence order must concatenate to the exact private raw shadow text.

## Canonical sequence transaction

`stage_r4r3_r3_sequence_entry_transaction` calls the existing R4-R3-R2 transaction first and records exactly one ledger entry from that result.

It must not duplicate:

```text
SentencePiece context resolution
byte-piece parsing
UTF-8 validation
byte carry
raw oracle logic
legacy fragment generation
```

Entry identity binds token ID, step and sequence index, piece kind, R4-R3-R2 decision, exact fragment bytes, context, pending-byte state, state revisions, prior entry digest, commit/rollback status, and production mutation count.

## Mixed full-sequence fixture

The audit runs a 1024-token mixed fixture containing:

```text
normal SentencePiece fragments
consecutive control/empty entries
structural <br>
byte-built line break
byte-built Hangul
byte-built ASCII space
byte-built emoji
byte-built tab
normal text after byte-built whitespace
```

It compares every ledger entry with the independent tokenizer-core byte-aware raw oracle.

Required parity:

```text
entry count
selected token ID
fragment class
fragment bytes
pending bytes
pending byte token IDs
raw visible bytes
final raw text bytes
final context
```

The first divergence must remain explicit and may not be summarized away.

## Duplicate, drop, reorder, and replay audit

Required zero counts:

```text
missing_sequence_entry_count
duplicate_sequence_entry_count
dropped_sequence_entry_count
dropped_visible_fragment_count
reordered_sequence_entry_count
stale_replay_entry_count
cross_step_fragment_merge_count
unauthorized_fragment_split_count
```

Hash equality alone does not imply duplication. Epoch, step, sequence index, token ID, and transaction identity are part of the decision.

## Flush boundary

Canonical finalizer:

```text
model_core::finalize_r4r3_r3_generation_boundary
```

Decisions:

```text
clean_empty_carry
typed_hold_incomplete_utf8
typed_hold_owner_previously_disabled
fail_invalid_terminal_state
```

Clean finalization requires empty carry, valid digest chain, consistent state revision, and an unfinalized ledger. It appends no visible fragment and owns no production flush capability.

Terminal incomplete UTF-8 is retained as evidence and produces typed HOLD. It is never force-materialized or replaced.

Finalization is exactly once. Double finalization and post-finalize append are failures.

## Generation epoch isolation

At least two epochs prove:

```text
owner IDs differ
sequence index resets to zero
pending bytes start empty
ledger starts unfinalized
prior entry and flush digests are not inherited
no cross-generation carry or replay
```

## Live hot-path integration

All eight materialization sites remain behind the same helper:

| Route | Initial | Loop |
|---|---:|---:|
| sampled cached | required | required |
| sampled streaming | required | required |
| greedy cached | required | required |
| greedy streaming | required | required |

Required static truth:

```text
route coverage=4/4
hot-path helper call sites=8
canonical sequence transaction count=1
canonical flush finalizer count=1
route-local ledger count=0
route-local finalizer count=0
```

Live activation:

```text
ASH_TCU_DECODE04_R4_R3_SHADOW=1
ASH_TCU_DECODE04_R4_R3_R1_STAGING=1
ASH_TCU_DECODE04_R4_R3_R1_PARENT_EXECUTION_ID=<R4-R3 execution ID>
ASH_TCU_DECODE04_R4_R3_R2_BYTE_CARRY=1
ASH_TCU_DECODE04_R4_R3_R2_PARENT_EXECUTION_ID=<R4-R3-R1 execution ID>
ASH_TCU_DECODE04_R4_R3_R3_SEQUENCE_LEDGER=1
ASH_TCU_DECODE04_R4_R3_R3_PARENT_EXECUTION_ID=<R4-R3-R2 execution ID>
```

Absent R4-R3-R3 activation leaves legacy generation and R4-R3-R1/R2 behavior unchanged.

## Capability and production parity

Allowed mutation is limited to one private fragment state and its private ledger.

Production handle and mutation counts remain zero for DecodeState, KV, output, stream, sampler, RNG, finish/stop, route switching, GPU queue/encoder, transaction, and flush authority.

Shadow enabled/disabled runs must preserve selected tokens, legacy fragments, output bytes, stream chunks and boundaries, DecodeState, KV owner, sampler, RNG, finish/stop, and runtime route.

## No cleanup or repair

The sequence and flush paths forbid lossy UTF-8, U+FFFD insertion, fragment trimming, whitespace collapse, Unicode normalization, invalid-byte skipping, silent fragment drop, and silent duplicate suppression.

Empty and suppressed steps remain ledger entries.

## Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_state_owner_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_sequence_entries_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_sequence_summary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_full_sequence_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_duplicate_drop_reorder_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_flush_boundary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_terminal_incomplete_hold_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_generation_epoch_isolation_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_shadow_on_off_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_non_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_no_cleanup_no_repair_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r3_static_structure_audit_latest.json
```

Writes are atomic and the local manifest is written last. Generated artifacts are not baked into source archives.

## Binary

```text
ash_tcu_decode_04_r4_r3_r3_stateful_shadow_fragment_sequence_parity_flush_boundary_gate
```

## Required CLI seals

The binary requires all activation and proof flags listed by the detailed R4-R3-R3 specification, including parent admission, one ledger, digest chain, one entry per token, duplicate/drop/reorder/replay prohibition, full oracle parity, clean and HOLD flush boundaries, exactly-once finalization, epoch isolation, four routes, eight call sites, production parity, no cleanup/repair, zero production mutations, and Rust artifact writes.

## Execution identity

```text
decode04r4r3r3-<first 20 hex of lineage_bundle_digest>
```

The stable lineage binds parent lineage, owner and tokenizer identity, sequence summary, oracle parity, duplicate/drop/reorder audit, clean and HOLD flush receipts, epoch isolation, route and capability evidence, production parity, mutation audit, cleanup audit, and static structure audit. Paths, timestamps, durations, process data, and pointer values are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R3_R3_STATEFUL_SHADOW_FRAGMENT_SEQUENCE_PARITY_FLUSH_BOUNDARY_GATE
```

PASS requires all sequence, oracle, flush, isolation, route, authority, and non-mutation checks to pass.

PASS grants only:

```text
decode04_r4_r3_r4_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/text/stream/finish/flush authority=false
```

HOLD and FAIL grant no next-stage or production authority.
