# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6

## True Kernel-Only Dispatch Timestamp Surface /
## Mirrored Epoch Same-Input Identity Lock /
## Physical Post-Attention Resource Contract Parity /
## Paired Non-Inferiority Test Direction Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R5
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r6.runtime_artifact.v1
local_manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r6.local_manifest.v1
promotion_scope=incremental_decode_only
```

Revisions:

```text
performance_surface_revision=R2-R6
mirrored_input_identity_revision=R2-R6
physical_post_attention_contract_revision=R2-R6
paired_non_inferiority_revision=R2-R6
```

R2-R6 changes measurement implementation, physical comparison contracts and statistical authority. Attention equations, Single/GQA2 WGSL arithmetic, route thresholds, Q/K/V values, guard math, downstream math, ring domains and rollback policy remain unchanged.

## 1. Bound R2-R5 evidence

R2-R5 established static lexical truth, scratch/dealias truth and dimension-specific tail attribution. Source inspection left four unresolved defects:

1. The named kernel-only probe still timed guard, downstream, telemetry and clear work.
2. Ascending and descending probe epochs included the epoch index in the input seed and therefore used different values and native leases.
3. Matched guarded E2E used different candidate allocation classes and proved parity with a constant contract identifier instead of runtime resource fields.
4. The probability named regression probability used the lower tail for significant improvement. Non-inferiority and regression hypotheses were conflated.

## 2. True kernel-only surface

Authoritative API:

```rust
encode_native_atlas_kernel_only_measurement_span(
    prepared,
    output_scratch,
    encoder,
    forced_route,
)
```

The timestamp interval contains only start timestamp, attention bind and dispatch, and end timestamp.

Forbidden inside the interval:

```text
guard-map dispatch
guard finalizer
downstream indirect dispatch
telemetry copy
clear_buffer
query resolve
queue submit
device poll
buffer or pipeline creation
```

Required runtime counters:

```text
attention_dispatch_count=1
guard_dispatch_count=0
downstream_dispatch_count=0
telemetry_copy_count=0
clear_buffer_count=0
```

Single and GQA2 outputs use distinct buffers from the same native scratch allocator with equal size, usage, offset, alignment and mapped-at-creation policy.

## 3. Mirrored probe input SSOT

One retained input set is created per probe bucket before either epoch:

```rust
HeadwiseMirroredProbeInputSet {
    seed,
    q,
    k,
    v,
    prepared,
    value_digest,
    native_lease_digest,
    single_output,
    gqa2_output,
}
```

The bucket seed depends on the canonical probe seed and `seq_kv` only. It excludes epoch index, direction and execution position.

Ascending and descending epochs reuse the same retained prepared object. Admission requires equality of input seed, Q/K/V canonical little-endian value digest, Q/K/V native buffer identities, offsets and sizes, and native lease digest.

Thermal evidence has no authority unless value and native-lease identity both pass.

## 4. Physical matched guarded E2E contract

Reference and Atlas matched surfaces both allocate candidate and downstream buffers through the same native scratch factory:

```text
Reference candidate=native matched candidate scratch
Atlas candidate=native matched candidate scratch
Reference downstream=native matched downstream scratch
Atlas downstream=native matched downstream scratch
```

Within each surface, candidate and downstream identities differ. Across surfaces, corresponding buffers are distinct objects while retaining equal physical contracts.

The physical contract digest includes actual runtime fields:

```text
allocator revision
candidate bytes, usage, offset, mapped state, arena ownership
downstream bytes, usage, offset, mapped state, arena ownership
guard-map geometry
guard and finalizer workgroup sizes
decision ring capacity
symmetric slot policy
submission topology
```

A digest of a constant contract string alone is forbidden.

Matched Reference and Atlas execute attention, the same device guard map, the same guard finalizer, the same decision-token policy and the same guarded downstream dispatch. Only the attention pipeline identity may differ.

## 5. Slot and submission topology

For each 32-pair round:

```text
Reference decision slots=0..31
Atlas decision slots=32..63
measurement ring capacity=64
```

AB/BA order remains balanced. All encoded command buffers for a round are submitted in one queue submission. Query resolution and timestamp readback occur outside measured spans.

## 6. Paired non-inferiority policy

Versioned policy:

```text
policy_id=paired-sign-noninferiority-upper-bound-v1
margin_policy_id=paired-margin-1p05-v1
alpha=0.05
pair_margin_ratio=1.05
minimum_effective_pairs=512
tie_policy=exclude-boundary
```

For each pair:

```text
ratio=Atlas_time/Reference_time
delta=ln(ratio)-ln(margin)
```

Classification:

```text
delta>0  margin violation
delta<0  margin non-violation
delta=0  boundary tie excluded from effective N
```

Non-inferiority uses the lower tail of the violation count:

```text
p_noninferiority=P(X<=violations | N, p=0.5)
```

Regression is reported separately using the upper tail of Atlas-slower pairs at zero margin:

```text
p_regression=P(X>=AtlasSlower | N0, p=0.5)
```

Improvement is reported separately. Ambiguous `regression_probability` naming is forbidden.

Median and p95 effect-size gates remain independent and cannot be overridden by the statistical test:

```text
median_ratio<=1.0
p95_ratio<=1.05
paired_non_inferiority_p_value<=0.05
```

## 7. Route and promotion authority

```text
route candidate=true kernel-only speed evidence
route promotability=kernel speed + parity + order-bias validity + thermal validity
runtime promotion=route promotability + matched guarded E2E effect-size + paired non-inferiority + guard + canary + rollback + static truth
```

Old guarded probe samples and unmatched legacy surfaces are diagnostic-only.

## 8. Tail attribution

Tail buckets 512, 1024 and 2048 preserve these dimensions independently:

```text
kernel speed
kernel parity
kernel order bias
kernel thermal
matched guarded E2E median/p95
matched guarded E2E non-inferiority
physical contract parity
scratch and alias integrity
```

A guarded E2E failure may not be reported as thermal failure.

## 9. Required CLI

```text
--kernel-timestamp-surface attention-dispatch-only
--require-kernel-guard-dispatch-zero true
--require-kernel-downstream-dispatch-zero true
--require-kernel-telemetry-copy-zero true
--require-kernel-clear-zero true
--probe-input-policy retained-per-bucket-v1
--probe-input-seed-policy bucket-only-no-epoch-v1
--require-mirrored-input-value-identity true
--require-mirrored-native-lease-identity true
--require-thermal-input-identity-lock true
--matched-candidate-storage shared-native-scratch-factory
--matched-downstream-storage shared-native-scratch-factory
--require-physical-candidate-contract-parity true
--require-physical-downstream-contract-parity true
--require-physical-guard-contract-parity true
--require-submission-topology-parity true
--forbid-constant-only-physical-contract-digest true
--paired-test-policy paired-sign-noninferiority-upper-bound-v1
--paired-non-inferiority-alpha 0.05
--paired-non-inferiority-margin-ratio 1.05
--paired-non-inferiority-minimum-effective-pairs 512
--paired-tie-policy exclude-boundary
--require-paired-test-direction-lower-tail true
--require-regression-test-direction-upper-tail true
--forbid-ambiguous-regression-probability-field true
--expected-negative-controls 1120
```

## 10. Negative controls

R2-R6 inherits 1080 controls and adds 40:

```text
kernel-only surface=10
mirrored input identity=10
physical contract parity=10
statistical direction=10

total=1120
executed=1120
skipped=0
fail=0
```

## 11. PASS boundary

PASS requires exact R2-R5 binding, preserved R2-R4 scratch/dealias truth and R2-R5 lexical/tail truth, zero non-attention operations in kernel-only timestamps, matched Single/GQA2 output contracts, identical retained probe inputs across epochs, valid kernel speed/order-bias/thermal evidence, physical Reference/Atlas contract equality, median and p95 non-regression, paired non-inferiority PASS, exact tail attribution, guard/canary/rollback PASS, 1120 controls and artifact digest truth.

PASS does not prove universal adapter performance, that Atlas is faster than Reference on the current adapter, transactional KV rollback, canonical full-model decode or model-quality improvement.

## 12. Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R6_TRUE_KERNEL_ONLY_DISPATCH_TIMESTAMP_SURFACE_MIRRORED_EPOCH_SAME_INPUT_IDENTITY_PHYSICAL_POST_ATTENTION_RESOURCE_CONTRACT_PARITY_PAIRED_NON_INFERIORITY_TEST_DIRECTION_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R6_TRUE_KERNEL_AND_MIRRORED_INPUT_TRUTH_ESTABLISHED_MATCHED_GUARDED_E2E_NON_INFERIORITY_INCOMPLETE
```
