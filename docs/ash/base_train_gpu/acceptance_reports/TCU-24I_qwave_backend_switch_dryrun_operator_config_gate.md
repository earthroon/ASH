# TCU-24I — QWave Backend Switch Dry-run / Operator Config Gate

## Status

`PASS_STATIC_TCU_24I_WITH_NATIVE_TESTS_NOT_RUN`

## Scope

TCU-24I consumes the TCU-24H QWave atlas backend advisory router and creates an operator/config-gated dry-run switch proposal.

## SSOT

- Source router: `QWaveAtlasBackendRouterReport`
- Current backend pointer: `LegacyElevenBuffer`
- Proposed backend pointer: `source_router.advisory_candidate_path`
- Fallback backend pointer: `LegacyElevenBuffer`

## Guard

The following remain sealed false:

- `apply_allowed`
- `runtime_apply_allowed`
- `current_backend_pointer_mutation_allowed`
- `active_backend_mutation_allowed`
- `production_default_change_allowed`
- `direct_replacement_allowed`
- `backend_policy_mutation_allowed`
- `fastest_candidate_auto_apply_allowed`
- `tensorcube_matmul_replacement_enabled`
- `subgroup_fast_path_enabled`

## Acceptance

1. TCU-24H router report is used as the source.
2. `advisory_candidate_path` is converted only into `proposed_backend_pointer`.
3. `current_backend_pointer` remains unchanged.
4. `active_backend` remains unchanged.
5. Operator approval is dry-run only.
6. Config gate receipt is generated.
7. Pointer snapshot, proposal, gate receipt, and runtime report JSON files are emitted.
8. No production switch, runtime apply, or backend policy mutation is opened.
