# ASH-BASE-TRAIN-P1B-R1A3-CURRENT-PRODUCTION-INTERNAL-CLASSIFICATION

## CURRENT PRODUCTION INTERNAL CLASSIFICATION
## + SHAREDCORE MATERIALIZATION
## + MCU DEPENDENCY-CLOSED SUBCUT
## + MUON DEPENDENCY-CLOSED SUBCUT
## + SCHEDULER / SESSION-OWNER DEPENDENCY-CLOSED SUBCUT
## + R1A2-R1B PAIRED RELEASE AUTHORITY INHERITANCE

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A3-CURRENT-PRODUCTION-INTERNAL-CLASSIFICATION

Short name:
P1B-R1A3

Class:
CURRENT-PRODUCTION INTERNAL RELEASE BISECTION
SUBFAMILY CLASSIFICATION
SHAREDCORE MATERIALIZATION
DEPENDENCY-CLOSED SUBCUT AUTHORITY
RUST-ONLY DIAGNOSTIC INFRASTRUCTURE
NO PRODUCTION RUNTIME SEMANTIC CHANGE

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1B_CARGO_JSON_DIAGNOSTIC_CHANNEL_AUTHORITY_CODE_ONLY.zip
```

---

# 1. Parent promoted evidence

R1A3 is admitted only because the parent R1A2-R1B machine suite produced:

```text
parent suite digest:
0b625a2d429b61f338ac5885018dcf965a2d22f6328f8a80df16ff0c2a2ee78c

burn-wgpu-local          = BuildPass
burn_webgpu_backend      = BuildPass
canonical-baseline       = SameE0275
bisect-control           = SameE0275
current-production-cut   = BuildPass
paired-status            = CurrentProductionClosureRequired
```

Therefore the CurrentProduction composition is a justified internal search surface.

R1A3 does not claim that R7, Muon, scheduler, a future, a static, or any exact Send/Sync consumer is already isolated.

---

# 2. Parent search universe

The parent Rust authority contains:

```text
P1BR1A_CURRENT_PRODUCTION_CLOSURE
    136 modules
```

R1A3 classifies exactly these 136 members.

Every first-round subcut member is required to belong to this parent universe.

---

# 3. Muon candidate boundary correction

The requested semantic Muon candidates were:

```text
tensorcube_local_muon_production_callsite_adoption
unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1
mcu_himuon_packed_gradient_r7a1
production_muon_commit_runtime_r8
```

Static source inspection shows the final two are not members of the 136-member parent CurrentProduction closure.

R1A3 therefore materializes:

```text
P1BR1A3_CURRENT_MUON_ROOT_CANDIDATES
    4 candidates

P1BR1A3_CURRENT_MUON_SEEDS
    2 active parent-contained seeds

P1BR1A3_CURRENT_MUON_DEFERRED_OUTSIDE_PARENT
    mcu_himuon_packed_gradient_r7a1
    production_muon_commit_runtime_r8
```

R1A3 does not silently enlarge the parent search universe to include them.

---

# 4. Primary classification

Materialized in:

```text
crates/base_train/src/current_production_internal_classification_p1b_r1a3.rs
```

Primary classes:

```text
Mcu
Muon
SchedulerSessionOwner
SharedCore
CurrentPeripheralSupport
```

Actual 136-member classification counts:

```text
Mcu                      5
Muon                    12
SchedulerSessionOwner   41
SharedCore               9
CurrentPeripheralSupport 69
TOTAL                   136
```

Every parent member has exactly one primary class.

---

# 5. Classification evidence law

Semantic seeds are explicitly fixed by R1A3.

Non-seed provider classification uses source-visible family-root dependency evidence.

A retained provider used by two or more semantic families may become `SharedCore`.

Modules without sufficient single-family or shared-provider evidence remain `CurrentPeripheralSupport` rather than being guessed into a family from naming alone.

This is SOURCE/STATIC classification evidence only.

---

# 6. SharedCore law

R1A3 materializes:

```text
P1BR1A3_SHARED_CORE
    9 modules
```

Every SharedCore member is retained by all three first-round subcuts.

SharedCore is provider-side shared authority, not a synonym for high fan-out, a large module, or a top-level orchestrator.

---

# 7. Static edge authority

R1A3 commits an explicit Rust edge table:

```text
P1BR1A3_STATIC_DEPENDENCY_EDGES
    214 edges
```

The static edge model is:

```text
DIRECT_MODULE_PATH
+
P1BR1A1_EXPLICIT_ROOT_SYMBOL_EDGES
```

Cross-family semantic edges materialized:

```text
44
```

Static fixed point is not promoted above Rust release compilation.

---

# 8. MCU subcut

Active MCU seeds:

```text
mcu_session_runtime_r7
mcu_session_runtime_r7b
mcu_device_resource_runtime_r7a
```

Feature:

```text
p1br1a3-cut-current-mcu
```

Static reverse-closure candidate:

```text
32 modules
```

Cross-family carried consumers:

```text
14 modules
```

Static purity:

```text
Mixed
```

Therefore an MCU subcut `BuildPass` alone may promote only:

```text
McuSeedClosureRequired
```

not exact MCU-family isolation.

---

# 9. Muon subcut

Active parent-contained Muon seeds:

```text
tensorcube_local_muon_production_callsite_adoption
unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1
```

Feature:

```text
p1br1a3-cut-current-muon
```

Static reverse-closure candidate:

```text
26 modules
```

Cross-family carried consumers:

```text
11 modules
```

Static purity:

```text
Mixed
```

A Muon `BuildPass` alone may promote only:

```text
MuonSeedClosureRequired
```

under the current manifest.

---

# 10. Scheduler / Session-Owner subcut

Seeds:

```text
production_multistep_loop_accumulation8_scheduler
trainable_session_active_production_owner_r4
```

Feature:

```text
p1br1a3-cut-current-scheduler-session
```

Static reverse-closure candidate:

```text
19 modules
```

Cross-family carried consumers:

```text
0
```

Static purity:

```text
Pure
```

If the paired suite yields only this treatment as `BuildPass` while MCU/Muon remain `SameE0275`, R1A3 may derive:

```text
ExactSchedulerSessionFamilyIsolated
```

This still does not identify the exact natural Send/Sync demand site.

---

# 11. Cargo features

Added to `crates/base_train/Cargo.toml`:

```text
p1br1a3-cut-current-mcu
    -> p1br1a-release-bisect

p1br1a3-cut-current-muon
    -> p1br1a-release-bisect

p1br1a3-cut-current-scheduler-session
    -> p1br1a-release-bisect
```

All are default OFF.

No production feature or default-member behavior is changed.

---

# 12. lib.rs cut gates

Every member of each Rust subcut manifest is gated at both applicable surfaces:

```text
pub mod <module>
pub use <module> ...
```

The R1A3 gate is added as an additional `cfg` condition and therefore composes with the existing R1A / Atlas gates.

Normal feature-OFF production graph remains unchanged.

---

# 13. Gate / manifest equality

Source/static bake verification:

```text
MCU manifest modules       = 32
MCU actual cfg modules     = 32
match                      = true

Muon manifest modules      = 26
Muon actual cfg modules    = 26
match                      = true

Scheduler manifest modules = 19
Scheduler actual cfg modules = 19
match                      = true
```

All discovered root re-export surfaces for these modules carry the same corresponding R1A3 gate.

---

# 14. Static reverse-closure result

Against the 214 committed known static dependency edges:

```text
MCU violations       = 0
Muon violations      = 0
Scheduler violations = 0
```

This is SOURCE/STATIC evidence only.

A cut-induced E0432/E0433/E0412/E0425 or other structural Rust error in user release compilation remains `InvalidSlice` and outranks any E0275 disappearance.

---

# 15. Subcut purity authority

Materialized:

```text
P1BR1A3_CURRENT_MCU_PURITY
    Mixed

P1BR1A3_CURRENT_MUON_PURITY
    Mixed

P1BR1A3_CURRENT_SCHEDULER_SESSION_PURITY
    Pure
```

Purity is bound to the exact classification source digest.

Observer authority digest:

```text
8cde6f25fd569ebc2bd455a1ab3b1f7b23b77269347184036ec7af6ce1068b3c
```

A classification source drift invalidates the internal suite.

---

# 16. Observer plan extension

Existing R1A2 observer gains typed plans:

```text
CurrentProductionCoarseCut
CurrentMcuCut
CurrentMuonCut
CurrentSchedulerSessionCut
```

Each authoritative subcut plan enables exactly one feature.

No arbitrary feature vector is accepted.

All plans preserve:

```text
--message-format=json
```

from R1A2-R1B.

---

# 17. R1A3 observer command

New CLI:

```text
current-production-internal
```

It runs an eight-stage same-source suite:

```text
1 burn-wgpu-local
2 burn_webgpu_backend
3 canonical-baseline
4 bisect-control
5 current-production-coarse
6 current-mcu
7 current-muon
8 current-scheduler-session
```

Progress is non-authoritative stderr telemetry.

---

# 18. Coarse anchor law

R1A3 re-runs:

```text
p1br1a-cut-current-production
```

because R1A3 changes the source digest by adding diagnostic features and authority source.

Required before subcut interpretation:

```text
current-production-coarse = BuildPass
```

Otherwise:

```text
HoldCoarseAnchorDrift
```

---

# 19. Internal promotion states

Materialized observer states include:

```text
HoldDependencyBaselineDrift
HoldCanonicalBaselineDrift
HoldBisectControlDrift
HoldCoarseAnchorDrift
HoldSourceDrift
HoldToolchainDrift
HoldEnvironmentDrift
HoldMetadataIdentityDrift
HoldClassificationAuthorityDrift
HoldInvalidSubcut
HoldDifferentE0275

ExactMcuFamilyIsolated
ExactMuonFamilyIsolated
ExactSchedulerSessionFamilyIsolated

McuSeedClosureRequired
MuonSeedClosureRequired
SchedulerSessionSeedClosureRequired

MultipleSubcutsRemoveReproducer
SharedCoreOrCrossCompositionUnresolved
Unresolved
```

No exact Send/Sync demand-site state exists in R1A3.

---

# 20. Promotion matrix

If exactly one treatment is `BuildPass`:

```text
MCU BuildPass + Mixed
    -> McuSeedClosureRequired

Muon BuildPass + Mixed
    -> MuonSeedClosureRequired

Scheduler BuildPass + Pure
    -> ExactSchedulerSessionFamilyIsolated
```

If two or more treatments are `BuildPass`:

```text
MultipleSubcutsRemoveReproducer
```

If all three are `SameE0275` while coarse cut is `BuildPass`:

```text
SharedCoreOrCrossCompositionUnresolved
```

Any `DifferentE0275`:

```text
HoldDifferentE0275
```

Any invalid/wrong-target/other structural treatment result:

```text
HoldInvalidSubcut
```

---

# 21. Parent lineage binding

R1A3 source and internal receipt bind:

```text
P1BR1A3_PARENT_R1A2_SUITE_DIGEST
=
0b625a2d429b61f338ac5885018dcf965a2d22f6328f8a80df16ff0c2a2ee78c
```

The R1A3 source digest is expected to differ from the parent R1A2 source digest.

Within the new eight-stage suite the R1A3 source/toolchain/environment/metadata identities must remain stable.

---

# 22. Rust tests materialized

`base_train` diagnostic authority tests cover:

```text
136-member exact classification coverage
Muon outside-parent candidate deferral
SharedCore first-round retention
known static reverse-closure law
lib.rs gate / manifest equality
subcut purity / carried-consumer consistency
```

Observer tests cover:

```text
one feature per R1A3 typed plan
plain Cargo JSON message-format preservation
pure Scheduler PASS promotion
mixed MCU PASS non-exact promotion
multiple PASS non-resolution
all SAME shared/cross unresolved state
```

---

# 23. No external loader

R1A3 adds:

```text
Python loader     0
PowerShell loader 0
new .ps1 files    0
```

All new diagnostic authority is Rust source.

No external manifest file is required at runtime.

---

# 24. Production non-goals

R1A3 modifies no production implementation file for:

```text
MCU runtime behavior
Muon math
Adam / HiMuon state
WGPU Device/Queue authority
Soft Tensor Matrix
Atlas execution
checkpoint format
R3C / R3C1 commit semantics
```

No:

```text
unsafe impl Send
unsafe impl Sync
Arc<Mutex> conversion
recursion_limit increase
stub runtime
fake root symbol
```

is introduced.

---

# 25. Actual source delta

Relative to R1A2-R1B parent:

```text
ADD 2
MOD 4
DEL 0
```

Added:

```text
crates/base_train/src/current_production_internal_classification_p1b_r1a3.rs
crates/ash_p1br1a2_release_observer/src/internal_r1a3.rs
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

No Cargo.lock change and no new dependency.

---

# 26. Static qualification actually executed

```text
TOML parse                                     PASS
CurrentProduction classification 136/136      PASS
MCU gate/manifest 32/32                        PASS
Muon gate/manifest 26/26                      PASS
Scheduler gate/manifest 19/19                  PASS
R1A3 re-export gate alignment                  PASS
SharedCore retained by all first-round cuts    PASS
Muon deferred roots outside parent verified    PASS
classification digest binding                  PASS
known static-edge fixed point 214 edges        PASS
new Rust `if` token count in changed logic     0
brace balance checks                           PASS
```

These are SOURCE/STATIC checks only.

Bake environment has no usable Cargo/rustc, therefore:

```text
observer compile       NOT RUN
base_train compile     NOT RUN
subcut release builds  NOT RUN
8-stage suite          NOT RUN
```

No COMPILE or RELEASE PASS is claimed by this bake.

---

# 27. Bake artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A3_CURRENT_PRODUCTION_INTERNAL_CLASSIFICATION_OVERLAY_CODE_ONLY.zip
SHA-256:
5164d58fcf01fd6963b586d8edc2ca543fab8b67260ee7d6bc8b8b0d1a891b61
Files: 6
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A3_CURRENT_PRODUCTION_INTERNAL_CLASSIFICATION_CODE_ONLY.zip
SHA-256:
e8fa4603d7ff3fe1c8fcd24e2fa5c04f5b8b090ce6d0db0eb6c87e42a353886b
Files: 8,434
CRC: PASS
```

Both code ZIPs contain zero generated:

```text
specs/
docs/
artifacts/
target/
*.ps1
```

Specification is committed separately.

---

# 28. First user-side gates

Because stale release artifacts were previously observed in this workspace, a one-time full clean after applying this complete tree is the safest qualification start:

```powershell
cargo clean
```

Compile/test the observer:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
```

No internal family claim is admitted from observer unit tests alone.

---

# 29. Manual subcut supporting commands

MCU:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3-cut-current-mcu
```

Muon:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3-cut-current-muon
```

Scheduler / Session Owner:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a3-cut-current-scheduler-session
```

These are supporting compile observations. A cut-induced structural error is `InvalidSlice`.

---

# 30. Authoritative command

Run the complete same-source internal suite:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production-internal
```

Expected progress surface:

```text
[P1B-R1A3][1/8] burn-wgpu-local
[P1B-R1A3][2/8] burn_webgpu_backend
[P1B-R1A3][3/8] canonical-baseline
[P1B-R1A3][4/8] bisect-control
[P1B-R1A3][5/8] current-production-coarse
[P1B-R1A3][6/8] current-mcu
[P1B-R1A3][7/8] current-muon
[P1B-R1A3][8/8] current-scheduler-session
```

No treatment outcome is predeclared by this specification.

---

# 31. Completion law

R1A3 release authority closes only when the eight-stage observer records:

```text
dependency controls classified
canonical baseline = SameE0275
bisect control = SameE0275
coarse CurrentProduction = BuildPass
MCU treatment classified
Muon treatment classified
Scheduler/Session treatment classified
source/toolchain/environment/metadata stable
classification source digest stable
internal-status derived
```

---

# 32. Stop law

Once a valid internal state is derived, broad R1A3 bisection stops.

Examples:

```text
ExactSchedulerSessionFamilyIsolated
McuSeedClosureRequired
MuonSeedClosureRequired
MultipleSubcutsRemoveReproducer
SharedCoreOrCrossCompositionUnresolved
```

The next revision operates only on that proven surface.

---

# 33. Final law

> R1A3 begins from a machine-proven CurrentProduction coarse requirement and does not reopen WGPU dependency or historical GPU qualification search.
>
> Semantic family ownership and dependency-closed cut membership are separate authorities. A consumer carried for compilation does not silently change semantic ownership.
>
> SharedCore remains retained in the first-round cuts.
>
> MCU and Muon candidate cuts are currently mixed. Their BuildPass can establish required seed closures but not exact family guilt.
>
> Scheduler/Session is statically pure under the committed edge model and can reach exact family isolation only if the paired release matrix supports it.
>
> Static closure is not compile closure. Any new cut-induced Rust error invalidates that treatment and must be repaired before attribution.
>
> R1A3 changes no production ownership, optimizer mathematics, WGPU runtime authority, or Send/Sync implementation.
