# ASH-ATTN-HEADWISE-CAUSAL-01B-R12

## GPU Finite Guard /
## Candidate Validation /
## Authority Commit Ordering Seal

---

# 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R11-R1
parent_runtime_schema=ash.attn.headwise.causal.01b.r11.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r12.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
promotion_scope=incremental_decode_only
full_prefill_promotion=false
chunked_decode_promotion=false
```

R12 does not modify the R10 short-KV or long-KV attention kernels. It places a GPU finite guard and an explicit authority state machine between the attention dispatch and downstream consumption.

---

# 1. Canonical authority flow

```text
CandidateDispatched
→ GuardPending
→ GuardCompleted
→ CandidateValidated
→ CommitEligible
→ AtlasProductionCommitted
→ reshape/o_proj permitted
```

Forbidden:

```text
CandidateDispatched → AtlasProductionCommitted
GuardPending → AtlasProductionCommitted
GuardCompleted → AtlasProductionCommitted
CandidateRejected → AtlasProductionCommitted
o_proj before AtlasProductionCommitted
KV/global cursor/sampling commit before AtlasProductionCommitted
```

The production helper owns the commit point. The output tensor cannot escape to `o_proj` before the guard and candidate validation complete.

---

# 2. Parent binding

Required:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_local_manifest.json
```

Parent requirements:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R11
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R11-R1
pass=true
status=PASS
incremental_decode_authority_mode=AtlasProductionScoped
full_prefill_authority_mode=ReferenceProduction
chunked_decode_authority_mode=AtlasShadow
performance_bucket_count=9
performance_bucket_fail_count=0
negative_control_count=160
negative_control_fail_count=0
```

---

# 3. GPU finite guard

New source:

```text
crates/burn_webgpu_backend/src/headwise_finite_guard.rs
crates/burn_webgpu_backend/src/shaders/headwise_atlas_output_finite_guard.wgsl
```

Canonical guard configuration:

```text
shader_id=headwise_atlas_output_finite_guard_v1
workgroup_size=256
guard_decision_mode=compact_async_readback_v1
```

The guard reads the exact output storage buffer and scans only `logical_element_count` values. It emits compact metadata:

```text
completion_marker
candidate_nonce_lo
candidate_nonce_hi
expected_element_count
visited_element_count
non_finite_count
nan_count
positive_infinity_count
negative_infinity_count
max_abs_bits
guard_error_bits
```

Positive production PASS:

```text
completion marker exact
candidate nonce exact
expected_element_count == visited_element_count
non_finite_count == 0
nan_count == 0
positive_infinity_count == 0
negative_infinity_count == 0
max_abs_value finite and >= 0
output_value_readback_count == 0
compact_guard_readback_count == 1
```

Only the compact guard result may be mapped. Attention output values must never be copied into the guard readback buffer.

---

# 4. Candidate identity and commit ordering

Each production attempt receives a monotonically increasing candidate nonce owned by `NativeWgpuModel`.

Before commit the model must validate:

```text
same runtime handles
Q/K/V zero-copy
output zero-copy
output primitive identity unchanged
output stream identity unchanged
candidate nonce echoed by guard
logical element count exact
finite guard pass
rollback anchor available
o_proj has not started
KV/global cursor/sampling have not committed
```

Success:

```text
atlas_output_commit_count=1
reference_output_commit_count=0
mixed_authority_count=0
authority_state=AtlasProductionCommitted
```

Guard or validation failure:

```text
atlas_output_commit_count=0
candidate rejected before downstream consumption
explicit rollback counter incremented
silent fallback forbidden
```

---

# 5. Fault injection and negative controls

R12 re-executes the 160 R11 controls and adds 80 R12 controls:

```text
guard_resource=20
numeric_classification=20
candidate_validation=20
commit_order=20
total=240
```

At least these numeric cases execute against the real GPU guard:

```text
single NaN
multiple NaNs
positive infinity
negative infinity
mixed NaN/+Inf/-Inf
```

Required aggregate:

```text
negative_control_count=240
negative_control_executed_count=240
negative_control_skipped_count=0
negative_control_fail_count=0
unexpected_failure_code_count=0
unintended production commit counts=0
```

---

# 6. Guarded performance

The Atlas timed route includes:

```text
attention dispatch
finite-guard dispatch
compact result copy/map/validation
candidate validation
commit bookkeeping
```

Mandatory buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Measurement:

```text
warmups>=128
rounds=32
pairs_per_round=32
pairs_per_bucket=1024
Reference-first rounds=16
Atlas-first rounds=16
```

Thresholds are not relaxed:

```text
bucket median_ratio<=1.00
bucket p95_ratio<=1.05
paired_regression_probability<=0.05
route geomean<=0.95
worst bucket<=1.00
```

---

# 7. Rust-generated artifacts

```text
workspace/runtime/attention/
  ash_attn_headwise_causal_01b_r12_runtime_artifact.json
  ash_attn_headwise_causal_01b_r12_local_manifest.json
  ash_attn_headwise_causal_01b_r12_parent_binding_receipt.json
  ash_attn_headwise_causal_01b_r12_scope_snapshot.json
  ash_attn_headwise_causal_01b_r12_promotion_policy_snapshot.json
  ash_attn_headwise_causal_01b_r12_guard_policy_snapshot.json
  ash_attn_headwise_causal_01b_r12_candidate_state_transition_log.json
  ash_attn_headwise_causal_01b_r12_guard_dispatch_receipts.json
  ash_attn_headwise_causal_01b_r12_candidate_validation_receipts.json
  ash_attn_headwise_causal_01b_r12_authority_commit_receipts.json
  ash_attn_headwise_causal_01b_r12_fault_injection_matrix.json
  ash_attn_headwise_causal_01b_r12_positive_incremental_receipts.json
  ash_attn_headwise_causal_01b_r12_canary_receipt.json
  ash_attn_headwise_causal_01b_r12_rollback_fixture_receipt.json
  ash_attn_headwise_causal_01b_r12_measurement_plan.json
  ash_attn_headwise_causal_01b_r12_measurement_round_receipts.json
  ash_attn_headwise_causal_01b_r12_performance_catalog.json
  ash_attn_headwise_causal_01b_r12_negative_control_registry.json
  ash_attn_headwise_causal_01b_r12_negative_control_outcomes.json
  ash_attn_headwise_causal_01b_r12_negative_control_group_summary.json
  ash_attn_headwise_causal_01b_r12_negative_control_isolation_receipt.json
  ash_attn_headwise_causal_01b_r12_static_checks.json
  ash_attn_headwise_causal_01b_r12_claim_boundary_receipt.json
  ash_attn_headwise_causal_01b_r12_verdict.json
```

Runtime artifacts and manifest are excluded from the source bake archive.

---

# 8. PASS formula

```text
PASS =
  exact R11-R1 parent binding
  && incremental-only scope
  && backend/model public ABI == R12
  && attention kernel revision remains R10
  && finite guard revision == R12
  && positive candidate guard pass
  && expected == visited element count
  && non-finite count == 0
  && output value readback count == 0
  && candidate state transitions valid
  && commit occurs only from CommitEligible
  && downstream pre-commit counters are zero
  && all guarded performance buckets pass
  && 240 controls execute and pass
  && static checks pass
  && artifact/manifest digests bind
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_GPU_FINITE_GUARD_CANDIDATE_VALIDATION_AUTHORITY_COMMIT_ORDERING_INCREMENTAL_ONLY_SAME_DEVICE_OUTPUT_PRESERVED_COMPACT_GUARD_READBACK_ONLY_NO_OUTPUT_VALUE_READBACK_GUARDED_PERFORMANCE_NON_REGRESSION_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_FINITE_GUARD_OR_COMMIT_ORDERING_INCOMPLETE
```

---

# 9. Claim boundary

R12 PASS grants:

```text
IncrementalDecode admitted buckets -> AtlasProductionGuardedScoped
FullPrefill -> ReferenceProduction
ChunkedDecode -> AtlasShadow
```

R12 does not prove:

```text
same-device guard decision without compact host metadata
transactional KV rollback
canonical 22-layer decode E2E
full-prefill production
chunked production
language or translation quality improvement
```

---

# 10. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-value-readback true `
  --forbid-output-host-upload true `
  --guard-mode compact-async-readback `
  --require-finite-guard true `
  --guard-workgroup-size 256 `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --expected-negative-controls 240 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```
