# ASH-WGPU-BENCHMARK-PROMOTION-09

## Physical Benchmark Promotion / Same-Workload Comparative Evidence

### Status

- Patch ID: `ASH-WGPU-BENCHMARK-PROMOTION-09`
- Parent: `ASH-WGPU-ASYNC-SUBMISSION-RETIREMENT-08`
- Benchmark authority: production N8 execution path plus D09 capture/aggregate receipts
- Static performance claim: forbidden
- Physical promotion claim: allowed only from measured physical run receipts
- Current source-bake state: `STATIC_READY`
- No physical D09 permit is baked into the source tree
- D10 production publication requires a valid physical `BenchmarkPromotionPermit`

D09 does not create a benchmark-only optimizer fast path. It measures the production path and only adds observation, identity, aggregation, and promotion gates.

---

## 1. Authority chain

```text
A00 inventory
→ A01 submission lifetime
→ A02 usage-segregated arena
→ A03 staging / compact readback
→ B04 resident Muon state
→ B05 device candidate
→ B06 hybrid optimizer commit
→ C07 compact GPU evidence
→ C08 async submission retirement
→ D09 physical benchmark promotion
→ D10 SSOT publication
```

`STATIC_SOURCE_ONLY PASS` is not a physical benchmark result.

---

## 2. Benchmark lanes

D09 distinguishes four lanes:

```text
HISTORICAL_A00
REPRODUCED_A00
SAME_TREE_CONTROL
C08_CANDIDATE
```

`HISTORICAL_A00` is descriptive history only. It cannot mint a promotion permit because current device/build equivalence is not proven by a historical number.

`REPRODUCED_A00` is the A00 snapshot rerun under the current sealed benchmark identity and may serve as a full-series promotion baseline.

`SAME_TREE_CONTROL` is the current tree executed with the candidate optimization disabled or in the approved blocking/control mode. It is the preferred incremental C08 baseline.

`C08_CANDIDATE` is valid only when the physical Active path is actually admitted. Mirror execution cannot be relabeled as an Active candidate after the run.

---

## 3. Run phases

Every benchmark invocation is labeled:

```text
COLD
WARMUP
MEASURED
```

Only `MEASURED` samples may enter a promotion population. Cold and warmup runs remain diagnostic evidence but are rejected by the promotion sample validator.

---

## 4. Measured telemetry window

Process-global cumulative counters are not sufficient because bootstrap and qualification work would contaminate the warm measurement.

D09 writes a start snapshot immediately before the N8 training loop:

```text
d09_runtime_telemetry_start.json
```

and an end snapshot after the production run:

```text
d09_runtime_telemetry_snapshot.json
```

The measured telemetry is the monotonic counter delta:

```text
MeasuredTelemetry = End - Start
```

Any monotonic counter regression invalidates the sample. Peak retained arena bytes remain an observed absolute peak rather than a counter delta.

---

## 5. Semantic identity snapshot

Before the production Muon runtime is released, D09 writes:

```text
d09_semantic_identity_snapshot.json
```

The snapshot binds:

```text
registry digest
optimizer routing digest
profile digest
ordered fusion-plan sequence digest
B06 canonical layout digest
B06 ownership digest
B06 runtime mode
C07 runtime mode
C08 runtime mode
C07 kernel qualification state
C08 Active physical admission state
segmented device-successor capability
current model generation
current optimizer generation
total trainable elements
Muon-owned elements
AdamW-owned elements
```

The snapshot is self-hashed. Same pair counts are not treated as the same fusion plan; the ordered actual plan-digest sequence is bound.

---

## 6. Workload identity

`BenchmarkWorkloadIdentity` binds:

```text
workload name
input digest
batch-shape digest
parameter count
trainable element count
Muon-owned element count
AdamW-owned element count
optimizer steps per run
registry digest
optimizer-routing digest
fusion-plan sequence digest
```

and seals them into `workloadDigest`.

A benchmark orchestration layer must provide the actual input/batch identity. D09 does not invent missing workload identity.

---

## 7. Build and device identity

`BuildBenchmarkIdentity` binds:

```text
rustc version
Cargo profile
target triple
optimization level
debug assertions
feature digest
```

`DeviceBenchmarkIdentity` binds:

```text
adapter name
backend
vendor ID
device ID
driver
driver info
limits digest
features digest
```

Promotion populations must use compatible sealed identities. Debug and release runs are not mixed.

---

## 8. Run identity

`BenchmarkRunIdentity` binds:

```text
D09 schema
code revision
runtime-mode digest
workload digest
initial model-state digest
initial optimizer-state digest
device identity digest
build identity digest
```

Baseline and candidate promotion populations must start from the same model/optimizer state and workload identity.

---

## 9. Explicit correctness authority

D09 never infers correctness from speed.

Each measured sample requires an explicit, self-hashed `BenchmarkCorrectnessReceipt` containing:

```text
numerical parity passed
generation parity passed
evidence parity passed
lifetime parity passed
ownership parity passed
device error count
validation error count
early-reuse violation count
active-lease eviction count
```

All parity booleans must pass and all error/violation counts must be zero for a promotable sample.

A failed sample cannot be dropped merely to improve performance statistics.

---

## 10. Existing production evidence is reused

D09 capture consumes the existing production receipts rather than replacing them:

```text
n8_phase_wall_time_attribution_receipt.json
basetrain_tensorcube_local_muon_production_callsite_receipt.json
d09_runtime_telemetry_start.json
d09_runtime_telemetry_snapshot.json
d09_semantic_identity_snapshot.json
```

The D09 CLI combines these with the sealed run identity and explicit correctness receipt to produce one raw `BenchmarkRunReceipt`.

---

## 11. Timing and throughput

The raw receipt records at least:

```text
optimizer total wall time
optimizer-step p50
optimizer-step p95
hot-path optimizer wall time
hot-path optimizer step count
AdamW wall time
Muon wall time
final-durability wall time
training-loop wall time
end-to-end wall time
```

When non-final steps exist, `finalMaterialization=true` steps are excluded from the hot-path optimizer population. Step-8 durability remains separately visible.

Throughput is computed from the sealed workload identity:

```text
trainable elements / second
=
trainableElements × measuredHotSteps / hotPathOptimizerWallTime
```

D09 does not fabricate unavailable GPU timestamp measurements.

---

## 12. Transport metrics

D09 separates:

```text
H2D bytes
D2H bytes
candidate bulk D2H bytes
compact status D2H bytes
compact evidence D2H bytes
committed-state materialization D2H bytes
```

Candidate readback and durable committed-state materialization are never merged.

H2D uses measured-window A03 tracked control/bulk upload bytes. This is a runtime transfer authority, not a claim of exact PCIe bus traffic.

Total tracked D2H uses the A00 readback-copy authority. Candidate-specific D2H is also reconstructed from B05/B06/C07 candidate telemetry.

---

## 13. Allocation and reuse metrics

D09 reports:

```text
A00 allocation call count
vendor allocation count when observable
A02 arena acquire count
A02 reuse hit count
A02 new-page count
A02 requested bytes
A02 reserved bytes
A02 peak retained page bytes
unexpected measured-window allocations
```

A02 reserved/retained bytes are not described as exact physical driver VRAM usage.

---

## 14. Warm-state seal

`BenchmarkWarmStateSeal` records:

```text
resident graph generation valid
arena stable
unexpected measured-window allocation count
resident graph rebootstrap count
```

A measured sample is invalid if the resident graph reboots during the measured run. A conservative measured-window policy may also reject new arena pages because warm allocator stability was not established.

This prevents a first-use bootstrap run from being silently promoted as steady-state performance.

---

## 15. Async metrics

D09 exposes at least:

```text
tracked submission count
exact-wait count
hot-path blocking-wait count
Mirror blocking-wait count
nonblocking poll count
completion callback observed count
deferred retirement count
capacity-defer count
compact-ring backpressure count
```

Shutdown/reference waits remain distinct from hot-path waits.

---

## 16. C08 candidate physical admission

A sample labeled `C08_CANDIDATE` is valid only when its semantic snapshot proves all of:

```text
C08 mode = ActiveAsync
C08 activePhysicalAdmission = true
segmented device successor = true
C07 mode = ActiveCompact
B06 mode = ActiveVerified
```

The C08 parent currently carries `activePhysicalAdmission=false`. Therefore the current D09 source bake is intentionally `STATIC_READY`, not `PROMOTED`.

---

## 17. Statistics

D09 does not promote the fastest run.

The aggregate uses all required valid samples and reports median and tail behavior, including:

```text
optimizer-step p50
optimizer-step p95
median throughput
median H2D
median D2H
median candidate bulk D2H
median compact-evidence D2H
median new arena pages
median peak retained arena bytes
maximum hot-path wait count
median exact-wait count
```

Best-run-only promotion is forbidden.

---

## 18. Frozen promotion policy

`BenchmarkPromotionPolicy` is sealed before aggregation and contains:

```text
minimum throughput gain ratio
maximum p95 regression ratio
maximum memory regression ratio
require zero hot-path wait
require zero candidate bulk D2H
require zero correctness failures
minimum valid samples per lane
policy digest
```

Floating thresholds are bound by their exact bit representations. Changing a threshold changes the policy digest.

---

## 19. Population identity gate

Baseline and candidate populations must match on:

```text
workload digest
initial model-state digest
initial optimizer-state digest
device identity digest
required build identity digest
```

All samples inside a population must preserve the same identity class.

---

## 20. Promotion order

Correctness is evaluated before performance statistics.

After correctness passes, D09 evaluates:

```text
candidate throughput / baseline throughput
candidate p95 / baseline p95
candidate retained-arena peak / baseline retained-arena peak
```

against the frozen policy.

When requested by policy, the candidate must also satisfy:

```text
hot-path blocking wait max = 0
candidate bulk D2H median = 0
```

---

## 21. Historical baseline restriction

`HISTORICAL_A00` may appear in reports but is explicitly rejected from `BenchmarkPromotionPermit` generation.

A permit baseline must be `REPRODUCED_A00` or `SAME_TREE_CONTROL`.

---

## 22. Promotion states

```text
SPEC_ONLY
STATIC_READY
PHYSICAL_RUN_COMPLETE
REJECTED
PROMOTED
```

Source code and static validation alone may reach `STATIC_READY`, never `PROMOTED`.

---

## 23. Benchmark promotion permit

Only a passing physical aggregate may emit `BenchmarkPromotionPermit` containing:

```text
aggregate receipt hash
baseline class
baseline identity hash
candidate identity hash
workload digest
promotion-policy digest
valid sample count
throughput gain ratio
p50 ratio
p95 ratio
candidate H2D
candidate D2H
candidate bulk D2H
candidate hot-path wait count
unexpected allocation count
numerical parity status
generation parity status
lifetime parity status
evidence parity status
physical benchmark passed
permit hash
```

`physicalBenchmarkPassed=true` is set only inside the passing aggregate path. No baked constant or static gate may mint it.

---

## 24. CLI

The source bake provides:

```text
ash_wgpu_benchmark_promotion_09
```

with:

```text
capture
aggregate
seal-workload
seal-build
seal-device
seal-identity
seal-correctness
seal-policy
```

`capture` consumes an already completed production run and produces one raw sample receipt.

`aggregate` consumes sealed baseline samples, C08 candidate samples, and one frozen promotion policy. It produces an aggregate receipt and only on PASS may write a promotion permit.

The seal commands bind operator-provided identities/policies. They do not change optimizer semantics.

---

## 25. Benchmark labels are observation-only

Forbidden:

```text
benchmark mode skips validation
benchmark mode changes optimizer math
benchmark mode changes fusion plan
benchmark mode changes batch size silently
benchmark mode changes arena/ring policy silently
benchmark mode bypasses C07/B06/C08 gates
```

D09 environment labels only enable measurement snapshots and sample labeling.

---

## 26. Generated artifact split

Generated physical benchmark outputs such as raw sample receipts, aggregates, promotion permits, traces, CSV/JSONL, and D09 runtime snapshots do not belong in the normal code ZIP.

The code bake contains source/spec/validator only.

---

## 27. Static source gate

The D09 static validator verifies, among other things:

```text
D09 module/export/bin exists
start/end telemetry window is production-wired
semantic identity is captured before runtime release
A00/A01/A02/A03 telemetry authorities are consumed
existing N8 phase and Muon receipts are consumed
explicit correctness receipt is mandatory
Cold/Warmup cannot enter promotion population
median and p95 aggregation exist
best-run promotion is absent
Historical A00 cannot mint permit
C08 candidate requires physical Active admission
candidate bulk D2H and hot-path waits are policy gates
policy digest is frozen
benchmark labels do not alter optimizer semantics
B06 committed materialization is separate from candidate D2H
C07/C08 backend source and optimizer WGSL remain parent-identical
no generated physical benchmark result is baked
```

`STATIC_SOURCE_ONLY` does not prove throughput or GPU timing.

---

## 28. Failure classes

```text
FAIL_D09_BENCHMARK_LANE_UNKNOWN
FAIL_D09_RUN_PHASE_UNKNOWN
FAIL_D09_RUNTIME_WINDOW_IDENTITY
FAIL_D09_RUNTIME_COUNTER_REGRESSION
FAIL_D09_WORKLOAD_IDENTITY_MISMATCH
FAIL_D09_MODEL_STATE_MISMATCH
FAIL_D09_OPTIMIZER_STATE_MISMATCH
FAIL_D09_OWNERSHIP_MISMATCH
FAIL_D09_FUSION_PLAN_MISMATCH
FAIL_D09_DEVICE_IDENTITY_MISMATCH
FAIL_D09_BUILD_IDENTITY_MISMATCH
FAIL_D09_WARM_STATE_NOT_REACHED
FAIL_D09_WARM_REBOOTSTRAP
FAIL_D09_INVALID_SAMPLE
FAIL_D09_NUMERICAL_PARITY
FAIL_D09_GENERATION_PARITY
FAIL_D09_EVIDENCE_PARITY
FAIL_D09_EARLY_REUSE
FAIL_D09_ACTIVE_LEASE_EVICTION
FAIL_D09_BULK_CANDIDATE_D2H
FAIL_D09_HOT_PATH_BLOCKING_WAIT
FAIL_D09_POLICY_CHANGED_AFTER_RUN_START
FAIL_D09_INSUFFICIENT_VALID_SAMPLES
FAIL_D09_HISTORICAL_BASELINE_NOT_PROMOTABLE
FAIL_D09_ACTIVE_RUNTIME_NOT_PHYSICALLY_ADMITTED
FAIL_D09_PROMOTION_NOT_GRANTED
```

---

## 29. Physical promotion gate

A D09 promotion permit requires:

```text
physical measured candidate samples exist
C08 candidate Active runtime physically admitted
same workload identity
same starting model state
same starting optimizer state
same device identity
same required build identity
all requested samples valid
numerical parity PASS
generation parity PASS
evidence parity PASS
lifetime parity PASS
ownership parity PASS
early reuse = 0
active lease eviction = 0
throughput policy PASS
p95 policy PASS
memory policy PASS
candidate bulk D2H = 0 when required
hot-path waits = 0 when required
```

Any missing physical prerequisite leaves the result unpromoted.

---

## 30. D10 handoff

D10 may publish the A00→D09 optimization chain as canonical production SSOT only when supplied with a valid physical `BenchmarkPromotionPermit`.

A D09 source gate, console line, historical benchmark, or Mirror run is insufficient.

### Center declaration

> **A00 through C08 changed where buffers live, how optimizer state advances, how evidence is compacted, and how GPU completion is observed. D09 is not allowed to assume that those changes improved performance. It measures the exact production path, seals workload/build/device/state identities, separates bootstrap from the measured window, rejects correctness failures before calculating performance statistics, and promotes median plus tail behavior rather than the fastest run. Historical A00 remains history; only a reproduced or same-tree baseline under a valid current physical identity can mint a promotion permit. The current source bake contains no fabricated physical result and remains STATIC_READY until the Active C08 path is physically admitted and measured.**