# ASH-ATTN-HEADWISE-CAUSAL-01A-R3

## Direct Relevant-Source Audit Binding /
## Repository-Wide Promotion Audit Decoupling /
## Headwise Causal Runtime Evidence SSOT Correction

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R3
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R2
correction_class=parent_scope_and_evidence_owner_truth_closure
```

## Correction

The R2 correction bound the Headwise Causal 01A gate to the repository-wide truth-audit artifact:

```text
ASH-TRUTH-AUDIT-01-R3-R4
workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json
```

That audit covers repository claim promotion, LoRA and decode evidence, source-artifact digests, and direct verified passthrough promotion. It can remain HOLD for blockers such as:

```text
PROMOTION_SOURCE_ARTIFACT_MISSING
PROMOTION_SOURCE_DIGEST_INVALID
```

Those blockers are unrelated to the Headwise Atlas causal-position ABI, KV visibility upper bound, shader route matrix, future-key poison test, or shadow parity result.

Therefore the repository-wide truth-audit PASS is not a valid prerequisite for this shadow-only attention gate.

## Correct evidence owner

Headwise Causal 01A is a direct source-and-runtime audit. Its evidence is owned by:

```text
relevant source tree digest
active shader digest
Rust/WGSL ABI receipt
GPU route matrix receipts
future-key poison receipts
GQA preservation receipt
two-pass softmax receipt
text-density freeze receipt
negative-control matrix
shadow-only no-promotion guard
```

Canonical parent evidence identity:

```text
parent_evidence_id=HEADWISE_CAUSAL_DIRECT_SOURCE_AUDIT_V1
parent_evidence_kind=direct_relevant_source_and_runtime_parity
external_repository_truth_audit_required=false
unrelated_claim_promotion_blockers_in_scope=false
```

## Source binding

The canonical source digest includes the exact active files used by the gate, including:

```text
crates/burn_webgpu_backend/src/headwise_causal.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention.wgsl
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01a_gate.rs
```

With `--full-source-hash true`, it also includes the relevant library export and binary registration surfaces.

Any missing source file, unreadable source, ABI mismatch, shader mismatch, parity failure, poison failure, unknown reachable variant, or promotion claim still fails closed.

## CLI correction

The following argument is removed:

```text
--parent-snapshot
```

The corrected command is:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01a_gate `
  -- `
  --repo-root . `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --route-matrix full `
  --include-prefill true `
  --include-incremental true `
  --include-chunked true `
  --future-poison true `
  --verify-gqa true `
  --freeze-text-density true `
  --require-shadow-only true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

## Scope preservation

This correction does not alter:

```text
absolute query-position ABI
KV visibility rule
prefill/incremental/chunked route definitions
GQA mapping
stable two-pass softmax
text-density freeze
numerical parity thresholds
future-key poison criteria
shadow-only boundary
production replacement default=false
model-quality non-claim
```

It only removes an unrelated repository-wide promotion audit from the Headwise Causal 01A prerequisite chain.
