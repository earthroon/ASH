# ASH-TCU-DECODE-04-R4-R4
# Live TensorCube Fragment Decoder Primary Candidate / Legacy Oracle Dual-Run Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4_LIVE_TENSORCUBE_FRAGMENT_DECODER_PRIMARY_CANDIDATE_LEGACY_ORACLE_DUAL_RUN_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R3-R4_SHADOW_SEQUENCE_CHECKPOINT_RESTORE_GENERATION_EPOCH_REENTRY_GATE`
- Runtime mode: `live_tensorcube_primary_candidate_legacy_oracle_dual_run_compare_only`
- TensorCube candidate mutation authority: private state only
- Legacy decoder production fragment authority: exclusive
- Production apply: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R4-R1_TENSORCUBE_FRAGMENT_AUTHORITY_CANARY_LEGACY_BYTE_EXACT_ROLLBACK_GATE`

## Purpose

R4-R4 is the first gate in which TensorCube independently computes a fragment candidate from the selected token and its own decode state.

```text
selected token ID
+ exact tokenizer manifest
+ TensorCube-owned SentencePiece context
+ TensorCube-owned pending UTF-8 bytes
+ TensorCube-owned sequence ledger
-> independent TensorCube candidate fragment
```

The legacy decoder runs after the candidate has been sealed and remains the only production fragment source.

```text
TensorCube candidate -> private compare-only state
legacy oracle        -> authoritative production fragment
comparator           -> byte/context/state evidence
```

TensorCube may not emit production text, stream chunks, KV, sampler, RNG, finish/stop, or route changes in this gate.

## Direct transition seal

The R4-R3-R4 parent reports:

```text
decode04_r4_r3_r5_authorized=true
decode04_r4_r4_authorized=false
```

R4-R3-R5 durable crash-recovery persistence is not required for live fragment-candidate correctness, but this branch transition may not be hidden. R4-R4 therefore requires:

```text
--authorize-r4-r4-direct-transition-from-r4-r3-r4
```

The parent-admission receipt preserves both facts:

```text
parent_decode04_r4_r4_authorized=false
direct_transition_operator_seal_required=true
```

This seal only defers R4-R3-R5. It grants no production authority and does not by itself authorize R4-R4-R1.

## Concrete SSOT

```text
model_core::R4R4CandidateDecodeState
model_core::R4R4CandidateFragment
model_core::R4R4LegacyOracleFragment
model_core::R4R4CandidateOracleComparison
model_core::R4R4CandidateMismatchClass
model_core::initialize_r4r4_candidate_state
model_core::decode_r4r4_tensorcube_fragment_candidate
model_core::run_r4r4_legacy_fragment_oracle
model_core::compare_r4r4_candidate_with_legacy_oracle
model_core::append_legacy_fragment_with_r4r4_dual_run
GenerationTelemetry::tensorcube_r4_r4_candidate
GenerationTelemetry::tensorcube_r4_r4_oracle
GenerationTelemetry::tensorcube_r4_r4_comparison
```

Required static ownership:

```text
canonical candidate decoder count=1
canonical legacy oracle adapter count=1
canonical comparator count=1
canonical dual-run helper count=1
route-local candidate decoder count=0
route-local comparator count=0
```

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r3-r4-parent-manifest <PATH>
```

The exact parent must prove R4-R3-R4 PASS, checkpoint roundtrip parity, restored-state parity, same-epoch re-entry, first-resumed-token exactly once, pending-byte restore parity, sequence digest continuity, multi-checkpoint parity, stale and cross-epoch rejection, corruption detection, zero dual active owners, four-route coverage, legacy-exclusive output authority, and zero production mutations.

Parent execution identity must reproduce as:

```text
execution_id="decode04r4r3r4-" + lineage_bundle_digest[0..20]
```

The exact parent manifest SHA, parent owner, tokenizer manifest SHA, tokenizer intrinsic identity, and route digest are bound.

## Candidate independence

Forbidden candidate inputs:

```text
legacy fragment
legacy output buffer
legacy stream chunk
legacy temporary decode buffer
legacy cleanup result
legacy sequence ledger
oracle comparator feedback
```

Allowed inputs:

```text
selected token ID
exact tokenizer surface
candidate-owned context
candidate-owned pending bytes
candidate-owned ledger
generation epoch
route identity
initial prefix
```

Required zero counts:

```text
candidate_legacy_fragment_read_count=0
candidate_legacy_output_read_count=0
candidate_legacy_stream_read_count=0
candidate_state_reconstruction_from_legacy_count=0
candidate_production_append_path_count=0
```

## Candidate owner and state

Exactly one candidate owner exists per generation epoch.

```text
r4r4-candidate-owner-<first 24 hex of owner binding digest>
```

The owner binds parent execution, tokenizer identity, generation epoch, initial-prefix digest, candidate schema, and route digest.

Candidate state owns:

```text
raw visible text and digest
SentencePiece context
pending bytes and contributing token IDs
state revision and next step index
independent sequence ledger
active/mismatch status
last comparison digest
```

It aliases neither production DecodeState/KV nor legacy decoder state.

## Dual-run ordering

Every selected token executes:

```text
1. validate candidate owner and token binding
2. capture candidate pre-state
3. independently decode TensorCube candidate
4. seal candidate fragment and candidate post-state
5. run legacy decoder oracle
6. seal oracle fragment
7. compare candidate and oracle
8. append only the legacy fragment to production output
9. write immutable receipts
```

Candidate execution after oracle or candidate mutation after oracle observation is forbidden.

## Candidate decisions

```text
normal SentencePiece start
normal SentencePiece continuation
empty SentencePiece
suppressed control
structural line break
byte carry started
byte carry extended
byte sequence materialized
typed HOLD incomplete byte boundary
typed HOLD invalid candidate state
```

SentencePiece context, byte carry, UTF-8 assembly, and sequence ledger are resolved from candidate state only.

## Comparison and mismatch policy

The comparator checks:

```text
fragment byte identity
fragment length
SentencePiece/control/line-break decision
context transition
pending byte state in independent audit corpus
sequence index
candidate state validity
```

Mismatch classes include visible/empty disagreement, byte or length mismatch, SentencePiece boundary mismatch, control/line-break mismatch, byte-carry or UTF-8 mismatch, context mismatch, pending-state mismatch, sequence-index mismatch, and candidate invariant failure.

Policy:

```text
stop_candidate_after_first_unexpected_mismatch
```

On mismatch, candidate evidence is frozen and the candidate owner is disabled. Legacy production continues. Candidate bytes may not be rewritten from oracle bytes, and a mismatch may not be reported as parity.

## Production append authority

```text
candidate production append count=0
oracle production append count=selected-token count
double append count=0
missing append count=0
```

Only the legacy oracle fragment is production-authoritative in R4-R4.

## Runtime corpus

The audit executes a 2048-token mixed corpus containing normal SentencePiece fragments, control suppression, structural line breaks, standalone markers when available, byte-built Hangul, ASCII space, emoji, tab, newline, and text following byte-built whitespace.

Required parity:

```text
per-step fragment bytes
per-step candidate decision
per-step context
per-step pending bytes and token IDs
per-step sequence index
final raw text bytes
final context
final pending state
final sequence ledger contents
```

Candidate checkpoint/restore must preserve candidate state and process the first resumed token exactly once. A second generation epoch must start with a distinct owner and empty carry/ledger/mismatch state.

## Hot-path routes

The same helper owns initial and loop tokens for:

```text
sampled cached
sampled streaming
greedy cached
greedy streaming
```

Required:

```text
route coverage=4/4
hot-path call sites=8
candidate bypass count=0
oracle bypass count=0
```

## Live activation

```text
ASH_TCU_DECODE04_R4_R4_CANDIDATE=1
ASH_TCU_DECODE04_R4_R4_PARENT_EXECUTION_ID=<exact R4-R3-R4 execution ID>
```

The candidate is calculated before `append_token_piece_to_text`. Candidate errors disable only the private candidate path; legacy generation continues.

## Capability boundary

Allowed:

```text
one private candidate state
one private candidate ledger
one private checkpoint roundtrip fixture
legacy oracle production fragment path
```

TensorCube production mutation counts are zero for token append, KV, text, stream, finish/stop, sampler, RNG, route changes, fragment commit, checkpoint, and resume.

## Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_candidate_owner_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_candidate_capability_inventory_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_dual_run_steps_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_candidate_sequence_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_legacy_oracle_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_candidate_oracle_comparison_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_first_mismatch_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_independence_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_mismatch_fixture_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_full_sequence_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_checkpoint_restore_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_generation_epoch_isolation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_route_coverage_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_shadow_on_off_production_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_non_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_static_structure_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_no_cleanup_no_repair_audit_latest.json
```

Writes are atomic and the local manifest is written last. Runtime evidence is excluded from source-only archives.

## Binary

```text
ash_tcu_decode_04_r4_r4_live_tensorcube_fragment_decoder_primary_candidate_legacy_oracle_dual_run_gate
```

## Execution identity

```text
decode04r4r4-<first 20 hex of lineage_bundle_digest>
```

Stable lineage binds parent and tokenizer identity, candidate owner/schema, candidate/oracle contracts, 2048-token parity, checkpoint/restore, epoch isolation, mismatch matrix, independence audit, route/capability evidence, production parity, mutation audit, static structure, and no-repair evidence. Paths, timestamps, timings, PIDs, pointers, capacities, and temporary names are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R4_LIVE_TENSORCUBE_FRAGMENT_DECODER_PRIMARY_CANDIDATE_LEGACY_ORACLE_DUAL_RUN_GATE
```

PASS requires exact parent admission plus the explicit direct-transition seal, candidate independence, candidate-before-oracle ordering, 2048-token per-step/final parity, checkpoint/restore parity, epoch isolation, classified mismatch fixtures, zero unexpected mismatch/HOLD in the positive corpus, zero candidate production commit, exact oracle append count, four routes/eight call sites, legacy-exclusive output authority, zero repair, and zero production mutation.

PASS grants only:

```text
decode04_r4_r4_r1_authorized=true
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
tensorcube_production_fragment_authority=false
tensorcube_production_stream_authority=false
tensorcube_production_kv_authority=false
```

HOLD and FAIL grant no production authority.
