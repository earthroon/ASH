# ASH-TCU-DECODE-04-R4-R4-R1
# TensorCube Fragment Authority Canary / Legacy Byte-Exact Rollback Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4-R1_TENSORCUBE_FRAGMENT_AUTHORITY_CANARY_LEGACY_BYTE_EXACT_ROLLBACK_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4_LIVE_TENSORCUBE_FRAGMENT_DECODER_PRIMARY_CANDIDATE_LEGACY_ORACLE_DUAL_RUN_GATE`
- Runtime mode: `greedy_cached_generation_buffered_tensorcube_fragment_authority_canary`
- TensorCube authority: bounded final-generation fragment commit only
- Legacy authority: parallel byte-exact rollback source
- Streaming authority: false
- General production apply: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R4-R2_FOUR_ROUTE_TENSORCUBE_FRAGMENT_AUTHORITY_STREAM_COMMIT_PARITY_GATE`

## Purpose

R4-R4-R1 is the first gate that permits TensorCube-produced fragment bytes to become returned production text. Authority is restricted to a deterministic greedy-cached canary and is granted only after a complete generation has been staged and compared.

```text
selected token IDs remain production-owned
TensorCube candidate fragments -> private generation buffer
legacy oracle fragments         -> private rollback buffer
final output                     -> empty until terminal decision
```

Terminal decision:

```text
all candidate/oracle checks pass
-> commit candidate generation buffer exactly once

first mismatch, candidate HOLD, invalid state, or terminal divergence
-> revoke candidate publication authority
-> commit complete legacy buffer exactly once
```

Candidate and legacy bytes may never be incrementally mixed in the final output.

## Canary scope

The only admitted authority scope is:

```text
route=greedy_cached
streaming=false
batch_size=1
1 <= max_new_tokens <= 256
legacy oracle dual-run mandatory
output publication at terminal generation boundary
```

The following are rejected before candidate authority allocation:

```text
sampled_cached
greedy_streaming
sampled_streaming
max_new_tokens=257
batch_size=2
```

Explicit operator seal:

```text
--authorize-greedy-cached-tensorcube-fragment-canary
```

The seal grants no token, KV, sampler, RNG, streaming, general apply, or legacy-retirement authority.

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r4-parent-manifest <PATH>
```

The exact parent must prove:

```text
R4-R4 PASS
execution_id="decode04r4r4-" + lineage_bundle_digest[0..20]
decode04_r4_r4_r1_authorized=true
candidate independence proven
2048-token candidate/oracle parity
unexpected mismatch count=0
candidate production append count=0
legacy-exclusive output authority
all production mutation counts zero
production apply=false
legacy retirement=false
```

The parent manifest exact-file SHA, candidate owner, tokenizer identity, and route identity are lineage-bound.

## Concrete SSOT

```text
model_core::R4R4R1CanaryScope
model_core::R4R4R1GenerationTransaction
model_core::R4R4R1GenerationTransactionState
model_core::R4R4R1CommitSource
model_core::R4R4R1RollbackReason
model_core::R4R4R1ProductionCommitReceipt
model_core::R4R4R1AtomicGenerationOutputSink
model_core::begin_r4r4_r1_canary_generation_transaction
model_core::stage_r4r4_r1_dual_fragment
model_core::stage_r4r4_r1_legacy_only_after_rollback
model_core::prepare_r4r4_r1_terminal_decision
model_core::commit_r4r4_r1_candidate_generation
model_core::rollback_r4r4_r1_to_legacy_generation
model_core::finalize_r4r4_r1_production_output
```

Exactly one canonical implementation of each transaction operation is permitted. Route-local canary transaction formats are forbidden.

## Generation transaction

One transaction owns one admitted generation epoch:

```text
selected token ledger
candidate comparison digests
candidate generation buffer
legacy generation buffer
first immutable rollback reason
terminal decision
commit source
output commit count
```

Allowed states:

```text
Created -> Collecting
Collecting -> CandidateCommitPrepared -> CandidateCommitted
Collecting -> LegacyRollbackPrepared -> LegacyRollbackCommitted
Collecting -> Rejected | Aborted
```

Committed states are terminal.

## Per-token staging

For each selected token:

```text
1. TensorCube candidate runs and seals its result
2. legacy oracle runs independently
3. comparator seals parity or mismatch
4. candidate fragment appends only to candidate buffer
5. oracle fragment appends only to legacy buffer
6. final output remains empty
```

After the first unexpected mismatch:

```text
candidate state freezes
candidate buffer remains private evidence
legacy oracle continues for all remaining tokens
legacy buffer becomes a complete rollback generation
```

Candidate state may not be repaired from legacy output.

## Candidate commit

Candidate commit eligibility requires:

```text
terminal generation boundary reached
candidate and oracle clean flush
selected-token and fragment counts exact
all per-step fragment/decision/context/pending-state comparisons pass
candidate final state valid
candidate buffer bytes == legacy buffer bytes
candidate buffer SHA == legacy buffer SHA
production token/KV/sampler/RNG state parity
final output sink empty
```

Commit behavior:

```text
source=Candidate
publish candidate buffer once
legacy buffer remains evidence only
output_commit_count=1
```

## Legacy rollback

Rollback triggers include:

```text
candidate HOLD
fragment byte mismatch
decision mismatch
context mismatch
pending-byte mismatch
sequence-index mismatch
terminal flush mismatch
candidate state invariant failure
candidate buffer digest mismatch
candidate/oracle final digest mismatch
production state parity mismatch
scope or output-sink precondition violation
```

Rollback behavior:

```text
freeze candidate
revoke candidate publication authority
complete legacy buffer
validate legacy-only baseline parity
publish legacy buffer once
source=LegacyRollback
```

Required output truth:

```text
final output == legacy oracle buffer == legacy-only baseline
candidate byte leak count=0
mixed-source output count=0
duplicate output byte count=0
missing output byte count=0
```

## Atomic output contract

The final output sink must support one logical generation publication:

```text
is_empty()
commit_generation(bytes)
committed_bytes()
```

Before terminal decision:

```text
final output length=0
final output write count=0
candidate byte leak=0
legacy byte leak=0
```

After publication:

```text
one source selected
one commit attempted
one commit succeeds
second commit count=0
post-commit append count=0
```

Incremental or streaming sinks are inadmissible in R4-R4-R1.

## Required positive corpus

Candidate commit must pass at generation lengths:

```text
1
8
32
128
256
```

The corpus covers normal SentencePiece fragments, empty/control fragments, structural line breaks, byte-built whitespace, line breaks, tabs, Hangul, emoji, and clean terminal flush.

Every admitted positive fixture commits `Candidate` and produces bytes equal to the legacy baseline.

## Required rollback matrix

The audit injects at least:

```text
first-token byte mismatch
middle-token byte mismatch
last-token byte mismatch
candidate visible/oracle empty
candidate empty/oracle visible
SentencePiece decision mismatch
control suppression mismatch
structural line-break mismatch
byte-carry decision mismatch
UTF-8 materialization mismatch
context-after mismatch
pending-byte mismatch
sequence-index mismatch
terminal flush mismatch
candidate buffer digest mismatch
candidate HOLD
candidate state invariant failure
production state parity mismatch
```

Every case must select `LegacyRollback`, commit once, expose zero candidate bytes, and equal the legacy-only baseline.

## Production ownership

TensorCube receives already-selected token IDs. It owns no production capability for:

```text
token selection
DecodeState mutation
KV mutation
sampler or RNG
finish/stop
stream emission
route switching
checkpoint/resume
non-canary fragment commit
```

The only permitted TensorCube production mutation is one final generation publication when `commit_source=Candidate` and all canary conditions pass.

## Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_canary_scope_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_transaction_owner_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_dual_buffer_steps_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_candidate_commit_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_legacy_rollback_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_rollback_injection_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_exactly_once_output_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_output_source_purity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_token_kv_state_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_shadow_canary_parity_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_route_scope_rejection_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_limit_boundary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_capability_inventory_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_non_canary_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_static_structure_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_no_cleanup_no_repair_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r1_performance_evidence_latest.json
```

Writes are atomic and the local manifest is written last. Runtime evidence is excluded from source-only archives.

## Binary

```text
ash_tcu_decode_04_r4_r4_r1_tensorcube_fragment_authority_canary_legacy_byte_exact_rollback_gate
```

## Execution identity

```text
decode04r4r4r1-<first 20 hex of lineage_bundle_digest>
```

Lineage binds parent and tokenizer identity, canary scope, transaction schema, positive commit receipts, rollback matrix, first/middle/last/flush rollback evidence, exactly-once publication, source purity, token/KV parity, route and limit rejections, capability inventory, mutation audit, static structure, and no-repair evidence.

Paths, timestamps, timings, PIDs, pointers, capacities, hostnames, and temporary names are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R4_R1_TENSORCUBE_FRAGMENT_AUTHORITY_CANARY_LEGACY_BYTE_EXACT_ROLLBACK_GATE
```

PASS requires:

```text
exact parent admission
explicit canary operator seal
greedy-cached scope only
positive candidate commits for 1/8/32/128/256 tokens
full candidate/oracle buffer parity
first/middle/last/terminal rollback proof
complete rollback injection matrix
legacy byte-exact rollback parity
zero candidate byte leak
zero mixed-source output
zero duplicate or missing bytes
exactly one output commit per generation
excluded route and limit rejection
token/KV/sampler/RNG/finish/route parity
zero cleanup or silent repair
zero TensorCube mutation outside bounded candidate terminal commit
all_truth_checks_pass=true
```

PASS grants only:

```text
decode04_r4_r4_r2_authorized=true
tensorcube_bounded_fragment_authority_proven=true
tensorcube_general_fragment_authority=false
tensorcube_streaming_fragment_authority=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
```

HOLD and FAIL grant no additional production authority.

## Next gate

PASS authorizes only:

```text
ASH-TCU-DECODE-04-R4-R4-R2
Four-Route TensorCube Fragment Authority / Stream Commit Parity Gate
```

R4-R4-R2 must define a stream-safe commit protocol that never requires retracting already exposed bytes. Legacy byte-exact rollback remains mandatory.
