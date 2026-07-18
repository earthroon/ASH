# ASH-TCU-DECODE-04-R4-R4-R2
# Four-Route TensorCube Fragment Authority / Stream Commit Parity Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4-R2_FOUR_ROUTE_TENSORCUBE_FRAGMENT_AUTHORITY_STREAM_COMMIT_PARITY_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4-R1_TENSORCUBE_FRAGMENT_AUTHORITY_CANARY_LEGACY_BYTE_EXACT_ROLLBACK_GATE`
- Runtime mode: `four_route_tensorcube_fragment_authority_with_cached_terminal_commit_and_stream_compare_before_emit`
- Cached authority: generation-buffered terminal commit
- Streaming authority: current-fragment compare-before-emit
- Legacy oracle: mandatory
- Production token/KV/sampler/RNG authority: legacy only
- General production apply: false
- Legacy retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R4-R3_LIVE_FRAGMENT_AUTHORITY_CORPUS_MISMATCH_TELEMETRY_PERFORMANCE_GATE`

## Purpose

R4-R4-R2 extends bounded TensorCube fragment publication from the R4-R4-R1 greedy-cached canary to all four routes:

```text
greedy cached
greedy streaming
sampled cached
sampled streaming
```

Two commit protocols are required.

```text
cached routes
-> TensorCube candidate generation buffer
-> legacy oracle generation buffer
-> terminal candidate commit or terminal legacy rollback

streaming routes
-> TensorCube candidate fragment
-> legacy oracle fragment
-> compare current bytes and state before exposure
-> emit exactly one source
-> mismatch revokes candidate authority before current candidate bytes are exposed
```

Previously emitted candidate stream fragments need no retraction because every one was byte-exact with the oracle before emission.

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r4-r1-parent-manifest <PATH>
```

The exact parent must prove:

```text
R4-R4-R1 PASS
execution_id="decode04r4r4r1-" + lineage_bundle_digest[0..20]
decode04_r4_r4_r2_authorized=true
tensorcube_bounded_fragment_authority_proven=true
greedy-cached positive candidate commits=5
legacy rollback fixtures=18
first/middle/last/terminal rollback proven
candidate byte leak=0
mixed-source output=0
exactly-once output=true
token/KV state parity=true
general fragment authority=false
streaming fragment authority=false
production apply=false
legacy retirement=false
```

The parent exact-file SHA, parent lineage, candidate owner, tokenizer identity, and route identity are bound.

## Operator seal

```text
--authorize-four-route-tensorcube-fragment-authority
```

This grants only R4-R4-R2 bounded fragment authority. It grants no TensorCube token-selection, sampler, RNG, KV, DecodeState, finish/stop, checkpoint, resume, general apply, or legacy-retirement authority.

## Concrete SSOT

```text
model_core::R4R4R2RouteClass
model_core::R4R4R2AuthorityMode
model_core::R4R4R2AuthorityState
model_core::R4R4R2RouteAuthorityPolicy
model_core::R4R4R2CachedGenerationTransaction
model_core::R4R4R2StreamFragmentTransaction
model_core::R4R4R2StreamAuthorityRevocation
model_core::R4R4R2FragmentCommitSource

model_core::resolve_r4r4_r2_route_authority
model_core::begin_r4r4_r2_cached_generation_transaction
model_core::stage_r4r4_r2_cached_dual_fragment
model_core::stage_r4r4_r2_cached_legacy_only
model_core::finalize_r4r4_r2_cached_generation
model_core::begin_r4r4_r2_stream_fragment_transaction
model_core::compare_before_emit_r4r4_r2_stream_fragment
model_core::emit_r4r4_r2_stream_candidate_fragment
model_core::emit_r4r4_r2_stream_oracle_fragment
model_core::revoke_r4r4_r2_stream_candidate_authority
model_core::append_fragment_with_r4r4_r2_four_route_authority
```

Required ownership:

```text
one route authority resolver
one cached transaction implementation
one stream transaction implementation
one stream revocation implementation
one four-route helper
eight existing selected-token hot-path call sites
```

## Cached protocol

Both greedy-cached and sampled-cached use generation buffering.

```text
all candidate/oracle parity passes
-> commit candidate buffer once

mismatch, HOLD, state divergence, digest divergence, or flush divergence
-> freeze candidate
-> complete legacy buffer
-> commit legacy buffer once
```

Required positive lengths for each cached route:

```text
1, 8, 32, 128, 256
```

Required rollback positions for each cached route:

```text
first, middle, last, terminal flush
```

Sampled-cached selected tokens, sampler state, and RNG remain production-owned. TensorCube may not rerun or advance the sampler or RNG.

## Streaming protocol

Streaming authority requires current-fragment compare-before-emit.

```text
1. production path selects token
2. TensorCube computes candidate
3. legacy computes oracle
4. candidate/oracle bytes and state are compared
5. exactly one source is emitted
```

Candidate emit admission requires:

```text
candidate active
candidate state valid
fragment byte parity
context parity
pending-byte parity
sequence-index parity
selected-token binding
route binding
current token not yet emitted
```

On first mismatch or HOLD:

```text
candidate current bytes remain private
oracle current fragment emits once
candidate state restores to last parity-accepted snapshot
candidate authority is revoked
remaining generation runs legacy-only
candidate re-enable count=0
```

Commit sources:

```text
Candidate
LegacyCurrentTokenFallback
LegacyPostRevocation
LegacyCachedRollback
```

Mixed or unknown sources are forbidden.

## Streaming UTF-8 and chunk boundaries

```text
byte-carry-only token emits zero bytes
materialized scalar emits atomically
incomplete UTF-8 never reaches stream
invalid UTF-8 chunk count=0
partial scalar emit count=0
replacement-character emit count=0
stream finalization exactly once
chunk sequence parity exact
chunk boundary parity exact
```

Empty, control, and byte-carry-only tokens still produce one logical transaction receipt even when they emit zero bytes.

## Fixtures

Positive lengths for each of the four routes:

```text
1, 8, 32, 128, 256
```

Cached rollback matrix:

```text
greedy cached: first, middle, last, terminal flush
sampled cached: first, middle, last, terminal flush
```

Streaming revocation matrix:

```text
greedy streaming: first, middle, last, byte materialization, structural line break, terminal-adjacent
sampled streaming: first, middle, last, byte materialization, structural line break, terminal-adjacent
```

Every stream revocation fixture must prove:

```text
mismatched candidate bytes not emitted
current oracle fragment emitted once
candidate authority revoked once
candidate never re-enabled
remaining fragments legacy-only
final stream equals legacy-only baseline
```

## Limits

```text
batch size=1
max_new_tokens<=256
legacy oracle required=true
mid-generation route change forbidden
batch size 2 rejected
max_new_tokens 257 rejected
```

No silent clamping, route migration, or batch splitting is allowed.

## Production parity

Across legacy-only, compare-only, candidate-authority success, and forced fallback/revocation:

```text
selected-token sequence parity
DecodeState parity
KV owner and logical-content parity
sampler-state parity
RNG-state parity
finish/stop parity
runtime-route parity
cached output byte parity
stream output byte parity
stream chunk sequence parity
stream chunk boundary parity
```

## Capability boundary

Allowed TensorCube mutations:

```text
bounded cached final-generation candidate commit
bounded stream candidate-fragment emit after oracle parity
```

Forbidden TensorCube mutations:

```text
token selection
KV
DecodeState
sampler
RNG
finish/stop
route
checkpoint
resume
```

Legacy oracle bypass count must remain zero.

## Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_operator_seal_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_route_authority_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_cached_generation_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_fragment_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_generation_summaries_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_revocation_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_cached_rollback_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_revocation_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_exactly_once_stream_emit_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_utf8_boundary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_stream_chunk_boundary_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_token_kv_sampler_rng_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_output_parity_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_capability_inventory_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_production_mutation_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_static_structure_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_no_cleanup_no_repair_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r4_r2_performance_evidence_latest.json
```

Writes are atomic, the local manifest is written last, and runtime evidence is excluded from source-only archives.

## Binary

```text
ash_tcu_decode_04_r4_r4_r2_four_route_tensorcube_fragment_authority_stream_commit_parity_gate
```

## Execution identity

```text
decode04r4r4r2-<first 20 hex of lineage_bundle_digest>
```

Lineage binds parent and tokenizer identity, operator seal, route policy, cached and stream protocol evidence, route fixtures, rollback and revocation matrices, UTF-8 and chunk boundaries, token/KV/sampler/RNG parity, output parity, capability inventory, mutation audit, static structure, and no-repair evidence.

Paths, timestamps, timings, PIDs, pointers, capacities, temporary filenames, and environment ordering are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R4_R2_FOUR_ROUTE_TENSORCUBE_FRAGMENT_AUTHORITY_STREAM_COMMIT_PARITY_GATE
```

PASS requires:

```text
route coverage=4/4
hot-path call sites=8
cached positive commits for both routes at 1/8/32/128/256
cached first/middle/last/flush rollback for both routes
stream positive candidate emits for both routes at 1/8/32/128/256
stream first/middle/last/materialization/linebreak/terminal revocation for both routes
compare-before-emit proven
current-token oracle fallback proven
post-revocation legacy continuation proven
candidate re-enable count=0
candidate byte leak=0
double emit=0
missing visible emit=0
invalid UTF-8 chunks=0
partial scalar emits=0
stream finalization exactly once
chunk sequence and boundary parity exact
token/KV/sampler/RNG/finish/route parity
oracle bypass=0
zero cleanup or repair
all_truth_checks_pass=true
```

PASS grants only:

```text
decode04_r4_r4_r3_authorized=true
tensorcube_four_route_fragment_authority_proven=true
tensorcube_general_fragment_authority=false
tensorcube_streaming_fragment_authority=true
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/sampler/RNG authority=false
```

HOLD and FAIL grant no additional authority.

## Next gate

```text
ASH-TCU-DECODE-04-R4-R4-R3
Live Fragment Authority Corpus / Mismatch Telemetry / Performance Gate
```

Legacy oracle remains mandatory until a later default-authority promotion gate passes.
