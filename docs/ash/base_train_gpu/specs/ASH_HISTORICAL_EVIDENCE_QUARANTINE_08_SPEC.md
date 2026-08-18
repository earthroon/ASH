# ASH-HISTORICAL-EVIDENCE-QUARANTINE-08

## Historical Proof-Line Classification / Production Import-Graph Exclusion / GPU70K Exact-Prefix Quarantine / G202D Collision Repair / Legacy R2A-E Supersession Seal / No Source Deletion

## 0. Status

```text
Patch ID: ASH-HISTORICAL-EVIDENCE-QUARANTINE-08
Direct parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Authority class: HistoricalEvidence
Production authority: None
Lineage family: historical-evidence-reconciliation
Runtime source modification: none
```

08 is a governance/static-enforcement patch. It classifies and quarantines historical proof/evidence sources without changing production runtime algorithms, optimizer mathematics, BP-Delta-K mathematics, Fusion/Fission planning, G1/G2 policy semantics, or public Rust module visibility.

## 1. Central SSOT

```text
COMPILED SOURCE != PRODUCTION AUTHORITY
PUBLIC MODULE != ACTIVE RUNTIME
SOURCE EXISTENCE != CURRENTNESS
```

Historical evidence may remain present and compile-visible, but current production source must not silently import a historical implementation.

## 2. Parent-tree inventory used by the bake

The 07 full-applied parent contains:

```text
GPU70K source files: 236
GPU70K top-level `pub mod` declarations in base_train/lib.rs: 146
non-GPU70K direct references to GPU70K module stems: 0
```

This establishes a strong 08 baseline: GPU70K is still source-visible, but current non-GPU70K Rust source does not consume its implementations.

## 3. No source deletion / no ABI mass removal

08 does not delete, rename, move, or `cfg`-hide the 236 GPU70K Rust sources.

The existing 146 top-level `pub mod ash_basetrain_gpu_70k_*` declarations are preserved.

This is deliberate. The local tree proves that current production code does not consume GPU70K, but it does not prove that no external crate or historical harness depends on the public module surface.

Physical public-ABI removal therefore remains out of scope.

## 4. Exact family classification

New tooling registry:

```text
tools/ash_historical_evidence_quarantine_08_registry.py
```

The canonical GPU70K family boundary is:

```text
filename prefix = ash_basetrain_gpu_70k_
```

Classification does not use generic tokens such as:

```text
gpu
70k
g202d
g203d
g204d
g205d
canary
production
promotion
rollback
operator_review
```

Those strings do not own lineage semantics.

## 5. GPU70K quarantine contract

The family rule is:

```text
family_id = gpu70k-proof-line
disposition = Historical
production_import_admission = Forbidden
qualification_import_admission = Forbidden
```

Current production may not import GPU70K implementation code.

Historical proof code may still reference current neutral primitives for regression/proof purposes. The quarantine direction is therefore intentionally one-way:

```text
Historical -> Current neutral primitive : allowed
Current production -> Historical implementation : forbidden
```

## 6. Production import graph gate

The 08 validator uses explicit current production roots:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/atlas_runtime_real_loss_backward.rs
```

It constructs a deterministic source-module token graph, with `lib.rs` exposure declarations excluded from runtime dependency edges.

Required invariants:

```text
non-GPU70K direct references to GPU70K = 0
production-root transitive GPU70K reachability = 0
```

A new current-source import of an `ash_basetrain_gpu_70k_*` module fails 08.

## 7. G202D collision repair

The parent registry previously contained a broad rule equivalent to:

```text
path_contains = g202d
```

That rule is removed.

This is required because the tree contains both:

```text
Historical:
crates/base_train/src/ash_basetrain_gpu_70k_g202d_quarantine_checkpoint_candidate.rs

Current:
crates/base_train/src/base_train_g202d_shared_attention_runtime.rs
```

The current shared-attention lineage is still consumed by the real backward path.

08 therefore seals:

```text
GPU70K prefix owns historical classification
G-number tokens own no classification authority
```

The same collision rule is checked for current G203D/G204D/G205D sources.

## 8. Current collision paths

The following current sources are explicitly protected from token-based historical classification:

```text
base_train_g202d_shared_attention_runtime.rs
base_train_g203d_forward_parity.rs
base_train_g204d_frozen_partition_backward.rs
base_train_g205d_gradient_accumulation_optimizer_candidate.rs
```

Their names overlap historical GPU70K generation tokens, but the exact source family does not.

## 9. Legacy Atlas R2E source remains unresolved

The legacy source:

```text
crates/base_train/src/atlas_runtime_gradient_optimizer_commit.rs
```

is classified Historical, but it is **not** placed under the same hard `Forbidden` import rule as GPU70K.

Current parent-tree incoming references are still:

```text
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/atlas_runtime_committed_generation_checkpoint_export.rs
```

Therefore its production import admission is:

```text
Unresolved
```

not `Allowed` and not `Forbidden`.

08 freezes this exact incoming-reference baseline. A new fourth consumer is treated as historical-route expansion and fails the quarantine gate.

This avoids silently disabling an existing route whose current authority has not yet been fully proven or disproven.

## 10. Legacy R2A-E semantic nodes

The existing source-less roadmap nodes remain:

```text
R2A_OLD
R2B_OLD
R2C_OLD
R2D_OLD
R2E_OLD
```

with:

```text
authority_class = HistoricalEvidence
status = Superseded
production_authority = None
```

Their existing mappings remain unchanged:

```text
R2A -> absorbed by current Planner 05
R2B -> current fused-executor domain
R2C -> 08A / 08B
R2D -> distributed across 05 / 08A / 14 / 15
R2E -> absorbed by current Planner 05
```

08 explicitly prevents those historical nodes from entering `CURRENT_EXECUTION_AUTHORITIES`.

They are historical roadmap semantics, not a new implementation backlog.

## 11. QualificationOnly is not Historical

The current qualification line remains distinct from historical quarantine.

The validator confirms current QualificationOnly status for representative authorities:

```text
DK08A physical qualification
DK08B-R1 physical same-source qualification
DK14 candidate canary qualification
```

A current qualification authority must not be downgraded to Historical just because historical code contains similar words such as `canary`, `promotion`, or `operator_review`.

## 12. Lineage registry adoption

`tools/ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-HISTORICAL-EVIDENCE-QUARANTINE-08

lineage family = historical-evidence-reconciliation
authority class = HistoricalEvidence
production authority = None
status = Active
parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

`Active` here describes the current governance/quarantine contract. It does not make the quarantined source families Active.

The current head adds:

```text
historical-evidence-reconciliation
 -> ASH-HISTORICAL-EVIDENCE-QUARANTINE-08
```

Current production execution authorities are not changed.

## 13. Vocabulary boundary

08 owns no BP-Delta-K data-plane, policy, or qualification generation:

```text
owned_data_plane_revision = None
target_data_plane_revision = None
owned_policy_generation = None
owned_qualification_generation = None
```

Historical governance is not artificially attached to `active-fusion/v1`.

## 14. Historical-family rule repair in 00

`HISTORICAL_FAMILY_RULES` is changed from broad substring semantics to exact family semantics:

```text
GPU70K -> path_prefix = ash_basetrain_gpu_70k_
Atlas R2E -> exact_filename = atlas_runtime_gradient_optimizer_commit.rs
```

The former broad `g202d` historical/reference matcher is removed.

A separate current-token collision table records exact current G202D/G203D/G204D/G205D files without granting their number tokens any lineage authority.

## 15. CF1 production vs historical-preservation classification

The existing `$AllValidators` population syntax is preserved for historical validator compatibility.

Before execution, CF1 projects it into:

```text
$ProductionValidators = @($AllValidators)
$HistoricalPreservationValidators = @(...)
```

08 is appended only to:

```text
$HistoricalPreservationValidators
```

The execution loops are distinct, and the CF1 receipt adds:

```text
productionStaticValidatorPassCount
productionStaticValidatorFailureCount
historicalPreservationValidatorPassCount
historicalPreservationValidatorFailureCount
```

The existing aggregate static-validator fields remain intact.

This separates failure meaning without rewriting dozens of historical validator string contracts.

## 16. 08 static validator

New validator:

```text
tools/validate_ash_historical_evidence_quarantine_08.py
```

It validates at least:

```text
08 registry/descriptor/head
R2A-E historical/superseded/no-execution status
QualificationOnly preservation
GPU70K exact source count
GPU70K public-module declaration baseline
GPU70K direct import count = 0
GPU70K production transitive reachability = 0
G202D historical/current exact split
G203D/G204D/G205D current collision protection
absence of broad G-token substring rules
Atlas R2E unresolved incoming-reference baseline
CF1 production/historical validator-set separation
no runtime patch-token injection
no GPU70K source move
```

The 08 validator does not load anything into the Rust runtime.

## 17. Runner

New runner:

```text
tools/run_ash_historical_evidence_quarantine_08.ps1
```

It runs:

```text
00 lineage reconciliation
01 vocabulary seal
07 Muon authority decomposition
08 historical evidence quarantine
```

No overlay search/application step is included.

## 18. Baked static evidence

Final work-tree validation:

```text
ASH-LINEAGE-RECONCILIATION-00                  175 / 175 PASS
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01          306 / 306 PASS
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02 216 / 216 PASS
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03    167 / 167 PASS
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04 198 / 198 PASS
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05        92 / 92 PASS
ASH-BP-DK-POLICY-R2-CLOSURE-06                143 / 143 PASS
ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07    345 / 345 PASS
ASH-HISTORICAL-EVIDENCE-QUARANTINE-08           82 / 82 PASS
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python validators: 64 / 64 PASS
modified Python source: py_compile PASS
```

The CF1 list was executed in two bounded halves of 32 validators each so every validator exit code completed within the execution-tool limit.

## 19. Compile / runtime evidence boundary

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore:

```text
Rust compile verification = EvidenceInsufficient / not executed
PowerShell runner execution = EvidenceInsufficient / not executed
physical training execution = not executed
```

08 modifies no Rust runtime source, so it introduces no new Rust code requiring a new runtime branch, but this is not represented as a cargo compile result.

## 20. Parent diff boundary

Compared with the 07 full-applied parent, 08 changes exactly six code/tool files:

```text
tools/ash_historical_evidence_quarantine_08_registry.py
tools/ash_lineage_reconciliation_00_registry.py
tools/run_ash_historical_evidence_quarantine_08.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_historical_evidence_quarantine_08.py
tools/validate_ash_lineage_reconciliation_00.py
```

Rust source changes:

```text
0 files
```

## 21. Packaging

Code ZIPs exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifest JSON
generated receipt JSON
generated report JSON
artifact/manifests directories
```

Deliverables:

```text
Overlay Code ZIP
 -> exactly six parent-to-08 changed tool/governance files

Full Applied Code ZIP
 -> complete 07 body with 08 applied
```

The Markdown specification remains outside the code ZIPs and is committed separately to GitHub.

## 22. Non-goals

08 does not:

```text
delete historical source
move historical source
rename historical source
remove GPU70K public modules
add historical runtime branches
change Muon runtime ownership
change G2 policy activation
change BP-Delta-K planning/execution
resolve the Atlas R2E legacy route by guess
```

## 23. Final seal

```text
HISTORICAL SOURCE IS PRESERVED
HISTORICAL SOURCE IS NOT PRODUCTION AUTHORITY

PUBLIC MODULE VISIBILITY IS NOT EXECUTION AUTHORITY
SOURCE EXISTENCE IS NOT CURRENTNESS

GPU70K IS CLASSIFIED BY EXACT FAMILY PREFIX
GPU70K IS FORBIDDEN FROM CURRENT PRODUCTION IMPORTS

NO GPU70K SOURCE IS DELETED
NO GPU70K SOURCE IS RENAMED
NO GPU70K PUBLIC ABI IS MASS-REMOVED

G202D / G203D / G204D / G205D NUMBER TOKENS OWN NO LINEAGE
CURRENT SHARED-ATTENTION/BACKWARD SOURCES ARE NOT HISTORICAL
BECAUSE HISTORICAL SOURCES SHARE THEIR NUMBERS

R2A-E REMAIN SUPERSEDED HISTORICAL ROADMAP NODES
THEY DO NOT RE-ENTER CURRENT EXECUTION AUTHORITY

QUALIFICATION-ONLY IS NOT HISTORICAL
HISTORICAL IS NOT INVALID
REFERENCE IS NOT EXECUTION

ATLAS R2E LEGACY IMPORTS REMAIN EXPLICITLY UNRESOLVED
THE KNOWN BASELINE IS FROZEN
NO NEW LEGACY CONSUMER IS SILENTLY ADMITTED

07 DEFINES WHO OWNS CURRENT STATE
08 DEFINES WHAT NO LONGER OWNS CURRENT STATE

THE ARCHIVE REMAINS VISIBLE
BUT IT CAN NO LONGER PRETEND TO BE THE ENGINE
```
