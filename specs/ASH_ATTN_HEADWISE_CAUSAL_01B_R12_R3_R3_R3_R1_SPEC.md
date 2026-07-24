# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1

## Input Identity Digest Helper Carry-Forward /
## Exact QKV Byte-Order Binding /
## Missing Symbol Compile Closure Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
runtime_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
input_identity_digest_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R1
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
micro_atlas_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
timestamp_measurement_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
promotion_scope=incremental_decode_only
```

R1 is a compile-closure revision. It does not change attention math, WGSL, query-atlas topology, timestamp boundaries, route policy, guard ownership, or performance thresholds.

## 1. Failure binding

Observed compiler failure:

```text
error[E0425]: cannot find function `digest_f32_inputs` in this scope
```

Observed call:

```rust
let input_identity_digest = digest_f32_inputs(&q_values, &k_values, &v_values);
```

The R3 gate carried the call forward from R2 but omitted the helper definition. No R3 runtime artifact or verdict from the failed build is authoritative.

## 2. Required helper

```rust
fn digest_f32_inputs(q: &[f32], k: &[f32], v: &[f32]) -> String {
    let mut hasher = Sha256::new();
    for values in [q, k, v] {
        for value in values {
            hasher.update(value.to_le_bytes());
        }
    }
    format!("{:x}", hasher.finalize())
}
```

Required semantic contract:

```text
digest algorithm=SHA-256
tensor order=Q,K,V
element order=original slice order
byte order=little-endian
bytes per element=4
```

Forbidden:

```text
to_ne_bytes
to_be_bytes
textual float formatting
JSON float serialization
pointer/address hashing
value sorting
length/separator/tag insertion into the digest stream
signed-zero normalization
NaN payload normalization
unsafe host-memory reinterpretation
```

## 3. Exact byte-stream binding

For Q, K and V arrays, the canonical stream is:

```text
LE32(q[0]) || ... || LE32(q[q_len-1])
|| LE32(k[0]) || ... || LE32(k[k_len-1])
|| LE32(v[0]) || ... || LE32(v[v_len-1])
```

`+0.0` and `-0.0` remain distinct. Distinct NaN payloads remain distinct. Subnormals and infinities are not normalized.

Length and shape identity remain separate receipt fields. They do not alter the carried-forward digest stream.

## 4. Pair identity binding

Every direct-kernel pair and every Reference/Atlas production pair must bind one shared input digest.

```text
pair_input_digest_mismatch_count=0
pair_input_shape_mismatch_count=0
pair_input_length_mismatch_count=0
```

A mismatch fails the complete bucket. Silent pair removal is forbidden.

## 5. Static truth

Required executable checks:

```text
digest_f32_inputs definition count=1
digest_f32_inputs call count>=1
Sha256::new reachable=true
to_le_bytes reachable=true
Q before K before V=true
to_ne_bytes absent=true
to_be_bytes absent=true
unsafe reinterpretation absent=true
```

The helper is included in source-tree digest binding. The build revision and input digest revision are emitted in the primary artifact and manifest.

## 6. Digest fixtures

Mandatory fixture families:

```text
empty tensors
single zero
signed-zero distinction
tensor-order distinction
element-order distinction
distinct NaN payloads
positive/negative infinity
known little-endian [1.0]/[2.0]/[3.0] vector
mixed Q/K/V lengths
production-shaped Q/K/V sample
```

Parent R2 helper parity must be exact for identical input slices.

## 7. Negative controls

R1 inherits 800 R3 controls and adds 20 digest controls:

```text
ID01 DigestFunctionMissing
ID02 DigestFunctionDuplicate
ID03 DigestCallMissing
ID04 QKVTensorOrderReversed
ID05 QAndKOrderSwapped
ID06 KAndVOrderSwapped
ID07 ElementOrderSorted
ID08 NativeEndianBytesUsed
ID09 BigEndianBytesUsed
ID10 TextFloatHashingUsed
ID11 JsonFloatHashingUsed
ID12 LengthInsertedIntoDigestStream
ID13 SeparatorInsertedIntoDigestStream
ID14 SignedZeroCanonicalized
ID15 NaNPayloadCanonicalized
ID16 UnsafeRawMemoryHashingUsed
ID17 PairDigestMismatchIgnored
ID18 PairShapeMismatchIgnored
ID19 ParentDigestParityFailureIgnored
ID20 InputIdentityReceiptDigestMismatch
```

Required aggregate after runtime execution:

```text
negative_control_count=820
negative_control_executed_count=820
negative_control_skipped_count=0
negative_control_fail_count=0
```

## 8. Required source changes

```text
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_r3_r3_gate.rs
specs/ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R1_SPEC.md
```

No backend, model-core, shader, route-LUT, or Cargo-bin registration change is required.

## 9. Compile closure

Canonical check:

```powershell
cargo check --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_r3_gate
```

Required:

```text
E0425 digest_f32_inputs count=0
missing symbol count=0
gate binary compile success=true
```

Warnings unrelated to R3-R1 do not fail this seal unless warnings are promoted to errors.

## 10. PASS boundary

```text
PASS =
  digest helper defined exactly once
  && helper call remains reachable
  && exact Q,K,V little-endian stream preserved
  && no native/big-endian or serialized-float path
  && signed zero and NaN payload bits preserved
  && parent helper parity passes
  && pair input identity mismatches=0
  && 20 new controls pass
  && total controls=820
  && E0425 is absent
  && gate binary compiles
  && runtime schema remains R3
  && build revision is R3-R1
```

Runtime promotion still requires the complete R3 GPU gate to execute and PASS.

## 11. Claim boundary

PASS proves only helper carry-forward, exact QKV byte-order binding and missing-symbol compile closure.

PASS does not prove query-atlas runtime validity, timestamp feature availability, 1024 GQA2 admission, 512/1024/2048 tail closure, attention promotion, canonical decode E2E or model-quality improvement.

Expected compile-closure token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R1_INPUT_IDENTITY_DIGEST_HELPER_CARRY_FORWARD_EXACT_QKV_LITTLE_ENDIAN_BYTE_ORDER_BINDING_MISSING_SYMBOL_COMPILE_CLOSURE_NO_RUNTIME_PROMOTION_CLAIM
```

Expected HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R1_INPUT_IDENTITY_DIGEST_HELPER_OR_COMPILE_CLOSURE_INCOMPLETE
```
