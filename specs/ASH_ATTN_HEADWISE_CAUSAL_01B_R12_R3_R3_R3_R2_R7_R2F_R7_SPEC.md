# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7

## Guarded Structural Preflight First / Parent Kernel Evidence Adoption / Reduced Continuity Sentinel / Bucket-Visit Primer Amortization / GPU Workload Economy Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F
PARENT_ADDENDUM=R2F_PAIR_ORDER_QUERY_SLOT_DECONFOUNDING_ADDENDUM
RUN_MODE=seal-only-v1
DEFAULT_VERDICT=HOLD
RUNTIME/MANIFEST/RECEIPT/VERDICT_AUTHORITY=Rust-only
```

Forbidden: production route mutation, production output commit, kernel WGSL mutation, threshold widening, numerical-envelope widening, raw-sample filtering, selective rerun, and prebaked runtime evidence.

## 1. Purpose

R2F-R7 removes GPU work that does not strengthen the final guarded evidence:

```text
guarded ABI and execution preflight before benchmarking
exact adoption of sealed R2E-R7 kernel evidence
384-pair current-binary continuity sentinel
one primer block per bucket visit instead of per pair
unchanged 8192-pair guarded promotion population
```

This revision implements `seal` mode only. Smoke and preflight-only modes are not claimed.

## 2. Canonical execution order

```text
1 strict CLI seal
2 parent artifact/manifest binding
3 parent kernel-hash and runtime-profile identity
4 GPU bootstrap
5 texture residency and all guarded pipeline construction
6 production-shaped bind-group construction
7 full-head output comparison
8 guarded preflight at KV 128,1024,2048
9 384-pair kernel continuity sentinel
10 guarded warmup
11 guarded 8192-pair measurement
12 statistics and shadow eligibility
13 active-path/rollback revalidation
14 Rust artifact and manifest publication
```

A guarded pipeline, layout, binding, numerical, guard, or downstream failure must occur before the sentinel and before promotion samples.

## 3. Parent kernel authority

The R2E-R7 runtime artifact and manifest remain the canonical kernel-performance authority.

Required exact truths:

```text
parent pass=true
parent candidate_eligibility_pass=true
parent measurement_validity_pass=true
parent negative_control_expected=260
candidate WGSL SHA-256 exact
reference WGSL SHA-256 exact
normalized --runtime-profile path exact
```

The runtime-profile value is read from the parent manifest's canonical run-contract artifact. Adapter identity exactness is not claimed because the parent artifact does not publish an exact adapter-identity field.

## 4. Guarded structural preflight

Preflight buckets:

```text
128,1024,2048
```

Required pipelines and paths:

```text
reference texture attention
GQA4 cluster attention
shadow poison
full-head output compare
production micro-atlas guard map
production guard finalizer
GPU-gated downstream copy
```

Reference and candidate attention ABI:

```text
binding 0 uniform
binding 1 Q storage buffer
binding 2 K texture_2d_array<f32>
binding 3 V texture_2d_array<f32>
binding 4 physical-page LUT
binding 5..9 scratch/output storage
```

For each preflight bucket, Rust executes one untimed guarded pair and requires two compact GPU guard records with authority granted, zero failure bits, valid completion marker, and 2048 visited elements. Preflight contributes zero promotion samples and zero timestamp statistics.

## 5. Reduced continuity sentinel

```text
policy=reduced-three-bucket-sentinel-v1
buckets=128,1024,2048
global rounds=4
pairs per bucket visit=32
pairs per bucket=128
total pairs=384
```

The sentinel is a current-binary regression detector. It never replaces or merges with the parent 8192-pair evidence.

```text
kernel_only_continuity_pass =
  parent_performance_authority_pass
  AND sentinel.pass
  AND sentinel.core_performance_pass
  AND sentinel.measurement_validity_pass
```

Sentinel schedules:

```text
A=128,2048,1024
B=1024,2048,128
```

AB/BA ownership uses each KV's canonical position in the full eight-bucket R2E-R7 schedules, preserving query-slot deconfounding. For every sentinel KV and query slot across four rounds, AB=2 and BA=2.

## 6. Bucket-visit primer

```text
policy=bucket-visit-self-primed-steady-state-v2
```

Once before each bucket visit:

```text
reference primer=32 single-head dispatches
candidate primer=1 dispatch call / 8 GQA4 workgroups
then 32 paired guarded measurements
```

Primer work is untimed, creates no promotion sample, performs no payload readback, and commits no production output. Pipeline, bind group, Q/K/V, page-table generation, scratch generation, guard domain, and downstream pipeline identities must remain fixed throughout the visit.

## 7. Workload authority

Guarded seal population remains unchanged:

```text
8 buckets
4 warmup rounds
32 measurement rounds
32 pairs per bucket visit
8192 guarded measured pairs
```

Continuity reduction:

```text
legacy=8192 pairs
R2F-R7=384 pairs
reduction=95.3125 percent
```

Primer counts:

```text
warmup visits=32
measured visits=256
total visits=288
reference primer dispatches=9216
candidate primer dispatches=288
total actual primer dispatches=9504
measured-only actual=8448
legacy measured-only=270336
measured primer reduction=96.875 percent
```

## 8. Guarded measurement preservation

```text
query heads=32
KV heads=4
head dimension=64
reference measured dispatches=32 per pair
candidate measured dispatch call=1 per pair
output elements=2048
output bytes=8192
```

Timed spans still include attention, guard map, guard finalizer, GPU decision dependency, and downstream dispatch. Pipeline creation, allocation, primer, timestamp resolve, telemetry drain, and host waits remain outside.

The 8192 raw samples retain round, epoch, bucket position, KV length, pair index, query slot, AB/BA order, ring slots, reference/candidate duration, and ratio.

Required zero counts: sample filtering, selective rerun, payload readback, candidate output commit, production consumer, and active-route mutation.

## 9. Workload economy receipt

Rust publishes:

```text
run_mode
preflight_pass/preflight_bucket_count
parent_performance_authority_pass
kernel_continuity_sentinel_pair_count
primer_scope/primer_visit_count
reference_primer_dispatch_count
candidate_primer_dispatch_count
legacy_kernel_continuity_pair_count
legacy_primer_dispatch_count
workload_economy_pass
```

Canonical values:

```text
run_mode=seal
preflight_bucket_count=3
sentinel_pair_count=384
primer_visit_count=288
reference_primer_dispatch_count=9216
candidate_primer_dispatch_count=288
legacy_kernel_continuity_pair_count=8192
legacy_primer_dispatch_count=270336
```

## 10. Strict CLI extension

Exact value keys:

```text
--gqa4-r2f-run-mode seal
--gqa4-r2f-stage-order-policy guarded-structural-preflight-first-v1
--gqa4-r2f-parent-performance-authority r2e-r7-sealed-artifact-exact-v1
--gqa4-r2f-kernel-continuity-policy reduced-three-bucket-sentinel-v1
--gqa4-r2f-sentinel-buckets 128,1024,2048
--gqa4-r2f-sentinel-global-rounds 4
--gqa4-r2f-sentinel-pairs-per-bucket-visit 32
--gqa4-r2f-primer-scope bucket-visit-self-primed-steady-state-v2
--gqa4-r2f-gpu-load-policy sustained-seal-v1
```

Required Boolean keys:

```text
--require-gqa4-r2f-preflight-before-benchmark true
--require-gqa4-r2f-all-pipelines-precreated true
--require-gqa4-r2f-all-bind-groups-prevalidated true
--require-gqa4-r2f-preflight-promotion-samples-zero true
--require-gqa4-r2f-parent-performance-authority-exact true
--require-gqa4-r2f-parent-runtime-profile-exact true
--require-gqa4-r2f-reduced-continuity-sentinel true
--require-gqa4-r2f-sentinel-regression-zero true
--require-gqa4-r2f-sentinel-parent-authority-nonreplacement true
--require-gqa4-r2f-bucket-visit-primer true
--require-gqa4-r2f-primer-identity-window-lock true
--require-gqa4-r2f-primer-promotion-samples-zero true
--require-gqa4-r2f-mode-count-exact true
--require-gqa4-r2f-workload-economy-receipt true
```

The registry extension is exactly 23 unique required keys.

## 11. Negative controls

```text
parent controls=260
current controls=260
combined authority=520
```

The current 260 controls are ten controls across 26 groups. The ten new workload-economy groups cover stage order, pipeline precreation, bind-group prevalidation, parent performance authority, parent identity, sentinel scope, sentinel nonreplacement, primer visit ownership, primer identity window, and mode semantics.

## 12. Production isolation

The active production dispatcher, active buffer-attention shader, parent identities, output ABI, and composite active-path digest must be equal before and after execution. The existing production route remains the rollback anchor.

## 13. PASS

PASS requires:

```text
strict CLI pass
parent promotion and identity pass
preflight pass on all three buckets
preflight promotion samples=0
sentinel pairs=384 and sentinel PASS
query-slot deconfounding PASS
primer scope/counts exact
workload economy PASS
guarded raw samples=8192
all guarded buckets noninferior
guarded long-KV improvement PASS
order/epoch validity PASS
matched scratch/guard/downstream contracts PASS
payload readback/output commit/route mutation=0
active path and rollback unchanged
520/520 negative controls PASS
Rust artifact and manifest emitted
```

Success verdict:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_PREFLIGHT_FIRST_PARENT_EVIDENCE_ADOPTION_REDUCED_SENTINEL_AND_BUCKET_VISIT_PRIMER_AMORTIZATION_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_EXECUTION_ECONOMY_OR_GUARDED_SHADOW_ELIGIBILITY_NOT_PROVEN
```

## 14. Packaging and non-goals

The code ZIP excludes specs, runtime artifacts, manifests, receipts, verdict JSON, PowerShell/batch files, command text, and prebaked evidence.

Non-goals: smoke mode, preflight-only mode, adaptive sample counts, reference measured-dispatch fusion, shader optimization, guarded sample reduction, threshold relaxation, production route promotion, and reference retirement.

## 15. Final seal

```text
preflight first
+ exact parent performance authority
+ 384-pair current-binary sentinel
+ one primer block per bucket visit
+ unchanged 8192-pair guarded promotion population
= lower total GPU work without weaker promotion evidence
```
