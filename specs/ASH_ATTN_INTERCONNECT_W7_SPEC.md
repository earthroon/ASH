# ASH-ATTN-INTERCONNECT-W7

## Patch identity

- Patch ID: `ASH-ATTN-INTERCONNECT-W7`
- Build revision: `W7-w6-global-state-frozen-kv-replay-stage12-shadow-r1`
- Parent authority: `ASH-ATTN-INTERCONNECT-W6-R1C`
- Production writer authority: `HeadwiseFullActive`
- TensorCube output commit authority: denied

## Scope

W7 adopts the W6 device-local global softmax state and replays the same frozen K/V partition in canonical chunk order. Each replay chunk is uploaded through Texture-06, consumed directly by TensorCube Stage12, and retired only after submission completion. Stage12 recomputes Q·K scores, applies the W6 global maximum and denominator, accumulates weighted V values, and produces a device-local context candidate for W8 adoption review.

## Required path

```text
W6 global softmax state
+ live Q RawWgpuBufferLease
+ same frozen canonical K/V partition
-> Texture-06 K/V replay upload
-> TensorCube Stage12 texture candidate
-> raw K/V oracle
-> cross-chunk context numerator
-> global denominator normalization
-> candidate/oracle GPU parity
-> optional physical-gate CPU f64 parity
-> W8 context candidate handoff
```

## Fixed execution profile

```text
query heads       32
KV heads           4
GQA group size     8
head dimension    64
query tile rows   16
subgroup size     32
texture format    rgba32float
texture dimension D2Array
```

Dynamic geometry includes `q_seq`, active query rows, chunk token start/count, KV block count, absolute Q/K positions, partition generation, and canonical replay ordinal.

## Frozen partition replay authority

W7 must not select a new partition. The replay plan is derived only from the W6 canonical stream plan.

Required invariants:

- partition generation unchanged
- partition digest unchanged
- canonical chunk-order digest unchanged
- chunk token ranges unchanged
- no hole or overlap
- replay step ordinal equals canonical chunk ordinal
- partition reselection count equals zero

Texture-06 slot capacity is bounded, so W7 does not retain every first-pass texture. It performs a second streaming pass over the same raw K/V leases and descriptors.

## Stage12 candidate path

Candidate bindings:

```text
0 params uniform
1 Q raw storage buffer
2 K rgba32float D2Array texture
3 V rgba32float D2Array texture
4 W6 candidate global state
5 candidate context numerator
6 candidate write counts
7 shared status ABI
```

Candidate shader requirements:

- direct `textureLoad` from K and V textures
- no texture-to-buffer rehydration
- no full score matrix
- no full probability matrix
- causal position checks use absolute Q/K positions
- GQA mapping is `kv_head = query_head / 8`
- score scaling is `1 / sqrt(head_dim)`
- weight is `exp(score - global_max)`
- numerator accumulates `weight * V`

## Stage12 raw oracle path

Oracle bindings mirror the candidate path but consume canonical raw K and V leases directly. The oracle must use the same W6 oracle global state, descriptor stream, causal mask, GQA mapping, score scaling, and replay ordinal.

The raw oracle is not a texture rehydration path. It consumes the existing canonical raw leases owned by the frozen partition.

## Global normalization

For valid rows:

```text
context = accumulated_numerator / W6_global_denominator
```

For all-masked rows:

```text
global max    = -infinity
denominator   = 0
context       = exact zero
V read count  = 0 for masked token contributions
no divide     = true
```

Inactive rows must also produce exact zero context.

## Context ABI

Context layout is:

```text
[q_token][query_head][head_dim]
f32 contiguous
```

The context candidate is device-local and remains non-authoritative. Runtime payload readback is prohibited. Only physical gates may request compact or full readback for parity evidence.

## Status ABI

Stage12 uses a 128-byte, 32-word status buffer:

```text
0..7    candidate replay diagnostics
8..15   oracle replay diagnostics
16..31  normalize and final parity diagnostics
```

Candidate and oracle lanes separately report invalid global state, descriptor bounds, prior-write order, non-finite score, non-finite V, non-finite numerator, duplicate writes, and reserved faults.

Final lanes report candidate/oracle mismatch, non-finite context, all-masked nonzero context, inactive nonzero context, denominator violations, missing or duplicate final writes, valid/all-masked/inactive counts, compared scalar count, candidate/oracle chunk write counts, CPU reference mismatch, and reserved faults.

## Canonical prior-write authority

The host canonical replay plan independently emits `expected_prior_chunk_write_count`. The shader compares that value to the previous value returned by `atomicAdd(write_count, 1)`.

The following is forbidden:

```text
expected ordinal copied from actual ordinal and compared to itself
```

## Submission and ownership

For every replay chunk:

```text
Texture-06 upload owner
+ W7 Stage12 consumer owner
-> K/V upload
-> candidate dispatch
-> oracle dispatch
-> queue submit
-> completion callback
-> Stage12 consumer owner-zero
-> texture slot retirement eligibility
```

The W6 global-state handle remains owned until Stage12 normalization and parity complete. It is drained before the W7 receipt is sealed. The W7 context handle is retained for W8.

## Physical verification

The physical gate must run the complete live path:

```text
Headwise live Q/K/V
-> W5 Stage10 local statistics
-> W6 Stage11 global softmax state
-> drain first-pass Texture-06 slots
-> W7 frozen K/V replay
-> Stage12 candidate and oracle
-> normalize and GPU parity
-> CPU f64 context parity
```

CPU f64 parity must use the original gate-owned Q/K/V values and the same absolute positions and causal mask. Candidate/oracle self-parity alone is insufficient.

## Forbidden paths

- full score matrix allocation
- full probability matrix allocation
- texture-to-buffer K rehydration
- texture-to-buffer V rehydration
- CPU Stage12 fallback
- host-side weighted-value accumulation
- runtime context payload readback
- partition reselection
- generation mutation during replay
- TensorCube output commit
- Headwise output mutation
- production route mutation

## Authority ledger

```text
HeadwiseFullActive     production attention writer
Texture-06             bounded K/V streaming residency
TensorCube Stage10     local score statistics producer
TensorCube Stage11     global softmax-state producer
TensorCube Stage12     non-authoritative context candidate producer
W8                     future adoption/parity authority review
```

## Completion gates

W7 passes only when:

- parent W6 receipt passes
- global state is W7-ready
- replay plan has exact canonical coverage
- partition reselection count is zero
- candidate and oracle dispatch counts are nonzero and exact
- K and V texture reads are observed
- candidate/oracle context mismatch count is zero
- CPU f64 context mismatch count is zero in the physical gate
- all-masked and inactive contexts are exact zero
- prior-write violations are zero
- missing/duplicate writes are zero
- non-finite context count is zero
- full score/probability allocations are zero
- texture rehydration count is zero
- TensorCube output commit count is zero
- production route mutation count is zero
- W6 global-state owner reaches zero
- replay texture slots reach owner-zero
- W8 context candidate handle remains live

## PASS token

```text
PASS_ASH_ATTN_INTERCONNECT_W7_W6_GLOBAL_SOFTMAX_STATE_ADOPTION_CANONICAL_FROZEN_KV_CHUNK_REPLAY_Q_RAW_KV_RGBA32F_TEXTURE_MIXED_BINDING_TENSORCUBE_STAGE12_FUSED_SCORE_RECOMPUTE_WEIGHTED_VALUE_ACCUMULATION_GLOBAL_MAX_DENOMINATOR_NORMALIZATION_CROSS_CHUNK_CONTEXT_ALL_MASKED_ZERO_GQA_PRESERVATION_NO_FULL_SCORE_NO_FULL_PROBABILITY_HEADWISE_FULLACTIVE_OUTPUT_AUTHORITY_SEALED
```
