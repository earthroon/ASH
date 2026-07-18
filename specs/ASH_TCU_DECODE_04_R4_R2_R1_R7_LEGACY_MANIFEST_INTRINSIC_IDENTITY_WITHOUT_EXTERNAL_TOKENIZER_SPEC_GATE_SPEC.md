# ASH-TCU-DECODE-04-R4-R2-R1-R7
# Legacy Manifest Intrinsic Identity Without External Tokenizer Spec Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R2-R1-R7_LEGACY_MANIFEST_INTRINSIC_IDENTITY_WITHOUT_EXTERNAL_TOKENIZER_SPEC_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R2-R1_PARENT_ARTIFACT_LINEAGE_SURFACE_DIGEST_TOKENIZER_IDENTITY_TRUTH_REPAIR_GATE`
- Runtime mode: `artifact_only_lineage_truth_repair`
- Production authority: `false`
- Tokenizer manifest mutation: `forbidden`
- PASS authorizes: existing R4-R2-R1 continuation only

## 1. Problem

Some canonical legacy tokenizer manifests contain no `lineage.tokenizer_spec_hash`, and the corresponding external `TokenizerSpec` source file is not present in the repository. In that state, structural autodiscovery must not invent, synthesize, or silently select a tokenizer spec.

The previous `tokenizer_spec_autodiscovery_no_identity_match` HOLD is therefore split into two explicit identity modes:

1. strict external tokenizer-spec identity
2. explicit legacy manifest-intrinsic identity

## 2. Required CLI mode exclusivity

Exactly one of the following must be present:

```text
--require-tokenizer-spec-hash-parity
--require-tokenizer-manifest-intrinsic-identity
```

The intrinsic mode additionally requires:

```text
--allow-legacy-manifest-intrinsic-identity-without-tokenizer-spec
```

The two identity modes may not be enabled together.

## 3. Strict mode

When an external tokenizer spec exists, existing behavior remains unchanged:

- exact spec bytes are read
- typed `TokenizerSpec` parsing succeeds
- embedded spec hash parity or explicitly authorized structural backfill succeeds
- trainer, normalization, special-token, and hot-cache contracts match

## 4. Legacy manifest-intrinsic mode

This mode is allowed only when all of the following are true:

```text
manifest.lineage.tokenizer_spec_hash == null
matching external TokenizerSpec candidate count == 0
explicit intrinsic authority flag == true
```

The gate must not construct a synthetic `TokenizerSpec`.

The following manifest-intrinsic evidence is required:

- exact tokenizer manifest file SHA-256
- canonical embedded manifest self-hash parity
- embedded vocab hash parity
- embedded reserved-token hash parity
- non-empty manifest ID
- non-empty tokenizer spec ID retained as a legacy identifier only
- non-empty trainer kind
- finite character coverage
- trainer vocab size equals 48,259
- manifest vocab entry count equals 48,259
- PAD/BOS/EOS/UNK IDs are exactly 0/1/2/3
- PAD/BOS/EOS/UNK token strings are non-empty
- no forbidden top-level `manifest_hash` key
- exact path and exact-byte identity remain bound to the parent R4-R2 tokenizer receipt

## 5. Receipt truth

Intrinsic mode must record:

```text
tokenizer_spec_path = null
tokenizer_spec_exact_file_sha256 = null
spec_tokenizer_spec_id = null
recomputed_tokenizer_spec_hash = null
tokenizer_spec_hash_match = false
tokenizer_spec_identity_proven = false
manifest_intrinsic_identity_proven = true
tokenizer_spec_resolution_mode = legacy_manifest_intrinsic_identity_without_external_spec
tokenizer_spec_identity_mode = legacy_manifest_intrinsic_exact_byte_identity_without_external_spec
tokenizer_manifest_rewrite_performed = false
```

This is not equivalent to external tokenizer-spec provenance. It proves only the exact identity and internal integrity of the canonical legacy manifest used by the parent decode gate.

## 6. Forbidden behavior

- synthesizing a `TokenizerSpec` from manifest fields
- treating `runtime_profile_v5_48259.toml` or `model_spec_v5_48259.toml` as a tokenizer training spec
- silently selecting an unrelated TOML file
- writing a missing spec hash into the manifest
- reporting external tokenizer-spec identity as proven in intrinsic mode
- enabling strict and intrinsic modes simultaneously

## 7. Rust-owned artifacts

The existing R4-R2-R1 Rust binary remains the only producer of the tokenizer identity receipt and local manifest. No runtime receipt or generated manifest is baked into the source ZIP.
