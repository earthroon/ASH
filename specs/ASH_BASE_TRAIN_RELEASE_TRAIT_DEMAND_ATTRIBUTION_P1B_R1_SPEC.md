# ASH-BASE-TRAIN-RELEASE-TRAIT-DEMAND-ATTRIBUTION-P1B-R1

## BASE-TRAIN RELEASE TRAIT-DEMAND SOURCE ATTRIBUTION
## + MODULE / IMPL BISECTION
## + FUTURE / CLOSURE CAPTURE DEMAND PROBE
## + EXACT E0275 REPRODUCER ISOLATION

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-RELEASE-TRAIT-DEMAND-ATTRIBUTION-P1B-R1

Class:
RELEASE-ONLY TRAIT-DEMAND ATTRIBUTION
MODULE / IMPL BISECTION
FUTURE / CLOSURE CAPTURE ISOLATION
DIAGNOSTIC ONLY

Direct parent:
ASH_PASS3_BASE_TRAIN_COMPOSITE_SEND_SYNC_LOCUS_P1B_CODE_ONLY.zip

Parent SHA-256:
dae2ea1e845c3df15a72042f9f0e9fda93539629f53285308c406e030c0bb5da
```

P1B structural evidence supplied by the user:

```text
McuSessionRuntimeR7
    Send = FAIL
    Sync = FAIL

McuSessionRuntimeR7B
    Send = FAIL
    Sync = FAIL

ProductionMuonRuntime
    Sync = FAIL
```

The first direct structural cause is:

```text
McuSessionRuntimeR7
    -> McuDeviceSoftSubgroupHandleR1A
    -> Rc<RefCell<McuDeviceSoftSubgroupInnerR1A>>
```

R7B also has an independent non-Sync path through:

```text
PendingAdamWActiveDeviceCandidateR1
    -> std::sync::mpsc::Receiver<...>
```

These are type properties. They are not yet evidence that the natural release build demands Send/Sync from R7/R7B.

---

# 1. Purpose

P1B-R1 changes the diagnostic question from:

```text
which type is !Send / !Sync?
```

to:

```text
which exact release source site asks rustc for the recursive trait proof?
```

Target:

```text
module family
-> module
-> impl/function/static
-> future/closure/trait-object boundary
-> exact Send or Sync demand
-> concrete instantiated type
```

No ownership/runtime architecture is changed before that demand site exists as evidence.

---

# 2. R7 Non-Send/Sync Seal

P1B-R1 records:

```text
McuSessionRuntimeR7 !Send / !Sync
    EXPECTED PROCESS-LOCAL AUTHORITY PROPERTY
```

The existing subgroup remains:

```rust
Rc<RefCell<McuDeviceSoftSubgroupInnerR1A>>
```

P1B-R1 does not change it to `Arc<Mutex<_>>`.

Likewise P1B-R1 adds no:

```text
unsafe impl Send
unsafe impl Sync
#![recursion_limit = ...]
```

The demand site must be proven before any such architecture question is reconsidered.

---

# 3. Baseline Fingerprint

Canonical baseline command:

```powershell
cargo build -p base_train --lib --release -j 1
```

The baseline fingerprint is:

```text
error[E0275]
validation::NumericDimension: Sync
ShaderModule
RenderPipeline
BindGroupLayout
PendingWrites
```

Materialized classifier states:

```text
SameE0275
E0275Absent
DifferentE0275
InvalidSlice
Unclassified
```

A different E0275 is not silently classified as the same reproducer.

---

# 4. Baseline Stability Gate

Before using the bisection cuts, reproduce the parent baseline twice without P1B/P1B-R1 probe features.

Required:

```text
run A = SAME_E0275
run B = SAME_E0275
```

If the baseline itself is unstable:

```text
HOLD_NONDETERMINISTIC_BASELINE
```

No bisection result is promotable.

---

# 5. P1B Artificial Assertion Retirement

P1B's Send/Sync assertion features remain in source but must be OFF during P1B-R1 bisection.

Do not combine:

```text
p1b-probe-*
```

with:

```text
p1br1-bisect-*
```

for authoritative release attribution.

P1B-R1 is looking for the compiler's natural release demand.

---

# 6. Diagnostic Authority Module

Added:

```text
crates/base_train/src/release_trait_demand_attribution_p1b_r1.rs
```

It materializes:

```text
baseline fingerprint classifier
explicit demand-kind enum
explicit attribution-state enum
module-group enum
bisection slice manifest
source-set SHA-256 identity
fail-closed attribution receipt
future Send assertion helper
capture Send assertion helper
capture Sync assertion helper
```

This module contains no physical WGPU payload and changes no production runtime ownership.

---

# 7. Demand Categories

Materialized:

```text
GenericTraitBound
StaticGlobalStorageBoundary
ThreadSpawnCapture
FutureSendBoundary
TraitObjectSend
TraitObjectSync
TraitObjectSendSync
ArcMutexRwLockOnceLockComposition
CallbackFnTraitBound
BackendAssociatedTypeInstantiation
OtherExactSourceObligation
```

The final attribution receipt must use one exact category or remain unpromoted.

---

# 8. Attribution States

Materialized:

```text
Unknown
BaselineConfirmed
ModuleFamilyIsolated
ModuleIsolated
ImplIsolated
FutureCaptureIsolated
ClosureCaptureIsolated
StaticDemandIsolated
TraitObjectDemandIsolated
ExactReproducerConfirmed
InvalidSlice
```

No boolean-only promotion state is used.

---

# 9. Fail-Closed Attribution Receipt

Materialized:

```rust
P1bR1TraitDemandAttributionReceipt
```

Promotion validation rejects when any of the following are missing:

```text
ExactReproducerConfirmed state
module path
source line
Send or Sync trait identity
concrete type
enabled -> SAME_E0275 evidence
disabled -> E0275_ABSENT evidence
dependency-closed slice evidence
```

Therefore a statement such as:

```text
probably module X
```

cannot become promotion authority.

---

# 10. Source-Set Identity

Each diagnostic slice can be identified using SHA-256 over:

```text
parent revision
+ bisection feature
+ sorted module member paths
```

Timestamps are not identity.

Materialized helper:

```rust
source_set_digest(...)
```

---

# 11. First Physical Bisection Family

The first materialized coarse family is:

```text
GpuPhysicalQualificationDiagnostics
```

This family contains the current library declarations for:

```text
atlas_group_streaming_weight_train_runtime_audit
ash_basetrain_gpu_00...
...
ash_basetrain_gpu_70m...
runtime_binding_registry
```

The compatibility audit module and runtime binding registry are included where required by their dependent GPU qualification chain.

This is a release compilation diagnostic family. It does not claim these modules are production runtime authorities.

---

# 12. Why This Family Is First

The source contains many historical/qualification GPU modules with actual WGPU shader/pipeline/device operations.

`cargo build -p base_train --lib --release` compiles library modules even when a particular physical campaign does not invoke them at runtime.

Therefore the first coarse experiment is:

```text
Does removing the dependency-closed GPU qualification family remove the baseline E0275?
```

No assumption is made before the compile result.

---

# 13. Materialized Bisection Features

All are default OFF.

```text
p1br1-release-bisect

p1br1-bisect-cut-gpu-all
p1br1-bisect-cut-gpu-late48
p1br1-bisect-cut-gpu-tail62
p1br1-bisect-cut-gpu-tail70
p1br1-bisect-cut-gpu-mid21
p1br1-bisect-cut-gpu-mid04
```

The cut features depend on `p1br1-release-bisect` only as diagnostic admission metadata.

---

# 14. Cut Semantics

A `cut` feature excludes only the corresponding `pub mod` declarations from the diagnostic release build.

Source files are not deleted.

When every cut feature is OFF:

```text
parent module graph is preserved
```

Therefore normal production semantics remain unchanged by default.

---

# 15. GPU ALL Cut

```text
p1br1-bisect-cut-gpu-all
```

Cuts the complete first GPU qualification family.

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-all
```

Interpretation:

```text
SAME_E0275
    -> this whole family is not sufficient to explain baseline

E0275_ABSENT
    -> reproducer is inside this family or one of its exact compile relations

INVALID_SLICE
    -> do not infer anything from disappearance
```

---

# 16. GPU LATE48 Suffix Cut

```text
p1br1-bisect-cut-gpu-late48
```

Cuts:

```text
GPU-48 through GPU-70M
+ runtime_binding_registry
```

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-late48
```

If `gpu-all` removed E0275:

```text
late48 also removes E0275
    -> search remains in 48..70M

late48 keeps SAME_E0275
    -> search moves to 00..37I
```

---

# 17. GPU TAIL62 Suffix Cut

```text
p1br1-bisect-cut-gpu-tail62
```

Cuts:

```text
runtime_binding_registry
GPU-62A through GPU-70M
```

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-tail62
```

Use only after evidence keeps the search in the late48 family.

---

# 18. GPU TAIL70 Suffix Cut

```text
p1br1-bisect-cut-gpu-tail70
```

Cuts:

```text
GPU-70B through GPU-70M
```

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-tail70
```

This narrows a late tail result without changing earlier GPU qualification modules.

---

# 19. GPU MID21 Cut

```text
p1br1-bisect-cut-gpu-mid21
```

Cuts the independent chain:

```text
GPU-21
GPU-21-0
GPU-25
GPU-26
GPU-37H
GPU-37I
```

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-mid21
```

This is intended for the branch where `gpu-all` removes E0275 but `late48` does not.

---

# 20. GPU MID04 Cut

```text
p1br1-bisect-cut-gpu-mid04
```

Cuts:

```text
GPU-03R1
GPU-04...
through GPU-12
```

`GPU-03R1` is included because its source directly references the GPU-05B repair-plan module. Without 03R1 the slice is not dependency closed.

Command:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-mid04
```

---

# 21. Dependency-Closure Evidence

Static source analysis in this bake checks direct module-path references from compiled `base_train` library modules.

Results:

```text
p1br1-bisect-cut-gpu-all     direct module-path violations = 0
p1br1-bisect-cut-gpu-late48  direct module-path violations = 0
p1br1-bisect-cut-gpu-tail62  direct module-path violations = 0
p1br1-bisect-cut-gpu-tail70  direct module-path violations = 0
p1br1-bisect-cut-gpu-mid21   direct module-path violations = 0
p1br1-bisect-cut-gpu-mid04   direct module-path violations = 0
```

This is source-level evidence only.

The authoritative closure test remains Rust compilation.

Any unresolved import/type/module caused by a cut is classified:

```text
INVALID_SLICE
```

and is not evidence that E0275 disappeared.

---

# 22. No Stub Substitution

P1B-R1 creates no:

```text
FakeRuntime
FakeWgpuDevice
fake module replacement
stub backend implementation
```

A cut either compiles with genuine remaining source or is invalid.

---

# 23. Future / Closure Escalation

P1B-R1 materializes helpers:

```rust
assert_future_send(...)
assert_capture_send(...)
assert_capture_sync(...)
```

They are not injected broadly in this first bake.

Rule:

```text
first isolate one module or narrow module cluster
then instrument only actual future/closure/trait-object sites inside it
```

This avoids turning the entire crate into another combinatorial probe surface.

---

# 24. Future Demand Law

For an isolated actual future:

```rust
let future = actual_async_call(...);
assert_future_send(&future);
```

is valid only when the real consumer requires `Future + Send`.

The probe must identify values alive across `.await` and the first non-Send capture.

A process-local future is not made Send merely for diagnostic convenience.

---

# 25. Closure Demand Law

For an isolated actual spawn/callback closure, preserve the real capture environment and probe the exact consumer contract.

For `thread::spawn`:

```text
Send is relevant
Sync is not added unless the consumer requires it
```

No stronger artificial trait is imposed.

---

# 26. Static / Global Boundary Priority

After a module is isolated, inspect first for:

```text
static
OnceLock<T>
LazyLock<T>
Mutex<T>
RwLock<T>
Arc<dyn ... + Send + Sync>
```

because these can impose Sync even when the underlying runtime is intentionally process-local.

If such a demand is confirmed, the later repair targets the demand/ownership boundary before making the entire runtime Sync.

---

# 27. Associated-Type / Generic Demand

The final exact reproducer must record both:

```text
abstract obligation
concrete instantiation
```

Example form:

```text
B::Something: Sync
B = ConcreteBackend
B::Something = ConcreteWgpuRelatedType
```

The WGPU long-type alone is insufficient attribution.

---

# 28. Release Authority

`cargo check` may help with syntax/borrow feedback but cannot close P1B-R1.

Authoritative evidence is:

```powershell
cargo build -p base_train --lib --release -j 1
```

with the exact diagnostic cut feature under test.

---

# 29. Exact Reproducer Law

P1B-R1 promotion ultimately requires:

```text
site/module ON
    -> SAME_E0275

site/module OFF
    -> E0275_ABSENT
```

with a dependency-closed slice.

The final receipt additionally requires:

```text
exact module path
exact source line
exact Send or Sync demand
exact concrete type
```

Only then:

```text
PASS_P1B_R1_EXACT_DEMAND_LOCUS
```

---

# 30. Stop Law

Once an exact ON/OFF reproducer exists, stop bisection.

Do not continue neighboring module probes for completeness.

The next revision becomes a local repair of that exact boundary.

---

# 31. Static Acceptance Actually Executed

```text
P1B-R1 focused       32 / 32 PASS
P1B                  42 / 42 PASS
P1A                  33 / 33 PASS
R7A                  83 / 83 PASS
R7                   55 / 55 PASS
R7B                  83 / 83 PASS
vendor/storage      117 / 117 PASS
storage root         39 / 39 PASS
```

R7A1 remains:

```text
81 / 82 FAIL
producer A01 tracked submit
```

The same failure existed in the parent.

Classification:

```text
PRE-EXISTING BASELINE FAILURE
NOT P1B-R1 REGRESSION
```

---

# 32. Toolchain Qualification

Bake environment:

```text
cargo unavailable
rustc unavailable
rustfmt unavailable
```

Therefore:

```text
Rust type check      NOT RUN
borrow check         NOT RUN
release codegen      NOT RUN
bisection builds     NOT RUN
native tests         NOT RUN
WGPU execution       NOT RUN
```

No release PASS is claimed by this bake.

---

# 33. Actual Source Bake

```text
ADD 2
MOD 2
DEL 0
```

Added:

```text
crates/base_train/src/release_trait_demand_attribution_p1b_r1.rs
tools/validate_ash_base_train_release_trait_demand_p1b_r1_static.py
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
```

Not modified:

```text
McuSessionRuntimeR7
McuSessionRuntimeR7B
McuDeviceSoftSubgroupHandleR1A
ProductionMuonRuntime
TrainBackend
P1 Soft Primitive candidate
physical WGPU runtime ownership
```

---

# 34. Artifacts

Overlay:

```text
ASH_BASE_TRAIN_RELEASE_TRAIT_DEMAND_ATTRIBUTION_P1B_R1_OVERLAY.zip
SHA-256: f422d8430d492ffc4250d847e7e15ffc9aa4f025d26c9822d43be1e219ee7b2d
Files: 4
Bytes: 17,877
CRC: PASS
Duplicate paths: 0
```

Full code-only bake:

```text
ASH_PASS3_BASE_TRAIN_RELEASE_TRAIT_DEMAND_ATTRIBUTION_P1B_R1_CODE_ONLY.zip
SHA-256: 21070abba47094501236a29caee0f619ae8e8367040444396a843f7b74c86728
Files: 8,423
Bytes: 21,917,512
CRC: PASS
Duplicate paths: 0
```

Validation logs:

```text
ASH_BASE_TRAIN_RELEASE_TRAIT_DEMAND_ATTRIBUTION_P1B_R1_VALIDATION_LOGS.zip
SHA-256: 079035e7ed5821c0d65aecd79c66f36376d772c547e8c7a3065a99d9025a2c33
Files: 21
Bytes: 14,475
```

Code ZIPs contain:

```text
PowerShell files: 0
generated specs root: 0
generated artifacts root: 0
generated reports root: 0
```

---

# 35. First Run Sequence

Run the normal baseline twice first.

Then run only:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1-bisect-cut-gpu-all
```

Do not run every cut immediately.

Branch by evidence:

```text
gpu-all SAME_E0275
    -> stop GPU-family bisection
    -> next diagnostic bake targets another module family

gpu-all E0275_ABSENT
    -> run late48
```

Then continue only down the side supported by the previous result.

---

# 36. Final Law

> P1B proved that R7 is naturally process-local and non-Send/non-Sync. P1B-R1 does not repair that property.
>
> The object of investigation is the source that demands the trait, not the type that fails the artificial assertion.
>
> Release source is bisected with default-off dependency-aware module cuts. A cut that breaks source dependencies is INVALID and cannot support attribution.
>
> Future, closure, static and trait-object probes are activated only after a module or narrow cluster is isolated.
>
> No recursion-limit increase, unsafe Send/Sync implementation, synthetic stub or speculative WGPU ownership rewrite is accepted.
>
> The revision closes only when an exact source boundary satisfies ON = SAME_E0275 and OFF = E0275_ABSENT with the concrete Send/Sync demand identified.
