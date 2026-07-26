# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F

## GQA4 Cluster Guard Binding / Matched Output Scratch and Downstream Contract / Guarded End-to-End Paired GPU Timestamp / Production-Route Shadow Eligibility Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2E-R7
PARENT_VERDICT=PROMOTE_R2E_R7_SELF_PRIMED_PAIRED_TIMESTAMP_MEASUREMENT_VALIDITY_AND_CORE_PERFORMANCE_SEALED
DEFAULT_VERDICT=HOLD

RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
RECEIPT_AUTHORITY=Rust-only
VERDICT_AUTHORITY=Rust-only

VALIDATION_SURFACE=production-contract-shadow-v1
PERFORMANCE_SURFACE=guarded-end-to-end-shadow-v1
REFERENCE_ROUTE=existing-production-headwise-reference-shadow-v1
CANDIDATE_ROUTE=gqa4-cluster-shadow-v1

PRODUCTION_ROUTE_MUTATION=forbidden
PRODUCTION_OUTPUT_COMMIT=forbidden
PRODUCTION_DECISION_TOKEN_WRITE=forbidden
PRODUCTION_DISPATCHER_REBIND=forbidden
ACTIVE_ROUTE_LUT_MUTATION=forbidden
KERNEL_ARITHMETIC_MUTATION=forbidden
NUMERICAL_TOLERANCE_WIDENING=forbidden
RAW_SAMPLE_FILTERING=forbidden
SELECTIVE_RERUN=forbidden
HOST_GUARD_DECISION=forbidden
PREBAKED_RUNTIME_EVIDENCE=forbidden
```

R2F takes the GQA4 candidate proven by R2E-R7 and binds it to a production-shaped, GPU-native guard and downstream contract in a measurement-only shadow domain. It must prove guarded eligibility without changing the active production route.

## 1. Parent authority

The R2E-R7 runtime artifact and local manifest are mandatory parents. Before GPU initialization, Rust must require:

```text
parent schema exact
parent patch id exact
parent pass=true
parent candidate_eligibility_pass=true
parent measurement_validity_pass=true
parent negative_control_expected=260
```

The candidate and reference WGSL SHA-256 values in the R2F static receipt must exactly match the parent static receipt. A kernel hash mismatch is an immediate HOLD.

## 2. Two independent measurement surfaces

R2F owns two independent evidence populations.

### 2.1 Kernel-only continuity surface

The parent R2E-R7 4-query-head surface is executed again through the existing `run_headwise_gqa4_cluster_performance` path.

```text
query heads=4
KV heads=1
head dimension=64
reference=4 single-head dispatches
candidate=1 GQA4 cluster dispatch
population=8192 paired samples
```

It remains the authority for continuity of the sealed kernel-only result.

### 2.2 Guarded production-contract surface

The guarded surface expands the unchanged GQA4 shader to the production guard shape.

```text
query heads=32
KV heads=4
query heads per KV=8
GQA4 clusters per KV head=2
query heads per cluster=4
head dimension=64
logical output elements=2048
logical output bytes=8192
```

Reference execution:

```text
32 single-query-head dispatches
```

Candidate execution:

```text
one dispatch call
dispatch_workgroups(1,4,2)
8 physical GQA4 cluster workgroups
32 query heads covered exactly once
```

Kernel-only and guarded samples cannot be substituted, merged, or reused across surfaces.

## 3. Production guard contract preservation

The existing production micro-atlas guard has a fixed 2,048-scalar contract. R2F must preserve that contract exactly rather than creating a reduced 256-scalar guard fork.

Canonical guard topology:

```text
logical elements=2048
query heads=32
head dimension=64
guard map workgroup size=64
guard map group count=8
guard finalizer workgroup size=32
ring domain=measurement-audit
ring capacity=64
```

The production-domain decision ring, production decision token, and production output owner remain untouched.

## 4. Matched output scratch

Reference and candidate measured outputs are allocated as dedicated native shadow buffers.

```text
shape=[1,32,1,64]
len elements=2048
len bytes=8192
element type=f32
usage=STORAGE
mapped_at_creation=false
```

Both leases must have exact shape, length, byte width, device, and generation parity.

Required alias results:

```text
reference output != candidate output
reference output != reference downstream
candidate output != candidate downstream
reference/candidate shadow output != production output
```

No output scratch may alias a guard token, timestamp resolve buffer, readback buffer, or downstream scratch.

## 5. Matched downstream scratch

Reference and candidate downstream buffers are created from one physical contract.

```text
shape=[1,32,1,64]
len elements=2048
len bytes=8192
usage=STORAGE|COPY_DST
mapped_at_creation=false
```

Both downstream buffers are cleared over the same exact range before each paired shadow execution. A one-sided clear, usage broadening, or range mismatch is HOLD.

The downstream shader is the existing GPU-gated production-compatible downstream copy. R2F does not claim full O-projection or residual performance.

## 6. Full-overwrite poison proof

Before each measured pair, Rust dispatches the R2F poison shader over both measured output buffers.

```text
poison value=0x7fc00000 canonical NaN
poisoned elements=2048
poison dispatch workgroups=8
poison occurs outside guarded timestamps
```

The measured attention path must overwrite all 2,048 scalars. The production guard must report:

```text
visited elements=2048
completion mask=0xff
failure mask=0
nonfinite count=0
```

Any remaining poison, numerical nonfinite, missing group completion, or incomplete visit count is HOLD.

## 7. Full-head numerical compare preflight

Before performance population, Rust executes a dedicated GPU comparison over the complete 2,048-scalar reference and candidate outputs.

Compact decision fields:

```text
nonfinite count
mismatch count
max absolute error bits
max relative error bits
first fault element
visited element count
```

Fixed envelope:

```text
absolute error <= 5e-5
relative error <= 5e-4 when |reference| >= 1e-4
visited element count=2048
nonfinite count=0
mismatch count=0
```

This compact decision may be read back during preflight. Payload output readback remains forbidden.

## 8. Self-primed guarded blocks

Each route is self-primed immediately before its guarded timestamp span.

Reference block:

```text
reference primer output, 32 single-head dispatches
reference begin timestamp
reference measured output, 32 single-head dispatches
production guard map
production guard finalizer
GPU-gated downstream copy
reference end timestamp
```

Candidate block:

```text
candidate primer output, dispatch_workgroups(1,4,2)
candidate begin timestamp
candidate measured output, dispatch_workgroups(1,4,2)
production guard map
production guard finalizer
GPU-gated downstream copy
candidate end timestamp
```

Primer outputs are dedicated, untimed, unread, and never part of promotion samples.

## 9. Guarded paired topology

AB pair:

```text
reference guarded block
candidate guarded block
```

BA pair:

```text
candidate guarded block
reference guarded block
```

Each pair uses:

```text
one command encoder
one queue submission
four timestamp queries
zero per-kernel submission
zero per-pair payload readback
```

The two compact guard tickets use unique measurement-ring slots within each 32-pair bucket visit.

## 10. Mirrored schedule

R2F inherits the R2E-R7 schedule exactly.

Schedule A:

```text
128,2048,256,1536,384,1024,512,768
```

Schedule B:

```text
768,512,1024,384,1536,256,2048,128
```

Population:

```text
32 global rounds
8 bucket visits per round
32 pairs per bucket visit
1024 pairs per bucket
8192 guarded paired samples
512 AB and 512 BA per bucket
512 mirrored_a and 512 mirrored_b per bucket
```

Pair order is deterministic:

```text
order_bit = pair_index_in_visit XOR global_round XOR bucket_position
0=AB
1=BA
```

## 11. Warmup

Warmup uses four mirrored global rounds when `warmup_pairs_per_bucket=128` and `pairs_per_bucket_visit=32`.

Warmup uses the same self-primed guarded route, scratch, guard, and downstream topology. Warmup records must all be valid, but warmup timestamps and samples are excluded from promotion statistics.

## 12. Guard telemetry authority

Guard decisions are produced by the GPU. The host may drain only compact telemetry after a complete 32-pair bucket visit.

Allowed:

```text
round-batched compact telemetry drain
round-batched timestamp resolve/readback
```

Forbidden:

```text
per-pair blocking guard readback
payload readback
host mismatch recomputation
host threshold override
host dispatch decision
production token write
```

Reference and candidate telemetry are classified by disjoint nonce domains.

## 13. Guarded raw sample authority

Each of the 8,192 guarded samples must retain:

```text
global round
mirrored epoch
bucket position
KV length
pair index
pair index in visit
AB/BA order
query/resolve/readback ring slots
reference nanoseconds
candidate nanoseconds
candidate/reference ratio
```

The following counts must be zero:

```text
sample filtering
outlier deletion
selective rerun
synthetic replacement
ratio clamping
```

## 14. Guarded statistics

Per bucket, Rust calculates from raw samples:

```text
pair count
effective pair count
AB and BA counts
reference distribution
candidate distribution
ratio median/p90/p95/p99
paired sign-test probability
success fraction
signed and absolute order bias
signed and absolute mirrored-epoch bias
```

Signed bias formulas:

```text
order signed=(median_AB-median_BA)/combined_median
epoch signed=(median_A-median_B)/combined_median
absolute=abs(signed)
```

Order limits remain 0.05. Mirrored-epoch limits remain 0.07.

## 15. Guarded non-inferiority

For every guarded bucket:

```text
effective pairs >= 512
paired upper-tail probability <= 0.05
ratio median <= 1.05
ratio p95 <= 1.10
```

All eight buckets must pass.

## 16. Guarded long-KV improvement

Eligibility buckets:

```text
512,768,1024,1536,2048
```

Per-bucket improvement:

```text
ratio median <= 0.98
ratio p95 <= 1.05
```

Global long-KV improvement requires:

```text
at least 3 of 5 eligibility buckets improve
1024 improves
1536 improves
2048 improves
```

The 0.98 guarded median threshold is surface-specific because identical guard and downstream cost is added to both routes. It is not a numerical-tolerance widening.

## 17. Physical and submission receipts

Rust publishes:

```text
matched output scratch pass
matched downstream scratch pass
output physical parity pass
downstream physical parity pass
reference/candidate alias zero
shadow/production alias zero
full overwrite pass
poison residue zero
submission topology parity
reference/candidate guard dispatch counts
reference/candidate downstream dispatch counts
reference/candidate poison dispatch counts
compact token readback count
payload readback count
candidate output commit count
production consumer count
active route mutation count
```

Physical truth must come from actual lease and buffer identities, not constant-only string digests.

## 18. Kernel-only continuity

The parent 4-head surface must still satisfy:

```text
kernel_only.pass=true
kernel_only.core_performance_pass=true
kernel_only.measurement_validity_pass=true
```

A guarded PASS cannot hide a kernel-only regression.

## 19. Shadow eligibility

Canonical eligibility:

```text
production_route_shadow_eligibility_pass =
    kernel_only_continuity
    AND full_head_mapping
    AND matched_output_scratch
    AND matched_downstream_scratch
    AND output_physical_parity
    AND downstream_physical_parity
    AND alias_zero
    AND full_overwrite
    AND poison_residue_zero
    AND guard_map_binding
    AND guard_finalizer_binding
    AND device_native_decision
    AND GPU-gated downstream
    AND submission_topology_parity
    AND all_bucket_guarded_noninferiority
    AND guarded_long_kv_improvement
    AND order_validity
    AND epoch_validity
    AND raw_sample_retention
```

Shadow eligibility does not authorize production routing.

## 20. Production isolation and rollback

Before and after R2F, Rust hashes:

```text
active dispatcher source
active buffer attention shader
parent artifact
parent manifest
output ABI identity
composite active-path digest
```

The snapshots must be exact-equal.

Required zero counts:

```text
payload readback=0
candidate output commit=0
production consumer=0
active route mutation=0
```

The existing production route is the rollback anchor.

## 21. Validation and first-fault behavior

Full-head comparison, scratch construction, guard topology, and downstream compatibility are validated before performance population. A validation failure must stop performance measurement and produce a Rust-authored HOLD artifact group.

If GPU bootstrap or guarded execution fails after the artifact output directory is available, Rust must still emit explicit unavailable/failure groups for:

```text
kernel-only continuity
guarded bucket statistics
guarded raw samples
guard validity
physical contract
shadow eligibility
```

A missing manifest group is not an acceptable substitute for a HOLD receipt.

## 22. CLI extension

Canonical enum keys:

```text
--gqa4-r2f-validation-surface production-contract-shadow-v1
--gqa4-r2f-performance-surface guarded-end-to-end-shadow-v1
--gqa4-r2f-reference-route existing-production-headwise-reference-shadow-v1
--gqa4-r2f-candidate-route gqa4-cluster-shadow-v1
--gqa4-r2f-output-scratch-factory matched-attention-output-scratch-factory-v1
--gqa4-r2f-downstream-scratch-factory matched-downstream-scratch-factory-v1
--gqa4-r2f-guard-mode device-native-micro-atlas-token-v1
--gqa4-r2f-downstream-probe production-compatible-identity-transform-v1
--gqa4-r2f-decision-policy gpu-native-compact-token-v1
--gqa4-r2f-timestamp-surfaces kernel-only,guarded-e2e
--gqa4-r2f-promotion-authority guarded-e2e-v1
--gqa4-r2f-shadow-eligibility-policy structural-validity-performance-isolation-v1
--gqa4-r2f-rollback-policy existing-production-route-anchor-v1
```

Required Boolean keys cover parent promotion, kernel identity, matched scratch, physical parity, alias zero, full overwrite, guard map/finalizer, device-native decision, no per-pair host wait, GPU-gated downstream, clear parity, submission parity, kernel continuity, guarded performance, order/epoch validity, raw samples, active-route protection, rollback, and authority order.

The inherited strict registry rejects duplicate, unknown, adhered, missing-value, positional, type-invalid, and semantically invalid tokens before GPU initialization.

## 23. Negative controls

R2F binds the parent 260 controls and executes 160 new controls, ten each across 16 groups:

```text
parent and kernel identity
output scratch parity
downstream scratch parity
alias matrix
full overwrite and poison
guard map
guard finalizer
GPU decision authority
downstream gate and clear
validation isolation
submission topology
kernel continuity
guarded non-inferiority
guarded long-KV improvement
raw sample authority
production isolation and rollback
```

Canonical total:

```text
parent=260
R2F=160
total=420
```

Runtime outcomes, not prebaked JSON, are authoritative.

## 24. Runtime outputs

Rust generates at runtime:

```text
parent binding
static checks
active path before/after
guarded shadow receipt
kernel-only receipt
guarded bucket statistics
guarded raw samples
guard validity
physical contract
shadow eligibility
negative registry and outcomes
strict CLI receipts
canonical run contract and command
runtime artifact
local manifest
verdict
```

## 25. Packaging

The distributed ZIP contains implementation and build source only.

It excludes:

```text
spec files
runtime artifact
manifest
receipt
verdict
runtime JSON
PowerShell
batch files
run-command text
prebaked runtime evidence
```

The specification is committed separately to `earthroon/ASH`.

## 26. PASS

PASS requires:

```text
parent R2E-R7 promoted
candidate/reference hashes unchanged
full-head GPU comparison pass
matched output/downstream contracts pass
all aliases zero
all poison overwritten
all guard tokens valid
GPU-gated downstream exact
kernel-only continuity pass
all guarded buckets noninferior
guarded long-KV improvement pass
order and epoch validity pass
8192 guarded raw samples retained
sample filtering and rerun zero
payload readback and output commit zero
active path unchanged
rollback anchor unchanged
420/420 controls pass
Rust artifact and manifest emitted
```

## 27. Summary

```text
[r2f][summary]
parent={}
kernel_identity={}
output_scratch={}
downstream_contract={}
full_overwrite={}
guard_map={}
guard_finalizer={}
gpu_decision={}
downstream_gate={}
submission_parity={}
kernel_continuity={}
guarded_noninferior={}
guarded_long_improved={}
order_valid={}
epoch_valid={}
raw_samples={}
isolation={}
rollback={}
shadow_eligible={}
negative={}/{}
active_route_unchanged={}
pass={}
```

## 28. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_GQA4_GUARDED_END_TO_END_PRODUCTION_ROUTE_SHADOW_ELIGIBILITY_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_GQA4_PRODUCTION_ROUTE_SHADOW_ELIGIBILITY_NOT_PROVEN
```

Representative failure dimensions:

```text
parent binding
kernel identity freeze
full-head mapping
output scratch
downstream contract
alias zero
full overwrite
poison residue
guard map
guard finalizer
GPU decision
downstream gate
submission parity
kernel continuity
guarded non-inferiority
guarded long-KV improvement
order validity
epoch validity
raw sample authority
production isolation
rollback anchor
negative controls
```

## 29. Non-goals

R2F does not perform:

```text
live production route activation
production LUT mutation
production output commit
reference retirement
fallback removal
full O-projection benchmark
full residual benchmark
full transformer-block benchmark
tokens-per-second claim
cold-start claim
kernel optimization
tolerance widening
```

## 30. Final seal

R2E-R7 proves that the 4-head GQA4 kernel is fast and measurement-stable. R2F proves that the unchanged kernel can cover all 32 production query heads, fully overwrite a production-shaped output, pass the existing production guard, drive a GPU-gated downstream contract, and retain its performance eligibility in a fully isolated shadow route.

Production adoption remains forbidden until a later explicit route-promotion revision.
