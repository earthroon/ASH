# ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15

## GPU70K Historical Source Preservation / Library Exposure Removal / Cargo Autobin Firewall / Explicit Non-GPU70K Bin Allowlist / R2E Operational Recovery Preservation

## 0. Status

```text
Patch ID: ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
Direct parent: ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14
Historical classification parent: ASH-HISTORICAL-EVIDENCE-QUARANTINE-08
R2E authority parent: ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09
Lineage family: production-build-surface
Authority class: BuildSurfaceGovernance
Production authority: CompileSurfaceAdmission
Status: Active
```

15 contracts the `base_train` build/import surface without deleting historical evidence. It does not change Muon mathematics, BP-Delta-K mathematics, generation transaction semantics, failure recovery semantics, checkpoint schemas, GPU shaders, or the R2E operational recovery route.

## 1. Central SSOT

```text
SOURCE PRESERVATION != COMPILE ADMISSION

A HISTORICAL SOURCE MAY REMAIN IN THE REPOSITORY
WITHOUT REMAINING A RUST MODULE OR CARGO TARGET.
```

08 owns the historical classification.
09 owns the explicit R2E recovery-bootstrap route.
15 owns the physical build-surface admission contract.

## 2. Parent-14 physical inventory

The exact parent-14 body contained:

```text
GPU70K root Rust sources:                 236
GPU70K top-level `pub mod` declarations: 146
GPU70K src/bin Rust sources:              354
non-GPU70K src/bin Rust sources:          143
Cargo explicit [[bin]] entries:           262
Cargo explicit GPU70K entries:            216
Cargo explicit non-GPU70K entries:         46
explicit targets with missing source:      29
```

Of the 29 missing target paths:

```text
GPU70K:     26
non-GPU70K:  3
```

The three non-GPU70K missing target names were:

```text
ash_basetrain_gpu_01_tensor_group_manifest_parser_execution
ash_basetrain_gpu_59_forward_candidate_operator_approval_gate
ash_basetrain_gpu_70m_qkv_manifest_source_selection
```

15 does not reclassify these three as historical. Their only established property is that their explicit Cargo target paths did not exist in the parent source tree.

## 3. GPU70K dependency evidence

Outside `lib.rs` and the GPU70K family itself, direct references to GPU70K module stems were:

```text
0
```

This agrees with the 08 contract:

```text
GPU70K disposition = Historical
production import admission = Forbidden
qualification import admission = Forbidden
```

Therefore the family can be removed from the crate/module and Cargo target graphs while preserving its source files as historical evidence.

## 4. Historical source byte-preservation seal

15 preserves every classified GPU70K source byte-for-byte.

```text
GPU70K root source count: 236
GPU70K bin source count:  354
GPU70K total source count: 590
```

Canonical path+content aggregate digests:

```text
root sources:
6405499d91bbc59bcf0165ad504fdc3f932910e8425073335c483b26232ea1c4

bin sources:
385bad486acf50ec7b43d18498538832ba963401ae8fdf87ff7b03cac911e36c

all GPU70K historical sources:
e1495144aab5635feef47144a5b053a4020a0d472eb6577bcf614b0ae7cc2a73
```

15 validation requires these exact counts and digests.

```text
historical source modified count = 0
historical source deleted count  = 0
```

The files are not moved into an archive directory and are not wrapped in a new historical crate.

## 5. Library module contraction

Parent:

```text
crates/base_train/src/lib.rs
pub mod ash_basetrain_gpu_70k_*;
count = 146
```

15:

```text
count = 0
```

No `#[cfg(test)]` replacement modules are created. 08 forbids both production and qualification import admission for this family.

The physical source files remain at their original paths.

## 6. Cargo autobin firewall

`crates/base_train/Cargo.toml` now declares:

```toml
[package]
autobins = false
```

This creates an explicit distinction:

```text
src/bin file exists
!=
Cargo executable target exists
```

A future file added under `src/bin` cannot silently enlarge the executable surface. Target admission now requires an explicit `[[bin]]` entry.

## 7. GPU70K Cargo contraction

Parent:

```text
explicit GPU70K [[bin]] entries = 216
auto bin discovery             = enabled
GPU70K src/bin sources          = 354
```

15:

```text
explicit GPU70K [[bin]] entries = 0
auto bin discovery             = disabled
GPU70K src/bin sources          = 354, preserved
```

Therefore the classified GPU70K family has:

```text
library module exposure = 0
Cargo binary targets    = 0
historical source files = preserved
```

## 8. Non-GPU70K availability preservation

15 deliberately does not perform a broad semantic cleanup of the remaining `src/bin` tree.

Every currently existing non-GPU70K bin source is retained as an explicit Cargo target:

```text
existing non-GPU70K src/bin sources = 143
contracted explicit bin targets      = 143
```

This includes sources that were previously explicit and sources that were previously admitted only by Cargo autobin discovery.

The `base_train` production binary is now explicitly admitted:

```toml
[[bin]]
name = "base_train"
path = "src/bin/base_train.rs"
```

Static validation requires:

```text
explicit target names unique = true
explicit target paths unique = true
all explicit target paths exist = true
base_train target count = 1
```

No non-GPU70K target is removed merely because patch 15 has not classified its semantic role.

## 9. Missing explicit target elimination

Parent explicit Cargo targets with missing source paths:

```text
29
```

15 contracted state:

```text
0
```

This is a manifest-surface correction, not a claim that all removed ghost entries were historical.

No source is fabricated to satisfy a missing target, and no missing target receives a silent replacement path.

## 10. R2E operational route preservation

R2E is explicitly excluded from GPU70K contraction.

Source:

```text
crates/base_train/src/atlas_runtime_gradient_optimizer_commit.rs
```

Its exact non-self incoming references remain:

```text
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/atlas_runtime_committed_generation_checkpoint_export.rs
```

09 semantics remain:

```text
route scope = RecoveryBootstrap
execution admission = ExplicitOnly
current R6 production execution = Forbidden
```

15 therefore retains the R2E library declaration, pipeline branch, and R3 dependency.

```text
GPU70K = HistoricalSourceOnly / no build edge
R2E    = OperationalRouteBound / build edge retained
```

These are intentionally different dispositions.

## 11. Current G-token collision protection

15 continues to preserve the exact current sources:

```text
base_train_g202d_shared_attention_runtime.rs
base_train_g203d_forward_parity.rs
base_train_g204d_frozen_partition_backward.rs
base_train_g205d_gradient_accumulation_optimizer_candidate.rs
```

No generic `g202d`, `g203d`, `g204d`, or `g205d` token is treated as historical authority.

Only the exact family prefix:

```text
ash_basetrain_gpu_70k_
```

owns the 15 contraction rule.

## 12. 08 forward-compatible quarantine update

08 retains its parent fact:

```text
GPU70K_PARENT14_TOP_LEVEL_MODULE_DECLARATION_COUNT = 146
```

and now separately recognizes the current contracted expectation:

```text
GPU70K_CONTRACTED_TOP_LEVEL_MODULE_DECLARATION_COUNT = 0
```

08 still requires:

```text
GPU70K root source count = 236
historical disposition
production import forbidden
non-family direct references = 0
production transitive reachability = 0
R2E route-bound reference preserved
```

Thus 08 remains the preservation/classification authority while 15 enforces the build-surface result.

## 13. Lineage adoption

`ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15

family = production-build-surface
authority class = BuildSurfaceGovernance
production authority = CompileSurfaceAdmission
status = Active
direct parent = ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14
```

Evidence/governance parents include:

```text
08 Historical Evidence Quarantine
09 Atlas R2E Route Authority
14 Recovery Physical Fault Matrix qualification surface
```

New head:

```text
production-build-surface
→ ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
```

A separate governance map now seals:

```text
CURRENT_BUILD_SURFACE_AUTHORITIES["base_train"]
= ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
```

15 is not placed in `CURRENT_EXECUTION_AUTHORITIES`.

## 14. CF1 classification

15 is a production build-surface invariant, not merely a qualification artifact.

Therefore its static validator is added to:

```text
ProductionValidators
```

08 remains in:

```text
HistoricalPreservationValidators
```

09 remains in:

```text
OperationalRecoveryValidators
```

14 remains in:

```text
RuntimeQualificationValidators
```

The pair of 08 + 15 gates enforces both sides:

```text
08 -> historical source must remain
15 -> historical source must not re-enter production build surface
```

## 15. New tooling

```text
tools/ash_production_import_surface_contraction_15_registry.py
tools/validate_ash_production_import_surface_contraction_15.py
tools/run_ash_production_import_surface_contraction_15.ps1
```

The dedicated runner performs:

```text
00 lineage validation
08 historical quarantine validation
09 R2E route validation
15 build-surface validation
cargo metadata --no-deps
cargo check --lib
cargo check --bin base_train
cargo check --all-targets
```

It contains no overlay application step.

## 16. Parent diff boundary

Compared with the exact 14 full-applied parent, the 15 bake changes exactly 10 files:

```text
MOD crates/base_train/Cargo.toml
MOD crates/base_train/src/lib.rs

MOD tools/ash_historical_evidence_quarantine_08_registry.py
MOD tools/validate_ash_historical_evidence_quarantine_08.py

MOD tools/ash_lineage_reconciliation_00_registry.py
MOD tools/validate_ash_lineage_reconciliation_00.py

MOD tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1

ADD tools/ash_production_import_surface_contraction_15_registry.py
ADD tools/validate_ash_production_import_surface_contraction_15.py
ADD tools/run_ash_production_import_surface_contraction_15.ps1
```

Runtime implementation files changed:

```text
Muon runtime:     0
R6 scheduler:     0
BP-Delta-K math:  0
WGSL:             0
```

One Rust crate-root file changes for module admission:

```text
crates/base_train/src/lib.rs
```

Historical GPU70K Rust source changes remain zero.

## 17. Static validation evidence

Validated source tree:

```text
00  252 / 252 PASS
01  306 / 306 PASS
02  216 / 216 PASS
03  167 / 167 PASS
04  198 / 198 PASS
05   92 /  92 PASS
06  143 / 143 PASS
07  347 / 347 PASS
08   83 /  83 PASS
09   68 /  68 PASS
10   66 /  66 PASS
11   91 /  91 PASS
12  156 / 156 PASS
13  140 / 140 PASS
14  165 / 165 PASS
15   45 /  45 PASS
```

Additional validation:

```text
BP-Delta-K *_static.py validators = 25 / 25 PASS
CF1-enumerated Python validators   = 71 / 71 PASS
changed/new Python syntax          = 6 / 6 PASS
Cargo.toml Python tomllib parse    = PASS
```

Static Cargo inspection confirms:

```text
autobins = false
explicit bin count = 143
missing target paths = 0
GPU70K target count = 0
base_train target count = 1
```

## 18. Packaged artifact verification

```text
Overlay Code ZIP = 10 files
Full Applied ZIP = 7254 files
```

Re-extracted Full ZIP versus validated source tree:

```text
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

The re-extracted Full ZIP directly re-passed:

```text
00→15 reconciliation/static chain = 16 / 16 PASS
BP-Delta-K static                 = 25 / 25 PASS
CF1-enumerated Python validators = 71 / 71 PASS
```

Code ZIPs contain no Markdown specs, `*.sha256`, `*.pyc`, or `__pycache__` files.

## 19. Physical Cargo evidence boundary

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore the following are not claimed here:

```text
cargo metadata physical PASS
cargo check --lib physical PASS
cargo check --bin base_train physical PASS
cargo check --all-targets physical PASS
PowerShell runner physical PASS
```

Current physical build disposition remains:

```text
EvidenceInsufficient
```

Static target-surface closure is established; physical Rust compilation is not.

## 20. Runtime-source identity change

The 10/11/14 physical qualification chain binds receipts to `runtime_source_digest()`, whose domain includes:

```text
crates/base_train/src/**/*.rs
crates/base_train/Cargo.toml
Cargo.lock when present
```

15 changes both `src/lib.rs` and `Cargo.toml`, so exact runtime-source identity changes even though Muon/scheduler/math implementation does not.

Exact digest transition:

```text
Parent 14 runtime-source digest:
a2167281461d69f50bde920cd4dc597178944578917813f74dcdbd9469f7838d

Current 15 runtime-source digest:
2960bb94abb4b9bece195e5c9b70ed195d84585d1228ad4aad2ed0151d691ca8

runtime-source file count: 969 -> 969
```

Therefore any physical 10/11/14 receipt bound to the parent-14 digest is stale for the 15 source tree and must be regenerated before an end-to-end current-source physical qualification claim.

## 21. Non-goals

15 does not:

```text
delete GPU70K source
rewrite GPU70K source
move GPU70K source
repair GPU70K compile errors
classify all remaining non-GPU binaries
remove R2E
feature-gate R2E
change R6 runtime admission
change optimizer mathematics
change BP-Delta-K mathematics
change checkpoint format
change recovery semantics
change GPU/WGSL behavior
claim build-time speedup without measurement
```

## 22. Error taxonomy

```text
Gpu70kHistoricalSourceMissing
Gpu70kHistoricalSourceModified
Gpu70kLibraryExposureReintroduced
Gpu70kCargoTargetReintroduced
CargoAutobinFirewallMissing
CargoExplicitTargetMissingPath
CargoBinTargetNameCollision
CargoBinTargetPathCollision
BaseTrainTargetMissing
NonGpuBinAvailabilityLost
R2ERouteSurfaceUnexpectedlyRemoved
R2EProductionAuthorityEscalated
CurrentGNumberCollisionMisclassified
HistoricalSourceDeletionDetected
CargoMetadataContradiction
BuildSurfaceContractContradiction
EvidenceInsufficient
```

## 23. Physical acceptance gates

On a Rust-capable host, full 15 closure requires:

```text
P0 cargo metadata --no-deps PASS
P1 metadata target inventory exact
P2 cargo check --lib PASS
P3 cargo check --bin base_train PASS
P4 cargo check --all-targets PASS
P5 GPU70K Cargo target count remains 0
P6 historical source digest inventory unchanged
```

A compile error from GPU70K would indicate a surface leak. 15 must not repair historical GPU70K code merely to make it compile.

A compile error in retained current code is a real current-build contradiction and must be repaired before progressing.

## 24. Next revision

After physical 15 Cargo closure on the exact current source, the natural next patch is:

```text
ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16
```

That patch can inspect borrow lifetimes, unnecessary clones, temporary ownership, and owner access paths against a much cleaner current production compile surface.

If 15 physical compile finds a contradiction, 16 should not proceed until a 15 repair revision closes it.

## 25. Final seal

```text
HISTORICAL SOURCE IS PRESERVED
WITHOUT REMAINING PRODUCTION BUILD SURFACE

GPU70K ROOT SOURCE COUNT REMAINS 236
GPU70K BIN SOURCE COUNT REMAINS 354
GPU70K HISTORICAL SOURCE BYTES REMAIN SEALED

GPU70K LIBRARY MODULE EXPOSURE IS 0
GPU70K CARGO TARGET COUNT IS 0

CARGO AUTOBIN DISCOVERY IS DISABLED

SRC/BIN PRESENCE NO LONGER AUTO-ADMITS EXECUTION

ALL 143 EXISTING NON-GPU70K BIN SOURCES
REMAIN EXPLICITLY ADMITTED

ALL EXPLICIT TARGET PATHS EXIST
BASE_TRAIN IS AN EXPLICIT TARGET

MISSING TARGETS ARE REMOVED AS MISSING TARGETS
NOT SILENTLY RECLASSIFIED HISTORY

R2E IS NOT GPU70K
R2E REMAINS OPERATIONAL ROUTE-BOUND RECOVERY
R2E CURRENT R6 PRODUCTION EXECUTION REMAINS FORBIDDEN

08 PRESERVES THE HISTORY
09 PRESERVES THE RECOVERY ROUTE
15 ENFORCES THE BUILD-SURFACE BOUNDARY

NO HISTORICAL SOURCE DELETION
NO HISTORICAL SOURCE REWRITE
NO BROAD G-TOKEN CLASSIFICATION
NO RUNTIME MATH CHANGE
NO CHECKPOINT CHANGE
NO GPU CHANGE

AFTER 15,
A SOURCE FILE MAY EXIST WITHOUT BEING A MODULE,
AND A BIN SOURCE MAY EXIST WITHOUT BEING A CARGO TARGET.

THAT DISTINCTION IS THE CLOSURE.
```
