# TCU-24J — QWave Backend Apply Candidate / Current Pointer Guard

## Status
PASS_STATIC_TCU_24J_WITH_NATIVE_TESTS_NOT_RUN

## SSOT
- Source: TCU-24I QWave backend switch dry-run report.
- Added: feature-gated apply candidate record.
- Current backend pointer remains unchanged.
- Active backend remains unchanged.

## Sealed invariants
- runtime_apply_allowed = false
- current_backend_pointer_mutation_allowed = false
- active_backend_mutation_allowed = false
- production_default_change_allowed = false
- direct_replacement_allowed = false
- backend_policy_mutation_allowed = false
- fastest_candidate_auto_apply_allowed = false
- tensorcube_matmul_replacement_enabled = false
- subgroup_fast_path_enabled = false

## Completed acceptance points
1. TCU-24I dry-run report is the source.
2. Source proposed backend pointer is copied into candidate metadata only.
3. Current backend pointer is not mutated.
4. Active backend is not mutated.
5. Feature gate receipt exists.
6. Feature gate is candidate-only.
7. Current pointer guard receipt exists.
8. Rollback backend pointer is LegacyElevenBuffer.
9. Apply candidate record exists as a safe candidate-only structure.
10. Runtime apply is not performed.
