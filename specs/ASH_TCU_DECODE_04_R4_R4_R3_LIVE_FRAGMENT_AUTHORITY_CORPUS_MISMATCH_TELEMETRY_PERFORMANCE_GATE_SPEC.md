# ASH-TCU-DECODE-04-R4-R4-R3
# Live Fragment Authority Corpus / Mismatch Telemetry / Performance Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R4-R3_LIVE_FRAGMENT_AUTHORITY_CORPUS_MISMATCH_TELEMETRY_PERFORMANCE_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4-R2_FOUR_ROUTE_TENSORCUBE_FRAGMENT_AUTHORITY_STREAM_COMMIT_PARITY_GATE`
- Runtime mode: `live_four_route_fragment_authority_corpus_mismatch_telemetry_performance`
- Cached authority: generation-buffered terminal commit
- Streaming authority: current-fragment compare-before-emit
- Legacy oracle: mandatory full dual-run
- Token/KV/sampler/RNG authority: existing production path only
- General production apply: false
- Legacy retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R4-R4_TENSORCUBE_DEFAULT_FRAGMENT_AUTHORITY_LEGACY_ORACLE_RETENTION_GATE`

## Purpose

R4-R4-R3 validates the R4-R4-R2 four-route fragment authority over a runtime-profile-bound corpus and records mismatch, revocation, output parity, latency, memory, and telemetry-integrity evidence.

```text
greedy cached
sampled cached
greedy streaming
sampled streaming
```

Cached routes retain candidate and legacy generation buffers and select one source at terminal. Streaming routes compute candidate and legacy fragments, compare before exposure, and emit exactly one current-fragment source.

## Parent admission

Inputs:

```text
--repo-root <PATH>
--r4-r4-r2-parent-manifest <PATH>
--runtime-profile <PATH>
```

The exact parent must prove:

```text
R4-R4-R2 PASS
execution_id="decode04r4r4r2-" + lineage_bundle_digest[0..20]
decode04_r4_r4_r3_authorized=true
tensorcube_four_route_fragment_authority_proven=true
tensorcube_streaming_fragment_authority=true
stream compare-before-emit=true
current-token oracle fallback=true
post-revocation legacy continuation=true
candidate byte leak=0
double emit=0
invalid UTF-8 stream chunk=0
stream chunk boundary parity=true
token/KV/sampler/RNG parity=true
general fragment authority=false
production apply=false
legacy retirement=false
```

Known parent:

```text
execution_id=decode04r4r4r2-3c901b5d87557d4ae6da
lineage_bundle_digest=3c901b5d87557d4ae6da5fa12ee6412c3b51b5d7f8f62e574aaf0e5932662ccf
```

## Operator seal

```text
--authorize-live-four-route-fragment-authority-corpus
```

The seal grants corpus execution, legacy-oracle dual-run, telemetry, and performance measurement. It grants no TensorCube token selection, sampler, RNG, KV, DecodeState, finish/stop, checkpoint, resume, candidate-only mode, general production apply, or legacy retirement.

## Identity binding

The gate binds:

```text
parent execution and lineage
parent manifest exact-file SHA-256
runtime profile exact-file SHA-256
model spec exact-file SHA-256
checkpoint path and non-zero size
model identity digest
tokenizer manifest exact-file SHA-256
tokenizer intrinsic identity
four-route policy digest
corpus manifest digest
performance policy digest
```

Changing model, checkpoint, tokenizer, parent, or route policy invalidates the evidence.

## Corpus plan

Required minimums:

```text
unique prompt identities >= 1700
total generation partitions >= 10000
generations per route >= 2500
corpus classes = 19/19
```

Classes:

```text
korean_general
english_general
korean_english_mixed
subtitle_short
subtitle_multiline
asr_noisy_input
numeric_and_punctuation
url_and_identifier
whitespace_stress
linebreak_stress
control_token_adjacent
byte_piece_stress
emoji_and_supplementary_plane
hangul_composition_stress
repetition_loop_stress
early_eos
max_token_termination
long_context
adversarial_mixed
```

Generation-length coverage includes 1-8, 9-32, 33-64, 65-128, and 129-256 selected-token bands.

## Ownership

The fragment gate receives selected token IDs and may not mutate token selection, KV, sampler, RNG, finish/stop, or route ownership.

Every natural corpus row requires:

```text
TensorCube candidate fragment
legacy oracle fragment
byte and state comparison
candidate commit or emit only after parity
zero natural fallback
zero natural revocation
legacy-baseline output parity
```

## Mismatch policy

Promotion budget:

```text
unexpected mismatch count=0
unexpected natural revocation count=0
production output divergence count=0
candidate byte leak count=0
```

Injected mismatch cases are tracked separately and must prove containment.

Cached containment:

```text
candidate output commit count=0
legacy rollback commit count=1
final output=legacy baseline
candidate byte leak=0
```

Streaming containment:

```text
mismatched candidate current-fragment emit count=0
oracle current-fragment emit count=1
candidate authority revoke count=1
candidate future run count=0
final stream=legacy baseline
```

## UTF-8 and stream integrity

Required:

```text
invalid UTF-8 count=0
partial scalar stream emit count=0
replacement fallback count=0
double emit count=0
missing visible emit count=0
stream chunk sequence parity=true
stream chunk boundary parity=true
stream finalization exactly once
```

Byte-carry-only tokens create a logical transaction and expose zero bytes until a complete scalar is materialized.

## Telemetry SSOT

```text
model_core::R4R4R3LiveCorpusClass
model_core::R4R4R3PromptEntry
model_core::R4R4R3LiveGenerationIdentity
model_core::R4R4R3LiveFragmentTelemetry
model_core::R4R4R3LiveGenerationReceipt
model_core::R4R4R3PerformanceSample
model_core::R4R4R3PercentileSummary
model_core::R4R4R3LiveCorpusSummary
model_core::r4r4r3_percentiles
orchestrator_local::run_r4_r4_r3_runtime
```

There is one canonical corpus reducer, percentile reducer, route policy, and promotion verdict path. Route-local mismatch or performance schemas are forbidden.

## Telemetry integrity

```text
generation receipt count=10000
fragment telemetry count=selected-token count
performance sample count=selected-token count
duplicate generation IDs=0
missing step IDs=0
orphan artifact references=0
telemetry integrity errors=0
```

Large JSONL artifacts are written separately. The local manifest contains summaries, lineage, artifact paths, and exact-file SHA-256 values.

## Performance policy

Required percentiles:

```text
p50
p90
p95
p99
max
```

Measured surfaces:

```text
TensorCube candidate fragment decode
legacy oracle fragment decode
comparison
cached stage or terminal commit
stream compare-before-emit and atomic emit
generation wall time
private fragment-authority memory
```

Default limits:

```text
candidate + oracle + comparison p99 <= 5 ms per selected token
stream added commit/emit p99 <= 5 ms per visible fragment
cached private dual-buffer peak <= 8 MiB
unbounded allocation count=0
normalized relative throughput floor >= 70% per route
```

Timing values are telemetry and excluded from execution identity.

## Production mutation boundary

Required zero counts:

```text
tensorcube_token_selection_count=0
tensorcube_sampler_use_count=0
tensorcube_rng_use_count=0
tensorcube_kv_mutation_count=0
tensorcube_decodestate_mutation_count=0
tensorcube_finish_stop_mutation_count=0
tensorcube_route_change_count=0
tensorcube_checkpoint_count=0
tensorcube_resume_count=0
```

Permitted TensorCube mutations are private fragment state, cached candidate terminal commit after full parity, streaming candidate emit after current-fragment parity, and telemetry-only state.

## No cleanup and no repair

Forbidden:

```text
String::from_utf8_lossy
U+FFFD replacement fallback
fragment trim
whitespace collapse
Unicode normalization
invalid-byte skip
silent token drop
silent fragment drop
silent mismatch suppression
legacy bytes copied into candidate and reported as candidate success
stream repair after exposure
prompt cleanup
```

## Artifacts

The Rust audit binary atomically writes parent, operator, runtime-profile, model, tokenizer, corpus, route, prompt, generation, fragment, performance, mismatch, route-summary, corpus-summary, output-parity, state-parity, UTF-8, sequence, finish, memory, VRAM-availability, telemetry-integrity, static, capability, mutation, no-repair, and promotion-verdict artifacts under `workspace/runtime/tensorcube/`.

The local manifest is written last. Runtime evidence is excluded from source-only archives.

## Binary

```text
ash_tcu_decode_04_r4_r4_r3_live_fragment_authority_corpus_mismatch_telemetry_performance_gate
```

## Execution identity

```text
decode04r4r4r3-<first 20 hex of lineage_bundle_digest>
```

Stable lineage binds parent, runtime profile, model and tokenizer identity, corpus and route policy, corpus summary, parity receipts, performance summary, memory summary, telemetry integrity, static structure, capability inventory, mutation audit, no-repair audit, and promotion verdict.

Paths, timestamps, raw timings, PIDs, pointers, allocation addresses, hostnames, temporary filenames, environment ordering, and scheduling noise are excluded.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R4_R3_LIVE_FRAGMENT_AUTHORITY_CORPUS_MISMATCH_TELEMETRY_PERFORMANCE_GATE
```

PASS requires:

```text
exact parent admission
explicit operator seal
runtime profile, model spec, checkpoint and tokenizer identity bound
1700 unique prompt identities
10000 generation partitions
2500 generations per route
19/19 corpus classes
all required length bands
unexpected mismatch=0
unexpected natural revocation=0
output divergence=0
candidate byte leak=0
double emit=0
missing emit=0
invalid UTF-8=0
partial scalar emit=0
replacement fallback=0
telemetry integrity errors=0
cached and streaming output parity=true
stream chunk sequence and boundary parity=true
fragment-layer token/KV/sampler/RNG mutation=0
injected mismatch containment=true
performance policy pass=true
zero cleanup or repair
all_truth_checks_pass=true
```

PASS grants only:

```text
decode04_r4_r4_r4_authorized=true
tensorcube_live_fragment_authority_corpus_proven=true
tensorcube_default_fragment_authority=false
tensorcube_general_fragment_authority=false
tensorcube_streaming_fragment_authority=true
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
production token/KV/sampler/RNG authority=false
```

HOLD or FAIL grants no additional authority.

## Next gate

```text
ASH-TCU-DECODE-04-R4-R4-R4
TensorCube Default Fragment Authority / Legacy Oracle Retention Gate
```

R4-R4-R4 may change the default fragment source to TensorCube while retaining the legacy oracle, fallback, mismatch telemetry, automatic authority revocation, and model/tokenizer identity invalidation. Legacy retirement remains forbidden.