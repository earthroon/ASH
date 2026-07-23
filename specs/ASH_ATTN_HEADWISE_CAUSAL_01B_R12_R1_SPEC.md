# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1

## WGSL IEEE-754 Finite Classification /
## Naga Parser Compatibility /
## Static Guard Source Truth Repair Seal

---

# 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
runtime_schema=ash.attn.headwise.causal.01b.r12.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
kernel_policy_change=false
commit_policy_change=false
performance_threshold_change=false
```

R12-R1 repairs the finite-guard shader parser closure only. It does not alter R12 authority semantics, output ownership, performance thresholds, or negative-control counts.

---

# 1. Observed failure

The first R12 canonical run failed during shader-module creation:

```text
Shader parsing error:
no definition in scope for identifier: isNan
```

The source used:

```wgsl
isNan(value)
isInf(value)
```

These identifiers are not accepted by the active `wgpu 26.0.1` / Naga WGSL parser.

---

# 2. Required repair

The guard must classify `f32` values through their IEEE-754 bit pattern:

```text
sign mask     = 0x80000000
exponent mask = 0x7f800000
mantissa mask = 0x007fffff
```

Classification:

```text
NaN:
  exponent == all ones
  && mantissa != 0

Positive infinity:
  exponent == all ones
  && mantissa == 0
  && sign == 0

Negative infinity:
  exponent == all ones
  && mantissa == 0
  && sign != 0

Finite:
  exponent != all ones
```

Canonical WGSL shape:

```wgsl
let value_bits = bitcast<u32>(value);
let exponent_bits = value_bits & F32_EXPONENT_MASK;
let mantissa_bits = value_bits & F32_MANTISSA_MASK;
let sign_bit = value_bits & F32_SIGN_MASK;
let exponent_all_ones = exponent_bits == F32_EXPONENT_MASK;
```

---

# 3. Numeric truth preservation

R12-R1 must preserve these counters exactly:

```text
non_finite_count
nan_count
positive_infinity_count
negative_infinity_count
visited_element_count
max_abs_bits
```

Required relation:

```text
nan_count
+ positive_infinity_count
+ negative_infinity_count
== non_finite_count
```

NaN and infinity return before `max_abs_bits` reduction.

Finite values, including:

```text
+0
-0
positive subnormal
negative subnormal
largest finite positive
largest finite negative
```

must remain eligible for `max_abs_bits` reduction.

---

# 4. Static truth repair

The R12 static checker must no longer require invalid WGSL identifiers.

Forbidden static predicate:

```text
guard_shader contains isNan
&& guard_shader contains isInf
```

Required predicate:

```text
guard shader contains @compute
guard shader contains bitcast<u32>
guard shader contains F32_SIGN_MASK
guard shader contains F32_EXPONENT_MASK
guard shader contains F32_MANTISSA_MASK
guard shader does not contain isNan(
guard shader does not contain isInf(
```

---

# 5. Revision boundary

Required runtime identity:

```text
boot revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
backend public ABI=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
model-core public ABI=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
attention kernel=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite guard=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
bootstrap=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
```

The public R12 API and runtime artifact schema remain unchanged.

---

# 6. PASS obligations

R12-R1 PASS requires the original R12 formula without relaxation, plus:

```text
finite-guard shader module parses successfully
finite-guard compute pipeline is created successfully
positive finite fixture passes
NaN fault fixture is rejected
positive-infinity fault fixture is rejected
negative-infinity fault fixture is rejected
classification sum is exact
static shader-source truth check passes
```

---

# 7. Canonical run

The canonical R12 command is unchanged:

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r11_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-value-readback true `
  --forbid-output-host-upload true `
  --guard-mode compact-async-readback `
  --require-finite-guard true `
  --guard-workgroup-size 256 `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --expected-negative-controls 240 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```
