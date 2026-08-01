# ASH-ATTN-INTERCONNECT-W6-R1B

## WGSL26 Float Classification /
## Bitwise Finite Guard /
## Stage11 Merge·Verify Parser Closure /
## Candidate·Oracle·Verify Status Lane Separation /
## Canonical Prior-Write Order Authority /
## Latent Non-Standard Builtin Inventory /
## No Recursion·No Feature Relaxation Seal

Status: correction specification rev.1

## Purpose

Close the WGPU 26 shader-module parsing failure caused by non-standard `isNan`, `isInf`, and `isFinite` calls in the Stage11 online-softmax merge and verify shaders. Preserve the W6 numerical contract while separating candidate, oracle, and final-verify diagnostics and replacing self-referential chunk-order checks with an independent prior-write authority.

## Direct failure

Observed failure:

```text
Device::create_shader_module
label = w6.tensorcube.stage11.online_softmax.merge.shader
WGSL parsing error: no definition in scope for identifier isNan
```

Affected direct files:

```text
crates/burn_webgpu_backend/src/shaders/
  tensorcube_stage11_online_softmax_merge.wgsl
  tensorcube_stage11_online_softmax_verify.wgsl
```

## Scope

Modify:

```text
crates/burn_webgpu_backend/src/shaders/
  tensorcube_stage11_online_softmax_merge.wgsl
  tensorcube_stage11_online_softmax_verify.wgsl

crates/burn_webgpu_backend/src/
  tensorcube_stage11_online_softmax_merge.rs

crates/model_core/src/
  attention_interconnect_w6.rs

crates/orchestrator_local/src/bin/
  ash_attn_interconnect_w6_verification_gate.rs
  ash_attn_interconnect_w6_physical_gate.rs

crates/orchestrator_local/src/
  attention_interconnect_w6_artifact_wave_map.rs
```

Do not modify W5 Stage10 score math, Texture-06 upload, W4 live Headwise binding, V consumption, Stage12, Decode, BaseTrain, or Headwise production output authority.

## Authority SSOT

| State | Authority |
|---|---|
| Stage11 numerical formula | W6 online-softmax merge contract |
| f32 classification | R1B bitwise classification contract |
| candidate diagnostics | status words 0..7 |
| oracle diagnostics | status words 8..15 |
| final verify diagnostics | status words 16..31 |
| canonical descriptor order | W6 host canonical stream plan |
| prior-write expectation | host-derived `expected_prior_write_count` |
| actual write progression | previous value returned by GPU `atomicAdd` |
| all-masked representation | exact negative infinity bits, zero sum, zero count |
| production attention output | Headwise FullActive |

## WGSL26 float classification

Stage11 direct shaders must contain zero calls to:

```text
isNan
isInf
isFinite
```

Use IEEE-754 binary32 bit classification:

```wgsl
const F32_EXPONENT_MASK: u32 = 0x7f800000u;
const F32_MANTISSA_MASK: u32 = 0x007fffffu;

const F32_CLASS_FINITE: u32 = 0u;
const F32_CLASS_INFINITY: u32 = 1u;
const F32_CLASS_NAN: u32 = 2u;

fn classify_f32(value: f32) -> u32 {
    let bits = bitcast<u32>(value);
    let exponent = bits & F32_EXPONENT_MASK;
    if (exponent != F32_EXPONENT_MASK) {
        return F32_CLASS_FINITE;
    }
    let mantissa = bits & F32_MANTISSA_MASK;
    return select(F32_CLASS_INFINITY, F32_CLASS_NAN, mantissa != 0u);
}

fn finite_f32(value: f32) -> bool {
    return classify_f32(value) == F32_CLASS_FINITE;
}
```

Required fixtures:

```text
+0.0
-0.0
smallest positive subnormal
largest finite f32
+infinity
-infinity
quiet NaN
nonzero-mantissa NaN
```

All-masked state may use exact negative infinity only under the canonical invalid-row contract:

```text
valid false
all_masked true
max_bits 0xff800000
sum_bits 0
count 0
```

Valid records containing infinity or NaN fail closed.

## Stage11 formula preservation

R1B must not change the online-softmax recurrence:

```text
M_next = max(M, m)
S_next = S * exp(M - M_next) + s * exp(m - M_next)
N_next = N + n
```

Invalid local records leave running state unchanged.

## Status ABI v2

Replace the shared 64-byte status buffer with:

```text
size   128 bytes
words  32 x atomic<u32>
init   all zero
```

Lane ownership:

```text
0..7    candidate merge only
8..15   oracle merge only
16..31  final verify only
```

Cross-phase writes are ABI violations.

### Candidate lanes

```text
0 candidate_local_contract_violation_count
1 candidate_count_overflow_count
2 candidate_descriptor_bounds_violation_count
3 candidate_prior_write_order_violation_count
4 candidate_non_finite_merged_state_count
5 candidate_local_nan_count
6 candidate_local_infinity_count
7 candidate_reserved_violation_count
```

### Oracle lanes

```text
8  oracle_local_contract_violation_count
9  oracle_count_overflow_count
10 oracle_descriptor_bounds_violation_count
11 oracle_prior_write_order_violation_count
12 oracle_non_finite_merged_state_count
13 oracle_local_nan_count
14 oracle_local_infinity_count
15 oracle_reserved_violation_count
```

### Final verify lanes

```text
16 candidate_oracle_mismatch_count
17 candidate_final_non_finite_count
18 oracle_final_non_finite_count
19 invalid_zero_sum_or_mask_contract_count
20 final_count_overflow_count
21 missing_final_write_count
22 duplicate_write_count
23 canonical_order_violation_count
24 valid_row_count
25 all_masked_row_count
26 inactive_row_count
27 compared_record_count
28 candidate_write_count_mismatch_count
29 oracle_write_count_mismatch_count
30 inactive_record_nonzero_count
31 verify_reserved_violation_count
```

## Canonical prior-write authority

Remove the self-referential check:

```text
chunk_ordinal == expected_chunk_ordinal
```

Host canonical planning must independently derive:

```text
expected_prior_write_count
```

GPU merge must compare it with the previous value returned from:

```wgsl
let actual_prior = atomicAdd(&write_counts.values[global_record_id], 1u);
```

Required invariant:

```text
actual_prior == expected_prior_write_count
```

Candidate and oracle use independent write-count buffers. Physical completion order, texture slot number, heat score, and submission callback order are not numerical merge authority.

## Latent non-standard builtin inventory

Inventory but do not silently modify:

```text
headwise_atlas_attention_texture_lut_alpha_scale.wgsl
headwise_atlas_attention_texture_lut_alpha_scale_sparse.wgsl
headwise_atlas_attention_texture_lut_alpha_scale_sparse_gpu.wgsl
```

Current expected inventory:

```text
latent files       3
latent call sites 18
```

Scan patterns:

```regex
\bisNan\s*\(
\bisInf\s*\(
\bisFinite\s*\(
```

Stage11 direct files require zero matches. Latent inventory is sorted by path, line, and identifier before digesting.

## No-recursion and no-feature-relaxation seal

Forbidden:

```text
recursion_limit increase
giant json macro reintroduction
WGPU validation disable
Naga parser bypass
unsafe shader module creation
SPIR-V bypass injection
required feature reduction
subgroup removal
SHADER_INT64 removal
timestamp-query removal
CPU Stage11 fallback
host-side full-statistics merge
```

Required features remain unchanged from W6-R1A.

## Resource and authority preservation

Preserve:

```text
W5 retained Stage10 candidate/oracle buffers
→ W6 merge submission
→ W6 completion observed
→ W6 final state retained
→ Stage10 statistics owner-zero
```

Must remain zero:

```text
full score matrix allocation
full probability matrix allocation
V read
Stage12 dispatch
TensorCube output commit
Headwise authority mutation
```

## Verification gate

Required checks:

```text
Stage11 direct non-standard builtin count 0
classify_f32 present
exponent and mantissa masks present
MergeParams ABI exact
VerifyParams ABI exact
status size 128 bytes
candidate base 0
oracle base 8
verify base 16
classification fixtures PASS
lane isolation negative controls PASS
prior-write negative controls PASS
recursion-limit workaround count 0
feature relaxation count 0
```

## Physical gate

Physical path:

```text
W4 live Headwise Q/K
→ Texture-06 K chunks
→ W5 Stage10 candidate/oracle statistics
→ retained device-local handles
→ W6 candidate merge at status base 0
→ W6 oracle merge at status base 8
→ W6 final verify at status base 16
→ 128-byte compact status readback
→ candidate final state readback
→ CPU f64 oracle
→ owner-zero
```

Required observations:

```text
merge shader module created
verify shader module created
merge pipeline created
verify pipeline created
candidate dispatch count > 0
oracle dispatch count > 0
verify dispatch count == 1
completion observed
```

## Completion gate

```text
Compile closure                         PASS
Merge shader parser closure             PASS
Verify shader parser closure            PASS
Bitwise classification fixtures         PASS
Candidate merge status cross-write         0
Oracle merge status cross-write            0
Verify status cross-write                  0
Canonical prior-write violations           0
Candidate/oracle final mismatch             0
Non-finite valid state count                0
All-masked contract violations              0
Candidate write count mismatch               0
Oracle write count mismatch                  0
CPU f64 oracle parity                     PASS
Full score matrix allocation                0
Full probability matrix allocation          0
V read                                      0
Stage12 dispatch                            0
TensorCube output commit                    0
Headwise authority mutation                 0
Recursion-limit workaround                  0
Feature relaxation                          0
```

## W7 handoff

R1B does not open W7. W7 may consume W6 global state only after Stage11 ABI v2, status ABI v2, all failure lanes zero, exact write counts, canonical all-masked state, CPU f64 parity, completion observation, and valid owner resource IDs.

## PASS token

```text
PASS_ASH_ATTN_INTERCONNECT_W6_R1B_WGSL26_FLOAT_CLASSIFICATION_BITWISE_FINITE_GUARD_STAGE11_MERGE_VERIFY_PARSER_CLOSURE_CANDIDATE_ORACLE_VERIFY_STATUS_LANE_SEPARATION_CANONICAL_PRIOR_WRITE_ORDER_AUTHORITY_LATENT_NON_STANDARD_BUILTIN_INVENTORY_NO_RECURSION_NO_FEATURE_RELAXATION_SEALED
```
