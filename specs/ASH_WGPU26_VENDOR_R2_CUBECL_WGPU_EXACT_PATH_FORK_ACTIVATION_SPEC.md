# ASH-WGPU26-VENDOR-R2

# CUBECL-WGPU 0.9.0 EXACT PATH FORK ACTIVATION
# + ASH OVERLAY MERGE
# + ROOT PATCH-CRATES-IO CUTOVER
# + SINGLE WGPU26 PACKAGE GRAPH
# + RELEASE ABI SEAL

## 0. Revision

```text
Patch ID:
ASH-WGPU26-VENDOR-R2-CUBECL-WGPU-EXACT-PATH-FORK-ACTIVATION

Short name:
WGPU26-VENDOR-R2

Direct code parent:
ASH_PASS3_P1B_CLOSE_R1_DIAGNOSTIC_SCAFFOLD_RETIREMENT_CODE_ONLY.zip

Parent SHA-256:
0a950ddd6791d2c784574f723e4250b3b463c663a966e3fa54fce2e184be4130

Class:
VENDOR SOURCE AUTHORITY SEAL
CUBECL-WGPU PATH FORK SSOT
WGPU26 GRAPH UNIFICATION
RUST-ONLY QUALIFICATION
NO ALGORITHM CHANGE
```

## 1. Existing activation state

The parent already contains the effective root authority:

```toml
[patch.crates-io]
cubecl-wgpu = { path = "vendor_fork_scaffold/cubecl-wgpu-ash" }
```

and the parent `Cargo.lock` already represents exactly one `cubecl-wgpu 0.9.0` package without a registry source/checksum. Therefore R2 does not rewrite the root patch or lockfile merely to create artificial delta. R2 promotes the already-active path fork into a verifiable source/package-graph SSOT.

Static parent/current lock projection:

```text
cubecl-wgpu  0.9.0   count=1   registry-source=0
wgpu         26.0.1  count=1
wgpu-core    26.0.1  count=1
wgpu-types   26.0.0  count=1
wgpu-hal     26.0.6  count=1
```

## 2. Published upstream provenance

Canonical upstream package identity:

```text
crate: cubecl-wgpu
version: 0.9.0
published archive SHA-256:
29787364632fc7ec6a11cf3d95187f82f6fcce17d6bb4f0fb0dde580b837631d
```

The published package records:

```text
.cargo_vcs_info.json git sha1:
2679028d1c62b9f432e77a0acb952c06481dd7a9

path_in_vcs:
crates/cubecl-wgpu
```

The local fork carries the same provenance record.

## 3. Upstream source lineage verification

The provenance commit's `crates/cubecl-wgpu/src` tree and top-level source files were compared to the active local fork using Git blob identity.

```text
upstream source/provenance paths compared: 34
Git-blob exact local paths:               33
ASH-modified source paths:                 1
missing compared upstream paths:           0
```

The sole source implementation delta in this projection is:

```text
src/compute/storage.rs
```

The active fork's `Cargo.toml.orig` is Git-blob exact to the upstream manifest. The active normalized `Cargo.toml` is an ASH overlay that preserves package identity while routing WGPU through the ASH WGPU26 API/storage interop surfaces.

`README.md` was missing from the prior local fork and is restored from the provenance commit in this bake.

## 4. Published-package ancillary Cargo.lock boundary

The crates.io package listing contains 39 files including a crate-local published `Cargo.lock`. The active ASH path fork contains 38 files and intentionally does not synthesize that package-local lockfile.

```text
published package files: 39
active path fork files:  38
published crate-local Cargo.lock omitted: true
```

Reason:

```text
workspace root Cargo.lock
= active dependency-resolution SSOT

crate-local published Cargo.lock
= package ancillary provenance artifact
= not active resolution authority for this path dependency
```

No lockfile bytes are fabricated. The published archive checksum remains provenance evidence. This omission is explicit and fail-visible rather than silently represented as byte-for-byte archive completeness.

## 5. Active fork identity

Canonical source path:

```text
vendor_fork_scaffold/cubecl-wgpu-ash
```

Cargo package identity remains:

```text
name = cubecl-wgpu
version = 0.9.0
readme = README.md
```

Active fork deterministic source digest:

```text
9fbaa4d44005e15ca66e7075da42b8da577eade099a27257bbe577311b542c0d
```

ASH overlay digest over the active modified manifest + storage implementation:

```text
17201d2b923db347b63a803112c828832679c18ca50207a2502a726ed821cfad
```

Restored README SHA-256:

```text
9d5119350428c7e0de53c898c6d7d96f21958437f5b613252c1cdea63acf0242
```

## 6. Legacy activation scaffold retirement

Retired:

```text
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/activate_cubecl_wgpu_r2.py
```

The old Python activator is no longer an authority. Cargo manifests and Rust qualification are SSOT.

Also retired because it was not the 0.9.0 published seed and carried a later Stage7K-era storage implementation:

```text
vendor_fork_scaffold/upstream_real_insert/cubecl-wgpu/crates/cubecl-wgpu/src/compute/storage.rs
```

The retained overlay evidence is only:

```text
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/storage.rs
```

and its bytes must equal the merged active fork `src/compute/storage.rs`.

## 7. Rust-only qualification authority

New module:

```text
crates/ash_wgpu26_qualification/src/vendor_r2.rs
```

New CLI surfaces:

```text
vendor-r2-static
vendor-r2-seal
```

`vendor-r2-static` validates without Cargo execution:

```text
root patch count = 1
fork package name/version identity
Cargo.toml.orig upstream WGPU 26.0.0 identity
provenance git commit/path
README digest
fork source digest/file count
ASH overlay digest
storage overlay merge
legacy Python activator retirement
stale upstream fragment retirement
Cargo.lock cubecl-wgpu path-source uniqueness
single lock generation for wgpu/wgpu-core/wgpu-types/wgpu-hal
single active cubecl-wgpu Cargo.toml authority
```

`vendor-r2-seal` first performs the static seal, then invokes the existing Rust `cargo metadata --locked` graph qualifier and requires:

```text
cubecl-wgpu package count = 1
cubecl-wgpu version = 0.9.0
cubecl-wgpu registry count = 0
manifest_path ends in vendor_fork_scaffold/cubecl-wgpu-ash/Cargo.toml
wgpu package count = 1
wgpu version = 26.0.1
root patch active = true
no alternate Burn path fork activated
no upstream_real_insert path active
```

## 8. Backend provenance constants

`burn_webgpu_backend::cubecl_wgpu_vendor_fork_r2` now records:

```text
upstream published version
published archive checksum
upstream provenance Git SHA
root patch authority string
legacy Python activator retired = true
stale cubecl upstream fragment retired = true
published crate-local lock ancillary omitted = true
```

No runtime algorithm or device ownership behavior is changed by these constants.

## 9. Single WGPU26 package graph law

R2 promotion requires the active Cargo graph to contain one compatible WGPU26 lineage only.

Static lock authority for this bake:

```text
wgpu       26.0.1
wgpu-core  26.0.1
wgpu-types 26.0.0
wgpu-hal   26.0.6
```

Any second major generation blocks promotion.

## 10. Release ABI chain

Physical qualification order on the user machine:

```text
1. vendor-r2-static
2. vendor-r2-seal (cargo metadata --locked)
3. cargo tree duplicate/inverse source inspection
4. burn-wgpu-local release
5. burn_webgpu_backend release
6. canonical base_train release
```

The path fork is transitively compiled by the Burn/backend release chain. No standalone fork-local generated lockfile is required.

## 11. P1B closure regression

The P1B E0275 incident is already `FullClosureSealed` in the direct parent. WGPU26-VENDOR-R2 must preserve:

```text
cargo build -p base_train --lib --release --locked -j 1
= BuildPass
```

A reappearance of the old `NumericDimension: Sync` E0275 is a vendor-R2 regression and does not justify restoring retired P1B observer scaffolding.

## 12. Actual source delta

Relative to P1B-CLOSE-R1:

```text
ADD 2
MOD 4
DEL 2
```

Added:

```text
crates/ash_wgpu26_qualification/src/vendor_r2.rs
vendor_fork_scaffold/cubecl-wgpu-ash/README.md
```

Modified:

```text
crates/ash_wgpu26_qualification/src/lib.rs
crates/ash_wgpu26_qualification/src/main.rs
crates/burn_webgpu_backend/src/cubecl_wgpu_vendor_fork_r2.rs
vendor_fork_scaffold/cubecl-wgpu-ash/Cargo.toml
```

Deleted:

```text
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/activate_cubecl_wgpu_r2.py
vendor_fork_scaffold/upstream_real_insert/cubecl-wgpu/crates/cubecl-wgpu/src/compute/storage.rs
```

Source-delta digest:

```text
c4f4b14d0397d65145c08f51f8a75354a512a57f434a338ac80878d6a7d5322c
```

Root `Cargo.toml` delta: 0.
Root `Cargo.lock` delta: 0.

## 13. Changed file hashes

```text
crates/ash_wgpu26_qualification/src/vendor_r2.rs
3d5471e0a93a82c852fb56cc235cf71c48f6e678796fcbe7c7726473746f1ba5

crates/ash_wgpu26_qualification/src/lib.rs
7dcd5bccbed772e47c4a5e380910a83cf7c08520ca478022e55289ce18237f36

crates/ash_wgpu26_qualification/src/main.rs
06de24b58fc5ab29f0dc601f92a125936bea900ff008494ce0534f6f4b9ceaff

crates/burn_webgpu_backend/src/cubecl_wgpu_vendor_fork_r2.rs
8deb84f1ba2a60e12ba967d6867cb1e9ef4b05d199bbcd3edc599fcd2d423db0

vendor_fork_scaffold/cubecl-wgpu-ash/Cargo.toml
053777065b44d70d1d7f84e9453f3fe78d0c172896574f29d0c96734906c6ff5

vendor_fork_scaffold/cubecl-wgpu-ash/README.md
9d5119350428c7e0de53c898c6d7d96f21958437f5b613252c1cdea63acf0242
```

## 14. Static qualification actually executed

```text
root Cargo.toml parse                         PASS
ash_wgpu26_qualification Cargo.toml parse     PASS
cubecl-wgpu active Cargo.toml parse           PASS
root cubecl-wgpu patch count                  1
fork name/version                             cubecl-wgpu / 0.9.0
fork readme authority                         README.md
fork provenance commit                        2679028d... PASS
upstream Git source paths compared            34
upstream Git-blob exact                       33
ASH-modified Git source paths                 1 (storage.rs)
missing compared upstream source               0
active fork files                             38
published package files                       39
published package local lock omission         explicit
fork source digest                            PASS
ASH overlay digest                            PASS
storage overlay merge                         PASS
legacy Python activator                       RETIRED
stale post-0.9 cubecl storage fragment        RETIRED
lock cubecl-wgpu count                        1
lock cubecl-wgpu registry count               0
lock wgpu versions                            [26.0.1]
lock wgpu-core versions                       [26.0.1]
lock wgpu-types versions                      [26.0.0]
lock wgpu-hal versions                        [26.0.6]
active cubecl-wgpu Cargo.toml authority       1
new positive `if` tokens                      0
changed Rust lexical delimiter balance        PASS
ZIP CRC                                       PASS
```

Bake environment has no usable Cargo/rustc toolchain. Current-revision `cargo metadata`, Rust tests and release chain were NOT RUN. Historical logs establish that the same local path fork previously compiled as `cubecl-wgpu v0.9.0` with WGPU 26.0.1, but that historical result is not promoted as this revision's release ABI seal.

## 15. Bake artifacts

```text
Overlay review-only:
ASH_WGPU26_VENDOR_R2_CUBECL_WGPU_EXACT_PATH_FORK_ACTIVATION_OVERLAY_REVIEW_ONLY_CODE_ONLY.zip
SHA-256:
51d65d3efc4f45ca5a5d94dbc6e3bbf121fab8a3f2493c7b47469cb02b6a40f8
Files: 6
CRC: PASS

Full applied code-only:
ASH_PASS3_WGPU26_VENDOR_R2_CUBECL_WGPU_EXACT_PATH_FORK_ACTIVATION_CODE_ONLY.zip
SHA-256:
d3d721ce6fc018aef9fb9847ad11aecbf4fb035311c7d856cde83266dc1237c2
Files: 8,420
CRC: PASS

Deletion commands:
WGPU26_VENDOR_R2_GIT_RM_COMMANDS.txt
SHA-256:
cff00554f751de7f0277ec6795f35b0131275f095ae45742ce66d3984dab8946
```

ZIP freshness:

```text
bake timestamp: 2026-09-09 15:18:42 Asia/Seoul
changed/new entries at bake mtime: 6/6 PASS
unchanged surviving parent entries preserve parent mtime: 8,414/8,414 PASS
```

The overlay cannot apply deletions by extraction alone. For an existing working tree, apply the six changed/new files and the explicit two `git rm` commands. The full ZIP physically omits the retired files.

## 16. User-side physical qualification

```powershell
cargo run -p ash-wgpu26-qualification --release --locked -- `
  vendor-r2-static --workspace .
```

Required token:

```text
PASS_WGPU26_VENDOR_R2_STATIC_SOURCE_AUTHORITY
```

Then:

```powershell
cargo run -p ash-wgpu26-qualification --release --locked -- `
  vendor-r2-seal --workspace .
```

Required token:

```text
PASS_WGPU26_VENDOR_R2_SINGLE_PACKAGE_GRAPH
```

Graph inspection:

```powershell
cargo tree -d --locked
cargo tree -i cubecl-wgpu --locked
cargo tree -i wgpu@26.0.1 --locked
cargo tree -i wgpu-core@26.0.1 --locked
```

Release ABI chain:

```powershell
cargo build -p burn-wgpu-local --lib --release --locked
cargo build -p burn_webgpu_backend --lib --release --locked
cargo build -p base_train --lib --release --locked -j 1
```

Only when all graph and release gates pass may the revision emit:

```text
WGPU26_VENDOR_R2_SEALED
```

## 17. Final law

WGPU26-VENDOR-R2 makes the already-active local CubeCL WGPU fork a formally sealed ASH vendor authority. Package identity stays `cubecl-wgpu 0.9.0`, the root patch remains the single crates.io redirection point, registry `cubecl-wgpu` resolution is prohibited, and the WGPU package graph remains one 26.x lineage. Published upstream provenance is bound to the exact 0.9.0 archive checksum and provenance Git commit; ASH's source delta is explicitly limited and the misleading later `upstream_real_insert` CubeCL fragment is retired. Release promotion ends at the canonical base_train BuildPass. `WGPU26_VENDOR_R2_SEALED` unlocks the next MCU production-session residency phase.
