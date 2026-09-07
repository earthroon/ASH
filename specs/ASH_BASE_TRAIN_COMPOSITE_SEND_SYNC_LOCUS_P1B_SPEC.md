# ASH-BASE-TRAIN-COMPOSITE-SEND-SYNC-LOCUS-P1B

## BASE-TRAIN COMPOSITE SEND/SYNC LOCUS PROBE
## TRAINBACKEND → SESSION → MCU → RESIDENT GRAPH → SCHEDULER → FUTURE/CLOSURE
## EXACT FIRST-FAIL TYPE ISOLATION + RELEASE-ONLY OBLIGATION ATTRIBUTION + NO ARCHITECTURE CUT BEFORE LOCUS

### 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-COMPOSITE-SEND-SYNC-LOCUS-P1B

Class:
DIAGNOSTIC ONLY
COMPOSITE AUTO-TRAIT ISOLATION
RELEASE OBLIGATION ATTRIBUTION

Direct parent:
ASH_PASS3_BURN_WGPU_SOFT_PRIMITIVE_ABI_P1A_FUSION_RUNTIME_PROBE_COMPILEFIX_CODE_ONLY.zip

Parent SHA-256:
9b26f61ee7ddf96eade74fe6c6fa1262828c2347404b9caa65dc41c43e18ee22
```

P1A premise supplied by the user:

```text
Device probe                  PASS
Queue probe                   PASS
WgpuRuntime probe             PASS
CubeTensor probe              PASS
FusionTensor probe            PASS
Wgpu backend primitive probe  PASS
TrainBackend primitive probe  PASS
SoftPrimitive probe           PASS
```

Current parent release state remains:

```text
cargo build -p base_train --lib --release -j 1
    FAIL

E0275:
validation::NumericDimension: Sync
```

P1B does not repair that baseline error. P1B identifies the first composite or live-capture boundary that creates the recursive obligation.

---

# 1. Purpose

P1B moves upward from the primitive chain and probes actual `base_train` composite types.

Target:

```text
LAST CLEAR
FIRST FAIL
```

at one of:

```text
TrainBackend
NativeWgpuRuntimeHandles
TrainableSessionParkedRuntimeR4
TrainableSessionRuntimeR4
McuSessionRuntimeR7
McuSessionRuntimeR7B
ProductionMuonRuntime
MuonResidentStateGraph
actual scheduler live wrappers/captures
```

No architecture cut is permitted before this locus is identified.

---

# 2. No Architecture Cut Law

P1B does not modify:

```text
TrainBackend representation
P1A Soft Primitive production status
P1 Physical WGPU Runtime Context SSOT
Soft Matrix topology
A01/A02/A03 semantics
Fusion token semantics
Adam/HiMuon mathematics or storage
Atlas execution semantics
```

P1B adds only diagnostic Cargo features, actual-type assertions, scheduler live assertions, and a static validator.

Forbidden during P1B:

```text
recursion_limit increase
unsafe impl Send
unsafe impl Sync
Rc/Arc ownership rewrite
Mutex insertion
thread_local physical payload store
primitive ABI cutover
Device/Queue hiding
```

---

# 3. Actual Probe Module

Added:

```text
crates/base_train/src/composite_send_sync_locus_probe_p1b.rs
```

It uses actual production types, not mirrors.

Helpers:

```rust
pub fn assert_send_type<T: Send>() {}
pub fn assert_sync_type<T: Sync>() {}
pub fn assert_send_value<T: Send>(_: &T) {}
pub fn assert_sync_value<T: Sync>(_: &T) {}
```

Send and Sync are independent probes.

---

# 4. Exact Named Composite Probes

Materialized probe pairs:

```text
TrainBackend
    p1b-probe-train-backend-send
    p1b-probe-train-backend-sync

NativeWgpuRuntimeHandles
    p1b-probe-runtime-handles-send
    p1b-probe-runtime-handles-sync

TrainableSessionParkedRuntimeR4
    p1b-probe-parked-runtime-send
    p1b-probe-parked-runtime-sync

TrainableSessionRuntimeR4
    p1b-probe-session-r4-send
    p1b-probe-session-r4-sync

McuSessionRuntimeR7
    p1b-probe-mcu-r7-send
    p1b-probe-mcu-r7-sync

McuSessionRuntimeR7B
    p1b-probe-mcu-r7b-send
    p1b-probe-mcu-r7b-sync

ProductionMuonRuntime
    p1b-probe-production-muon-send
    p1b-probe-production-muon-sync

MuonResidentStateGraph
    p1b-probe-resident-graph-send
    p1b-probe-resident-graph-sync
```

All features are OFF by default.

---

# 5. Single-Probe Authority

The diagnostic module counts enabled P1B features at compile time.

More than one enabled probe rejects with:

```text
E_P1B_MULTIPLE_PROBES_FORBIDDEN
```

Authoritative runs therefore compile exactly one Send or Sync assertion at a time.

---

# 6. Scheduler Live Probes

P1B also instruments three actual values inside:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

### 6.1 Parked runtime live wrapper

Actual value:

```text
r4_parked_runtime
```

which is the real scheduler `Option<TrainableSessionParkedRuntimeR4>` result from `begin_invocation()`.

Features:

```text
p1b-probe-live-parked-option-send
p1b-probe-live-parked-option-sync
```

### 6.2 Native runtime handles live value

Actual value:

```text
native_handles
```

immediately after `try_extract_runtime_handles(device)`.

Features:

```text
p1b-probe-live-runtime-handles-send
p1b-probe-live-runtime-handles-sync
```

### 6.3 Production Muon live wrapper

Actual value:

```text
production_muon_runtime
```

immediately after restoration/take from the parked runtime.

Features:

```text
p1b-probe-live-production-muon-option-send
p1b-probe-live-production-muon-option-sync
```

These probes distinguish a naked type from its actual `Option<T>` scheduler wrapper.

---

# 7. Probe Classification

Because the baseline release build already fails, a whole build exit code is not sufficient.

Classification:

```text
PROBE_CLEAR
    no new P1B assertion-anchored Send/Sync error
    baseline E0275 may still appear elsewhere

PROBE_SEND_FAIL
    error is anchored to the active P1B Send assertion

PROBE_SYNC_FAIL
    error is anchored to the active P1B Sync assertion

PROBE_OTHER_FAIL
    probe injection produces another source-anchored compile error

UNCLASSIFIED
    compiler output cannot distinguish probe from baseline
```

A P1B FAIL must point to the P1B probe module or the explicitly instrumented scheduler line.

The WGPU internal long-type alone is not attribution.

---

# 8. Probe Order

Recommended authoritative order:

```text
C0 TrainBackend
C1 NativeWgpuRuntimeHandles
C2 TrainableSessionParkedRuntimeR4
C3 TrainableSessionRuntimeR4
C4 McuSessionRuntimeR7
C5 McuSessionRuntimeR7B
C6 ProductionMuonRuntime
C7 MuonResidentStateGraph
C8 live parked Option
C9 live runtime handles
C10 live production Muon Option
```

For every row:

```text
SEND first
SYNC second
```

Stop once the earliest reproducible first-fail boundary is sufficient for analysis.

---

# 9. Probe Commands

Baseline once:

```powershell
cargo build -p base_train --lib --release -j 1
```

Then one feature per run.

```powershell
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-train-backend-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-train-backend-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-runtime-handles-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-runtime-handles-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-parked-runtime-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-parked-runtime-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-session-r4-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-session-r4-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-mcu-r7-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-mcu-r7-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-mcu-r7b-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-mcu-r7b-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-production-muon-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-production-muon-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-resident-graph-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-resident-graph-sync
```

Live probes:

```powershell
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-parked-option-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-parked-option-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-runtime-handles-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-runtime-handles-sync

cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-production-muon-option-send
cargo build -p base_train --lib --release -j 1 --no-default-features --features p1b-probe-live-production-muon-option-sync
```

---

# 10. Future / Closure Escalation

P1B does not blindly rewrite async/closure code in the first bake.

If all named and current live probes are CLEAR while baseline E0275 remains, the next diagnostic substep is:

```text
actual production future value Send probe
actual spawn/callback closure Send probe
actual trait-object coercion probe
```

Only source sites reachable from current release library code are eligible.

`thread::spawn` closures are probed for Send unless the consumer explicitly requires Sync.

No architecture change is allowed during that escalation.

---

# 11. Module Bisection Fallback

If all type/live/future/closure probes remain CLEAR, perform diagnostic-only release module bisection.

Candidate coarse groups:

```text
core training/runtime
MCU / Adam / HiMuon
production Atlas
checkpoint / durability
historical GPU qualification
legacy compatibility
```

The goal is one module or impl surface whose inclusion reproduces E0275.

Modules are not deleted or semantically rewritten during bisection.

---

# 12. First-Fail Law

Valid evidence example:

```text
TrainBackend
    SEND CLEAR
    SYNC CLEAR

TrainableSessionParkedRuntimeR4
    SEND CLEAR
    SYNC CLEAR

McuSessionRuntimeR7
    SEND CLEAR
    SYNC FAIL
```

Conclusion:

```text
FIRST FAIL:
McuSessionRuntimeR7 : Sync
```

Only that exact boundary becomes eligible for the next surgery revision.

---

# 13. No Probe Mirror Types

P1B uses the actual types directly.

Forbidden authoritative evidence:

```text
FakeMcuRuntime
FakeSession
FakeResidentGraph
```

A mirror may not substitute for actual production type auto-trait behavior.

---

# 14. P1A Status

P1A Soft Primitive remains:

```text
VALID CANDIDATE
NOT PROMOTED
```

P1B does not modify or promote it.

If P1B identifies a composite or capture boundary unrelated to primitive payload, Soft Primitive cutover is not justified as an E0275 fix.

---

# 15. P1 Status

P1 Physical WGPU Runtime Context SSOT remains authoritative.

```text
actual WGPU bootstrap
→ physical runtime binding
→ R7 session
→ subgroup
```

P1B does not roll it back or create a competing Device/Queue identity system.

---

# 16. Static Acceptance Actually Executed

P1B focused validator:

```text
42 / 42 PASS
```

Existing regressions:

```text
P1A focused                    33 / 33 PASS
R7A                            83 / 83 PASS
R7                             55 / 55 PASS
R7B                            83 / 83 PASS
Burn/CubeCL/WGPU vendor       117 / 117 PASS
base_train storage root        39 / 39 PASS
```

R7A1:

```text
P1B parent: 81 / 82 FAIL
P1B bake:   81 / 82 FAIL
same failure: producer A01 tracked submit
```

Classification:

```text
PRE-EXISTING BASELINE FAILURE
NOT P1B REGRESSION
```

---

# 17. Toolchain Qualification

Bake environment:

```text
cargo unavailable
rustc unavailable
rustfmt unavailable
```

Therefore:

```text
Rust type checking     NOT RUN
borrow checking        NOT RUN
release codegen        NOT RUN
P1B trait probes       NOT RUN
native tests           NOT RUN
WGPU execution         NOT RUN
```

No compile PASS is claimed by this bake.

---

# 18. Actual Source Bake

```text
ADD 2
MOD 3
DEL 0
```

Added:

```text
crates/base_train/src/composite_send_sync_locus_probe_p1b.rs
tools/validate_ash_base_train_composite_send_sync_locus_p1b_static.py
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

No backend storage, WGPU runtime, MCU owner, Soft Matrix, Fusion, Adam or HiMuon implementation file is modified.

---

# 19. Artifacts

Overlay:

```text
ASH_BASE_TRAIN_COMPOSITE_SEND_SYNC_LOCUS_P1B_OVERLAY.zip
SHA-256: 0f77059108e6039302e0d080d55ae5c4120a2136c8c211ea6bfc48e518266d59
Bytes: 160,804
Files: 5
CRC: PASS
Duplicate paths: 0
```

Full code-only bake:

```text
ASH_PASS3_BASE_TRAIN_COMPOSITE_SEND_SYNC_LOCUS_P1B_CODE_ONLY.zip
SHA-256: dae2ea1e845c3df15a72042f9f0e9fda93539629f53285308c406e030c0bb5da
Bytes: 21,482,156
Files: 8,421
CRC: PASS
Duplicate paths: 0
```

Validation logs:

```text
ASH_BASE_TRAIN_COMPOSITE_SEND_SYNC_LOCUS_P1B_VALIDATION_LOGS.zip
SHA-256: ddc42878529be4f9981a38ef7d63def4750dfc3612be2716dca0e153b83e93a1
Bytes: 12,176
```

Code ZIPs contain no generated spec/artifact root and no PowerShell loader.

---

# 20. Promotion Seal

P1B may issue only:

```text
PASS_P1B_LOCUS_IDENTIFIED
```

when one exact first-fail boundary has been established by the user's release compiler.

P1B cannot issue:

```text
PASS_E0275_FIXED
```

because it intentionally performs no repair.

---

# 21. Completion Law

P1B completes when one of these is identified:

```text
FIRST FAIL composite type
FIRST FAIL live scheduler wrapper
FIRST FAIL future/closure/trait-object capture
single module/impl reproducer
```

Otherwise:

```text
HOLD_P1B_LOCUS_UNRESOLVED
```

---

# 22. After P1B

The next revision is not another broad architecture roadmap.

It takes exactly the identified boundary.

Example:

```text
FIRST FAIL:
McuSessionRuntimeR7 : Sync
```

Then only `McuSessionRuntimeR7` fields and the first failing contained field/wrapper are analyzed.

Example:

```text
FIRST FAIL:
scheduler closure line N : Send
```

Then only that closure's exact capture set is analyzed.

---

# 23. Final Law

> P1A cleared the isolated primitive chain. P1B therefore probes actual base_train composites and live wrappers instead of cutting more WGPU ownership by guesswork.
>
> Send and Sync are independent evidence.
>
> The baseline release failure may remain in every probe build; authoritative P1B failure must be source-anchored to the active assertion or later isolated module.
>
> No architecture is changed before FIRST FAIL is known.
>
> Once FIRST FAIL is found, probing stops and only that exact boundary becomes eligible for surgery.
