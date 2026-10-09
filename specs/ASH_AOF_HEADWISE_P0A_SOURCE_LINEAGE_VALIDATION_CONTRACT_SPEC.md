# ASH-AOF-HEADWISE-P0-A
## HISTORICAL / CURRENT SOURCE-LINEAGE VALIDATION CONTRACT RECONCILIATION

**Class:** diagnostic/source-lineage authority repair; no runtime semantic change  
**Parent:** `ASH_PASS3_HEADWISE_R3_CF4_CURRENT_SOURCE_HEAD_CHECKPOINT_LINEAGE_QUALITY_CODE_ONLY.zip`  
**Parent SHA-256:** `6f6ac28b6196104064893cbd81ac8bd2ef85d0c2e1d0ed2faef14c3a76bda01b`  
**Parent entries:** 8,755; archive CRC: PASS  
**Dependency:** none of P0-B's GPU tests; P0-A supplies the exact source-lineage classification P0-B may consume  
**Status (2026-10-09): PARTIAL SOURCE BAKE / STATIC 60/60 PASS; lineage negative 25/25 rejected, original AOF R3 negative 15/15 rejected.** Rust COMPILE, Naga, real WGPU PHYSICAL and checkpoint training/load NOT_RUN. Historical archive not materialized; see exact SOURCE-bake annex. This status is *not* a production approval.

```text
ASH-AOF-HEADWISE-P0-A

HISTORICAL / CURRENT SOURCE-LINEAGE CONTRACT RECONCILIATION

+ HISTORICAL e20f... CHECKPOINT / SOURCE BASELINE PRESERVATION
+ CURRENT CF2/CF3/CF4 0b10... 19-INPUT BYTE AUTHORITY
+ TRAINING-SOURCE / RUNTIME-SOURCE / BINARY / CHECKPOINT IDENTITY SEPARATION
+ AOF CF5-C-R3 STALE STATIC PREDICATE EXPLICIT SUPERSESSION
+ NO LITERAL REPLACEMENT AS CHECKPOINT EQUIVALENCE
+ EXISTING SELECTED-ROUTE NEGATIVE GATES PRESERVATION
+ VALIDATED LINEAGE CLASSIFICATION WITH NOT_RUN / HOLD TRUTH
+ NO LEGACY CHECKPOINT MANIFEST RESEAL
+ NO STATIC-TO-RUNTIME / PHYSICAL PROMOTION
+ NO HEADWISE, FUTUREPOOL, KV, TOKEN, STOP, EMIT CHANGE
+ NO CF5-D ACTIVE
```

---

## 0. Exact observed baseline

On the **CF4 full ZIP**, `tools/validate_ash_aof_r1_cf5_c_r3_selected_route_static.py` returns:

```text
R3 STATIC 59/60 FAIL ['checkpoint_training_19_source_exact']
TRAINING_SOURCE_DIGEST 0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094 INPUTS 19
```

The same source tree's Headwise CF3 static validator reports `32/32 PASS`, and CF4's validator returns its source/static PASS. These are static observations only. The AOF R3 validator's line 6 pins:

```text
TRAINING_DIGEST='e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283'
```

It later evaluates `training_digest()[0] == TRAINING_DIGEST` unconditionally, even while operating on the newer CF4 tree. The first digest is the **historical** 19-input training source. CF2 intentionally changed `crates/model_core/src/native_wgpu.rs`, one of those 19 inputs; the second digest describes the **current** CF2-and-later source lineage.

This is a **scope conflict between historical validator baseline and current checkout**, not evidence of a failed GPU dispatch. Neither digest is a substitute for real checkpoint weights.

## 1. Authority domains, never conflated

| Authority | Actual source | Meaning |
|---|---|---|
| Training source | `model_core::aof_r1_shared_lm_head_math::shared_lm_training_source_digest()` | ordered byte content of 19 `include_bytes!` inputs |
| Historical training source | archived parent 19-input byte set, when physically available | can authenticate historical source ONLY |
| Runtime source | `model_core::aof_r1_admission::ark_runtime_source_digest()` | broader runtime code/shader implementation; separate domain |
| Qualification source | P0-A verifier and its own source bytes | proof logic revision only, not model-training provenance |
| Binary | SHA-256 of actual executable used | compiled artifact; not inferred from source |
| Checkpoint | actual safetensors SHA-256 + sealed manifest | real trained head weights and their provenance |
| Native execution | real session, Device/Queue, loaded checkpoint, completed observation | never derived from source hash |

An exact file hash does not by itself prove execution, semantic compatibility, or trained checkpoint validity.

## 2. Immutable named lineage identifiers

```text
HistoricalPreCf2:
  e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283

CurrentCf2Source:
  0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
```

A new source digest other than either value must be classified `UNKNOWN_NEW_SOURCE`, not automatically added to a trusted digest set. A future lineage requires separate source attribution and explicit user-authorized transition. P0-A does **not** whitelist arbitrary checkpoints on the basis that their manifest spells either digest.

## 3. Canonical 19-input hashing contract

Derive the list from the actual `source!("...")` invocations within `shared_lm_training_source_digest()`; preserve its order and literal spelling. For each named input, hash:

```text
u64_le(path_utf8_len)
path_utf8_bytes
u64_le(file_byte_len)
file_bytes
```

The concatenation is SHA-256 hashed. Preserve all **19** inputs, including `native_wgpu.rs` and `Cargo.lock`. No sorted order, normalized path spelling, content-string reserialization, symlink substitution, or omission of the root lock file. Report per-input SHA-256 and the first byte-changing file when comparing parent and child source trees.

A verifier reading the current files is independent evidence of what those bytes are, but `current_digest == newly_computed_digest` alone is tautological. Check it against the frozen, source-backed **CF2 current baseline**, including exact parent provenance and per-input bytes. If any 19-input bytes changed after CF2, do not claim the frozen current digest still binds those bytes.

## 4. Separate current and historical predicates

Replace the overloaded `checkpoint_training_19_source_exact` semantic check with **two distinct authorities** (proposed typed states; exact names may reuse existing types):

```rust
enum HeadTrainingLineageClass {
    HistoricalPreCf2,
    CurrentCf2,
    UnknownNewSource,
}

enum HeadTrainingSourceObservation {
    Exact19InputBytes,
    Mismatched { first_path: String },
    SourceUnavailable,
}

enum HeadCheckpointObservation {
    NotProvided,
    ManifestBound,
    CheckpointBytesVerified,
    NativeLoadedAndExecuted,
    Rejected { reason: String },
}
```

These types are **proposed**, not claimed present in the ZIP.

- **Current checkout gate:** require current source byte authority and `0b10...`. An exact current checkout yields `CURRENT_SOURCE_EXACT`, not `CURRENT_CHECKPOINT_VALID`.
- **Historical gate:** retain `e20f...` as immutable reference; only execute exact historic 19-byte-source comparison when an actual historical source tree/archive is provided and verified. On the CF4 checkout without historical bytes, report `HISTORICAL_NOT_EXECUTED_HERE` (not PASS).
- **Legacy-source test replay:** remains able to verify the old source under the exact historic input set, without pretending that checkout is CF4.
- **Unexpected source:** reject current-lineage claims, report the exact changed path and digest, then HOLD.

Do not replace the old literal in place and falsely report that all historical assertions passed. The AOF R3 aggregate should show current-applicable checks and historical observations as **separate totals**. Previously valid route predicates and negative mutations remain enabled.

## 5. Checkpoint admission is a third, independent gate

A checkpoint is accepted into an execution arm only after all of the following:

1. Real checkpoint bytes exist and their SHA-256 matches their bound manifest.
2. The canonical model/tokenizer/dataset/rank/training source provenance is checked by the existing strict loader and CF4 contract.
3. `checkpoint.manifest.training.source_digest` is verified against the **source that actually trained those weights**, not an arbitrary caller-chosen digest string.
4. Native loading and the actual forward/Queue completion are observed before claiming GPU execution.
5. The W8/W9A join and CF3 selected-output parity remain separately qualified.

A historical checkpoint is **not adopted** into current CF2 code merely because P0-A knows both source digest values. Do not rewrite `training.source_digest`, reuse an old manifest under a new filename, disable strict source validation, or create a compatibility-mode default. An explicitly approved migration would be an independent later patch with genuine equivalence/provenance evidence.

## 6. Minimal implementation touch points

**Expected narrow edit:**

```text
tools/validate_ash_aof_r1_cf5_c_r3_selected_route_static.py
```

**Optional new qualification-only verifier, only if the existing script would become ambiguous:**

```text
tools/validate_ash_aof_headwise_p0a_lineage_contract_static.py
```

**Read-only source authorities:**

```text
crates/model_core/src/aof_r1_shared_lm_head_math.rs
crates/model_core/src/aof_r1_admission.rs
crates/orchestrator_local/src/headwise_r3_cf4_checkpoint_lineage.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/src/aof_r1_cf5_qualification_cli.rs
```

No P0-A changes to the 19 training inputs, production Rust model files, WGSL, checkpoint contents, optimizer, sampling, KV storage, or runtime admission. New verifier files are included in **their own** qualification-source digest, not smuggled into the historical training digest. If scope unexpectedly requires modifying a hashed training file, stop and declare a new lineage rather than continuing under `0b10...`.

## 7. Result/receipt schema (proposed)

File: `aof_headwise_p0a_source_lineage_contract_receipt.json`

```text
schema: ash.aof_headwise.p0a.lineage.v1
parent_archive_sha256
parent_archive_entries
qualification_source_digest
checkout_source_identity
training_input_count (=19)
ordered_input_path_and_sha256[]
current_expected_digest
current_observed_digest
current_source_status
historical_expected_digest
historical_observed_digest: null unless historical bytes were actually read
historical_source_status
runtime_source_digest: null unless genuinely computed
checkpoint_status: NotProvided / ...
checkpoint_manifest_sha256: null unless read
checkpoint_bytes_sha256: null unless read
native_load_status: NOT_RUN
selected_cf3_gpu_status: NOT_RUN
w8_w9a_physical_status: NOT_RUN
original_aof_r3_route_gate_status
source_gate_applicable_count
source_gate_passed_count
first_failure_class: null | string
source_static_only: true
receipt_sha256
```

Never use a literal `0` in an unobserved measurement field, nor a `true` physical status produced from static source comparison. A JSON receipt is audit data, not live WGPU resource authority.

## 8. Fail-closed negative matrix

| Negative | Required result |
|---|---|
| Current CF4 tree checked as `HistoricalPreCf2` | source mismatch, not historical PASS |
| Old source tree checked as `CurrentCf2` | source mismatch, not current PASS |
| Caller supplies matching digest but one input byte differs | reject |
| `native_wgpu.rs` changed, digest constant unchanged | reject |
| `Cargo.lock` changed, digest constant unchanged | reject |
| 18 or 20 hashed inputs / reordered inputs | reject |
| Same bytes, different digest encoding recipe | reject |
| Historical checkpoint manifest relabelled to current source | reject |
| New manifest with no checkpoint bytes | `CHECKPOINT_NOT_MATERIALIZED` |
| Real checkpoint bytes but no native load | `NATIVE_NOT_RUN` |
| CF3 static PASS relabelled GPU PASS | reject |
| CF2 W8 join SOURCE relabelled physical PASS | reject |
| AOF CF5-D ACTIVE set without consumer gates | reject |
| Removed pre-existing AOF R3 route-negative guard | reject regression |

Static mutations qualify a *validator*, not the runtime behavior of the GPU.

## 9. Source/static acceptance sequence

From the exact CF4 checkout (all relative paths below are real; optional new script is a proposed file and **does not yet exist**):

```powershell
python .\tools\validate_ash_headwise_r3_cf2_same_invocation_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf3_selected_reference_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py --negative-tests

# After P0-A source bake:
python .\tools\validate_ash_aof_r1_cf5_c_r3_selected_route_static.py --negative-tests
python .\tools\validate_ash_aof_headwise_p0a_lineage_contract_static.py --negative-tests
```

Only invoke the last command if that new file is created; otherwise use the actual modified validator. Require strict current-lineage binding, zero newly false-accepted mutations, and unchanged route/consumer negative gates. A new result must not silently reinterpret earlier `59/60 FAIL` as a historic `60/60 PASS`; the versioned receipt reports *why the evaluation domain changed*.

## 10. Native acceptance boundary

```powershell
cargo metadata --format-version 1 --locked
cargo check -p model_core --lib --release --locked -j 1
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
```

These commands are **acceptance steps, not executed results**. Resolve `vendor/sherpa-rs-main/crates/sherpa-rs` from the correct existing dependency source if missing. Do not use a dummy crate, silently change a version, or delete the dependency. Since P0-A is a source-lineage verifier correction, Naga/real GPU physical evidence is explicitly **independent**.

## 11. PASS / HOLD tokens

A new P0-A **source-only** pass may be emitted as:

```text
PASS_AOF_HEADWISE_P0A_CURRENT_SOURCE_LINEAGE_STATIC
```

only with all relevant static checks and negatives, current 19-input digest, and current-source identity binding. Historical evidence may independently emit `PASS_AOF_HEADWISE_P0A_HISTORICAL_SOURCE_REPLAY` **only after archived historic source bytes were actually replayed**. Otherwise report `HOLD_AOF_HEADWISE_P0A_HISTORICAL_SOURCE_NOT_MATERIALIZED` for that optional arm.

Mandatory first-failure classes:

```text
FAIL_P0A_TRAINING_INPUT_SET_DRIFT
FAIL_P0A_TRAINING_SOURCE_DIGEST_DRIFT
FAIL_P0A_HISTORICAL_LINEAGE_MISCLASSIFIED
FAIL_P0A_CHECKPOINT_SOURCE_RESEAL
FAIL_P0A_CHECKPOINT_ARTIFACT_UNVERIFIED
FAIL_P0A_STATIC_TO_PHYSICAL_PROMOTION
FAIL_P0A_PARENT_ROUTE_GATE_WEAKENED
HOLD_P0A_UNKNOWN_NEW_SOURCE
HOLD_P0A_HISTORICAL_SOURCE_NOT_MATERIALIZED
HOLD_P0A_CURRENT_CHECKPOINT_NOT_MATERIALIZED
```

## 12. Completion law and handoff

```text
EXACT CURRENT CF4 SOURCE
+ SAME 19 INPUTS / ORDERED BYTE HASH
+ HISTORICAL EXPECTATION PRESERVED AS HISTORICAL
+ PRE-EXISTING AOF R3 ROUTE GATES PRESERVED
+ STRICT CHECKPOINT PROVENANCE UNWEAKENED
+ ZERO STATIC NEGATIVE FALSE ACCEPTANCE
= CURRENT SOURCE-LINEAGE STATIC CONTRACT QUALIFIED

NOT = old checkpoint migration
NOT = CF3 GPU output parity
NOT = W8/W9A physical join
NOT = AOF CF5-C all-route PHYSICAL
NOT = CF5-D ACTIVE
```

P0-B may consume the current source-lineage *identity*, but not interpret P0-A's static receipt as a GPU runtime permit. This patch changes neither decoder semantics nor any default admission policy.

---

## 13. SOURCE bake evidence annex (2026-10-09)

**Evidence tier:** SOURCE/STATIC only. This annex supersedes the initial SPECIFICATION ONLY status above; no historical checkpoint replay, Rust compilation or actual GPU run is claimed.

### Artifacts (ZIP SHA-256 / entries / CRC)

| Artifact | SHA-256 | Entries | CRC |
|---|---|---:|---|
| CF4 parent | `6f6ac28b6196104064893cbd81ac8bd2ef85d0c2e1d0ed2faef14c3a76bda01b` | 8,755 | PASS |
| P0-A Overlay | `754bc82c772001ca76ef63d69b42708dcd0e265b458bfd02147aa89e63db568d` | 3 | PASS |
| P0-A Full | `eba90c54dada1f6138ca51401e4aad2e1611791cb660e8ad767dd01d8c32d96b` | 8,757 | PASS |

### Exact changed files

- `MOD tools/validate_ash_aof_r1_cf5_c_r3_selected_route_static.py`
- `ADD tools/ash_aof_headwise_p0a_lineage.py`
- `ADD tools/validate_ash_aof_headwise_p0a_lineage_contract_static.py`

### Verified evidence

```text
AOF CF5-C-R3             STATIC 60/60 PASS; negative 15/15 rejected
P0-A source-lineage      STATIC 60/60 PASS; negative 25/25 rejected
CURRENT 19-input digest  0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
HISTORICAL_PRE_CF2       e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283
HISTORICAL_REPLAY        HOLD_NOT_MATERIALIZED
CHECKPOINT               NotProvided
COMPILE / GPU            NOT_RUN
PRODUCTION_PROMOTED      false
```

All undeclared parent files are byte-identical; the frozen 19-input training digest and `Cargo.lock` are unchanged. An old checkpoint is never relabeled as the new lineage. This SOURCE-bake receipt does not qualify CF3 GPU output, W8/W9A physical join or CF5-D ACTIVE. Only the specification is committed to GitHub; the source is supplied separately in code-only ZIPs.
