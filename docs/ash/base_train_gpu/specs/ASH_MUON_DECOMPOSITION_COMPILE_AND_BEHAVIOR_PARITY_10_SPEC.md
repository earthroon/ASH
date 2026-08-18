# ASH-MUON-DECOMPOSITION-COMPILE-AND-BEHAVIOR-PARITY-10

## Current-09 Physical Compile Authority / Normalized-06 Monolith Reference / 07 Decomposition Behavioral Equivalence / Exact Evidence Comparator / No Hidden Baseline Repair

## 0. Status

```text
Patch ID: ASH-MUON-DECOMPOSITION-COMPILE-AND-BEHAVIOR-PARITY-10
Direct parent: ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09
Authority class: OptimizerDataPlane
Lineage status: QualificationOnly
Runtime parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Current candidate: ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09
Behavior reference: ASH-MUON-PARITY-REFERENCE-06N
Raw reference: ASH-BP-DK-POLICY-R2-CLOSURE-06
Target data plane: bp-dk-data-plane/active-fusion/v1
Rust runtime source changes: 0
```

10 is a qualification harness. It does not become optimizer execution authority and does not rewrite Muon, BP-Delta-K, Fusion/Fission, G1/G2 policy, checkpoint, or training mathematics.

## 1. Central SSOT

```text
07 CHANGED STATE OWNERSHIP
07 MUST NOT HAVE CHANGED ENGINE SEMANTICS
```

A full 10 claim requires four distinct evidence stages:

```text
P0 Compile
P1 Parameter Semantics
P2 Generation Transaction
P3 Execution Surface
```

Static source validation alone does not establish any physical stage.

## 2. Raw 06 is not a valid direct compile reference

The raw 06 body contains an inherited source defect in `ProductionMuonRuntime::packed_index_for_logical()`: the 03 expected-generation guard references `optimizer_step` although that function does not own an `optimizer_step` parameter or local.

07 already moved the intended guard to `execute_muon_parameter(... optimizer_step ...)`, where the optimizer-generation authority exists.

Therefore:

```text
raw 06 = semantic reference
raw 06 != direct physical compile reference
```

10 does not silently repair arbitrary 06 failures.

## 3. Test-only normalized reference 06N

10 introduces test-only identity:

```text
ASH-MUON-PARITY-REFERENCE-06N
```

06N is not a production patch, release, lineage head, data-plane revision, or policy generation.

The preparation tool accepts exactly one normalization operation: remove the misplaced 03 expected-generation guard from `packed_index_for_logical()` and insert the same guard before training-provenance admission in `execute_muon_parameter()`.

### Exact raw-06 pins

```text
filtered file count: 7222
raw 06 filtered tree SHA-256:
cfe8614defaf26e83579513ab211759eea6b94d641ae1bc49314fa5385b88ad1

raw 06 callsite SHA-256:
f43cd15e5c820ad25b171d2c942423f0199bc40e804e72c33318031432435d57
```

Any different raw tree is rejected rather than normalized by approximation.

### Actual 06N preparation evidence from this bake

The preparer was executed against the exact baked 06 full-applied ZIP.

```text
PASS_ASH_MUON_PARITY_REFERENCE_06N_EXACT_LOCATION_REPAIR_ONLY
changed files: 1
file count: 7222
normalization semantic change count: 0
normalization location repair count: 1

normalized callsite SHA-256:
fe0d94445968f9133ccc815f85db9fc4ffe9cc547615bdc2fae2749b0e7495b6

normalized filtered tree SHA-256:
cb6021a2a8785341011f2b558f7349a9f613357f96fee5880f8111bdaaea39d1
```

This establishes reference preparation only. It is not compile or behavior parity evidence.

## 4. New tooling

```text
tools/ash_muon_decomposition_parity_10_registry.py
tools/prepare_ash_muon_parity_reference_06n.py
tools/compare_ash_muon_decomposition_parity_10.py
tools/run_ash_muon_decomposition_compile_and_behavior_parity_10.ps1
tools/validate_ash_muon_decomposition_compile_and_behavior_parity_10.py
```

The contract registry owns exact reference/current IDs, raw-06 pins, P0-P3 stages, default evidence patterns, no-invented-tolerance policy, and no-production-pointer-mutation policy.

The 06N preparer materializes raw 06 into a separate tree and verifies that the normalization changes exactly one source file.

The comparator uses:

```text
ExactCanonicalJsonOrExactBinary
```

JSON is canonically serialized only to remove formatting/key-order differences. Semantic field values are not dropped, rewritten, or tolerated. Binary evidence is exact digest comparison.

```text
inventedNumericalToleranceCount = 0
```

## 5. Physical fixture contract

The dedicated runner requires:

```text
Raw06Zip
FixtureArgsJson
WorkRoot
```

The fixture schema is:

```text
ash.muon.decomposition.parity10.fixture.v1
```

It contains the exact `base_train` CLI argument array and may use `{ROOT}` and `{OUTPUT}` placeholders.

The fixture must explicitly exercise the TensorCube Local Muon production callsite. A fixture that does not admit Muon is rejected.

The parity run may observe control-binding state but may not activate or roll back production policy. 10 is qualification-only.

## 6. P0 compile contract

Current 09 and reference 06N use separate Cargo target directories:

```text
target_current09
target_reference06n
```

Both must pass:

```text
cargo check --manifest-path crates/base_train/Cargo.toml --lib
cargo check --manifest-path crates/base_train/Cargo.toml --bin base_train
```

The existing CPU Muon deterministic oracle is also executed in both trees:

```text
local_muon_cpu_reference_is_finite_and_deterministic
```

No P1-P3 parity claim is allowed before both P0 compile authorities pass.

## 7. P1/P2/P3 exact behavior comparison

The same fixture is run independently against:

```text
REFERENCE = 06N
CANDIDATE = current 09
```

Default evidence includes:

```text
**/basetrain_tensorcube_local_muon_production_callsite_receipt.json
**/bp_dk_generation_completeness_audit_step_*.json
**/training_generation_provenance_closure_step_*.json
**/bp_dk_control_data_plane_binding_step_*.json
**/tensorcube_local_muon_momentum_manifest.json
**/tensorcube_local_muon_momentum.f32.bin
```

A fixture may explicitly add stronger evidence patterns.

Missing required evidence produces:

```text
EvidenceInsufficient
```

A semantic or binary mismatch produces:

```text
Contradictory
```

No `close enough` fallback exists.

## 8. Numerical policy

10 introduces no epsilon and no numerical tolerance.

```text
No implicit epsilon
No percentage fallback
No NaN-equals-NaN shortcut
No approximate binary digest
```

If physical GPU parity later needs a tolerance, it must come from an already authoritative numerical qualification contract in a separate explicit revision.

## 9. Current 09 ownership invariants

10 rechecks that current 09 still contains the 07 decomposition and that the inherited 03 guard is owned by the correct method.

Required current invariants include:

```text
ProductionMuonRuntime facade remains decomposed
Execution/Observation/Bridge/Planning/ControlBinding/Evidence owners remain explicit
packed_index_for_logical does not own optimizer-generation authority
execute_muon_parameter owns exactly one expected-generation gate
the generation gate precedes training-provenance admission
no Mutex<ProductionMuonRuntime>
no RefCell<ProductionMuonRuntime>
no unsafe ownership escape
```

The 10 patch token must not enter Rust/WGSL/application runtime sources.

## 10. Lineage registry

00 registry adds 10 as:

```text
family = optimizer-runtime-qualification
authority class = OptimizerDataPlane
status = QualificationOnly
direct parent = ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09
runtime parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

A separate head is added:

```text
optimizer-runtime-qualification
 -> ASH-MUON-DECOMPOSITION-COMPILE-AND-BEHAVIOR-PARITY-10
```

Current optimizer execution authority does not change:

```text
CURRENT_EXECUTION_AUTHORITIES["optimizer"]
=
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1
```

10 targets `bp-dk-data-plane/active-fusion/v1` for qualification but owns no new data-plane/policy/qualification generation.

## 11. CF1 classification

Existing groups remain:

```text
ProductionValidators
HistoricalPreservationValidators
OperationalRecoveryValidators
```

10 adds:

```text
RuntimeQualificationValidators
```

The 10 static validator is registered there. The physical compile/behavior runner remains separate from CF1 Python static qualification.

## 12. Baked static evidence

Final work-tree results:

```text
ASH-LINEAGE-RECONCILIATION-00                  196 / 196 PASS
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01          306 / 306 PASS
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02 216 / 216 PASS
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03    167 / 167 PASS
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04 198 / 198 PASS
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05        92 / 92 PASS
ASH-BP-DK-POLICY-R2-CLOSURE-06                143 / 143 PASS
ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07    345 / 345 PASS
ASH-HISTORICAL-EVIDENCE-QUARANTINE-08           82 / 82 PASS
ASH-ATLAS-R2E-ROUTE-AUTHORITY-CLOSURE-09        68 / 68 PASS
ASH-MUON-DECOMPOSITION-COMPILE-AND-BEHAVIOR-10 65 / 65 PASS
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python validators: 66 / 66 PASS
modified Python source: py_compile PASS
```

The packaged full-applied ZIP was re-extracted and the same 00-10, BP-Delta-K 25/25, and CF1 66/66 static gates passed again.

## 13. Comparator self-test boundary

The exact comparator was tested with synthetic evidence:

```text
same semantic JSON with different key order -> ParityEstablished
changed semantic value -> Contradictory
```

This validates comparator branching only. It is not Muon physical runtime parity evidence.

## 14. Physical evidence boundary in this bake

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore:

```text
P0 current09 compile = EvidenceInsufficient / not executed
P0 reference06N compile = EvidenceInsufficient / not executed
P1 parameter behavior parity = EvidenceInsufficient / not executed
P2 generation transaction parity = EvidenceInsufficient / not executed
P3 execution-surface parity = EvidenceInsufficient / not executed

FINAL PHYSICAL PARITY DISPOSITION = EvidenceInsufficient
```

Static PASS is not compile PASS.
06N normalization PASS is not reference compile PASS.
Comparator self-test PASS is not Muon behavior parity PASS.

## 15. Parent diff boundary

Compared with 09 full-applied, 10 changes exactly eight tool/governance files:

```text
MOD tools/ash_lineage_reconciliation_00_registry.py
ADD tools/ash_muon_decomposition_parity_10_registry.py
ADD tools/compare_ash_muon_decomposition_parity_10.py
ADD tools/prepare_ash_muon_parity_reference_06n.py
ADD tools/run_ash_muon_decomposition_compile_and_behavior_parity_10.ps1
MOD tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
MOD tools/validate_ash_lineage_reconciliation_00.py
ADD tools/validate_ash_muon_decomposition_compile_and_behavior_parity_10.py
```

```text
Rust runtime changes = 0
WGSL changes = 0
optimizer formula changes = 0
```

## 16. Packaging

Code ZIPs exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated reports
generated receipts
generated manifests
artifact/manifests directories
target directories
06N temporary reference tree
physical parity outputs
```

Baked package results:

```text
Overlay: 8 files
Full applied: 7235 files
Re-extracted full ZIP vs validated work tree:
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

## 17. Non-goals

10 does not optimize Muon, modify Fusion/Fission planning, change BP-Delta-K, activate G2 policy, change checkpoint schema, perform resume parity, embed a shadow 06 runtime in current Rust source, or claim performance parity.

## 18. Next revision

```text
ASH-MUON-LOAD-RESUME-CHECKPOINT-PARITY-11
```

11 should begin only after the dedicated 10 physical runner executes on a Rust-capable host and its exact disposition is known. A semantic contradiction in 10 must be resolved before resume parity proceeds.

## 19. Final seal

```text
STATIC PASS IS NOT COMPILE PASS
COMPILE PASS IS NOT BEHAVIOR PARITY

RAW 06 IS NOT SILENTLY REPAIRED
06N IS TEST-ONLY
06N ACCEPTS EXACTLY ONE SOURCE-LOCATION REPAIR

ANY OTHER REFERENCE DIFF INVALIDATES THE BASELINE

CURRENT CANDIDATE = 09
REFERENCE = 06N

CURRENT AND REFERENCE USE SEPARATE CARGO TARGET DIRECTORIES
THE SAME EXPLICIT FIXTURE MUST RUN ON BOTH

MUON ADMISSION IS REQUIRED
PRODUCTION POINTER MUTATION IS FORBIDDEN

JSON EVIDENCE IS SEMANTICALLY EXACT
BINARY EVIDENCE IS BYTE-DIGEST EXACT
NO NUMERICAL TOLERANCE IS INVENTED

MISSING EVIDENCE = EVIDENCE INSUFFICIENT
REAL MISMATCH = CONTRADICTORY

10 IS QUALIFICATION-ONLY
10 DOES NOT BECOME THE OPTIMIZER EXECUTOR

THE CURRENT BAKE PROVIDES THE PHYSICAL QUALIFICATION HARNESS
BUT THIS ENVIRONMENT CANNOT EXECUTE CARGO OR POWERSHELL

THEREFORE PHYSICAL PARITY REMAINS EVIDENCE INSUFFICIENT
UNTIL THE DEDICATED RUNNER COMPLETES ON A RUST-CAPABLE HOST
```
