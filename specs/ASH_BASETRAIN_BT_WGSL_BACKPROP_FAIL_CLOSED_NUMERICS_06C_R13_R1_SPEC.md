# ASH-BASETRAIN-BT-WGSL-BACKPROP-FAIL-CLOSED-NUMERICS-06C-R13-R1

## R12 Physical Parent / R13 Same-Invocation Closure / WebGPU Dispatch-Grid Limit Repair / G204D No Gradient Zeroing / Row Fault Whole-Row Invalidation / No Partial Row-Dot Continuation / DKDV Uniform Preflight Hoist / Zero Inner-Loop Return / R13 SwiGLU Stable Derivative / R13 Explicit Nonfinite Status / No NaN Clamp / No Gradient Clamp / Host Hard-Fail Before Publication / Live-BQHD Synthetic CPU-f64 Oracle / Live-BQHD Directional Finite-Difference / Production Payload Readback Still Zero / Optimizer Commit Barrier Future Seal

> Patch ID: `ASH-BASETRAIN-BT-WGSL-BACKPROP-FAIL-CLOSED-NUMERICS-06C-R13-R1`
>
> Build revision: `bt-wgsl-backprop-fail-closed-numerics-06c-r13-r1`
>
> Physical parent: `BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12`
>
> Corrected code parent: `BT-WGSL-OPROJ-FFN-BACKWARD-06C-R13`
>
> Proof ledger: `HOLD`

---

## 1. Purpose

R13-R1 combines two corrections that belong to the same numerical-authority boundary:

1. Repair the physically observed WebGPU dispatch failure in R13 parameter-gradient tiles.
2. Promote G204D and R13 FFN numerics from post-hoc detection to fail-closed publication semantics.

The physical failure that triggered the dispatch repair was:

```text
dispatch group size = [90112, 1, 1]
max_compute_workgroups_per_dimension = 65535
```

R13-R1 does not reduce the logical 1024-row gradient tile merely to satisfy the API limit. It maps one logical 1D invocation range onto a bounded 2D dispatch grid and reconstructs the linear index in WGSL.

---

## 2. Dispatch-grid repair

For any one-dimensional R13 kernel with `N` scalar invocations:

```text
logicalWorkgroups = ceil(N / 64)
limit = device.limits().max_compute_workgroups_per_dimension

gridY = ceil(logicalWorkgroups / limit)
gridX = ceil(logicalWorkgroups / gridY)
```

Admission requires:

```text
gridX <= limit
gridY <= limit
```

WGSL reconstructs:

```text
linearIndex = global_id.x + global_id.y * gridX * 64
```

The previously failing 90,112-workgroup tile therefore becomes:

```text
gridX = 45,056
gridY = 2
```

while preserving the existing 1024-row logical gradient tile identity.

The same dispatch helper is used by R13 linear backward, SwiGLU, fixture seeding, and add/merge kernels so future 1D surfaces do not silently reintroduce the same limit violation.

---

## 3. G204D no gradient zeroing

The previous shader behavior on a nonfinite final accumulator was equivalent to:

```text
fault observed
→ status counter increment
→ gradient accumulator overwritten with 0
```

R13-R1 forbids this.

A faulted gradient is never converted into a valid-looking zero gradient.

Required:

```text
fault-gradient-zero-write count = 0
NaN clamp count = 0
gradient clamp count = 0
```

A faulted output carries an explicit invalid/nonfinite representation and the host rejects the invocation before a gradient authority is published.

---

## 4. Row fault whole-row invalidation

`backward_dq_rowdot` owns one complete `(q_row, q_head)` gradient row per workgroup.

If any probability, `dP`, row-dot accumulation, `dScore`, or dQ lane becomes nonfinite:

```text
shared_row_fault = 1
STATUS_NON_FINITE += 1
```

The workgroup continues only the synchronization structure required for barrier safety.

It does not continue a partial mathematical row.

Final result:

```text
entire dQ row = invalid/nonfinite
STATUS_DQ_ROW_FAULT += 1
```

The host hard-fails before constructing the returned dQ/dK/dV leases.

---

## 5. No partial row-dot continuation

The old path skipped a nonfinite `P*dP` term and retained the finite prefix of the row-dot sum.

That creates a mathematically invalid softmax VJP because the corrupted partial row-dot is reused by every key in the row.

R13-R1 changes the authority rule to:

```text
first nonfinite row-dot contribution
→ row fault
→ no further row-dot authority
→ no dScore authority from that row
→ host fail
```

No partial row-dot is promoted.

---

## 6. DKDV uniform preflight hoist

The old `backward_dkdv` contained a `return` inside nested loops that also contain workgroup barriers.

The index was currently workgroup-uniform, but safety depended on that invariant remaining unchanged.

R13-R1 hoists all state-capacity and geometry checks before the loops:

```text
requiredStateRecords = qSeq * qHeads
requiredQElements = qSeq * qHeads * headDim
requiredContextElements = requiredQElements
requiredKvElements = kvSeq * kvHeads * headDim
GQA exactness
```

Failure occurs before entering the barrier-bearing loop.

Required:

```text
innerLoopReturnCount = 0
```

---

## 7. DKDV fail-closed row semantics

Each `(key_row, kv_head)` workgroup owns one K/V gradient vector.

Any invalid global state or nonfinite probability/dScore/accumulator sets a workgroup fault.

The final dK/dV vector is marked invalid and:

```text
STATUS_DKDV_ROW_FAULT += 1
```

No faulted dK/dV vector is converted to zeros.

---

## 8. Host hard-fail before G204D publication

The compact G204D status buffer remains the only production readback.

Live admission requires all of:

```text
invalidGlobalStateCount = 0
nonFiniteGpuCount = 0
boundsViolationCount = 0
dqRowFaultCount = 0
dkdvRowFaultCount = 0
```

Only after these checks pass may the host construct and return GPU gradient leases.

Therefore:

```text
productionGradientPayloadReadbackCount = 0
```

remains unchanged.

---

## 9. Live G204D ABI

Fail-closed semantics change the live ABI identity to:

```text
ash.basetrain.g204d.attention_backward.live_bqhd.fail_closed.v2
```

Legacy probe entrypoints remain available, but use the same corrected shader and therefore inherit the no-zeroing and preflight safety changes.

---

## 10. Live-BQHD synthetic CPU-f64 oracle

R11/R12 already physically proved Q32 BQHD live execution and deterministic GPU fingerprints, but deterministic repetition alone cannot detect an identically wrong layout computation.

R13-R1 therefore adds a synthetic Q32 BQHD numerical canary:

```text
Q = 32
K = 8
Q heads = 32
KV heads = 4
head dim = 64
GQA = 8
layout = BQHD
```

The fixture is intentionally separate from production R10/R12 tape.

It generates deterministic Q/K/V/dContext and matching softmax global-state records, then runs the exact live-BQHD G204D path.

The synthetic outputs are read back only for oracle comparison.

Required distinction:

```text
syntheticOracleGradientReadbackCount = 3
productionGradientPayloadReadbackCount = 0
```

The oracle must not read production gradient payloads.

---

## 11. CPU-f64 parity

The synthetic live-BQHD gradients are compared against an independent CPU f64 implementation of:

```text
dP = dContext · V^T
rowDot = Σ(P * dP)
dScore = P * (dP - rowDot) * scale
dQ = dScore · K
dK = dScore^T · Q
dV = P^T · dContext
```

The CPU oracle uses BQHD indexing directly.

Required:

```text
dQ mismatch = 0
dK mismatch = 0
dV mismatch = 0
CPU/GPU nonfinite = 0
```

---

## 12. Directional finite-difference

The same synthetic BQHD fixture performs an independent directional derivative check on Q.

For deterministic nontrivial direction `v` selected from the final Q row, where multiple causal keys are visible:

```text
finiteDifference = [L(Q + εv) - L(Q - εv)] / (2ε)
analytic = <dQ, v>
```

Required:

```text
directionalPass = true
```

This seals both the live layout and the backward equation independently of GPU-vs-GPU reproducibility.

---

## 13. R13 SwiGLU stable derivative

The previous direct form:

```text
sigmoid(x) * [1 + x * (1 - sigmoid(x))]
```

is mathematically correct but uses `exp(-x)` directly.

R13-R1 uses a branch-stable sigmoid:

```text
x >= 0: 1 / (1 + exp(-x))
x < 0 : exp(x) / (1 + exp(x))
```

and the retained forward SiLU value:

```text
SiLU'(x) = sigmoid(x) + SiLU(x) * (1 - sigmoid(x))
```

No forward GateProj recomputation is introduced.

---

## 14. R13 explicit nonfinite status

R13 linear backward, SwiGLU backward, and FFN add/merge kernels gain explicit GPU nonfinite status buffers.

On a numerical fault:

```text
status += 1
output = explicit invalid/nonfinite value
```

Forbidden:

```text
output = 0 as recovery
clamp to finite
NaN replacement
```

The host reads only the compact status and hard-fails before returning the corresponding gradient surface.

---

## 15. R13 linear backward publication boundary

For each linear backward call, the status buffer spans:

```text
dX dispatch
all dW tile dispatches
```

The host checks the status after all queued work completes and before returning `R13LinearBackwardOutput`.

Required:

```text
nonFiniteCount = 0
compactStatusReadbackCount = 1
```

The dW payload itself remains GPU resident.

---

## 16. R13 dispatch limit receipt

R13-R1 records:

```text
dispatchWorkgroupLimit
maxDispatchWorkgroupsX
maxDispatchWorkgroupsY
originalFailingDispatchX = 90112
twoDimensionalGridLinearization = true
```

PASS requires both observed dimensions to be within the physical device limit.

---

## 17. Optimizer commit barrier future seal

No optimizer is active in R13-R1.

The patch therefore does not claim a physical optimizer commit gate.

It seals the future contract:

```text
any nonfinite / invalid / row-fault status
→ gradient publication rejected
→ future optimizer commit must be impossible
```

Current counters remain:

```text
optimizerCount = 0
optimizerStepCount = 0
weightMutationCount = 0
```

Future G205D/G206D optimizer adoption must bind commit admission to these fail-closed receipts rather than invent a parallel numerical policy.

---

## 18. CLI gates

All must be true:

```text
--require-bt-wgsl-r13-r1-dispatch-grid-limit-repair
--require-bt-wgsl-r13-r1-g204d-no-gradient-zeroing
--require-bt-wgsl-r13-r1-row-fault-whole-row-invalidation
--require-bt-wgsl-r13-r1-no-partial-rowdot-continuation
--require-bt-wgsl-r13-r1-dkdv-uniform-preflight-hoist
--require-bt-wgsl-r13-r1-zero-inner-loop-return
--require-bt-wgsl-r13-r1-swiglu-stable-derivative
--require-bt-wgsl-r13-r1-explicit-nonfinite-status
--require-bt-wgsl-r13-r1-no-nan-clamp
--require-bt-wgsl-r13-r1-no-gradient-clamp
--require-bt-wgsl-r13-r1-host-hard-fail-before-publication
--require-bt-wgsl-r13-r1-live-bqhd-cpu-f64-oracle
--require-bt-wgsl-r13-r1-live-bqhd-directional-finite-difference
--require-bt-wgsl-r13-r1-production-gradient-readback-zero
--require-bt-wgsl-r13-r1-future-optimizer-commit-barrier
```

---

## 19. Runtime receipts

R13-R1 adds:

```text
r13_r1_live_bqhd_cpu_f64_oracle_receipt.json
r13_r1_dispatch_grid_receipt.json
r13_r1_fail_closed_numerics_receipt.json
bt_wgsl_backprop_fail_closed_numerics_06c_r13_r1_final.json
```

The R13 receipts remain separately materialized and must pass in the same invocation before R13-R1 is sealed.

---

## 20. Physical target

```text
[bt-wgsl-backprop-fail-closed-numerics-06c-r13-r1]
r12_physical_parent=1
r13_same_invocation_closure=1

dispatch_limit=65535
max_dispatch_x<=65535
max_dispatch_y<=65535

g204d_gradient_zeroing=0
row_fault_whole_row=1
partial_rowdot_continuation=0
dkdv_inner_loop_return=0

swiglu_stable_derivative=1
explicit_nonfinite_status=1
host_fail_before_publication=1

live_bqhd_cpu_f64_oracle=1
directional_finite_difference=1
synthetic_oracle_gradient_readback=3
production_gradient_payload_readback=0

optimizer_commit_barrier_future=1
optimizer=0
weight_mutation=0
proof_ledger=HOLD
```

---

## 21. PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_BACKPROP_FAIL_CLOSED_NUMERICS_06C_R13_R1
R12_PHYSICAL_PARENT /
R13_SAME_INVOCATION_CLOSURE /
R13_DISPATCH_GRID_LIMIT_REPAIR /
G204D_NO_GRADIENT_ZEROING /
ROW_FAULT_WHOLE_ROW_INVALIDATION /
NO_PARTIAL_ROW_DOT_CONTINUATION /
DKDV_UNIFORM_PREFLIGHT_HOIST /
ZERO_INNER_LOOP_RETURN /
R13_SWIGLU_STABLE_DERIVATIVE /
R13_EXPLICIT_NONFINITE_STATUS /
NO_NAN_CLAMP /
NO_GRADIENT_CLAMP /
HOST_HARD_FAIL_BEFORE_PUBLICATION /
LIVE_BQHD_SYNTHETIC_CPU_F64_ORACLE /
LIVE_BQHD_DIRECTIONAL_FINITE_DIFFERENCE /
PRODUCTION_PAYLOAD_READBACK_ZERO /
FUTURE_OPTIMIZER_COMMIT_BARRIER /
PROOF_LEDGER_HOLD_SEALED
```

## One-line SSOT

> A nonfinite backward value is not repaired into a plausible gradient: the owning row/surface is invalidated, compact evidence is returned, host publication stops, and the same live-BQHD math is independently checked against CPU-f64 and finite difference while production payload readback remains zero.
