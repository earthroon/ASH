# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4-C1

## Stage12 Deterministic Score Replay and Receipt Diagnostics Closure

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4`  
> Required parent state: R6-R3-C4 physical PASS  
> Build revision: `stage12-atlas-parallel-streaming-weighted-v-bhqd-deterministic-score-replay-v2`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

R6-R4 Stage12 must reconstruct every score with the same dimension-ascending floating-point accumulation order used by the Stage10 statistics that produced the frozen Stage11 global max and denominator. V accumulation remains 32-lane parallel. The Stage12 numerator and frozen denominator must never be derived from different QK dot reduction orders.

## 1. Root cause

The first R6-R4 physical run reached Stage12 and failed with `AW02R6R4Stage12ReceiptNotPass`.

Stage10 generated partial statistics with a dimension-ascending serial dot. The initial R6-R4 Stage12 reconstructed numerator weights through a 32-lane tree reduction. Stage12 therefore normalized numerator weights derived from one floating-point reduction order with a frozen denominator derived from another.

## 2. C1 correction

Both Stage12 paths replay the Stage10 score calculation exactly:

```text
candidate:
    lane 0 serially accumulates dimensions 0 .. 63 from Q buffer and K texture
    lane 0 publishes one shared weight
    32 lanes accumulate V dimensions in parallel

oracle:
    lane 0 serially accumulates dimensions 0 .. 63 from raw Q/K buffers
    lane 0 publishes one shared weight
    32 lanes accumulate raw V dimensions in parallel
```

Chunk ordering, causal admission, frozen max, frozen denominator, BHQD output layout and Headwise authority remain unchanged.

## 3. Static admission

The backend rejects R6-R4 candidate or oracle shaders containing `partial_dot` or `subgroupAdd`. Both shaders must contain the canonical dimension-ascending replay loop.

## 4. Receipt diagnostics

A failed compact receipt reports all nonzero status words and named counters for candidate/oracle mismatch, Headwise mismatch, non-finite values, denominator violations, write errors, row/layout errors and comparison coverage.

No context payload readback is introduced. Diagnostics remain derived from the existing 256-byte compact status buffer.

## 5. Preserved prohibitions

```text
full score matrix allocation = 0
full probability matrix allocation = 0
texture-to-buffer rehydration = 0
global-state payload readback = 0
context payload readback = 0
Headwise writer mutation = 0
TensorCube context commit = 0
OProj dispatch = 0
MLP dispatch = 0
next-layer dispatch = 0
production promotion = 0
```

## 6. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r4_stage12_weighted_v_context_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r4.args"
```
