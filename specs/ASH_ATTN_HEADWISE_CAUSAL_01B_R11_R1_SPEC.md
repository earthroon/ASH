# ASH-ATTN-HEADWISE-CAUSAL-01B-R11-R1

## Canonical Negative-Control Baseline Decoupling /
## Measurement Truth and Performance Threshold Separation /
## HOLD Artifact Completion Seal

---

# 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R11-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R11
production_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
runtime_schema=ash.attn.headwise.causal.01b.r11.runtime_artifact.v1
kernel_change=false
shader_change=false
```

R11-R1 repairs an implementation coupling discovered by the first canonical R11 run.

Observed failure:

```text
Error: CanonicalNegativeControlTruthInvalid
```

The run had already completed all nine incremental benchmark buckets. The failure occurred before negative-control execution and before Rust emitted the R11 artifacts.

---

# 1. Root cause

R11 assigned:

```rust
measurement_rounds: performance_route_pass
```

`performance_route_pass` combined two independent facts:

```text
measurement structure truth
  round count
  pair count
  ordering balance
  dispatch accounting

performance threshold truth
  bucket median ratio
  bucket p95 ratio
  paired probability
  route geomean
  worst bucket ratio
```

A performance threshold failure therefore invalidated the canonical negative-control baseline and aborted the process with a generic error. This prevented the intended HOLD artifacts from being written.

---

# 2. Required separation

Add:

```text
measurement_truth_pass
performance_threshold_pass
performance_route_pass = measurement_truth_pass && performance_threshold_pass
```

`measurement_truth_pass` owns only:

```text
observed_round_count == bucket_count * requested_rounds
observed_pair_count == bucket_count * requested_pairs
missing_round_count == 0
duplicate_round_count == 0
missing_pair_count == 0
duplicate_pair_count == 0
ordering_violation_count == 0
per-bucket round count exact
per-bucket pair count exact
per-bucket Reference-first count exact
per-bucket Atlas-first count exact
per-bucket timed dispatch counts exact
```

`performance_threshold_pass` owns only:

```text
all bucket performance thresholds pass
geometric_mean_median_ratio <= 0.95
worst_bucket_median_ratio <= 1.00
```

The canonical actual-run truth snapshot must bind:

```rust
measurement_rounds: measurement_truth_pass
```

It must not bind the combined performance verdict.

---

# 3. Negative-control validator baseline

Negative-control execution is an independent validator exercise. It must run even when production performance produces HOLD.

Use an isolated all-valid validator baseline:

```text
parent_bound=true
same_device=true
output_owned=true
kv_lifecycle=true
route_scope=true
measurement_rounds=true
rollback_fixture=true
static_truth=true
all commit counters=0
```

Each registered case injects exactly one expected failure into this isolated baseline.

The actual run snapshot remains separately recorded as:

```text
canonical_negative_truth_pass
canonical_negative_truth_failure_code
measurement_truth_pass
performance_threshold_pass
```

Negative-control PASS must not convert an actual production HOLD into PASS. The final verdict still requires `performance_route_pass` and all existing R11 production obligations.

---

# 4. Artifact completion rule

The following must no longer abort execution:

```text
performance threshold regression
canonical actual-run negative truth invalidation
```

After benchmark completion, Rust must emit:

```text
performance catalog
measurement round receipts
negative-control registry
negative-control outcomes
negative-control summary
claim boundary receipt
verdict
primary runtime artifact
local manifest
```

A failed performance threshold produces:

```text
status=HOLD
measurement_truth_pass=true
performance_threshold_pass=false
failed_components includes performance_true_round_non_regression
```

A structural measurement failure produces:

```text
status=HOLD
measurement_truth_pass=false
canonical_negative_truth_failure_code=MeasurementRoundFailure
```

---

# 5. Required diagnostics

Before negative-control execution, print:

```text
[headwise-causal-01b-r11][canonical-negative-baseline]
  pass=<bool>
  failure_code=<stable code or none>
```

Primary artifact and verdict must include:

```text
measurement_truth_pass
performance_threshold_pass
canonical_negative_truth_pass
canonical_negative_truth_failure_code
```

---

# 6. PASS boundary

R11-R1 does not relax any performance threshold.

```text
PASS = original R11 PASS formula
       && measurement_truth_pass
       && performance_threshold_pass
```

R11-R1 only prevents unrelated negative-control infrastructure from swallowing the real failure and suppressing HOLD evidence.

---

# 7. Canonical run

The canonical command remains unchanged:

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
