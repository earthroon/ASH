# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R3

## Parent Terminal Contract / Full Parent Evidence Binding / Manifest·Runtime Profile·Route Generation Identity / Child Admission Independence / Exact Fallback Continuity Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2
PARENT_TERMINAL_POLICY=pass-or-hold-contract-valid-v1
RUN_SCOPE=fresh-parent-rerun-plus-complete-evidence-binding-plus-independent-child-fallback-v1
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
PARENT_EVIDENCE_POLICY=manifest-closed-full-artifact-graph-binding-v1
RUNTIME_PROFILE_POLICY=canonical-path-byte-digest-and-run-immutability-v1
ROUTE_GENERATION_POLICY=parent-14-15-16-child-17-18-lineage-v1
CHILD_ADMISSION_POLICY=parent-terminal-outcome-independent-evidence-only-v1
FALLBACK_CONTINUITY_POLICY=parent-generation-16-to-child-generation-18-independent-reference-route-v1
STALE_ARTIFACT_POLICY=delete-before-run-recreate-after-run-fail-closed-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R2-R3 seals whether the complete R1-R2 terminal evidence is fresh, internally consistent, manifest-closed, runtime-profile-identical, route-generation-consistent, admission-safe, and followed by an exact independent fallback.

It does not reclassify the two R1-R2 conflicting paired units, repair the target-state lattice, alter the q99 ruler, rerun the paired statistics offline, repair the GQA4 kernel, or promote the candidate route.

The governing rule is:

```text
parent PASS is valid input when its complete PASS contract is exact
parent HOLD is valid input when its complete HOLD contract is exact
parent terminal validity determines child evidence eligibility
parent terminal success does not determine child success
```

A parent HOLD is evidence to bind, not an automatic child failure.

---

## 1. Purpose

The parent R1-R2 gate may terminate in either of two legitimate process forms:

```text
PASS token + process success + runtime pass=true + manifest pass=true
HOLD token + process failure + runtime pass=false + manifest pass=false
```

Both forms keep candidate admission closed and preserve the existing production headwise reference route.

R2-R3 closes five unresolved contracts:

1. the parent terminal result is interpreted through an exact PASS-or-HOLD matrix rather than a HOLD-only substring check;
2. the parent runtime artifact is not reduced to a handful of hard-coded counters but is bound as a complete evidence graph;
3. the parent local manifest, runtime profile bytes, artifact hashes, and route generations are tied to one fresh execution;
4. the child admission state is derived only from evidence-binding validity and never from `parent.pass` directly;
5. a new child-owned reference-route fallback proves continuity after the parent terminal generation without reusing the parent session, KV owner, scratch owner, or token domain.

---

## 2. Non-goals and frozen authority

R2-R3 must not change:

```text
kernel q99 ratio=1.40
q99 exceedance budget=0.01
paired family alpha=0.05
paired family size=24
control KVs=256,768
target KVs=384,512
Probe diagnostic passes=124928
Shadow diagnostic passes=0
full authority sessions=72
Probe sessions=8
Shadow sessions=8
total parent sessions=88
parent candidate steps=85504
parent compact tokens=85504
parent production query batches=360
parent diagnostic query batches=1952
parent queue-state records=32768
parent Shadow Reference cells=32
parent candidate route admission=closed
active global route=existing-production-headwise-reference-v1
payload readback=0
```

Forbidden in this revision:

```text
paired-unit statistical recomputation from raw samples
ConflictingEvidence reinterpretation
TargetDriftNotReproduced reinterpretation
Inconclusive collapse
threshold relaxation
alpha expansion
tail filtering
selective parent rerun
parent artifact field rewriting
parent manifest rewriting
parent failed-component deletion
parent terminal token substitution
candidate dispatch in the child gate
candidate lease issuance
candidate route activation
automatic re-entry
same-session fallback
cross-route KV reuse
```

---

## 3. Parent identity

Canonical parent identity:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2
binary=ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_r1_r2_gate
runtime schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.runtime_artifact.v1
manifest schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.local_manifest.v1
```

Canonical parent terminal tokens:

```text
PASS=PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PAIRED_NO_PROBE_SHADOW_QUEUE_STATE_EQUIVALENCE_DIAGNOSTIC_INTERFERENCE_CONTROL_STABILITY_AND_LOCALIZATION_VALIDITY_SEALED

HOLD=HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PROBE_SHADOW_INTERFERENCE_CONTROL_STABILITY_OR_LOCALIZATION_VALIDITY_NOT_PROVEN
```

The child hashes the parent executable before launch and after exit.

Required:

```text
pre-run parent binary SHA-256 == post-run parent binary SHA-256
parent binary canonical path remains under target/release
parent binary file identity does not change during execution
parent binary is not the child binary
parent response file is generated from the exact parent CLI registry
parent response file contains no child-only key
parent response file SHA-256 is retained
```

---

## 4. Fresh parent execution and stale evidence exclusion

Before launching the parent, R2-R3 removes every parent output that can satisfy the binding contract.

Required stale-set deletion:

```text
*_parent_rerun.args
*_parent_rerun.log
*_parent_binding.json
*_probe_shadow_pairs.json
*_shadow_reference_boundaries.json
*_probe_shadow_reproduction.json
*_paired_interference_units.json
*_control_kv_stability.json
*_target_kv_validity.json
*_localization_validity.json
*_admission_receipt.json
*_fallback_receipt.json
*_negative_control_outcomes.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

The 17-file required parent set is recreated only by the fresh parent process or by its canonical post-run writer path.

Required:

```text
stale required files remaining before launch=0
parent launch count=1
parent selective retry count=0
parent process PID retained
parent launch start timestamp retained
parent process end timestamp retained
all required parent files exist after process end
all required parent files are regular files
all required parent paths canonicalize under workspace/runtime/attention
path traversal count=0
symlink escape count=0
duplicate canonical path count=0
```

A crash, missing file, stale file collision, path escape, or second launch is terminal HOLD.

---

## 5. Parent terminal contract matrix

The child first reads the fresh parent runtime artifact `pass` Boolean. That Boolean selects the only legal terminal row.

| Parent artifact `pass` | Process status | Terminal line | Runtime verdict | Manifest `pass` | Manifest verdict | Contract |
|---|---|---|---|---|---|---|
| `true` | success | exact parent PASS token | exact parent PASS token | `true` | exact parent PASS token | valid PASS parent |
| `false` | failure | exact parent HOLD token | exact parent HOLD token | `false` | exact parent HOLD token | valid HOLD parent |
| any other combination | any | any | any | any | any | invalid parent |

Terminal-line authority:

```text
last non-empty parent log line after normalization must equal selected token
selected token must appear as the terminal line exactly once
opposite token must not appear as the terminal line
substring-only matching is forbidden
historical nested-parent tokens do not replace the R1-R2 terminal line
```

Process authority:

```text
output.status.success() == parent.runtime.pass
exit code retained exactly
signal termination is invalid
missing exit code on normal Windows termination is invalid
```

Manifest authority:

```text
manifest.pass == runtime.pass
manifest.verdict == runtime.verdict
manifest.failed_components == runtime.failed_components
manifest.patch_id == runtime.patch_id
manifest.parent_patch_id == runtime.parent_patch_id
```

---

## 6. Parent terminal semantic consistency

R2-R3 does not recompute paired statistics from raw timestamp samples. It does recompute the parent terminal Boolean from the already published R1-R2 evidence fields and receipts.

Parent PASS requires all published R1-R2 PASS predicates to be true:

```text
88/88 sessions
85504/85504 candidate steps
85504/85504 compact tokens
8/8 exact pairs
Probe-first=4
Shadow-first=4
Probe diagnostic passes=124928
Shadow diagnostic passes=0
production query batches=360
diagnostic query batches=1952
32768 queue-state records
32 Shadow Reference cells
24 paired units
ConflictingEvidence=0
Underpowered=0
both controls pass
both targets pass
overall localization validity pass
payload readback zero
parent fallback exact
default route unchanged
auto re-entry=0
1240/1240 parent negative controls
parent failed_components empty
```

Parent HOLD requires:

```text
at least one parent PASS predicate false
runtime pass=false
manifest pass=false
parent failed_components non-empty
selected parent HOLD token exact
candidate admission remains closed
default route remains unchanged
parent fallback remains exact unless fallback itself is the failed component
```

The current observed parent form is a valid HOLD candidate only when the fresh artifacts exactly retain:

```text
confirmed_interference_units=0
conflicting_units=2
control_256=ShadowStable
control_768=ShadowStable
target_384=TargetDriftNotReproduced
target_512=TargetDriftNotReproduced
localization_validity=LocalizationValidityInconclusive
primary_terminal_reason=LocalizationValidityInconclusiveHold
negative_control_passed=1230
negative_control_expected=1240
pass=false
```

These values are not hard-coded as the only admissible HOLD. They are named current evidence and must be bound exactly when observed.

A future fresh parent PASS or a different internally consistent parent HOLD remains admissible under the same terminal matrix.

---

## 7. Full parent evidence binding

R2-R3 binds the complete parent evidence surface instead of copying summary constants.

Required parent runtime fields:

```text
schema
patch_id
parent_patch_id
artifact_layout
atlas_group_count
atlas_groups
atlas_digest
full_sessions
probe_sessions
shadow_sessions
total_sessions
candidate_steps
compact_tokens
probe_diagnostic_passes
shadow_diagnostic_passes
production_query_batches
diagnostic_query_batches
pair_count
paired_unit_count
confirmed_interference_units
conflicting_units
control_256
control_768
target_384
target_512
localization_validity
primary_terminal_reason
secondary_terminal_reasons
final_admission_state
payload_readback_zero
fallback_exact
default_route_unchanged
negative_control_expected
negative_control_passed
pass
verdict
failed_components
```

Required parent evidence artifacts:

```text
parent_binding
probe_shadow_pairs
shadow_reference_boundaries
probe_shadow_reproduction
paired_interference_units
control_kv_stability
target_kv_validity
localization_validity
admission_receipt
fallback_receipt
negative_control_outcomes
runtime_artifact
```

The child publishes a field-level binding map:

```text
parent runtime JSON pointer
source artifact path
source artifact SHA-256
source receipt JSON pointer
observed value digest
consistency predicate
predicate result
```

Required cross-artifact relations:

```text
runtime pair_count == probe_shadow_pairs length
runtime paired_unit_count == paired_interference_units length
runtime confirmed_interference_units == count(verdict=ConfirmedProbeInterference)
runtime conflicting_units == count(verdict=ConflictingEvidence)
runtime control_256 == exact control receipt for KV 256
runtime control_768 == exact control receipt for KV 768
runtime target_384 == exact target receipt for KV 384
runtime target_512 == exact target receipt for KV 512
runtime localization_validity == exact localization receipt class
runtime primary_terminal_reason == localization receipt primary reason
runtime secondary_terminal_reasons == localization receipt secondary reasons
runtime failed_components == localization receipt failed components plus infrastructure failures under canonical ordering
runtime final_admission_state == admission receipt final_state
runtime fallback_exact == fallback receipt exact predicate
runtime negative_control_passed == inherited 940 + child-parent negative-control artifact passed count from R1-R2
```

No parent value may be silently replaced by an expected constant in the child receipt.

---

## 8. Parent atlas integrity

The parent runtime artifact uses `atlas-parallel-group-map-v1`.

R2-R3 recomputes:

```text
per-group canonical field count
per-group canonical JSON digest
group ID uniqueness
atlas group count
canonical sorted atlas digest
```

Required parent groups:

```text
identity
population
queue_state
boundaries
paired_authority
control_stability
target_validity
localization_validity
observer
admission
fallback
negative_controls
verdict
```

Required:

```text
13/13 required groups present
unknown authority group count=0
duplicate group ID count=0
group field_count exact
every group_digest recomputed exact
runtime atlas_group_count exact
runtime atlas_digest recomputed exact
```

Unknown non-authority extension groups may be retained only when explicitly marked extension and excluded from canonical authority. Silent group replacement is forbidden.

---

## 9. Manifest closure

The parent manifest is treated as an artifact graph, not a filename list.

For every manifest artifact entry:

```text
path is relative and canonical
path remains under repository root
path remains under workspace/runtime/attention for runtime evidence
SHA-256 matches bytes on disk
group exists in manifest artifact_groups
group exists in runtime atlas when authority-bearing
no duplicate path
no duplicate path with different digest
no missing file
no zero-length JSON authority artifact
JSON parses successfully
```

Manifest closure digest:

```text
sort by canonical relative path
bind path + SHA-256 + group
hash canonical sequence with SHA-256
```

Required:

```text
manifest schema exact
manifest patch ID exact
manifest parent patch ID exact
manifest artifact_group_count exact
manifest runtime_artifact_path resolves to the exact bound parent runtime artifact
all manifest-listed artifacts verified
all 12 parent authority JSON artifacts represented
17/17 required parent files independently present
manifest closure digest retained
orphan authority artifact count=0
```

The parent manifest file itself is hashed by the child and included in the child manifest. A manifest is not permitted to authenticate its own bytes recursively.

---

## 10. Runtime profile identity

The child resolves the inherited `--runtime-profile` exactly once before launching the parent.

Canonical runtime profile contract:

```text
path=canonical repository-relative path
expected current profile=specs/runtime_profile_v5_48259.toml
byte digest=SHA-256 over exact file bytes
semantic digest=SHA-256 over canonical parsed TOML
```

Required sequence:

```text
hash profile bytes before parent response-file generation
write the exact canonical profile path into parent response file
hash parent response file
launch parent once
hash profile bytes after parent exit
parse profile again after parent exit
compare semantic digest
```

Required:

```text
profile pre-byte digest == profile post-byte digest
profile pre-semantic digest == profile post-semantic digest
parent response file contains the profile path exactly once
parent response file profile path == child CLI profile path
profile file is a regular file
profile path does not escape repository root
profile mutation count=0
profile substitution count=0
```

The child emits the runtime-profile digest even when the parent artifact does not expose a top-level profile digest.

When parent pair receipts expose runtime-profile identity, every pair must match the child-computed digest. Missing optional pair-level digest is reported as unavailable, not fabricated.

---

## 11. Production route identity

The following route identities are immutable:

```text
active production route=existing-production-headwise-reference-v1
candidate route=gqa4-cluster-production-canary-v1
fallback route=existing-production-headwise-reference-v1
```

R2-R3 validates:

```text
parent runtime default_route_unchanged=true
parent admission candidate_rejections >=1
parent admission auto_reentry=0
parent fallback candidate_dispatch_count=0
parent fallback fallback_payload_dispatches=128
parent fallback route is the reference route
child candidate dispatch count=0
child candidate lease count=0
child route mutation count=0
```

Route names, route generations, and dispatch counts are separate authorities. A matching route name cannot excuse a generation mismatch.

---

## 12. Route-generation lineage

Canonical lineage:

```text
R1-R1 parent terminal generation=14
R1-R2 pair execution generation=15
R1-R2 terminal and parent fallback generation=16
R2-R3 child evidence-open generation=17
R2-R3 child terminal and child fallback generation=18
```

The child binds the parent chain from published receipts:

```text
parent binding generation=14
parent admission expected_generation=14
parent admission open_generation=15
parent admission terminal_generation=16
all Probe/Shadow production records route_generation=15
parent fallback route_generation=16
```

Child CAS:

```text
pre-generation=16
open CAS=16 -> 17
terminal CAS=17 -> 18
```

Required:

```text
no generation skip
no generation regression
no generation reuse by a new authority state
no candidate generation publication
no device-generation change
all child fallback tokens observe route_generation=18
all child fallback tokens observe device_generation=1
```

A parent PASS and a parent HOLD use the same generation lineage. Terminal outcome does not alter generation identity.

---

## 13. Device identity

R2-R3 records and binds:

```text
adapter identity
backend identity
device feature set
subgroup size
subgroup exact32 result
timestamp-query capability
shader-int64 capability
device generation
raw bridge identity
runtime handle identity receipt
```

Required:

```text
parent evidence device_generation=1
child bootstrap device_generation=1
subgroup size=32
subgroup exact32=true
required features requested and observed
no device loss between child open and fallback close
no adapter substitution
```

The child may bootstrap a fresh runtime handle set. It must bind the same adapter identity and device-generation contract; it must not claim pointer identity with the terminated parent process.

---

## 14. Parent admission binding

Legal parent final admission states are the explicit R1-R2 terminal Hold states:

```text
LocalizationValiditySealedHold
DiagnosticInterferenceConfirmedHold
MixedInterferenceAndIntrinsicDriftHold
ControlKvInstabilitySealedHold
TargetDriftNotReproducedInShadowHold
PartialLocalizationValiditySealedHold
LocalizationValidityInconclusiveHold
```

Required parent admission receipt:

```text
expected_generation=14
open_generation=15
terminal_generation=16
open_state=EligibleForProbeShadowInterferenceOnly
final_state in legal terminal Hold set
candidate_rejections >=1
auto_reentry=0
pass=true for admission mechanics
```

The admission receipt's mechanical `pass=true` means the gate closed admission correctly. It is distinct from the parent runtime's scientific `pass` Boolean.

The child must preserve both fields without collapsing them.

---

## 15. Child admission independence

Child result authority:

```text
child_pass = all parent-contract, artifact, profile, route, generation, admission, and fallback continuity predicates
```

Forbidden:

```text
child_pass = parent_pass
child_pass = parent_pass && binding_pass
child_hold = !parent_pass
child final state copied from parent final state
```

Child state machine:

```text
pre-state=<exact parent final admission state>
pre-generation=16
open-state=EligibleForParentEvidenceBindingOnly
open-generation=17
success terminal-state=ParentEvidenceBindingSealedHold
failure terminal-state=ParentEvidenceBindingInvalidHold
terminal-generation=18
```

Success behavior:

```text
parent PASS + exact binding -> child PASS, final admission Hold
parent HOLD + exact binding -> child PASS, final admission Hold
```

Failure behavior:

```text
parent PASS + invalid binding -> child HOLD
parent HOLD + invalid binding -> child HOLD
invalid parent terminal matrix -> child HOLD
```

Every child terminal state:

```text
rejects candidate lease
publishes candidate_rejections=1 or greater
publishes auto_reentry=0
leaves global default unchanged
```

---

## 16. Parent fallback binding

The child first verifies the parent fallback receipt without rerunning it inside the parent process.

Expected parent fallback configuration:

```text
token_ring_capacity=1024
route_generation=16
device_generation=1
kv_generation=0x7fff_fffd
token_sequence_base=0
seq_kv=128
telemetry_window_steps=256
```

Expected parent fallback outcome:

```text
pass=true
candidate_dispatch_count=0
fallback_payload_dispatches=128
payload_readback_count=0
per_step_host_wait_count=0
same_session_fallback_count=0
cross_route_kv_reuse_count=0
route_generation observed=16
device_generation observed=1
```

If the parent terminal failure was itself caused by fallback failure, R2-R3 cannot declare fallback continuity sealed. It remains HOLD even when the parent HOLD contract is otherwise internally consistent.

---

## 17. Independent child fallback

After successful parent binding and child CAS open, R2-R3 runs one child-owned fallback session.

Child fallback configuration:

```text
session_id=post-parent-evidence-binding-hold-fallback-128
token_ring_capacity=1024
route_generation=18
device_generation=1
kv_generation=0x7fff_fffc
token_sequence_base=0
seq_kv=128
telemetry_window_steps=256
steps=128
route=existing-production-headwise-reference-v1
```

Required ownership separation:

```text
child session ID != parent fallback session ID
child KV generation != parent fallback KV generation
child KV owner != parent fallback KV owner
child scratch owner != parent fallback scratch owner
child token domain != parent fallback token domain
same-session fallback=0
cross-route KV reuse=0
cross-generation token reuse=0
```

Required child fallback outcome:

```text
pass=true
candidate dispatcher calls=0
candidate lease count=0
fallback dispatches=128
published health tokens=128
payload readback=0
per-step host waits=0
route-generation mismatches=0
device-generation mismatches=0
sequence mismatches=0
KV ownership mismatches=0
health failures=0
```

The child fallback is executed only after parent binding succeeds. Binding failure does not permit a fallback run to launder invalid parent evidence into a child PASS.

---

## 18. Fallback continuity matrix

| Parent fallback | Parent binding | Child fallback | Child result |
|---|---|---|---|
| exact | exact | exact | PASS with `ParentEvidenceBindingSealedHold` |
| invalid | exact otherwise | any | HOLD |
| exact | invalid | not authoritative | HOLD |
| exact | exact | invalid | HOLD |
| missing | any | any | HOLD |

Continuity means:

```text
same fallback route identity
strictly advancing route generation
fresh ownership domains
zero candidate execution
zero payload readback
exact 128-step completion on both sides
```

It does not mean parent and child fallback buffers or sessions are reused.

---

## 19. Parent evidence snapshot receipt

R2-R3 emits an immutable parent terminal snapshot containing:

```text
parent terminal class=ParentPassBound or ParentHoldBound
parent process exit code
parent process success Boolean
parent terminal token
parent runtime pass
parent manifest pass
parent verdict
parent failed components
parent primary terminal reason
parent secondary terminal reasons
parent final admission state
parent negative controls passed/expected
parent binary digest
parent args digest
parent log digest
parent runtime artifact digest
parent manifest digest
parent manifest closure digest
parent atlas digest
runtime profile byte digest
runtime profile semantic digest
route-generation lineage digest
```

The receipt is a child-owned binding record. It never edits the parent files.

---

## 20. Required child runtime artifacts

R2-R3 emits:

```text
*_parent_rerun.args
*_parent_rerun.log
*_parent_terminal_contract.json
*_parent_evidence_snapshot.json
*_parent_artifact_closure.json
*_parent_manifest_closure.json
*_parent_atlas_revalidation.json
*_runtime_profile_identity.json
*_route_generation_lineage.json
*_parent_admission_binding.json
*_child_admission_receipt.json
*_fallback_continuity.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

Large maps use `atlas-parallel-group-map-v1` with independently recomputable group digests.

The child manifest includes hashes for every child artifact and hashes for the bound parent runtime artifact, parent manifest, parent response file, parent log, and runtime profile.

---

## 21. Child runtime artifact schema

```text
schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.r3.runtime_artifact.v1
manifest schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.r3.local_manifest.v1
```

Required top-level fields:

```text
schema
patch_id
parent_patch_id
artifact_layout
atlas_group_count
atlas_groups
atlas_digest
parent_terminal_class
parent_pass
parent_process_status_consistent
parent_terminal_token_exact
parent_runtime_digest
parent_manifest_digest
parent_manifest_closure_digest
parent_atlas_revalidated
parent_required_files_present
runtime_profile_path
runtime_profile_byte_digest
runtime_profile_semantic_digest
runtime_profile_immutable
parent_generation
child_open_generation
child_terminal_generation
route_lineage_exact
parent_admission_closed
child_admission_independent
parent_fallback_exact
child_fallback_exact
fallback_continuity_exact
payload_readback_zero
candidate_dispatch_zero
default_route_unchanged
negative_control_expected
negative_control_passed
pass
verdict
failed_components
```

---

## 22. Child atlas groups

Required child groups:

```text
identity
parent_binary
parent_terminal
parent_evidence
parent_artifact_closure
parent_manifest
parent_atlas
runtime_profile
route_identity
generation_lineage
parent_admission
child_admission
parent_fallback
child_fallback
fallback_continuity
negative_controls
verdict
```

Required:

```text
17/17 groups present
all group IDs unique
all field counts exact
all group digests independently recomputable
atlas digest exact
```

---

## 23. CLI contract

The explicit registry is authoritative.

### Exact-value keys, 40

```text
--gqa4-r2f-r6-r5-r1-r2-r3-parent-terminal-policy pass-or-hold-contract-valid-v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-execution-policy fresh-single-run-no-selective-retry-v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-evidence-policy manifest-closed-full-artifact-graph-binding-v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-manifest-policy canonical-path-hash-group-closure-v1
--gqa4-r2f-r6-r5-r1-r2-r3-runtime-profile-policy canonical-path-byte-digest-and-run-immutability-v1
--gqa4-r2f-r6-r5-r1-r2-r3-route-generation-policy parent-14-15-16-child-17-18-lineage-v1
--gqa4-r2f-r6-r5-r1-r2-r3-child-admission-policy parent-terminal-outcome-independent-evidence-only-v1
--gqa4-r2f-r6-r5-r1-r2-r3-fallback-continuity-policy independent-reference-route-generation-continuity-v1
--gqa4-r2f-r6-r5-r1-r2-r3-stale-artifact-policy delete-before-run-recreate-after-run-fail-closed-v1
--gqa4-r2f-r6-r5-r1-r2-r3-artifact-layout atlas-parallel-group-map-v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-patch-id ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2
--gqa4-r2f-r6-r5-r1-r2-r3-parent-runtime-schema ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.runtime_artifact.v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-manifest-schema ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r2f.r7.r6.r5.r1.r2.local_manifest.v1
--gqa4-r2f-r6-r5-r1-r2-r3-parent-pass-token PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PAIRED_NO_PROBE_SHADOW_QUEUE_STATE_EQUIVALENCE_DIAGNOSTIC_INTERFERENCE_CONTROL_STABILITY_AND_LOCALIZATION_VALIDITY_SEALED
--gqa4-r2f-r6-r5-r1-r2-r3-parent-hold-token HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PROBE_SHADOW_INTERFERENCE_CONTROL_STABILITY_OR_LOCALIZATION_VALIDITY_NOT_PROVEN
--gqa4-r2f-r6-r5-r1-r2-r3-parent-binary-name ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r6_r5_r1_r2_gate
--gqa4-r2f-r6-r5-r1-r2-r3-parent-cli-registry-id headwise-r7-r2f-r7-r6-r5-r1-r2-cli-registry-v1
--gqa4-r2f-r6-r5-r1-r2-r3-required-parent-file-count 17
--gqa4-r2f-r6-r5-r1-r2-r3-parent-full-session-count 72
--gqa4-r2f-r6-r5-r1-r2-r3-parent-probe-session-count 8
--gqa4-r2f-r6-r5-r1-r2-r3-parent-shadow-session-count 8
--gqa4-r2f-r6-r5-r1-r2-r3-parent-total-session-count 88
--gqa4-r2f-r6-r5-r1-r2-r3-parent-candidate-steps 85504
--gqa4-r2f-r6-r5-r1-r2-r3-parent-compact-tokens 85504
--gqa4-r2f-r6-r5-r1-r2-r3-parent-probe-diagnostic-passes 124928
--gqa4-r2f-r6-r5-r1-r2-r3-parent-shadow-diagnostic-passes 0
--gqa4-r2f-r6-r5-r1-r2-r3-parent-production-query-batches 360
--gqa4-r2f-r6-r5-r1-r2-r3-parent-diagnostic-query-batches 1952
--gqa4-r2f-r6-r5-r1-r2-r3-parent-pair-count 8
--gqa4-r2f-r6-r5-r1-r2-r3-parent-paired-unit-count 24
--gqa4-r2f-r6-r5-r1-r2-r3-parent-terminal-generation 16
--gqa4-r2f-r6-r5-r1-r2-r3-child-open-generation 17
--gqa4-r2f-r6-r5-r1-r2-r3-child-terminal-generation 18
--gqa4-r2f-r6-r5-r1-r2-r3-fallback-route-id existing-production-headwise-reference-v1
--gqa4-r2f-r6-r5-r1-r2-r3-child-fallback-steps 128
--gqa4-r2f-r6-r5-r1-r2-r3-child-fallback-seq-kv 128
--gqa4-r2f-r6-r5-r1-r2-r3-child-fallback-token-ring-capacity 1024
--gqa4-r2f-r6-r5-r1-r2-r3-child-fallback-telemetry-window-steps 256
--gqa4-r2f-r6-r5-r1-r2-r3-child-fallback-kv-generation 2147483644
--gqa4-r2f-r6-r5-r1-r2-r3-combined-negative-control-expected 1560
```

### Boolean keys, 64

The Boolean registry covers:

```text
parent binary and response-file identity
fresh-run and stale-output exclusion
PASS/HOLD terminal matrix
process-status equivalence
runtime and manifest identity
required-file closure
manifest path and hash closure
atlas group and digest revalidation
runtime-profile path and byte identity
runtime-profile semantic identity
runtime-profile immutability
parent population evidence
pair and queue evidence
statistical receipt structural evidence
control and target receipt evidence
localization and terminal-reason evidence
failed-component preservation
parent negative-control preservation
parent admission closure
parent route-generation lineage
parent fallback exactness
child admission independence
child CAS exactness
child fallback exactness
fallback ownership separation
zero candidate dispatch
zero payload readback
default-route immutability
artifact and manifest publication
forbidden mutation paths
```

```text
40 exact-value keys
64 Boolean keys
104 new keys total
```

No CLI key may silently default. Unknown keys, duplicate keys, omitted keys, and parent/child namespace collisions are terminal HOLD.

---

## 24. Static truth

Static extraction must prove:

```text
child binary invokes the exact R1-R2 parent binary
parent PASS and HOLD tokens are both present in the terminal matrix
last-line exact token parsing is present
substring-only terminal authority is absent
parent process success is compared to runtime pass
parent runtime and manifest pass/verdict are cross-checked
parent failed_components are preserved
17 required parent files are enumerated
manifest path canonicalization is present
manifest SHA-256 revalidation is present
parent atlas group digest recomputation is present
runtime-profile pre/post byte hashing is present
runtime-profile semantic digest is present
route generations 14/15/16/17/18 are distinct
child pass is not assigned from parent pass
child candidate execution path is absent
child candidate lease path is absent
parent fallback receipt is validated
child fallback config is explicit
child fallback route_generation=18
child fallback kv_generation=0x7fff_fffc
payload readback path is absent
same-session fallback path is absent
cross-route KV reuse path is absent
global route mutation path is absent
automatic re-entry path is absent
```

Forbidden static patterns include:

```text
if !parent_pass { return HOLD }
child_pass = parent_pass
expected_parent_token = PARENT_HOLD_TOKEN
log.contains(PARENT_HOLD_TOKEN) as sole authority
final_state = parent.final_admission_state
candidate dispatcher call from child main path
reuse(parent_fallback_config) without generation and ownership replacement
```

---

## 25. Negative controls

Thirty-two groups, ten controls each:

```text
parent binary identity
parent response-file identity
fresh execution identity
stale artifact exclusion
parent PASS/HOLD terminal matrix
parent process-status consistency
parent runtime artifact identity
parent manifest identity
required parent file set
manifest artifact graph closure
manifest path containment
parent atlas closure
runtime-profile path identity
runtime-profile byte identity
runtime-profile semantic identity
runtime-profile run immutability
parent population evidence
parent pair and queue evidence
parent statistical receipt structure
parent control evidence
parent target evidence
parent localization evidence
parent terminal-reason evidence
parent failed-component preservation
parent negative-control preservation
parent admission closure
route identity
route-generation lineage
child admission independence
parent fallback binding
child fallback exactness
final artifact and atlas integrity
```

```text
new controls=320
inherited parent authority=1240
combined expected=1560
```

The inherited 1240 parent controls are bound as parent evidence. They are not required to have passed when the parent terminal is HOLD. The child requires exact consistency between the parent's reported passed count, outcomes artifact, failed components, and parent terminal Boolean.

The 320 new R2-R3 controls must all pass.

---

## 26. PASS

R2-R3 PASS requires:

```text
exact parent binary identity
single fresh parent execution
17/17 required parent files recreated
parent terminal matrix exact for either PASS or HOLD
parent process status exact
parent runtime schema and patch identity exact
parent manifest schema and patch identity exact
parent runtime/manifest pass and verdict agreement
parent failed-component preservation exact
parent semantic terminal recomputation equals parent pass
12/12 parent authority JSON artifacts bound
parent manifest closure exact
13/13 parent atlas groups revalidated
runtime-profile path exact
runtime-profile pre/post byte digest exact
runtime-profile semantic digest exact
runtime-profile mutation count=0
parent population and counter evidence exact
parent pair, queue, control, target, localization, and terminal receipts structurally exact
parent admission remains closed
parent generations 14->15->16 exact
child CAS 16->17->18 exact
child admission independent from parent pass
parent fallback exact
child fallback 128/128 exact
child candidate dispatches=0
child candidate leases=0
payload readback=0
same-session fallback=0
cross-route KV reuse=0
default route unchanged
auto re-entry=0
320/320 new negative controls
combined evidence expected=1560
all child artifacts and atlas digests exact
```

A current parent HOLD with `1230/1240` inherited controls can therefore produce:

```text
parent_terminal=HOLD
parent_pass=false
parent_contract_valid=true
child_pass=true
child_final_admission=ParentEvidenceBindingSealedHold
```

This is the intended closure.

---

## 27. HOLD

R2-R3 remains HOLD on any:

```text
parent launch failure without valid fresh HOLD artifacts
second or selective parent rerun
stale required file survival
missing required parent file
parent binary mutation
parent CLI mismatch
terminal token mismatch
terminal line ambiguity
process/runtime pass mismatch
runtime/manifest mismatch
failed-component mismatch
parent semantic terminal recomputation mismatch
manifest path escape
manifest file hash mismatch
manifest orphan or missing authority artifact
atlas group or digest mismatch
runtime-profile path substitution
runtime-profile byte mutation
runtime-profile semantic mutation
route identity mismatch
route-generation mismatch
device-generation mismatch
parent admission reopening
child admission dependence on parent pass
candidate dispatch or lease
parent fallback invalidity
child fallback invalidity
payload readback
same-session fallback
cross-route KV reuse
global default mutation
automatic re-entry
new negative-control failure
child artifact or digest failure
```

Parent scientific HOLD by itself is not a child HOLD reason.

---

## 28. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R3_PARENT_TERMINAL_FULL_EVIDENCE_MANIFEST_RUNTIME_PROFILE_ROUTE_GENERATION_CHILD_ADMISSION_AND_FALLBACK_CONTINUITY_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R3_PARENT_TERMINAL_EVIDENCE_IDENTITY_ADMISSION_OR_FALLBACK_CONTINUITY_NOT_PROVEN
```

PASS promotes only the R2-R3 evidence-binding seal. It does not promote the GQA4 candidate route.

---

## 29. Canonical summary line

```text
[r2f-r7-r6-r5-r1-r2-r3][summary]
parent_terminal=<PASS|HOLD>
parent_pass=<true|false>
parent_contract_valid=<true|false>
parent_required_files=17/17
parent_authority_artifacts=12/12
parent_atlas_groups=13/13
parent_manifest_closed=<true|false>
runtime_profile_immutable=<true|false>
parent_generation=16/16
child_open_generation=17/17
child_terminal_generation=18/18
parent_admission_closed=<true|false>
child_admission_independent=<true|false>
parent_fallback_exact=<true|false>
child_fallback_dispatches=128/128
candidate_dispatches=0
payload_readback_zero=<true|false>
default_route_unchanged=<true|false>
parent_negative=<passed>/1240
new_negative=<passed>/320
combined_negative_visible=<passed>/1560
pass=<true|false>
```

For the current observed parent HOLD, a successful R2-R3 run should resemble:

```text
parent_terminal=HOLD
parent_pass=false
parent_contract_valid=true
parent_required_files=17/17
parent_manifest_closed=true
runtime_profile_immutable=true
parent_generation=16/16
child_open_generation=17/17
child_terminal_generation=18/18
parent_admission_closed=true
child_admission_independent=true
parent_fallback_exact=true
child_fallback_dispatches=128/128
candidate_dispatches=0
payload_readback_zero=true
default_route_unchanged=true
parent_negative=1230/1240
new_negative=320/320
combined_negative_visible=1550/1560
pass=true
```

The summary must report inherited parent failures separately from new child control failures. The aggregate `1550/1560` is evidence visibility, not the child PASS predicate. Child PASS requires `new=320/320` and exact parent terminal consistency.

---

## 30. Final seal

```text
fresh exact R1-R2 parent execution
+ PASS-or-HOLD terminal matrix
+ process/runtime/manifest terminal agreement
+ complete parent evidence snapshot
+ 17-file required parent set
+ manifest path and hash closure
+ 12 parent authority artifacts
+ 13 parent atlas groups revalidated
+ runtime-profile canonical path
+ runtime-profile byte and semantic immutability
+ parent route generations 14->15->16
+ child generations 16->17->18
+ parent admission Hold preserved
+ child admission independent from parent outcome
+ parent fallback generation 16 bound
+ fresh child fallback generation 18
+ zero candidate dispatch
+ zero candidate lease
+ zero payload readback
+ zero same-session fallback
+ zero cross-route KV reuse
+ zero global route mutation
= parent HOLD or PASS captured as exact evidence without allowing either outcome to steer child admission authority
```
