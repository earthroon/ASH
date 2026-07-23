# ASH-ATTN-HEADWISE-CAUSAL-01A-R9

## Near-Zero Relative Error Truth /
## Combined Absolute-Relative Tolerance /
## Route Parity False-HOLD Closure

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R9
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R8
correction_class=numerical_parity_tolerance_policy_truth_closure
parity_policy_id=atol_plus_rtol_reference_floor_v1
```

## Observed false HOLD

The R8 runtime proved:

```text
poison_pass=true
static_pass=true
parallel_group_map_pass=true
negative_fail_count=0
future_key_visit_count=0
bound_mismatch_count=0
```

Only route parity failed. The failing cases reported:

```text
P03 max_abs_error approximately 6e-8, mismatch_element_count=0
I03 max_abs_error approximately 6e-8, mismatch_element_count=0
```

Their global maximum relative errors exceeded `1e-3` only because the corresponding reference values were close to zero. Requiring both:

```text
max_abs_error <= atol
max_rel_error <= rtol
```

as independent global maxima creates a false HOLD even when every element is within an accepted absolute-relative tolerance envelope.

## Canonical parity rule

For each finite element:

```text
reference_scale = max(abs(reference), relative_floor)
allowed_error = atol + rtol * reference_scale
tolerance_ratio = abs(actual-reference) / allowed_error
```

Canonical constants:

```text
atol=1e-3
rtol=1e-3
relative_floor=1e-6
hard_abs_ceiling=1e-2
```

An element passes when:

```text
tolerance_ratio <= 1.0
```

A route passes numerical parity when:

```text
non_finite_count == 0
mismatch_element_count == 0
max_tolerance_ratio <= 1.0
max_abs_error <= hard_abs_ceiling
```

## Diagnostic role of max relative error

`max_rel_error` remains in receipts and console diagnostics, but it no longer independently owns PASS/HOLD.

This is required because relative error is unstable near zero and can be large while absolute error remains several orders of magnitude below the accepted tolerance.

## Required receipts

Add or preserve:

```text
parity_policy_id
parity_abs_tolerance
parity_rel_tolerance
parity_relative_floor
parity_hard_abs_ceiling
max_abs_error
max_rel_error
max_tolerance_ratio
mismatch_element_count
non_finite_count
```

The policy identity and constants must be present in the primary artifact and parity summary.

## Prohibited shortcuts

Forbidden:

```text
removing relative-error telemetry
raising atol only to make a case pass
raising hard_abs_ceiling
special-casing P03 or I03
ignoring non-finite values
rounding GPU output before comparison
changing the CPU reference output
changing the headwise shader numerical path in this closure
```

## Scope preservation

This correction does not change:

```text
absolute query-position SSOT
KV visibility upper bound
prefill/incremental/chunked route matrix
future-key poison criteria
GQA group ownership
atlas parallel group map
single-pass grouped dispatch
text-density neutralization
shadow-only authority boundary
production replacement default=false
model-quality non-claim
```

It only replaces the invalid independent-global-max relative gate with one elementwise combined absolute-relative tolerance policy.
