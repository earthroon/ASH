# ASH-P1B-OBS-R1B

# LOCKFILE IMMUTABILITY
# + WORKSPACE ROOT MANIFEST AUTHORITY
# + `--LOCKED` CARGO CHILD CONTRACT
# + PER-STAGE SOURCE IDENTITY FENCE
# + CHECK-PREDICATE PHYSICAL QUALIFICATION
# + CODEGEN-REQUIRED FALLBACK

## Revision

```text
Patch ID:
ASH-P1B-OBS-R1B-LOCKFILE-IMMUTABILITY-AND-CHECK-PREDICATE-QUALIFICATION

Short name:
P1B-OBS-R1B

Direct code parent:
ASH_PASS3_P1B_OBS_R1A_AUTHORITY_SURFACE_SOURCE_SEAL_CODE_ONLY.zip

Class:
OBSERVER EXECUTION AUTHORITY CLOSURE
LOCKFILE IMMUTABILITY
WORKSPACE ROOT MANIFEST IDENTITY
CARGO CHILD MUTATION RETIREMENT
CHECK PREDICATE PHYSICAL QUALIFICATION
CODEGEN-REQUIRED BOUNDED FALLBACK
RUST-ONLY
NO TRAINING SEMANTIC CHANGE
```

## 1. Parent physical evidence

OBS-R1A physically established source-surface admission and unrelated-drift tolerance, but the subsequent fast run ended as:

```text
obs-preflight=ReadyWithUnrelatedDrift
parent-seal-reuse=Admitted
check-canonical-baseline=CheckPass
check-bisect-control=CheckPass
check-current-production-coarse=CheckPass
check-demand-D001-D002=CheckPass
check-trainbackend-autodiffbackend=CheckPass
fast-candidate=Invalid
final-status=HoldSourceDrift
final-build-budget=3 used=0
```

This run is not valid evidence that canonical E0275 disappeared. The observer allowed Cargo execution while source identity could change, and the check predicate had never been physically qualified against a current-source canonical build.

## 2. Workspace root manifest becomes fail-closed authority

OBS-R1B adds workspace-root `Cargo.toml` to the required authority-surface manifest.

```text
Cargo.toml SHA-256:
db8e37f7fc2e02f380abbacb34d932387f8918fb98fd6e061575072c07a0c2f5

required-authority-files: 15
required-manifest-digest:
737f5857e343978bdd94f784c6160f82de8055eacbe366ab692f9c2e7ca074ad

canonical-authority-surface-digest:
ef95fff2c15a5e349b1671b5a6f928fa6359c3d668399a19d67157b361a5e53a
```

Any byte drift in root `Cargo.toml` or `Cargo.lock` yields `AuthoritySurfaceMismatch` before observer attribution. Whole-base_train forensic inventory remains 1,230 files and remains observation-only outside the explicit required authority surface.

## 3. Cargo lock immutability

Every base_train/dependency observation command materialized by `P1bR1a2ObservationPlan::args_for` contains exactly one `--locked`.

Check form:

```text
cargo check -p <package> --lib --release --locked --message-format=json
```

Build form:

```text
cargo build -p <package> --lib --release --locked -j 1 --message-format=json
```

`cargo metadata` is also explicitly materialized as:

```text
cargo metadata --format-version 1 --locked
```

The observer contains no `cargo update`, `cargo generate-lockfile`, source-side lock repair, or executable `cargo clean` path.

If Cargo reports that the lockfile would need to change under `--locked`, observation classifies the condition as `LockedResolutionMismatch` / `LOCKFILE_RESOLUTION_MISMATCH` and stops. The observer never regenerates the lockfile.

## 4. Per-stage source identity fence

New authority module:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1b_execution_authority.rs
```

Each stage snapshot binds:

```text
source_set_digest
workspace_manifest_sha256
cargo_lock_sha256
authority_surface_runtime_digest
observer_source_digest
```

Stages fenced in the R1B fast route include workspace metadata, both dependency seals, canonical check/build, admitted control/prefix probes, final build witnesses, and final workspace metadata.

Required invariant:

```text
before == after
```

for all identity dimensions. A failed fence stops before the next stage with `STAGE_SOURCE_IDENTITY_DRIFT`. The old suite-level source-before/source-after comparison remains defense in depth.

## 5. Check predicate physical qualification

The first current-source canonical pair is now always:

```text
canonical cargo check
→ canonical cargo build
```

under the same source, lockfile, workspace manifest, toolchain, environment, metadata and feature identity. The canonical build consumes build budget slot 1.

Predicate matrix:

```text
check SameE0275 + build SameE0275
    => Admitted

check CheckPass + build SameE0275
    => Insufficient / CodegenRequired

check CheckPass + build BuildPass
    => CanonicalReproducerLost

check DifferentE0275 + build SameE0275
    => CheckPredicateMismatch

any check + build DifferentE0275
    => CanonicalFingerprintChanged

check SameE0275 + build BuildPass
    => CheckBuildDivergence

structural/spawn/locked-resolution failure
    => QualificationInvalid
```

No R1A4 phase claim may be emitted from an unqualified check predicate.

## 6. Admitted check path

When canonical pair yields `SameE0275 / SameE0275`, R1B admits check-first reduction and executes the existing control spine plus adaptive prefix narrowing.

Final full-build witness policy remains:

```text
Build 1: canonical qualification
Build 2: last passing adjacent witness
Build 3: first failing adjacent witness
```

`MAX_BASE_TRAIN_FINAL_BUILDS = 3` remains hard authority.

## 7. Insufficient check path / codegen-required fallback

When:

```text
canonical check = CheckPass
canonical build = SameE0275
```

R1B does not interpret `CheckPass` as obligation clearance. It records `check-predicate=Insufficient`, enters `CodegenRequired`, executes no further check-prefix probes, and performs exactly one Q2 build.

```text
Q2 SameE0275 => interval=P0..P2
Q2 BuildPass => interval=P3..P5
```

A valid interval yields:

```text
codegen-status=Narrowed
final-status=CodegenRequiredNarrowed
```

The first codegen-required run therefore normally uses only two current-source base_train builds: canonical build plus Q2 build. It does not automatically launch a linear build sweep or historical slow observer. Exact continuation beyond the half-interval remains an explicit later action.

## 8. Dependency seal interaction

Existing dependency BuildPass cache remains under `target/p1b_obs_r1/cache/`. Build argv now contains `--locked`, so prior unlocked cache keys fail closed. Dependency stages are source-identity fenced.

## 9. Locked-resolution detection

`P1bR1a2ReleaseObservationReceipt` now records:

```text
locked_resolution_mismatch: bool
```

Fast classification adds `LockedResolutionMismatch`, keeping dependency-resolution refusal distinct from E0275, wrong target, invalid slice, or generic compiler failure.

## 10. Observer source identity

OBS-R1B adds its execution-authority module to the embedded observer source manifest.

```text
observer-source-files: 15
observer-static-source-digest:
053a0dd3a292d6263bfcbb6b84ccd7a3bace57f33bef65194bab3cd713bc5a36
```

Compiled-vs-disk observer digest equality remains mandatory.

## 11. Receipt changes

R1A4 suite schema advances to `P1B-R1A4-R1+R3D+OBS-R1B` and binds workspace manifest SHA, check predicate status, codegen status/interval, and all stage-fence evidence.

## 12. Actual source delta

Relative to OBS-R1A canonical full tree:

```text
ADD 1
MOD 7
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/src/obs_r1b_execution_authority.rs
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/fast_observer_r3d.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/metadata.rs
crates/ash_p1br1a2_release_observer/src/obs_r1.rs
crates/ash_p1br1a2_release_observer/src/obs_r1a_source_seal.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/training_body_r1a4_r1.rs
```

No `crates/base_train/**` source delta, no `Cargo.lock` semantic delta, no root `Cargo.toml` semantic delta, and no production training/runtime semantic delta.

```text
source-delta-digest:
027a31b761c03b0224ba3e362bc6a266392699898690388e40ea3635583819e9
```

## 13. Overlay authority reapply entries

The overlay contains 10 entries: 8 R1B code delta entries plus canonical root `Cargo.toml` and `Cargo.lock`. The latter two are authority-reapply entries, not semantic source delta. They restore a tree potentially mutated by the previous unlocked R1A run in the same extraction step.

The full applied ZIP preserves parent bytes and parent mtime for those two files because they are unchanged relative to the canonical parent.

## 14. ZIP freshness

```text
bake timestamp: 2026-09-08 19:52:50 Asia/Seoul
changed/new code entries: 8
changed/new at bake mtime: 8/8 PASS
unchanged parent entries: 8,438
unchanged parent mtimes preserved: 8,438/8,438 PASS
```

mtime is only a Cargo invalidation aid. Content SHA-256 remains semantic authority.

## 15. Static qualification actually executed

```text
source delta                                  ADD1 / MOD7 / DEL0
base_train source delta                       0
Cargo.lock semantic delta                     0
root Cargo.toml semantic delta                0
required authority files                     15
required authority hashes canonical          15 / 15 PASS
required manifest digest                     737f5857e343978bdd94f784c6160f82de8055eacbe366ab692f9c2e7ca074ad
canonical authority-surface digest           ef95fff2c15a5e349b1671b5a6f928fa6359c3d668399a19d67157b361a5e53a
whole-base_train forensic inventory           1,230 files
observer source manifest                      15 files
observer static source digest                 053a0dd3a292d6263bfcbb6b84ccd7a3bace57f33bef65194bab3cd713bc5a36
all observation action argv                   --locked PRESENT
cargo metadata argv                           --locked PRESENT
check action                                  -j 1 ABSENT
build action                                  -j 1 PRESENT
canonical check before canonical build        PASS
canonical build consumes budget               PASS
codegen insufficient path                     no further check probes
codegen first physical fallback               Q2 Build
max current-source base_train build budget    3
stage fence begin/end authority               PRESENT
observer executable cargo-clean action        0
new if-token count in changed observer files  0
Rust delimiter/static balance on changed files PASS
ZIP CRC                                       PASS
```

The bake container has no usable Cargo/rustc toolchain. Observer compilation/tests, base_train tests, physical canonical check/build qualification, `--locked` runtime behavior, stage-fence runtime behavior and final release seal were NOT RUN. No COMPILE PASS or RELEASE PASS is claimed.

## 16. Artifacts

```text
Overlay:
ASH_P1B_OBS_R1B_LOCKFILE_IMMUTABILITY_CHECK_PREDICATE_QUALIFICATION_OVERLAY_CODE_ONLY.zip
SHA-256:
2666005c8b875ced401cd533de98480d4fca90288eb1e6407163843cc305f29c
Entries: 10
CRC: PASS

Full applied:
ASH_PASS3_P1B_OBS_R1B_LOCKFILE_IMMUTABILITY_CHECK_PREDICATE_QUALIFICATION_CODE_ONLY.zip
SHA-256:
b8ac3bc4d6e20641554581837715e7d50e60f3092ccfd3ba4afa7ee820937bbc
Files: 8,446
CRC: PASS
```

Both artifacts contain zero generated `specs/`, `docs/`, `artifacts/`, `target/`, or `.ps1` paths.

## 17. User-side qualification

Apply the R1B overlay to repository root. Do not run workspace-wide clean.

```powershell
cargo build -p ash_p1br1a2_release_observer --release --locked
.\target\release\ash_p1br1a2_release_observer.exe obs-preflight
cargo test -p ash_p1br1a2_release_observer --release --locked
cargo test -p base_train --lib --locked
.\target\release\ash_p1br1a2_release_observer.exe current-training-body-obligation-fast
```

Admitted preflight states remain `ReadyExactTree` and `ReadyWithUnrelatedDrift`.

The decisive physical result is either `check-predicate=Admitted`, or `check-predicate=Insufficient` followed by `codegen-status=Narrowed` and `codegen-interval=P0..P2|P3..P5`. If canonical build is `BuildPass`, `DifferentE0275`, or structurally invalid, attribution stops.

## 18. Completion law

R1B closes operationally only after a physical run demonstrates root `Cargo.toml` exact, `Cargo.lock` exact, metadata and all observation children locked, stage identity stable, canonical check/build physical pairing completed, predicate explicitly admitted or insufficient, no unqualified CheckPass used as bisection evidence, codegen fallback using physical build evidence only, and no more than three current-source base_train builds in one run.

> P1B-OBS-R1B removes Cargo's authority to rewrite the experiment while the observer is measuring it. It binds the workspace manifest and lockfile, fences every Cargo stage, proves whether `cargo check` is a valid E0275 oracle with a current-source canonical build, and falls back to bounded physical codegen evidence when check is insufficient. The observer may write only under `target/`; it has no source or lockfile write authority.
