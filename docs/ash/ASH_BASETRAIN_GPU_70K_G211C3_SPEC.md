# ASH-BASETRAIN-GPU-70K-G211C3

## TensorCube Microbench Baseline / Burn Matmul Versus TensorCube Candidate / Perf Win Required For Further Promotion

Seal: Microbench Evidence Only / No Runtime Splice / No Production Route.

## SSOT

`70K-G211C3` consumes the G211C2 TensorCube CPU/WGPU parity shape sweep output as its only entry authority.

`70K-G211C3` may only pass after the current baseline matmul path and the TensorCube candidate path are measured under the same required shapes, same deterministic inputs, same adapter, and same iteration policy, while preserving parity.

`70K-G211C3` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not claim translation quality, TensorCore usage, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C2
TensorCube CPU/WGPU Parity Shape Sweep /
8x8 Reference To Shape Matrix Guard /
No Runtime Splice No Production Route
```

Required predecessor evidence:

```text
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_TENSORCUBE_PARITY_SHAPE_SWEEP.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_SHAPE_PARITY_MATRIX.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_ADAPTER_FINGERPRINT.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_NEXT_ENTRY_PACKET_G211C3.json
artifacts/g211c2/PASS_ASH_BASETRAIN_GPU_70K_G211C2.txt
```

G211C3 must block if the G211C2 entry packet or PASS marker is missing.

## Purpose

G211C3 exists to decide whether TensorCube is eligible for the next shadow-splice probe.

G211C3 proves only this:

```text
baseline matmul path was measured
TensorCube candidate matmul path was measured
all required shapes used matching inputs
candidate parity remained valid
microbench verdict was recorded
no runtime splice or production route mutation occurred
```

G211C3 does not promote TensorCube. G211C3 does not activate production inference. G211C3 does not claim general acceleration.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3_tensorcube_microbench_baseline.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3_tensorcube_microbench_baseline
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3_tensorcube_microbench_baseline
```

Optional arguments:

```text
--g211c2-dir artifacts/g211c2
--out-dir artifacts/g211c3
--warmup-iterations 20
--measured-iterations 100
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE
```

## Required Bench Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B2 = [16, 16, 64]
B3 = [64, 64, 64]
B4 = [128, 128, 128]
B5 = [17, 31, 65]
```

G211C3 required shapes must match G211C2 required shapes. Removing or replacing a required shape blocks PASS.

## Benchmark Contract

Each required shape must satisfy:

```text
same_shape = true
same_dtype = true
same_input_a_hash = true
same_input_b_hash = true
same_adapter = true
same_iteration_policy = true
candidate_vs_cpu_parity_pass = true
candidate_vs_baseline_parity_pass = true
```

Warmup and measured iterations must be separated.

Minimum:

```text
warmup_iterations >= 10
measured_iterations >= 50
```

Recommended:

```text
warmup_iterations = 20
measured_iterations = 100
```

## Timing Metrics

Each baseline and candidate measurement must record:

```text
min_ms
p50_ms
p95_ms
max_ms
mean_ms
stddev_ms
iteration_count
warmup_count
```

Candidate speedup ratio:

```text
candidate_speedup_ratio_p50 = baseline_p50_ms / candidate_p50_ms
candidate_speedup_ratio_p95 = baseline_p95_ms / candidate_p95_ms
```

## Promotion Decision Contract

G211C3 never promotes production directly. It only decides whether G211C4 shadow probe is allowed.

Verdict values:

```text
STOP_PARITY_FAILED
STOP_PERF_LOSS
SHADOW_ONLY_PERF_NEUTRAL
SHADOW_ALLOWED_PERF_WIN
```

Decision rules:

```text
if parity_pass == false:
  verdict = STOP_PARITY_FAILED
  g211c4_entry_packet_generated = false

if parity_pass == true and geomean_speedup_ratio < 1.0:
  verdict = STOP_PERF_LOSS
  g211c4_entry_packet_generated = false

if parity_pass == true and geomean_speedup_ratio >= 1.0 and geomean_speedup_ratio < 1.05:
  verdict = SHADOW_ONLY_PERF_NEUTRAL
  g211c4_entry_packet_generated = true
  g211c4_mode_limit = ShadowOnly

if parity_pass == true and geomean_speedup_ratio >= 1.05 and min_speedup_ratio >= 1.0:
  verdict = SHADOW_ALLOWED_PERF_WIN
  g211c4_entry_packet_generated = true
  g211c4_mode_limit = Shadow
```

Default required performance win:

```text
geomean_speedup_ratio >= 1.05
min_speedup_ratio >= 1.0
no required shape has parity failure
```

## Local Outputs

The baked package must not contain prebaked `artifacts/g211c3` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_SHAPE_BENCHMARK_MATRIX.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_BAKE_MANIFEST.json
artifacts/g211c3/PASS_ASH_BASETRAIN_GPU_70K_G211C3.txt
```

Only one of the following should be authoritative:

```text
NEXT_ENTRY_PACKET_G211C4 when verdict is SHADOW_ONLY_PERF_NEUTRAL or SHADOW_ALLOWED_PERF_WIN
PROMOTION_STOP_PACKET when verdict is STOP_PARITY_FAILED or STOP_PERF_LOSS
```

## Required Receipt Fields

Main microbench receipt must include:

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3",
  "patch_name": "TensorCube Microbench Baseline",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C2",
  "g211c2_entry_verified": true,
  "physical_dispatch_executed": true,
  "logical_gate_transition_only": false,
  "benchmark": {
    "required_shape_count": 6,
    "all_required_shapes_measured": true,
    "same_input_policy_pass": true,
    "same_adapter_policy_pass": true
  },
  "summary": {
    "parity_pass": true,
    "any_latency_regression": false,
    "geomean_speedup_ratio": 0.0,
    "min_speedup_ratio": 0.0,
    "max_speedup_ratio": 0.0,
    "microbench_verdict": "SHADOW_ALLOWED_PERF_WIN"
  },
  "forbidden_mutations": {
    "runtime_route_changed": false,
    "tensorcube_runtime_splice_changed": false,
    "production_route_changed": false,
    "decode_output_replaced": false,
    "weights_changed": false,
    "checkpoint_written": false,
    "optimizer_step_executed": false,
    "training_step_executed": false
  },
  "claims": {
    "quality_claim_allowed": false,
    "speedup_claim_allowed": false,
    "tensorcore_claim_allowed": false,
    "production_promotion_claim_allowed": false
  }
}
```

## Invariants

```text
physical_dispatch_executed = true
logical_gate_transition_only = false
all_required_shapes_measured = true
same_input_policy_pass = true
same_adapter_policy_pass = true
candidate_vs_cpu_parity_pass = true for every shape
candidate_vs_baseline_parity_pass = true for every shape
microbench_verdict exists
production_route_changed = false
tensorcube_runtime_splice_changed = false
runtime_splice_allowed = false unless verdict permits shadow-only probe
weights_changed = false
checkpoint_written = false
quality_claim_allowed = false
speedup_claim_allowed = false
tensorcore_claim_allowed = false
promotion_allowed = false
```

## PASS Meaning

PASS means the G211C3 microbench gate executed, baseline and TensorCube candidate measurements were recorded for all required shapes, parity remained valid, and a promotion/shadow eligibility verdict was written.

PASS does not mean TensorCube production route is connected. PASS does not mean TensorCube runtime splice is active. PASS does not mean TensorCube decode output is used. PASS does not mean production acceleration is claimed. PASS does not mean TensorCore is used.

## BLOCKED Codes

```text
ERR_70K_G211C3_G211C2_ENTRY_PACKET_MISSING
ERR_70K_G211C3_G211C2_PASS_MARKER_MISSING
ERR_70K_G211C3_BASELINE_PATH_UNRESOLVED
ERR_70K_G211C3_CANDIDATE_PATH_UNRESOLVED
ERR_70K_G211C3_REQUIRED_SHAPE_NOT_MEASURED
ERR_70K_G211C3_PARITY_MISMATCH
ERR_70K_G211C3_RUNTIME_MUTATION_DETECTED
```

## Next Gate

If verdict allows shadow:

```text
ASH-BASETRAIN-GPU-70K-G211C4
Runtime Splice Shadow Probe /
Baseline Output Remains Authority /
No Decode Replacement No Silent Fallback
```

If verdict stops promotion:

```text
G211C4 entry packet must not be generated.
TensorCube candidate remains research-only.
```
