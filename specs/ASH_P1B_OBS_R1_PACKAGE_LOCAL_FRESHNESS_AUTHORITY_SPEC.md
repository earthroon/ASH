# ASH-P1B-OBS-R1-PACKAGE-LOCAL-FRESHNESS-AUTHORITY

## PACKAGE-LOCAL FRESHNESS AUTHORITY
## + ZIP BAKE MTIME NORMALIZATION
## + GLOBAL CARGO CLEAN RETIREMENT
## + OBSERVER EXECUTABLE SOURCE-DIGEST SELF-CHECK
## + BASE_TRAIN PACKAGE-LOCAL INVALIDATION
## + CHECK-FIRST ADAPTIVE SWEEP
## + MINIMAL FINAL BUILD WITNESS

### Revision

```text
Patch ID:
ASH-P1B-OBS-R1-PACKAGE-LOCAL-FRESHNESS-AUTHORITY

Short name:
P1B-OBS-R1

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A4_R1_R3D_FAST_OBSERVER_TRAINING_BODY_PHASE_BISECTION_CODE_ONLY.zip

Class:
OBSERVER INFRASTRUCTURE CLOSURE
PACKAGE-LOCAL FRESHNESS
STALE-BINARY FAIL-FAST
DEPENDENCY SEAL REUSE
CHECK-FIRST ATTRIBUTION
MAX-3 BASE_TRAIN FINAL BUILD AUTHORITY
RUST-ONLY
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

Parent R3 release evidence remains `TrainingLoopGenericObligationBeyondBaseTraits`, suite digest `0d68023dd8b3a25d888428b62bff438b6d91fd851b529b9459599102e3858f77`.

### Problem closed

The prior workflow could degrade into ZIP apply, stale observer executable, package or workspace clean, dependency reconstruction, then repeated release builds. A single diagnostic iteration was reported at roughly 110 minutes. OBS-R1 treats that as an infrastructure defect.

Normal P1B authority therefore retires workspace-wide `cargo clean` and bounds current-source `base_train` full release builds.

### Actual source delta

```text
ADD 1
MOD 3
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
```

`crates/base_train/**`, `Cargo.lock`, production training source, Burn/CubeCL/WGPU vendor source are unchanged. Overlay source-delta digest: `6a4f6c3a95fea244fec1320bac40988540c66cc9e041a17f3739369bec42ba84`.

### Observer executable source-digest self-check

OBS-R1 embeds all 13 current observer Rust source files with `include_str!`. Runtime computes `compiled_observer_source_digest` from that compiled snapshot and independently computes `disk_observer_source_digest` from the active workspace.

Before any observation Cargo child:

```text
compiled == disk -> fresh
compiled != disk -> STALE_OBSERVER_EXECUTABLE
```

Static observer-source digest for this bake: `ab20f7e6088a197055f5a0bfdd177ee94005c9eb8e580e11e022841a2d2c39dd`.

### Base-train exact source seal

OBS-R1 hashes `crates/base_train/Cargo.toml` plus `crates/base_train/src/**/*.rs` in deterministic path order. Expected digest for this bake:

```text
3084d43586d7312464c4eec0d1fa68aecbe489e57ffa16b409b482df82ac67a4
```

Mismatch yields `SOURCE_TREE_MISMATCH` before observation begins.

### Preflight CLI

Added:

```text
obs-preflight
```

Expected fresh result:

```text
[P1B-OBS-R1][PRECHECK]
observer-fresh=true
base-train-exact=true
verdict=Ready
```

### Global clean retirement

Observer execution source contains no executable `cargo clean` path. Normal workflow contains no bare `cargo clean`. Manual exceptional recovery may use package-local clean for the observer, or later `base_train` only when package-local evidence requires it. Such clean operations are outside receipt authority.

### ZIP delta-only mtime authority

Overlay ZIP entries that are changed or new receive the current bake timestamp.

Full applied ZIP rules:

```text
changed/new -> bake timestamp
byte-identical parent file -> preserve parent ZIP mtime
```

Actual bake metadata qualification:

```text
bake timestamp: 2026-09-08 16:01:30 Asia/Seoul
changed entries: 4
changed entries at bake mtime: PASS
unchanged entries: 8,440
unchanged parent mtimes preserved: PASS
```

mtime is only a Cargo invalidation hint. SHA-256 remains semantic authority. Iterative application should prefer the overlay ZIP. No touch/mtime repair script is shipped.

### Dependency BuildPass seal cache

Dependency seal cache moves to:

```text
target/p1b_obs_r1/cache/
```

for `burn-wgpu-local` and `burn_webgpu_backend`. Cache key binds plan and full Build argv/feature identity, package source digest, Cargo.lock digest, Cargo/rustc digests, environment digest and required metadata projection digest. Only final `BuildPass` populates a reusable seal. Any mismatch executes a fresh dependency build.

### Check-first authority

Fast search remains:

```text
cargo check --release
```

with `CheckPass` distinct from `BuildPass`. Check mode uses Cargo JSON and no `-j 1`. Canonical `SameE0275` semantics remain unchanged.

### Final build budget

OBS-R1 materializes:

```text
MAX_BASE_TRAIN_FINAL_BUILDS = 3
```

A fourth current-source `base_train` final build is rejected before spawn.

Normal failing-phase seal:

```text
Build 1 CanonicalBaseline -> SameE0275
Build 2 last passing prefix -> BuildPass
Build 3 first failing prefix -> SameE0275
```

P0 and TrainingCoreBodyCleared branches require only two current-source final builds.

### Parent seal reuse

OBS-R1 changes observer infrastructure only. Production semantic delta certificate is all-false for production body, runtime route, default features, vendor and lockfile changes. Previously promoted coarse CurrentProduction and D001+D002 BuildPass results remain lineage seals. The current fast suite still rechecks coarse and pair with `cargo check`, but does not full-build them again. Current-source canonical E0275 is always full-built once.

### R1A4 fast-seal change

The prior fast suite full-built canonical, bisect, coarse, pair and witnesses. OBS-R1 fast mode full-builds only canonical plus adjacent prefix witnesses. Check/build parity remains mandatory for all plans observed in both tiers.

Receipt schema advances to `P1B-R1A4-R1+R3D+OBS-R1` and records freshness, parent-seal reuse, final-build budget and final-build usage.

### Fail-fast law

Stale observer or base_train source mismatch stops before expensive observation. `InvalidSlice`, `WrongTarget`, structural compiler failure or `DifferentE0275` stops ordinary fast reduction. Fast mode never silently launches the slow reference suite.

### Static qualification actually executed

```text
source delta                                  ADD1 / MOD3 / DEL0
base_train source delta                       0
Cargo.lock delta                              0
observer source manifest files                13
observer static source digest                 ab20f7e6088a197055f5a0bfdd177ee94005c9eb8e580e11e022841a2d2c39dd
expected base_train source digest             3084d43586d7312464c4eec0d1fa68aecbe489e57ffa16b409b482df82ac67a4
obs-preflight dispatch                        PRESENT
fast CLI dispatch                             PRESENT
dependency cache path                         target/p1b_obs_r1/cache
base_train final build budget                 3
final full control set                        canonical only
observer executable cargo-clean action        0
Check builder -j1                             ABSENT
Build builder -j1                             PRESENT
changed ZIP entries mtime normalized          PASS
unchanged full-ZIP mtimes preserved           PASS
Rust delimiter balance on changed files       PASS
```

Bake environment has no usable Cargo/rustc, therefore observer/base_train tests, runtime preflight, fast sweep and final release seal were NOT RUN. No COMPILE or RELEASE PASS is claimed by this bake.

### Bake artifacts

Overlay:

```text
ASH_P1B_OBS_R1_PACKAGE_LOCAL_FRESHNESS_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256: cf8584a91c953357b042c770dc63bae22d2a4a2d3f965ac62f9c3cd583b70da1
Files: 4
CRC: PASS
```

Full applied:

```text
ASH_PASS3_P1B_OBS_R1_PACKAGE_LOCAL_FRESHNESS_AUTHORITY_CODE_ONLY.zip
SHA-256: 7354e21f82a56d323bab3800ce58967fbe820da76fecf5971dac172630f4dbf0
Files: 8,444
CRC: PASS
```

Both contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths.

### User-side qualification

Apply the overlay. Do not run a workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
```

Required preflight: `observer-fresh=true`, `base-train-exact=true`, `verdict=Ready`.

Then:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
cargo test -p base_train --lib
.\target\release\ash_p1br1a2_release_observer.exe current-training-body-obligation-fast
```

Only when an observer rebuild still fails freshness may the user run package-local observer clean and rebuild. No official OBS-R1 sequence contains bare `cargo clean`.

### Completion law

OBS-R1 closes operationally only after a machine run demonstrates preflight Ready, no global clean, exact dependency seal reuse or exact one-time dependency rebuild, adaptive check sweep, at most three current-source base_train full builds, check/build parity and one final R1A4 phase status.

> P1B-OBS-R1 treats 110-minute observer loops as an infrastructure failure. It preserves Cargo's target tree, makes changed archive entries fresh without rewriting unchanged full-tree mtimes, rejects stale executables before compilation, reuses exact dependency seals, and limits fast authoritative mode to three current-source base_train full release builds. The goal is not to make rustc magically faster. It is to stop asking rustc to repeat work already sealed.