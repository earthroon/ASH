# ASH-TCU-K7N-D1R9 SPEC

## Shadow Route Exact Signature Apply

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R9_SHADOW_ROUTE_EXACT_SIGNATURE_APPLY`
- Parent execution: `d1r8-7c4b7516128d604a271a`
- Parent decision: `promote_observed_shapes_shadow_partial`
- Required whitelist count: `17`
- Required holdlist count: `4`
- PASS:

```text
PASS_ASH_TCU_K7N_D1R9_SHADOW_ROUTE_EXACT_SIGNATURE_APPLY_D1R8_WHITELIST_APPLIED_BURN_OUTPUT_AUTHORITY_PRESERVED_ROLLBACK_ARMED
```

D1R9 is the first K7N stage permitted to mutate shadow-route state. It does not grant TensorCube authoritative output.

## 2. Parent SSOT

Required D1R8 state:

```text
execution_id=d1r8-7c4b7516128d604a271a
decision=promote_observed_shapes_shadow_partial
reviewed_shape_count=21
green_shape_count=17
amber_shape_count=4
red_shape_count=0
whitelist_shape_count=17
holdlist_shape_count=4
rollback_shape_count=0
all_categories_covered=true
control_policy_band=promotion_green
s15_policy_band=promotion_amber
output_authority=burn
runtime_output_changed=false
route_mutation_authorized=false
route_mutation_count=0
```

D1R9 loads the D1R8 decision receipt, whitelist, holdlist, final seal and local manifest. Manifest immutable hashes must match current bytes.

## 3. Operator Approval

Route mutation requires an explicit approval receipt containing:

```text
approved_parent_execution_id=d1r8-7c4b7516128d604a271a
approved_action=apply_exact_signature_non_authoritative_shadow_route
approved_shape_count=17
approved_decision_digest=<D1R8 decision receipt digest>
approved_whitelist_digest=<D1R8 whitelist artifact digest>
approved_by=<operator identity>
approved_at_utc=<runtime timestamp>
```

The approval is sealed before route staging. A CLI boolean without the written and hashed approval receipt is insufficient.

## 4. Registry Ownership

D1R9 does not reuse the single-slot production `TensorCubeRouteRegistryV4` as a shape matrix.

It owns a dedicated registry:

```text
schema=ash_tensorcube_shadow_route_registry_v1
path=workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r9_shadow_route_registry_latest.json
```

This avoids contaminating candidate, default, user-visible and production route slots.

## 5. Exact Signature SSOT

Every active entry is derived from one D1R8 green whitelist signature and includes:

```text
shape_id
M/N/K
LHS logical shape and stride
RHS storage shape
RHS logical shape and stride
output shape
dtype
workgroup
dispatch
canonical K tile extent
shader digest
ABI digest
pipeline-layout digest
runtime authority
signature digest
```

Required runtime authority:

```text
ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
```

Range matching, wildcard matching, nearest-shape matching, category matching and dispatch-only matching are forbidden.

## 6. Whitelist and Holdlist

Required:

```text
whitelist entries=17
all whitelist policy bands=promotion_green
holdlist entries=4
all holdlist policy bands=promotion_amber
S15_M1_N16_K16 in holdlist=true
holdlist active route count=0
```

D1R9 does not hard-code the 17 shape IDs as a second authority. Membership comes from the D1R8 artifacts.

## 7. Route Entry Contract

Every active route entry uses:

```text
mode=exact_signature_non_authoritative_shadow
output_authority=burn
shadow_output_commit_authorized=false
production_output_commit_authorized=false
enabled=true
health=active
```

Route IDs are deterministic:

```text
ash.tensorcube.k7n.d1r9.shadow.<lowercase-shape-id>.<signature-digest-prefix>
```

Duplicate shape IDs, route IDs and signature digests are rejected.

## 8. Atomic Transaction

Apply sequence:

```text
load and verify D1R8 evidence
write operator approval
snapshot current shadow registry
write rollback snapshot
arm rollback authority
construct 17 route entries
run matcher probes
stage complete registry in memory
seal staged registry digest
publish registry atomically
increment route epoch once
reload registry from disk
verify 17 active entries and zero holdlist entries
write mutation ledger and apply receipt
```

Required epoch transition:

```text
apply: N -> N+1
route_epoch_increment_count=1
```

The 17 entries are one transaction. One through sixteen visible entries are forbidden.

## 9. Failure and Rollback

Before commit failure:

```text
active registry unchanged
route epoch unchanged
Burn-only behavior retained
```

After commit verification failure:

```text
rollback registry published
active route count=0
shadow feature disabled
rollback epoch=N+2
output_authority=burn
rollback receipt written
```

Rollback epochs remain monotonic and are never decremented.

## 10. Matcher Probes

CPU-side probes are required before commit:

```text
17 whitelist exact matches
4 holdlist skips
1 unknown-shape skip
1 stride-mismatch skip
1 shader-digest mismatch skip
1 ABI-digest mismatch skip
1 pipeline-layout mismatch skip
1 runtime-authority mismatch skip
```

The probes perform no GPU dispatch.

## 11. Runtime Shadow Contract

For exact matches:

```text
Burn path required=true
TensorCube shadow eligible=true
Burn authoritative=true
TensorCube authoritative=false
```

For holdlist, unknown or identity mismatch:

```text
Burn-only execution
TensorCube shadow skipped
skip reason recorded
```

Required isolation:

```text
same adapter=true
same device=true
same queue=true
shadow output separate=true
shadow readback sampling enabled=false
sampler substitution=false
KV-state mutation=false
shadow output commit=false
production output commit=false
```

## 12. Failure Policy

Initial sealed policy:

```text
consecutive shadow failure limit=3
rolling shadow failure rate limit=0.05
rolling shadow failure window=100
signature quarantine enabled=true
global rollback armed=true
```

A shadow failure must not fail an otherwise successful Burn request.

## 13. Output Authority

Required after apply:

```text
output_authority=burn
TensorCube authoritative output count=0
shadow output commit count=0
production output commit count=0
sampler substitution count=0
KV-state mutation count=0
runtime_output_changed=false
```

D1R9 changes route eligibility state, not downstream output ownership.

## 14. Protected State

Protected before and after:

- D1R8 manifest, decision receipt, whitelist, holdlist, policy bands and final seal
- canonical K7N WGSL
- RHS ABI
- pipeline-layout source
- Burn baseline source
- legacy route registry and ledger when present
- production defaults when present
- model-weight receipt when present

Allowed mutations:

```text
D1R9 shadow registry
D1R9 route epoch
D1R9 mutation ledger
D1R9 approval, rollback and apply artifacts
```

## 15. PASS Boundary

```text
parent evidence valid=true
operator approval valid=true
requested whitelist count=17
validated whitelist count=17
staged route count=17
applied route count=17
active route count=17
holdlist count=4
holdlist active route count=0
route transaction committed=true
route epoch increment count=1
shadow feature enabled=true
output authority=burn
shadow output commit count=0
production output commit count=0
TensorCube authoritative output count=0
rollback snapshot valid=true
rollback armed=true
runtime output changed=false
```

## 16. PASS Verdict

```text
the_d1r8_partial_shadow_decision_and_seventeen_green_exact_shape_signatures_were_verified_against_the_parent_manifest_and_operator_approval_then_applied_as_one_atomic_non_authoritative_shadow_route_transaction_with_four_amber_shapes_remaining_burn_only_the_route_epoch_incremented_once_burn_output_sampler_and_kv_authority_preserved_and_immediate_signature_and_global_rollback_armed_without_tensorcube_output_commit_or_production_authority
```

## 17. Non-Authorization

D1R9 does not authorize:

- TensorCube authoritative output
- Burn replacement
- amber or S15 shadow admission
- unobserved-shape shadow admission
- range expansion
- full-vocabulary claims
- removal of Burn fallback
- removal of rollback authority
- production readiness claims

## 18. Next State

D1R9 PASS authorizes drafting only:

```text
ASH-TCU-K7N-D1R10_SHADOW_ROUTE_RUNTIME_OBSERVATION_AND_PARITY_TELEMETRY
```

D1R10 must observe exact-match counts, holdlist and unknown skips, shadow success and failure rates, quarantine, sampled parity, GPU overhead, device loss and rollback behavior without changing Burn output authority.

## 19. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r9_shadow_route_exact_signature_apply -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r8-execution d1r8-7c4b7516128d604a271a `
  --require-d1r8-decision promote_observed_shapes_shadow_partial `
  --require-d1r8-decision-marker DECISION_ASH_TCU_K7N_D1R8_PROMOTE_OBSERVED_SHAPES_SHADOW_PARTIAL `
  --require-parent-reviewed-shape-count 21 `
  --require-parent-green-shape-count 17 `
  --require-parent-amber-shape-count 4 `
  --require-parent-red-shape-count 0 `
  --require-parent-whitelist-shape-count 17 `
  --require-parent-holdlist-shape-count 4 `
  --require-parent-rollback-shape-count 0 `
  --require-parent-control-policy-band promotion_green `
  --require-parent-s15-policy-band promotion_amber `
  --require-parent-output-authority burn `
  --operator-approval-action apply_exact_signature_non_authoritative_shadow_route `
  --operator-approval-parent-execution d1r8-7c4b7516128d604a271a `
  --operator-approval-shape-count 17 `
  --operator-approved-by operator `
  --require-whitelist-count 17 `
  --require-holdlist-count 4 `
  --require-holdlist-shape S15_M1_N16_K16 `
  --require-runtime-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-staged-route-count 17 `
  --require-route-mode exact_signature_non_authoritative_shadow `
  --require-route-output-authority burn `
  --require-shadow-output-commit-authorized false `
  --require-production-output-commit-authorized false `
  --require-holdlist-active-route-count 0 `
  --require-whitelist-exact-match-count 17 `
  --require-holdlist-skip-count 4 `
  --require-applied-route-count 17 `
  --require-route-epoch-increment-count 1 `
  --require-active-d1r9-route-count 17 `
  --set-consecutive-shadow-failure-limit 3 `
  --set-rolling-shadow-failure-rate-limit 0.05 `
  --set-rolling-shadow-failure-window 100 `
  --require-d1r8-pass `
  --require-parent-all-categories-covered `
  --require-parent-runtime-output-unchanged `
  --load-parent-decision-receipt `
  --load-parent-whitelist `
  --load-parent-holdlist `
  --load-parent-final-seal `
  --load-parent-local-manifest `
  --require-parent-digests-exact `
  --require-operator-approval `
  --record-operator-approval `
  --require-all-whitelist-cells-green `
  --require-all-holdlist-cells-amber `
  --reject-duplicate-shape-ids `
  --reject-duplicate-signature-digests `
  --reject-range-based-route-matching `
  --require-exact-shape-match `
  --require-exact-stride-match `
  --require-exact-dtype-match `
  --require-exact-workgroup-match `
  --require-exact-dispatch-match `
  --require-exact-k-tile-extent-match `
  --require-exact-shader-digest-match `
  --require-exact-abi-digest-match `
  --require-exact-pipeline-layout-digest-match `
  --create-route-registry-snapshot `
  --create-rollback-snapshot `
  --require-rollback-armed-before-commit `
  --stage-exact-signature-shadow-routes `
  --verify-route-matcher-probes `
  --require-unknown-shape-skip `
  --require-stride-mismatch-skip `
  --require-shader-digest-mismatch-skip `
  --require-abi-digest-mismatch-skip `
  --require-pipeline-layout-mismatch-skip `
  --require-runtime-authority-mismatch-skip `
  --commit-route-transaction-atomically `
  --reload-route-registry-after-commit `
  --require-unique-route-ids `
  --require-unique-active-signatures `
  --enable-exact-signature-shadow-feature `
  --require-tensorcube-production-output-disabled `
  --require-tensorcube-authoritative-route-disabled `
  --require-signature-quarantine-enabled `
  --require-global-rollback-armed `
  --require-burn-authoritative-output `
  --require-shadow-output-separate `
  --require-no-sampler-substitution `
  --require-no-kv-state-mutation `
  --require-no-shadow-output-commit `
  --require-no-production-output-commit `
  --verify-d1r8-evidence-unchanged `
  --verify-k7n-shader-unchanged `
  --verify-k7n-abi-unchanged `
  --verify-pipeline-layout-unchanged `
  --verify-burn-source-unchanged `
  --verify-model-weights-unchanged `
  --write-route-apply-receipt `
  --write-route-mutation-ledger `
  --write-output-authority-guard `
  --write-protected-state-guard `
  --write-final-seal `
  --no-runtime-output-change `
  --no-production-claim
```
