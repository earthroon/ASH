base_train_atlas_wave_02_r5_rope_interleaved_adjacent.wgsl
```

Each pipeline contains one pairing formula.

The host selects a pipeline only after validating the sealed convention authority.

A single shader with an undocumented fallback branch is forbidden.

A single shader with an explicit layout code may be admitted only if:

```text
invalid code traps or produces gate failure
both branches have physical known-vector coverage
pipeline receipt records selected code
no default branch maps to a valid convention
```

Separate shader modules are preferred because their module digests become direct evidence.

---

# 12. WGSL indexing contracts

## 12.1 Common domain decomposition

Let:

```text
TQ = batch × seq × query_heads
TK = batch × seq × kv_heads
P  = rotary_dim / 2
```

Required pair invocation counts:

```text
Q pair invocations = TQ × P
K pair invocations = TK × P
```

Q and K counts remain separate.

## 12.2 NeoX half-split indexing

For pair index `i`:

```wgsl
let lane_a = i;
let lane_b = i + params.rotary_dim / 2u;
```

Frequency exponent:

```wgsl
let exponent = -2.0 * f32(i) / f32(params.rotary_dim);
```

## 12.3 Interleaved indexing

For pair index `i`:

```wgsl
let lane_a = 2u * i;
let lane_b = lane_a + 1u;
```

Frequency exponent remains:

```wgsl
let exponent = -2.0 * f32(i) / f32(params.rotary_dim);
```

The exponent must be derived from pair index, not from an accidentally layout-dependent lane variable.

## 12.4 Q and K base addresses

```text
Q base = token_index × q_width  + q_head  × head_dim
K base = token_index × kv_width + kv_head × head_dim
```

The Q base may not be reused for K.

## 12.5 Non-rotary tail

When `rotary_dim < head_dim`, the non-rotary tail is copied without modification. This path remains non-promoted but must be structurally represented.

---

# 13. CPU-f64 external convention reference

## 13.1 Independent reference contract

The CPU-f64 reference accepts an explicit:

```rust
BaseTrainAtlasWave02R5RopePairingLayout
```

It must not infer layout from shader names, build features, or profile kind.

## 13.2 Reference functions

Admitted split:

```rust
build_rope_reference_neox_half_split_f64(...)
build_rope_reference_interleaved_adjacent_f64(...)
```

or one exhaustive match with no wildcard arm.

## 13.3 No shared pair-index helper with WGSL generator

The CPU oracle and WGSL module must not share generated pair tables from one function. Otherwise the same indexing error can be duplicated into both sides.

They may share only sealed authority values:

```text
theta
rotary_dim
pairing layout ID
position IDs
Q/K shape
```

## 13.4 f64 and GPU f32 boundary

External theta is sealed as f64 bits.

GPU uniform theta is derived by checked conversion to f32.

Receipts record:

```text
source theta f64 bits
GPU theta f32 bits
round-trip f64 value
absolute conversion error
conversion finite
conversion positive
```

CPU external reference uses source f64 theta.

A secondary CPU-f32-emulation receipt may isolate expected transcendental precision differences.

---

# 14. Known-vector fixture

R5-R5 requires an independent, hand-sealed known-vector fixture.

## 14.1 Fixture geometry

```text
batch size       1
sequence length  2
query heads      4
KV heads         2
head dimension   4
rotary dimension 4
Q width          16
K width           8
theta             10000.0
positions         [0, 1]
layout            NeoXHalfSplit
```

Position 0 provides an identity control.

Position 1 distinguishes the layouts.

## 14.2 Position-1 input heads

```text
Q0 [ 1.0,  2.0,  3.0,  4.0]
Q1 [ 5.0,  6.0,  7.0,  8.0]
Q2 [ 9.0, 10.0, 11.0, 12.0]
Q3 [13.0, 14.0, 15.0, 16.0]

K0 [-1.0,  0.5, 2.0, -0.25]
K1 [ 3.0, -4.0, 1.5,  2.5]
```

## 14.3 Expected NeoX half-split outputs

The expected f64 values are:

```text
Q0 [-1.984110648556,  1.959900667497,  2.462377902412,  4.019799668335]
Q1 [-3.188785364315,  5.919701335827,  7.989471065116,  8.059599003338]
Q2 [-4.393460080074,  9.879502004157, 13.516564227821, 12.099398338342]
Q3 [-5.598134795833, 13.839302672487, 19.043657390525, 16.139197673345]

K0 [-2.223244275484,  0.502474958542, 0.239133626928, -0.244987583437]
K1 [ 0.358700440393, -4.024799585002, 3.334866413226,  2.459875667705]
```

The fixture file stores decimal strings and their parsed f64 bit patterns.

## 14.4 Interleaved counterfactual

For Q0, the adjacent-interleaved output is:

```text
[-1.142639663748, 1.922075596544, 2.959850667913, 4.029799501669]
```

It must not match the NeoX output under the admitted tolerance.

Required counterfactual assertions:

```text
NeoX expected vs Interleaved expected mismatch count > 0
maximum absolute difference > 0.1
GPU NeoX output matches NeoX expected
GPU NeoX output does not match Interleaved expected
CPU-f64 NeoX output matches NeoX expected
CPU-f64 Interleaved output matches Interleaved expected
```

## 14.5 Theta mutation control

A second control changes theta while preserving all other inputs:

```text
theta = 1000.0
```

The output must differ at the low-frequency pair.

This proves that the checkpoint theta is consumed rather than merely copied into a receipt.

---

# 15. Synthetic GQA end-to-end fixture

After the isolated known-vector gate passes, R5-R5 reruns the R5-R4 synthetic GQA prefill with the externally bound convention authority.

Required path:

```text
external config snapshot
  -> convention authority
  -> ModelSpec
  -> geometry authority
  -> Params
  -> resident Q/K/V
  -> QKV projection
  -> Q NeoX RoPE, 4 heads
  -> K NeoX RoPE, 2 heads
  -> quotient GQA attention
  -> CPU-f64 external-convention reference
  -> context parity
  -> live handoff
```

Required stage parity:

```text
embedding
RMSNorm
Q
K
V
Q_RoPE
K_RoPE
context
```

The Q/K pre-RoPE stages should remain unchanged from R5-R4.

Only Q_RoPE, K_RoPE, and downstream context are expected to change when switching from adjacent-interleaved to NeoX half-split.

---

# 16. Physical gate sequence
