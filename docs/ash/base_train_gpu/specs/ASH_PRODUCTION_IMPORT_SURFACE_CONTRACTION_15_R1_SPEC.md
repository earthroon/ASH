# ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15-R1

## MONOTONIC HISTORICAL FAMILY PRESERVATION / BASELINE SUBSET IMMUTABILITY / POST-BASELINE HISTORICAL ADDITION ADMISSION / CURRENT NON-GPU BIN AVAILABILITY REBASE / EXPLICIT 160-BIN CARGO ALLOWLIST / NO GPU70K BUILD RE-ADMISSION

## 0. Status

```text
Patch ID: ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15-R1
Physical direct parent: ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16
Repaired authority: ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
Historical parent: ASH-HISTORICAL-EVIDENCE-QUARANTINE-08
R2E parent: ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09
Lineage family: production-build-surface
Authority class: BuildSurfaceGovernance
Production authority: CompileSurfaceAdmission
Status: Active / RepairRevision
```

15-R1 repairs the temporal model of 15. It does not change Muon math, BP-Delta-K math, scheduler order, recovery semantics, WGSL, checkpoint schemas, or the 16 hotpath ownership cleanup.

## 1. Triggering contradiction

Patch 15 baked against this exact parent snapshot:

```text
GPU70K root sources = 236
GPU70K bin sources = 354
GPU70K total = 590
non-GPU src/bin sources = 143
explicit Cargo bins = 143
```

The user's current local lineage was physically observed as:

```text
GPU70K root sources = 268
GPU70K bin sources = 399
GPU70K total = 667
non-GPU src/bin sources = 160
explicit Cargo bins = 143
```

Delta from the 15 parent:

```text
GPU70K root +32
GPU70K bin +45
GPU70K total +77
non-GPU bin +17
```

The old 15 validator incorrectly treated the historical family snapshot as a permanent current-world equality constraint.

## 2. Repaired SSOT

```text
HISTORICAL PRESERVATION != HISTORICAL FAMILY FREEZE

ADOPTED BASELINE FILES MAY NOT DISAPPEAR
ADOPTED BASELINE FILES MAY NOT MUTATE
NEW HISTORICAL FILES MAY APPEAR
NEW HISTORICAL FILES MAY NOT REGAIN A BUILD EDGE
```

The GPU70K family is therefore monotonic at the source-governance layer while remaining zero-admission at the production build layer.

## 3. Parent-15 immutable subset

15-R1 adds an exact 590-entry path+SHA256 baseline generated from the original 15/16 baked parent:

```text
tools/ash_production_import_surface_contraction_15_r1_baseline.py
```

Validation is per-file:

```text
Parent15 baseline path exists
AND
SHA256(current file) == SHA256(parent15 baseline file)
```

The previous whole-tree equality checks are removed from current authority.

The old aggregate digests remain historical provenance only:

```text
root baseline digest:
6405499d91bbc59bcf0165ad504fdc3f932910e8425073335c483b26232ea1c4

bin baseline digest:
385bad486acf50ec7b43d18498538832ba963401ae8fdf87ff7b03cac911e36c

all baseline digest:
e1495144aab5635feef47144a5b053a4020a0d472eb6577bcf614b0ae7cc2a73
```

They are not compared against the entire future historical tree.

## 4. Current R1 observation

The user's observed current historical tree is recorded as an adoption-time lower-bound witness, not a ceiling:

```text
root floor = 268
bin floor = 399
total floor = 667
```

Observed current aggregate digests are diagnostic only:

```text
root:
d36933730e0eb1fc0e9958f00de797a7f4218e4abb15c92f2ff53bfbe74dea32

bin:
fec23ee621f84416d50df9b9ebc85b583a077183d82cbbd17bb5beab4ee7dcd4

all:
079cfbefd5984c53670c0ad0a15ae93a55ecb5b8201f0a47b2ebb2d2a366892c
```

15-R1 does not require future whole-tree equality to these values.

## 5. Post-baseline GPU70K additions

Current files outside the immutable Parent-15 subset are admitted as historical additions only when the exact GPU70K family prefix owns them.

All current and future GPU70K files remain subject to:

```text
lib.rs exposure = 0
Cargo target = 0
non-family direct Rust references = 0
```

`autobins = false` remains mandatory, preventing historical `src/bin` files from silently becoming executables.

## 6. 08 historical validator forward compatibility

08 previously required:

```text
root GPU70K source count == 236
```

15-R1 changes this check to preservation of the Parent-15 historical floor:

```text
root GPU70K source count >= 236
```

The family classification, zero direct-reference rule, production reachability quarantine, token-collision protections, and R2E route-bound semantics remain unchanged.

This is required so 08 does not reject legitimate post-baseline historical accumulation before 15-R1 runs.

## 7. Non-GPU executable availability rebase

The user's local tree contains 17 non-GPU `src/bin` files that were absent from the 15 bake snapshot and therefore lost Cargo admission when `autobins=false` was introduced.

15-R1 restores explicit Cargo admission for these exact files:

```text
ash_basetrain_gpu_01_tensor_group_manifest_parser_execution.rs
ash_basetrain_gpu_07_forward_output_receipt_audit.rs
ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt.rs
ash_basetrain_gpu_35_r1_selected_group_manifest_binding.rs
ash_basetrain_gpu_35_r1a_selected_group_manifest_binding_failure_triage.rs
ash_basetrain_gpu_35_r2_selected_group_manifest_template_materialization.rs
ash_basetrain_gpu_35_r2a_operator_manifest_materialization_failure_detail.rs
ash_basetrain_gpu_35_r2c_atlas_group_plan_receipt_locator.rs
ash_basetrain_gpu_35_r3_selected_group_manifest_from_atlas_plan_receipt.rs
ash_basetrain_gpu_59_forward_candidate_operator_approval_gate.rs
ash_basetrain_gpu_70m_qkv_manifest_source_selection.rs
ash_basetrain_hotpath_01_r3_dataset_text_compose_candidate_promotion_gate.rs
ash_basetrain_hotpath_01_r3a_dataset_text_compose_real_dataset_parity_preflight.rs
ash_basetrain_hotpath_01_r4_dataset_text_compose_candidate_default_swap.rs
ash_basetrain_hotpath_03_training_loop_typed_receipt_staging.rs
checkpoint_smoke_generate.rs
checkpoint_text_generate.rs
```

The R1 non-GPU availability baseline is therefore:

```text
143 Parent-15 retained paths
+17 recovered current paths
=160 baseline paths
```

## 8. Future non-GPU growth

160 is a baseline, not a permanent ceiling.

Current invariant:

```text
CURRENT non-GPU src/bin source path set
==
CURRENT explicit Cargo bin target path set
```

Therefore a future 161st non-GPU bin is admitted only if its source and explicit Cargo target arrive together.

This preserves both:

```text
NO SILENT EXECUTABLE LOSS
NO SILENT EXECUTABLE GROWTH
```

## 9. Cargo state after applying 15-R1 to the user's current tree

Expected:

```text
autobins = false
non-GPU src/bin sources = 160
explicit Cargo bins = 160
GPU70K Cargo targets = 0
missing explicit target paths = 0
base_train target = exactly 1
```

Target names and target paths must both be unique.

## 10. R2E remains operationally retained

R2E is not GPU70K and is not contracted by 15-R1.

Expected incoming references remain exactly:

```text
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/atlas_runtime_committed_generation_checkpoint_export.rs
```

09's explicit recovery-bootstrap admission semantics remain authoritative.

## 11. Lineage repair

15 remains registered as historical build-surface provenance.

16 remains the hotpath ownership head:

```text
optimizer-hotpath-ownership
→ ASH-HOTPATH-OWNERSHIP-BORROW-CLEANUP-16
```

15-R1 becomes the current build-surface head:

```text
production-build-surface
→ ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15-R1

CURRENT_BUILD_SURFACE_AUTHORITIES["base_train"]
→ ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15-R1
```

15-R1 physically follows 16 and supersedes 15 only for current build-surface authority. It does not supersede 16 runtime ownership semantics.

## 12. CF1 adoption

The old exact-snapshot 15 validator is retained as source provenance but removed from the current `ProductionValidators` set.

Current production gate uses:

```text
validate_ash_production_import_surface_contraction_15_r1.py
```

16 runner is forward-updated to invoke 15-R1 instead of the old 15 validator.

## 13. New tooling

```text
tools/ash_production_import_surface_contraction_15_r1_baseline.py
tools/ash_production_import_surface_contraction_15_r1_registry.py
tools/validate_ash_production_import_surface_contraction_15_r1.py
tools/run_ash_production_import_surface_contraction_15_r1.ps1
```

Modified governance/tooling:

```text
crates/base_train/Cargo.toml
tools/ash_lineage_reconciliation_00_registry.py
tools/validate_ash_lineage_reconciliation_00.py
tools/validate_ash_historical_evidence_quarantine_08.py
tools/run_ash_hotpath_ownership_borrow_cleanup_16.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Total overlay diff:

```text
10 files
```

No Muon runtime Rust, scheduler Rust, BP-Delta-K algorithm Rust, WGSL, or checkpoint schema file is changed.

## 14. Validation evidence

Because the assistant-side parent does not contain the user's local-only +77 GPU70K files or +17 non-GPU bin source contents, a synthetic local-lineage mirror was used only to exercise the governance contracts. Synthetic files are not included in delivered artifacts.

On that mirror:

```text
00 lineage = 284 / 284 PASS
08 historical quarantine = 83 / 83 PASS
09 R2E authority = 68 / 68 PASS
15-R1 build surface = 49 / 49 PASS
16 hotpath ownership = 80 / 80 PASS
```

Active CF1 Python validator set, with old 15 removed and 15-R1 added:

```text
72 / 72 PASS
```

Negative contract tests:

```text
future extra GPU70K historical source
→ PASS

one Parent-15 baseline file byte mutation
→ FAIL gpu70k:parent15-baseline-byte-immutable

one R1 non-GPU baseline source removed
→ FAIL cargo:missing-target-path-zero
     cargo:r1-non-gpu-baseline-source-present
     cargo:current-non-gpu-source-target-exact
```

The packaged overlay was reapplied to a fresh synthetic local-lineage mirror and re-passed the active 00/08/15-R1/16 chain.

## 15. Packaging boundary

Delivered code artifact:

```text
ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15-R1 local-lineage overlay
10 changed files
```

A full-applied ZIP is intentionally not emitted.

Reason:

```text
The user's current tree contains 94 local-only source files relative to the assistant's 16 baked parent:
77 GPU70K historical additions
17 non-GPU bin additions
```

The assistant does not possess their source contents. Producing a full-applied tree would require either deleting them or fabricating them, both of which violate the project SSOT.

The overlay is therefore the correct artifact for this repair revision.

## 16. Physical evidence boundary

The assistant environment still does not provide the user's Rust/PowerShell execution environment. The following must be run on the user's local current tree after applying the overlay:

```text
cargo metadata
cargo check --lib
cargo check --bin base_train
cargo check --all-targets
cargo test --lib --no-run
```

The dedicated 15-R1 runner executes these in order after static 00/08/09/15-R1/16 gates.

Current local physical compilation remains EvidenceInsufficient until the user runs that command.

## 17. Final seal

```text
HISTORY MAY GROW
BUT ADOPTED BASELINE HISTORY MAY NOT DISAPPEAR OR MUTATE

THE PARENT-15 590-FILE BASELINE IS AN IMMUTABLE SUBSET
NOT A PERMANENT WHOLE-WORLD SNAPSHOT

THE CURRENT +77 GPU70K FILES ARE NOT A REGRESSION
SIMPLY BECAUSE THEY EXIST

GPU70K LIBRARY EXPOSURE REMAINS ZERO
GPU70K CARGO TARGETS REMAIN ZERO
AUTOBINS REMAINS FALSE

NON-GPU EXECUTABLE AVAILABILITY IS REBASED TO THE ACTUAL 160-FILE LOCAL LINEAGE
THE 17 CURRENTLY PRESENT BIN SOURCES REGAIN EXPLICIT CARGO TARGETS

160 IS A BASELINE, NOT A CEILING
FUTURE NON-GPU BIN GROWTH REQUIRES SOURCE AND EXPLICIT TARGET TO ARRIVE TOGETHER

08 STILL OWNS HISTORICAL CLASSIFICATION
09 STILL OWNS R2E RECOVERY AUTHORITY
16 STILL OWNS HOTPATH OWNERSHIP PROJECTION
15-R1 NOW OWNS THE CURRENT BASE_TRAIN BUILD-SURFACE CONTRACT

THE BUG WAS NOT THAT HISTORY GREW
THE BUG WAS THAT 15 TREATED A HISTORICAL SNAPSHOT AS A PERMANENT CEILING
```
