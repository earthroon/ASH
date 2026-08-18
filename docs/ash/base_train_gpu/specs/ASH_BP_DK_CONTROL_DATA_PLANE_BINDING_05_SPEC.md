# ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05

## Durable Active-Pointer / Startup-Binding / Immutable Policy Artifact / Planner Runtime Provenance / Parameter Execution Binding / Generation Closure / Restart-Bound Control-to-Data Authority Seal

## 0. Status

```text
Patch ID: ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
Direct parent: ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04
Authority class: BpDkPolicyControlPlane
Primary authority: Observation
Target data plane: bp-dk-data-plane/active-fusion/v1
New data-plane revision: none
New policy generation: none
New qualification generation: none
```

This revision binds already-existing control-plane selection evidence to already-existing data-plane execution evidence. It does not take policy-selection authority from 15 and does not take Fusion/Fission decision authority from the original planner 05.

Forbidden:

```text
live active-pointer polling
policy hot reload
mid-generation policy mutation
latest-policy fallback
runtime active-pointer mutation
new policy recommendation / review / canary authority
new optimizer or Fusion mathematics
silent Local fallback on invalid binding
```

## 1. Authority split

```text
ASH-BP-DK-FUSION-FISSION-PLANNER-05
 -> BpDkDataPlane / Planning

ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
 -> BpDkPolicyControlPlane / PolicySelection

ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
 -> BpDkPolicyControlPlane / Observation
```

Therefore:

```text
CONTROL PLANE SELECTS
DATA PLANE EXECUTES
NEW 05 BINDS THEIR PROVENANCE
```

The shared numeric suffix does not imply shared lineage or authority.

## 2. Canonical chain

```text
Durable Active Pointer
 -> Exact Immutable Policy Artifact
 -> 15 Startup Binding Receipt
 -> Managed Child Startup Transport
 -> ProductionMuonRuntime one-time binding load
 -> Existing Fusion/Fission Planner 05
 -> 02 Parameter PRE Snapshot / Execution Binding
 -> Actual Local/Fused execution
 -> 03 Generation Completeness Audit
 -> 04 Training Generation Provenance Closure
 -> 05 Control/Data Generation Binding Receipt
```

05 adds provenance around this chain. It creates neither a competing selection route nor a competing planner.

## 3. Existing 15 startup binding is reused

The current 15 activation implementation already owns an immutable startup receipt containing active-pointer, policy, and policy-artifact evidence. 05 does not create a second startup truth.

The existing startup receipt is transported to the managed child through:

```text
ASH_BP_DK_FUSION_STARTUP_BINDING_PATH
ASH_BP_DK_FUSION_STARTUP_BINDING_DIGEST
```

The parent managed runner rejects pre-existing values for those variables to prevent dual authority, removes inherited values from the child command, then sets the exact receipt path and exact binding digest selected for this launch.

The existing exact policy transport remains:

```text
ASH_BP_DK_FUSION_POLICY_PATH
```

Path is a location/transport field, not policy identity.

## 4. Restart-bound semantics

```text
control-plane activation
 -> durable pointer
 -> exact startup receipt
 -> child process start
 -> immutable runtime binding
 -> zero live policy reselection during child lifetime
```

Policy change becomes effective only through a new managed startup binding.

05 introduces no step-level, parameter-level, or generation-level active-pointer polling; no latest-policy directory scan; no mtime/revision fallback; and no runtime policy reload.

## 5. New runtime module

```text
crates/base_train/src/bp_delta_k_control_data_plane_binding.rs
```

Primary types:

```text
AshBpDkControlDataPlaneBindingStatus
AshBpDkControlDataPlaneRuntimeBinding
AshBpDkParameterControlDataPlaneBinding
AshBpDkControlDataPlaneGenerationBindingReceipt
```

Primary functions:

```text
load_control_data_plane_runtime_binding
seal_parameter_control_data_plane_binding
seal_control_data_plane_generation_binding_receipt
```

## 6. Runtime binding load

`ProductionMuonRuntime` constructs the existing Fusion/Fission planner, then calls `load_control_data_plane_runtime_binding()` exactly once during runtime construction.

Disabled mode seals a `NotApplicable` binding and does not require a startup selection.

Active mode requires the exact startup-binding path and transport digest. Runtime initialization:

1. reads the exact startup receipt once,
2. verifies its binding digest,
3. verifies transport digest equality,
4. checks startup policy revision/digest against the planner policy semantics,
5. hashes the exact policy artifact bytes and checks `policy_artifact_digest`,
6. seals one immutable runtime control/data binding.

`ACTIVE + missing startup binding` is invalid. It does not silently become Local-only execution.

## 7. Digest domains remain separate

```text
active pointer digest
startup binding digest
policy artifact digest
planner policy semantic digest
runtime control/data binding digest
parameter control binding digest
generation receipt digest
```

These are separate semantic identities even when the same hash primitive is used. Equal length does not imply equivalent meaning.

## 8. Effective policy generation is not inferred

The current legacy startup-binding receipt does not carry the 01 vocabulary's explicit semantic policy-generation field. Therefore current 05 runtime bindings deliberately retain:

```text
effective_policy_generation = None
```

This is evidence-insufficient generation classification, not missing selected-artifact identity.

In particular:

```text
latest production-aware control head = G2
```

does not imply:

```text
effective runtime policy generation = G2
```

21 review/qualification evidence is not production-activation evidence. 05 does not silently label the current active runtime as G1 or G2.

## 9. Parameter binding

After 02 seals the parameter execution binding, 05 seals `AshBpDkParameterControlDataPlaneBinding` containing:

```text
parameter ID
canonical parameter index
runtime control binding digest
02 PRE snapshot digest
02 execution binding digest
planner policy digest
parameter binding digest
```

The binding verifies that the planner policy sealed by 02 equals the planner policy represented by the runtime control binding.

This validation occurs before later physical parameter execution consumes the plan. 05 does not choose Local/Fused mode itself.

## 10. Generation-local ownership

`ProductionMuonRuntime` stores generation-local parameter-control bindings in deterministic canonical order. The set is cleared with generation-local BP-Delta-K rollover/abort state.

Duplicate/cross-parameter binding is not silently replaced. In one active managed runtime all Fusion-policy-governed parameters of a generation must refer to one runtime-control-binding digest.

## 11. 03 expected-domain reconciliation

For an exact Active runtime binding, 05 compares the parameter-control-binding domain with the canonical HiMuon parameter domain sealed by 03 expected inventory.

```text
03 expected parameter IDs / canonical indices
==
05 parameter-control-binding IDs / canonical indices
```

This is exact identity comparison, not count-only comparison. AdamW-only parameters remain outside the Fusion-policy control-binding domain.

## 12. 04 closure binding

Scheduler seals the 05 generation receipt only after the existing 04 training-generation provenance closure exists:

```text
existing durable commit
 -> BP-Delta-K record_step_commit
 -> 03 generation audit
 -> 04 TrainingGenerationProvenanceClosure
 -> 05 ControlDataPlaneGenerationBindingReceipt
```

05 therefore references the exact 04 closure digest rather than duplicating the training provenance graph.

## 13. Generation receipt

`AshBpDkControlDataPlaneGenerationBindingReceipt` seals:

```text
optimizer generation
04 training-generation provenance closure digest
runtime control binding digest
canonical parameter-control-binding set digest
parameter-control-binding count
binding status
optional effective policy generation
receipt digest
```

Generated runtime receipt JSON is evidence output only and is excluded from delivered code ZIPs.

## 14. No authority inversion

```text
15 owns policy selection
old planner 05 owns Fusion/Fission decisions
02 owns parameter PRE identity
03 owns generation completeness
04 owns training-generation provenance
new 05 owns only the provenance bridge
```

04 does not become dependent on 05 as a second training-state authority.

## 15. Existing pointer guard remains

The existing 15 managed-run pointer-immutability guard remains. 05 adds no child-side live pointer watcher.

The distinction is:

```text
parent guard
 -> selected active pointer did not mutate improperly across the managed run

child binding
 -> this runtime actually consumed this exact startup selection
```

## 16. Historical validator forward compatibility

Because 05 legitimately adds startup-binding transport to the existing 15 activation module, historical validators 16, 17, and 18 are made narrowly forward-compatible.

The activation-module parent-byte exception opens only when all required 05 and pre-existing 15 anchors remain visible, including:

```text
05 control/data binding module
resolve_managed_active_policy
checkpoint-policy binding
pointer-unchanged guard
startup-binding path/digest transport
```

No generic "file changed therefore pass" exception is introduced.

## 17. Lineage registry

00 registry adds:

```text
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
family = bp-dk-control-data-binding
authority = BpDkPolicyControlPlane / Observation
status = Active
direct parent = ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04
runtime parent = Production Muon callsite
evidence parents = 15 / 02 / 03 / 04
control parent = 15
```

It explicitly does not supersede old planner 05, 13, 15, 21, 02, 03, or 04.

Current production authorities remain:

```text
policy_selection = 15
fusion_planning = old planner 05
```

## 18. Vocabulary binding

```text
owned_data_plane_revision = None
target_data_plane_revision = bp-dk-data-plane/active-fusion/v1
owned_policy_generation = None
owned_qualification_generation = None
```

No effective policy generation is defaulted from the latest control head.

## 19. Tooling and CF1

New validator:

```text
tools/validate_ash_bp_dk_control_data_plane_binding_05.py
```

New runner:

```text
tools/run_ash_bp_dk_control_data_plane_binding_05.ps1
```

CF1 order:

```text
...
21
 -> LINEAGE-RECONCILIATION-00
 -> LINEAGE-VOCABULARY-SEAL-01
 -> PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
 -> GENERATION-COMPLETENESS-AUDIT-03
 -> TRAINING-GENERATION-PROVENANCE-CLOSURE-04
 -> CONTROL-DATA-PLANE-BINDING-05
```

## 20. Baked static evidence

Validated work-tree evidence:

```text
ASH-LINEAGE-RECONCILIATION-00                    PASS 153 / 153
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01            PASS 306 / 306
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02   PASS 216 / 216
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03      PASS 167 / 167
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04   PASS 198 / 198
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05         PASS 92 / 92
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python static validators: 61 / 61 PASS
modified Python validators/registry: py_compile PASS
```

The packaged full-applied source tree was extracted and compared byte-for-byte against the validated work tree:

```text
validated work-tree files = 7,219
packaged recheck files     = 7,219
missing files              = 0
extra files                = 0
SHA-256 content diffs      = 0
```

The extracted full ZIP also re-ran reconciliation validators 00 through 05 and all 25 existing BP-Delta-K static validators successfully.

A second full 61-validator CF1 execution from the extracted ZIP exceeded the command timeout after the preceding gates. Because the packaged 7,219-file source tree is byte-identical to the already-validated 61/61 work tree, no fabricated second-execution claim is made.

## 21. Compile / physical execution boundary

The bake environment does not provide:

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
managed child physical startup execution = not executed
GPU/training runtime evidence = not claimed
```

Static/source validation is not a substitute for compilation or physical managed execution.

## 22. Parent diff boundary

Compared with the 04 full-applied parent, exactly twelve code/tool files changed:

```text
crates/base_train/src/bp_delta_k_control_data_plane_binding.rs
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs

tools/ash_lineage_reconciliation_00_registry.py
tools/run_ash_bp_dk_control_data_plane_binding_05.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_control_data_plane_binding_05.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
tools/validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
tools/validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
```

The overlay ZIP contains exactly those twelve paths.

## 23. Packaging

Code ZIPs exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifests
generated receipts
generated reports
artifact/manifests directories
```

```text
Overlay Code ZIP
 -> exactly the twelve parent-to-05 changed code/tool files

Full Applied Code ZIP
 -> complete 04 parent body with 05 applied
```

The GitHub Markdown specification remains outside both code ZIPs.

## 24. Non-goals

05 does not implement:

```text
G2 physical canary
G2 explicit production activation
G2 soak/rollback health
policy-generation inference from latest head
new Fusion topology
new planner thresholds
new optimizer mathematics
Muon runtime decomposition
policy hot reload
live pointer polling
```

## 25. Next revision

```text
ASH-BP-DK-POLICY-R2-CLOSURE-06
```

Planned control-plane continuation:

```text
21 G2 review / qualification ticket
 -> 22 G2 physical canary
 -> 23 explicit G2 production activation
 -> 24 G2 production soak / rollback health
```

Future G2 activation should reuse this restart-bound 05 binding contract rather than inventing another runtime policy bridge.

## 26. Final seal

```text
CONTROL PLANE SELECTS
DATA PLANE EXECUTES
05 BINDS THE TWO

15 KEEPS POLICY-SELECTION AUTHORITY
OLD PLANNER 05 KEEPS FUSION/FISSION DECISION AUTHORITY

ONE MANAGED CHILD PROCESS
ONE STARTUP BINDING
ONE IMMUTABLE RUNTIME CONTROL BINDING

NO LIVE POINTER POLLING
NO POLICY HOT RELOAD
NO MID-GENERATION POLICY MUTATION
NO LATEST-POLICY FALLBACK

POINTER DIGEST
!= STARTUP BINDING DIGEST
!= POLICY ARTIFACT DIGEST
!= PLANNER SEMANTIC DIGEST

02 SNAPSHOT MUST CONSUME THE SAME PLANNER POLICY
03 EXPECTED HIMUON DOMAIN MUST MATCH THE CONTROL-BOUND DOMAIN
04 TRAINING PROVENANCE REMAINS THE TRAINING AUTHORITY

LATEST POLICY DOES NOT MEAN ACTIVE POLICY
G2 REVIEW DOES NOT MEAN G2 PRODUCTION ACTIVATION
NO GENERATION IS INFERRED
NO INVALID BINDING SILENTLY FALLS BACK TO LOCAL

ACTIVE POINTER
 -> STARTUP BINDING
 -> POLICY ARTIFACT
 -> PLANNER SEMANTICS
 -> PARAMETER EXECUTION
 -> TRAINING GENERATION RECEIPT

IS ONE TRACEABLE CONTROL-TO-DATA LINEAGE
```
