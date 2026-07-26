# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E

## Long-KV Denominator Canonicalization Addendum

```text
ADDENDUM_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E-DENOM-CANON-01
PARENT_SPEC=ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2E_SPEC.md
AUTHORITY=R7-R2E long-KV numerical preflight and candidate kernel
TOLERANCE_WIDENING=forbidden
PRODUCTION_ROUTE_MUTATION=forbidden
```

## 1. Runtime finding

The first instrumented R7-R2E long-KV preflight established:

```text
score bit mismatch count=0
tile-max bit mismatch count=0
probability envelope violations=0
output envelope violations=0
non-finite count=0
```

The only failed surface was the denominator produced by repeated online tile rescaling:

```text
KV 768:  max denominator ULP=20
KV 1536: max denominator ULP=41
KV 2048: max denominator ULP=51
```

The sealed denominator envelope remains:

```text
maximum ULP error <= 16
maximum relative error <= 2.0e-6
```

The envelope must not be widened after observing runtime data.

## 2. Canonical repair

The GQA4 candidate continues to use subgroup-online tiled execution for:

```text
exact score generation
tile maximum reduction
running maximum discovery
streaming structural accounting
shared K/V population and four-head consumption
```

After all tile scores are stored and the exact final row maximum is known, each query-head subgroup leader performs a denominator canonicalization pass:

```text
canonical_sum=0
for kv_position in ascending visible order:
    canonical_sum += exp(score[kv_position]-final_row_max)
```

The candidate then publishes:

```text
shared_running_sum=query-head canonical_sum
denominator=row canonical_sum
probability=exp(score-final_row_max)/canonical_sum
```

The operation order matches the reference denominator loop. The repair does not change Q/K/V identity, score order, texture coordinates, texture-load count, shared K/V reuse factor, page generation, output ownership, or production-route isolation.

## 3. Barrier contract

Before the canonicalization leader reads stored scores:

```text
storageBarrier
workgroupBarrier
```

After the leader publishes the canonical denominator:

```text
workgroupBarrier
storageBarrier
```

All barriers remain in uniform control flow.

## 4. Performance accounting

The canonicalization loop is part of the candidate attention dispatch and therefore remains inside the candidate GPU timestamp span. It must not be hidden as setup or validation overhead.

Shared texture-load accounting remains unchanged:

```text
candidate physical K loads=KV length*16 vec4
candidate physical V loads=KV length*16 vec4
reference physical K loads=candidate*4
reference physical V loads=candidate*4
```

No additional K/V texture load is introduced by denominator canonicalization because it reads the already stored score surface.

## 5. Receipt requirements

Rust must emit:

```text
long_kv_denominator_canonicalization_pass
```

The field is true only when every R7-R2E performance bucket reports:

```text
denominator_envelope_violation_count=0
```

R7-R2E preflight PASS requires all of:

```text
parent_numerical_preflight_pass=true
long_kv_capacity_preflight_pass=true
long_kv_denominator_canonicalization_pass=true
```

The R7-R2E static source receipt must verify the canonical ascending score re-sum exists in the candidate shader.

## 6. Fail-closed conditions

The revision remains HOLD when any of the following occurs:

```text
canonicalization source check absent
denominator envelope violation count nonzero
canonical loop reads beyond visible KV range
canonical denominator not published to shared state
canonicalization performed outside the timestamp span
additional K/V texture loads attributed to canonicalization
tolerance widened instead of arithmetic repaired
```

## 7. Supersession

This addendum supersedes only the statement in the parent R7-R2E specification that the long-KV extension changes capacity only. The 64-tile capacity extension now also includes exact-order denominator canonicalization required to preserve the pre-existing fixed numerical envelope through KV length 2048.

All other R7-R2E policies remain unchanged.