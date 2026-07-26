# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R2

## Reduced Sentinel Order-Bias Diagnostic Scope / Parent and Guarded Full-Population Order Authority / Non-Order Continuity Contract Seal

## 0. Scope

This addendum corrects the authority assigned to the 384-pair R2F-R7 kernel continuity sentinel.

The reduced sentinel executes:

```text
3 buckets x 4 rounds x 32 pairs = 384 pairs
128 pairs per bucket
```

The generic `HeadwiseGqa4PerformanceReceipt` applies the full-population order-bias threshold:

```text
abs(reference AB/BA median bias) <= 0.05
abs(candidate AB/BA median bias) <= 0.05
```

That threshold was designed for 1,024 samples per bucket. Applying it as a promotion-blocking requirement to 128 samples per bucket converts the continuity sentinel into a second promotion benchmark.

## 1. Authority separation

Canonical order authorities are:

```text
Parent R2E-R7 sealed 8,192-pair receipt:
  kernel-only promotion-grade order authority

R2F-R7 guarded 8,192-pair population:
  guarded end-to-end promotion-grade order authority

R2F-R7 384-pair sentinel:
  non-order current-binary continuity authority
  order-bias observation is diagnostic only
```

The sentinel must not replace either full-population order authority.

## 2. Sentinel continuity contract

The top-level sentinel continuity contract passes only when all of the following hold:

```text
parent performance authority exact
timestamp query features valid
numerical and long-KV preflight valid
pair topology valid
input identity and generation lock valid
scratch isolation valid
raw sample retention valid
sample filtering count = 0
selective rerun count = 0
per-kernel submit count = 0
per-pair readback count = 0
timed host wait/allocation/clear/resolve counts = 0
core noninferiority and required improvement valid
thermal epoch validity valid
primer topology and isolation valid
pipeline-transition exclusion valid
mirrored schedule valid
pair-order query-slot deconfounding valid
signed bias receipt finite
shared-load reuse valid
payload readback/output commit/production consumer/route mutation = 0
cost decomposition valid
promotion sample count = 384
```

The generic sentinel `measurement_validity_pass` and `pass` fields are not authoritative because they include the 5 percent promotion-grade order threshold.

## 3. Order-bias handling

The raw generic sentinel fields remain unchanged and are retained:

```text
order_bias_pass
measurement_validity_pass
pass
failures
reference_order_bias_ratio
candidate_order_bias_ratio
```

R2F-R7-R2 publishes:

```text
parent_order_validity_authority_pass
sentinel_order_bias_diagnostic_only
sentinel_order_bias_observed_pass
sentinel_continuity_contract_pass
```

Canonical values:

```text
sentinel_order_bias_diagnostic_only = true
parent_order_validity_authority_pass = exact parent authority result
sentinel_order_bias_observed_pass = raw generic sentinel order result
```

A false `sentinel_order_bias_observed_pass` is retained as diagnostic evidence but does not independently HOLD the run.

## 4. Diagnostic receipt

Each sentinel bucket publishes:

```text
KV length and pair count
core noninferiority and improvement
raw order diagnostic result
thermal epoch result
reference/candidate order absolute ratios
reference/candidate epoch absolute ratios
median and p95 candidate/reference ratios
```

No sample may be removed, filtered, relabeled, or selectively rerun.

## 5. Final order gate preservation

The final guarded 8,192-pair population retains the existing promotion requirements:

```text
all guarded buckets order_bias_pass = true
all guarded buckets epoch_bias_pass = true
measurement_validity_pass = order_validity_pass AND epoch_validity_pass
```

`production_route_shadow_eligibility_pass` still requires the final guarded `measurement_validity_pass`.

Therefore this addendum does not widen the final threshold or weaken guarded promotion evidence.

## 6. HOLD behavior

The run HOLDS before guarded measurement when:

```text
sentinel_continuity_contract_pass = false
```

The run does not HOLD solely because:

```text
sentinel_order_bias_observed_pass = false
```

The final guarded population still HOLDS on any order-validity failure.

## 7. Non-goals

This addendum does not change AB/BA ownership, the v2 query-slot deconfounding schedule, sentinel or guarded pair counts, performance or numerical thresholds, candidate/reference shaders, or production routes.

## 8. Seal

```text
full parent order authority
+ diagnostic-only reduced-sentinel order observation
+ strict non-order sentinel continuity contract
+ unchanged guarded 8,192-pair order promotion gate
= reduced workload without converting a small sentinel into a second promotion benchmark
```
