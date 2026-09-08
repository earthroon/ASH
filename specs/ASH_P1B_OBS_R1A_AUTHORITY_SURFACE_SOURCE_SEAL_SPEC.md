# ASH-P1B-OBS-R1A-AUTHORITY-SURFACE-SOURCE-SEAL

## AUTHORITY-SURFACE SOURCE SEAL
## + WHOLE-TREE DIGEST OBSERVATION-ONLY
## + REQUIRED FILE PER-PATH HASH MANIFEST
## + ADDED / MISSING / CHANGED SOURCE DIFF REPORT
## + UNRELATED LOCAL DRIFT TOLERANCE

### Revision

```text
Patch ID:
ASH-P1B-OBS-R1A-AUTHORITY-SURFACE-SOURCE-SEAL

Short name:
P1B-OBS-R1A

Direct code parent:
ASH_PASS3_P1B_OBS_R1_PACKAGE_LOCAL_FRESHNESS_AUTHORITY_CODE_ONLY.zip

Class:
OBSERVER SOURCE-IDENTITY REFINEMENT
AUTHORITY-SURFACE FAIL-CLOSED SEAL
WHOLE-TREE FORENSIC OBSERVATION
LOCAL-DRIFT TOLERANCE
RUST-ONLY
NO PRODUCTION RUNTIME SEMANTIC CHANGE
```

## 1. Parent authority preserved

OBS-R1 remains authoritative for executable source-digest self-check, delta-only ZIP mtime freshness, global `cargo clean` retirement, dependency BuildPass seal reuse, check-first adaptive sweep and `MAX_BASE_TRAIN_FINAL_BUILDS = 3`.

R1A changes only `base_train` source admission and mismatch reporting.

## 2. Whole-tree exact admission retirement

Whole `crates/base_train/src/**/*.rs` byte identity is no longer a blocking condition. Source identity is split into:

```text
LAYER A  authority surface
  explicit path + explicit SHA-256
  fail-closed

LAYER B  whole tree
  full path/hash inventory
  observation-only when drift is outside Layer A
```

Whole-tree digest and diff identity remain sealed into receipts.

## 3. Required authority manifest

New Rust authority:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
```

Required exact files: 14.

```text
Cargo.lock
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/training.rs
crates/base_train/src/config.rs
crates/base_train/src/dataset.rs
crates/base_train/src/hybrid.rs
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
crates/base_train/src/release_trait_demand_attribution_p1b_r1.rs
crates/base_train/src/current_production_demand_edge_ledger_p1b_r1a3_r1.rs
crates/base_train/src/current_production_demand_pair_p1b_r1a3_r2.rs
crates/base_train/src/current_trainbackend_obligation_decomposition_p1b_r1a3_r3.rs
crates/base_train/src/training_loop_body_obligation_bisection_p1b_r1a4_r1.rs
```

`config.rs`, `dataset.rs`, and `hybrid.rs` are included because the R1A4 witness directly instantiates their actual config, batch and hybrid-model composition surfaces.

```text
required-manifest-digest:
d5bf2b644dd25b0a5c7e721154a60496883ee66947807b9d6770b56265e2b861

canonical-exact-authority-surface-digest:
644cc0f108fac1c4827b2bf8f29a68684a23ab33b1962d2ccca999131fde24a8
```

Each required path is classified `Exact`, `Missing`, or `Changed`. Any required `Missing/Changed` yields `AuthoritySurfaceMismatch` before observation Cargo spawn.

## 4. Cross-platform path identity

Path identity is normalized workspace-relative UTF-8 path using `/` separators plus raw file-byte SHA-256. Normalize paths before sorting. Raw OS `PathBuf` ordering is not semantic authority. CRLF/LF bytes are not normalized.

## 5. Whole-tree forensic inventory

Sealed inventory covers:

```text
crates/base_train/Cargo.toml
crates/base_train/src/**/*.rs
```

Count: 1,230 files.

```text
sealed-whole-tree-digest:
7a2fbf47321553dfaa44b8c1457d4823b995cc6deda0058e7423c13c387d2214

canonical-empty-diff-digest:
b9a9b640161d1e8f8bf0b2907b5b79632006e1b1040d186dbc1cfee50da478a2
```

Disk differences are recorded as `Added`, `Missing`, or `Changed`, including normalized path, expected hash, actual hash, and `authority_file` flag. Full diff remains in receipt; console output is capped at 50 paths per category.

## 6. Admission and drift tolerance

```text
observer fresh + authority exact + whole tree exact
  -> ReadyExactTree

observer fresh + authority exact + whole tree drift
  -> ReadyWithUnrelatedDrift

observer stale
  -> StaleObserverExecutable

authority path missing/changed
  -> AuthoritySurfaceMismatch
```

An unrelated file is tolerable only when it is outside the authority manifest while exact `Cargo.toml`, `lib.rs`, and `Cargo.lock` continue to bind package/module/dependency identity. No required authority path can be downgraded to unrelated drift.

`SourceTreeMismatch` is retired from the active OBS-R1A base-train preflight path.

## 7. Path-level mismatch report

`obs-preflight` reports:

```text
authority-missing
authority-changed
unrelated-missing
unrelated-changed
unrelated-added
```

Changed required files print expected and actual SHA-256. The observer no longer returns only opaque whole-tree aggregate hashes.

`AuthoritySurfaceMismatch` recommends restoring the reported required path and rerunning preflight. It does not recommend workspace-wide clean. `ReadyWithUnrelatedDrift` requires no source restoration.

## 8. Observer executable self-check

`obs_r1a_source_seal.rs` is added to the embedded observer source manifest.

```text
observer-source-manifest-files: 14
observer-static-source-digest:
c1df4131bbc82aa03dc783f1082b7300035d7c12ab0f4deca71ed3ebeb756ae9
```

Runtime still requires compiled observer source digest to equal disk observer source digest before attribution.

## 9. Fast-suite integration

`obs-preflight` and `current-training-body-obligation-fast` use R1A preflight. Both `ReadyExactTree` and `ReadyWithUnrelatedDrift` are admitted. `StaleObserverExecutable` and `AuthoritySurfaceMismatch` stop before Cargo observation.

R1A4 receipt schema advances to:

```text
P1B-R1A4-R1+R3D+OBS-R1A
```

Suite digest additionally binds authority-surface digest, disk whole-tree digest and whole-tree-diff digest. Different unrelated local trees therefore remain forensically distinct even when they yield the same attribution result.

Check-first adaptive narrowing, dependency seal reuse and the max-three current-source final build budget remain unchanged.

## 10. Actual source delta

Relative to OBS-R1:

```text
ADD 1
MOD 3
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
crates/ash_p1br1a2_release_observer/src/main.rs
```

No `base_train` source delta, no Cargo.lock delta, no production runtime delta.

```text
source-delta-digest:
24bbc450155b418476453dffc45baaad32d86322a275fa9b88aa715c0a268cea
```

## 11. Static qualification actually executed

```text
source delta                                  ADD1 / MOD3 / DEL0
base_train source delta                       0
Cargo.lock delta                              0
required authority files                     14
canonical required hashes                    14 / 14 PASS
whole-tree sealed inventory                   1,230
canonical whole-tree match                    1,230 / 1,230 PASS
unrelated-added simulation                    ReadyWithUnrelatedDrift PASS
authority-change simulation                   AuthoritySurfaceMismatch PASS
observer source manifest                      14 files
new Rust if-token count                       0
Rust delimiter/static syntax balance          PASS
ZIP CRC                                       PASS
```

Bake environment has no usable Cargo/rustc. Observer compile/tests, base_train tests, runtime preflight, fast sweep and release seal were NOT RUN. No COMPILE or RELEASE PASS is claimed.

## 12. ZIP freshness and artifacts

OBS-R1 delta-only mtime law is preserved.

```text
bake timestamp: 2026-09-08 16:46:14 Asia/Seoul
changed/new entries at bake mtime: 4
unchanged parent entries: 8,441
unchanged parent mtimes preserved: PASS
```

Overlay:

```text
ASH_P1B_OBS_R1A_AUTHORITY_SURFACE_SOURCE_SEAL_OVERLAY_CODE_ONLY.zip
SHA-256:
0aa2ee1b08e5daa1b2cdaacfbde1882d8cdb9bc2b1ecc907bd8ddd830b87bf36
Files: 4
CRC: PASS
```

Full:

```text
ASH_PASS3_P1B_OBS_R1A_AUTHORITY_SURFACE_SOURCE_SEAL_CODE_ONLY.zip
SHA-256:
cae34b298326b2f4713032cb1e47810f90e9b112ae71ade466cafedaf70658f9
Files: 8,445
CRC: PASS
```

Both exclude generated `specs/`, `docs/`, `artifacts/`, `target/`, and `.ps1` paths.

## 13. User-side qualification

Apply the R1A overlay over the existing OBS-R1/R1A4 tree. Do not run workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
```

Admitted preflight verdicts:

```text
ReadyExactTree
ReadyWithUnrelatedDrift
```

If `AuthoritySurfaceMismatch` occurs, restore only the concrete required paths printed by preflight, then rerun preflight.

After admission:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
cargo test -p base_train --lib
.\target\release\ash_p1br1a2_release_observer.exe current-training-body-obligation-fast
```

## 14. Final law

> OBS-R1A stops requiring every local `base_train` byte to equal the canonical bake. It remains fail-closed for the exact files capable of changing the P1B experiment, reports every other drift by path, preserves unrelated local work, and keeps the OBS-R1 latency protections intact.
