# ASH-TCU-DECODE-04-R4-R2-R1-R5
# Legacy Missing Tokenizer Spec Hash / Explicit Structural Backfill Gate

- Parent: `ASH-TCU-DECODE-04-R4-R2-R1_PARENT_ARTIFACT_LINEAGE_SURFACE_DIGEST_TOKENIZER_IDENTITY_TRUTH_REPAIR_GATE`
- Runtime mode: `artifact_only_tokenizer_identity_legacy_backfill_candidate`
- Tokenizer manifest rewrite authority: `false`
- Tokenizer spec rewrite authority: `false`
- Production authority: `false`

## 1. Purpose

Some deployed tokenizer v5 manifests contain a valid manifest ID, tokenizer spec ID, trainer contract, normalization contract, special-token contract, vocabulary hashes, and manifest self hash, but omit `lineage.tokenizer_spec_hash`.

The parent R1 gate previously stopped before tokenizer spec discovery with:

```text
r4r2r1_hold:tokenizer_manifest_spec_hash_missing
```

R5 does not pretend that a missing embedded hash matches. It allows a non-mutating backfill candidate only when the operator supplies the explicit flag:

```text
--allow-legacy-missing-tokenizer-spec-hash-backfill
```

Without that flag, missing `lineage.tokenizer_spec_hash` remains HOLD.

## 2. Resolution contract

When an embedded tokenizer spec hash exists, the original exact hash path remains authoritative.

When the embedded tokenizer spec hash is absent and explicit backfill authority is present, Rust scans repository-local TOML/JSON tokenizer spec candidates. A candidate is accepted only when all of the following match the tokenizer manifest:

- `tokenizer_spec_id`
- trainer kind
- trainer vocabulary size
- character coverage bit pattern
- trainer seed
- byte-fallback policy
- normalization structure
- PAD/BOS/EOS/UNK strings
- PAD/BOS/EOS/UNK IDs `0/1/2/3`
- hot-token-cache contract when the manifest contains that section

Exactly one candidate must match. Zero candidates HOLD. More than one candidate HOLD.

## 3. Evidence semantics

The tokenizer identity receipt schema is promoted to `ash_tensorcube_decode04_r4_r2_r1_tokenizer_identity_truth_v2` and records:

```text
embedded_tokenizer_spec_hash
recomputed_tokenizer_spec_hash
tokenizer_spec_hash_match
tokenizer_spec_identity_mode
tokenizer_spec_identity_proven
legacy_missing_tokenizer_spec_hash
legacy_missing_tokenizer_spec_hash_backfill_authorized
tokenizer_spec_hash_backfill_candidate
tokenizer_manifest_rewrite_performed
```

For a legacy missing-hash manifest:

```text
tokenizer_spec_hash_match=false
tokenizer_spec_identity_mode=legacy_missing_hash_unique_structural_backfill_candidate
tokenizer_spec_identity_proven=true
tokenizer_spec_hash_backfill_candidate=<canonical recomputed hash>
tokenizer_manifest_rewrite_performed=false
```

This is not represented as embedded hash parity. It is represented as a uniquely proven, non-mutating backfill candidate.

## 4. Forbidden behavior

- silently treating a missing embedded hash as a match
- selecting the first parseable TOML
- selecting by filename alone
- selecting by tokenizer spec ID alone
- rewriting the tokenizer manifest
- writing the computed hash into the tokenizer manifest
- accepting multiple structural matches
- accepting a structural mismatch because vocabulary size alone matches

## 5. PASS and HOLD

PASS requires either:

1. exact embedded tokenizer spec hash parity, or
2. explicit legacy-backfill authority plus exactly one structurally matching tokenizer spec candidate.

HOLD reasons include:

```text
r4r2r1_hold:tokenizer_manifest_spec_hash_missing:explicit_backfill_authorization_required
r4r2r1_hold:tokenizer_spec_autodiscovery_no_identity_match
r4r2r1_hold:tokenizer_spec_autodiscovery_ambiguous:<COUNT>
r4r2r1_hold:tokenizer_spec_override_structural_contract_mismatch
```

PASS does not authorize tokenizer manifest mutation. Any actual manifest backfill requires a separate reviewed apply gate.