# ASH-ATTN-HEADWISE-CAUSAL-01A-R2

## Parent Truth-Audit R3-R4 Binding and Artifact Path Correction

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R2
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A
correction_class=parent_identity_and_artifact_path_truth_closure
```

## Correction

The original 01A specification referenced a non-existent parent artifact:

```text
workspace/runtime/truth_audit/ash_truth_audit_01_r3_r2_runtime_artifact.json
```

and labeled the parent as:

```text
ASH-TRUTH-AUDIT-01-R3-R2
```

The actual repository parent producer is:

```text
binary=crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
patch_id=ASH-TRUTH-AUDIT-01-R3-R4
schema=ash.truth_audit.01.r3.runtime_artifact.v1
artifact=workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json
```

## Required parent checks

The Headwise Causal 01A gate must fail closed unless the parent JSON proves:

```text
schema == ash.truth_audit.01.r3.runtime_artifact.v1
patch_id == ASH-TRUTH-AUDIT-01-R3-R4
repository_truth_audit_pass == true
all_truth_checks_pass == true
```

A generic JSON object, copied receipt, renamed file, or stale R3-R2 identity is not accepted.

## Correct parent generation command

```powershell
cargo run --release --manifest-path crates/lora_train/Cargo.toml `
  --bin ash_truth_audit_01_r3 `
  -- `
  --repo-root . `
  --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json `
  --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json `
  --runtime-artifact workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json `
  --write-runtime-artifact `
  --require-pass `
  --print-repository-predicate-receipt `
  --print-claim-promotion-receipt `
  --print-verifier-receipt `
  --print-repository-hold-roadmap
```

## Correct Headwise Causal 01A command

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01a_gate `
  -- `
  --repo-root . `
  --parent-snapshot workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json `
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

This correction changes parent evidence truth only. It does not alter the causal position ABI, shader visibility rule, parity thresholds, shadow-only boundary, or model-quality non-claim.
