# ASH-BP-DK-POLICY-R2-CLOSURE-06

## Production-Aware Policy G2 Physical Canary / Explicit G2 Activation / Revisioned Active Pointer V2 / Managed Restart / Runtime Confirmation / Soak Health / Explicit Rollback Closure

## 0. Status

```text
Patch ID: ASH-BP-DK-POLICY-R2-CLOSURE-06
Direct parent: ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
Authority class: BpDkPolicyControlPlane
Primary authority: PolicySelection
Policy generation: bp-dk-policy/production-aware/g2
Qualification generation: bp-dk-qualification/production-aware/g2
Target data-plane revision: bp-dk-data-plane/active-fusion/v1
New data-plane revision: none
```

This revision closes the production-aware G2 control lineage without rewriting the legacy G1 15/16/17 contracts and without changing Fusion, Muon, BP-Delta-K, forward, backward, or optimizer mathematics.

## 1. Central authority split

```text
21 = G2 operator review / qualification-ticket authority
06A = G2 physical canary qualification authority
06B = explicit G2 production activation authority
05 = control-to-data runtime provenance binding authority
old Planner 05 = Fusion/Fission planning authority
06C = G2 production soak/health evidence authority
```

A review ticket is not a canary receipt.
A canary receipt is not an activation intent.
An activation intent is not an active pointer.
An active pointer is not an effective runtime until managed startup is confirmed.

## 2. No G1 ticket masquerade

The new 06 module consumes the existing production-aware 21 ticket:

```text
AshFusionProductionAwareQualificationTicketR2
```

It does not import, construct, or convert through the legacy G1 qualification types:

```text
AshBpDkFusionPolicyQualificationTicket
AshBpDkFusionPolicyCanaryQualificationReceipt
```

The legacy 14 physical branch executor is reused only as a generation-neutral process-execution primitive.

## 3. G2 physical canary

New module:

```text
crates/base_train/src/bp_delta_k_policy_r2_closure.rs
```

G2 canary admission requires exact evidence for:

```text
21 qualification ticket
candidate policy digest
candidate policy artifact digest
target/current policy digest
bounded canary schedule
source checkpoint authority
base-train binary digest
model-spec digest
common-argument digest
explicit G2 canary qualification policy
```

Canary disposition:

```text
Qualified
Rejected
EvidenceInsufficient
Contradictory
```

Missing evidence is not silently converted into rejection or success.

## 4. Non-production canary runtime binding

After 05, Active planner mode requires an exact control/data runtime binding. A physical canary therefore cannot simply launch an Active child with only a policy path.

06 closes that structural gap explicitly.

05 runtime binding now carries a scope:

```text
NotApplicable
Production
QualificationCanary
```

The runtime-binding schema and generation-receipt schema are revisioned to v2 for this scope addition.

06A creates separate immutable non-production runtime bindings for:

```text
CURRENT_BASELINE
CANDIDATE
```

and passes them to the canary child through:

```text
ASH_BP_DK_G2_CANARY_RUNTIME_BINDING_PATH
ASH_BP_DK_G2_CANARY_RUNTIME_BINDING_DIGEST
```

05 validates the canary binding before admitting Active planner execution.

The canary binding explicitly seals:

```text
qualification ticket digest
branch kind
policy revision
policy digest
policy artifact digest
optional policy generation
G2 qualification generation
planner policy digest
schedule digest
production_active = false
binding digest
```

The candidate branch explicitly carries Policy G2.
The current baseline branch does not infer a policy generation from the latest G2 control head.

Thus:

```text
CANARY ACTIVE PLANNER EXECUTION
!= PRODUCTION ACTIVE POINTER AUTHORITY
```

## 5. Physical canary source immutability

06A verifies before and after branch execution that the bounded source checkpoint authority is unchanged.

If a production active-pointer file is supplied as witness, its file digest must also remain unchanged across canary execution.

Canary code has no production-pointer mutation path.

## 6. G2 canary receipt

The immutable G2 canary receipt binds:

```text
21 ticket digest
candidate policy digest/artifact digest
target policy digest
G2 policy/qualification generations
canary qualification-policy digest
baseline non-production runtime-binding digest
candidate non-production runtime-binding digest
schedule digest
baseline branch receipt digest
candidate branch receipt digest
evidence-set digest
disposition
receipt digest
```

The baseline and candidate runtime bindings remain distinct evidence identities.

## 7. Explicit activation only

A Qualified canary alone does not mutate the active pointer.

06B requires an explicit `AshBpDkG2ActivationIntent` that binds:

```text
exact 21 ticket
exact Qualified 06A canary receipt
exact candidate policy digest
exact candidate artifact digest
expected previous active-pointer digest
G2 policy generation
G2 qualification generation
```

Any candidate substitution or stale previous-pointer identity is rejected.

## 8. Active Pointer V2

06 introduces a revisioned semantic sidecar:

```text
AshBpDkActivePolicyPointerV2
active/bp_dk_fusion_active_policy_v2.json
```

V2 explicitly carries:

```text
pointer revision
selected candidate ID
selected policy revision/digest/artifact digest
policy generation = bp-dk-policy/production-aware/g2
qualification generation = bp-dk-qualification/production-aware/g2
activation-intent digest
21 qualification-ticket digest
06A physical-canary receipt digest
previous V1 pointer digest
optional previous V2 pointer digest
compatibility V1 pointer digest
effective optimizer boundary
pointer digest
```

The legacy V1 pointer remains readable for existing 15/21 compatibility paths.

V1 is not silently reinterpreted as G2.

## 9. Activation transaction

06B reuses generation-neutral durability primitives from 15:

```text
managed trainer authority lock
immutable artifact storage
flush-before-commit
atomic active-file replacement
pointer history
managed restart semantics
```

G2 admission semantics remain owned by 06.

Canonical transaction:

```text
validate exact ticket/canary/candidate
 -> seal durable G2 activation intent
 -> validate expected previous V1/V2 pointer identity
 -> archive prior pointer state
 -> store exact candidate artifact
 -> stage semantic V2 pointer
 -> commit V1 compatibility pointer
 -> verify committed pointer pair
 -> seal G2 activation receipt
 -> require managed restart
```

The V1 compatibility swap remains the commit point for legacy readers, while V2 carries the explicit G2 semantic axis.

## 10. Managed restart and startup projection

The existing 15 managed launcher is extended, not replaced.

For an active V2 pointer compatible with the resolved V1 selection, it creates an immutable G2 startup-binding sidecar and transports:

```text
ASH_BP_DK_FUSION_G2_STARTUP_BINDING_PATH
ASH_BP_DK_FUSION_G2_STARTUP_BINDING_DIGEST
```

The launcher preserves the existing V1 pointer immutability guard and additionally verifies that the V2 pointer file did not change during the child run.

No hot reload or mid-generation policy mutation is introduced.

## 11. 05 runtime confirmation

05 remains the control-to-data binding authority.

Production startup scope is explicitly:

```text
AshBpDkControlDataPlaneBindingScope::Production
```

Only an exact G2 startup sidecar may set:

```text
effective_policy_generation = bp-dk-policy/production-aware/g2
effective_qualification_generation = bp-dk-qualification/production-aware/g2
```

V1-only startup continues to leave those generation axes unsealed rather than inferred.

06 runtime confirmation additionally requires Production scope. A QualificationCanary scope can never satisfy production activation confirmation.

## 12. G2 activation success boundary

Pointer commit alone is not sufficient to claim effective G2 production.

The activation chain is only runtime-confirmed when:

```text
G2 activation receipt
+
exact V1 compatibility pointer
+
exact V2 semantic pointer
+
managed restart
+
05 Production-scope runtime binding
+
explicit effective Policy G2
+
explicit effective Qualification G2
```

all agree.

## 13. Production soak health

06C begins only after runtime confirmation.

It consumes existing evidence rather than rebuilding it:

```text
05 control/data generation binding receipt
04 training-generation provenance closure
optional 03 generation completeness audit
explicit G2 soak-health policy
```

Health disposition:

```text
Healthy
ContinueSoak
RollbackRecommended
EvidenceInsufficient
Contradictory
```

`JudgmentDeferred` from 03 remains insufficient evidence.
`StaleEvidence` can recommend rollback according to the explicit health contract.
`Contradictory` remains contradictory.

Health code has no active-pointer write path.

## 14. Same-epoch health requirement

Production evidence admitted to one soak epoch must share the exact production runtime binding/activation lineage.

A canary-scope control/data receipt cannot be accepted as a production-soak receipt when exact control binding is required.

Runtime binding or activation changes require a new soak epoch.

## 15. Explicit rollback

Rollback is a separate control-plane transaction.

Health may recommend rollback but does not perform it.

Rollback requires an explicit `AshBpDkG2RollbackIntent` that binds the exact current G2 pointer and the exact historical pointer to restore.

Canonical rollback:

```text
prepare explicit rollback intent
 -> acquire managed authority lock
 -> compare current pointer identity
 -> restore archived V1 pointer
 -> restore/remove prior V2 semantic pointer as exact history requires
 -> seal rollback receipt
 -> require managed restart
```

No in-process policy swap is introduced.

## 16. State ownership

```text
21 review/ticket                     -> existing G2 review authority
06A physical canary                  -> G2 qualification evidence
06B active-pointer transaction       -> G2 PolicySelection authority
05 runtime control/data binding      -> control-to-data provenance
old Planner 05                       -> Fusion/Fission planning
02 Parameter PRE snapshot            -> parameter source identity
03 completeness audit                -> generation completeness
04 training provenance               -> training/gradient/optimizer lineage
06C soak health                      -> G2 production health evidence
06 rollback transaction              -> explicit rollback pointer authority
```

No execution mathematics authority moves into 06.

## 17. Lineage registry and vocabulary

00 registry adds:

```text
ASH-BP-DK-POLICY-R2-CLOSURE-06
family = bp-dk-policy-r2
authority = BpDkPolicyControlPlane / PolicySelection
status = Active
parent = ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
```

Vocabulary binding:

```text
owned data-plane revision = none
target data-plane revision = bp-dk-data-plane/active-fusion/v1
owned policy generation = bp-dk-policy/production-aware/g2
owned qualification generation = bp-dk-qualification/production-aware/g2
accepted qualification generations = [bp-dk-qualification/production-aware/g2]
```

The static control head can move to 06 while effective production policy remains unknown in the source tree.

The legacy static `policy_selection` authority remains 15 until actual runtime evidence proves a G2 V2 activation. The registry records G2 policy-selection capability separately.

## 18. Historical validator forward compatibility

06 exposes two generation-neutral helpers from the legacy 14 canary implementation:

```text
execute_training_branch_with_env
canary_checkpoint_authority
```

The old G1 ticket/receipt qualification authority remains unchanged.

Legacy validators 15 and 21 retain their parent byte anchors but permit this exact 06 helper exposure only when the 06 module exists and the original G1 qualification surfaces remain present.

Existing 15/16/17 G1 semantics are not rewritten.

## 19. Tooling

New validator:

```text
tools/validate_ash_bp_dk_policy_r2_closure_06.py
```

New runner:

```text
tools/run_ash_bp_dk_policy_r2_closure_06.ps1
```

CF1 order:

```text
...
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
 -> ASH-BP-DK-POLICY-R2-CLOSURE-06
```

## 20. Baked static evidence

Final source-tree evidence:

```text
ASH-LINEAGE-RECONCILIATION-00                  158 / 158 PASS
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01          306 / 306 PASS
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02 216 / 216 PASS
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03    167 / 167 PASS
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04 198 / 198 PASS
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05        92 / 92 PASS
ASH-BP-DK-POLICY-R2-CLOSURE-06                 143 / 143 PASS
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python static validators: 62 / 62 PASS
modified Python validators/registry: py_compile PASS
```

The CF1 Python list was executed in two bounded halves after the single long sequential invocation exceeded the tool timeout. Both halves passed, and the final revised 06 validator was rerun independently after its canary-scope checks were added.

## 21. Compile and physical-execution evidence boundary

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
physical G2 canary execution = not executed
managed G2 production restart = not executed
production soak execution = not executed
```

Static validation is not represented as a substitute for compilation or physical execution.

The earlier structural issue where a post-05 Active canary child lacked an exact control/data binding was identified during this bake and closed by the explicit `QualificationCanary` binding scope before packaging.

## 22. Parent diff boundary

Compared with the 05 full-applied parent, 06 changes exactly twelve code/tool files:

```text
crates/base_train/src/bp_delta_k_control_data_plane_binding.rs
crates/base_train/src/bp_delta_k_fusion_policy_candidate_canary_qualification.rs
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs
crates/base_train/src/bp_delta_k_policy_r2_closure.rs
crates/base_train/src/lib.rs

tools/ash_lineage_reconciliation_00_registry.py
tools/run_ash_bp_dk_policy_r2_closure_06.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
tools/validate_ash_bp_dk_fusion_policy_production_aware_recommendation_operator_review_adoption_21_static.py
tools/validate_ash_bp_dk_lineage_vocabulary_seal_01.py
tools/validate_ash_bp_dk_policy_r2_closure_06.py
```

No `ash_core`, WGSL, app, vendor-fork, forward/backward formula, optimizer formula, or Fusion planner mathematics source is changed by 06.

## 23. Packaging

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
 -> exactly the twelve parent-to-06 changed code/tool files

Full Applied Code ZIP
 -> complete 05 parent body with 06 applied
```

The Markdown specification remains outside both code ZIPs and is committed separately to GitHub.

## 24. Non-goals

06 does not implement:

```text
Muon runtime authority decomposition
new Fusion topology
new BP-Delta-K formula
new optimizer
new Atlas training route
hot policy reload
live active-pointer polling
automatic policy recommendation from health
implicit automatic rollback
```

## 25. Next revision

```text
ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

07 may decompose the large `ProductionMuonRuntime` into Observation / Bridge / Planning / Execution / Evidence sub-runtimes after the current control/data/training lineage is explicit.

## 26. Final seal

```text
R2 MEANS PRODUCTION-AWARE POLICY GENERATION G2
R2 DOES NOT MEAN THE HISTORICAL PHYSICAL R2A-R2E ROADMAP

21 REVIEWS
06A PHYSICALLY QUALIFIES
06B EXPLICITLY ACTIVATES
05 BINDS SELECTION TO EXECUTION
06C OBSERVES PRODUCTION HEALTH

G2 DOES NOT ENTER THROUGH A G1 QUALIFICATION TICKET
CANARY DOES NOT WRITE THE PRODUCTION POINTER
HEALTH DOES NOT WRITE THE PRODUCTION POINTER

QUALIFICATION CANARY SCOPE IS NOT PRODUCTION SCOPE

ACTIVE POINTER V2 EXPLICITLY CARRIES POLICY G2 AND QUALIFICATION G2
V1 IS NOT SILENTLY REINTERPRETED AS G2

NO LATEST-CANDIDATE FALLBACK
NO LATEST-CANARY FALLBACK
NO GENERATION INFERENCE
NO HOT RELOAD
NO LIVE POINTER POLLING
NO MID-GENERATION POLICY MUTATION

EXPLICIT TICKET
 -> EXACT CANARY
 -> EXPLICIT ACTIVATION INTENT
 -> V2 SEMANTIC POINTER
 -> V1 COMPATIBILITY COMMIT
 -> MANAGED RESTART
 -> 05 PRODUCTION-SCOPE RUNTIME CONFIRMATION
 -> SOAK HEALTH
 -> EXPLICIT ROLLBACK

IS ONE TRACEABLE PRODUCTION-AWARE POLICY G2 LINEAGE
```
