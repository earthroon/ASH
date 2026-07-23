# ASH-ATTN-HEADWISE-CAUSAL-01B-R11

## Incremental-Only Verdict Scope /
## Executed Negative-Control Accounting /
## Measurement-Round Truth Repair Seal

---

# 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R11
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
parent_runtime_schema=ash.attn.headwise.causal.01b.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r11.runtime_artifact.v1
production_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
promotion_scope=incremental_decode_only
kernel_change=false
shader_change=false
canonical_full_01b_claim=false
model_quality_claim=false
```

R11 repairs the evidence layer around the R10 production kernel ABI. It does not modify the short-KV or long-KV WGSL kernels.

---

# 1. Required truth repairs

R11 must:

```text
emit only an incremental-only scoped verdict
keep FullPrefill as ReferenceProduction
keep ChunkedDecode as AtlasShadow
replace hard-coded negative-control counts with executed outcomes
interpret measurement_rounds as a real outer loop
emit all runtime artifacts and the local manifest from Rust
```

Forbidden source patterns:

```rust
let negative_control_count = 160usize;
let negative_control_fail_count = 0usize;
let atlas_first = (pair / rounds.max(1)) % 2 == 1;
```

---

# 2. Parent binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_local_manifest.json
```

Required parent identity:

```text
schema=ash.attn.headwise.causal.01b.runtime_artifact.v1
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
pass=true
status=PASS
incremental_decode_authority_mode=AtlasProduction
full_prefill_authority_mode=ReferenceProduction
chunked_decode_authority_mode=AtlasShadow
same_device_dispatcher=true
qkv_zero_copy_all=true
output_zero_copy=true
output_cpu_readback_count=0
output_host_upload_count=0
mixed_authority_count=0
performance_bucket_count=9
performance_bucket_fail_count=0
model_quality_claim_count=0
```

R10 negative-control and measurement-round claims are not inherited as repaired evidence. R11 reruns and re-emits them.

---

# 3. CLI scope

Required:

```text
--verdict-scope incremental-only
--negative-control-mode executed
--promote-full-prefill false
--promote-incremental-decode true
--promote-chunked-decode false
--internal-canary-prefills 0
```

Reject:

```text
measurement-pairs<1024
measurement-rounds<32
measurement-pairs % measurement-rounds != 0
minimum-live-negative-controls>40
```

`minimum-live-negative-controls` is retained as a compatibility flag. R11 truthfully classifies these 40 controls as `LiveReceiptMutation`, not live production fault injection.

---

# 4. Positive incremental fixtures

Mandatory:

```text
I01B-INC-8
  seq_q=1
  seq_kv=8
  q_position_base=7
  kernel=subgroup32_single_q_head_v1

I01B-INC-2048-LONG-KV
  seq_q=1
  seq_kv=2048
  q_position_base=2047
  kernel=subgroup32_gqa2_long_kv_tiled_v1
```

PASS requires:

```text
same_device=true
qkv_zero_copy=true
output_zero_copy=true
output_buffer_identity_match=true
output_cpu_readback_count=0
output_host_upload_count=0
atlas_output_commit_count=1
reference_output_commit_count=0
mixed_authority_count=0
pipeline_cache_hit=true
group_map_cache_hit=true
mismatch_element_count=0
non_finite_count=0
max_tolerance_ratio<=1.0
```

Parity readback is fixture evidence only. It is not a canonical GPU finite-guard claim.

---

# 5. True measurement rounds

Per bucket:

```text
policy_id=paired_gpu_timestamp_true_rounds_v1
measurement_pairs=1024
measurement_rounds=32
pairs_per_round=32
reference_first_rounds=16
atlas_first_rounds=16
```

Required loop:

```rust
for round_index in 0..measurement_rounds {
    let reference_first = round_index % 2 == 0;
    for pair_index in 0..pairs_per_round {
        // one reference measurement and one atlas measurement
    }
}
```

Canonical pair identity:

```text
incremental/<seq_kv>/round-<01..32>/pair-<01..32>
```

Across 9 buckets:

```text
round_receipt_count=288
pair_count=9216
missing_round_count=0
duplicate_round_count=0
missing_pair_count=0
duplicate_pair_count=0
ordering_violation_count=0
```

Thresholds:

```text
median_ratio<=1.00
p95_ratio<=1.05
paired_regression_probability<=0.05
geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
```

---

# 6. Executed negative controls

The Rust registry owns exactly 160 controls:

```text
parent_binding=20
device_identity=20
output_ownership=20
kv_lifecycle=20
route_authority=20
performance=20
rollback=20
receipt_static=20
```

Execution kinds:

```text
ValidatorMutation=112
LiveReceiptMutation=40
StaticSourceMutation=8
```

Every case emits:

```text
case_id
group
execution_kind
expected_failure_code
executed
skipped
observed_failure_code
expected_failure_observed
unintended production counters
receipt_digest
pass
```

Aggregate PASS:

```text
negative_control_count=160
negative_control_executed_count=160
negative_control_skipped_count=0
negative_control_fail_count=0
negative_control_expected_failure_observed_count=160
negative_control_unexpected_failure_code_count=0
negative_control_unintended_atlas_commit_count=0
negative_control_unintended_reference_commit_count=0
negative_control_unintended_kv_commit_count=0
negative_control_unintended_sampling_commit_count=0
```

The control namespace has no production policy token and cannot commit production output.

---

# 7. Claim boundaries

Canary:

```text
canary_evidence_class=dispatcher_smoke_short_kv_r10_preserved
canary_sequence_range=8..32
long_kv_canary_proven=false
canonical_decode_loop_canary_proven=false
```

Rollback:

```text
rollback_evidence_class=isolated_fixture_r10_preserved
live_forward_block_decode_rollback_proven=false
transactional_layer_kv_commit_proven=false
post_demotion_next_step_proven=false
sampling_boundary_proven=false
```

Additional non-claims:

```text
live_runtime_fault_matrix_proven=false
gpu_finite_guard_proven=false
canonical_full_01b_claim_count=0
model_quality_claim_count=0
```

---

# 8. Rust-generated artifacts

```text
workspace/runtime/attention/
  ash_attn_headwise_causal_01b_r11_runtime_artifact.json
  ash_attn_headwise_causal_01b_r11_local_manifest.json
  ash_attn_headwise_causal_01b_r11_parent_binding_receipt.json
  ash_attn_headwise_causal_01b_r11_scope_snapshot.json
  ash_attn_headwise_causal_01b_r11_promotion_policy_snapshot.json
  ash_attn_headwise_causal_01b_r11_positive_incremental_receipts.json
  ash_attn_headwise_causal_01b_r11_canary_receipt.json
  ash_attn_headwise_causal_01b_r11_rollback_fixture_receipt.json
  ash_attn_headwise_causal_01b_r11_measurement_plan.json
  ash_attn_headwise_causal_01b_r11_measurement_round_receipts.json
  ash_attn_headwise_causal_01b_r11_performance_catalog.json
  ash_attn_headwise_causal_01b_r11_negative_control_registry.json
  ash_attn_headwise_causal_01b_r11_negative_control_outcomes.json
  ash_attn_headwise_causal_01b_r11_negative_control_group_summary.json
  ash_attn_headwise_causal_01b_r11_negative_control_isolation_receipt.json
  ash_attn_headwise_causal_01b_r11_static_checks.json
  ash_attn_headwise_causal_01b_r11_claim_boundary_receipt.json
  ash_attn_headwise_causal_01b_r11_verdict.json
```

Runtime artifacts and the local manifest are excluded from the source bake archive.

---

# 9. PASS formula

```text
PASS =
  exact R10 parent binding
  && incremental-only scope
  && no prefill or chunked promotion
  && 2 positive incremental fixtures pass
  && same-device zero-copy invariants pass
  && all 9 performance buckets pass
  && 288 true round receipts exist
  && 9216 pairs are accounted for
  && no round/pair/order violation exists
  && route performance thresholds pass
  && 160 negative controls execute
  && every expected failure code is observed
  && every control leak count is zero
  && preserved dispatcher canary passes
  && preserved isolated rollback fixture passes
  && static truth checks pass
  && all artifact digests bind
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R11_INCREMENTAL_ONLY_VERDICT_SCOPE_EXECUTED_NEGATIVE_CONTROLS_TRUE_MEASUREMENT_ROUNDS_PERFORMANCE_NON_REGRESSION_SAME_DEVICE_ZERO_COPY_PRESERVED_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_CANONICAL_FULL_01B_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R11_TRUTH_REPAIR_INCOMPLETE
```

---

# 10. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r11"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r11_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-readback true `
  --forbid-output-host-upload true `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

---

# 11. Boundary after R11

```text
IncrementalDecode admitted buckets -> AtlasProductionScoped
FullPrefill -> ReferenceProduction
ChunkedDecode -> AtlasShadow
canonical full 01B -> not promoted
GPU finite guard -> not promoted
transactional runtime rollback -> not promoted
canonical model decode E2E -> not promoted
```

Next:

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12
GPU Finite Guard /
Candidate Validation /
Authority Commit Ordering Seal
```
