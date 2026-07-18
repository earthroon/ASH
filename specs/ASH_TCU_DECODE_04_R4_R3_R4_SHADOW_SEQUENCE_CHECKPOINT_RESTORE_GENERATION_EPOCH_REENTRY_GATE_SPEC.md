# ASH-TCU-DECODE-04-R4-R3-R4
# Shadow Sequence Checkpoint / Restore / Generation Epoch Re-entry Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R3-R4_SHADOW_SEQUENCE_CHECKPOINT_RESTORE_GENERATION_EPOCH_REENTRY_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R3-R3_STATEFUL_SHADOW_FRAGMENT_SEQUENCE_PARITY_FLUSH_BOUNDARY_GATE`
- Runtime mode: `live_shadow_checkpoint_restore_reentry_compare_only`
- Legacy output authority: exclusive
- Production checkpoint/resume authority: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R3-R5_SHADOW_CHECKPOINT_PERSISTENCE_CRASH_RECOVERY_REPLAY_EXCLUSION_GATE`

## Purpose

R4-R3-R4 proves that the private generation-scoped R4-R3-R1/R2/R3 shadow owner can be checkpointed at a selected-token transaction boundary, restored into one fresh private owner, and re-entered in the same generation epoch without fragment replay, entry loss, byte-carry corruption, ledger-chain divergence, or production mutation.

Required truth:

```text
checkpoint only between selected-token transactions
canonical payload bytes and content-derived checkpoint ID
payload SHA and lineage binding
paused original private owner
single-consumption restore
same-generation epoch re-entry only
first resumed token and entry exactly once
pending UTF-8 carry restore parity
sequence ledger digest-chain continuity
uninterrupted baseline parity
stale/cross-epoch/mismatch/corruption rejection
no dual mutable private owner
legacy production output unchanged
```

## Concrete SSOT

```text
model_core::R4R3R4CheckpointPayload
model_core::R4R3R4CheckpointEnvelope
model_core::R4R3R4CheckpointLease
model_core::R4R3R4RestoreAdmission
model_core::R4R3R4RestoreDecision
model_core::create_r4r3_r4_shadow_checkpoint
model_core::validate_r4r3_r4_shadow_checkpoint
model_core::restore_r4r3_r4_shadow_checkpoint
model_core::reenter_r4r3_r4_generation_epoch
model_core::R4R3R1FragmentStagingState
model_core::R4R3R3SequenceLedger
```

There is exactly one checkpoint serializer, one validator, one restore constructor, and one same-epoch re-entry function. Route-local checkpoint formats and restore policies are forbidden.

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r3-r3-parent-manifest <PATH>
```

The exact parent must prove:

```text
R4-R3-R3 PASS
all_truth_checks_pass=true
decode04_r4_r3_r4_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
sequence_entry_count=1024
sequence digest chain valid
full sequence oracle parity
zero duplicate/drop/reorder
clean flush and terminal incomplete typed HOLD
generation epoch isolation
legacy exclusive output authority
zero production mutations
execution_id="decode04r4r3r3-" + lineage_bundle_digest[0..20]
```

The parent manifest exact-file SHA, lineage digest, owner ID, tokenizer identity, and route digest are bound.

## Checkpoint-safe boundary

Checkpoint creation is admitted only when:

```text
no selected-token transaction in flight
no ledger transaction in flight
state_revision == next_step_index
ledger next index == ledger entry count
ledger digest chain valid
raw-visible length and digest valid
context matches raw-visible text
pending byte count == pending token-ID count
pending bytes empty or valid incomplete UTF-8
ledger not finalized
owner not disabled
```

A partial transaction can never be checkpointed.

## Canonical payload and envelope

The payload directly owns all continuation state:

```text
parent execution and lineage
fragment parent execution ID
tokenizer identity and manifest SHA
owner ID and generation epoch
state revision and next step index
initial prefix digest
raw visible text and rolling digest
SentencePiece context
last token and piece kind
fragment/control/line-break counters
pending UTF-8 bytes and token IDs
complete R4-R3-R3 sequence ledger
runtime route digest
checkpoint step and sequence boundaries
```

Serialization contract:

```text
canonical_struct_json_utf8_v1
serde struct declaration order
UTF-8 without BOM
no pretty printing
no unordered map
no timestamp, duration, PID, pointer, hostname, or random nonce
```

Checkpoint ID:

```text
r4r3r4-checkpoint-<first 24 hex of payload_sha256>
```

The envelope binds payload length, payload SHA, owner, epoch, revision, next step, last sequence digest, finalization state, and lineage binding digest. Envelope/payload disagreement is rejection.

## Pause, restore, and single consumption

After successful capture:

```text
original private owner paused
original append/finalize authority disabled
payload and envelope immutable evidence
```

Accepted restore constructs a fresh in-memory owner with the same logical owner ID and generation epoch. The checkpoint lease becomes consumed. A second restore is rejected.

At all times:

```text
active mutable private owner count <= 1
```

## Restore admission

Restore validates, in order:

```text
schema and encoding
payload length and SHA
content-derived checkpoint ID
lineage binding digest
parent execution and lineage
tokenizer manifest SHA
owner ID
generation epoch
runtime route digest
state invariants
pending UTF-8 prefix
sequence ledger digest chain
finalized status
single consumption
staleness against active revision
```

No missing field may be defaulted and no state may be reconstructed from legacy output.

## Same-epoch re-entry

The first resumed token must satisfy:

```text
resumed step index == checkpoint next step index
resumed sequence index == checkpoint next sequence index
previous entry digest == checkpoint last entry digest
selected token ID == expected next selected token ID
first resumed token processed once
first resumed entry appended once
```

Required zero counts:

```text
resume duplicate
resume drop
resume reorder
stale replay
```

Cross-generation restore, epoch rewrite, owner rewrite, tokenizer migration, and route migration are forbidden.

## Runtime fixtures

A pending-byte fixture checkpoints after the first byte of a multibyte scalar, restores, and proves exact continuation materialization.

A separate 1024-token mixed fixture includes normal SentencePiece, standalone empty marker, consecutive controls, structural line break, byte-built line break, Hangul, ASCII space, emoji, tab, and normal text after byte-built whitespace.

The 1024-token fixture checkpoints and restores at:

```text
0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 15, 16, 17,
32, 128, 512, 1023
```

This covers before-first-token, normal, empty, control, structural line break, pending byte carry, completed byte materialization, byte-built whitespace, Hangul, emoji, and long-sequence boundaries.

Checkpoint/restore execution must equal an uninterrupted baseline for:

```text
selected token sequence
fragment class and bytes
context
pending bytes and token IDs
state revision and sequence index
entry digest chain
final raw-visible bytes
rolling digest
final ledger digest
flush decision
```

## Negative and corruption fixtures

Required rejection classes include:

```text
payload byte change
payload length change
checkpoint ID change
lineage binding change
parent mismatch
tokenizer mismatch
owner mismatch
generation epoch mismatch
route mismatch
stale revision
checkpoint second consumption
finalized checkpoint for running restore
invalid pending UTF-8
broken ledger digest chain
dual active owner attempt
```

All rejection paths leave production state unchanged.

## Live activation

```text
ASH_TCU_DECODE04_R4_R3_SHADOW=1
ASH_TCU_DECODE04_R4_R3_R1_STAGING=1
ASH_TCU_DECODE04_R4_R3_R1_PARENT_EXECUTION_ID=<R4-R3 execution ID>
ASH_TCU_DECODE04_R4_R3_R2_BYTE_CARRY=1
ASH_TCU_DECODE04_R4_R3_R2_PARENT_EXECUTION_ID=<R4-R3-R1 execution ID>
ASH_TCU_DECODE04_R4_R3_R3_SEQUENCE_LEDGER=1
ASH_TCU_DECODE04_R4_R3_R3_PARENT_EXECUTION_ID=<R4-R3-R2 execution ID>
ASH_TCU_DECODE04_R4_R3_R4_CHECKPOINT_RESTORE=1
ASH_TCU_DECODE04_R4_R3_R4_PARENT_EXECUTION_ID=<R4-R3-R3 execution ID>
```

R4-R3-R4 activation requires R4-R3-R3 sequence-ledger activation and an explicit parent execution ID. Absence of R4-R3-R4 activation leaves the prior legacy-authoritative generation path unchanged.

## Route and capability boundary

All four production routes remain covered:

```text
sampled cached
sampled streaming
greedy cached
greedy streaming
```

The existing eight selected-token materialization call sites remain unchanged. Checkpointing operates only on the private shadow owner.

Forbidden production authority counts are zero for DecodeState, KV, token append, output, stream, sampler, RNG, finish/stop, route switching, checkpoint, and resume.

Shadow disabled, shadow enabled without restore, and checkpoint/restore runs must preserve production selected tokens, legacy fragments, output bytes, stream chunks and boundaries, DecodeState, KV owner, sampler, RNG, finish/stop, and route.

## Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_checkpoint_payload_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_checkpoint_envelope_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_checkpoint_creation_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_restore_admission_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_restore_state_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_generation_reentry_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_uninterrupted_baseline_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_pending_byte_restore_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_multi_checkpoint_same_epoch_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_stale_checkpoint_rejection_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_cross_epoch_rejection_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_corruption_matrix_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_dual_owner_exclusion_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_shadow_on_off_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_non_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_r4_static_structure_audit_latest.json
```

Writes are atomic and the local manifest is written last. Runtime evidence is excluded from source-only archives.

## Binary and CLI

Binary:

```text
ash_tcu_decode_04_r4_r3_r4_shadow_sequence_checkpoint_restore_generation_epoch_reentry_gate
```

The binary requires every activation and proof flag in the detailed R4-R3-R4 specification, covering parent admission, canonical checkpoint format, restore bindings, same-epoch re-entry, first-resumed-token exactly-once, pending-byte continuation, 1024-token checkpoint matrix, mismatch and corruption rejection, route coverage, production parity, zero repair, and zero production mutation.

## Execution identity

```text
decode04r4r3r4-<first 20 hex of lineage_bundle_digest>
```

Stable lineage binds parent identity, tokenizer SHA, checkpoint payload SHA, checkpoint lineage binding, restore-state parity, re-entry receipt, 1024-token baseline parity, pending-byte restore, multi-checkpoint parity, stale and cross-epoch rejection, corruption matrix, dual-owner exclusion, route and capability evidence, production parity, mutation audit, and static structure audit.

Absolute paths, timestamps, durations, PIDs, pointer values, allocation capacities, temporary filenames, hostnames, and environment ordering are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R3_R4_SHADOW_SEQUENCE_CHECKPOINT_RESTORE_GENERATION_EPOCH_REENTRY_GATE
```

PASS requires all checkpoint, restore, re-entry, baseline, pending-byte, long-sequence, corruption, ownership, route, authority, and non-mutation checks to pass.

PASS grants only:

```text
decode04_r4_r3_r5_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production_checkpoint_authorized=false
production_resume_authorized=false
production token/KV/text/stream/finish authority=false
```

HOLD and FAIL grant no next-stage or production authority.