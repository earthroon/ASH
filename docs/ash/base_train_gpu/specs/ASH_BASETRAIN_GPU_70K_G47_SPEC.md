# ASH-BASETRAIN-GPU-70K-G47 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G47
Explicit Promotion Execution Gate Preflight /
Execution Gate To Controlled Promotion Execution Candidate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G47 consumes the `ASH-BASETRAIN-GPU-70K-G46` explicit promotion execution gate and creates two candidate-only outputs:

1. explicit promotion execution gate preflight
2. controlled promotion execution candidate

G47 creates a preflight/candidate surface only. It does not execute route promotion, does not bind a runtime route, does not adopt a default route, and does not perform loss/backward/optimizer work.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent route promotion stability ledger: `ASH-BASETRAIN-GPU-70K-G45`
- Parent explicit promotion execution gate: `ASH-BASETRAIN-GPU-70K-G46`
- Current patch: `ASH-BASETRAIN-GPU-70K-G47`
- Next patch: `ASH-BASETRAIN-GPU-70K-G48`

## Implementation style

G47 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G47ProbeKey` enumerates the preflight and closed-boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G47FailureReason`.
- Forbidden claim patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g47_explicit_promotion_execution_gate_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g47_explicit_promotion_execution_gate_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G47_EXPLICIT_PROMOTION_EXECUTION_GATE_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_CONTROLLED_PROMOTION_EXECUTION_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_EXPLICIT_PROMOTION_EXECUTION_GATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_CONTROLLED_PROMOTION_EXECUTION_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_CONTROLLED_PROMOTION_EXECUTION_CANDIDATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G47_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- final output artifacts
- display surface artifacts
- route/default adoption artifacts
- promotion execution artifacts
- approval artifacts
- loss/backward/optimizer artifacts
- model delta/checkpoint/weight artifacts

## Allowed in G47 runtime probe

- Read G4-R2 current head freeze
- Read G45 route promotion stability ledger
- Read G46 operator review gate
- Read G46 explicit promotion execution gate
- Read G46 explicit promotion execution gate boundary audit
- Check explicit promotion execution gate acceptance
- Check operator review gate acceptance
- Create explicit promotion execution gate preflight
- Create controlled promotion execution candidate as candidate-only
- Validate state through lookup-table and match-based boundary classification
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G47

G47 must keep closed: operator auto-approval, operator approval mutation, route promotion execution, controlled promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, runtime route bind execution, final output emission, display surface writes, loss target creation, loss computation, backward, gradient materialization, optimizer state creation, optimizer execution, model delta materialization, model delta commit, checkpoint mutation, weight mutation, training claim, and model quality claim.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G47_EXPLICIT_PROMOTION_EXECUTION_GATE_PREFLIGHT_READY_NO_LOCAL_PROMOTION_EXECUTION_RUNTIME_CLAIM
```

The baked ZIP contains the G47 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` were unavailable, so no local compile claim or explicit promotion execution gate preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G47_EXPLICIT_PROMOTION_EXECUTION_GATE_PREFLIGHT
```

G47 reaches runtime PASS only when the G46 explicit promotion execution gate is accepted, the operator review gate is accepted, the execution gate boundary is accepted, an explicit promotion execution gate preflight is created, and a controlled promotion execution candidate is created as candidate-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G48
Atlas Route Bootstrap Fix /
Controlled Promotion Execution Candidate To Explicit Atlas Route Bootstrap Seal
No Silent Fallback No FreshInit Fallback No Full Tensor Load
```
