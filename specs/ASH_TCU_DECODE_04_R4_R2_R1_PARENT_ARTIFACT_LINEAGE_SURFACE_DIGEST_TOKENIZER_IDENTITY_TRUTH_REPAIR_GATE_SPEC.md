# ASH-TCU-DECODE-04-R4-R2-R1
# Parent Artifact Lineage / Surface Digest / Tokenizer Identity Truth Repair Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R2-R1_PARENT_ARTIFACT_LINEAGE_SURFACE_DIGEST_TOKENIZER_IDENTITY_TRUTH_REPAIR_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R2_SHADOW_SELECTED_TOKEN_DECODE_SURFACE_AND_SPECIAL_TOKEN_CLASSIFICATION_NON_EMIT_GATE`
- Runtime mode: `artifact_only_lineage_truth_repair`
- Production authority: `false`
- Token append authority: `false`
- KV mutation authority: `false`
- Text emit authority: `false`
- Special-token semantic authority: `false`
- PASS authorizes: `ASH-TCU-DECODE-04-R4-R2-R2`
- Direct R4-R3 promotion: `forbidden`
- Workspace/runtime dependency repair: out of scope; the canonical local workspace is assumed to exist.

## 1. Purpose

R4-R2 already produces a selected-token decode surface and special-token classification. This gate does not add another decode feature. It repairs the proof chain beneath that result.

The gate must recompute and prove all of the following from exact artifact bytes and typed content:

1. R4-R1 and R4-R2 execution identities.
2. R4-R1 standalone artifact path, byte SHA-256, schema, and embedded-content parity.
3. The canonical digest of the complete 64-entry parent Top-K surface.
4. The selected token's rank, ID, raw logit, adjusted logit, probability, and CDF binding.
5. Tokenizer manifest/spec exact-file and embedded structural identities.
6. Zero production mutation while the truth receipts are generated.

The existing R4-R2 boolean `parent_surface_digest_continuity=true` is an observed legacy claim only. It must never be accepted as proof.

## 2. SSOT

| Domain | SSOT |
|---|---|
| R4-R1 execution | typed R4-R1 local manifest plus `r4r1_execution_seed(runtime)` |
| R4-R2 execution | typed R4-R2 local manifest plus `r4r2_execution_seed(runtime)` |
| Parent surface | standalone typed R4-R1 parent-surface receipt |
| Surface digest | canonical encoding of all 64 entries |
| Selection | standalone typed R4-R1 selection receipt |
| Canonical stochastic fixture | embedded `F2_canonical_stochastic` adapter/oracle fixture |
| Non-commit state | standalone and embedded typed-equal R4-R1 non-commit audit |
| Tokenizer file identity | exact manifest/spec bytes |
| Tokenizer structural identity | parsed `TokenizerManifest` and `TokenizerSpec` |
| Manifest self hash | canonical manifest serialization with `hashes.manifest_hash` cleared |

Forbidden substitutes:

- trusting legacy continuity booleans
- filename equality without canonical path identity
- token-ID-only binding
- float-to-string comparison
- generic JSON key-order-dependent identity seeds
- silent missing-field defaults
- `<unk>` fallback
- parent or tokenizer artifact rewrite

## 3. Required inputs

```text
--repo-root <PATH>
--r4-r2-parent-manifest <PATH>
--r4-r1-parent-manifest <PATH>
--r4-r1-parent-surface-receipt <PATH>
--r4-r1-selection-receipt <PATH>
--r4-r1-oracle-parity-receipt <PATH>
--r4-r1-non-commit-audit <PATH>
--tokenizer-manifest <PATH>
--tokenizer-spec <PATH>
```

All relative paths resolve against `--repo-root`. Every supplied R4-R1 artifact must resolve to the same canonical target declared by the R4-R1 manifest. All resolved inputs must remain inside the canonical repository root.

## 4. Required seals

The binary must require all activation and non-mutation seals explicitly:

```text
--activate-parent-artifact-lineage-truth-repair
--activate-parent-surface-digest-recompute
--activate-canonical-selection-full-binding
--activate-tokenizer-identity-recompute

--require-parent-r4-r2-pass
--require-parent-r4-r1-pass
--require-parent-report-execution-id-recompute
--require-parent-artifact-path-identity
--require-parent-artifact-byte-sha256
--require-parent-embedded-standalone-content-parity
--require-parent-surface-canonical-order
--require-parent-surface-digest-three-way-parity
--require-selected-rank-entry-binding
--require-selected-probability-and-cdf-binding
--require-canonical-fixture-adapter-oracle-binding
--require-tokenizer-file-sha256
--require-tokenizer-embedded-manifest-hash-parity
--require-tokenizer-vocab-hash-parity
--require-tokenizer-reserved-hash-parity
--require-tokenizer-spec-hash-parity
--require-tokenizer-core-contract-parity

--require-no-parent-artifact-write
--require-no-tokenizer-write
--require-no-checkpoint-read
--require-no-gpu-dispatch
--require-no-production-sampler-use
--require-no-production-rng-use
--require-no-token-append
--require-no-kv-append
--require-no-eos-stop-transition
--require-no-text-emit
--require-no-stream-emit
--require-no-runtime-output-change
--require-no-production-route-change

--write-runtime-artifacts
--write-local-manifest

--require-topk-entry-count 64
--require-unique-token-count 64
--require-tokenizer-vocab-size 48259
--require-max-probability-abs-error 0.000000000001
--require-max-cdf-abs-error 0.000000000001
```

Missing or altered required values fail closed.

## 5. Rust-owned outputs

The Rust binary is the only producer of the manifest and evidence artifacts. No generated JSON is baked into the source ZIP.

```text
workspace/runtime/tensorcube/
  ash_tensorcube_decode_04_r4_r2_r1_local_manifest_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_parent_execution_truth_receipt_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_parent_artifact_lineage_receipt_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_surface_digest_truth_receipt_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_canonical_selection_truth_receipt_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_tokenizer_identity_truth_receipt_latest.json
  ash_tensorcube_decode_04_r4_r2_r1_non_mutation_audit_latest.json
```

Write protocol:

```text
serialize typed value to pretty JSON bytes
write <target>.tmp
flush
sync_all
remove existing target only after the complete temp write
rename temp to target
write the local manifest last
```

If any output resolves to a parent artifact, tokenizer manifest, or tokenizer spec path, execution fails before writing.

## 6. Parent execution truth

### R4-R1

Recompute with:

```rust
r4r1_execution_seed(&parent_r4_r1.runtime)
```

Expected ID:

```text
"decode04r4r1-" + seed_sha256[0..20]
```

### R4-R2

Promote the R4-R2 digest logic to:

```rust
pub fn r4r2_execution_seed(runtime: &R4R2RuntimeReceipt) -> Result<String>;
```

Expected ID:

```text
"decode04r4r2-" + seed_sha256[0..20]
```

The following identities must match:

```text
R4-R1 report execution ID
R4-R2 report parent execution ID
R4-R2 runtime parent execution ID
```

Both parents must have exact PASS status, expected verdict, route digest, and non-production authority.

## 7. Parent artifact lineage

Required standalone R4-R1 artifacts:

1. parent surface
2. canonical selection
3. oracle parity
4. non-commit audit

For each artifact record and verify:

```text
declared path
supplied path
declared canonical path
supplied canonical path
canonical path equality
exact byte length
exact file SHA-256
embedded typed-content digest
standalone typed-content digest
embedded/standalone typed equality
exact schema
```

The R4-R2 parent receipt's recorded R4-R1 manifest, selection, oracle, and non-commit SHA-256 values must equal the exact supplied files.

`lineage_pass=true` requires exactly four observations and zero path, schema, SHA, or typed-content mismatches.

## 8. Canonical surface truth

The surface must contain exactly 64 entries and 64 unique token IDs. For each index `i`:

```text
entry.rank == i
entry.token_id < 48259
entry.logit is finite
entries are descending by logit
bit-equal logit ties are ascending by token ID
```

Canonical entry bytes:

```text
rank as u64 little-endian
|| token_id as u32 little-endian
|| f64::to_bits(logit) as u64 little-endian
```

Surface digest:

```text
SHA-256(concatenated canonical bytes for all 64 entries)
```

The recomputed digest must equal:

- embedded R4-R1 parent-surface digest
- standalone R4-R1 parent-surface digest
- legacy R4-R2 parent-surface digest

The embedded and standalone entry vectors must also be typed-equal.

The R4-R2 legacy continuity claim is recorded as observed but never trusted:

```text
parent_r4_r2_legacy_surface_continuity_claim_observed=true
parent_r4_r2_legacy_surface_continuity_claim_trusted=false
```

## 9. Canonical selection truth

The canonical fixture must be exactly:

```text
F2_canonical_stochastic
```

The canonical draw index must match the R4-R1 runtime draw receipt.

The standalone selection must be typed-equal to:

- the embedded canonical R4-R1 selection
- the canonical fixture adapter selection

The fixture oracle must match the selection for:

- token ID
- parent rank
- probability within `1e-12`
- CDF start/end within `1e-12`

The selected rank must exist in the 64-entry surface. The rank entry must match selected token ID exactly and selected raw logit by `f64::to_bits`.

The legacy R4-R2 selected token ID, rank, probability, and non-commit flag must match the standalone R4-R1 selection. `commit_authorized` must remain false.

## 10. Tokenizer identity truth

Read exact tokenizer manifest and tokenizer spec bytes and parse typed values.

Required recomputation:

```text
manifest_exact_file_sha256 = SHA-256(exact manifest bytes)
spec_exact_file_sha256 = SHA-256(exact spec bytes)

canonical_manifest = manifest.clone()
canonical_manifest.hashes.manifest_hash = ""
recomputed_manifest_hash = SHA-256(serde_json::to_vec(canonical_manifest))

recomputed_vocab_hash = SHA-256(serde_json::to_vec(manifest.vocab))
recomputed_reserved_hash = SHA-256(serde_json::to_vec(manifest.reserved_tokens))
recomputed_spec_hash = SHA-256(serde_json::to_vec(spec))
```

The recomputed values must match:

- `manifest.hashes.manifest_hash`
- `manifest.hashes.vocab_hash`
- `manifest.hashes.reserved_tokens_hash`
- `manifest.lineage.tokenizer_spec_hash`

Core contract parity must include:

```text
manifest.tokenizer_spec_id == spec.tokenizer_spec_id
trainer kind
trainer vocab size == 48259
manifest vocab entry count == 48259
character coverage bit equality
seed equality
byte-fallback equality
PAD token and ID 0
BOS token and ID 1
EOS token and ID 2
UNK token and ID 3
```

A legacy top-level raw JSON key named `manifest_hash` is forbidden. The self hash may exist only under `hashes.manifest_hash`.

The R4-R2 tokenizer receipt must resolve to the same canonical manifest path and match exact file SHA-256, manifest ID, and tokenizer spec ID.

## 11. Non-mutation seal

All counters remain zero:

```text
checkpoint_open_count
checkpoint_range_read_count
gpu_dispatch_count
production_sampler_use_count
production_rng_read_count
production_rng_advance_count
parent_artifact_write_count
tokenizer_write_count
token_append_attempt_count
kv_append_attempt_count
finish_reason_change_count
stop_state_change_count
text_emit_attempt_count
stream_emit_attempt_count
production_route_change_count
```

And:

```text
runtime_output_changed=false
all_state_unchanged=true
```

This proves that the artifact-only gate receives no production authority. It does not claim live DecodeState or KV snapshot parity. That claim belongs to R4-R2-R2.

## 12. PASS, HOLD, FAIL

### PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R2_R1_PARENT_ARTIFACT_LINEAGE_SURFACE_DIGEST_TOKENIZER_IDENTITY_TRUTH_REPAIR_GATE
```

Verdict:

```text
decode04_r4_r2_r1_parent_lineage_surface_digest_tokenizer_identity_truth_repair_pass
```

PASS requires every execution, lineage, surface, selection, tokenizer, and non-mutation check to pass.

PASS authority:

```text
production_authority=false
token_append_authorized=false
kv_mutation_authorized=false
text_emit_authorized=false
special_token_semantic_authority=false
decode04_r4_r2_r2_authorized=true
decode04_r4_r3_authorized=false
```

### HOLD

Missing or mismatched input evidence must fail closed with a typed `r4r2r1_hold:*` reason. Required categories include:

```text
r4_r1_execution_id_mismatch
r4_r2_execution_id_mismatch
parent_execution_id_mismatch
declared_supplied_path_mismatch
embedded_standalone_content_mismatch
surface_entry_count_mismatch
surface_unique_token_count_mismatch
surface_rank_violation
surface_order_violation
surface_digest_parity_mismatch
selected_rank_entry_id_mismatch
selected_rank_entry_raw_logit_mismatch
fixture_oracle_probability_mismatch
fixture_oracle_cdf_mismatch
tokenizer_manifest_hash_mismatch
tokenizer_vocab_hash_mismatch
tokenizer_reserved_hash_mismatch
tokenizer_spec_hash_mismatch
tokenizer_core_contract_mismatch
```

### FAIL

Forbidden mutation, output overlap, or internal determinism failure must produce a typed `r4r2r1_fail:*` reason. Required categories include:

```text
output_target_overlaps_protected_input
parent_artifact_write_observed
tokenizer_write_observed
checkpoint_read_observed
gpu_dispatch_observed
production_sampler_observed
production_rng_observed
token_append_observed
kv_append_observed
text_emit_observed
stream_emit_observed
runtime_output_changed
production_route_changed
```

## 13. Execution order

```text
1. CLI requirement seal
2. exact input-byte reads
3. typed parsing
4. R4-R2 execution-ID recompute
5. R4-R1 execution-ID recompute
6. parent execution/route/authority checks
7. canonical path identity checks
8. exact parent byte-SHA checks
9. embedded/standalone typed-content parity
10. surface canonical validation and digest recompute
11. selected-token full binding
12. tokenizer exact-byte and structural identity recompute
13. non-mutation audit
14. lineage-bundle digest
15. R4-R2-R1 execution ID
16. truth receipt atomic writes
17. local manifest atomic write last
```

The PASS local manifest must never be written before every truth receipt has been built successfully.

## 14. Regression and determinism

Required positive cases:

- canonical current R4-R1/R4-R2/tokenizer bundle
- relative and normalized path spellings resolving to the same target
- repeated execution with identical identity digests

Required HOLD cases:

- one surface-logit bit flip
- surface reorder
- swapped selection/oracle/non-commit artifact
- same token ID with wrong rank
- same ID/rank with wrong probability or CDF
- embedded/standalone content mismatch
- tokenizer manifest self-hash mutation
- vocab or reserved-token content/hash mutation
- tokenizer spec mismatch
- top-level legacy `manifest_hash`

Run the same exact input bundle ten times. These values must remain identical:

```text
R4-R1 recomputed execution ID
R4-R2 recomputed execution ID
recomputed surface digest
selection truth digest
tokenizer identity digest
lineage bundle digest
R4-R2-R1 execution ID
```

Wall-clock time and file timestamps must not enter any identity seed.

## 15. Definition of done

- [ ] R4-R1 and R4-R2 execution IDs are recomputed from typed runtime receipts.
- [ ] Parent surface is a required standalone input.
- [ ] Four parent declared paths equal supplied canonical paths.
- [ ] Four standalone artifacts are typed-equal to embedded runtime objects.
- [ ] Parent SHA values recorded by R4-R2 equal supplied exact files.
- [ ] Surface digest is recomputed from all 64 canonical entries.
- [ ] Embedded, standalone, legacy, and recomputed surface digests match.
- [ ] Selected token is bit-exactly bound to its parent rank entry.
- [ ] Selected probability/CDF matches canonical adapter/oracle within `1e-12`.
- [ ] Tokenizer manifest self, vocab, reserved, and spec hashes are recomputed.
- [ ] Tokenizer core trainer and special-token contracts match.
- [ ] Parent and tokenizer write counts remain zero.
- [ ] GPU, checkpoint, sampler, RNG, token, KV, finish, emit, and route mutation counts remain zero.
- [ ] Rust writes all evidence artifacts and the local manifest atomically.
- [ ] The source bake contains no pre-generated manifest or runtime evidence artifact.
- [ ] R4-R2 direct R4-R3 authorization is disabled.
- [ ] PASS authorizes only R4-R2-R2.
