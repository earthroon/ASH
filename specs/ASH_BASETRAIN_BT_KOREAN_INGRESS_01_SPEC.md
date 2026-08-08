# ASH-BASETRAIN-BT-KOREAN-INGRESS-01

## Runtime Korean Text Tokenization Authority / Frozen Tokenizer Identity Binding / Canonical Text-to-Token Candidate / Fixed-Q Pad-Suffix Model-Input Packet / Fixture Token SSOT Separation / No Model-Forward Mutation Seal

> Implementation parent: pass61 `ASH-BASETRAIN-INFERENCE-CANARY-01-D2`
> Runtime text mode: `korean_text_tokenizer_v1`
> Tokenizer identity SSOT: `ASH-TOK-TENSOR-00` + `R4R2R1TokenizerIdentityTruth`
> Tokenizer semantics SSOT: `tokenizer_core::NativeTokenizer`
> Candidate sequence SSOT: `BaseTrainRuntimeInputSequenceAuthority`
> Fixed geometry: B=1, Q=32
> Live model forward: blocked in this patch
> Proof ledger: HOLD

---

# 1. Goal

Replace synthetic CLI token-id authority with a reproducible Korean UTF-8 text-derived candidate authority without changing the physically admitted BaseTrain decoder path yet.

Canonical candidate flow:

```text
exact UTF-8 source file bytes
  -> BaseTrainRuntimeTextSourceAuthority
  -> frozen tokenizer_v5 identity truth
  -> tokenizer_core-owned normalization
  -> tokenizer_core-owned encode
  -> exact unpadded token ids
  -> fixed B1/Q32 packet
  -> manifest-owned PAD suffix
  -> row_valid_lengths=[N]
  -> derived position ids
  -> one BaseTrainRuntimeInputSequenceAuthority candidate
  -> BaseTrainKoreanIngressAuthority
```

No R6-R10, loss, backward, optimizer, sampling, generation, Hangul structure tensor, Cheon-Ji-In, or Q-wave execution is admitted here.

---

# 2. Source authority

Canonical source transport is one explicit UTF-8 file:

```text
--bt-korean-ingress-text-file
D:\1111113232\DUST\1\ash_pass3\workspace\runtime\basetrain\ingress_input.txt
```

Read raw bytes before any normalization. Seal:

```text
canonical path
byte count
raw byte SHA-256
UTF-8 validity
UTF-8 BOM presence
CR count
LF count
NUL count
```

Required:

```text
byte count > 0
valid UTF-8
BOM = 0
NUL count = 0
```

No trim, line-ending rewrite, BOM stripping, or Unicode normalization is performed by the orchestrator.

---

# 3. Frozen tokenizer authority

Exact manifest:

```text
D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json
```

Do not rederive tokenizer identity locally. Reuse:

```rust
build_r4r2_r1_tokenizer_identity_truth(...)
```

Required truth:

```text
identity_pass=1
frozen_reference_exact_file_sha256_match=1
frozen_reference_embedded_manifest_hash_match=1
frozen_reference_embedded_vocab_hash_match=1
frozen_exact_file_binds_reserved_hash_representation=1
manifest_intrinsic_core_contract_match=1
top_level_manifest_hash_absent=1
vocab_size_match=1
```

No alternate manifest search or tokenizer fallback.

---

# 4. Model vocabulary authority

The model vocabulary size is derived from the existing production-config authority:

```rust
BaseTrainAtlasWave02R5R6ProductionConfigAuthority::from_path(...)
```

The ingress gate does not run a model forward or load checkpoint tensor payloads merely to learn V.

Required:

```text
model config vocab == tokenizer trainer vocab
model config vocab == tokenizer vocab entry count
all encoded ids < model vocab
PAD id < model vocab
```

Current physical model observation is V=48259, but implementation derives it at runtime.

---

# 5. Tokenizer encode authority

`TokenizerEngine::encode()` remains semantic authority.

`tokenizer_core` adds a receipt-bearing path that shares the same internal implementation:

```rust
fn encode_canonical_with_normalized(...)
TokenizerEngine::encode(...)
NativeTokenizer::encode_with_authority(...)
```

Both public encode paths consume the same internal normalization/tokenization route.

`TokenizerEncodeAuthority` seals:

```text
tokenizer manifest id
tokenizer identity digest
source text SHA-256
normalized text SHA-256
normalized char/byte counts
token count
exact token ids
token ids digest
special-token insertion mode
authority digest
```

Required parity:

```text
TokenizerEngine::encode(text)
== encode_with_authority(text).token_ids
```

The orchestrator must contain no copy of tokenizer normalization, pretokenization, byte fallback, or piece matching logic.

---

# 6. Special-token policy

Preserve native tokenizer semantics:

```text
implicit BOS insertion = 0
implicit EOS insertion = 0
implicit task token insertion = 0
implicit language token insertion = 0
implicit control token insertion = 0
```

If input text literally names a special token and tokenizer_core encodes it, that is tokenizer output evidence, not orchestrator insertion.

---

# 7. Fixed geometry and overlength

Initial ingress geometry remains:

```text
B=1
Q=32
```

Let N be the exact unpadded encode token count.

Required:

```text
1 <= N <= 32
```

Failures:

```text
N=0  -> BTKoreanIngressEncodedTokenCountZero
N>32 -> BTKoreanIngressTokenCountExceedsFixedQ
```

No left/right/middle truncation, sliding window, alternate retokenization, or silent context repair.

---

# 8. PAD suffix authority

PAD id is read from:

```rust
manifest.special_tokens.pad.id
```

For N<32:

```text
padded_token_ids = exact encoded ids + PAD repeated (32-N)
row_valid_lengths = [N]
position_ids = [0..N-1] + zero repeated (32-N)
```

Required:

```text
valid prefix byte/ID equality with tokenizer output
PAD suffix exact
padded count=32
valid length=N
position ids derived, never CLI supplied
```

The ingress layer does not rewrite a PAD-valued id if tokenizer_core emitted it inside the valid prefix.

---

# 9. Candidate authorities

New model-core authorities:

```text
BaseTrainRuntimeTextSourceAuthority
BaseTrainKoreanIngressAuthority
```

Existing numerical candidate authority:

```text
BaseTrainRuntimeInputSequenceAuthority
```

Exactly one sequence authority is sealed per build.

`BaseTrainKoreanIngressAuthority` binds:

```text
source authority digest
tokenizer identity digest
tokenizer encode authority digest
model/tokenizer vocab sizes
B/Q/N
PAD id
unpadded/padded token digests
row-valid-length digest
position-id digest
logical attention-mask digest
padding policy
special-token policy
sequence authority digest
```

No text or structure authority silently reconstructs another layer's state.

---

# 10. Fixture separation

Text mode is:

```text
korean_text_tokenizer_v1
```

Historical synthetic token mode is quarantined as fixture-only.

The ingress gate fails if it receives explicit:

```text
--token-ids
--row-valid-lengths
--position-ids
```

for the same candidate operation.

The tokenizer output is the only numerical token source in text mode.

---

# 11. Reproducibility

The gate builds the complete candidate twice from the same source/config/tokenizer inputs.

Required:

```text
run_count=2
source authority match=1
tokenizer identity digest match=1
normalized text digest match=1
unpadded token ids match=1
padded token ids match=1
position ids match=1
sequence authority digest match=1
ingress authority digest match=1
```

Any mismatch fails:

```text
BTKoreanIngressReproducibilityMismatch
```

---

# 12. Dedicated gate

Binary:

```text
ash_basetrain_korean_ingress_01_gate
```

It is explicitly registered in `crates/orchestrator_local/Cargo.toml` because this crate uses an explicit `[[bin]]` registry.

Dedicated response file:

```text
specs/cli/ash_basetrain_korean_ingress_01.args
```

The response file references:

```text
${ASH_R5R6_PRODUCTION_CONFIG}
${ASH_R5R6_PRODUCTION_CONFIG_SHA256}
```

for the already-used production-config SSOT and uses explicit current-workspace source/manifest paths.

---

# 13. No model mutation boundary

Required counts:

```text
R6-R10 call=0
R6-R11 call=0
R6-R12 call=0
model forward=0
loss=0
backward=0
optimizer=0
weight mutation=0
```

This patch proves text-to-token candidate construction only.

Current R6-R6 fixture-only guards remain untouched. Real-text live forward adoption is a separate later boundary.

---

# 14. Runtime receipts

Default output directory:

```text
workspace/runtime/basetrain/korean_ingress/01
```

Receipts:

```text
source_receipt.json
tokenizer_encode_receipt.json
ingress_receipt.json
reproducibility_receipt.json
final_receipt.json
```

Raw source text and normalized text are not emitted by default. They may remain process-local for the next alignment stage.

---

# 15. Expected terminal evidence

```text
[bt-korean-ingress-01]
mode=korean_text_tokenizer_v1
source_utf8_valid=1
source_utf8_bom=0
source_byte_count=<runtime>
model_vocab_size=48259
tokenizer_vocab_size=48259
tokenizer_identity_bound=1
normalization_owner=tokenizer_core
encode_owner=tokenizer_core
implicit_bos=0
implicit_eos=0
encoded_token_count=<N>
batch_size=1
seq_len=32
valid_token_count=<N>
padded_token_count=32
pad_suffix_count=<32-N>
position_ids_derived=1
sequence_authority_publication=1
reproducibility_runs=2
reproducibility_match=1
fixture_token_authority_used=0
model_forward=0
loss=0
backward=0
optimizer=0
weight_mutation=0
source_authority_digest=<sha256>
tokenizer_encode_authority_digest=<sha256>
sequence_authority_digest=<sha256>
ingress_authority_digest=<sha256>
proof_ledger=HOLD
```

N is deliberately runtime-derived from the user-supplied text file.

---

# 16. PASS token

```text
PASS_ASH_BASETRAIN_BT_KOREAN_INGRESS_01_EXACT_UTF8_SOURCE_FILE_AUTHORITY_RAW_BYTE_DIGEST_BEFORE_NORMALIZATION_FROZEN_TOKENIZER_V5_IDENTITY_REUSED_FROM_ASH_TOK_TENSOR_00_AND_R4R2R1_TRUTH_ZERO_LOCAL_MANIFEST_HASH_REDERIVATION_MODEL_TOKENIZER_VOCAB_EXACT_BINDING_TOKENIZER_CORE_SINGLE_NORMALIZATION_OWNER_TOKENIZER_CORE_SINGLE_ENCODE_OWNER_ZERO_ORCHESTRATOR_NORMALIZATION_ZERO_TOKEN_ID_OVERRIDE_ZERO_IMPLICIT_BOS_EOS_CONTROL_INSERTION_NONEMPTY_EXACT_UNPADDED_TOKEN_SEQUENCE_RUNTIME_DERIVED_VALID_TOKEN_COUNT_FIXED_B1_Q32_GEOMETRY_ZERO_TRUNCATION_MANIFEST_PAD_ID_RIGHT_SUFFIX_PADDING_VALID_LENGTH_EQUALS_UNPADDED_TOKEN_COUNT_DETERMINISTIC_VALID_POSITION_IDS_AND_ZERO_PAD_POSITION_IDS_SINGLE_BASETRAIN_RUNTIME_INPUT_SEQUENCE_AUTHORITY_CANDIDATE_SEAL_SOURCE_TOKENIZER_ENCODE_PADDING_POSITION_AND_SEQUENCE_DIGEST_LINEAGE_SAME_TEXT_SAME_TOKENIZER_SAME_GEOMETRY_DOUBLE_BUILD_REPRODUCIBILITY_EXACT_FIXTURE_TOKEN_AUTHORITY_EXPLICITLY_SEPARATE_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 17. Implementation surface

Pass62 changes only:

```text
crates/tokenizer_core/src/lib.rs
crates/model_core/src/lib.rs
crates/model_core/src/base_train_runtime_text_source_authority.rs
crates/model_core/src/base_train_korean_ingress_authority.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_korean_ingress_01.rs
crates/orchestrator_local/src/bin/ash_basetrain_korean_ingress_01_gate.rs
specs/cli/ash_basetrain_korean_ingress_01.args
```

Static closure before physical execution: `42/42 PASS`.

---

# 18. Package hygiene

Baked ZIP excludes:

```text
*.md
*.sha256
artifacts/
manifests/
runtime receipts
checkpoint weights copied for this patch
tokenizer manifest copy
source text copy
KSS corpus
```

The tokenizer manifest and text source remain external SSOT inputs.

---

# 19. Admission state

After physical PASS:

```text
Existing R6-R10 fixed-token forward = unchanged ADMITTED
INFERENCE-CANARY-01 = unchanged ADMITTED
BT-KOREAN-INGRESS-01 text->token candidate = ADMITTED
Real-text R6-R10 adoption = BLOCKED
Token/surface/syllable alignment = next boundary
Cheon-Ji-In basis = BLOCKED
Q-wave conditioning = BLOCKED
CANARY-02 = BLOCKED
Production inference = BLOCKED
Proof ledger = HOLD
```

---

# 20. Natural next boundary

```text
BT-TOKEN-SPAN-ALIGNMENT-02

Korean Ingress Exact Parent /
Normalized Text Exact Binding /
Tokenizer Token Sequence Exact Binding /
Vocab Piece Decode Surface /
Token Position to Text Surface Range /
Multi-Syllable Token Preservation /
Hangul Scalar Extraction /
Token-to-Syllable Ownership Ledger /
No One-Token-One-Syllable Assumption /
No Hangul Tensor Aggregation Yet /
No Q-wave Yet Seal
```

---

# 21. Architecture seal

BT-KOREAN-INGRESS-01 creates one reproducible Korean text-derived numerical candidate without disturbing the proven decoder. Raw UTF-8 bytes are sealed before normalization; tokenizer identity is delegated to the already frozen ASH-TOK-TENSOR-00/R4R2R1 authority; tokenizer_core alone owns normalization and encoding; the encoded sequence receives no implicit orchestrator special tokens and is never truncated; fixed Q32 geometry is satisfied only by exact manifest-PAD right suffix; valid length and position ids are deterministic; one runtime input sequence candidate is sealed and double-built for exact reproducibility. The historical synthetic token fixture remains isolated, and live forward adoption plus Hangul/Cheon-Ji-In/Q-wave work stay behind later explicit gates.